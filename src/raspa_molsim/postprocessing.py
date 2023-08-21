def read_henry(structure, unitcell, ExternelTemperature, **kwargs):
    with open ("output_"+ structure + "_" + str(unitcell[0]) + "." +
            str(unitcell[1]) + "." + str(unitcell[2]) + "_" +
            str(ExternelTemperature) + ".000000_0.data", 'r') as fi:
        data = fi.readlines()
    for line in data:
        if "] Average Henry coefficient:" in line:
            kh_line = line.split()
            kh, kh_dev = float(kh_line[4]), float(kh_line[6])
    fi.close()
    return kh, kh_dev

def read_gcmc(structure, unitcell, T, P, **kwargs):
    with open ("output_"+ structure + "_" + str(unitcell[0]) + "." +
               str(unitcell[1]) + "." + str(unitcell[2]) + "_" +
               str(T) + ".000000_" + str(P) + ".data", 'r') as fi:
        data = fi.readlines()
        for line in data:
            if "Enthalpy of adsorption:" in line:
                Q_line = data[data.index(line) + 10]
                Q = float(Q_line.split()[0])
            elif "Average loading absolute [mol/kg framework]" in line:
                L = float(line.split()[5])
    fi.close()
    # L (mmol/g) and Q (J/mmol)
    return L, Q
