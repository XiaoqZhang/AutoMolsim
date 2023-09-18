# Prerequisites
- Install zeo++ (http://www.zeoplusplus.org/download.html)
- Create an Anaconda environment with python version 3.8 by `conda create -m <env-name> python=3.8 -y`
- Install RASPA by `conda install -c conda-forge raspa2`
- Setup the environment path by `export RASPA_DIR=</path/to/conda/environment>`
- Create an Anaconda environment and install this package by `pip install -e .`

# How to use

- Configure your simulation by files in `conf` folder
- Run the program by `python run.py`
- If there are too many structures and you want to split the jobs into batchs, you can use ` for f in *; do d=dir_$(printf %03d $((i/1000+1)));mkdir -p $d; mv "$f" $d; let i++; done`

# molsim_workflow
A computational workflow which takes as input a CIF (Crystallographic Information File) of a MOF (Metal Organic Framework) and then performs the following operations:

1. Preparation of lammps input file (for energy minimization) using lammps_interface (https://github.com/peteboyd/lammps_interface) -- Not implemented yet
2. Energy minimzation of the MOF using lammps (https://github.com/lammps/lammps) -- Not implemented yet
3. Partial charge assignment of the MOF using EQeq method (https://github.com/danieleongari/EQeq) -- Not implemented yet
4. Various molecular simulations using RASPA (https://github.com/iRASPA/RASPA2), including GCMC, Henry coefficient, NVT, Energy grid simulations. 

Please make sure that all the respective programs are installed in your system. 

To do list:
- check if gcmc function running well
- add make_grid function