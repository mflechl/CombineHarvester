#!/bin/bash
declare -A ds

do6000=1

d='output/'
tag='jul17_'
tag2='jul20_'
tag3='jul07_'
tag4='oct28_'

ds_nosys=( ${d}${tag}'lumi-35.9_nosyst/'       ${d}${tag}'lumi-300.0_nosyst/'      ${d}${tag}'lumi-3000.0_nosyst/' )
ds_nosca=( ${d}${tag}'lumi-35.9/'              ${d}${tag}'lumi-300.0/'             ${d}${tag}'lumi-3000.0/' )
#ds_scall=( ${d}${tag}'lumi-35.9_scale-all/'    ${d}${tag}'lumi-300.0_scale-all/'   ${d}${tag}'lumi-3000.0_scale-all/' )
#ds_scbbb=( ${d}${tag}'lumi-35.9_scale-bbb/'    ${d}${tag}'lumi-300.0_scale-bbb/'   ${d}${tag}'lumi-3000.0_scale-bbb/' )
ds_scsc2=( ${d}${tag}'lumi-35.9_scale-scen2/'  ${d}${tag}'lumi-300.0_scale-scen2/' ${d}${tag}'lumi-3000.0_scale-scen2/' )
#ds_scnob=( ${d}${tag}'lumi-35.9_scale-scen2_nobbb/' ${d}${tag}'lumi-300.0_scale-scen2_nobbb/' ${d}${tag}'lumi-3000.0_scale-scen2_nobbb/' )

if [ $do6000 -eq 1 ]; then
    ds_scsc2=( ${d}${tag}'lumi-35.9_scale-scen2/'  ${d}${tag}'lumi-300.0_scale-scen2/' ${d}${tag}'lumi-3000.0_scale-scen2/' ${d}${tag4}'lumi-6000.0_scale-scen2/' )
fi

pas=1

o="output/limit_comp"
lbl="Internal"
suf='_internal'

if [ "$pas" == "1" ]; then
    o="output/limit_comp_pas"
#    o="output/limit_comp_int"
#    o="output/limit_comp_tmp"
#    lbl="Preliminary Simulation"
    lbl="Projection"
    suf='_pas'
#    lbl="Internal"
fi


#modes=( 'no_systematics' 'no_scaling'  'scale_all' 'scale_bbb' 'scen2' 'scen2_nobbb' )
#scripts/plotMSSMLimits.py , line 264
#modes=( 'no_systematics' 'no_scaling'  'scen2' )
#modes=( 'no_scaling'   'scen2'  'no_systematics' )
modes=( 'scen2' )
#lumi=(  '35.9_fb^{-1}'   '300_fb^{-1}' '3000_fb^{-1}'          )
lumi=(  'HIG-17-020'   '300_fb^{-1}' '3000_fb^{-1}'          )

if [ $do6000 -eq 1 ]; then
    lumi=(  'HIG-17-020'   '300_fb^{-1}' '3000_fb^{-1}' '6000_fb^{-1}'         )
    suf+='_w6000'
fi

ds[no_systematics]=ds_nosys[@]
ds[no_scaling]=ds_nosca[@]
#ds[scale_all]=ds_scall[@]
#ds[scale_bbb]=ds_scbbb[@]
ds[scen2]=ds_scsc2[@]
#ds[scen2_nobbb]=ds_scnob[@]

for m in ${modes[@]}; do 
    i=0
    for d in ${!ds[$m]}; do ds_[i]=$d; let i=$i+1; done

    for p in 'ggH' 'bbH'; do
	title_left="with YR18 syst. uncert."
	if [ "$pas" != "1" ]; then
	    title_left+=", ${p}, `echo $m | tr _ ' '`"
	fi
	echo "##### $title_left #####"
	lterm=''
	for i in `seq 0 $(( ${#lumi[@]} - 1 ))`; do
	    lterm+=${ds_[$i]}${p}'_cmb.json:exp0:Title='"\"${lumi[$i]}\""
	    lterm+=" "
	done
	echo Using $lterm
	python scripts/plotMSSMLimits.py --logy --logx --show exp0 $lterm --cms-sub="${lbl}" -o ${o}/${m}_${p}${suf} --process=${p:0:2}'#phi' --title-right="13 TeV" --use-hig-17-020-style --auto-style --ratio-to ${ds_[0]}${p}'_cmb.json:exp0' --title-left="$title_left"
    done
done

for l in ${lumi[@]}; do 
    lumititle=${l/"_fb^{-1}"/""}
    i=0
#    echo lumititle $lumititle
    for m in ${modes[@]}; do for d in ${!ds[$m]}; do 
	    if [[ "$d" =~ "${lumititle}." ]] || [[ "$d" =~ "${lumititle}_" ]] || [[ "$d" =~ "${lumititle}/" ]]; then ds_[i]=$d; let i=$i+1; fi; done; 
    done
    echo XX ${ds_[@]}

    lumititle=${lumititle/"."/"p"}
    for p in 'ggH' 'bbH'; do
#	title_left="${p}, `echo $l | tr _ ' '`"
	title_left="`echo $l | tr _ ' '`"
	echo "##### $title_left #####"
	lterm=''
	for i in `seq 0 $(( ${#modes[@]} - 1 ))`; do
	    lterm+=${ds_[$i]}${p}'_cmb.json:exp0:Title='"\"${modes[$i]}\""
	    lterm+=" "
	done
	echo Using $lterm
	python scripts/plotMSSMLimits.py --logy --logx --show exp0 $lterm --cms-sub="${lbl}" -o ${o}/${lumititle}fb_${p}${suf} --process=${p:0:2}'#phi' --title-right="13 TeV" --use-hig-17-020-style --auto-style --ratio-to ${ds_[0]}${p}'_cmb.json:exp0' --title-left="$title_left"
    done
done


#    python scripts/plotMSSMLimits.py --logy --logx --show exp0 ${ds_unsc[0]}${p}'_cmb.json:exp0:Title="35.9 fb^{-1}"' ${ds_unsc[1]}${p}'_cmb.json:exp0:Title="300/fb"' ${ds_unsc[2]}${p}'_cmb.json:exp0:Title="3000/fb"' --cms-sub="Preliminary" -o output/noscale_${p} --process=${p:0:2}'#phi' --title-right="13 TeV" --use-hig-17-020-style --auto-style --ratio-to ${ds_unsc[0]}${p}'_cmb.json:exp0' --title-left=''${p}', unscaled'

