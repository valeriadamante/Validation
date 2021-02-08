from ROOT import *
import argparse
import json
from numpy import *
import os
import shutil
import write_index
import ROOT as rt
import CMS_lumi, tdrstyle
import array

gROOT.SetBatch(kFALSE)

#set the tdr style
tdrstyle.setTDRStyle()
#change the CMS_lumi variables (see CMS_lumi.py)
CMS_lumi.writeExtraText = 1
CMS_lumi.extraText = "Simulation"
CMS_lumi.lumi_sqrtS = "14 TeV" # used with iPeriod = 0, e.g. for simulation-only plots (default is an empty string)

iPos = 11
if( iPos==0 ): CMS_lumi.relPosX = 0.12

H_ref = 600;
W_ref = 800;
W = W_ref
H  = H_ref

iPeriod = 0

# references for T, B, L, R
T = 0.08*H_ref
B = 0.12*H_ref
L = 0.13*W_ref
R = 0.04*W_ref




class histomaker:
    top_level_dir = "CMSSW_11_2_0_phase2"
    opt_stat = 1111
    color_list = [kBlack, kBlue, kRed, kGreen, kOrange, kYellow, kAzure+8, kPink+6, kViolet+1]
    stop = True
    base_path = ""
    variables = ["Delta_X_vs_Eta", "Delta_X", "Delta_X_vs_Phi", "Pull_X_vs_Eta", "Pull_X_vs_Phi", "Delta_Y_vs_Eta", "Delta_Y_vs_Phi", "Pull_Y_vs_Eta", "Pull_Y_vs_Phi"]
    directories = ["TrackerPhase2"]
    subdirectories_names= ["RecHit/", "RecHitV/", "Digi/", "Cluster/"]
    subdirectories = {"IT": subdirectories_names, "OT": subdirectories_names}

    #variables = ["Pull_Y_vs_Eta", "Pull_Y_vs_Phi"]
    #directories = ["TrackerPhase2"]
    #subdirectories_names= ["RecHit/", "RecHitV/"]
    #subdirectories = {"IT": subdirectories_names}

    files_open = []
    paths_file_name="all_paths.txt"
    paths = []

    def open_files(self, input_files):
        for file in input_files:
            self.files_open.append(TFile(file, "READ"))

    def __init__(self, input_files):
        self.input_files = input_files
        self.open_files(input_files)

    def search_paths(self):
        full_paths = []
        for key in self.subdirectories:
            for i in self.subdirectories[key]:
                full_paths.append(self.directories[0]+key+i)
        with open(self.paths_file_name, 'r') as paths_file:
            for line in paths_file.read().splitlines():
                for i in full_paths:
                        for j in self.variables:
                            if i in line and j in line: # and "Barrel/Layer1" in line :
                                self.paths.append(line)

    def histo_name(self, path):
        histo_name = ""
        substrings = path.split("/")
        # reverse order
        histo_name = substrings[-1]
        for i, p in enumerate(substrings):
            if i>3  and i<len(path.split("/"))-1:
                if i < len(path.split("/"))-1:
                    histo_name = histo_name + "_"
                histo_name = histo_name + p
        # normal order
        '''
        for i, p in enumerate(substrings):
            if i>3  and i<len(path.split("/")):
                if i < len(path.split("/"))-1:
                    histo_name = histo_name + "_"
                histo_name = histo_name + p
        '''
        return histo_name

    def get_hist_title(self, file_name):
        i=0
        title =""
        for p in file_name.split("_"):
            if i>3:
                if ".root" in p:
                    p=p.rstrip('.root')
                title=title+p+" "
            i=i+1
        return title

    def dir_name(self, path):
        dir_name = self.top_level_dir+"/"
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        write_index.write_php_file(dir_name)
        for key in self.subdirectories:
            for i in self.subdirectories[key]:
                 if key in path and i in path:
                     dir_name = dir_name + key + "/"
                     if not os.path.exists(dir_name):
                         os.makedirs(dir_name)
                     write_index.write_php_file(dir_name)
                     dir_name = dir_name + i
                     if not os.path.exists(dir_name):
                        os.makedirs(dir_name)
                     write_index.write_php_file(dir_name)
        return dir_name

    def canvas_style(self, canvas):
        canvas.SetFillColor(0)
        canvas.SetBorderMode(0)
        canvas.SetFrameFillStyle(0)
        canvas.SetFrameBorderMode(0)
        canvas.SetLeftMargin( L/W )
        canvas.SetRightMargin( R/W )
        canvas.SetTopMargin( T/H )
        canvas.SetBottomMargin( B/H )
        canvas.SetTickx(0)
        canvas.SetTicky(0)
        return canvas

    def profile_style(self, profile, i):
        y_min = profile.GetMinimum()
        y_max = profile.GetMaximum()
        profile.BuildOptions(y_min*0.1,y_max*1.1,"")
        profile.SetMarkerSize(1)
        profile.SetMarkerStyle(22)
        profile.SetMarkerColor(self.color_list[i])
        return profile

    def stat_style(self, s, i, position):
        s.SetTextColor(self.color_list[i])
        s.SetX1NDC(position[0])
        s.SetX2NDC(position[1])
        s.SetY1NDC(position[2])
        s.SetY2NDC(position[3])
        s.SetFillStyle(1)
        return s

    def draw_histograms(self):
        self.search_paths()
        gStyle.SetOptStat(1111)
        for path in self.paths:
            position = [0.75, 0.959, 0.73, 0.92]
            histo_name = self.histo_name(path)
            dir_name = self.dir_name(path)
            i=0
            canvas = TCanvas("c2","c2",50,50,W,H)
            canvas = self.canvas_style(canvas)
            for file in self.files_open:
                c1=TCanvas()
                c1.cd()
                file.cd()
                htemp = file.Get(path)
                htemp.SetName(self.get_hist_title(self.input_files[i]))
                options = ""
                if "TH1" in htemp.ClassName():
                    htemp.SetLineColor(self.color_list[i])
                elif "TProfile" in htemp.ClassName():
                    htemp = self.profile_style(htemp, i)
                    options = options+ "hist p"
                htemp.SetStats(1)
                htemp.GetYaxis().SetTitleOffset(1.2)
                htemp.Draw()
                gPad.Update()
                canvas.cd()
                s= htemp.GetListOfFunctions().FindObject("stats")
                if i>0:
                    options = options+ "sames"
                    position[2]= position[2]-0.5
                    position[3]= position[3]-0.5
                s = self.stat_style(s, i, position)
                print s.GetName()
                i=i+1
                htemp.Draw(options)
                CMS_lumi.CMS_lumi(canvas, iPeriod, iPos)
                canvas.cd()
                frame = canvas.GetFrame()
                frame.Draw()
                canvas.Update()
            #ciao  = raw_input("ciao")
            canvas.Print(dir_name+histo_name+".png", "png")
            #canvas.Print(dir_name+histo_name+".pdf", "pdf")

