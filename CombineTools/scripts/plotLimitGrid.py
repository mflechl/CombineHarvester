#!/usr/bin/env python
import CombineHarvester.CombineTools.plotting as plot
import ROOT
import argparse
from math import isnan

ROOT.PyConfig.IgnoreCommandLineOptions = True
ROOT.gROOT.SetBatch(ROOT.kTRUE)

def manip(hist,typ,mod,lumi):
  hist.SaveAs('hist_'+typ+'_before.C')
  for x in xrange(1, hist.GetNbinsX()+1):
      for y in xrange(hist.GetNbinsY(), 0, -1):
#      for y in xrange(1, hist.GetNbinsY()+1):

          val=hist.GetBinContent(x,y)
          print 'AA '+typ+'   '+str(hist.GetXaxis().GetBinCenter(x))+' / '+str(hist.GetYaxis().GetBinCenter(y))+' = '+str(val)+'   '+str(x)+' / '+str(y)


          if mod=='tauphobic' and lumi=='3000.0' and scen=='scen2':
            if ( (  typ=='exp0' and
                    ( x==78 and (y==16 or y==17) ) or
                    ( x==79 and (y==17 or y==18) ) or
                    ( x==80 and  y==18           ) or
                    ( x==81 and  y==18           ) 
                    ) or
                 (  typ=='exp+2' and
                    ( x==66 and (y>=14 and y<=20) ) or
                    ( x==67 and (y>=14 and y<=20) ) or
                    ( x==68 and (y>=15 and y<=20) ) or
                    ( x==69 and (y>=15 and y<=20) ) or
                    ( x==70 and (y>=16 and y<=20) ) or
                    ( x==71 and (y>=17 and y<=20) ) or
                    ( x==72 and (y>=17 and y<=20) ) or
                    ( x==73 and (y>=18 and y<=20) ) or
                    ( x==74 and  y==19           ) 
                    )
                 ):
              newval=( 49*hist.GetBinContent(x,y+1) + hist.GetBinContent(x,y-1) )/50.0
              hist.SetBinContent(x,y,newval)
              print 'ZZ'+typ+'    '+str(hist.GetXaxis().GetBinCenter(x))+' / '+str(hist.GetYaxis().GetBinCenter(y))+' = '+str(val)+' ==> '+str(newval)
              continue

          if mod=='tauphobic' and lumi=='300.0' and scen=='scen2':
            if (  typ=='exp0' and
                  ( x==61 and (y>=15 and y<=19) ) or
                  ( x==62 and (y>=15 and y<=19) ) or
                  ( x==63 and (y>=16 and y<=20) ) or
                  ( x==64 and (y>=17 and y<=20) ) or
                  ( x==65 and (y>=17 and y<=21) ) or #18
                  ( x==66 and (y>=18 and y<=21) ) or
                  ( x==67 and (y>=18 and y<=22) ) or #19
                  ( x==68 and (y>=19 and y<=22) ) or
                  ( x==69 and (y>=20 and y<=22) ) or
                  ( x==70 and (y>=21 and y<=22) ) or
                  ( x==71 and (y>=21 and y<=22) ) or #22
                  ( x==72 and (y>=22 and y<=22) ) or
                  ( x==73 and (y>=22 and y<=22) ) or
                  ( x==74 and (y>=23 and y<=23) )
                  ):
              newval=0.04 #( 99*hist.GetBinContent(x,y+1) + hist.GetBinContent(x,y-1) )/100.0
              hist.SetBinContent(x,y,newval)
              print 'ZZ'+typ+'    '+str(hist.GetXaxis().GetBinCenter(x))+' / '+str(hist.GetYaxis().GetBinCenter(y))+' = '+str(val)+' ==> '+str(newval)
              continue
            if (  typ=='exp0' and
                  ( x==66 and (y>=16 and y<=17) ) or
                  ( x==67 and (y>=16 and y<=17) ) or #19
                  ( x==68 and (y>=17 and y<=18) ) or
                  ( x==69 and (y>=18 and y<=19) ) or
                  ( x==70 and (y>=19 and y<=20) )
                  ):
              newval=0.06 #( 99*hist.GetBinContent(x,y+1) + hist.GetBinContent(x,y-1) )/100.0
              hist.SetBinContent(x,y,newval)
              print 'ZZ'+typ+'    '+str(hist.GetXaxis().GetBinCenter(x))+' / '+str(hist.GetYaxis().GetBinCenter(y))+' = '+str(val)+' ==> '+str(newval)
              continue

          if mod=='tauphobic' and ( lumi=='3000.0' or lumi=='300.0' ) and (x==0 or x==1 or x==2):
            newval=0.01
            hist.SetBinContent(x,y,newval)
            print 'YY'+typ+'    '+str(hist.GetXaxis().GetBinCenter(x))+' / '+str(hist.GetYaxis().GetBinCenter(y))+' = '+str(val)+' ==> '+str(newval)
          elif isnan(val) or val<1e-12:
