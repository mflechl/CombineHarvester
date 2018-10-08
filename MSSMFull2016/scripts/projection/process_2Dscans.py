import ROOT as r
import json
from array import array
#import yaml
from copy import deepcopy
import os

r.gROOT.SetBatch()
r.gStyle.SetOptStat(0)

CMSSW_BASE=os.environ['CMSSW_BASE']
rundir=CMSSW_BASE+'/src/CombineHarvester/MSSMFull2016/'

nbins = 200


yaml_table_dict_template = {}


yaml_table_dict_template["independent_variables"] = [
    {
        "header" : {"name" : "$\\sigma(gg\\phi)\\times B(\\phi\\to\\tau\\tau)$", "units" : "PB"},
        "values" : [
        ]
    },
    {
        "header" : {"name" : "$\\sigma(bb\\phi)\\times B(\\phi\\to\\tau\\tau)$", "units" : "PB"},
        "values" : [
        ]
    }
]

yaml_table_dict_template["dependent_variables"] = [
    {
        "header" : {"name" : "$\\Delta(-\\ln\\mathrm{L})$"},
        "qualifiers" : [
            { "name" : "SQRT(S)", "units" : "GEV", "value" : 13000},
            { "name" : "Luminosity", "units" : "FB**-1", "value" : 35.9},
            { "name" : "$m_{\\phi}$", "units" : "GEV", "value" : 90},
        ],
        "values" : [
        ]
    }
]

def MakeTChain(files, tree):
    chain = r.TChain(tree)
    for f in files:
        chain.Add(f)
    return chain

def TGraph2DFromTree(tree, xvar,  yvar, zvar, selection):
    tree.Draw(xvar + ':' + yvar + ':' + zvar, selection, 'goff')
    gr = r.TGraph2D(
        tree.GetSelectedRows(), tree.GetV1(), tree.GetV2(), tree.GetV3())
    return gr

def FillHistFromTree(h,tree,name,interpolate=False):
    for i in range(1,h.GetNbinsX()+1):
        for j in range(1,h.GetNbinsY()+1):
            h.SetBinContent(i,j,99999.0)

    for entry in tree:
        deltaNLLBin = h.FindBin(entry.r_ggH, entry.r_bbH)
        if entry.deltaNLL == 0 and h.GetBinContent(deltaNLLBin) == 99999.0:
            print "Bin found for Minimum",deltaNLLBin,"Content in hist",h.GetBinContent(deltaNLLBin),"place",entry.r_ggH, entry.r_bbH
            h.SetBinContent(deltaNLLBin, entry.deltaNLL)
        
    for entry in tree:
        deltaNLLBin = h.FindBin(entry.r_ggH, entry.r_bbH)
        if entry.deltaNLL > 0.0 and h.GetBinContent(deltaNLLBin) == 99999.0:
            h.SetBinContent(deltaNLLBin, entry.deltaNLL)

    if interpolate:
        gr = TGraph2DFromTree(tree,"r_ggH","r_bbH", "deltaNLL","")
        for i in range(1,h.GetNbinsX()+1):
            for j in range(1,h.GetNbinsY()+1):
                if h.GetBinContent(i,j) == 99999.0:
                    h.SetBinContent(i,j,gr.Interpolate(h.GetXaxis().GetBinCenter(i),h.GetYaxis().GetBinCenter(j)))
                    if h.GetBinContent(i,j) == 0:
                        print "Caution: interpolated to zero! Correction attempt for:",i,j
                        if (j == 1 or j == h.GetNbinsY()) and i > 1:
                            step = 1 if j == 1 else -1
                            print "Bin at border. Performing linear interpolation along the border."
                            search_left = i-1
                            search_right = i+1
                            search_away_from_border = j+step
                            neighbour_away = 0.0
                            neighbour_left = 0.0
                            neighbour_right= 0.0
                            while neighbour_away == 0.0 and search_away_from_border >= 1 and search_away_from_border <= 200:
                                test = h.GetBinContent(i,search_away_from_border)
                                if test > 0.0 and test < 99999.0:
                                    neighbour_away = test
                                else:
                                    search_away_from_border += step
                            while neighbour_left == 0.0 and search_left >= 1:
                                test = h.GetBinContent(search_left,j)
                                if test > 0.0 and test < 99999.0:
                                    neighbour_left = test
                                else:
                                    search_left -= 1
                            while neighbour_right == 0.0 and search_right <= 200:
                                test = h.GetBinContent(search_right,j)
                                if test > 0.0 and test < 99999.0:
                                    neighbour_right = test
                                else:
                                    search_right += 1
                            values_list = [v for v in [neighbour_away,neighbour_right,neighbour_left] if v != 0.0]
                            h.SetBinContent(i,j,sum(values_list)/len(values_list))
                        elif (i == 1 or i == h.GetNbinsX()) and j > 1:
                            step = 1 if i == 1 else -1
                            print "Bin at border. Performing linear interpolation along the border."
                            search_away_from_border = i+step
                            search_left = j-1
                            search_right = j+1
                            neighbour_away = 0.0
                            neighbour_left = 0.0
                            neighbour_right= 0.0
                            while neighbour_away == 0.0 and search_away_from_border >= 1 and search_away_from_border <= 200:
                                test = h.GetBinContent(search_away_from_border,j)
                                if test > 0.0 and test < 99999.0:
                                    neighbour_away = test
                                else:
                                    search_away_from_border += step
                            while neighbour_left == 0.0 and search_left >= 1:
                                test = h.GetBinContent(i,search_left)
                                if test > 0.0 and test < 99999.0:
                                    neighbour_left = test
                                else:
                                    search_left -= 1
                            while neighbour_right == 0.0 and search_right <= 200:
                                test = h.GetBinContent(i,search_right)
                                if test > 0.0 and test < 99999.0:
                                    neighbour_right = test
                                else:
                                    search_right += 1
                            values_list = [v for v in [neighbour_away,neighbour_right,neighbour_left] if v != 0.0]
                            h.SetBinContent(i,j,sum(values_list)/len(values_list))
                        else:
                            print "Attention!!! Arived at edge",i,j


