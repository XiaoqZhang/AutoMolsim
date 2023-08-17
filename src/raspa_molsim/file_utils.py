import os
import shutil
from raspa_molsim.raspa import *

def write_simulation_input(step, path, params):
    if params.name == "henry":
        str_out = henry(**params)
    if params.name == "nvt":
        str_out = nvt(**params) 
    if params.name == "gcmc":
        str_out = gcmc(**params)
    if params.name == "minimization":
        str_out = minimization(**params)
    if params.name == "grid":
        str_out = grid(**params)
    
    if step == 0:
        with open(os.path.join(path, "simulation.input"), "w") as fo:
            fo.write(str_out)
    else: 
        with open(os.path.join(path, "simulation_%s.input" %(step+1)), "w") as fo:
            fo.write(str_out)


def restart_file(out_dir, structure, ori_file_name, restart_file_name):
    # check if RestartInit exists or not
    if not os.path.exists(os.path.join(out_dir, structure, "RestartInitial")):
        os.mkdir(os.path.join(out_dir, structure, "RestartInitial"))
        os.mkdir(os.path.join(out_dir, structure, "RestartInitial/System_0"))
    # copy restart file
    shutil.copy(
        os.path.join(out_dir, structure, "Restart/System_0", ori_file_name),
        os.path.join(out_dir, structure, "RestartInitial/System_0", restart_file_name)
    )