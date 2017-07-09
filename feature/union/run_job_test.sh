#! /usr/bin/env python

INPUT_PATH=/user/yangyiming/train.data
OUTPUT_PATH=/user/yangyiming/fun015/feature_test

hadoop fs -rmr $OUTPUT_PATH

#hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.2.0.jar \
#-mapper "python mapper.py 20150423 20150521" \
#-reducer "python reducer_test.py 20150423 20150521 20150521" \
#-file mapper.py \
#-file reducer_test.py \
#-file extract_feature.py \
#-file time_stamp.py \
#-file my_format.py \
#-file feature_user_8 \
#-file feature_spid_8 \
#-file feature_caid_8 \
#-file feature_browser_8 \
#-input $INPUT_PATH \
#-output $OUTPUT_PATH \
#-jobconf mapred.reduce.tasks=100
hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.2.0.jar \
-mapper "python mapper.py 20150526 20150623" \
-reducer "python reducer_test.py 20150526 20150623 20150623" \
-file mapper.py \
-file reducer_test.py \
-file extract_feature.py \
-file time_stamp.py \
-file my_format.py \
-file feature_user_9 \
-file feature_spid_9 \
-file feature_caid_9 \
-input $INPUT_PATH \
-file feature_browser_9 \
-output $OUTPUT_PATH \
-jobconf mapred.reduce.tasks=100

hadoop fs -get $OUTPUT_PATH /home/yangyiming/minglue_ctr/train/
