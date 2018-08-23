#!/bin/bash

if [ "$1" == "" ]; then exit; fi

lumis=( 3000 300 35.9 )
#lumis=( 300 35.9 )
#odir="aug03"
odir="jul31"

#modes="datacard ws limit"  #model-dep step 1
modes="limit"              #model-dep step 2
extra="--model ${1} --symdir latest_${1}/ --lxb"

for l in "${lumis[@]}"; do
    echo "###############################"
#    run.py $modes --lumi $l --outdir $odir  --nosyst $extra
    echo "###############################"
    run.py $modes --lumi $l --outdir $odir --scale scen2 $extra
#    echo "###############################"
#    run.py $modes --lumi $l --outdir $odir --scale scen2 --bbb 0.0 $extra
    echo "###############################"
#    run.py $modes --lumi $l --outdir $odir --scale all $extra
    echo "###############################"
#    run.py $modes --lumi $l --outdir $odir --scale bbb $extra
    echo "###############################"
#    run.py $modes --lumi $l --outdir $odir $extra
done


# for i in jul31_lumi-3*hmssm*; do echo -e `ls $i/higgsC*root | wc -l`  " "`ll -Sr $i/higgsC*root | head -1 | awk {'print $5'}` "\t  $i"; done
