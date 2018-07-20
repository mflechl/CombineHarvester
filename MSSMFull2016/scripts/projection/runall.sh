#!/bin/bash

lumis=( 35.9 300 3000 )
odir="jul20"

modes="datacard ws limit"  #model-dep step 1
#modes="limit"              #model-dep step 2
extra="--model mhmod --symdir latest/ --lxb"
#extra="--model hmssm --symdir latest/ --lxb"

for l in "${lumis[@]}"; do
    echo "###############################"
    run.py $modes --lumi $l --outdir $odir  --nosyst $extra
    echo "###############################"
    run.py $modes --lumi $l --outdir $odir --scale scen2 $extra
    echo "###############################"
    run.py $modes --lumi $l --outdir $odir --scale scen2 --bbb 0.0 $extra
    echo "###############################"
    run.py $modes --lumi $l --outdir $odir --scale all $extra
    echo "###############################"
    run.py $modes --lumi $l --outdir $odir --scale bbb $extra
    echo "###############################"
    run.py $modes --lumi $l --outdir $odir $extra
done
