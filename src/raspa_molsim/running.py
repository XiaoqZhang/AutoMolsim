import hydra
from omegaconf import DictConfig, OmegaConf

import os
import shutil
import logging
from tqdm import tqdm
import pandas as pd

from raspa_molsim.cells import *
from raspa_molsim.raspa import *
from raspa_molsim.script import *
from raspa_molsim.run_workchain import *
from raspa_molsim.file_utils import *
from raspa_molsim.postprocessing import *

def run_preprocessing(cfg: DictConfig) -> None:
     
    assert cfg.machine.name in ["local", "fidis", "lsmosrv"], "Unknown machine!"
    assert cfg.task.name in ["zeopp" ,"henry", "nvt", "gcmc", "minimization"], "Unknown task!"

    # create output directory
    if not os.path.exists(cfg.out_dir):
        os.mkdir(cfg.out_dir) 

    # read cif list
    structure_list = os.listdir(cfg.cif_dir)
    structures = [s.rsplit('.', 1)[0] for s in structure_list if s.rsplit('.', 1)[-1]=="cif"]
    for structure in tqdm(structures):
        unitcell = extract_geometry(os.path.join(cfg.cif_dir, structure+".cif"), cfg.task.CutOffVDW)

        # create a folder for each structure
        sim_dir = os.path.join(cfg.out_dir, structure)
        if not os.path.exists(sim_dir):
            os.mkdir(sim_dir)
        shutil.copyfile(os.path.join(cfg.cif_dir, structure+".cif"), 
                        os.path.join(sim_dir, structure+".cif"))

        # prepare simulation.input
        if cfg.task.name == "nvt":
            if cfg.task.RestartFile == "yes":
                ori_file_name = "restart_{}_{}.{}.{}_{:.6f}_0".format(structure, unitcell[0], unitcell[1], unitcell[2], cfg.task.last_temperature)
                # sanity check
                try:
                    restart_file_name = "restart_{}_{}.{}.{}_{:.6f}_0".format(structure, unitcell[0], unitcell[1], unitcell[2], cfg.task.ExternelTemperature)
                    restart_file(cfg.out_dir, structure, ori_file_name, restart_file_name)
                except:
                    logging.warning("%s: Restart file doesn't exist!" %structure)
                    # change ExternalTemperature to the last one
                    cfg.task.ExternelTemperature = cfg.task.last_temperature
            str_out = nvt(structure = structure, unitcell = unitcell, **cfg.task)
            with open(os.path.join(sim_dir, "simulation.input"), "w") as fo:
                fo.write(str_out)
        elif cfg.task.name == "henry":
            str_out = henry(structure, unitcell, **cfg.task)
            with open(os.path.join(sim_dir, "simulation.input"), "w") as fo:
                fo.write(str_out)
        elif cfg.task.name == "gcmc":
            str_out = gcmc(structure, unitcell, **cfg.task)
            with open(os.path.join(sim_dir, "simulation.input"), "w") as fo:
                fo.write(str_out)
        elif cfg.task.name == "minimization":
            if cfg.task.RestartFile == "yes":
                ori_file_name = "restart_{}_{}.{}.{}_{:.6f}_0".format(structure, unitcell[0], unitcell[1], unitcell[2], cfg.task.last_temperature)
                # sanity check
                try:
                    restart_file_name = "restart_{}_{}.{}.{}_{:.6f}_0".format(structure, unitcell[0], unitcell[1], unitcell[2], cfg.task.T)
                    restart_file(cfg.out_dir, structure, ori_file_name, restart_file_name)
                except:
                    logging.warning("%s: Restart file doesn't exist!" %structure)
            str_out = minimization(structure, unitcell, **cfg.task)
            with open(os.path.join(sim_dir, "simulation.input"), "w") as fo:
                fo.write(str_out)
        
        # prepare shell script
        if cfg.machine.name == "local":
            str_out = local(**cfg.machine, **cfg.zeo_params, structure=structure+".cif")
            with open(os.path.join(sim_dir, "run.sh"), "w") as fo:
                fo.write(str_out)
        elif cfg.machine.name == "fidis":
            str_out = fidis(**cfg.machine, **cfg.zeo_params, structure=structure+".cif")
            with open(os.path.join(sim_dir, "run.sh"), "w") as fo:
                fo.write(str_out)
        elif cfg.machine.name == "lsmosrv":
            str_out = fidis(**cfg.machine, **cfg.zeo_params, structure=structure+".cif")
            with open(os.path.join(sim_dir, "run.sh"), "w") as fo:
                fo.write(str_out)
           
