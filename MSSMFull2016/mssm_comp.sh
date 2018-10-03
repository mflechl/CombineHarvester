#!/bin/bash

#in "output"
#first do
#for i in jul5*; do cp -p $i/mssm_mhmod_cmb.png mssm_mhmod_$i.png; cp -p $i/asymptotic_grid.root asymptotic_grid_$i.root; done

pas=1

od="mssmplots/"
lbl="Internal"

if [ "$pas" == "1" ]; then
    od="mssmplots_pas/"
#    lbl="Preliminary Simulation"
#    lbl="Internal"
    lbl="Projection"
fi


function plotscen {

  #plotscen ${tag[$i]} ${lab[$i]} ${name[$i]} ${fn[$i]}
echo $1 $2 $3 $4

for i in ${1}*${3}*; do 
#    cp -p $i/mssm_mhmod_cmb.png ${od}mssm_mhmod_$i.png; cp -p $i/asymptotic_grid.root ${od}asymptotic_grid_$i.root; 
    cp -p $i/asymptotic_grid_*.root ${od} 
done


yrange=""
if [ "${3}" == "tauphobic" ]; then
    yrange="--y-range 1,50"
fi


#S2
   sl="${2}"
   if [ "${pas}" != "1" ]; then
       sl="${2} scenario, S2"
   fi
   python ../scripts/projection/compareLimitMSSM.py ${od}asymptotic_grid_${1}_lumi-35.9_scale-scen2_${3}.root --scenario-label="${sl}" --output="${od}mssm_${3}_${1}_scen2" --cms-sub="${lbl}" --contours="exp-2,exp-1,exp0,exp+1,exp+2" --x-range 90,2000 $yrange --model_file=/afs/cern.ch/work/m/mflechl/mssm_asymgrid/CMSSW_7_4_7/src/CombineHarvester/MSSMFull2016/shapes/Models/${4}_13TeV.root --extra_contour_file=${od}asymptotic_grid_${1}_lumi-300.0_scale-scen2_${3}.root,${od}asymptotic_grid_${1}_lumi-3000.0_scale-scen2_${3}.root --extra_contour_title='300 fb^{-1}','3000 fb^{-1}' --extra_contour_style=2,2 --extra_contour_color=4,2 | grep -v "has.*points\|Two of these three"

if [ "$pas" == "1" ]; then
    return
fi

#S2, no bbb
   python ../scripts/projection/compareLimitMSSM.py ${od}asymptotic_grid_${1}_lumi-35.9_scale-scen2_nobbb_${3}.root --scenario-label="${2} scenario, S2 (no bbb)" --output="${od}mssm_${3}_${1}_scen2_nobbb" --cms-sub="${lbl}" --contours="exp-2,exp-1,exp0,exp+1,exp+2" --x-range 90,2000 $yrange --model_file=/afs/cern.ch/work/m/mflechl/mssm_asymgrid/CMSSW_7_4_7/src/CombineHarvester/MSSMFull2016/shapes/Models/${4}_13TeV.root --extra_contour_file=${od}asymptotic_grid_${1}_lumi-300.0_scale-scen2_nobbb_${3}.root,${od}asymptotic_grid_${1}_lumi-3000.0_scale-scen2_nobbb_${3}.root --extra_contour_title='300 fb^{-1}','3000 fb^{-1}' --extra_contour_style=2,2 --extra_contour_color=4,2 | grep -v "has.*points\|Two of these three"

if [ "${3}"=="tauphobic" ] || [ "${3}"=="lightstau" ]; then return; fi

#No scaling
    python ../scripts/projection/compareLimitMSSM.py ${od}asymptotic_grid_${1}_lumi-35.9_${3}.root --scenario-label="${2} scenario, no scaling" --output="${od}mssm_${3}_${1}_noscale" --cms-sub="${lbl}" --contours="exp-2,exp-1,exp0,exp+1,exp+2" --x-range 90,2000 $yrange --model_file=/afs/cern.ch/work/m/mflechl/mssm_asymgrid/CMSSW_7_4_7/src/CombineHarvester/MSSMFull2016/shapes/Models/${4}_13TeV.root --extra_contour_file=${od}asymptotic_grid_${1}_lumi-300.0_${3}.root,${od}asymptotic_grid_${1}_lumi-3000.0_${3}.root --extra_contour_title='300 fb^{-1}','3000 fb^{-1}' --extra_contour_style=2,2 --extra_contour_color=4,2 | grep -v "has.*points\|Two of these three"

#all
    python ../scripts/projection/compareLimitMSSM.py ${od}asymptotic_grid_${1}_lumi-35.9_scale-all_${3}.root --scenario-label="${2} scenario, all scaled" --output="${od}mssm_${3}_${1}_all" --cms-sub="${lbl}" --contours="exp-2,exp-1,exp0,exp+1,exp+2" --x-range 90,2000 $yrange --model_file=/afs/cern.ch/work/m/mflechl/mssm_asymgrid/CMSSW_7_4_7/src/CombineHarvester/MSSMFull2016/shapes/Models/${4}_13TeV.root --extra_contour_file=${od}asymptotic_grid_${1}_lumi-300.0_scale-all_${3}.root,${od}asymptotic_grid_${1}_lumi-3000.0_scale-all_${3}.root --extra_contour_title='300 fb^{-1}','3000 fb^{-1}' --extra_contour_style=2,2 --extra_contour_color=4,2 | grep -v "has.*points\|Two of these three"

#bbb
    python ../scripts/projection/compareLimitMSSM.py ${od}asymptotic_grid_${1}_lumi-35.9_scale-bbb_${3}.root --scenario-label="${2} scenario, bbb scaled" --output="${od}mssm_${3}_${1}_bbb" --cms-sub="${lbl}" --contours="exp-2,exp-1,exp0,exp+1,exp+2" --x-range 90,2000 $yrange --model_file=/afs/cern.ch/work/m/mflechl/mssm_asymgrid/CMSSW_7_4_7/src/CombineHarvester/MSSMFull2016/shapes/Models/${4}_13TeV.root --extra_contour_file=${od}asymptotic_grid_${1}_lumi-300.0_scale-bbb_${3}.root,${od}asymptotic_grid_${1}_lumi-3000.0_scale-bbb_${3}.root --extra_contour_title='300 fb^{-1}','3000 fb^{-1}' --extra_contour_style=2,2 --extra_contour_color=4,2 | grep -v "has.*points\|Two of these three"

#no syst
    python ../scripts/projection/compareLimitMSSM.py ${od}asymptotic_grid_${1}_lumi-35.9_nosyst_${3}.root --scenario-label="${2} scenario, no systematics" --output="${od}mssm_${3}_${1}_nosyst" --cms-sub="${lbl}" --contours="exp-2,exp-1,exp0,exp+1,exp+2" --x-range 90,2000 $yrange --model_file=/afs/cern.ch/work/m/mflechl/mssm_asymgrid/CMSSW_7_4_7/src/CombineHarvester/MSSMFull2016/shapes/Models/${4}_13TeV.root --extra_contour_file=${od}asymptotic_grid_${1}_lumi-300.0_nosyst_${3}.root,${od}asymptotic_grid_${1}_lumi-3000.0_nosyst_${3}.root --extra_contour_title='300 fb^{-1}','3000 fb^{-1}' --extra_contour_style=2,2 --extra_contour_color=4,2 | grep -v "has.*points\|Two of these three"

}

cd output
mkdir -p ${od}

tag=( "jul31"         "jul31"  "aug03" "aug03" )
lab=( "m_{h}^{mod+}"  "hMSSM" "tau-phobic" "light-stau" )
name=( "mhmod"        "hmssm" "tauphobic"  "lightstau" )
fn=(   "mhmodp_mu200" "hMSSM" "tauphobic" "lightstau1" )

for i in `seq 0 3`; do
#for i in `seq 1 1`; do
    plotscen ${tag[$i]} ${lab[$i]} ${name[$i]} ${fn[$i]}
done

