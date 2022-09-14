def local(raspa_dir):
    str_out = ""
    str_out += "#! /bin/sh -f\n"
    str_out += "export RASPA_DIR=%s\n" %raspa_dir
    str_out += "$RASPA_DIR/bin/simulate simulation.input"
    return str_out