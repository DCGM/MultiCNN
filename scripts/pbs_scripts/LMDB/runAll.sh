# Submit caffe jobs on PBS (anselm)
#
# Takes all subdirectories and submits them as an array job.
# The directories should each contain a net_solver.prototxt file.
# Logs are created in your home directory.
# If you are ressuming previous training, your nets should be stored in files something_something_something_iter_102000.solverstate.
# In such case, the last solverstate is taken as a starting point for training.
#
# Your .bash_profile should contain (or the environment should be setup correctly some other way):
# export PATH=/home/psvoboda/ITS/caffe_its/tools:$PATH
# export LD_LIBRARY_PATH=/home_lustre/psvoboda/apps/lib:$LD_LIBRARY_PATH


TASK_LIST=tasklist

# put names of sub-directories in the current directory into a file
find . -maxdepth 1 -type d | grep / | sed 's|./||' | sort >$TASK_LIST


# Check if there is anything to process
size=$(cat $TASK_LIST | wc -l)
if [ $size -eq 0 ]; then
    echo "No configuration directories found in the current directory."
    rm $TASK_LIST
    exit 1
else
	# Run job
	qsub -N Caffe_a -J 1-$size -k oe -j oe run.sh
fi