#              print 'XX'+typ+'    '+str(hist.GetBinLowEdge(x))+' / '+str(hist.GetBinLowy)+' = '+str(hist.GetBinContent(x,y))
              babove=hist.GetBinContent(x,y+1)
              bbelow=hist.GetBinContent(x,y-1)
              bleft=hist.GetBinContent(x-1,y)
              bright=hist.GetBinContent(x+1,y)
              newval=1e-12
              if bbelow > 1e-12 and babove > 1e-12: newval= (bbelow+babove)/2
              elif bleft > 1e-12 and bright > 1e-12: newval= (bleft+bright)/2
              elif babove > 1e-12: newval=babove
              elif bbelow > 1e-12: newval=bbelow #
              elif bleft > 1e-12: newval=bleft #
              elif bright > 1e-12: newval=bright #
#              if mod=='hmssm' and ( lumi=='3000.0' or lumi=='300.0' ):
#                if x==1: newval=0.01
              print 'XX'+typ+'    '+str(hist.GetXaxis().GetBinCenter(x))+' / '+str(hist.GetYaxis().GetBinCenter(y))+' = '+str(val)+' ==> '+str(newval)
              hist.SetBinContent(x,y,newval)
  hist.SaveAs('hist_'+typ+'_after.C')

parser = argparse.ArgumentParser(
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument(
    'input', help="""ROOT file containing the output of the
    combineTool.py AsymptoticGrid or HybridNewGrid methods""")
parser.add_argument(
    '--output', '-o', default='limit_grid_output', help="""Name of the output
    plot without file extension""")
parser.add_argument(
    '--contours', default='exp-2,exp-1,exp0,exp+1,exp+2,obs', help="""List of
    contours to plot. These must correspond to the names of the TGraph2D
    objects in the input file""")
parser.add_argument(
    '--bin-method', default='BinEdgeAligned', help="""One of BinEdgeAligned or
    BinCenterAligned. See plotting.py documentation for details.""")
parser.add_argument(
    '--debug-output', '-d', help="""If specified, write the contour TH2s and
    TGraphs into this output ROOT file""")
parser.add_argument(
    '--CL', default=0.95, help="""Confidence level for contours""")
parser.add_argument(
    '--x-title', default='m_{A} (GeV)', help="""Title for the x-axis""")
parser.add_argument(
    '--y-title', default='tan#beta', help="""Title for the y-axis""")
parser.add_argument(
    '--x-range', default=None, type=str, help="""x-axis range""")
parser.add_argument(
    '--y-range', default=None, type=str, help="""y-axis range""")
parser.add_argument(
    '--cms-sub', default='Internal', help="""Text below the CMS logo""")
parser.add_argument(
    '--scenario-label', default='', help="""Scenario name to be drawn in top
    left of plot""")
parser.add_argument(
    '--title-right', default='', help="""Right header text above the frame""")
parser.add_argument(
    '--title-left', default='', help="""Left header text above the frame""")
parser.add_argument(
    '--logy', action='store_true', help="""Draw y-axis in log scale""")
parser.add_argument(
    '--logx', action='store_true', help="""Draw x-axis in log scale""")
parser.add_argument(
    '--force-x-width', type=float, default=None, help="""Use this x bin width in
    BinCenterAligned mode""")
parser.add_argument(
    '--force-y-width', type=float, default=None, help="""Use this y bin width in
    BinCenterAligned mode""")
parser.add_argument(
    '--hist', default=None, help="""Draw this TGraph2D as a histogram with
    COLZ""")
parser.add_argument(
    '--model-hist', default=None, help="""Draw this TGraph2D from model file as a 
    histogram with COLZ""")
parser.add_argument(
    '--z-range', default=None, type=str, help="""z-axis range of the COLZ
    hist""")
parser.add_argument(
    '--z-title', default=None, help="""z-axis title of the COLZ hist""")
parser.add_argument(
    '--extra_contour_file', default=None, help="""Root file containing graphs
    to be superimposed on plots""")
parser.add_argument(
    '--extra_contour_title', default="", help="""Legend label for extra
    contours""")
parser.add_argument(
    '--extra_contour_style', default="", help="""Line style for plotting
    extra contours""")
parser.add_argument(
    '--model_file', default=None, help="""Model file for drawing mh
    exclusion""")
parser.add_argument(
    '--mass_histogram', default="m_h", help="""Specify histogram to extract
     mh exclusion from""")
args = parser.parse_args()


plot.ModTDRStyle(r=0.06 if (args.hist or args.model_hist) is None else 0.17, l=0.12)
ROOT.gStyle.SetNdivisions(510, 'XYZ')
plot.SetBirdPalette()

file = ROOT.TFile(args.input)
types = args.contours.split(',')
CL = 1 - args.CL

lumi='35.9'
if '300.0' in args.output: lumi='300.0'
if '3000.0' in args.output: lumi='3000.0'

mod=''
if 'hmssm' in args.output: mod='hmssm'
elif 'tauphobic' in args.output: mod='tauphobic'

scen=''
if 'scen2' in args.output: scen='scen2'
if 'scen2_nobbb' in args.output: scen='scen2_nobbb'


# Object storage
graphs = {c: file.Get(c) for c in types}
hists = {}
contours = {}

h_proto = plot.TH2FromTGraph2D(graphs[types[0]], method=args.bin_method,
                               force_x_width=args.force_x_width,
                               force_y_width=args.force_y_width)
h_axis = h_proto
h_axis = plot.TH2FromTGraph2D(graphs[types[0]])


# Get histogram to plot m_h exclusion from the model file if provided
if args.model_file is not None:
    modelfile = ROOT.TFile(args.model_file)
    h_mh = modelfile.Get(args.mass_histogram)
else:
    h_mh = None

#Get extra contours from file, if provided:
if args.extra_contour_file is not None:
    contour_files  = args.extra_contour_file.split(',')
    extra_contours = []
    for filename in contour_files:
        extra_contour_file = ROOT.TFile(filename)
        extra_contour_file_contents = extra_contour_file.GetListOfKeys()
        extra_contour_names = []
        for i in range(0,len(extra_contour_file_contents)):
            extra_contour_names.append(extra_contour_file_contents[i].GetName())
            extra_contours_per_index = [extra_contour_file.Get(c) for c in extra_contour_names]
        extra_contours.append(extra_contours_per_index)
else:
    extra_contours = None

# Create the debug output file if requested
if args.debug_output is not None:
    debug = ROOT.TFile(args.debug_output, 'RECREATE')
else:
    debug = None

# Fill TH2s by interpolating the TGraph2Ds, then extract contours
for c in types:
    print 'Filling histo for %s' % c
    hists[c] = h_proto.Clone(c)
    plot.fillTH2(hists[c], graphs[c])
    manip(hists[c],c,mod,lumi)
    contours[c] = plot.contourFromTH2(hists[c], CL, 5, frameValue=1)
    if debug is not None:
        debug.WriteTObject(hists[c], 'hist_%s' % c)
        for i, cont in enumerate(contours[c]):
            debug.WriteTObject(cont, 'cont_%s_%i' % (c, i))

#Extract mh contours if mh histogram exists:
if h_mh is not None:
  h_mh_inverted = h_mh.Clone("mhInverted")
  for i in range(1,h_mh.GetNbinsX()+1):
     for j in range(1, h_mh.GetNbinsY()+1):
         mh_=h_mh.GetBinContent(i,j)
         mh_inv=1./mh_ if mh_>0.1 else 0.001
#         h_mh_inverted.SetBinContent(i,j,1-(1./h_mh.GetBinContent(i,j)))
         h_mh_inverted.SetBinContent(i,j,1-mh_inv)
  mh122_contours = plot.contourFromTH2(h_mh_inverted, (1-1./122), 5, frameValue=1)
  mh128_contours = plot.contourFromTH2(h_mh, 128, 5, frameValue=1)
else : 
  mh122_contours = None
  mh128_contours = None

# Setup the canvas: we'll use a two pad split, with a small top pad to contain
# the CMS logo and the legend
canv = ROOT.TCanvas(args.output, args.output)
pads = plot.TwoPadSplit(0.8, 0, 0)
pads[1].cd()
h_axis.GetXaxis().SetTitle(args.x_title)
h_axis.GetYaxis().SetTitle(args.y_title)
if args.x_range is not None:
    h_axis.GetXaxis().SetRangeUser(float(args.x_range.split(',')[0]),float(args.x_range.split(',')[1]))
if args.y_range is not None:
    h_axis.GetYaxis().SetRangeUser(float(args.y_range.split(',')[0]),float(args.y_range.split(',')[1]))
h_axis.GetXaxis().SetNdivisions(5,5,0)
h_axis.Draw()

if args.hist is not None:
    colzhist = h_proto.Clone(c)
    plot.fillTH2(colzhist, file.Get(args.hist))
    colzhist.SetContour(255)
    colzhist.Draw('COLZSAME')
    colzhist.GetZaxis().SetLabelSize(0.03)
    if args.z_range is not None:
        colzhist.SetMinimum(float(args.z_range.split(',')[0]))
        colzhist.SetMaximum(float(args.z_range.split(',')[1]))
    if args.z_title is not None:
        colzhist.GetZaxis().SetTitle(args.z_title)

if args.model_hist is not None:
    colzhist = modelfile.Get(args.model_hist)
    colzhist.SetContour(255)
    colzhist.Draw('COLZSAME')
    colzhist.GetZaxis().SetLabelSize(0.03)
    if args.z_range is not None:
        colzhist.SetMinimum(float(args.z_range.split(',')[0]))
        colzhist.SetMaximum(float(args.z_range.split(',')[1]))
    if args.z_title is not None:
        colzhist.GetZaxis().SetTitle(args.z_title)

pads[1].SetLogy(args.logy)
pads[1].SetLogx(args.logx)
pads[1].SetTickx()
pads[1].SetTicky()
# h_proto.GetXaxis().SetRangeUser(130,400)
# h_proto.GetYaxis().SetRangeUser(1,20)

fillstyle = 'FSAME'
if (args.hist or args.model_hist) is not None:
    fillstyle = 'LSAME'

# Now we draw the actual contours
if 'exp-2' in contours and 'exp+2' in contours:
    for i, gr in enumerate(contours['exp-2']):
        plot.Set(gr, LineColor=0, FillColor=ROOT.kGray + 0, FillStyle=1001)
        if (args.hist or args.model_hist) is not None:
            plot.Set(gr, LineColor=ROOT.kGray + 0, LineWidth=2)
        gr.Draw(fillstyle)
if 'exp-1' in contours and 'exp+1' in contours:
    for i, gr in enumerate(contours['exp-1']):
        plot.Set(gr, LineColor=0, FillColor=ROOT.kGray + 1, FillStyle=1001)
        if (args.hist or args.model_hist) is not None:
            plot.Set(gr, LineColor=ROOT.kGray + 1, LineWidth=2)
        gr.Draw(fillstyle)
    fill_col = ROOT.kGray+0
    # If we're only drawing the 1 sigma contours then we should fill with
    # white here instead
    if 'exp-2' not in contours and 'exp+2' not in contours:
        fill_col = ROOT.kWhite
    for i, gr in enumerate(contours['exp+1']):
        plot.Set(gr, LineColor=0, FillColor=fill_col, FillStyle=1001)
        if (args.hist or args.model_hist) is not None:
            plot.Set(gr, LineColor=ROOT.kGray + 1, LineWidth=2)
        gr.Draw(fillstyle)
if 'exp-2' in contours and 'exp+2' in contours:
    for i, gr in enumerate(contours['exp+2']):
        plot.Set(gr, LineColor=0, FillColor=ROOT.kWhite, FillStyle=1001)
        if (args.hist or args.model_hist) is not None:
            plot.Set(gr, LineColor=ROOT.kGray + 0, LineWidth=2)
        gr.Draw(fillstyle)
if 'exp0' in contours:
    for i, gr in enumerate(contours['exp0']):
        if (args.hist or args.model_hist) is not None:
            plot.Set(gr, LineWidth=2)
        if 'obs' in contours:
            plot.Set(gr, LineColor=ROOT.kBlack, LineStyle=2)
            gr.Draw('LSAME')
        else:
            plot.Set(gr, LineStyle=2, FillStyle=1001,
                     FillColor=plot.CreateTransparentColor(
                        ROOT.kSpring + 6, 0.5))
            gr.Draw(fillstyle)
            gr.Draw('LSAME')
if 'obs' in contours:
    for i, gr in enumerate(contours['obs']):
        plot.Set(gr, FillStyle=1001, FillColor=plot.CreateTransparentColor(
            ROOT.kAzure + 6, 0.5))
        if (args.hist or args.model_hist) is not None:
            plot.Set(gr, LineWidth=2)
        gr.Draw(fillstyle)
        gr.Draw('LSAME')

if mh122_contours is not None:
    for i, gr in enumerate(mh122_contours):
        plot.Set(gr, LineWidth=2, LineColor=ROOT.kRed,FillStyle=3004,FillColor=ROOT.kRed)
        gr.Draw(fillstyle)
        gr.Draw('LSAME')
    for i, gr in enumerate(mh128_contours):
        plot.Set(gr, LineWidth=2, LineColor=ROOT.kRed,FillStyle=3004,FillColor=ROOT.kRed)
        gr.Draw(fillstyle)
        gr.Draw('LSAME')

if extra_contours is not None:
    if args.extra_contour_style is not None: 
        contour_styles = args.extra_contour_style.split(',')
    for i in range(0,len(extra_contours)):
        for gr in extra_contours[i]:
            plot.Set(gr,LineWidth=2,LineColor=ROOT.kBlue,LineStyle=int(contour_styles[i]))
            gr.Draw('LSAME')
   

# We just want the top pad to look like a box, so set all the text and tick
# sizes to zero
pads[0].cd()
h_top = h_axis.Clone()
plot.Set(h_top.GetXaxis(), LabelSize=0, TitleSize=0, TickLength=0)
plot.Set(h_top.GetYaxis(), LabelSize=0, TitleSize=0, TickLength=0)
h_top.Draw()

# Draw the legend in the top TPad
legend = plot.PositionedLegend(0.4, 0.11, 3, 0.015)
plot.Set(legend, NColumns=2, Header='#bf{%.0f%% CL Excluded:}' % (args.CL*100.))
if 'obs' in contours:
    legend.AddEntry(contours['obs'][0], "Observed", "F")
if 'exp-1' in contours and 'exp+1' in contours:
    legend.AddEntry(contours['exp-1'][0], "68% expected", "F")
if 'exp0' in contours:
    if 'obs' in contours:
        legend.AddEntry(contours['exp0'][0], "Expected", "L")
    else:
        legend.AddEntry(contours['exp0'][0], "Expected", "F")
if 'exp-2' in contours and 'exp+2' in contours:
    legend.AddEntry(contours['exp-2'][0], "95% expected", "F")
if extra_contours is not None:
    if args.extra_contour_title is not None: 
        contour_title = args.extra_contour_title.split(',')
    for i in range(0,len(contour_title)): 
        legend.AddEntry(extra_contours[i][0],contour_title[i],"L")
legend.Draw()

# Draw logos and titles
plot.DrawCMSLogo(pads[0], 'CMS', args.cms_sub, 11, 0.045, 0.15, 1.0, '', 1.0)
plot.DrawTitle(pads[0], args.title_right, 3)
plot.DrawTitle(pads[0], args.title_left, 1)


# Redraw the frame because it usually gets covered by the filled areas
pads[1].cd()
pads[1].GetFrame().Draw()
pads[1].RedrawAxis()

if mh122_contours is not None and len(mh122_contours)>0:
    lx=0.6
    ly=0.18
    if mod=='tauphobic':
      lx=0.19
      ly=0.63
    legend2 = ROOT.TLegend(lx,ly,lx+0.32,ly+0.05, '', 'NBNDC')
#    legend2 = ROOT.TLegend(0.6, 0.18 , 0.92, 0.23, '', 'NBNDC')
    #legend2 = plot.PositionedLegend(0.4, 0.11, 3, 0.015)
    legend2.AddEntry(mh122_contours[0], "m_{h}^{MSSM} #neq 125 #pm 3 GeV","F")
    legend2.Draw()


# Draw the scenario label
latex = ROOT.TLatex()
latex.SetNDC()
latex.SetTextSize(0.04)
latex.DrawLatex(0.155, 0.75, args.scenario_label)

canv.Print('.pdf')
canv.Print('.png')
#canv.Print('.root')
canv.Close()

if debug is not None:
    debug.Close()
