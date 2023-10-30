import os
import warnings
import logging

def read_henry(structure, unitcell, ExternelTemperature, **kwargs):
    output_path = "Output/System_0/output_%s_%d.%d.%d_%lf_0.data" %(structure, unitcell[0], unitcell[1], unitcell[2], ExternelTemperature)
    if not os.path.exists(output_path):
        return None, None
    with open (output_path, 'r') as fi:
        data = fi.readlines()
        if ("Simulation finished,  0 warnings\n" in data):
            for line in data:
                if "] Average Henry coefficient:" in line:
                    kh_line = line.split()
                    kh, kh_dev = float(kh_line[4]), float(kh_line[6])
        elif ("Simulation finished,  1 warnings\n" in data) and ("WARNING: THE SYSTEM HAS A NET CHARGE \n" in data):
            for line in data:
                if "] Average Henry coefficient:" in line:
                    kh_line = line.split()
                    kh, kh_dev = float(kh_line[4]), float(kh_line[6])
        else:
            warnings.warn("Simulation not finished")
            logging.info(f"Simulation not finished for {structure}")
            return None, None

    return kh, kh_dev

def read_gcmc(structure, unitcell, no_component, T, P, **kwargs):
    print("The %s component. " %no_component)
    output_path = "Output/System_0/output_%s_%d.%d.%d_%lf_%lg.data" %(structure, unitcell[0], unitcell[1], unitcell[2], T, P)
    if not os.path.exists(output_path):
        print(os.getcwd())
        print(f"{output_path} not exist")
        return (None, None), (None, None)
    with open (output_path, 'r') as fi:
        data = fi.readlines()
        q_counter, l_counter = -1, -1
        if ("Simulation finished,  0 warnings\n" in data):
            for no, line in enumerate(data):
                if "Note: The heat of adsorption Q=-H" in line:
                    q_counter += 1
                    if q_counter == (no_component+1):
                        Q_line = data[no - 2]
                        Q = float(Q_line.split()[0])
                        Q_dev = float(Q_line.split()[2])
                elif "Average loading absolute [mol/kg framework]" in line:
                    l_counter += 1
                    if l_counter == no_component:
                        L = float(line.split()[5])
                        L_dev = float(line.split()[7])
        elif ("Simulation finished,  1 warnings\n" in data) and ("WARNING: THE SYSTEM HAS A NET CHARGE \n" in data):
            for no, line in enumerate(data):
                if "Note: The heat of adsorption Q=-H" in line:
                    if q_counter == (no_component+1):
                        Q_line = data[no - 2]
                        Q = float(Q_line.split()[0])
                        Q_dev = float(Q_line.split()[2])
                        q_counter += 1
                elif "Average loading absolute [mol/kg framework]" in line:
                    if l_counter == no_component:
                        L = float(line.split()[5])
                        L_dev = float(line.split()[7])
                        l_counter += 1
        else:
            warnings.warn("Simulation not finished")
            logging.info(f"Simulation not finished for {structure}")
            L, L_dev, Q, Q_dev = None, None, None, None
    # L (mmol/g) and Q (J/mmol)
        print(L, Q)
    return (L, L_dev), (Q, Q_dev)
