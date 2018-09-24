#!/usr/bin/python

import argparse
import os
import sys
from time import localtime, strftime

CMSSW_BASE=os.environ['CMSSW_BASE']
rundir=CMSSW_BASE+'/src/CombineHarvester/MSSMFull2016/'
mdir=strftime("%Y-%m-%d_%Hh%Mm%S", localtime())
physdir=rundir+'output/'+mdir+'/'
symdir='latest/'
basedir=rundir+'output/'+symdir
logfile=basedir+'log.txt'

baselumi=35.9
#baselumi=36.9
dryrun=False

def main(argv):

  global mdir,physdir
  global loglevel
  global symdir,basedir,logfile

  parser = argparse.ArgumentParser(description='Steer the projection')
  parser.add_argument('mode', nargs='*',                       default=['all'], choices=['all','allnp','datacard','ws','limit','mlfit','np'],     help='Mode of operation')
  parser.add_argument('--lumi',     dest='lumi',   type=float, default=baselumi,                                      help='Luminosity in fb-1')
  parser.add_argument('--nosyst',   dest='syst', nargs='?',    default=True, const=False,                             help='Flag to disable ystematics')
  parser.add_argument('--scale',    dest='scale',              default='none',  choices=['all','bbb','scen2','none'], help='Scaling of uncertainties. Options: all, bbb, scen2, none')
  parser.add_argument('--bbb',      dest='bbb', type=float,    default=0.4,                                           help='BinByBin threshold. 0 for none; default: 0.4')
  parser.add_argument('--model',    dest='model',              default='none',  choices=['mhmod','hmssm','lightstau','lightstop','lowtb','tauphobic','none'],     help='Model-(in)dependent limits. Options: none, mhmod, hmssm, lightstau,lightstop,lowtb,tauphobic')
  parser.add_argument('--loglevel', dest='loglevel', type=int, default=1,                                             help='Verbosity, 0-essential, 1-most commands, 2-all commands')
  parser.add_argument('--outdir',   dest='outdir',             default=mdir,                                          help='root of output dir name (default: date/time)')
  parser.add_argument('--symdir',   dest='symdir',             default='latest/',                                     help='Symlink of output dir (change when running parallel!)')
  parser.add_argument('--dim2',     dest='dim2', nargs='?',    default=False, const=True,                             help='Do 2D limits (only for model-independent)')
  parser.add_argument('--dryrun',   dest='dryrun', nargs='?',  default=False, const=True,                             help='Dry run, do not execute commands')
  parser.add_argument('--lxb',      dest='lxb', nargs='?',     default=False, const=True,                             help='Run on lxbatch (AsymptoticGrid)')

  args = parser.parse_args()

  lumiscale=round(args.lumi/baselumi,2)
  cme='13' if (lumiscale>3) else '13'  #14 does not work yet

  syst=args.syst
  scale=args.scale
  loglevel=args.loglevel
  model=args.model
  dim2=args.dim2
