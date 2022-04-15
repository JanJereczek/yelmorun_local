"""
Author: Jan Swierczek-Jereczek
Date: 17.11.2021

Script to run retreat of WAIS based on AQEF.
It is possible to run this by directly typing the shell command... however that can be very tedious!
"""

#%% ####################################################################################################
##################################### Import packages ##################################################
########################################################################################################
import subprocess
import os
import psutil
import numpy as np

#%% ##########################################################################################
################################### Utilities ################################################
##############################################################################################

# Set yelmox to current folder in order to run the shell commands correctly.
def operateOnFolder(folder):
     os.chdir("/home/jan/yelmo-ucm/yelmox_v1.662/")

for k in os.listdir("."):
    if os.path.isdir(k):
        operateOnFolder(k)

#%% ####################################################################################################
####################################### Run command ####################################################
########################################################################################################

param_dict = dict()
param_dict["hyster.dt_init"] = 10e3             # yr
param_dict["hysteresis_proj.time_end"] = 400e3   # yr
param_dict["hysteresis_proj.dtt"] = 1           # yr
param_dict["yelmo.restart"] = "\"/home/jan/yelmo-ucm/yelmox_v1.662/output/aqef_retreat/dtt.1.0_tend.130000/yelmo_restart.nc\""
param_dict["ytherm.H_w_max"] = 2.0
param_dict["ytopo.kt"] = 0.003
param_dict["tf_corr_ant.ronne"] = 0.25
param_dict["tf_corr_ant.ross"] = 0.2
param_dict["tf_corr_ant.pine"] = -0.5
param_dict["hyster.f_max"] = 5.5


par_file = "/home/jan/yelmo-ucm/yelmox_v1.662/par/yelmo_ismip6_Antarctica_AQEF_regrowth.nml"
output_folder = "dtt."+str(param_dict["hysteresis_proj.dtt"])+"_tend."+str(param_dict["hysteresis_proj.time_end"])

cmd = "./runylmox -r -e ismip6 -n "+par_file+" -o output/aqef_regrowth/"+output_folder+" -p"

for name in param_dict.keys():
    cmd+= " "+name+"="+str(param_dict[name])

# print(cmd)
subprocess.call(cmd, shell=True)