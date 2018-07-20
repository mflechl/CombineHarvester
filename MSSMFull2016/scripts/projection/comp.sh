#!/bin/bash
declare -A ds

d='output/'
tag='jul05_'
tag2='jul05_'
tag3='jul07_'

ds_nosys=( ${d}${tag}'lumi-35.9_nosyst/'       ${d}${tag2}'lumi-300.0_nosyst/'    ${d}${tag2}'lumi-3000.0_nosyst/' )
ds_nosca=( ${d}${tag}'lumi-35.9/'              ${d}${tag2}'lumi-300.0/'           ${d}${tag2}'lumi-3000.0/' )
ds_scall=( ${d}${tag}'lumi-35.9_scale-all/'    ${d}${tag2}'lumi-300.0_scale-all/' ${d}${tag2}'lumi-3000.0_scale-all/' )
ds_scbbb=( ${d}${tag}'lumi-35.9_scale-bbb/'    ${d}${tag2}'lumi-300.0_scale-bbb/' ${d}${tag2}'lumi-3000.0_scale-bbb/' )
ds_scsc2=( ${d}${tag3}'lumi-35.9_scale-scen2/' ${d}${tag3}'lumi-300.0_scale-scen2/' ${d}${tag3}'lumi-3000.0_scale-scen2/' )
ds_scnob=( ${d}${tag3}'lumi-35.9_scale-scen2_nobbb/' ${d}${tag3}'lumi-300.0_scale-scen2_nobbb/' ${d}${tag3}'lumi-3000.0_scale-scen2_nobbb/' )
o='output/limit_comp' 


#modes=( 'no_systematics' 'no_scaling'  'scale_all' 'scale_bbb' 'scale_scen2' 'scale_scen2-nobbb' )
modes=( 'no_systematics' 'no_scaling'  'scale_all' 'scale_bbb' 'scen2' 'scen2_nobbb' )
lumi=(  '35.9_fb^{-1}'   '300_fb^{-1}' '3000_fb^{-1}'          )
ds[no_systematics]=ds_nosys[@]
ds[no_scaling]=ds_nosca[@]
ds[scale_all]=ds_scall[@]
ds[scale_bbb]=ds_scbbb[@]
ds[scen2]=ds_scsc2[@]
ds[scen2_nobbb]=ds_scnob[@]

for m in ${modes[@]}; do 
    i=0
    for d in ${!ds[$m]}; do ds_[i]=$d; let i=$i+1; done

    for p in 'ggH' 'bbH'; do
	title_left="${p}, `echo $m | tr _ ' '`"
	echo "##### $title_left #####"
	lterm=''
	for i in `seq 0 $(( ${#lumi[@]} - 1 ))`; do
	    lterm+=${ds_[$i]}${p}'_cmb.json:exp0:Title='"\"${lumi[$i]}\""
	    lterm+=" "
	done
	echo Using $lterm
	python scripts/plotMSSMLimits.py --logy --logx --show exp0 $lterm --cms-sub="Internal" -o ${o}/${m}_${p} --process=${p:0:2}'#phi' --title-right="13 TeV" --use-hig-17-020-style --auto-style --ratio-to ${ds_[0]}${p}'_cmb.json:exp0' --title-left="$title_left"
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
	title_left="${p}, `echo $l | tr _ ' '`"
	echo "##### $title_left #####"
	lterm=''
	for i in `seq 0 $(( ${#modes[@]} - 1 ))`; do
	    lterm+=${ds_[$i]}${p}'_cmb.json:exp0:Title='"\"${modes[$i]}\""
	    lterm+=" "
	done
	echo Using $lterm
	python scripts/plotMSSMLimits.py --logy --logx --show exp0 $lterm --cms-sub="Internal" -o ${o}/${lumititle}fb_${p} --process=${p:0:2}'#phi' --title-right="13 TeV" --use-hig-17-020-style --auto-style --ratio-to ${ds_[0]}${p}'_cmb.json:exp0' --title-left="$title_left"
    done
done


#    python scripts/plotMSSMLimits.py --logy --logx --show exp0 ${ds_unsc[0]}${p}'_cmb.json:exp0:Title="35.9 fb^{-1}"' ${ds_unsc[1]}${p}'_cmb.json:exp0:Title="300/fb"' ${ds_unsc[2]}${p}'_cmb.json:exp0:Title="3000/fb"' --cms-sub="Preliminary" -o output/noscale_${p} --process=${p:0:2}'#phi' --title-right="13 TeV" --use-hig-17-020-style --auto-style --ratio-to ${ds_unsc[0]}${p}'_cmb.json:exp0' --title-left=''${p}', unscaled'