masses =  ["90", "100", "110","120", "125", "130", "140", "160", "180", "200", "250", "350", "400", "450", "500", "600", "700", "800", "900","1000","1200","1400","1600","1800","2000","2300","2600","2900","3200"]
masses =  ["90", "100", "110","120", "125", "130", "140", "160", "180", "200", "700"]
#masses =  ["90","200","3200"]
#masses = [ "700" ]

version_1_dict = {
"noSMHinBG" : ["400","500","700","800","1000","1200","1400"],
#"noSMHinBG" : [],
"SMHinBG" : ["600","700","1000"]
#"SMHinBG" : []
}

#for higgs in ["noSMHinBG","SMHinBG"]:
for higgs in ["noSMHinBG"]:
#for higgs in ["SMHinBG"]:
    for datamode in [""]:
        hstring = "" if higgs == "noSMHinBG" else "_SMHbkg"
        #dmstring = "" if datamode == "" else "_asimov"
#        json_name = rundir+"input/mssm_ggH_bbH_2D_boundaries{HIGGS}_both.json".format(HIGGS=hstring)
        json_name = rundir+"input/mssm_ggH_bbH_2D_boundaries_both_3000fb.json".format(HIGGS=hstring)
        boundaries = json.load(open(json_name))

#        files = ["higgsCombine.ggH-bbH.40k.DataBase.{HIGGS}{ASIMOV}.{VERSION}.MultidimFit.EqualRanges.mH{MASS}.root".format(HIGGS=higgs,MASS=m,VERSION="v1" if m in version_1_dict[higgs] or datamode == "_Asimov" else "v2",ASIMOV=datamode) for m in masses]
        files = ["higgsCombine.ggH-bbH.40k.DataBase.{HIGGS}_3000fb_Asimov.v1.MultiDimFit.mH{MASS}.root".format(HIGGS=higgs,MASS=m) for m in masses]
#        files = [ "test.root" ]
        scans = {}
        c = r.TCanvas("c","c")
        c.cd()
        for mass,f in zip(masses,files):
            print "Updating 2D scan for",mass
            limit = MakeTChain([f],"limit")
            limit.SetBranchStatus("*",0)
            limit.SetBranchStatus("deltaNLL",1)
            limit.SetBranchStatus("r_ggH",1)
            limit.SetBranchStatus("r_bbH",1)
            limit.SetBranchStatus("quantileExpected",1)
