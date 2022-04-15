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
     # os.chdir("/home/jan/yelmo-ucm/old_yelmo_versions/yelmox_v1.42")

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

param_dict = dict()
param_dict["hyster.dt_init"] = 20e3              # yr
param_dict["hysteresis_proj.time_end"] = 20e3   # yr
param_dict["hysteresis_proj.dtt"] = 1           # yr
# param_dict["yelmo.restart"] = "/home/jan/yelmo-ucm/yelmox_v1.662/output/aqef/dtt=1.0yr/yelmo_restart.nc"
# param_dict["yelmo.restart"] = "/home/jan/yelmo-ucm/old_yelmo_versions/yelmox_v1.64/output/yelmo_restart.nc"
param_dict["yelmo.restart"] = "/home/jan/yelmo-ucm/yelmox_v1.662/output/yelmo_restart2.nc"
# param_dict["yelmo.restart"] = "\"/home/jan/yelmo-ucm/old_yelmo_versions/yelmox_v1.64/output/aqef/dtt=1.0yr/yelmo_restart.nc\""

par_file = "/home/jan/yelmo-ucm/yelmox_v1.662/par/yelmo_ismip6_Antarctica.nml"
output_folder = "restart=" + param_dict["yelmo.restart"]

cmd = "./runylmox -r -e ismip6 -n "+par_file+" -o output/restart_test/"+output_folder
cmd+= " -p tf_corr_ant.ronne=0.25 tf_corr_ant.ross=0.2 tf_corr_ant.pine=-0.5"

for name in param_dict.keys():
    print(name)
    cmd+= " "+name+"="+str(param_dict[name])

# print(cmd)
subprocess.call(cmd, shell=True)