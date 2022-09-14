# Create simulation.input file for molsim tasks

# Henry coefficient
def henry(structure, unitcell, config):
    with open("simulation.input","w") as fo:
        str_out = ""
        str_out += "SimulationType               MonteCarlo\n"
        str_out += "NumberOfCycles               10000\n"
        str_out += "NumberOfInitializationCycles 0\n"
        str_out += "PrintEvery                   100\n"
        str_out += "RestartFile                  no\n\n"
        str_out += "Forcefield                   diversity-ff\n"
        str_out += "UseChargesFromCIFFile   yes\n"
        str_out += "CutOff                  12.8\n"
        str_out += "ChargeMethod            Ewald\n\n"
        str_out += "Framework               0\n"
        str_out += "FrameworkName           %s\n"%(structure)
        str_out += "UnitCells               %i %i %i\n"%(unitcell[0],unitcell[1],unitcell[2])
        str_out += "ExternalTemperature     %s\n\n"%str(T)
        str_out += "Component 0 MoleculeName                 %s\n"%(molecule)
        str_out += "            MoleculeDefinition           TraPPE\n"
        str_out += "            WidomProbability              1.0\n"
        str_out += "            CreateNumberOfMolecules      0\n"
        fo.write(str_out)
        fo.close()

def nvt(structure, unitcell, molecule, NumberOfCycles, NumberOfInitializationCycles, Forcefield, CutOffVDW, ExternelTemperature, Movies, WriteMoviesEvery, MoleculeDefinition):
    str_out = ""
    str_out += "SimulationType               MonteCarlo\n"
    str_out += "NumberOfCycles               %s\n" %NumberOfCycles
    str_out += "NumberOfInitializationCycles %s\n" %NumberOfInitializationCycles
    str_out += "RestartFile                  no\n\n"
    str_out += "Forcefield                   %s\n" %Forcefield
    str_out += "CutOffVDW                  %s\n" %CutOffVDW
    str_out += "UseChargesFromCIFFile   yes\n"
    str_out += "ChargeMethod            Ewald\n\n"
    str_out += "Framework               0\n"
    str_out += "FrameworkName           %s\n" %structure
    str_out += "UnitCells               %i %i %i\n" %(unitcell[0],unitcell[1],unitcell[2])
    str_out += "ExternalTemperature     %s\n" %ExternelTemperature
    str_out += "Movies                  yes\n"
    str_out += "WriteMoviesEvery        1\n"
    str_out += "Component 0 MoleculeName                 %s\n" %molecule
    str_out += "            MoleculeDefinition           %s\n" %MoleculeDefinition
    str_out += "            TranslationProbability       1.0\n"
    str_out += "            RotationProbability          1.0\n"
    str_out += "            ReinsertionProbability       1.0\n"
    str_out += "            CreateNumberOfMolecules      1\n"
    return str_out

# Create a simulation.input file for GCMC calculations
def gcmc(cycles, structure, unitcell, T, P, molecule, block):
    # T and P are in (K) and (Pa) respectively
    with open("simulation.input","w") as fo:
        str_out = ""
        str_out += "SimulationType               MonteCarlo\n"
        str_out += "NumberOfCycles               %i\n"%(cycles)
        str_out += "NumberOfInitializationCycles %i\n"%(cycles/10)
        str_out += "PrintEvery                   %i\n"%(cycles/10)
        str_out += "PrintPropertiesEvery         %i\n"%(cycles/10)
        str_out += "RestartFile                  no\n\n"
        str_out += "Forcefield                   local\n\n"
        str_out += "Framework               0\n"
        str_out += "FrameworkName           %s\n"%(structure)
        str_out += "UseChargesFromCIFFile   yes\n"
        str_out += "UnitCells               %i %i %i\n"%(unitcell[0],unitcell[1],unitcell[2])
        str_out += "ExternalTemperature     %s\n"%str(T)
        str_out += "ExternalPressure        %s\n\n"%str(P)
        str_out += "Component 0 MoleculeName                 %s\n"%(molecule)
        str_out += "            MoleculeDefinition           local\n"
        if (block == "yes"):
            str_out += "            BlockPockets                 %s\n"%(block)
            str_out += "            BlockPocketsFilename         %s\n"%(structure)
        str_out += "            TranslationProbability       1.0\n"
        str_out += "            RotationProbability          1.0\n"
        str_out += "            ReinsertionProbability       1.0\n"
        str_out += "            SwapProbability              1.0\n"
        str_out += "            CreateNumberOfMolecules      0\n"
        fo.write(str_out)
        fo.close()