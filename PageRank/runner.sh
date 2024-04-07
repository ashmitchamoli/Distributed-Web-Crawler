#!/usr/bin/bash

STREAM_JAR=$1
ITERATIONS=$2
LOCAL_INP_DIR="./input/"
LOCAL_OUT_DIR="./output/"
HDFS_INP="pagerank/input/"
HDFS_OUT="pagerank/output/"
FILES="./"

# put files on hdfs
hdfs dfs -rm -r ${HDFS_INP}/ ${HDFS_OUT}/
hdfs dfs -mkdir -p ${HDFS_INP}/
hdfs dfs -put ${LOCAL_INP_DIR}/* ${HDFS_INP}/

# run map reduce job
# for i in `seq 1 $ITERATIONS`; do
#     echo "iteration $i"
#     # run map reduce job
#     hap

hadoop jar $STREAM_JAR -D mapred.reduce.tasks=1 \
                       -input ${HDFS_INP}/ \
                       -output $HDFS_OUT/ \
                       -mapper ${FILES}/mapper.py \
                       -file ${FILES}/mapper.py \
                       -reducer ${FILES}/reducer.py \
                       -file ${FILES}/reducer.py

# get results from hdfs
hdfs dfs -get ${HDFS_OUT}/* ${LOCAL_OUT_DIR}/

# concatenate all the files into one
cat ${LOCAL_OUT_DIR}/* > ${LOCAL_OUT_DIR}/output.txt
