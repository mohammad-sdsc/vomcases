#!/bin/sh
#compiles and runs the model

exe_dir=$1
inputdir=$2
outputdir=$3
nml_input=$4

date

#compile code
make --directory $exe_dir

#run the model 
$exe_dir/model.x -i $inputdir -o $outputdir -n $nml_input

#clean again
make clean --directory $exe_dir

date
