#!/bin/bash

#lumis=( 35.9 300 3000 )
lumis=( 6000 )
odir="oct28"

modes="all"
#modes="all mlfit" #model-indep
#modes="allnp" #model-indep
#modes="mlfit np" #model-indep
#extra=""
extra="--symdir latest"

for l in "${lumis[@]}"; do
    echo "###############################"
#    run.py $modes --lumi $l --outdir $odir  --nosyst $extra
    echo "###############################"
    run.py $modes --lumi $l --outdir $odir --scale scen2 $extra
    echo "###############################"
#    run.py $modes --lumi $l --outdir $odir --scale all $extra
    echo "###############################"
#    run.py $modes --lumi $l --outdir $odir --scale bbb $extra
    echo "###############################"
#    run.py $modes --lumi $l --outdir $odir $extra
    echo "###############################"
#    run.py $modes --lumi $l --outdir $odir --scale scen2 --bbb 0.0 $extra
done