#  mdir+='_lumi-'+str(args.lumi)
  customdir=False
  if mdir != args.outdir:
    customdir=True
  mdir=args.outdir+'_lumi-'+str(args.lumi)
  if not syst: mdir+='_nosyst'
  if not scale=='none': mdir+='_scale-'+scale
  if args.bbb<0.0001: mdir+='_nobbb'
  if not model=='none': mdir+='_'+model
  physdir=rundir+'output/'+mdir+'/'

  symdir=args.symdir
  if not symdir.endswith('/'): symdir+='/'
  basedir=rundir+'output/'+symdir
  logfile=basedir+'log.txt'

  global dryrun
  dryrun=args.dryrun
  lxb=args.lxb

  if 'allnp' in args.mode:
    args.mode.remove('allnp')
    args.mode.append('datacard')
    args.mode.append('ws')
    args.mode.append('limit')
    args.mode.append('mlfit')
    args.mode.append('np')

  if 'all' in args.mode:
    args.mode.remove('all')
    args.mode.append('datacard')
    args.mode.append('ws')
    args.mode.append('limit')

  if customdir or 'datacard' in args.mode:
    create_output_dir()

  make_print ( ' '.join(sys.argv)+' #COMMAND' , 0)
  make_print ( 'Mode: '+str(args.mode) )
  make_print ( 'Projecting to lumi='+str(args.lumi)+' using a lumi scale of '+str(lumiscale)+' to scale the base lumi of '+str(baselumi) )
  make_print ( 'Applying systematics: '+str(syst) )
  make_print ( 'Scaling uncertainties: '+scale )
  make_print ( 'Model: '+model )
  make_print ( 'Writing to '+physdir )
  make_print ( 'Symlink dir '+basedir )

  os.chdir(rundir)
  ############################################## DATACARD
  if 'datacard' in args.mode:
    pcall_base='MorphingMSSMFull2016 --output_folder='+symdir+' --manual_rebin=true --real_data=false --bbb_threshold='+str(args.bbb) + ' -h "bkg_SM125"'
    if model=='none':
      pcall=pcall_base+' -m MH'
    else:
      pcall=pcall_base+' --remove_h=true'
    pcall=pcall+' &>'+basedir+'/log_datacard.txt'
    make_pcall(pcall,'Producing data cards for model '+model,0)
  ############################################## DATACARD

  #https://indico.cern.ch/event/718592/contributions/3042780/attachments/1669046/2676739/HFuture-Proj-June.pdf#page9
  #https://cms-hcomb.gitbooks.io/combine/content/part3/nonstandard.html#scaling-constraints
  #https://twiki.cern.ch/twiki/bin/viewauth/CMS/YR2018Systematics
  ############################################## WORKSPACE
  if model=='mhmod': mf='mhmodp_mu200'
  if model=='hmssm': mf='hMSSM'
  if model=='lightstau': mf='lightstau1'
  if model=='lightstop': mf='lightstopmod'
  if model=='lowtb': mf='low-tb-high'
  if model=='tauphobic': mf='tauphobic'
  
  if 'ws' in args.mode:
    scale_bbb=' --X-nuisance-function \'CMS_htt_.*bin_[0-9]+\' \'"expr::scaleBBB(\\"1/sqrt(@0)\\",lumi[1])"\''
    scale_all=' --X-nuisance-function \'CMS_+\' \'"expr::scaleAll(\\"1/sqrt(@0)\\",lumi[1])"\''  +  ' --X-nuisance-function \'lumi_+\' \'"expr::scaleLumi(\\"1/sqrt(@0)\\",lumi[1])"\'' + ' --X-nuisance-function \'.*ff_.*_syst+\' \'"expr::scaleAll(\\"1/sqrt(@0)\\",lumi[1])"\'' + ' --X-nuisance-function \'.*ff_.*_stat+\' \'"expr::scaleAll(\\"1/sqrt(@0)\\",lumi[1])"\'' + ' --X-nuisance-function \'QCDScale_+\' \'"expr::scaleAll(\\"1/sqrt(@0)\\",lumi[1])"\''

    scale_no_floor=' --X-nuisance-group-function \'no_floor\'   \'"expr::scaleNoFloor(\\"1/sqrt(@0)\\",lumi[1])"\''
    scale_eff_m   =' --X-nuisance-group-function \'eff_m\'      \'"expr::scaleEffM(\\"max(0.25,1/sqrt(@0))\\",lumi[1])"\''
    scale_eff_e   =' --X-nuisance-group-function \'eff_e\'      \'"expr::scaleEffE(\\"max(0.50,1/sqrt(@0))\\",lumi[1])"\''
    scale_eff_t   =' --X-nuisance-group-function \'eff_t\'      \'"expr::scaleEffT(\\"max(0.50,1/sqrt(@0))\\",lumi[1])"\''
    scale_eff_b   =' --X-nuisance-group-function \'eff_b\'      \'"expr::scaleEffB(\\"max(0.50,1/sqrt(@0))\\",lumi[1])"\''
    scale_jf_syst =' --X-nuisance-group-function \'jf_syst\'    \'"expr::scaleJfSyst(\\"max(0.50,1/sqrt(@0))\\",lumi[1])"\''
    scale_theory  =' --X-nuisance-group-function \'theory\'     \'0.5\''
    scale_lumi    =' --X-nuisance-group-function \'luminosity\' \'"expr::scaleLumi(\\"max(0.37,1/sqrt(@0))\\",lumi[1])"\''    #1.0/2.7=0.37

    scaleterm=''
    if scale=='all':
      scaleterm=scale_all
    if scale=='bbb' and args.bbb>0.001:
      scaleterm=scale_bbb
    if scale=='scen2':
      scaleterm=scale_no_floor+scale_eff_m+scale_eff_e+scale_eff_t+scale_eff_b+scale_jf_syst+scale_theory+scale_lumi
      if args.bbb>0.001: scaleterm+=scale_bbb
