#!/bin/sh
# Submit caffe jobs to SGE.
#
# Takes all subdirectories and submits them as an array job.
# The directories should each contain a net_sover.prototxt file.
# Specify MEAN_FILE, TRAIN_DB, VAL_DB (mean image, training database, validation database).
# Simlinks are created for all data files in the working directories.
# The Caffe spripts should use ./mean.binaryproto, ./train_db, and ./val_db.
# Set PATH and LD_LIBRARY_PATH to your version of Caffe in SGE-jobs.sh.
#
# Author: Michal Hradis
# email: ihradi@fit.vutbr.cz

FILE_LIST="tasklist"
QUE_LIST=long.q@dellgpu1
RESOURCES=ram_free=2000M,mem_free=2000M,gpu=1

CAFFE_DIR=/mnt/matylda1/hradis/CAFFE/dep

MEAN_FILE=/mnt/matylda1/its/datasets/ImageNet/binary/imagenet_mean.binaryproto
TRAIN_DB=/mnt/matylda1/its/datasets/ImageNet/binary/ILSVRC2012-256_train
VAL_DB=/mnt/matylda1/its/datasets/ImageNet/binary/ILSVRC2012-256_val

JOB_ID=CAFFE

WORK_DIRECTORY=`pwd`

# put names of all *.xml files in the current directory into a file
find . -maxdepth 1 -type d | grep / | sed 's|./||' | sort >$FILE_LIST

# Check if there is anything to process
size=`wc -l $FILE_LIST | cut -d \  -f 1`
if [ $size -eq 0 ]; then
    echo "No configuration directories found in the current directory."
    rm $FILE_LIST
    exit 1
fi

qsub -q $QUE_LIST -t 1-$size -N $JOB_ID -l $RESOURCES -v WORK_DIRECTORY=$WORK_DIRECTORY,FILE_LIST=$FILE_LIST,CAFFE_DIR=$CAFFE_DIR,MEAN_FILE=$MEAN_FILE,TRAIN_DB=$TRAIN_DB,VAL_DB=$VAL_DB ./SGE-jobs.sh

