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

t_end = int(130e3)         # in yr

# dtt_vec = np.array([1., 2., 5., 10.])
dtt_vec = np.array([1.])

for dtt in dtt_vec:
    output_folder = "qnl_dtt."+str(dtt)+"_tend."+str(t_end)
    cmd = "./runylmox -r -e ismip6 -n par/yelmo_ismip6_Antarctica_AQEF_qnl.nml -o output/aqef_retreat/"+output_folder
    cmd+= " -p tf_corr_ant.ronne=0.25 tf_corr_ant.ross=0.2 tf_corr_ant.pine=-0.5"
    cmd+=" yelmo.restart=\"/media/Data/ice_data/Antarctica/ANT-32KM/Restart/ANT-32KM_QUAD-NL-dT_OPT_J20.nc\""
    cmd+= " hysteresis_proj.time_end="+str(t_end)
    cmd+= " hysteresis_proj.dtt="+str(dtt)
    cmd+= " hyster.dt_init=1e3"
    cmd+= " hyster.f_max=5.5"

    # print(cmd)
    subprocess.call(cmd, shell=True)
    # print("Retreat experiment correctly started...")

"""
./runylmox -r -e ismip6 -n par/yelmo_ismip6_Antarctica_AQEF.nml -o output/aqef/dtt=0.5yr -p tf_corr_ant.ronne=0.25 tf_corr_ant.ross=0.2 tf_corr_ant.pine=-0.5 hysteresis_proj.time_end=300000 hysteresis_proj.dtt=0.5
"""