#!/bin/bash

INPUT_PATH=/user/jd_ad/chenyunfeng4/ctr_predict/data/train.data
OUTPUT_PATH=/user/jd_ad/chenyunfeng4/ctr_predict/data/browser_train

hadoop fs -rmr $OUTPUT_PATH

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.7.1.jar \
	-mapper "python ./mapper.py" \
	-reducer "python ./reducer.py" \
	-file mapper.py \
	-file reducer.py \
	-file my_format.py \
	-file time_stamp.py \
	-input $INPUT_PATH \
	-output $OUTPUT_PATH \
	-jobconf mapred.reduce.tasks=100
