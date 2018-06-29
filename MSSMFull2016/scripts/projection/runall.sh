#!/bin/bash

lumis=( 36.9 300 3000 )
odir="jun29"

#modes="all" #model-indep
#extra=""

modes="datacard ws limit"  #model-dep step 1
#modes="limit"              #model-dep step 2
extra="--model mhmod --symdir latest/ --lxb"

for l in "${lumis[@]}"; do
    echo "###############################"
    run.py $modes --lumi $l --outdir $odir  --nosyst $extra
    echo "###############################"
    run.py $modes --lumi $l --outdir $odir --scale scen2 $extra
    echo "###############################"
    run.py $modes --lumi $l --outdir $odir $extra
    echo "###############################"
    run.py $modes --lumi $l --outdir $odir --scale all $extra
    echo "###############################"
    run.py $modes --lumi $l --outdir $odir --scale bbb $extra
done
