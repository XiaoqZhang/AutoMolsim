# Create simulation.input file for molsim tasks

# Henry coefficient
def henry(structure, unitcell, NumberOfCycles, Forcefield, CutOff, ExternelTemperature, MoleculeName, MoleculeDefinition, **kwargs):
    with open("simulation.input","w") as fo:
        str_out = ""
        str_out += "SimulationType               MonteCarlo\n"
        str_out += "NumberOfCycles               %s\n" %NumberOfCycles
        str_out += "NumberOfInitializationCycles 0\n"
        str_out += "PrintEvery                   100\n"
        str_out += "RestartFile                  no\n\n"
        str_out += "Forcefield                   %s\n" %Forcefield
        str_out += "UseChargesFromCIFFile   yes\n"
        str_out += "CutOff                  %s\n" %CutOff
        str_out += "ChargeMethod            Ewald\n\n"
        str_out += "Framework               0\n"
        str_out += "FrameworkName           %s\n" %structure
        str_out += "UnitCells               %i %i %i\n"%(unitcell[0],unitcell[1],unitcell[2])
        str_out += "ExternalTemperature     %s\n\n" %ExternelTemperature
        str_out += "Component 0 MoleculeName                 %s\n" %MoleculeName
        str_out += "            MoleculeDefinition           %s\n" %MoleculeDefinition
        str_out += "            WidomProbability              1.0\n"
        str_out += "            CreateNumberOfMolecules      0\n"
        fo.write(str_out)
        fo.close()
    return str_out

# NVT simulation
def nvt(structure, unitcell, NumberOfCycles, NumberOfInitializationCycles, RestartFile, Forcefield, CutOffVDW, ExternelTemperature, Movies, WriteMoviesEvery, MoleculeName, MoleculeDefinition, **kwargs):
    str_out = ""
    str_out += "SimulationType               MonteCarlo\n"
    str_out += "NumberOfCycles               %s\n" %NumberOfCycles
    str_out += "NumberOfInitializationCycles %s\n" %NumberOfInitializationCycles
    str_out += "RestartFile                  %s\n\n" %RestartFile
    str_out += "Forcefield                   %s\n" %Forcefield
    str_out += "CutOffVDW                  %s\n" %CutOffVDW
    str_out += "UseChargesFromCIFFile   yes\n"
    str_out += "ChargeMethod            Ewald\n\n"
    str_out += "Framework               0\n"
    str_out += "FrameworkName           %s\n" %structure
    str_out += "UnitCells               %i %i %i\n" %(unitcell[0],unitcell[1],unitcell[2])
    str_out += "ExternalTemperature     %s\n" %ExternelTemperature
    str_out += "Movies                  %s\n" %Movies
    str_out += "WriteMoviesEvery        %i\n" %WriteMoviesEvery
    str_out += "Component 0 MoleculeName                 %s\n" %MoleculeName
    str_out += "            MoleculeDefinition           %s\n" %MoleculeDefinition
    str_out += "            TranslationProbability       1.0\n"
    str_out += "            RotationProbability          1.0\n"
    str_out += "            ReinsertionProbability       1.0\n"
    str_out += "            CreateNumberOfMolecules      1\n"
    return str_out

# Grand Canonical Monte Carlo (GCMC)
def gcmc(structure, unitcell, NumberOfCycles, NumberOfInitializationCycles, Forcefield, T, P, MoleculeName, MoleculeDefinition, block, **kwargs):
    # T and P are in (K) and (Pa) respectively
    with open("simulation.input","w") as fo:
        str_out = ""
        str_out += "SimulationType               MonteCarlo\n"
        str_out += "NumberOfCycles               %i\n" %NumberOfCycles
        str_out += "NumberOfInitializationCycles %i\n" %NumberOfInitializationCycles
        str_out += "PrintEvery                   10\n" 
        str_out += "PrintPropertiesEvery         10\n"
        str_out += "RestartFile                  no\n\n"
        str_out += "Forcefield                   %s\n\n" %Forcefield
        str_out += "Framework               0\n"
        str_out += "FrameworkName           %s\n" %structure
        str_out += "UseChargesFromCIFFile   yes\n"
        str_out += "UnitCells               %i %i %i\n"%(unitcell[0],unitcell[1],unitcell[2])
        str_out += "ExternalTemperature     %s\n" %str(T)
        str_out += "ExternalPressure        %s\n\n" %str(P)
        str_out += "Component 0 MoleculeName                 %s\n" %MoleculeName
        str_out += "            MoleculeDefinition           %s\n" %MoleculeDefinition
        if (block == "yes"):
            str_out += "            BlockPockets                 %s\n" %block
            str_out += "            BlockPocketsFilename         %s\n" %structure
        str_out += "            TranslationProbability       1.0\n"
        str_out += "            RotationProbability          1.0\n"
        str_out += "            ReinsertionProbability       1.0\n"
        str_out += "            SwapProbability              1.0\n"
        str_out += "            CreateNumberOfMolecules      0\n"
        fo.write(str_out)
        fo.close()
        return str_out

# Energy grid
def make_grid(structure, grid_type, **kwargs):
    # need to do!
    with open("simulation.input","w") as fo:
        str_out = ""
        fo.write(str_out)
        fo.close()
    return str_out

# Energy minimization
def minimization(
    structure, unitcell, NumberOfCycles, PrintEvery, RestartFile, 
    MaximumNumberOfMinimizationSteps, 
    Forcefield, CutOffVDW, T, 
    MoleculeName, MoleculeDefinition, CreateNumberOfMolecules, **kwargs
):
    with open("simulation.input","w") as fo:
        str_out = ""
        str_out += "SimulationType                  Minimization\n"
        str_out += "NumberOfCycles                  %i\n" %NumberOfCycles
        str_out += "NumberOfInitializationCycles    0\n"
        str_out += "PrintEvery                      %s\n" %PrintEvery
        str_out += "RestartFile                     %s\n\n" %RestartFile
        str_out += "MaximumNumberOfMinimizationSteps    %s\n" %MaximumNumberOfMinimizationSteps
        str_out += "RMSGraientTolerance             1e-6\n"
        str_out += "MaxGradientTolerance            1e-6\n\n"
        str_out += "Forcefield                      %s\n" %Forcefield
        str_out += "CutOffVDW                       %s\n" %CutOffVDW
        str_out += "UseChargesFromCIFFile           yes\n"
        str_out += "ChargeMethod                    Ewald\n\n"
        str_out += "Framework                       0\n"
        str_out += "FrameworkName                   %s\n" %structure
        str_out += "UnitCells                       %i %i %i\n"%(unitcell[0],unitcell[1],unitcell[2])
        str_out += "ExternalTemperature             %s\n\n" %str(T)
        str_out += "Movies                          yes\n"
        str_out += "WriteMoviesEvery                1\n\n"
        str_out += "Component 0 MoleculeName                 %s\n" %MoleculeName
        str_out += "            MoleculeDefinition           %s\n" %MoleculeDefinition
        str_out += "            TranslationProbability       1.0\n"
        str_out += "            RotationProbability          1.0\n"
        str_out += "            ReinsertionProbability       1.0\n"
        str_out += "            SwapProbability              1.0\n"
        str_out += "            CreateNumberOfMolecules      %s\n" %CreateNumberOfMolecules
        fo.write(str_out)
        fo.close()
        return str_out