#PBS -A IT4I-6-9
#PBS -q qnvidia
#PBS -l select=1:ncpus=16

TRAIN_DB=/scratch/ITS/binary/ilsvrc12-256_train_lmdb
VAL_DB=/scratch/ITS/binary/ilsvrc12-256_val_lmdb
MEAN_FILE=/scratch/ITS/binary/ilsvrc12-256_train_mean_lmdb

module load cuda
module load mkl
module load hdf5

# PBS Environemt variable: Directory where the qsub command was executed.
cd $PBS_O_WORKDIR

# get individual task from tasklist with index from PBS JOB ARRAY
TASK=$(sed -n "${PBS_ARRAY_INDEX}p" $PBS_O_WORKDIR/tasklist)

echo CONFIGURATION $TASK >&2
cd $TASK

# get last snapshot
LAST_SNAPSHOT=$(find . -name "*.solverstate" | sed "s/\.\///" | sort -n -t "_" -k 4 | tail -n 1)
#LAST_SNAPSHOT=`ls | grep solverstate | gawk 'BEGIN{FS="[_.]"}{print $4, $0}' | sort -n  |tail -1 |cut -f 2 -d \ `

echo "LAST_SNAPSHOT $LAST_SNAPSHOT"

SNAPSHOT_PARAM=""
#Does the snapshot exist? Then use it...
if [ -n "$LAST_SNAPSHOT" ]; then
	SNAPSHOT_PARAM="-snapshot=$LAST_SNAPSHOT"
fi

#run it
/home/psvoboda/ITS/caffe_its/build/tools/caffe train -solver=net_solver.prototxt $SNAPSHOT_PARAM >log.txt 2>&1

echo ALL_DONE $TASK  >&2