#    pcall='combineTool.py -M T2W -o ws.root --parallel 8 -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO \'"map=^.*/ggH.?$:r_ggH[0,0,200]"\' --PO \'"map=^.*/bbH$:r_bbH[0,0,200]"\' '+scaleterm+' -i output/'+symdir+'* &> '+basedir+'/log_ws.txt'
#    pcall_base='combineTool.py -M T2W -v 3 -o ws.root --parallel 8 '+scaleterm+' -i output/'+symdir+'*'
    pcall_base='combineTool.py -M T2W -o ws.root --parallel 8'+scaleterm+' -i output/'+symdir+'*'  #MF

    if model=='none':
      pcall=pcall_base+' -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO \'"map=^.*/ggH.?$:r_ggH[0,0,200]"\' --PO \'"map=^.*/bbH$:r_bbH[0,0,200]"\''
    else:
      pcall=pcall_base+' -P CombineHarvester.CombinePdfs.MSSM:MSSM --PO filePrefix=$PWD/shapes/Models/ --PO modelFiles='+cme+'TeV,'+mf+'_'+cme+'TeV.root,1 --PO MSSM-NLO-Workspace=$PWD/shapes/Models/higgs_pt_v3_mssm_mode.root'

    pcall+=' &> '+basedir+'/log_ws.txt'
    make_pcall(pcall,'Producing workspace',0)
  ############################################## WORKSPACE

  ############################################## LIMIT
  if 'limit' in args.mode:
    nfreeze='lumi'
    if not syst: nfreeze='all'

    if model=='none' and not dim2:
      proc=[ 'ggH' , 'bbH' ]
      make_pcall('echo Processes: '+str(proc)+' > '+basedir+'/log_lim.txt','',2)
      for p in proc:
        pcall1='combineTool.py -m "90,100,110,120,130,140,160,180,200,250,350,400,450,500,600,700,800,900,1000,1200,1400,1600,1800,2000,2300,2600,2900,3200" -M Asymptotic -t -1 --parallel 8 --rAbsAcc 0 --rRelAcc 0.0005 --boundlist input/mssm_boundaries-100.json --setPhysicsModelParameters r_ggH=0,r_bbH=0,lumi='+str(lumiscale)+' --freezeNuisances '+nfreeze+' --floatAllNuisances 1 --redefineSignalPOIs r_'+p+' -d output/'+symdir+'cmb/ws.root --there -n ".'+p+'" &>> '+basedir+'/log_lim.txt'
        pcall2='combineTool.py -M CollectLimits output/'+symdir+'cmb/higgsCombine.'+p+'*.root --use-dirs -o "output/'+symdir+p+'.json" &>> '+basedir+'/log_lim.txt'
        pcall3='python scripts/plotMSSMLimits.py --logy --logx --show exp output/'+symdir+p+'_cmb.json --cms-sub="Preliminary" -o output/'+symdir+p+'_cmb --process=\''+p[0:2]+'#phi\' --title-right="'+str(args.lumi)+' fb^{-1} ('+cme+' TeV)" --use-hig-17-020-style >> '+basedir+'/log_lim.txt'
        make_pcall(pcall1,'Producing  limit for '+p,0)
        make_pcall(pcall2,'Collecting limit for '+p,0)
        make_pcall(pcall3,'Plotting   limit for '+p,0)
    elif model=='none' and dim2:
        pcall1='combineTool.py -m "90,100,110,120,130,140,160,180,200,250,350,400,450,500,600,700,800,900,1000,1200,1400,1600,1800,2000,2300,2600,2900,3200" -M MultiDimFit -t -1 --parallel 8 --boundlist input/mssm_ggH_bbH_2D_boundaries.json --setPhysicsModelParameters r_ggH=0,r_bbH=0,lumi='+str(lumiscale)+' --freezeNuisances '+nfreeze+' --floatAllNuisances 1 --redefineSignalPOIs r_ggH,r_bbH -d output/'+symdir+'cmb/ws.root --there -n ".ggH-bbH" --points 500 --algo grid &>> '+basedir+'/log_lim.txt'