parser = argparse.ArgumentParser()
parser.add_argument('machine', type=str, default="pccms65", choices=["lxplus", "local"])
parser.add_argument('--reference', required=True, type=str, help= "input reference file")
parser.add_argument('--targets', required=True, type=str, help= "input target files to compare separated by comma")
parser.add_argument('--variables', required=False, type=str, default= "", help= "input variables separated by comma")
parser.add_argument('--txtname', required=False, type=str, default="all_paths", help= "txt file with all paths")
parser.add_argument('--dirsuffix', required=False, type=str, default="", help="additional suffix for base directory name")
parser.add_argument('--topdir', required=False, type=str, default="../CMSSW_11_2_0_phase2", help="base directory name")
args = parser.parse_args()

# ****** dictionary for in/out directories ******
dir_dict = {}
dir_dict["local"]={}
dir_dict["local"]["input"]="/Users/valeriadamante/Desktop/Dottorato/public/CMSSW_11_2_0_pre9/src/RootFiles/"
dir_dict["local"]["output"]="/Users/valeriadamante/Desktop/Dottorato/public/CMSSW_11_2_0_pre9/src/"

dir_dict["lxplus"]={}
dir_dict["lxplus"]["input"]="/afs/cern.ch/work/v/vdamante/public/CMSSW_11_2_0_pre9/src/RootFiles/"
dir_dict["lxplus"]["output"]="/afs/cern.ch/work/v/vdamante/public/CMSSW_11_2_0_pre9/src/"#"/eos/home-v/vdamante/www/phase2validation/"

input_dir = dir_dict[args.machine]["input"]
out_dir =  dir_dict[args.machine]['output']

# **** create txt file with all paths  ****
input_files_str = args.reference+","+args.targets
if not os.path.exists(args.txtname+".txt"):
    command="root -l -b make_histogram.cpp+O\(\\\""+input_files_str+"\\\",\\\""+args.txtname+"\\\"\)"
    print command
    os.system(command)

# **** create list of files ****
input_files = []
input_files.append(input_dir+args.reference)
for file in (input_dir+args.targets).split(","):
    input_files.append(file)

# **** initialize the class and its values ****
make_histogram = histomaker(input_files)
make_histogram.file_name=args.txtname+".txt"                            # file name with paths
make_histogram.top_level_dir = out_dir+args.topdir+args.suffix          # base directory name

# **** eventually initialize variables ****
variables =[]
if args.variables != "":
    for var in (args.variables).split(","):
        variables.append(var)
    make_histogram.variables = variables

# **** draw histograms ****
make_histogram.draw_histograms()
