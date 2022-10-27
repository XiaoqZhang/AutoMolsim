import hydra
from omegaconf import DictConfig, OmegaConf

import os
import shutil

from src.cells import *
from src.raspa import *
from src.script import *

@hydra.main(version_base=None, config_path="conf", config_name="config")
def run(cfg: DictConfig) -> None:
     
    assert cfg.machine.name in ["local", "fidis"], "Unknown machine!"
    assert cfg.task.name in ["henry", "nvt", "gcmc"], "Unknown task!"

    # create output directory
    if not os.path.exists(cfg.out_dir):
        os.mkdir(cfg.out_dir) 

    # read cif list
    structure_list = os.listdir(cfg.cif_dir)
    structures = [s.rsplit('.', 1)[0] for s in structure_list]
    for structure in structures:
        unitcell = extract_geometry(os.path.join(cfg.cif_dir, structure+".cif"))

        # create a folder for each structure
        sim_dir = os.path.join(cfg.out_dir, structure)
        if not os.path.exists(sim_dir):
            os.mkdir(sim_dir)
        shutil.copyfile(os.path.join(cfg.cif_dir, structure+".cif"), 
                        os.path.join(sim_dir, structure+".cif"))

        # check if perform zeo calculation for blocking sphere or not
        if cfg.task.block == "yes":
            zeo(structure.split('.', 1)[0])
            with open(structure.rsplit('.',1)[0] + ".block") as f9:
                if "0" in f9.readline():
                    block = "no"
                else:
                    block = "yes"
                f9.close()
        else:
            block = "no"
    
        # prepare simulation.input
        if cfg.task.name == "nvt":
            print("Generating NVT simulation.input for %s" %structure)
            str_out = nvt(structure = structure, unitcell = unitcell, **cfg.task)
            with open(os.path.join(sim_dir, "simulation.input"), "w") as fo:
                fo.write(str_out)
        elif cfg.task.name == "henry":
            print("Generating KH simulation.input for %s" %structure)
            str_out = henry(structure, unitcell, **cfg.task)
            with open(os.path.join(sim_dir, "simulation.input"), "w") as fo:
                fo.write(str_out)
        elif cfg.task.name == "gcmc":
            print("Generating GCMC simulation.input for %s" %structure)
            str_out = gcmc(structure, unitcell, **cfg.task)
            with open(os.path.join(sim_dir, "simulation.input"), "w") as fo:
                fo.write(str_out)
        
        # prepare shell script
        if cfg.machine.name == "local":
            str_out = local(**cfg.machine)
            with open(os.path.join(sim_dir, "run.sh"), "w") as fo:
                fo.write(str_out)
        elif cfg.machine.name == "fidis":
            str_out = fidis(**cfg.machine)
            with open(os.path.join(sim_dir, "run.sh"), "w") as fo:
                fo.write(str_out)

if __name__ == "__main__":
    run()