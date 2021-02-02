from ROOT import *
import argparse
import json
from numpy import *
import os
import shutil
import write_index

gROOT.SetBatch(kFALSE)

class histomaker:
    top_level_dir = "CMSSW_11_2_0_phase2"
    opt_stat = 1111
    color_list = [kBlack, kBlue, kRed, kGreen, kOrange, kYellow, kAzure+8, kPink+6, kViolet+1]
    stop = True
    base_path = ""
    variables = ["Delta_X_vs_Eta", "Delta_X_vs_Phi", "Pull_X_vs_Eta", "Pull_X_vs_Phi", "Delta_Y_vs_Eta", "Delta_Y_vs_Phi", "Pull_Y_vs_Eta", "Pull_Y_vs_Phi"]
    directories = ["TrackerPhase2ITRecHitV"]
    subdirectories = ["Barrel", "EndCap_Side1", "EndCap_Side2",]
    files_open = []
    paths_file_name="all_paths.txt"
    paths = []
    additional_suffix = ""

    def open_files(self, input_files):
        for file in input_files:
            self.files_open.append(TFile(file, "READ"))

    def __init__(self, input_files):
        self.input_files = input_files
        self.open_files(input_files)

    def search_paths(self):
        with open(self.paths_file_name, 'r') as paths_file:
            for line in paths_file.read().splitlines():
                if self.directories[0] in line:
                    for i in self.subdirectories:
                        if i in line:
                            for j in self.variables:
                                if j in line:
                                    self.paths.append(line)

    def fill_dirs(self, path):
        dirs = []
        i=0
        for p in path.split("/"):
            if i<=1 or i==3:
                pass
            else:
                dirs.append(p)
            i=i+1
        return dirs

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

    def make_dir(self, path, dirs):
        dir_name=self.top_level_dir+self.additional_suffix+"/"
        shutil.copy("index.php", dir_name)
        i=0
        for d in dirs:
            dir_name= dir_name+ d+"/" 
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            write_index.write_php_file(dir_name)
        return dir_name

    def draw_histograms(self):
        self.search_paths()
        gStyle.SetOptStat(1111)
        for path in self.paths:
            dirs = self.fill_dirs(path)
            dir_name= self.make_dir(path, dirs)
            write_index.write_php_file(dir_name)
            i=0
            c = TCanvas()
            for file in self.files_open:
                c1=TCanvas()
                c1.cd()
                file.cd()
                htemp = file.Get(path)
                htemp.SetName(self.get_hist_title(self.input_files[i]))
                options = ""
                htemp.SetStats(0)
                htemp.SetStats(1)
                if "TH1" in htemp.ClassName():
                    htemp.SetLineColor(self.color_list[i])
                    htemp.Draw()
                elif "TProfile" in htemp.ClassName():
                    y_min = htemp.GetYmin()
                    y_max = htemp.GetYmax()
                    htemp.BuildOptions(y_min*0.5,y_max*1.5,"")
                    htemp.SetMarkerSize(1)
                    htemp.SetMarkerStyle(22)
                    htemp.SetMarkerColorAlpha(self.color_list[i], i/(i+1))
                    htemp.Draw()
                    options += "p HIST"
                gPad.Update()
                c.cd()
                s= htemp.GetListOfFunctions().FindObject("stats")
                s.SetTextColor(self.color_list[i])
                previous_position= [s.GetY1NDC(), s.GetY2NDC()]
                if i>0:
                    options += "sames"
                    s.SetOptStat(1111)
                    s.SetY1NDC(previous_position[0]-0.6)
                    s.SetY2NDC(previous_position[1]-0.6)
                i=i+1
                htemp.Draw(options)
                c.Update()
                gPad.Update()
                c.Print(dir_name+dirs[len(dirs)-1]+".png", "png")
                #c.Print(dir_name+dirs[len(dirs)-1]+".pdf", "pdf")

parser = argparse.ArgumentParser()
parser.add_argument('--reference', required=True, type=str, help= "input reference file")
parser.add_argument('--targets', required=True, type=str, help= "input target files to compare separated by comma")
parser.add_argument('--variables', required=False, type=str, default= "", help= "input variables separated by comma")
parser.add_argument('--directories', required=False, type=str, default="TrackerPhase2ITRecHitV", help= "input directories to explore separated by comma")
parser.add_argument('--txtname', required=False, type=str, default="all_paths", help= "txt file with all paths")
parser.add_argument('--dirname', required=False, type=str, default="", help="additional suffix for base directory name")


args = parser.parse_args()
input_files = []
input_files_str = args.reference+","+args.targets
if not os.path.exists(args.txtname+".txt"):
    command="root -l -b make_histogram.cpp+O\(\\\""+input_files_str+"\\\",\\\""+args.txtname+"\\\"\)"
    print command
    os.system(command)

input_files.append(args.reference)
for file in (args.targets).split(","):
    input_files.append(file)

make_histogram = histomaker(input_files)
histomaker.additional_suffix=args.dirname
variables =[]
if(args.variables != ""):
    for var in (args.variables).split(","):
        variables.append(var)
    make_histogram.variables = variables
make_histogram.draw_histograms()
