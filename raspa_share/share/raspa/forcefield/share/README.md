The force_field_mixing_rules.def is from [Moosavi, S.M., Nandy, A., Jablonka, K.M. et al. Understanding the diversity of the metal-organic framework ecosystem. Nat Commun 11, 4068 (2020).]
But use tail correction. 

C_co2, O_co2 Lennard-Jones parameters are cited from TraPPE. http://trappe.oit.umn.edu/

pseudo_atoms.def is taken from fidis folder /work/lsmo/aiida-lsmo-codes/data/raspa/share/raspa/forcefield/TraPPE/pseudo_atoms.def 

This folder includes CO2, N2, CH4, N2O, H2S, and H2O. The definitions about small molecules can be found in molecules/TraPPE, except for H2O. Find H2O.def in molecules/TIP4P. The reference for N2O, H2O can be found in the last line of molecule definition. 
