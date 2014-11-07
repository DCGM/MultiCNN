# Submit caffe jobs on PBS (anselm)
#
# Takes all subdirectories and submits them as an array job (NOT THE PBS ARRAY).
# Each directories has to contain a net_solver.prototxt file.
# Logs are created in your home directory.
# If you are ressuming previous training, your nets should be stored in files something_something_something_iter_102000.solverstate.
# In such case, the last solverstate is taken as a starting point for training.

TASK_LIST=tasklist
ITERATION=1

# put names of sub-directories in the current directory into a file
find . -maxdepth 1 -type d | grep / | sed 's|./||' | sort >$TASK_LIST

# Check if there is anything to process
size=$(cat $TASK_LIST | wc -l)
if [ $size -eq 0 ]; then
    echo "No configuration directories found in the current directory."
    rm $TASK_LIST
    exit 1
else
	TASK_ID=1
	# Run jobs
	while read job;
	do
		qsub -N "c${ITERATION}_${TASK_ID}" -v ITERATION=${ITERATION},TASK_ID=${TASK_ID} -k oe -j oe run.sh
		TASK_ID=$((TASK_ID+1))
	done < ${TASK_LIST}
fi