def run_postprocessing(cfg: DictConfig) -> None:
    # read cif list
    structure_list = os.listdir(cfg.cif_dir)
    structures = [s.rsplit('.', 1)[0] for s in structure_list if s.rsplit('.', 1)[-1]=="cif"]
    
    unfinished = []
    
    if cfg.task.name == "henry":
        khs, kh_devs = [], []
        for structure in tqdm(structures):
            unitcell = extract_geometry(os.path.join(cfg.cif_dir, structure+".cif"), cfg.task.CutOffVDW)

            # get the output folder for each structure
            sim_dir = os.path.join(cfg.out_dir, structure)
            os.chdir(sim_dir)
            kh, kh_dev = read_henry(structure, unitcell, **cfg.task)
            khs.append(kh)
            kh_devs.append(kh_dev)
            if kh is None:
                unfinished.append(structure)
        
        df = pd.DataFrame(
            {
                "cif": structures,
                "%s_kh" %cfg.task.MoleculeName: khs,
                "%s_kh_dev" %cfg.task.MoleculeName: kh_devs
            }
        )
                
    elif cfg.task.name == "gcmc":
        df = pd.DataFrame(
            {
                "cif": structures
            }
        )
        
        for i, com in enumerate(cfg.task.MoleculeName):
            loadings, loading_devs, qs, q_devs = [], [], [], []
            for structure in tqdm(structures):
                unitcell = extract_geometry(os.path.join(cfg.cif_dir, structure+".cif"), cfg.task.CutOffVDW)

                # get the output folder for each structure
                sim_dir = os.path.join(cfg.out_dir, structure)
                os.chdir(sim_dir)
                if len(cfg.task.MoleculeName) > 1:
                    j = i + 1
                else:
                    j = i
                (l, l_dev), (q, q_dev) = read_gcmc(structure, unitcell, i, j, **cfg.task)
                loadings.append(l)
                loading_devs.append(l_dev)
                qs.append(q)
                q_devs.append(q_dev)
                if l is None:
                    unfinished.append(structure)

            for col, values in zip(
                ["%s_uptake_%s" %(cfg.task.MoleculeName[i], cfg.task.P), "%s_uptake_%s_dev" %(cfg.task.MoleculeName[i], cfg.task.P), "%s_enthalpy_%s" %(cfg.task.MoleculeName[i], cfg.task.P), "%s_enthalpy_%s_dev" %(cfg.task.MoleculeName[i], cfg.task.P)],
                [loadings, loading_devs, qs, q_devs]
            ):
                df[col] = values
        
        unfinished = np.unique(unfinished)
                
    logging.info(f"Saving results in {cfg.out_dir}. \n")
    df.to_csv(
        os.path.join(cfg.out_dir, "results.csv"),
        index=False
    )
  
    # write unfinished cifs
    if len(unfinished) > 0:
        logging.info(f"{len(unfinished)} structures unfinished. \n")
        with open(os.path.join(cfg.out_dir, "unfinished"), "w") as fp:
            for struc in unfinished:
                fp.write("%s\n" %struc)
        os.mkdir(os.path.join(cfg.out_dir, "newround"))
        for i in unfinished:
            shutil.copytree(
                os.path.join(cfg.out_dir, i),
                os.path.join(cfg.out_dir, "newround", i)
            )
        