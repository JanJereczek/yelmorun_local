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
     os.chdir("/home/jan/yelmo-ucm/yelmox_v1.75/")

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
param_dict["hysteresis_proj.time_end"] = 5e3        # yr
param_dict["hysteresis_proj.dtt"] = 1.0             # yr
param_dict["hysteresis_proj.dt2D_out"] = 1e3        # yr
param_dict["hysteresis.dt2D_small_out"] = 1e2       # yr
param_dict["hyster.dt_init"] = 10e3                 # yr
param_name = param_dict.keys()

output_folder = "control_16km"
cmd = "./runylmox -r -e ismip6 -n par/yelmo_ismip6_Antarctica_Rtip.nml -o output/"+output_folder
cmd+= " -p yelmo.grid_name=\"ANT-16KM\" ctrl.run_step=\"hysteresis_proj\" yelmo.restart=\"/home/jan/yelmo-ucm/yelmox_v1.75/output/spinup_16km/yelmo_restart.nc\""

for name in param_name:
    cmd+= " "+name+"="+str(param_dict[name])

# print(cmd)
subprocess.call(cmd, shell=True)