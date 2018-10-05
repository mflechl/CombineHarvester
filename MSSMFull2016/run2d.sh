#!/bin/bash

ind=(     0    1    2   3    4    5    6    7    8    9   10   11   12   13   14   15   16   17   18   19   20   21   22   23   24   25   26   27   28 )
masses=( 90  100  110 120  125  130  140  160  180  200  250  350  400  450  500  600  700  800  900 1000 1200 1400 1600 1800 2000 2300 2600 2900 3200 )
split=(  100 100  100 100  100  100  100  100  100  100   70   70   70   70   70   70   70   70   70   60   60   60   60   60   60   80   80   80   80  )

do_fr=0
do_to=${#masses[@]}

if [ $# -ge 1 ]; then
    do_fr=$1
    do_to=$1
fi
if [ $# -ge 2 ]; then
    do_to=$2
fi

#masses=( 700 )
p="output/oct04_lumi-3000.0_scale-scen2/cmb"

ctr=-1
for m in ${masses[@]}; do
  let ctr=$ctr+1
  if [ $ctr -lt $do_fr ]; then continue; fi
  if [ $ctr -gt $do_to ]; then continue; fi
  combineTool.py -m $m -M MultiDimFit --boundlist input/mssm_ggH_bbH_2D_boundaries_both_3000fb.json --setPhysicsModelParameters r_ggH=0,r_bbH=0,lumi=83.57 --redefineSignalPOIs r_ggH,r_bbH -d ${p}/ws.root --there --algo grid --points 40000 --robustFit 1 --minimizerTolerance 0.001 --minimizerStrategy 0 --cminPreScan --X-rtd OPTIMIZE_BOUNDS=0 --startFromPreFit 1 --cminFallbackAlgo "Minuit2,migrad,0:0.01" --cminFallbackAlgo "Minuit2,migrad,0:0.2" --freezeNuisances lumi --floatAllNuisances 1 --split-points ${split[$ctr]} -t -1 -n ".ggH-bbH-split.POINTS.40k.DataBase.NoSMHinBG_3000fb_Asimov.v1" --job-mode lxbatch --sub-opts '-q 1nd' --task-name oct5_m${m}
done

#combineTool.py -m $m -M MultiDimFit --boundlist input/mssm_ggH_bbH_2D_boundaries_both_3000fb.json --setPhysicsModelParameters r_ggH=0,r_bbH=0,lumi=83.57 --redefineSignalPOIs r_ggH,r_bbH -d ${p}/ws.root --there --algo grid --points 40000 --robustFit 1 --minimizerTolerance 0.001 --minimizerStrategy 0 --cminPreScan --X-rtd OPTIMIZE_BOUNDS=0 --startFromPreFit 1 --cminFallbackAlgo "Minuit2,migrad,0:0.01" --cminFallbackAlgo "Minuit2,migrad,0:0.2" --freezeNuisances lumi --floatAllNuisances 1 --split-points 500 -t -1 -n ".ggH-bbH-split.POINTS.40k.DataBase.NoSMHinBG_Asimov.v1" --job-mode lxbatch --sub-opts '-q 1nd' --task-name oct4_m${m}

#combineTool.py -m 700 -M MultiDimFit --boundlist ../input/mssm_ggH_bbH_2D_boundaries_SMHbkg_both.json --setPhysicsModelParameters r_ggH=0,r_bbH=0,lumi=1 --redefineSignalPOIs r_ggH,r_bbH -d ../ws.root --there --algo grid --points 40000 --robustFit 1 --minimizerTolerance 0.001 --minimizerStrategy 0 --cminPreScan --X-rtd OPTIMIZE_BOUNDS=0 --startFromPreFit 1 --cminFallbackAlgo "Minuit2,migrad,0:0.01" --cminFallbackAlgo "Minuit2,migrad,0:0.2" --freezeNuisances lumi --floatAllNuisances 1 --split-points 500 -t -1 -n ".ggH-bbH-split.POINTS.40k.DataBase.NoSMHinBG_Asimov.v1" --job-mode lxbatch --sub-opts '-q 1nd' --task-name oct3_m700
