# generate shell script for RASPA

def local(raspa_dir, **kwargs):
    str_out = ""
    str_out += "#! /bin/sh -f\n"
    str_out += "export RASPA_DIR=%s\n" %raspa_dir
    str_out += "$RASPA_DIR/bin/simulate simulation.input\n"
    return str_out

def fidis(time, mem, raspa_dir, lib_dir, raspa_bin, **kwargs):
    str_out = ""
    str_out += "#! /bin/bash\n\n"
    str_out += "#SBATCH --no-requeue\n"
    str_out += "#SBATCH --get-user-env\n"
    str_out += "#SBATCH --nodes 1\n"
    str_out += "#SBATCH --ntasks 1\n"
    str_out += "#SBATCH --time %s\n" %time
    str_out += "#SBATCH --mem %s\n\n" %mem
    str_out += "export RASPA_DIR=%s\n" %raspa_dir
    str_out += "export DYLD_LIBRARY=%s\n" %lib_dir
    str_out += "export LD_LIBRARY_PATH=%s\n\n" %lib_dir
    str_out += "%s simulation.input\n" %raspa_bin
    return str_out