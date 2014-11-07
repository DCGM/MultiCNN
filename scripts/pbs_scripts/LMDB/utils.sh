#!/bin/bash

function log()
{
	echo "${*}"
}

function die()
{
	log "${*}"
	echo "${*}" >&2
	exit -1
}

function run()
{
	log "run: '${*}'"
	eval $@ || die "run: $@ failed"
}

function prolog()
{
	module load cuda
	module load mkl
	module load hdf5
}

# Global variables, updated paths

# Number of iterations
export ITERATION_SIZE=5

# Caffe path
PATH=/home/psvoboda/ITS/caffe_its/build/tools:$PATH
export PATH

# User libraries
LD_LIBRARY_PATH=/home_lustre/psvoboda/apps/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH

