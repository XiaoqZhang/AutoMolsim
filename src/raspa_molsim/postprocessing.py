import os
import warnings
import logging

def read_henry(structure, unitcell, ExternelTemperature, **kwargs):
    output_path = "Output/System_0/output_"+ structure + "_" + str(unitcell[0]) + "." + str(unitcell[1]) + "." + str(unitcell[2]) + "_" + str(ExternelTemperature) + ".000000_0.data"
    if not os.path.exists(output_path):
        return None, None
    with open (output_path, 'r') as fi:
        data = fi.readlines()
        if not "Simulation finished,  0 warnings\n" in data:
            warnings.warn("Simulation not finished")
            logging.info(f"Simulation not finished for {structure}")
            return None, None
        else:
            for line in data:
                if "] Average Henry coefficient:" in line:
                    kh_line = line.split()
                    kh, kh_dev = float(kh_line[4]), float(kh_line[6])
    return kh, kh_dev

def read_gcmc(structure, unitcell, T, P, **kwargs):
    output_path = "Output/System_0/output_"+ structure + "_" + str(unitcell[0]) + "." + str(unitcell[1]) + "." + str(unitcell[2]) + "_" + str(T) + ".000000_" + str(P) + ".data"
    if not os.path.exists(output_path):
        print(os.getcwd())
        print(f"{output_path} not exist")
        return (None, None), (None, None)
    with open (output_path, 'r') as fi:
        data = fi.readlines()
        if not "Simulation finished,  0 warnings\n" in data:
            warnings.warn("Simulation not finished")
            logging.info(f"Simulation not finished for {structure}")
            return (None, None), (None, None)
        else:
            for line in data:
                if "Enthalpy of adsorption:" in line:
                    Q_line = data[data.index(line) + 10]
                    Q = float(Q_line.split()[0])
                    Q_dev = float(Q_line.split()[2])
                elif "Average loading absolute [mol/kg framework]" in line:
                    L = float(line.split()[5])
                    L_dev = float(line.split()[7])
    # L (mmol/g) and Q (J/mmol)
    return (L, L_dev), (Q, Q_dev)
