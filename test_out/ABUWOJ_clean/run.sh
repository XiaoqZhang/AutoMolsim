#! /bin/bash

#SBATCH --no-requeue
#SBATCH --get-user-env
#SBATCH --nodes 1
#SBATCH --ntasks 1
#SBATCH --partition serial
#SBATCH --time 04:00:00
#SBATCH --mem 4G

export RASPA_DIR=/home/xiazhang/bin/aiida-lsmo-codes/data/raspa
export DYLD_LIBRARY=/home/xiazhang/bin/aiida-lsmo-codes/lib/raspa_4467e14_fidis
export LD_LIBRARY_PATH=/home/xiazhang/bin/aiida-lsmo-codes/lib/raspa_4467e14_fidis

/home/xiazhang/bin/aiida-lsmo-codes/bin/simulate_4467e14_fidis simulation.input
