#!/bin/sh
#compiles and runs the model

exe_dir=$1
inputdir=$2
input_weather=$3
nml_input=$4
outputdir=$5
restart_dir=$6

date

#compile code
make --directory $exe_dir FC=gfortran

#check if the outputdir exists and else make one
if [ ! -d "$outputdir" ]; then
   mkdir $outputdir
fi

if [ -f "$restart_dir/sce_lastloop.txt" ]; then
   cp $restart_dir/* $outputdir
fi

if [ ! -d  "$inputdir" ]; then
mkdir $inputdir
cp $input_weather $inputdir
fi

#run the model 
$exe_dir/model.x -i $inputdir -o $outputdir -n $nml_input

#clean again
make clean --directory $exe_dir

date
