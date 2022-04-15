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

# a_rsl = 0.01
# f_rsl = 0.1
a_rsl = 0.02
f_rsl = 0.3
dfdt_vec = np.flip(np.round(np.arange(0.015, 0.055, a_rsl), 3))        # flip to have most interesting exp at begin
fmax_vec = np.flip(np.round(np.arange(4.75, 5.35, f_rsl), 3))

batch_size = 4

param_name = ["hysteresis_proj.time_end", "hyster.dt_init", "hyster.dt_ramp", "hyster.f_max", "hysteresis_proj.dtt"]
param_dict = dict()
param_dict["hyster.dt_init"] = 0e3              # yr
param_dict["hysteresis_proj.time_end"] = 5e2   # yr
param_dict["hysteresis_proj.dtt"] = 1           # yr

i = 0
for fmax in fmax_vec:
    for dfdt in dfdt_vec:
        if i%batch_size==0: print("----------------Starting batch n°",int(i/batch_size),"----------------")
        # print(i, fmax, dfdt)
        param_dict["hyster.f_max"] = fmax
        param_dict["hyster.df_dt_max"] = dfdt
        param_dict["hyster.dt_ramp"] = np.round(fmax/dfdt, 2)
        
        # output_folder = "fmax="+str(fmax)+"_dfdt="+str(dfdt)+"_tend="+\
        #                str(param_dict["hysteresis_proj.time_end"])+"_dtt="+str(param_dict["hysteresis_proj.dtt"])
                        
        output_folder = str(i)
        cmd = "./runylmox -r -e ismip6 -n par/yelmo_ismip6_Antarctica_Rtip.nml -o output/ramp/test/"+output_folder
        cmd+= " -p yelmo.grid_name=\"ANT-16KM\""

        for name in param_name:
            cmd+= " "+name+"="+str(param_dict[name])

        print(cmd)
        # subprocess.call(cmd, shell=True)
        i += 1

        if i%batch_size == 0:
            time.sleep(1)
            print("Checking for running processes")
            ProcessRunning = True
            while ProcessRunning:
                ProcessRunning = checkIfProcessRunning('yelmox_ismip6.x')