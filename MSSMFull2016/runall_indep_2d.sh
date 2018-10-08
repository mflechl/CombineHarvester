#!/bin/bash

lumis=( 3000 )
odir="oct04"

modes="datacard ws" #model-indep
#modes="all" #model-indep
#modes="allnp" #model-indep
#modes="mlfit np" #model-indep
#extra=""
extra="--symdir latest --dim2"

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
