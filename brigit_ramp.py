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
from collections import defaultdict   # Allow nested dictionnaries.

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

batch_size = 30
f_resolution = 0.1
dfdt_vec = np.flip(np.round(np.arange(0.01, 0.06, 0.01), 2))        # flip to have most interesting exp at begin
fmax_vec = np.flip(np.round(np.arange(4.7, 5.3, f_resolution), 2))

param = defaultdict(dict)

i = 0
for fmax in fmax_vec:
    for dfdt in dfdt_vec:
        if i%batch_size==0: print("----------------Starting batch n°",int(i/5),"----------------")

        dt_ramp = np.round(fmax/dfdt, 2)
        cmd = "python2 run_my_yelmo.py -l -f -a output/ramp/"
        cmd+= " \&tf_corr_ant=\"ronne=0.25 ross=0.2 pine=-0.5\"  \&hysteresis_proj=\"time_end=75e3\" \&hyster=\"dt_init=5e3 "
        cmd+= "dt_ramp="+str(dt_ramp)
        cmd+= " fmax="+str(fmax)+"\""

        print(cmd)
        # subprocess.call(cmd, shell=True)
        i += 1