#        pcall2='combineTool.py -M CollectLimits output/'+symdir+'cmb/higgsCombine.'+p+'*.root --use-dirs -o "output/'+symdir+p+'.json" &>> '+basedir+'/log_lim.txt'
        pcall3='python scripts/plotMultiDimFit.py --cms-sub="Preliminary" -o output/'+symdir+'2d_cmb --title-right="'+str(args.lumi)+' fb^{-1} ('+cme+' TeV)" --mass 350 -o 2d_mH350 output/'+symdir+'cmb/higgsCombine.ggH-bbH.MultiDimFit.mH350.root  >> '+basedir+'/log_lim.txt'
        make_pcall(pcall1,'Producing  2D limit for mass '+str(350),0)
#        make_pcall(pcall2,'Collecting limit for '+p,0)
        make_pcall(pcall3,'Plotting   2D limit for mass '+str(350),0)
    else:
      os.chdir(basedir)
      dp='../../'
      #TODO: other models
      js=dp+'./scripts/mssm_asymptotic_grid.json'
      modelfile=mf+'_'+cme+'TeV.root'
      scenlabel=''
      yrange=''

      if model=='mhmod':
#        js=dp+'./scripts/mssm_asymptotic_grid_mhmodp.json'
        scenlabel='m_{h}^{mod+} scenario'
#        modelfile='mhmodp_mu200_'+cme+'TeV.root'
      if model=='hmssm':
        js=dp+'./scripts/mssm_asymptotic_grid_hMSSM.json'
        scenlabel='hMSSM scenario'
#        modelfile='hMSSM_'+cme+'TeV.root'
      if model=='tauphobic':
#        js=dp+'./scripts/mssm_asymptotic_grid_tauphobic_'+str(args.lumi)+'.json'
        js=dp+'./scripts/mssm_asymptotic_grid_tauphobic.json'
        scenlabel='tau-phobic scenario'
        yrange='--y-range 1,50 '
      if model=='lightstop':
        scenlabel='light-stop scenario'
      if model=='lightstau':
        scenlabel='light-stau scenario'
      if model=='lowtb':
        scenlabel='low tan #beta scenario'
      it=0
      ret=''
      while True:
        it+=1
        subarg='--parallel 8'
#        if lxb: subarg='--job-mode lxbatch --task-name '+mdir+'_grid --sub-opts \'-q 8nh\' --merge 20'
        if lxb: subarg='--job-mode lxbatch --task-name '+mdir+'_grid --sub-opts \'-q 1nd\' --merge 10' #be on the safe side for now - 3000/fb jobs could take much longer

        pcall='combineTool.py -M AsymptoticGrid '+js+' -d cmb/ws.root --setPhysicsModelParameters lumi='+str(lumiscale)+' --freezeNuisances '+nfreeze+' --floatAllNuisances 1 -t -1 '+subarg+' &>> '+basedir+'/log_lim.txt'
        make_pcall(pcall,'Producing limit for '+model,0)
        ret=os.popen('tail -1 '+basedir+'/log_lim.txt').read().rstrip()
        if 'Replacing existing TGraph2D' in ret: 
          break
        if lxb:
          break
        if it>10: 
          make_print( 'Stopping after restarting AsymptoticGrid for ten times. There is probably some problem, rather give up than ending up in an infinite loop' )
          break

      if 'New jobs were created' in ret: #jobs were just submitted, only do this on final run
        print 'New jobs were created... rerun limit step once they are done to produce plots.'
      else:
        pcall='python ../../../CombineTools/scripts/plotLimitGrid.py asymptotic_grid.root --scenario-label="'+scenlabel+'" --output="mssm_'+mdir+'" --title-right="'+str(args.lumi)+' fb^{-1} ('+cme+' TeV)" --cms-sub="Preliminary" --contours="exp-2,exp-1,exp0,exp+1,exp+2" --x-range 90,2000 '+yrange+'--model_file='+rundir+'shapes/Models/'+modelfile+' | grep -v "has.*points\|Two of these three" &> '+basedir+'/log_plotlim.txt'
