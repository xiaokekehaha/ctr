#!/bin/bash

INPUT_PATH=/user/yangyiming/train.data
OUTPUT_PATH=/user/yangyiming/spid_train

hadoop fs -rmr $OUTPUT_PATH

hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.2.0.jar \
	-mapper "python ./mapper.py" \
	-reducer "python ./reducer.py" \
	-file mapper.py \
	-file reducer.py \
	-file my_format.py \
	-file time_stamp.py \
	-input $INPUT_PATH \
	-output $OUTPUT_PATH \
	-jobconf mapred.reduce.tasks=100