#            r_ggH_bounds, r_bbH_bounds = boundaries["r_ggH"][str(float(mass))],boundaries["r_bbH"][str(float(mass))]
            r_ggH_bounds, r_bbH_bounds = boundaries["r_ggH"][mass],boundaries["r_bbH"][mass]
            print r_ggH_bounds
            print r_bbH_bounds

            #h = FillHistFromTree(limit,"h")
            #h.Draw("COLZ")
            #h.GetZaxis().SetRangeUser(0.0,10.0)
            #h.Draw("COLZ")
            #c.SaveAs("original_scan_%s.pdf"%mass)
            #c.Clear()

            tree_min = limit.GetMinimum('deltaNLL')
            scans[mass] = r.TTree("limit_copy","limit_copy")
            deltaNLL = array('f',[0.0])
            r_ggH = array('f',[0.0]) 
            r_bbH = array('f',[0.0]) 
            quantileExpected = array('f',[0.0])
            scans[mass].Branch("deltaNLL",deltaNLL,"deltaNLL/F")
            scans[mass].Branch("r_ggH",r_ggH,"r_ggH/F")
            scans[mass].Branch("r_bbH",r_bbH,"r_bbH/F")
            scans[mass].Branch("quantileExpected",quantileExpected,"quantileExpected/F")

            for entry in limit:
                #if abs(entry.deltaNLL) < 0.0001 and entry.deltaNLL < 0:
                #    deltaNLL[0] = entry.deltaNLL
                #else:
                #    deltaNLL[0] = entry.deltaNLL - tree_min
                deltaNLL[0] = entry.deltaNLL - tree_min
                if entry.deltaNLL < 0:
                    print "place:",entry.r_ggH, ",",entry.r_bbH,"values:", entry.deltaNLL, deltaNLL, tree_min, entry.quantileExpected
                r_ggH[0] = entry.r_ggH
                r_bbH[0] = entry.r_bbH
                quantileExpected[0] = entry.quantileExpected
                scans[mass].Fill()
            print "Minimum in Tree Copy:",scans[mass].GetMinimum("deltaNLL")

            h2 = r.TH2D(mass,mass,nbins,r_ggH_bounds[0],r_ggH_bounds[1],nbins,r_bbH_bounds[0],r_bbH_bounds[1])

            #FillHistFromTree(h2,scans[mass],mass,False)
            FillHistFromTree(h2,scans[mass],mass,True)
            #h2.Scale(2.0)

            it=15
            if float(mass)>300: it=2
            for i in xrange(0,it):  #repeat n=arg2 times
                h2.Smooth(1,"k5b")

            textfile = open("2D_scan_%s_%s.txt" %(higgs+datamode,mass),"w")
            yamlfile = open("2D_scan_%s_%s.yaml" %(higgs+datamode,mass),"w")
            
            yaml_table_dict = deepcopy(yaml_table_dict_template)
            yaml_table_dict["dependent_variables"][0]["qualifiers"][2]["value"] = int(mass)
            info = ""

            for i in range(1,h2.GetNbinsX()+1):
                for j in range(1,h2.GetNbinsY()+1):
                    r_ggH_value,r_bbH_value,deltaNLL_value = h2.GetXaxis().GetBinLowEdge(i), h2.GetYaxis().GetBinLowEdge(j), h2.GetBinContent(i,j)
                    info += "%s %s %s\n" %(r_ggH_value, r_bbH_value, deltaNLL_value)
                    yaml_table_dict["dependent_variables"][0]["values"].append({"value" : deltaNLL_value})
                    yaml_table_dict["independent_variables"][0]["values"].append({"value" : r_ggH_value})
                    yaml_table_dict["independent_variables"][1]["values"].append({"value" : r_bbH_value})

            if h2.GetMinimum() != 0.0:
                print "Place of Minimum",h2.GetMinimum(),"in hist:",h2.GetXaxis().GetBinLowEdge(i),",",h2.GetYaxis().GetBinLowEdge(j),"global bin",h2.GetBin(i,j),h2.GetBinContent(h2.GetBin(i,j)),"mass",mass

            textfile.write(info)
            textfile.close()

#            yamlfile.write(yaml.dump(yaml_table_dict))
            yamlfile.close()

            h2.GetZaxis().SetRangeUser(0.0,20.0)

            h2.Draw("COLZ")
            #contours = array('d',[r.Math.chisquared_quantile_c(1 - 0.95, 2)])
            #h2.SetContour(1,contours)
            #h2.Draw("SAME CONT1 Z")
            c.Update()
            name = "modified_scan_%s.pdf" %(higgs+datamode)
            if mass == masses[0]:
                c.Print(name+"(","pdf")
            elif mass == masses[-1]:
                c.Print(name+")","pdf")
            else:
                c.Print(name,"pdf")
#            c.SaveAs("modified_scan.pdf")
            c.Clear()
            del(h2)
    