#for i in jun28*; do cp -p $i/mssm_mhmod_cmb.png mssm_mhmod_$i.png; cp -p $i/asymptotic_grid.root asymptotic_grid_$i.root; done

        import socket
        if 'lxplus' in socket.gethostname():
#          pcall2='grep -v ",nan)" hist_exp+2_after.C | sed s\'#exp+#exp#g\' | sed s\'#Draw("")#Draw("colz")#g\' > hist_exp+1_after2.C'
          pcall2='for i in hist*C; do echo $i; grep -v ",nan)" $i | sed s\'#exp+#exp#g\' | sed s\'#exp-#exp#g\' | sed s\'#Draw("")#Draw("colz")#g\' > c_$i; done'
          make_pcall(pcall,'Producing limit plots for '+model,0)
          make_pcall(pcall2,'Fixing macros',2)
          make_pcall('cp -p asymptotic_grid.root asymptotic_grid_'+mdir+'.root','Copying asymptotic grid output files',2) #do not mv so that rerunning still works
        else: #for some reason, does not run on heplx
          make_print( pcall )
          make_print( '#Run the above on lxplus: /afs/cern.ch/work/m/mflechl/mssm_projection_tmp/CMSSW_7_4_7/src/CombineHarvester/MSSMFull2016' )
  ############################################## LIMIT

  ############################################## NP
  smass=700
  nfreeze='r_bbH,lumi'
  if not syst: nfreeze='all'
  os.chdir(basedir)

  if 'mlfit' in args.mode:

    mllog=basedir+'log_mlfit.txt'
#    pcall2='combineTool.py -M MaxLikelihoodFit -t -1 --parallel 8 --robustFit 1 --setPhysicsModelParameters r_ggH=0.0,r_bbH=0.0,lumi='+str(lumiscale)+' --freezeNuisances '+nfreeze+' --floatAllNuisances 1 --setPhysicsModelParameterRanges r_ggH=-0.000001,0.000001 --setPhysicsModelParameterRanges r_bbH=-0.000001,0.000001 -d cmb/ws.root --redefineSignalPOIs r_ggH --there -m '+str(smass)+' --boundlist '+rundir+'/input/mssm_boundaries-100.json --minimizerTolerance 0.1 --minimizerStrategy 0 --name ".res" '+' &>'+mllog
    pcall2='combineTool.py -M MaxLikelihoodFit -t -1 --parallel 8 --robustFit 1 --setPhysicsModelParameters r_ggH=0.0,r_bbH=0.0,lumi='+str(lumiscale)+' --freezeNuisances '+nfreeze+' --floatAllNuisances 1 --setPhysicsModelParameterRanges r_ggH=-0.000001,0.000001 --setPhysicsModelParameterRanges r_bbH=-0.000001,0.000001 -d cmb/ws.root --redefineSignalPOIs r_ggH --there -m '+str(smass)+' --boundlist '+rundir+'/input/mssm_boundaries-100.json --minimizerTolerance 0.5 --minimizerStrategy 1 --name ".res" '+' &>'+mllog
    make_pcall(pcall2, 'Running ML fit')
    make_pcall('mv cmb/mlfit.res.root cmb/mlfit.root','Renaming mlfit output files',2)

    make_print( '########################################################################################' )
    ret=os.popen('root -l cmb/mlfit.root <<<"fit_b->Print();" | grep "covariance matrix quality"').read().rstrip()
    make_print( ret , 0 )
    print_file(ret,mllog,'a')
    make_print( '########################################################################################' )

  if 'np' in args.mode:
