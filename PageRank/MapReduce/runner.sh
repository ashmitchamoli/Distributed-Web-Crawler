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

# run map reduce job for given number of iterations
for i in $(seq 1 $ITERATIONS)
do
    echo "iteration $i"
    # check if i is odd or even
    if [ $(($i % 2)) -eq 0 ]
    then
        TEMP_INP_DIR=${HDFS_OUT}
        TEMP_OUT_DIR=${HDFS_INP}
    else
        TEMP_INP_DIR=${HDFS_INP}
        TEMP_OUT_DIR=${HDFS_OUT}
    fi

    echo "input directory: $TEMP_INP_DIR"
    echo "output directory: $TEMP_OUT_DIR"
    hadoop jar $STREAM_JAR -D mapred.reduce.tasks=3 \
                           -input ${TEMP_INP_DIR}/ \
                           -output ${TEMP_OUT_DIR}/ \
                           -mapper ${FILES}/mapper.py \
                           -file ${FILES}/mapper.py \
                           -reducer ${FILES}/reducer.py \
                           -file ${FILES}/reducer.py
    hdfs dfs -rm -r ${TEMP_INP_DIR}/
done

# if TEMP_OUT_DIR is not HDFS_OUT the copy from temp to HDFS_OUT
if [ "$TEMP_OUT_DIR" != "$HDFS_OUT" ]
then
    hdfs dfs -mkdir -p ${HDFS_OUT}/
    hdfs dfs -cp ${TEMP_OUT_DIR}/* ${HDFS_OUT}/
fi

# get results from hdfs
rm ${LOCAL_OUT_DIR}/*
hdfs dfs -get ${HDFS_OUT}/* ${LOCAL_OUT_DIR}/

# concatenate all the files into one
cat ${LOCAL_OUT_DIR}/* > ${LOCAL_OUT_DIR}/output.txt
