#! /bin/bash

#SBATCH --no-requeue
#SBATCH --get-user-env
#SBATCH --nodes 1
#SBATCH --ntasks 1
#SBATCH --partition serial
#SBATCH --time 24:00:00
#SBATCH --mem 32G

export RASPA_DIR=/work/lsmo/aiida-lsmo-codes/data/raspa
export DYLD_LIBARY=/work/lsmo/aiida-lsmo-codes/lib/raspa_4467e14_fidis
export LD_LIBRARY_PATH=/work/lsmo/aiida-lsmo-codes/lib/raspa_4467e14_fidis

/work/lsmo/aiida-lsmo-codes/bin/simulate_4467e14_fidis simulation.input
