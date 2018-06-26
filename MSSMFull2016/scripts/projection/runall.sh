#!/bin/bash

lumis=( 36.9 300 3000 )
odir="jun15"

#modes="all" #model-indep
#extra=""

modes="datacard ws limit"  #model-dep
extra="--model mhmod --symdir latest/"

for l in "${lumis[@]}"; do
    echo "###############################"
    run.py $modes --lumi $l --outdir $odir  --nosyst $extra
    echo "###############################"
    run.py $modes --lumi $l --outdir $odir $extra
    echo "###############################"
    run.py $modes --lumi $l --outdir $odir --scale all $extra
    echo "###############################"
    run.py $modes --lumi $l --outdir $odir --scale bbb $extra
done
