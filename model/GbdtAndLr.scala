/**
 * Created by extremor on 17-6-21.
 */
import org.apache.spark.mllib.classification.{LogisticRegressionModel, LogisticRegressionWithLBFGS}
import org.apache.spark.mllib.evaluation.MulticlassMetrics
import org.apache.spark.mllib.linalg.DenseVector
import org.apache.spark.mllib.regression.LabeledPoint
import org.apache.spark.mllib.tree.GradientBoostedTrees
import org.apache.spark.mllib.tree.configuration.{BoostingStrategy, FeatureType}
import org.apache.spark.mllib.tree.model.{DecisionTreeModel, Node}
import org.apache.spark.{SparkConf,SparkContext}
import org.apache.spark.mllib.util.MLUtils
import org.apache.spark.mllib.tree.model.GradientBoostedTreesModel
import org.apache.spark.mllib.evaluation.BinaryClassificationMetrics
import org.apache.spark.mllib.optimization.L1Updater

object GbdtAndLr {

  //get decision tree leaf's nodes
  def getLeafNodes(node:Node):Array[Int] = {
    var treeLeafNodes = new Array[Int](1)
    if (node.isLeaf){
      treeLeafNodes = treeLeafNodes.:+(node.id)
    }else{
      treeLeafNodes = treeLeafNodes ++ getLeafNodes(node.leftNode.get)
      treeLeafNodes = treeLeafNodes ++ getLeafNodes(node.rightNode.get)
    }
    treeLeafNodes
  }

  // predict decision tree leaf's node value
  def predictModify(node:Node,features:DenseVector):Int={
    val split = node.split
    if (node.isLeaf) {
      node.id
    } else {
      if (split.get.featureType != FeatureType.Continuous) {
        if (features(split.get.feature) <= split.get.threshold) {
          predictModify(node.leftNode.get,features)
        } else {
          predictModify(node.rightNode.get,features)
        }
      } else {
        if (!split.get.categories.contains(features(split.get.feature))) {
          predictModify(node.leftNode.get,features)
        } else {
          predictModify(node.rightNode.get,features)
        }
      }
    }
  }

  def trainGbdtModel(sc:SparkContext, GbdtDataDir:String, GbdtSaveDir:String, numTrees:Int): Unit ={
    val data = MLUtils.loadLibSVMFile(sc, GbdtDataDir)
    val splits = data.randomSplit(Array(0.8, 0.2))
    val training = splits(0)
    //training.cache()
    val test = splits(1)

    val boostingStrategy = BoostingStrategy.defaultParams("Classification")
    boostingStrategy.numIterations = numTrees // Note: Use more iterations in practice.
    boostingStrategy.treeStrategy.numClasses = 2
    boostingStrategy.treeStrategy.maxDepth = 6
    // Empty categoricalFeaturesInfo indicates all features are continuous.
    boostingStrategy.treeStrategy.categoricalFeaturesInfo = Map[Int, Int]()

    val gbdtModel = GradientBoostedTrees.train(training, boostingStrategy)
    gbdtModel.save(sc, GbdtSaveDir)

    // model evaluating
    val labelAndPreds = test.map { point =>
      val prediction = gbdtModel.predict(point.features)
      (prediction, point.label)
    }
    val testAcc = labelAndPreds.filter(r => r._1 == r._2).count.toDouble / test.count()
    println("Train GBDT, The 20 % Test Accuracy = " + testAcc)
    //println("Learned classification GBT model:\n" + gbdtModel.toDebugString)

  }


  def trainLrModel(sc:SparkContext, GbdtSaveDir:String,  LrDataDir:String, LrSaveDir:String, numTrees:Int): Unit ={
    val gbdtModel = GradientBoostedTreesModel.load(sc,GbdtSaveDir)

    val treeLeafArray = new Array[Array[Int]](numTrees)
    for(i<- 0.until(numTrees)){
      treeLeafArray(i) = getLeafNodes(gbdtModel.trees(i).topNode)
    }

    val newFeatureDataSets = MLUtils.loadLibSVMFile(sc, LrDataDir).map {
      case LabeledPoint(label, features) =>
        (label.toInt, features.toDense)
    }
    val newFeatureDataSet = newFeatureDataSets.map{ x =>
      var newFeature = new Array[Double](0)
      for(i<- 0.until(numTrees)){
        val treePredict = predictModify(gbdtModel.trees(i).topNode,x._2)
        val treeArray = new Array[Double]((gbdtModel.trees(i).numNodes+1)/2)
        treeArray(treeLeafArray(i).indexOf(treePredict))=1
        newFeature = newFeature ++ treeArray
      }
      (x._1, newFeature)
    }

    val newData = newFeatureDataSet.map(x=>LabeledPoint(x._1,new DenseVector(x._2)))
    //newData.saveAsTextFile("/user/jd_ad/chenyunfeng4/result/aftergbdt")
    val splits = newData.randomSplit(Array(0.8,0.2))
    val training = splits(0)
    //training.cache()
    val testing = splits(1)

    val Lr = new LogisticRegressionWithLBFGS().setNumClasses(2)
    Lr.optimizer.setUpdater(new L1Updater).setRegParam(0.1).setNumIterations(10000).setConvergenceTol(0.1)
    val LrModel = Lr.run(training)
    LrModel.save(sc, LrSaveDir)
    // Clear the prediction threshold so the model will return probabilities
    LrModel.clearThreshold
    // model evaluating
    val predictionAndLabels = testing.map { case LabeledPoint(label, features) =>
      val prediction = LrModel.predict(features)
      (prediction, label)
    }
    //predictionAndLabels.saveAsTextFile("/user/jd_ad/chenyunfeng4/result/auc")
    val metrics = new BinaryClassificationMetrics(predictionAndLabels)
    val auROC = metrics.areaUnderROC
    println("Train LR,The 20% test AUC = " + auROC)
  }

