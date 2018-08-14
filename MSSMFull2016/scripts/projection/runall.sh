#!/bin/bash

#lumis=( 35.9 300 3000 )
lumis=( 300 3000 )
odir="jul31"

#modes="datacard ws limit"  #model-dep step 1
modes="limit"              #model-dep step 2
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


# for i in jul31_lumi-3*hmssm*; do echo -e `ls $i/higgsC*root | wc -l`  " "`ll -Sr $i/higgsC*root | head -1 | awk {'print $5'}` "\t  $i"; done