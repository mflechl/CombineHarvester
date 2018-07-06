#for i in jun28*; do cp -p $i/mssm_mhmod_cmb.png mssm_mhmod_$i.png; cp -p $i/asymptotic_grid.root asymptotic_grid_$i.root; done

#in "output"
#first do
#for i in jul05*; do cp -p $i/mssm_mhmod_cmb.png mssm_mhmod_$i.png; cp -p $i/asymptotic_grid.root asymptotic_grid_$i.root; done
#for i in jul06*; do cp -p $i/mssm_mhmod_cmb.png mssm_mhmod_$i.png; cp -p $i/asymptotic_grid.root asymptotic_grid_$i.root; done


tag1="jul06"
tag2="jul05"

#no scaling
python ../scripts/projection/compareLimitMSSM.py asymptotic_grid_${tag1}_lumi-35.9.root --scenario-label="m_{h}^{mod+} scenario, no scaling" --output="mssm_mhmod_noscale" --title-right="35.9 fb^{-1}" --cms-sub="Internal" --contours="exp-2,exp-1,exp0,exp+1,exp+2" --x-range 90,2000 --model_file=/afs/cern.ch/work/m/mflechl/mssm_asymgrid/CMSSW_7_4_7/src/CombineHarvester/MSSMFull2016/shapes/Models/mhmodp_mu200_13TeV.root --extra_contour_file=asymptotic_grid_${tag2}_lumi-300.0.root,asymptotic_grid_${tag2}_lumi-3000.0.root --extra_contour_title='300 fb^{-1}','3000 fb^{-1}' --extra_contour_style=2,2 --extra_contour_color=4,2

#S2
python ../scripts/projection/compareLimitMSSM.py asymptotic_grid_${tag1}_lumi-35.9_scale-scen2.root --scenario-label="m_{h}^{mod+} scenario, S2" --output="mssm_mhmod_scen2" --title-right="35.9 fb^{-1}" --cms-sub="Internal" --contours="exp-2,exp-1,exp0,exp+1,exp+2" --x-range 90,2000 --model_file=/afs/cern.ch/work/m/mflechl/mssm_asymgrid/CMSSW_7_4_7/src/CombineHarvester/MSSMFull2016/shapes/Models/mhmodp_mu200_13TeV.root --extra_contour_file=asymptotic_grid_${tag2}_lumi-300.0_scale-scen2.root,asymptotic_grid_${tag2}_lumi-3000.0_scale-scen2.root --extra_contour_title='300 fb^{-1}','3000 fb^{-1}' --extra_contour_style=2,2 --extra_contour_color=4,2

#all
python ../scripts/projection/compareLimitMSSM.py asymptotic_grid_${tag1}_lumi-35.9_scale-all.root --scenario-label="m_{h}^{mod+} scenario, all scaled" --output="mssm_mhmod_all" --title-right="35.9 fb^{-1}" --cms-sub="Internal" --contours="exp-2,exp-1,exp0,exp+1,exp+2" --x-range 90,2000 --model_file=/afs/cern.ch/work/m/mflechl/mssm_asymgrid/CMSSW_7_4_7/src/CombineHarvester/MSSMFull2016/shapes/Models/mhmodp_mu200_13TeV.root --extra_contour_file=asymptotic_grid_${tag2}_lumi-300.0_scale-all.root,asymptotic_grid_${tag2}_lumi-3000.0_scale-all.root --extra_contour_title='300 fb^{-1}','3000 fb^{-1}' --extra_contour_style=2,2 --extra_contour_color=4,2

#bbb
python ../scripts/projection/compareLimitMSSM.py asymptotic_grid_${tag1}_lumi-35.9_scale-bbb.root --scenario-label="m_{h}^{mod+} scenario, bbb scaled" --output="mssm_mhmod_bbb" --title-right="35.9 fb^{-1}" --cms-sub="Internal" --contours="exp-2,exp-1,exp0,exp+1,exp+2" --x-range 90,2000 --model_file=/afs/cern.ch/work/m/mflechl/mssm_asymgrid/CMSSW_7_4_7/src/CombineHarvester/MSSMFull2016/shapes/Models/mhmodp_mu200_13TeV.root --extra_contour_file=asymptotic_grid_${tag2}_lumi-300.0_scale-bbb.root,asymptotic_grid_${tag2}_lumi-3000.0_scale-bbb.root --extra_contour_title='300 fb^{-1}','3000 fb^{-1}' --extra_contour_style=2,2 --extra_contour_color=4,2

#no syst
python ../scripts/projection/compareLimitMSSM.py asymptotic_grid_${tag1}_lumi-35.9_nosyst.root --scenario-label="m_{h}^{mod+} scenario, no systematics" --output="mssm_mhmod_nosyst" --title-right="35.9 fb^{-1}" --cms-sub="Internal" --contours="exp-2,exp-1,exp0,exp+1,exp+2" --x-range 90,2000 --model_file=/afs/cern.ch/work/m/mflechl/mssm_asymgrid/CMSSW_7_4_7/src/CombineHarvester/MSSMFull2016/shapes/Models/mhmodp_mu200_13TeV.root --extra_contour_file=asymptotic_grid_${tag2}_lumi-300.0_nosyst.root,asymptotic_grid_${tag2}_lumi-3000.0_nosyst.root --extra_contour_title='300 fb^{-1}','3000 fb^{-1}' --extra_contour_style=2,2 --extra_contour_color=4,2