  def GbgtLrModels(sc:SparkContext, GbdtSaveDir:String, LrSaveDir:String, testDataDir:String, numTrees:Int): Unit ={
    val gbdtModel = GradientBoostedTreesModel.load(sc,GbdtSaveDir)
    val LrModel = LogisticRegressionModel.load(sc, LrSaveDir)
    val treeLeafArray = new Array[Array[Int]](numTrees)
    for(i<- 0.until(numTrees)){
      treeLeafArray(i) = getLeafNodes(gbdtModel.trees(i).topNode)
    }
    val rawFeatureDataSets = MLUtils.loadLibSVMFile(sc, testDataDir)
    val newFeatureDataSets = rawFeatureDataSets.map {
      case LabeledPoint(label, features) =>
        (label.toInt, features.toDense)
    }
    val newFeatureDataSet = newFeatureDataSets.map{ x =>
      var newFeature = new Array[Double](0)
      for(i<- 0.until(numTrees)){
        val treePredict = predictModify(gbdtModel.trees(i).topNode,x._2)
        val treeArray = new Array[Double]((gbdtModel.trees(i).numNodes+1)/2)
        treeArray(treeLeafArray(i).indexOf(treePredict))=1
        newFeature = newFeature ++ treeArray
      }
      (x._1, newFeature)
    }

    val newTestData = newFeatureDataSet.map(x=>LabeledPoint(x._1,new DenseVector(x._2)))
    // Clear the prediction threshold so the model will return probabilities
    LrModel.clearThreshold
    // model evaluating
    val predictionAndLabels = newTestData.map { case LabeledPoint(label, features) =>
      val prediction = LrModel.predict(features)
      (prediction, label)
    }
    // Instantiate metrics object
    val metrics = new BinaryClassificationMetrics(predictionAndLabels)
    val auROC = metrics.areaUnderROC
    println("GbgtLrModels ,The AUC = " + auROC)
  }
  def singleLrmodel(sc:SparkContext, LrDataDir:String, testDataDir:String): Unit ={
    val training = MLUtils.loadLibSVMFile(sc, LrDataDir)
    //training.cache()
    val testing = MLUtils.loadLibSVMFile(sc, testDataDir)

    val Lr = new LogisticRegressionWithLBFGS().setNumClasses(2)
    Lr.optimizer.setUpdater(new L1Updater).setRegParam(0.1).setNumIterations(100000).setConvergenceTol(0.1)
    val LrModel = Lr.run(training)
    LrModel.clearThreshold
    // model evaluating
    val predictionAndLabels = testing.map { case LabeledPoint(label, features) =>
      val prediction = LrModel.predict(features)
      (prediction, label)
    }
    // Instantiate metrics object
    val metrics = new BinaryClassificationMetrics(predictionAndLabels)
    val auROC = metrics.areaUnderROC
    println("The single LR,The AUC = " + auROC)
  }
  def main(args: Array[String]) {
    if (args.length != 6) {
      System.err.println("args error!!!")
      System.exit(1)
    }
    val sparkConf = new SparkConf().setAppName("GbdtAndLr")
    val sc = new SparkContext(sparkConf)


    val GbdtDataDir= args(0)
    val GbdtSaveDir= args(1)
    val LrDataDir= args(2)
    val LrSaveDir= args(3)
    val testDataDir = args(4)
    val numTrees = args(5).toInt
    trainGbdtModel(sc, GbdtDataDir, GbdtSaveDir, numTrees)
    trainLrModel(sc, GbdtSaveDir, LrDataDir, LrSaveDir, numTrees)
    GbgtLrModels(sc, GbdtSaveDir, LrSaveDir, testDataDir, numTrees)
    singleLrmodel(sc,LrDataDir,testDataDir)
    sc.stop()
  }
}


