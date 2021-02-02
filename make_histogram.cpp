#include <iostream>
#include <fstream>
#include "TColor.h"
#include "TFile.h"
#include "TKey.h"
#include "TDirectory.h"
#include "TCanvas.h"
#include "TROOT.h"
#include <string.h>
#include <stdio.h>
#include <boost/algorithm/string/replace.hpp>
#include "TStyle.h"
#include "TH1F.h"
#include "TLegend.h"
#include <boost/filesystem/convenience.hpp>
#include <boost/algorithm/string/trim.hpp>
#include <boost/algorithm/string/classification.hpp>
#include <boost/algorithm/string.hpp>
/**/

using namespace std;
int color_list[] = {kBlack, kBlue, kGreen, kRed, kOrange, kYellow, kAzure+8, kPink+6, kViolet+1};
int opt_stat = 1111111;
ofstream file_to_write;

/***** Fill a vector with all the histograms paths *****/
bool explore_paths(TList *keys, vector<string> &paths, TFile *file, std::string directory_name="TrackerPhase2"){
    bool found= false;
    for (auto &&k : *keys) {
        TKey *key = (TKey*)(k);
        if (!strncmp(key->GetClassName(),"TDirectory", 10) ){
            found = true;
            TDirectory *dir = (TDirectory*)key->ReadObj();
            for (auto j : *dir->GetListOfKeys()){
                TKey *j_key = (TKey*)(j);
                if (!strncmp(j_key->GetClassName(),"TDirectory", 10)  ){
                    TDirectory *j_dir = (TDirectory*)j_key->ReadObj();
                    keys->Add(j);
                }
                else{
                    string path_total = static_cast<string>(dir->GetPath())+ "/"+ static_cast<string>(j->GetName());
                    if (path_total.find(directory_name)==string::npos) continue;
                    paths.push_back(path_total);
                    boost::replace_all(path_total, file->GetPath(), "");
                    file_to_write<<path_total << "\n";
                }
            }
            keys->Remove(k);
        }
    }
    return found;
}



/******** Draw histograms ********/
void draw_histograms(string variable, vector<string> paths, vector<TFile*> files){
    gStyle->SetOptStat(opt_stat);
    for (int j = 0; j<(int)paths.size(); j++){
        string canvas_name = paths[j];
        if(canvas_name.find("/")!=string::npos)
            boost::replace_all(canvas_name, "/", "_");
        if(canvas_name.find(" ")!=string::npos)
            boost::replace_all(canvas_name, " ", "_");
        TCanvas *c = new TCanvas(canvas_name.c_str(), canvas_name.c_str(), 10000, 10000);
        int i=0;
        TLegend *legend = new TLegend(0.6, 0.8, 0.9, 0.9);
        for (auto &file : files) {
            c->Update();
            TH1F *htemp=(TH1F*) file->Get(paths[j].c_str());
            htemp->SetLineColor(color_list[i]);
            //htemp->SetTitle(canvas_name.c_str());
            string legend_title = static_cast<string>(file->GetPath());
            legend_title.erase(0, legend_title.find("TeV")+4);
            legend_title.erase(legend_title.find(".root"));
            legend->AddEntry(htemp, legend_title.c_str(), "l");
            i++;
            gPad->SetLeftMargin(0.16);//DQM_RelValTTbar_14TeV_mcRun4_2026D66noPU_pre11
            if (i==0)
                htemp->Draw();
            else
                htemp->Draw("same");
        }
        legend->Draw();
        c->Update();
        if( j==0 )
            c->Print((variable+".pdf(").c_str(), ("Title:"+canvas_name).c_str());
        else if (j==(int)paths.size()-1)
            c->Print((variable+".pdf)").c_str(), ("Title:"+canvas_name).c_str());
        else
            c->Print((variable+".pdf").c_str(), ("Title:"+canvas_name).c_str());
    }

}
/**** Split the string passed ****/
std::vector<std::string> SplitValueList(const std::string& _values_str, bool allow_duplicates,
                                        const std::string& separators, bool enable_token_compress)
{
    std::string values_str = _values_str;
    std::vector<std::string> result;
    if(enable_token_compress)
        boost::trim_if(values_str, boost::is_any_of(separators));
    if(!values_str.size()) return result;
    const auto token_compress = enable_token_compress ? boost::algorithm::token_compress_on
                                                      : boost::algorithm::token_compress_off;
    boost::split(result, values_str, boost::is_any_of(separators), token_compress);
    if(!allow_duplicates) {
        std::unordered_set<std::string> set_result;
        for(const std::string& value : result) {
            if(set_result.count(value))
                cout << "Value " << value << " listed more than once in the value list " << values_str << endl;
            set_result.insert(value);
        }
    }
    return result;
}

int make_histogram(string files, string file_name = "all_paths", string variables = "Delta_X_vs_Eta,Delta_X_vs_Phi,Pull_X_vs_Eta,Pull_X_vs_Phi,Delta_Y_vs_Eta,Delta_Y_vs_Phi,Pull_Y_vs_Eta,Pull_Y_vs_Phi", string interesting_directories = "Run summary,"){
    vector<string> file_list = SplitValueList(files, false, ",", true);
    vector<string> variables_list = SplitValueList(variables, false, ",", true);
    vector<string> directories_list = SplitValueList(interesting_directories, false, ",", true);
    vector<TFile*> files_open;
    for (auto file:file_list){
        TFile *f = new TFile(file.c_str(), "READ");
        files_open.push_back(f);
    }
    file_to_write.open((file_name+".txt").c_str());
    TList *keys = files_open[0]->GetListOfKeys();
    vector<string> paths;
    for (auto directory : directories_list){
        while (explore_paths(keys, paths, files_open[0], directory));
    }
    /*
    for (auto &var : variables_list){
        vector<string> paths_to_pass;
        std::cout << var << std::endl;
        for(auto &path : paths){
            if (path.find(var)!=string::npos){
                std::cout<<path<<std::endl;
                boost::replace_all(path, files_open[0]->GetPath(), ""); // remove root file from path to pass
                paths_to_pass.push_back(path);
            }
        }
        //draw_histograms(var, paths_to_pass, files_open);
    }
    file_to_write.close();*/

return 0;
}
