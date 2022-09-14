import numpy as np
import math

# Calculate the minimum unit cells needed for GCMC simulation
def cell_units(lens, angs, co):
    # lens and cutoff (co) are given in A and angs in degrees
    # unpack parameters
    a = lens[0]
    b = lens[1]
    c = lens[2]
    alpha = math.radians(angs[0])
    beta = math.radians(angs[1])
    gamma = math.radians(angs[2])
    # Start the calculations (https://en.wikipedia.org/wiki/Fractional_coordinates)
    K = c*(math.cos(alpha)-math.cos(beta)*math.cos(gamma))/math.sin(gamma)
    V = math.sqrt(1-math.cos(alpha)**2-math.cos(beta)**2-math.cos(gamma)**2+2*math.cos(alpha)*math.cos(beta)*math.cos(gamma))
    Minv = [[a, 0, 0], [b*math.cos(gamma), b*math.sin(gamma), 0] , [c*math.cos(beta), K, c*V/math.sin(gamma)]]
    axb = np.cross(Minv[0],Minv[1])
    bxc = np.cross(Minv[1],Minv[2])
    cxa = np.cross(Minv[2],Minv[0])
    x = np.dot(Minv[0],bxc)/np.linalg.norm(bxc)
    y = np.dot(Minv[1],cxa)/np.linalg.norm(cxa)
    z = np.dot(Minv[2],axb)/np.linalg.norm(axb)
    xmin = math.ceil(2*co/x)
    ymin = math.ceil(2*co/y)
    zmin = math.ceil(2*co/z)
    return xmin, ymin, zmin

# Extract the edge lengths and angles from the .cif file
def extract_geometry(structure_path):
    with open (structure_path, 'r') as fi:
        data = fi.readlines()
        for line in data:
            if "_cell_length_a" in line:
                a = float(line.split()[1])
            elif "_cell_length_b" in line:
                b = float(line.split()[1])
            elif "_cell_length_c" in line:
                c = float(line.split()[1])
            elif "_cell_angle_alpha" in line:
                alpha = float(line.split()[1])
            elif "_cell_angle_beta" in line:
                beta = float(line.split()[1])
            elif "_cell_angle_gamma" in line:
                gamma = float(line.split()[1])
        lens = [a, b, c]
        angs = [alpha, beta, gamma]
        fi.close()
    unitcell = cell_units(lens, angs, 12)
    return unitcell