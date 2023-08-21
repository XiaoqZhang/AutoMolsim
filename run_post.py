import hydra
from omegaconf import DictConfig, OmegaConf

import os
import shutil
import logging
from tqdm import tqdm
import pandas as pd

from raspa_molsim.cells import *
from raspa_molsim.zeo import *
from raspa_molsim.file_utils import *
from raspa_molsim.postprocessing import *

@hydra.main(version_base=None, config_path="conf", config_name="config")
def run(cfg: DictConfig) -> None:
    # read cif list
    structure_list = os.listdir(cfg.cif_dir)
    structures = [s.rsplit('.', 1)[0] for s in structure_list if s.rsplit('.', 1)[-1]=="cif"]
    
    khs, kh_devs = [], []
    for structure in tqdm(structures):
        unitcell = extract_geometry(os.path.join(cfg.cif_dir, structure+".cif"))

        # get the output folder for each structure
        sim_dir = os.path.join(cfg.out_dir, structure, "Output/System_0")
        os.chdir(sim_dir)
        if cfg.task.name == "henry":
            kh, kh_dev = read_henry(structure, unitcell, **cfg.task)
            khs.append(kh)
            kh_devs.append(kh_dev)
            
    df = pd.DataFrame(
        {
            "cif": structures,
            "kh": khs,
            "kh_dev": kh_devs
        }
    )
    logging.info(f"Saving results in {cfg.out_dir}")
    df.to_csv(
        os.path.join(cfg.out_dir, "results.csv"),
        index=False
    )  
  
if __name__ == "__main__":
    run()   