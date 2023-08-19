import subprocess

# Obtain blocking spheres using zeo++
def zeo_block(structure, radius, n_points):
    subprocess.call(["network", "-ha", "-block", "%s" %radius, "%s" %n_points, structure + ".cif"])