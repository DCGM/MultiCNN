#!/bin/bash
## -o /dev/null
## -e /dev/null
#   PE name  CPU_Number_requested
## -pe smp 8

echo START
echo WORK_DIRECTORY $WORK_DIRECTORY
echo FILE_LIST $FILE_LIST
echo SGE_TASK_ID $SGE_TASK_ID
echo CAFFE_DIR $CAFFE_DIR

export OMP_NUM_THREADS=$NSLOTS
export PATH="/homes/kazi/ihradis/bin:$CAFFE_DIR/bin:$PATH"
export LD_LIBRARY_PATH="/usr/local/share/cuda/lib64:$CAFFE_DIR/lib:$LD_LIBRARY_PATH"

echo $LD_LIBRARY_PATH
cd $WORK_DIRECTORY

CONFIG=`cat $FILE_LIST | head -n $SGE_TASK_ID | tail -n 1 `

echo CONFIG $CONFIG
echo WORK_DIRECTORY $WORK_DIRECTORY

cd $CONFIG

echo PWD `pwd`
echo start
echo TRAIN_DB $TRAIN_DB
echo VAL_DB $VAL_DB

mkdir train_db
ln -s -t ./train_db $TRAIN_DB/*
rm ./train_db/LOCK
touch ./train_db/LOCK

mkdir val_db
ln -s -t ./val_db $VAL_DB/*
rm ./val_db/LOCK
touch ./val_db/LOCK

ln -s  $MEAN_FILE ./mean.binaryproto


#ulimit -t 100000
GLOG_logtostderr=1 train_net.bin net_solver.prototxt >log.txt 2>&2

echo DONE $CONFIG