#    pcall='python '+CMSSW_BASE+'/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py cmb/mlfit.root -A -a --stol 0.99 --stol 0.99 --vtol 99. --vtol2 99. -f text --poi r_ggH --histogram nuisance_tests.root &> '+basedir+'/log_np.txt'
    pcall='python '+CMSSW_BASE+'/src/HiggsAnalysis/CombinedLimit/test/diffNuisances.py cmb/mlfit.root -a --stol 0.99 --stol 0.99 --vtol 99. --vtol2 99. -f text --poi r_ggH --histogram nuisance_tests.root &> '+basedir+'/log_np.txt'
    make_pcall(pcall,'Make NP texts... in dir: '+basedir)

    exvar=' --exclude `cat ../combined.txt.cmb | awk {\'print $1\'} | grep _bin_ | head -c -1 | tr \'\\n\' \',\' `' if (args.bbb>0.001) else ''
    idir=basedir+'/cmb/impacts'
    make_dir(idir)
    os.chdir(idir)
    make_print( '### Make NP plots... in dir: '+idir)
    pcall4=[ 
#      'combineTool.py -t -1 -M Impacts -d ../ws.root -m '+str(smass)+' --setPhysicsModelParameters r_bbH=0,r_ggH=0,lumi='+str(lumiscale)+' --setPhysicsModelParameterRanges r_ggH=-1.0,1.0 --doInitialFit --robustFit 1 --minimizerAlgoForMinos Minuit2,Migrad --redefineSignalPOIs r_ggH --freezeNuisances '+nfreeze+' --floatAllNuisances 1 '+exvar+' &>log1.txt',
#      'combineTool.py -t -1 -M Impacts -d ../ws.root -m '+str(smass)+' --setPhysicsModelParameters r_bbH=0,r_ggH=0,lumi='+str(lumiscale)+' --setPhysicsModelParameterRanges r_ggH=-1.0,1.0 --doInitialFit --robustFit 1 --minimizerAlgoForMinos Minuit2,Migrad --redefineSignalPOIs r_ggH --freezeNuisances '+nfreeze+' --floatAllNuisances 1 '+exvar+' --saveFitResult &>log1.txt',
      'combineTool.py -t -1 -M Impacts -d ../ws.root -m '+str(smass)+' --setPhysicsModelParameters r_bbH=0,r_ggH=0,lumi='+str(lumiscale)+' --setPhysicsModelParameterRanges r_ggH=-0.05,0.05 --doInitialFit --robustFit 1 --minimizerAlgoForMinos Minuit2,Migrad --redefineSignalPOIs r_ggH --freezeNuisances '+nfreeze+' --floatAllNuisances 1 '+exvar+' --saveFitResult &>log1.txt',

#      'combineTool.py -t -1 -M Impacts -d ../ws.root -m '+str(smass)+' --setPhysicsModelParameters r_bbH=0,r_ggH=0,lumi='+str(lumiscale)+' --setPhysicsModelParameterRanges r_ggH=-1.0,1.0 --robustFit 1 --doFits --minimizerAlgoForMinos Minuit2,Migrad  --redefineSignalPOIs r_ggH --freezeNuisances '+nfreeze+ ' --floatAllNuisances 1 --allPars --parallel 8'+exvar+' &>log2.txt',
#      'combineTool.py -t -1 -M Impacts -d ../ws.root -m '+str(smass)+' --setPhysicsModelParameters r_bbH=0,r_ggH=0,lumi='+str(lumiscale)+' --setPhysicsModelParameterRanges r_ggH=-1.0,1.0 --robustFit 1 --doFits --minimizerAlgoForMinos Minuit2,Migrad  --redefineSignalPOIs r_ggH --freezeNuisances '+nfreeze+ ' --floatAllNuisances 1 --allPars --parallel 8'+exvar+' --saveFitResult &>log2.txt',
      'combineTool.py -t -1 -M Impacts -d ../ws.root -m '+str(smass)+' --setPhysicsModelParameters r_bbH=0,r_ggH=0,lumi='+str(lumiscale)+' --setPhysicsModelParameterRanges r_ggH=-0.05,0.05 --robustFit 1 --doFits --minimizerAlgoForMinos Minuit2,Migrad  --redefineSignalPOIs r_ggH --freezeNuisances '+nfreeze+ ' --floatAllNuisances 1 --allPars --parallel 8'+exvar+' --saveFitResult &>log2.txt',

      'combineTool.py -M Impacts -d ../ws.root --allPars --redefineSignalPOIs r_ggH --setPhysicsModelParameters r_bbH=0,r_ggH=0,lumi='+str(lumiscale)+' --floatAllNuisances 1 --exclude r_bbH,lumi -m '+str(smass)+' -o impacts.json'+exvar+' &>log3.txt',
      'plotImpacts.py -i impacts.json -o impacts --transparent &>log4.txt',
      'cp -p impacts.pdf ../',
      ]
    ll=[1,1,1,1,2]
    for j,p4 in enumerate(pcall4):
      make_pcall(p4,'',ll[j])

    os.chdir(rundir)

  ############################################## NP


