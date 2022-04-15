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
import time
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

# Function to check whether yelmox is running --> wait until simulation is over.
def checkIfProcessRunning(processName):
    '''
    Check if there is any running process that contains the given name processName.
    '''
    #Iterate over the all the running process
    for proc in psutil.process_iter():
        try:
            # Check if process name contains the given name string.
            if processName.lower() in proc.name().lower():
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False;


#%% ####################################################################################################
####################################### Run command ####################################################
########################################################################################################

with_tfcorr = True

param_dict = dict()
param_dict["spinup.time_end"] = 40e3            # yr
param_dict["spinup.dtt"] = 1.0                  # yr
param_dict["yelmo.restart"] = "\"None\""
param_dict["ctrl.run_step"] = "\"spinup_ismip6\""
param_dict["opt_L21.cf_min"] = 1e-3
param_dict["ytherm.H_w_max"] = 2.0

if with_tfcorr:
    param_dict["ytopo.kt"] = 0.003
    param_dict["tf_corr_ant.ronne"] = 0.25
    param_dict["tf_corr_ant.ross"] = 0.2
    param_dict["tf_corr_ant.pine"] = -0.5

else:
    param_dict["ytopo.kt"] = 0.10e-2
    param_dict["tf_corr_ant.ronne"] = 0.0
    param_dict["tf_corr_ant.ross"] = 0.0
    param_dict["tf_corr_ant.pine"] = 0.0


par_file = "/home/jan/yelmo-ucm/yelmox_v1.662/par/yelmo_ismip6_Antarctica.nml"

cmd = "./runylmox -r -e ismip6 -n "+par_file+" -o output/spinup/with_tfcorr."+str(with_tfcorr)+" -p"

for name in param_dict.keys():
    cmd+= " "+name+"="+str(param_dict[name])

# print(cmd)
subprocess.call(cmd, shell=True)