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
param_dict["spinup_ismip6.time_end"] = 20e3     # yr
param_dict["spinup_ismip6.dtt"] = 1.0           # yr
param_dict["spinup_ismip6.dt2D_out"] = 1e3      # yr

param_name = param_dict.keys()

output_folder = "spinup_16km"
cmd = "./runylmox -r -e ismip6 -n par/yelmo_ismip6_Antarctica_Rtip.nml -o output/"+output_folder
cmd+= " -p yelmo.grid_name=\"ANT-16KM\""

for name in param_name:
    cmd+= " "+name+"="+str(param_dict[name])

# print(cmd)
subprocess.call(cmd, shell=True)