#def create_output_dir(webdir):
def create_output_dir():
#    if not dryrun:    #currently, dryrun needs at least the directory to be created...
  os.system('mkdir -p '+physdir)
  if os.path.islink(basedir.rstrip('/')): os.remove(basedir.rstrip('/'))
  os.symlink(mdir,basedir.rstrip('/')) #symdir
  make_print( '### output dir '+physdir+' and symlink created.' , 0)

  print 'XXXX',physdir,mdir,basedir.rstrip('/')

#        make_dir(webdir.replace(symdir.rstrip('/'),mdir))
#        if os.path.islink(webdir): 
#            os.remove(webdir)
#        os.symlink(mdir,webdir)

def make_dir(d,msg=''):
    if not msg=='':
        make_print( '### '+msg )

    if not os.path.exists(d):
        make_print( ' >> mkdir -p '+d )
        os.makedirs(d)

def make_print(msg,level=1):
    global logf
    if not 'logf' in globals():
        logf = open(logfile, 'a')

    if level <= loglevel:
        print msg

    logf.write(msg+'\n')

def print_file(text,fname,mode='w'):
    f = open(fname, mode)
    f.write(text)
    f.close()

def make_pcall(pcall,msg='',level=1,rep=0):
    if rep==0 and not msg=='': 
        make_print( '### '+msg )
    make_print( ' >> '+pcall.replace(basedir,'') , level )

    if not dryrun: os.system(pcall)

if __name__ == '__main__':
  main(sys.argv[1:])




#combineTool.py -M T2W -o "ws.root" -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO '"map=^.*/ggH.?$:r_ggH[0,0,200]"' --PO '"map=^.*/bbH$:r_bbH[0,0,200]"' -i output/mssm_201017_scale-bbb/* --X-nuisance-function 'CMS_htt_.*bin_[0-9]+' '"expr::lumisyst(\"1/sqrt(@0)\",lumiscale[1])"' &> output/mssm_201017_scale-bbb/log_ws.txt
#combineTool.py -M T2W -o "ws.root" -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO '"map=^.*/ggH.?$:r_ggH[0,0,200]"' --PO '"map=^.*/bbH$:r_bbH[0,0,200]"' -i output/mssm_201017_scale-all/* --X-nuisance-function 'CMS_+' '"expr::lumisyst(\"1/sqrt(@0)\",lumiscale[1])"' --X-nuisance-function 'lumi_+' '"expr::lumisyst(\"1/sqrt(@0)\",lumiscale[1])"' &> output/mssm_201017_scale-all/log_ws.txt

#for i in jun15*; do cp -p $i/asymptotic_grid.root asymptotic_grid_$i.root ; done
