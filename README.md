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