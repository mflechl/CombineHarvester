#!/bin/bash

#lumis=( 36.9 300 3000 )
lumis=( 300 )
odir="jul03"

modes="all" #model-indep
#extra=""
extra="--symdir latest300"

#modes="datacard ws limit"  #model-dep
#extra="--model mhmod --symdir latest/"

for l in "${lumis[@]}"; do
    echo "###############################"
    run.py $modes --lumi $l --outdir $odir  --nosyst $extra
    echo "###############################"
    run.py $modes --lumi $l --outdir $odir --scale scen2 $extra
    echo "###############################"
    run.py $modes --lumi $l --outdir $odir --scale all $extra
    echo "###############################"
    run.py $modes --lumi $l --outdir $odir --scale bbb $extra
    echo "###############################"
    run.py $modes --lumi $l --outdir $odir $extra
done
