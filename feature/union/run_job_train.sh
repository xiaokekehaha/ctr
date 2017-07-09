#!/bin/bash

train_start=("20150101" "20150115" "20150129" "20150212" "20150226" "20150312" "20150326" "20150409" "20150423")
train_end11=("20150129" "20150212" "20150226" "20150312" "20150326" "20150409" "20150423" "20150507" "20150521")
test_end111=("20150206" "20150220" "20150306" "20150320" "20150404" "20150417" "20150501" "20150515" "20150529")

for i in $(seq 0 8);do
	INPUT_PATH=/user/yangyiming/train.data
	OUTPUT_PATH=/user/yangyiming/fun/feature_$i

	hadoop fs -rmr $OUTPUT_PATH

	hadoop jar $HADOOP_HOME/share/hadoop/tools/lib/hadoop-streaming-2.2.0.jar \
		-mapper "python mapper.py ${train_start[i]} ${test_end111[i]}" \
		-reducer "python reducer.py ${train_start[i]} ${train_end11[i]} ${test_end111[i]} $i" \
		-file mapper.py \
		-file reducer.py \
		-file extract_feature.py \
		-file time_stamp.py \
		-file my_format.py \
		-file feature_user_$i \
		-file feature_spid_$i \
		-file feature_caid_$i \
		-file feature_browser_$i \
		-input $INPUT_PATH \
		-output $OUTPUT_PATH \
		-jobconf mapred.reduce.tasks=100

	hadoop fs -get $OUTPUT_PATH /home/yangyiming/minglue_ctr/train/

done
