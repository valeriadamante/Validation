echo # Validation
# Validation

In this repository there are only the scripts to produce the plots for DQM.
How to run the scripts:
1. the python file accepts the following strings arguments:
  1.0) 'machine' --> required, possible choices [local, lxplus]. These ones are used in the directories dictionary. However it has to be customised with your local and lxplus input/output directories.

  1.1) '--reference'  required -->  reference file. It will be drawn in black

  1.2) '--targets'    required -->  target file(s) to compare. Must be written separated by comma (max number is 8).
  They will be drawn in different colors. The first color is blue.

  1.3) '--variables'  not necessary required, variables, must be written separated by comma. Since the default value is
  "", if it is not written a set of variables is prepared to be plotted, written in line 20.

  1.4) '--txtname'    not necessary required. This is the txt file with all paths, with a default value of "all_paths".
  If it is not given in input, the algo will search for the "all_paths.txt" file and if it does not find it, the CPP
  algo will be run to produce it.

  1.5) '--topdir'  not necessary required. It is an additional suffix for base directory name, and its default value
  is "CMSSW_11_2_0_phase2"

  1.5) '--dirsuffix'  not necessary required. It is an additional suffix for base directory name, and its default value
  is empty string

2. The cpp file runs over the files and produces a file with all paths or a subset of paths according
to different given options. It's run by python scripts if it does not find the txt file with all paths.

Here you find some examples:
- Simple one:
  ```python make_histogram.py local --reference DQM_V0001_R000000001__Global__CMSSW_11_2_0_pre10__RECO.root --targets DQM_V0001_R000000001__Global__CMSSW_11_3_0_pre1__RECO.root --dirsuffix _RECO ```

  reference file = DQM_V0001_R000000001__Global__CMSSW_11_2_0_pre10__RECO.root
  target file = DQM_V0001_R000000001__Global__CMSSW_11_3_0_pre1__RECO.root
  directory suffix = _RECO

######### To be added #######

Take in input files coming from internet
