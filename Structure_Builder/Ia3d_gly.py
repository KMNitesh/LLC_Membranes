# This script creates the BCC Ia3d phase.
# Author: Norma Langdon

print 'This is a .gro file'

import numpy as np
import math
import os
import argparse
import sys

parser = argparse.ArgumentParser(description = 'Build BCC Structure')
parser.add_argument('-i', '--input', default = 'monomer58.pdb', help = 'Path to input file')
parser.add_argument('-l', '--layers', default = 10, type = int, help = 'Number of Layers')
parser.add_argument('-mi', '--monomers_inner', default = 4, type = int, help = 'Number of monomers in inner ring at limiting radius')
parser.add_argument('-mo', '--monomers_outer', default = 10, type = int, help = 'Number of monomers in outer ring at limiting radius')
parser.add_argument('-w', '--pore_width', default = 12, type = float, help = 'Pore width')
parser.add_argument('-d', '--dist', default = 10, type = float, help = 'Distance between layers')
parser.add_argument('-p', '--dist_periodic', default = 5, type = float, help = 'Negative distance between periodic boundary conditions')
args = parser.parse_args()

location = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
fileopen = open("%s/../BCC_Monomer_Configurations/%s" % (location, args.input), "r")

no_layers = args.layers
no_monomers_inner = args.monomers_inner
no_monomers_outer = args.monomers_outer
pore_width = args.pore_width
dist = args.dist
dist_periodic = args.dist_periodic
name = 'MOL'
no_ions = 2

# The inner arms are longer than the outer arms, so that they will connect at the junctions.
no_layers_inner = no_layers + 2

# Imports location information about the monomer
read = []
for line in fileopen:
    read.append(line)
lines_of_text = 0
for i in range(0, len(read)):     # Counts the number of text lines at the top of .pdb file
    if read[i].count('ATOM') == 0:
        lines_of_text += 1
    if read[i].count('ATOM') == 1:
        break
no_atoms = 0
for i in range(0, len(read)):
    no_atoms += read[i].count('ATOM')     # Counts the number of non-text lines in the .pdb file to find the number of atoms in the monomers
x_values_inp = []  # list to hold input values of x stored from .pdb file
y_values_inp = []  # list to hold input values of y stored from .pdb file
z_values_inp = []  # list to hold input values of z stored from .pdb file
positions_inp = []  # holds x, y, z coordinates of input .pdb file
identity = []  # holds the names of atom in the order that they appear in the .pdb file
for i in range(lines_of_text, lines_of_text + no_atoms): # Searches the non-text lines
    x_values_inp.append(float(read[i][26:38]))  # Use this to read specific entries in a text file
    y_values_inp.append(float(read[i][38:46]))
    z_values_inp.append(float(read[i][46:54]))
    positions_inp.append([x_values_inp[i - lines_of_text], y_values_inp[i - lines_of_text], z_values_inp[i - lines_of_text]])
    identity.append(read[i][12:16])  # hold name of atom (C, N, H or BR)

# Imports location information about glycerol
read2 = []
fileopen2 = open("../BCC_Monomer_Configurations/gly_box_em1.gro", "r")
for line in fileopen2:
    read2.append(line)
x_gly = []; y_gly = []; z_gly = []; positions_inp_gly = []; identity_gly = []
for i in range(0, len(read2)):
    x_gly.append(float(read2[i][20:28]))
    y_gly.append(float(read2[i][28:36]))
    z_gly.append(float(read2[i][36:44]))
    positions_inp_gly.append([x_gly[i], y_gly[i], z_gly[i]])
    identity_gly.append(read2[i][12:16])
name_GLC = 'GLC'
x_ave_sum_gly = 0; y_ave_sum_gly = 0; z_ave_sum_gly = 0; divisor = 0
for i in range(0, len(positions_inp_gly)):
    x_ave_sum_gly = x_ave_sum_gly + positions_inp_gly[i][0]
    y_ave_sum_gly = y_ave_sum_gly + positions_inp_gly[i][1]
    z_ave_sum_gly = z_ave_sum_gly + positions_inp_gly[i][2]
    divisor += 1
x_ave_gly = x_ave_sum_gly/float(divisor); y_ave_gly = y_ave_sum_gly/float(divisor); z_ave_gly = z_ave_sum_gly/float(divisor)

# This next section defines a plane through the monomer and rotates the monomer to align with the xy-plane.
# The plane is defined by three points. The points are locations: N1, N2 and the average of C22 and C23, respectively.
plane_x = np.zeros((3, 1))
plane_y = np.zeros((3, 1))
plane_z = np.zeros((3, 1))

plane_x[0] = float(read[lines_of_text + 21][26:38])
plane_y[0] = float(read[lines_of_text + 21][38:46])
plane_z[0] = float(read[lines_of_text + 21][46:54])

plane_x[1] = float(read[lines_of_text + 28][26:38])
plane_y[1] = float(read[lines_of_text + 28][38:46])
plane_z[1] = float(read[lines_of_text + 28][46:54])

plane_x[2] = (float(read[lines_of_text + 24][26:38]) + float(read[lines_of_text + 25][26:38]))/2.0
plane_y[2] = (float(read[lines_of_text + 24][38:46]) + float(read[lines_of_text + 25][38:46]))/2.0
plane_z[2] = (float(read[lines_of_text + 24][46:54]) + float(read[lines_of_text + 25][46:54]))/2.0

# A plane can be defined by two vectors.
vector12 = [float(plane_x[1]-plane_x[0]), float(plane_y[1]-plane_y[0]), float(plane_z[1]-plane_z[0])]
vector13 = [float(plane_x[2]-plane_x[0]), float(plane_y[2]-plane_y[0]), float(plane_z[2]-plane_z[0])]
# The cross product of the two vectors gives a new vector that is perpendicular to the plane.
normalvector = np.cross(vector12, vector13)
# Since we want the plane of the monomer to be the xy-plane, we want the vector normal to the plane to be the z-axis.
normalvector_desired = [0, 0, 1]

rotation_to_xy = np.cross(normalvector, normalvector_desired)
# Rotation angle
theta = math.acos(np.dot(normalvector, normalvector_desired)/(np.linalg.norm(normalvector)*np.linalg.norm(normalvector_desired)))
# Normalized rotation axis
rotation_norm = [rotation_to_xy[0]/np.linalg.norm(rotation_to_xy), rotation_to_xy[1]/np.linalg.norm(rotation_to_xy), rotation_to_xy[2]/np.linalg.norm(rotation_to_xy)]

# Rotation matrix to rotate plane:
Rot_to_xy = np.zeros((4, 4))
Rot_to_xy[3, 3] = 1
Rot_to_xy[0, 0] = rotation_norm[0]**2 + (rotation_norm[1]**2 + rotation_norm[2]**2)*math.cos(theta)  # math.cos takes theta in radians by default
Rot_to_xy[0, 1] = rotation_norm[0]*rotation_norm[1]*(1 - math.cos(theta)) - rotation_norm[2]*math.sin(theta)
Rot_to_xy[0, 2] = rotation_norm[0]*rotation_norm[2]*(1 - math.cos(theta)) + rotation_norm[1]*math.sin(theta)
Rot_to_xy[1, 0] = rotation_norm[0]*rotation_norm[1]*(1 - math.cos(theta)) + rotation_norm[2]*math.sin(theta)
Rot_to_xy[1, 1] = rotation_norm[1]**2 + (rotation_norm[0]**2 + rotation_norm[2]**2)*math.cos(theta)
Rot_to_xy[1, 2] = rotation_norm[1]*rotation_norm[2]*(1 - math.cos(theta)) - rotation_norm[0]*math.sin(theta)
Rot_to_xy[2, 0] = rotation_norm[0]*rotation_norm[2]*(1 - math.cos(theta)) - rotation_norm[1]*math.sin(theta)  # math.cos takes theta in radians by default
Rot_to_xy[2, 1] = rotation_norm[2]*rotation_norm[1]*(1 - math.cos(theta)) + rotation_norm[0]*math.sin(theta)
Rot_to_xy[2, 2] = rotation_norm[2]**2 + (rotation_norm[0]**2 + rotation_norm[1]**2)*math.cos(theta)

for i in range(0, no_atoms):
    positions_inp[i].append(1)
    x = np.dot(Rot_to_xy, np.array(positions_inp[i]))
    positions_inp[i] = [x[0], x[1], x[2]]
# Now the monomer is in line with the xy-plane.

# This section will move the monomer to the origin. The average of the locations of C22 and C23 will be translated to the origin.
# Find the location of that center point:
x_center = (positions_inp[24][0] + positions_inp[25][0])/2.0
y_center = (positions_inp[24][1] + positions_inp[25][1])/2.0
z_center = (positions_inp[24][2] + positions_inp[25][2])/2.0
center = [x_center, y_center, z_center]

translation_to_origin = np.matrix([[1, 0, 0, -(center[0])], [0, 1, 0, -(center[1])], [0, 0, 1, -(center[2])], [0, 0, 0, 1]])

for i in range(0, no_atoms):
    positions_inp[i].append(1)
    x = np.dot(translation_to_origin, np.array(positions_inp[i]))
    positions_inp[i] = [x[0, 0], x[0, 1], x[0, 2]]

# This section will rotate the monomer so that it is along the x-axis. The locations of all the atoms are found and averaged.
# Then a line is drawn between that and the center point. The angle between that line and the x-axis is found, and the
# monomer is rotated by that angle.
[x_sum, y_sum, z_sum] = [0, 0, 0]
for i in range(0, no_atoms):
    x_sum = x_sum + positions_inp[i][0]
    y_sum = y_sum + positions_inp[i][1]
    z_sum = z_sum + positions_inp[i][2]
x_average = x_sum/no_atoms
y_average = y_sum/no_atoms
z_average = z_sum/no_atoms
pt_average = [x_average, y_average, z_average]

slope_monomer = pt_average[1]/pt_average[0]
slope_xaxis = 0

def Rot_x(theta):
    Rotmatrix_x = np.zeros((3, 3))
    Rotmatrix_x[0, 0] = 1
    Rotmatrix_x[1, 1] = math.cos(theta)
    Rotmatrix_x[1, 2] = -math.sin(theta)
    Rotmatrix_x[2, 1] = math.sin(theta)
    Rotmatrix_x[2, 2] = math.cos(theta)
    return Rotmatrix_x
def Rot_y(theta):
    Rotmatrix_y = np.zeros((3, 3))
    Rotmatrix_y[0, 0] = math.cos(theta)
    Rotmatrix_y[2, 0] = -math.sin(theta)
    Rotmatrix_y[1, 1] = 1
    Rotmatrix_y[0, 2] = math.sin(theta)
    Rotmatrix_y[2, 2] = math.cos(theta)
    return Rotmatrix_y
def Rot_z(theta):
    Rotmatrix_z = np.zeros((3, 3))
    Rotmatrix_z[0, 0] = math.cos(theta)
    Rotmatrix_z[1, 0] = math.sin(theta)
    Rotmatrix_z[0, 1] = -math.sin(theta)
    Rotmatrix_z[1, 1] = math.cos(theta)
    Rotmatrix_z[2, 2] = 1
    return Rotmatrix_z

theta = -math.atan(slope_monomer) # Angle between lines
Rot_to_xaxis = Rot_z(theta)
for i in range(0, no_atoms):
    x = np.array(positions_inp[i])
    rotation_to_xaxis = np.dot(Rot_to_xaxis, x)
    positions_inp[i] = [float(rotation_to_xaxis[0]), float(rotation_to_xaxis[1]), float(rotation_to_xaxis[2])]
# Now the monomer is along the x-axis.
# This next section rotates the average point. The average point is checked to see that y = 0. If it is not, something is incorrect.
x = np.array(pt_average)
rotation_pt_average = np.dot(Rot_to_xaxis, x)
pt_average = [float(rotation_pt_average[0]), float(rotation_pt_average[1]), float(rotation_pt_average[2])]
if abs(pt_average[1]) > 0.001:
    print 'error with rotation to x-axis (line 157)'
    sys.exit()
pt_average = [pt_average[0], 0, pt_average[2]]

# The next section works exclusively on the inner ring, the ring inside of the pore. The length of the monomer will be
# determined. The monomer will be translated so that it is the correct radius and its tail is facing the origin. Then,
# the monomer will be put into multiple layers and rotated around the z-axis.
positions_inp_inner = positions_inp
length_monomer = 0
for i in range(0, no_atoms):
    if abs(positions_inp[i][0]) > abs(length_monomer):
        length_monomer = positions_inp[i][0]
max_radius_inner = abs(length_monomer)

# At the smallest part of the ring, the nonpolar tails of the monomer will completely overlap. The limiting radius is found
# by finding the average of the x-coordinates of the carbons C17 and C28, which are attached directly to the nitrogen rings
# on the nonpolar tails.
if abs(positions_inp[17][0]) > abs(positions_inp[32][0]):
    length_tail = max_radius_inner - abs(positions_inp[17][0])
if abs(positions_inp[17][0]) < abs(positions_inp[32][0]):
    length_tail = max_radius_inner - abs(positions_inp[32][0])
lim_radius_inner = max_radius_inner - abs(length_tail)/2.0

# Determining the basic parabolic curve
if no_layers % 2 == 0:
    h = float((no_layers - 2)*dist/2)
if no_layers % 2 == 1:
    h = float((no_layers - 1)*dist/2)
c = lim_radius_inner
a = (max_radius_inner - lim_radius_inner)/(h*h)

z_min_inp = 0
z_max_inp = 0
for i in range(0, no_atoms - no_ions):
    if positions_inp[i][2] < z_min_inp:
        z_min_inp = positions_inp[i][2]
    if positions_inp[i][2] > z_max_inp:
        z_max_inp = positions_inp[i][2]
z_monomer = z_max_inp - z_min_inp

# Setting the coordinates of the inner ring
inner_pointlist = []
inner_dxdzlist = []
if no_layers % 2 == 0:
    z_top = dist*(no_layers_inner/2.0 - 0.5)
    height = 2*z_top
    no_monomers_inner = int(math.floor(height/(z_monomer/2.0)))
    z_comp = height/float(no_monomers_inner)
    if no_monomers_inner % 2 == 0:
        for i in range(0, no_monomers_inner/2):
            z = z_comp*(0.5 + i)
            z2 = z_comp*i
            if i == no_monomers_inner/2:
                z2 = z_comp * (i - 1)
            x = a*z2**2 + c
            dxdz = 2*a*z2
            inner_dxdzlist.append(dxdz)
            points = [x, 0, z]
            inner_pointlist.append(points)
        for i in range(0, no_monomers_inner/2):
            z = -z_comp*(0.5 + i)
            z2 = -z_comp*i
            if i == no_monomers_inner/2:
                z2 = -z_comp * (i - 1)
            x = a*z2**2 + c
            dxdz = 2*a*z2
            inner_dxdzlist.insert(0, dxdz)
            points = [x, 0, z]
            inner_pointlist.insert(0, points)
    if no_monomers_inner % 2 == 1:
        for i in range(0, (no_monomers_inner + 1)/2):
            z = z_comp*i
            x = a*z**2 + c
            if i == no_monomers_inner/2:
                z2 = z_comp * (i - 1)
                x = a*z2**2 + c
            dxdz = 2*a*z
            inner_dxdzlist.append(dxdz)
            points = [x, 0, z]
            inner_pointlist.append(points)
        for i in range(1, (no_monomers_inner + 1)/2):
            z = -z_comp*i
            x = a*z**2 + c
            if i == no_monomers_inner/2:
                z2 = -z_comp * (i - 1)
                x = a*z2**2 + c
            dxdz = 2*a*z
            inner_dxdzlist.insert(0, dxdz)
            points = [x, 0, z]
            inner_pointlist.insert(0, points)
    no_layers_inner = no_monomers_inner
if no_layers % 2 == 1:
    z_top = dist*(no_layers_inner/2.0)
    height = 2*z_top
    no_monomers_inner = int(math.floor(height/(z_monomer/2.0)))
    z_comp = height/float(no_monomers_inner)
    if no_monomers_inner % 2 == 0:
        for i in range(0, no_monomers_inner/2):
            z = z_comp*(0.5 + i)
            z2 = z_comp*i
            if i == no_monomers_inner/2:
                z2 = z_comp * (i - 1)
            z = a*z2**2 + c
            dxdz = 2*a*z2
            inner_dxdzlist.append(dxdz)
            points = [x, 0, z]
            inner_pointlist.append(points)
        for i in range(0, no_monomers_inner/2):
            z = -z_comp*(0.5 + i)
            z2 = -z_comp*i
            if i == no_monomers_inner/2:
                z2 = -z_comp * (i - 1)
            x = a*z2**2 + c
            dxdz = 2*a*z2
            inner_dxdzlist.insert(0, dxdz)
            points = [x, 0, z]
            inner_pointlist.insert(0, points)
    if no_monomers_inner % 2 == 1:
        for i in range(0, (no_monomers_inner + 1)/2):
            z = z_comp*i
            x = a*z**2 + c
            if i == (no_monomers_inner + 1)/2:
                z2 = z_comp * (i - 1)
                x = a * z2 ** 2 + c
            dxdz = 2*a*z
            inner_dxdzlist.append(dxdz)
            points = [x, 0, z]
            inner_pointlist.append(points)
        for i in range(1, (no_monomers_inner + 1)/2):
            z = -z_comp*i
            x = a*z**2 + c
            if i == (no_monomers_inner + 1)/2:
                z2 = -z_comp * (i - 1)
                x = a * z2 ** 2 + c
            dxdz = 2*a*z
            inner_dxdzlist.insert(0, dxdz)
            points = [x, 0, z]
            inner_pointlist.insert(0, points)
    no_layers_inner = no_monomers_inner

# Function to determine if the monomer is on the positive or negative x-axis. It will determine the direction in which the monomer is translated.
def translationtoradius_inner(radius, z):
    if pt_average[1] != 0:
        return 'error in determining location on x-axis, line 192'
        sys.exit()
    if pt_average[1] == 0:  # The monomer lies on the x-axis
        if pt_average[0] < 0:  # The monomer lies on the negative x-axis
            translation = np.matrix([[1, 0, 0, radius], [0, 1, 0, 0], [0, 0, 1, z], [0, 0, 0, 1]])
            return translation
        if pt_average[0] > 0:  # The monomer lies on the positive x-axis
            translation = np.matrix([[1, 0, 0, -radius], [0, 1, 0, 0], [0, 0, 1, z], [0, 0, 0, 1]])
            return translation

# Translates the monomer to the correct radius, which is a function of the row number
positions_inner = []
for i in range(0,  no_atoms):
    positions_inp_inner[i].append(1)
for i in range(0, no_layers_inner):
    positions_inner.append([])
    radius_row = inner_pointlist[i][0]
    z = inner_pointlist[i][2]
    translation_inner = translationtoradius_inner(radius_row, z)
    for j in range(0, no_atoms):
        positions_inner[i].append([])
        x = np.dot(translation_inner, np.array(positions_inp_inner[j]))
        positions_inner[i][j] = [x[0, 0], x[0, 1], x[0, 2]]

# Rotates the monomer so that it is perpendicular to the parabola at all points.
positions_perp_inner = []
for i in range(0, no_layers_inner):
    positions_perp_inner.append([])
    normal = -inner_dxdzlist[i]
    theta = -math.atan(normal)
    for j in range(0, no_atoms):
        positions_perp_inner[i].append([])
        x = np.array(positions_inner[i][j])
        Rot_perp = np.zeros((3,3))
        Rot_perp[0, 0] = math.cos(theta)
        Rot_perp[2, 0] = -math.sin(theta)
        Rot_perp[1, 1] = 1
        Rot_perp[0, 2] = math.sin(theta)
        Rot_perp[2, 2] = math.cos(theta)
        rotation_perp = np.dot(Rot_perp, x)
        positions_perp_inner[i][j] = [float(rotation_perp[0]), float(rotation_perp[1]), float(rotation_perp[2])]
# The rotation matrix will end up translating, not only rotating, the monomers. When the above rotation matrix is run,
# the monomers end up being moved slightly, which is undesirable. This loop correct that.
# This next loop stores the original (before rotation) coordinates, and translates the monomers back to them while
# keeping them perpendicular to the parabola.
for i in range(0, no_layers_inner):
    x_old_center = (positions_inner[i][24][0] + positions_inner[i][25][0])/2
    y_old_center = (positions_inner[i][24][1] + positions_inner[i][25][1])/2
    z_old_center = (positions_inner[i][24][2] + positions_inner[i][25][2])/2
    old_center = [x_old_center, y_old_center, z_old_center]
    x_new_center = (positions_perp_inner[i][24][0] + positions_perp_inner[i][25][0])/2.0
    y_new_center = (positions_perp_inner[i][24][1] + positions_perp_inner[i][25][1])/2
    z_new_center = (positions_perp_inner[i][24][2] + positions_perp_inner[i][25][2])/2
    new_center = [x_new_center, y_new_center, z_new_center]
    translation_correction = np.matrix([[1, 0, 0, old_center[0] - new_center[0]], [0, 1, 0, 0], [0, 0, 1, old_center[2] - new_center[2]], [0, 0, 0, 1]])
    for j in range(0, no_atoms):
        positions_perp_inner[i][j].append(1)
        x = np.dot(translation_correction, np.array(positions_perp_inner[i][j]))
        positions_inner[i][j] = [x[0, 0], x[0, 1], x[0,2]]

# This loop makes copies of the monomer and rotates the copies by equal angles to make layers of rings.
angle = 0
positionsrot_inner = []
for i in range(0, no_layers_inner):
    positionsrot_inner.append([])
    if i == 0 or i == no_layers_inner - 1:
        no_monomers_row = 5
    else:
        no_monomers_row = 1
    for j in range(0, no_monomers_row):
        if j == 0:
            angle = angle + 2*math.pi/5.0
        if j == 1 or j == 2:
            angle = angle + 2*math.pi/5.0
        positionsrot_inner[i].append([])
        Rx_inner = Rot_z(angle)
        for k in range(0, no_atoms):
            positionsrot_inner[i][j].append([])
            x = np.array(positions_inner[i][k])
            rotation = np.dot(Rx_inner, x)
            rotation = [float(rotation[0]), float(rotation[1]), float(rotation[2])]
            positionsrot_inner[i][j][k] = rotation

# This next section will take care of the outer ring. It will essentially do the exact same thing as above, except that
# the monomers will face the opposite direction. Additionally, they will be translated from the origin farther, to
# establish the pore between the inner and outer ring.
positions_inp_outer = positions_inp
max_radius_outer = max_radius_inner + pore_width
# The limiting radius of the outer ring is the sum of the limiting radius of the inner ring, the pore width and the length of the monomer.
lim_radius_outer = lim_radius_inner + pore_width

f = lim_radius_outer
d = (max_radius_outer - lim_radius_outer)/(h*h)

# To determine the basic parabolic curve of the outer ring.
outer_pointlist = []
outer_dxdzlist = []
if no_layers % 2 == 0:
    for i in range(0, no_layers/2):
        z = dist*(0.5 + i)
        z2 = dist*i
        x = d*z2*z2 + f
        dxdz = 2*d*z2
        outer_dxdzlist.append(dxdz)
        points = [x, 0, z]
        outer_pointlist.append(points)
    for i in range(0, no_layers/2):
        z = -dist*(0.5 + i)
        z2 = -dist*i
        x = d*z2*z2 + f
        dxdz = 2*d*z2
        outer_dxdzlist.insert(0, dxdz)
        points = [x, 0, z]
        outer_pointlist.insert(0, points)
if no_layers % 2 == 1:
    for i in range(0, ((no_layers + 1)/2)):
        z = dist*i
        x = d*z*z + f
        dxdz = 2*d*z
        outer_dxdzlist.append(dxdz)
        points = [x, 0, z]
        outer_pointlist.append(points)
    for i in range(1, ((no_layers + 1)/2)):
        z = -dist*i
        x = d*z*z + f
        dxdz = 2*d*z
        outer_dxdzlist.insert(0, dxdz)
        points = [x, 0, z]
        outer_pointlist.insert(0, points)

def translationtoradius_outer(radius, z):
    if pt_average[1] != 0:
        return 'error in determining location on x-axis, line 192'
        sys.exit()
    if pt_average[1] == 0:  # The monomer lies on the x-axis
        if pt_average[0] < 0:  # The monomer lies on the negative x-axis
            translation = np.matrix([[1, 0, 0, -radius], [0, 1, 0, 0], [0, 0, 1, z], [0, 0, 0, 1]])
            return translation
        if pt_average[0] > 0:  # The monomer lies on the positive x-axis
            translation = np.matrix([[1, 0, 0, radius], [0, 1, 0, 0], [0, 0, 1, z], [0, 0, 0, 1]])
            return translation

# Translate the monomer to the outer radius.
positions_outer = []
for i in range(0, no_layers):
    positions_outer.append([])
    radius_row = outer_pointlist[i][0]
    z = outer_pointlist[i][2]
    translation_outer = translationtoradius_outer(radius_row, z)
    for j in range(0, no_atoms):
        positions_outer[i].append([])
        x = np.dot(translation_outer, np.array(positions_inp_outer[j]))
        positions_outer[i][j] = [x[0, 0], x[0, 1], x[0, 2]]
# Translate the glycerol to the middle of the ring
positions_gly_arc = []
for i in range(0, no_layers):
    positions_gly_arc.append([])
    radius = outer_pointlist[i][0] - pore_width / 2.0
    z = outer_pointlist[i][2]
    translation_gly = np.matrix(
        [[1, 0, 0, radius - x_ave_gly], [0, 1, 0, -y_ave_gly], [0, 0, 1, z - z_ave_gly], [0, 0, 0, 1]])
    for j in range(0, len(positions_inp_gly)):
        positions_gly_arc[i].append([])
        if len(positions_inp_gly[j]) == 3:
            positions_inp_gly[j].append(1)
        x = np.dot(translation_gly, np.array(positions_inp_gly[j]))
        positions_gly_arc[i][j] = [x[0, 0], x[0, 1], x[0, 2]]

# Make the monomers perpendicular to the parabola.
positions_perp_outer = []
for i in range(0, no_layers):
    positions_perp_outer.append([])
    normal = outer_dxdzlist[i]
    theta = -math.atan(normal)
    for j in range(0, no_atoms):
        positions_perp_outer[i].append([])
        x = np.array(positions_outer[i][j])
        Rot_perp = np.zeros((3,3))
        Rot_perp[0, 0] = math.cos(theta)
        Rot_perp[2, 0] = -math.sin(theta)
        Rot_perp[1, 1] = 1
        Rot_perp[0, 2] = math.sin(theta)
        Rot_perp[2, 2] = math.cos(theta)
        rotation_perp = np.dot(Rot_perp, x)
        positions_perp_outer[i][j] = [float(rotation_perp[0]), float(rotation_perp[1]), float(rotation_perp[2])]
# Translation matrix to correct the translation made by the above loop.
# The above rotation matrix will end up translating, not only rotating, the monomers. This next loop stores the original
# (before rotation) coordinates, and translates the monomers back to them while keeping them perpendicular to the parabola.
for i in range(0, no_layers):
    x_old_center = (positions_outer[i][24][0] + positions_outer[i][25][0])/2
    y_old_center = (positions_outer[i][24][1] + positions_outer[i][25][1])/2
    z_old_center = (positions_outer[i][24][2] + positions_outer[i][25][2])/2
    old_center = [x_old_center, y_old_center, z_old_center]
    x_new_center = (positions_perp_outer[i][24][0] + positions_perp_outer[i][25][0])/2.0
    y_new_center = (positions_perp_outer[i][24][1] + positions_perp_outer[i][25][1])/2
    z_new_center = (positions_perp_outer[i][24][2] + positions_perp_outer[i][25][2])/2
    new_center = [x_new_center, y_new_center, z_new_center]
    translation_correction = np.matrix([[1, 0, 0, old_center[0] - new_center[0]], [0, 1, 0, 0], [0, 0, 1, old_center[2] - new_center[2]], [0, 0, 0, 1]])
    for j in range(0, no_atoms):
        positions_perp_outer[i][j].append(1)
        x = np.dot(translation_correction, np.array(positions_perp_outer[i][j]))
        positions_outer[i][j] = [x[0, 0], x[0, 1], x[0,2]]

# Make copies of the monomer and rotate them around the outer ring.
sys_atoms_outer = 0
space_per_outer = 2*math.pi*lim_radius_outer/no_monomers_outer
positionsrot_outer = []
for i in range(0, no_layers):
    positionsrot_outer.append([])
    radius_row = outer_pointlist[i][0]
    no_monomers_row_float = 2*math.pi*radius_row/space_per_outer
    no_monomers_row = int(round(no_monomers_row_float, 0))
    sys_atoms_outer = sys_atoms_outer + no_monomers_row*no_atoms
    angleinitial = 2*math.pi/float(no_monomers_row)
    for j in range(0, no_monomers_row):
        positionsrot_outer[i].append([])
        angle = j*angleinitial
        Rx_outer = Rot_z(angle)
        for k in range(0, no_atoms):
            positionsrot_outer[i][j].append([])
            x = np.array(positions_outer[i][k])
            rotation = np.dot(Rx_outer, x)
            rotation = [float(rotation[0]), float(rotation[1]), float(rotation[2])]
            positionsrot_outer[i][j][k] = rotation

# This is a function to copy a list (or list of lists) and put it in a new list. This is needed because in the code, lists
# need to be copied. However, if a command is made saying list2 = list1, any changes to list2 will also change list1.
# Without this loop, the code would essentially make four arm4's, as opposed to arm1-arm4.
def copylist(old):
    new = []
    for i in range(0, len(old)):
        new.append([])
        for j in range(0, len(old[i])):
            new[i].append([])
            for k in range(0, len(old[i][j])):
                new[i][j].append([])
                new[i][j][k] = old[i][j][k]
    return new

positions_a1_inner = copylist(positionsrot_inner)
positions_a1_outer = copylist(positionsrot_outer)
no_mon_in = 0
for i in range(0, len(positions_a1_inner)):
    for j in range(0, len(positions_a1_inner[i])):
        no_mon_in += 1
no_mon = no_mon_in
for i in range(0, len(positions_a1_outer)):
    for j in range(0, len(positions_a1_outer[i])):
        no_mon += 1
no_gly = int(round(no_mon*3901/1638.0))

# Make copies of glycerol and rotate them around inside the outer ring.
positions_a1_gly = []
for i in range(0, no_layers):
    positions_a1_gly.append([])
    no_monomers_row = len(positions_a1_outer[i])
    no_gly_row = int(round(no_monomers_row*no_gly/float(no_mon - no_mon_in)))
    angle_gly = 2*math.pi/float(no_gly_row)
    for j in range(0, no_gly_row):
        positions_a1_gly[i].append([])
        angle = j*angle_gly
        Rx_outer = Rot_z(angle)
        for k in range(0, len(positions_gly_arc[i])):
            positions_a1_gly[i][j].append([])
            x = np.array(positions_gly_arc[i][k])
            rotation = np.dot(Rx_outer, x)
            positions_a1_gly[i][j][k] = rotation

def transpivot(positions):
    xsum = 0
    ysum = 0
    zsum = 0
    for i in range(0, len(positions[0])):
        xsum = xsum + (positions[0][i][24][0] + positions[0][i][25][0])/2.0
        ysum = ysum + (positions[0][i][24][1] + positions[0][i][25][1])/2.0
        zsum = zsum + (positions[0][i][24][2] + positions[0][i][25][2])/2.0
    xtrans = xsum/float(len(positions[0]))
    ytrans = ysum/float(len(positions[0]))
    ztrans = zsum/float(len(positions[0]))
    translation = np.matrix([[1, 0, 0, -xtrans], [0, 1, 0, -ytrans], [0, 0, 1, -ztrans], [0, 0, 0, 1]])
    return translation

def transhalf(positions):
    xsum = 0
    ysum = 0
    zsum = 0
    for i in range(0, len(positions[3])):
        xsum = xsum + (positions[3][i][24][0] + positions[3][i][25][0])/4.0
        ysum = ysum + (positions[3][i][24][1] + positions[3][i][25][1])/4.0
        zsum = zsum + (positions[3][i][24][2] + positions[3][i][25][2])/4.0
    for i in range(0, len(positions[2])):
        xsum = xsum + (positions[2][i][24][0] + positions[2][i][25][0])/4.0
        ysum = ysum + (positions[2][i][24][1] + positions[2][i][25][1])/4.0
        zsum = zsum + (positions[2][i][24][2] + positions[2][i][25][2])/4.0
    xtrans = xsum/float(len(positions[2]))
    ytrans = ysum/float(len(positions[2]))
    ztrans = zsum/float(len(positions[2]))
    translation = np.matrix([[1, 0, 0, xtrans], [0, 1, 0, ytrans], [0, 0, 1, ztrans], [0, 0, 0, 1]])
    return translation

positions_a1 = [positions_a1_inner, positions_a1_outer, positions_a1_gly]

translation_to_pivot = transpivot(positions_a1_outer)
for i in range(0, len(positions_a1)):
    for j in range(0, len(positions_a1[i])):
        for k in range(0, len(positions_a1[i][j])):
            for l in range(0, len(positions_a1[i][j][k])):
                positions_a1[i][j][k][l] = np.append(positions_a1[i][j][k][l], 1)
                #positions_a1[i][j][k][l].append(1)
                x = np.dot(translation_to_pivot, np.array(positions_a1[i][j][k][l]))
                positions_a1[i][j][k][l] = [x[0, 0], x[0, 1], x[0, 2]]

translation_half = transhalf(positions_a1_outer)
for i in range(0, len(positions_a1)):
    for j in range(0, len(positions_a1[i])):
        for k in range(0, len(positions_a1[i][j])):
            for l in range(0, len(positions_a1[i][j][k])):
                positions_a1[i][j][k][l].append(1)
                x = np.dot(translation_half, np.array(positions_a1[i][j][k][l]))
                positions_a1[i][j][k][l] = [x[0, 0], x[0, 1], x[0, 2]]

positions_a2_inner = copylist(positions_a1_inner)
positions_a2_outer = copylist(positions_a1_outer)
positions_a2_gly = copylist(positions_a1_gly)
positions_a2 = [positions_a2_inner, positions_a2_outer, positions_a2_gly]
theta = 2*math.pi/3.0
Rot_arm2 = Rot_y(theta)
for i in range(0, len(positions_a2)):
    for j in range(0, len(positions_a2[i])):
        for k in range(0, len(positions_a2[i][j])):
            for l in range(0, len(positions_a2[i][j][k])):
                x = np.array(positions_a2[i][j][k][l])
                rotation_a2 = np.dot(Rot_arm2, x)
                positions_a2[i][j][k][l] = [float(rotation_a2[0]), float(rotation_a2[1]), float(rotation_a2[2])]

translation_to_pivot = transpivot(positions_a2_outer)
for i in range(0, len(positions_a2)):
    for j in range(0, len(positions_a2[i])):
        for k in range(0, len(positions_a2[i][j])):
            for l in range(0, len(positions_a2[i][j][k])):
                positions_a2[i][j][k][l].append(1)
                x = np.dot(translation_to_pivot, np.array(positions_a2[i][j][k][l]))
                positions_a2[i][j][k][l] = [x[0, 0], x[0, 1], x[0, 2]]

translation_half = transhalf(positions_a2_outer)
for i in range(0, len(positions_a2)):
    for j in range(0, len(positions_a2[i])):
        for k in range(0, len(positions_a2[i][j])):
            for l in range(0, len(positions_a2[i][j][k])):
                positions_a2[i][j][k][l].append(1)
                x = np.dot(translation_half, np.array(positions_a2[i][j][k][l]))
                positions_a2[i][j][k][l] = [x[0, 0], x[0, 1], x[0, 2]]

positions_a3_inner = copylist(positions_a2_inner)
positions_a3_outer = copylist(positions_a2_outer)
positions_a3_gly = copylist(positions_a2_gly)
positions_a3 = [positions_a3_inner, positions_a3_outer, positions_a3_gly]
theta = 2*math.pi/3.0
Rot_arm3 = Rot_y(theta)
for i in range(0, len(positions_a3)):
    for j in range(0, len(positions_a3[i])):
        for k in range(0, len(positions_a3[i][j])):
            for l in range(0, len(positions_a3[i][j][k])):
                x = np.array(positions_a3[i][j][k][l])
                rotation_a3 = np.dot(Rot_arm3, x)
                positions_a3[i][j][k][l] = [float(rotation_a3[0]), float(rotation_a3[1]), float(rotation_a3[2])]

translation_to_pivot = transpivot(positions_a3_outer)
for i in range(0, len(positions_a3)):
    for j in range(0, len(positions_a3[i])):
        for k in range(0, len(positions_a3[i][j])):
            for l in range(0, len(positions_a3[i][j][k])):
                positions_a3[i][j][k][l].append(1)
                x = np.dot(translation_to_pivot, np.array(positions_a3[i][j][k][l]))
                positions_a3[i][j][k][l] = [x[0, 0], x[0, 1], x[0, 2]]

translation_half = transhalf(positions_a3_outer)
for i in range(0, len(positions_a3)):
    for j in range(0, len(positions_a3[i])):
        for k in range(0, len(positions_a3[i][j])):
            for l in range(0, len(positions_a3[i][j][k])):
                positions_a3[i][j][k][l].append(1)
                x = np.dot(translation_half, np.array(positions_a3[i][j][k][l]))
                positions_a3[i][j][k][l] = [x[0, 0], x[0, 1], x[0, 2]]

junction = [positions_a1, positions_a2, positions_a3]

positions_a4_inner = copylist(positions_a2_inner)
positions_a4_outer = copylist(positions_a2_outer)
positions_a4_gly = copylist(positions_a2_gly)
positions_a4 = [positions_a4_inner, positions_a4_outer, positions_a4_gly]
positions_a5_inner = copylist(positions_a3_inner)
positions_a5_outer = copylist(positions_a3_outer)
positions_a5_gly = copylist(positions_a3_gly)
positions_a5 = [positions_a5_inner, positions_a5_outer, positions_a5_gly]
theta = math.pi
Rot_up = Rot_y(theta)
for i in range(0, len(positions_a4)):
    for j in range(0, len(positions_a4[i])):
        for k in range(0, len(positions_a4[i][j])):
            for l in range(0, len(positions_a4[i][j][k])):
                x = np.array(positions_a4[i][j][k][l])
                rotation_a4 = np.dot(Rot_up, x)
                positions_a4[i][j][k][l] = [float(rotation_a4[0]), float(rotation_a4[1]), float(rotation_a4[2])]
                x = np.array(positions_a5[i][j][k][l])
                rotation_a5 = np.dot(Rot_up, x)
                positions_a5[i][j][k][l] = [float(rotation_a5[0]), float(rotation_a5[1]), float(rotation_a5[2])]

z_max = 0
for i in range(0, len(positions_a1_inner)):
    for j in range(0, len(positions_a1_inner[i])):
        for k in range(0, no_atoms):
            if positions_a1_inner[i][j][k][2] > z_max:
                z_max = positions_a1_inner[i][j][k][2]
translation = np.matrix([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, z_max], [0, 0, 0, 1]])
for i in range(0, len(positions_a4)):
    for j in range(0, len(positions_a4[i])):
        for k in range(0, len(positions_a4[i][j])):
            for l in range(0, len(positions_a4[i][j][k])):
                positions_a4[i][j][k][l].append(1)
                x = np.dot(translation, np.array(positions_a4[i][j][k][l]))
                positions_a4[i][j][k][l] = [x[0, 0], x[0, 1], x[0, 2]]
                positions_a5[i][j][k][l].append(1)
                x = np.dot(translation, np.array(positions_a5[i][j][k][l]))
                positions_a5[i][j][k][l] = [x[0, 0], x[0, 1], x[0, 2]]

def copyjunction(old):
    new = []
    for i in range(0, len(old)):
        new.append([])
        for j in range(0, len(old[i])):
            new[i].append([])
            for k in range(0, len(old[i][j])):
                new[i][j].append([])
                for l in range(0, len(old[i][j][k])):
                    new[i][j][k].append([])
                    for m in range(0, len(old[i][j][k][l])):
                        new[i][j][k][l].append([])
                        new[i][j][k][l][m] = old[i][j][k][l][m]
    return new

junction2 = copyjunction(junction)
junction3 = copyjunction(junction)

x_total_a2 = 0
z_total_a2 = 0
divisor = 0
for i in range(0, len(positions_a2_inner)):
    for j in range(0, len(positions_a2_inner[i])):
        for k in range(0, no_atoms):
            x_total_a2 = x_total_a2 + positions_a2_inner[i][j][k][0]
            z_total_a2 = z_total_a2 + positions_a2_inner[i][j][k][2]
            divisor += 1
x_mean_a2 = x_total_a2/float(divisor)
z_mean_a2 = z_total_a2/float(divisor)

x_total_a4 = 0
z_total_a4 = 0
divisor = 0
for i in range(0, len(positions_a4_inner)):
    for j in range(0, len(positions_a4_inner[i])):
        for k in range(0, no_atoms):
            x_total_a4 = x_total_a4 + positions_a4_inner[i][j][k][0]
            z_total_a4 = z_total_a4 + positions_a4_inner[i][j][k][2]
            divisor += 1
x_mean_a4 = x_total_a4/float(divisor)
z_mean_a4 = z_total_a4/float(divisor)

translation_j2 = np.matrix([[1, 0, 0, x_mean_a4 - x_mean_a2], [0, 1, 0, 0], [0, 0, 1, z_mean_a4 - z_mean_a2], [0, 0, 0, 1]])
for i in range(0, len(junction2)):
    for j in range(0, len(junction2[i])):
        for k in range(0, len(junction2[i][j])):
            for l in range(0, len(junction2[i][j][k])):
                for m in range(0, len(junction2[i][j][k][l])):
                    junction2[i][j][k][l][m].append(1)
                    x = np.dot(translation_j2, np.array(junction2[i][j][k][l][m]))
                    junction2[i][j][k][l][m] = [x[0, 0], x[0, 1], x[0, 2]]
translation_j3 = np.matrix([[1, 0, 0, x_mean_a2 - x_mean_a4], [0, 1, 0, 0], [0, 0, 1, z_mean_a4 - z_mean_a2], [0, 0, 0, 1]])
for i in range(0, len(junction3)):
    for j in range(0, len(junction3[i])):
        for k in range(0, len(junction3[i][j])):
            for l in range(0, len(junction3[i][j][k])):
                for m in range(0, len(junction3[i][j][k][l])):
                    x = np.dot(translation_j3, np.array(junction3[i][j][k][l][m]))
                    junction3[i][j][k][l][m] = [x[0, 0], x[0, 1], x[0, 2]]

# The rotation of junction 2 and 3 occurs along an axis that does not pass through the origin. Therefore, the rotation
# will also translate the junctions. In the next section, the average coordinates of the junctions is being stored, so
# that after the rotation, the junctions can be translated back.
x_storesum_j2 = 0; y_storesum_j2 = 0; z_storesum_j2 = 0
x_storesum_j3 = 0; y_storesum_j3 = 0; z_storesum_j3 = 0
divisor = 0
for i in range(0, len(junction3)):
    for j in range(0, len(junction3[i]) - 1):
        for k in range(0, len(junction3[i][j])):
            for l in range(0, len(junction3[i][j][k])):
                x_storesum_j2 = x_storesum_j2 + junction2[i][j][k][l][24][0]
                y_storesum_j2 = y_storesum_j2 + junction2[i][j][k][l][24][1]
                z_storesum_j2 = z_storesum_j2 + junction2[i][j][k][l][24][2]
                x_storesum_j3 = x_storesum_j3 + junction3[i][j][k][l][24][0]
                y_storesum_j3 = y_storesum_j3 + junction3[i][j][k][l][24][1]
                z_storesum_j3 = z_storesum_j3 + junction3[i][j][k][l][24][2]
                divisor += 1
x_store_j2 = x_storesum_j2/float(divisor); y_store_j2 = y_storesum_j2/float(divisor); z_store_j2 = z_storesum_j2/float(divisor)
x_store_j3 = x_storesum_j3/float(divisor); y_store_j3 = y_storesum_j3/float(divisor); z_store_j3 = z_storesum_j3/float(divisor)

# The next two sections rotate junctions 2 and 3 by 70.5 degrees around the axis where they are connected to junction 1.
theta_ideal = -math.pi*47/120.0
u = -math.sqrt(3)/2.0
w = 1/2.0
Rx_ideal = np.zeros((3, 3))  # makes a 3 x 3 zero matrix
Rx_ideal[0, 0] = math.cos(theta_ideal) + u**2*(1 - math.cos(theta_ideal))
Rx_ideal[0, 1] = -w*math.sin(theta_ideal)
Rx_ideal[0, 2] = u*w*(1 - math.cos(theta_ideal))
Rx_ideal[1, 0] = w*math.sin(theta_ideal)
Rx_ideal[1, 1] = math.cos(theta_ideal)
Rx_ideal[1, 2] = -u*math.sin(theta_ideal)
Rx_ideal[2, 0] = w*u*(1 - math.cos(theta_ideal))
Rx_ideal[2, 1] = u*math.sin(theta_ideal)
Rx_ideal[2, 2] = math.cos(theta_ideal) + w**2*(1 - math.cos(theta_ideal))
for i in range(0, len(junction2)):
    for j in range(0, len(junction2[i])):
        for k in range(0, len(junction2[i][j])):
            for l in range(0, len(junction2[i][j][k])):
                for m in range(0, len(junction2[i][j][k][l])):
                    x = np.array(junction2[i][j][k][l][m])
                    rotation_j2 = np.dot(Rx_ideal, x)
                    junction2[i][j][k][l][m] = [float(rotation_j2[0]), float(rotation_j2[1]), float(rotation_j2[2])]

u = math.sqrt(3)/2.0
w = 1/2.0
Rx_ideal = np.zeros((3, 3))  # makes a 3 x 3 zero matrix
Rx_ideal[0, 0] = math.cos(theta_ideal) + u**2*(1 - math.cos(theta_ideal))
Rx_ideal[0, 1] = -w*math.sin(theta_ideal)
Rx_ideal[0, 2] = u*w*(1 - math.cos(theta_ideal))
Rx_ideal[1, 0] = w*math.sin(theta_ideal)
Rx_ideal[1, 1] = math.cos(theta_ideal)
Rx_ideal[1, 2] = -u*math.sin(theta_ideal)
Rx_ideal[2, 0] = w*u*(1 - math.cos(theta_ideal))
Rx_ideal[2, 1] = u*math.sin(theta_ideal)
Rx_ideal[2, 2] = math.cos(theta_ideal) + w**2*(1 - math.cos(theta_ideal))
for i in range(0, len(junction3)):
    for j in range(0, len(junction3[i])):
        for k in range(0, len(junction3[i][j])):
            for l in range(0, len(junction3[i][j][k])):
                for m in range(0, len(junction3[i][j][k][l])):
                    x = np.array(junction3[i][j][k][l][m])
                    rotation_j3 = np.dot(Rx_ideal, x)
                    junction3[i][j][k][l][m] = [float(rotation_j3[0]), float(rotation_j3[1]), float(rotation_j3[2])]

# This section finds the new average coordinates of junctions 2 and 3, so that they can be translated back to their
# original locations.
x_newsum_j2 = 0; y_newsum_j2 = 0; z_newsum_j2 = 0
x_newsum_j3 = 0; y_newsum_j3 = 0; z_newsum_j3 = 0
divisor = 0
for i in range(0, len(junction3)):
    for j in range(0, len(junction3[i]) - 1):
        for k in range(0, len(junction3[i][j])):
            for l in range(0, len(junction3[i][j][k])):
                x_newsum_j2 = x_newsum_j2 + junction2[i][j][k][l][24][0]
                y_newsum_j2 = y_newsum_j2 + junction2[i][j][k][l][24][1]
                z_newsum_j2 = z_newsum_j2 + junction2[i][j][k][l][24][2]
                x_newsum_j3 = x_newsum_j3 + junction3[i][j][k][l][24][0]
                y_newsum_j3 = y_newsum_j3 + junction3[i][j][k][l][24][1]
                z_newsum_j3 = z_newsum_j3 + junction3[i][j][k][l][24][2]
                divisor += 1
x_new_j2 = x_newsum_j2/float(divisor); y_new_j2 = y_newsum_j2/float(divisor); z_new_j2 = z_newsum_j2/float(divisor)
x_new_j3 = x_newsum_j3/float(divisor); y_new_j3 = y_newsum_j3/float(divisor); z_new_j3 = z_newsum_j3/float(divisor)

translation_j2 = np.matrix([[1, 0, 0, x_store_j2 - x_new_j2], [0, 1, 0, y_store_j2 - y_new_j2], [0, 0, 1, z_store_j2 - z_new_j2], [0, 0, 0, 1]])
for i in range(0, len(junction2)):
    for j in range(0, len(junction2[i])):
        for k in range(0, len(junction2[i][j])):
            for l in range(0, len(junction2[i][j][k])):
                for m in range(0, len(junction2[i][j][k][l])):
                    junction2[i][j][k][l][m].append(1)
                    x = np.dot(translation_j2, np.array(junction2[i][j][k][l][m]))
                    junction2[i][j][k][l][m] = [x[0, 0], x[0, 1], x[0, 2]]
translation_j3 = np.matrix([[1, 0, 0, x_store_j3 - x_new_j3], [0, 1, 0, y_store_j3 - y_new_j3], [0, 0, 1, z_store_j3 - z_new_j3], [0, 0, 0, 1]])
for i in range(0, len(junction3)):
    for j in range(0, len(junction3[i])):
        for k in range(0, len(junction3[i][j])):
            for l in range(0, len(junction3[i][j][k])):
                for m in range(0, len(junction3[i][j][k][l])):
                    junction3[i][j][k][l][m].append(1)
                    x = np.dot(translation_j3, np.array(junction3[i][j][k][l][m]))
                    junction3[i][j][k][l][m] = [x[0, 0], x[0, 1], x[0, 2]]

# This section groups junction2 and 3 together, and rotates them by 70.5 degrees around the z-axis.
Rx_ideal = Rot_z(theta_ideal)
for i in range(0, len(junction2)):
    for j in range(0, len(junction2[i])):
        for k in range(0, len(junction2[i][j])):
            for l in range(0, len(junction2[i][j][k])):
                for m in range(0, len(junction2[i][j][k][l])):
                    x = np.array(junction2[i][j][k][l][m])
                    rotation_j2 = np.dot(Rx_ideal, x)
                    junction2[i][j][k][l][m] = [float(rotation_j2[0]), float(rotation_j2[1]), float(rotation_j2[2])]
for i in range(0, len(junction3)):
    for j in range(0, len(junction3[i])):
        for k in range(0, len(junction3[i][j])):
            for l in range(0, len(junction3[i][j][k])):
                for m in range(0, len(junction3[i][j][k][l])):
                    x = np.array(junction3[i][j][k][l][m])
                    rotation_j3 = np.dot(Rx_ideal, x)
                    junction3[i][j][k][l][m] = [float(rotation_j3[0]), float(rotation_j3[1]), float(rotation_j3[2])]

junction4 = copyjunction(junction)
junction5 = copyjunction(junction)
junction6 = copyjunction(junction)
junction7 = copyjunction(junction)

x_max_j1 = 0; z_max_j1 = 0; z_min_j1 = 0
for i in range(0, len(junction)):
    for j in range(0, len(junction[i]) - 1):
        for k in range(0, len(junction[i][j])):
            for l in range(0, len(junction[i][j][k])):
                if (junction[i][j][k][l][24][0] + junction[i][j][k][l][25][0])/2.0 > x_max_j1:
                    x_max_j1 = (junction[i][j][k][l][24][0] + junction[i][j][k][l][25][0])/2.0
                if (junction[i][j][k][l][24][2] + junction[i][j][k][l][25][2])/2.0 > z_max_j1:
                    z_max_j1 = (junction[i][j][k][l][24][2] + junction[i][j][k][l][25][2])/2.0
                if (junction[i][j][k][l][24][2] + junction[i][j][k][l][25][2])/2.0 < z_min_j1:
                    z_min_j1 = (junction[i][j][k][l][24][2] + junction[i][j][k][l][25][2])/2.0

translation_j4 = np.matrix([[1, 0, 0, 2*x_max_j1], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
for i in range(0, len(junction4)):
    for j in range(0, len(junction4[i])):
        for k in range(0, len(junction4[i][j])):
            for l in range(0, len(junction4[i][j][k])):
                for m in range(0, len(junction4[i][j][k][l])):
                    x = np.dot(translation_j4, np.array(junction4[i][j][k][l][m]))
                    junction4[i][j][k][l][m] = [x[0, 0], x[0, 1], x[0, 2]]
translation_j5 = np.matrix([[1, 0, 0, x_max_j1], [0, 1, 0, 0], [0, 0, 1, z_min_j1 - z_max_j1], [0, 0, 0, 1]])
for i in range(0, len(junction5)):
    for j in range(0, len(junction5[i])):
        for k in range(0, len(junction5[i][j])):
            for l in range(0, len(junction5[i][j][k])):
                for m in range(0, len(junction5[i][j][k][l])):
                    x = np.dot(translation_j5, np.array(junction5[i][j][k][l][m]))
                    junction5[i][j][k][l][m] = [x[0, 0], x[0, 1], x[0, 2]]
translation_j6 = np.matrix([[1, 0, 0, -2*x_max_j1], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]])
for i in range(0, len(junction6)):
    for j in range(0, len(junction6[i])):
        for k in range(0, len(junction6[i][j])):
            for l in range(0, len(junction6[i][j][k])):
                for m in range(0, len(junction6[i][j][k][l])):
                    x = np.dot(translation_j6, np.array(junction6[i][j][k][l][m]))
                    junction6[i][j][k][l][m] = [x[0, 0], x[0, 1], x[0, 2]]
translation_j7 = np.matrix([[1, 0, 0, -x_max_j1], [0, 1, 0, 0], [0, 0, 1, z_min_j1 - z_max_j1], [0, 0, 0, 1]])
for i in range(0, len(junction7)):
    for j in range(0, len(junction7[i])):
        for k in range(0, len(junction7[i][j])):
            for l in range(0, len(junction7[i][j][k])):
                for m in range(0, len(junction7[i][j][k][l])):
                    x = np.dot(translation_j7, np.array(junction7[i][j][k][l][m]))
                    junction7[i][j][k][l][m] = [x[0, 0], x[0, 1], x[0, 2]]

# Now each individual junction must be rotated along its connection to the junction of junctions.
# Then, the entire junction will be rotated.
# This next loop will store the average location of junctions 4-7.
x_storesum_j4 = 0; y_storesum_j4 = 0; z_storesum_j4 = 0
x_storesum_j5 = 0; y_storesum_j5 = 0; z_storesum_j5 = 0
x_storesum_j6 = 0; y_storesum_j6 = 0; z_storesum_j6 = 0
x_storesum_j7 = 0; y_storesum_j7 = 0; z_storesum_j7 = 0
divisor = 0
for i in range(0, len(junction4)):
    for j in range(0, len(junction4[i]) - 1):
        for k in range(0, len(junction4[i][j])):
            for l in range(0, len(junction4[i][j][k])):
                x_storesum_j4 = x_storesum_j4 + junction4[i][j][k][l][24][0]
                y_storesum_j4 = y_storesum_j4 + junction4[i][j][k][l][24][1]
                z_storesum_j4 = z_storesum_j4 + junction4[i][j][k][l][24][2]
                x_storesum_j5 = x_storesum_j5 + junction5[i][j][k][l][24][0]
                y_storesum_j5 = y_storesum_j5 + junction5[i][j][k][l][24][1]
                z_storesum_j5 = z_storesum_j5 + junction5[i][j][k][l][24][2]
                x_storesum_j6 = x_storesum_j6 + junction6[i][j][k][l][24][0]
                y_storesum_j6 = y_storesum_j6 + junction6[i][j][k][l][24][1]
                z_storesum_j6 = z_storesum_j6 + junction6[i][j][k][l][24][2]
                x_storesum_j7 = x_storesum_j7 + junction7[i][j][k][l][24][0]
                y_storesum_j7 = y_storesum_j7 + junction7[i][j][k][l][24][1]
                z_storesum_j7 = z_storesum_j7 + junction7[i][j][k][l][24][2]
                divisor += 1
x_store_j4 = x_storesum_j4/float(divisor); y_store_j4 = y_storesum_j4/float(divisor); z_store_j4 = z_storesum_j4/float(divisor)
x_store_j5 = x_storesum_j5/float(divisor); y_store_j5 = y_storesum_j5/float(divisor); z_store_j5 = z_storesum_j5/float(divisor)
x_store_j6 = x_storesum_j6/float(divisor); y_store_j6 = y_storesum_j6/float(divisor); z_store_j6 = z_storesum_j6/float(divisor)
x_store_j7 = x_storesum_j7/float(divisor); y_store_j7 = y_storesum_j7/float(divisor); z_store_j7 = z_storesum_j7/float(divisor)

u = math.sqrt(3)/2.0
w = 1/2.0
Rx_ideal_j4 = np.zeros((3, 3))  # makes a 3 x 3 zero matrix
Rx_ideal_j4[0, 0] = math.cos(theta_ideal) + u**2*(1 - math.cos(theta_ideal))
Rx_ideal_j4[0, 1] = -w*math.sin(theta_ideal)
Rx_ideal_j4[0, 2] = u*w*(1 - math.cos(theta_ideal))
Rx_ideal_j4[1, 0] = w*math.sin(theta_ideal)
Rx_ideal_j4[1, 1] = math.cos(theta_ideal)
Rx_ideal_j4[1, 2] = -u*math.sin(theta_ideal)
Rx_ideal_j4[2, 0] = w*u*(1 - math.cos(theta_ideal))
Rx_ideal_j4[2, 1] = u*math.sin(theta_ideal)
Rx_ideal_j4[2, 2] = math.cos(theta_ideal) + w**2*(1 - math.cos(theta_ideal))
for i in range(0, len(junction4)):
    for j in range(0, len(junction4[i])):
        for k in range(0, len(junction4[i][j])):
            for l in range(0, len(junction4[i][j][k])):
                for m in range(0, len(junction4[i][j][k][l])):
                    x = np.array(junction4[i][j][k][l][m])
                    rotation_j4 = np.dot(Rx_ideal_j4, x)
                    junction4[i][j][k][l][m] = [float(rotation_j4[0]), float(rotation_j4[1]), float(rotation_j4[2])]
w = -1
Rx_ideal_j5 = np.zeros((3, 3))  # makes a 3 x 3 zero matrix
Rx_ideal_j5[0, 0] = math.cos(theta_ideal)
Rx_ideal_j5[0, 1] = -w*math.sin(theta_ideal)
Rx_ideal_j5[0, 2] = 0
Rx_ideal_j5[1, 0] = w*math.sin(theta_ideal)
Rx_ideal_j5[1, 1] = math.cos(theta_ideal)
Rx_ideal_j5[1, 2] = 0
Rx_ideal_j5[2, 0] = 0
Rx_ideal_j5[2, 1] = 0
Rx_ideal_j5[2, 2] = math.cos(theta_ideal) + w**2*(1 - math.cos(theta_ideal))
for i in range(0, len(junction5)):
    for j in range(0, len(junction5[i])):
        for k in range(0, len(junction5[i][j])):
            for l in range(0, len(junction5[i][j][k])):
                for m in range(0, len(junction5[i][j][k][l])):
                    x = np.array(junction5[i][j][k][l][m])
                    rotation_j5 = np.dot(Rx_ideal_j5, x)
                    junction5[i][j][k][l][m] = [float(rotation_j5[0]), float(rotation_j5[1]), float(rotation_j5[2])]
u = -math.sqrt(3) / 2.0
w = 1 / 2.0
Rx_ideal_j6 = np.zeros((3, 3))  # makes a 3 x 3 zero matrix
Rx_ideal_j6[0, 0] = math.cos(theta_ideal) + u ** 2 * (1 - math.cos(theta_ideal))
Rx_ideal_j6[0, 1] = -w * math.sin(theta_ideal)
Rx_ideal_j6[0, 2] = u * w * (1 - math.cos(theta_ideal))
Rx_ideal_j6[1, 0] = w * math.sin(theta_ideal)
Rx_ideal_j6[1, 1] = math.cos(theta_ideal)
Rx_ideal_j6[1, 2] = -u * math.sin(theta_ideal)
Rx_ideal_j6[2, 0] = w * u * (1 - math.cos(theta_ideal))
Rx_ideal_j6[2, 1] = u * math.sin(theta_ideal)
Rx_ideal_j6[2, 2] = math.cos(theta_ideal) + w ** 2 * (1 - math.cos(theta_ideal))
for i in range(0, len(junction6)):
    for j in range(0, len(junction6[i])):
        for k in range(0, len(junction6[i][j])):
            for l in range(0, len(junction6[i][j][k])):
                for m in range(0, len(junction6[i][j][k][l])):
                    x = np.array(junction6[i][j][k][l][m])
                    rotation_j6 = np.dot(Rx_ideal_j6, x)
                    junction6[i][j][k][l][m] = [float(rotation_j6[0]), float(rotation_j6[1]), float(rotation_j6[2])]
w = -1
Rx_ideal_j7 = np.zeros((3, 3))  # makes a 3 x 3 zero matrix
Rx_ideal_j7[0, 0] = math.cos(theta_ideal)
Rx_ideal_j7[0, 1] = -w*math.sin(theta_ideal)
Rx_ideal_j7[0, 2] = 0
Rx_ideal_j7[1, 0] = w*math.sin(theta_ideal)
Rx_ideal_j7[1, 1] = math.cos(theta_ideal)
Rx_ideal_j7[1, 2] = 0
Rx_ideal_j7[2, 0] = 0
Rx_ideal_j7[2, 1] = 0
Rx_ideal_j7[2, 2] = math.cos(theta_ideal) + w**2*(1 - math.cos(theta_ideal))
for i in range(0, len(junction7)):
    for j in range(0, len(junction7[i])):
        for k in range(0, len(junction7[i][j])):
            for l in range(0, len(junction7[i][j][k])):
                for m in range(0, len(junction7[i][j][k][l])):
                    x = np.array(junction7[i][j][k][l][m])
                    rotation_j7 = np.dot(Rx_ideal_j7, x)
                    junction7[i][j][k][l][m] = [float(rotation_j7[0]), float(rotation_j7[1]), float(rotation_j7[2])]

x_newsum_j4 = 0; y_newsum_j4 = 0; z_newsum_j4 = 0
x_newsum_j5 = 0; y_newsum_j5 = 0; z_newsum_j5 = 0
x_newsum_j6 = 0; y_newsum_j6 = 0; z_newsum_j6 = 0
x_newsum_j7 = 0; y_newsum_j7 = 0; z_newsum_j7 = 0
divisor = 0
for i in range(0, len(junction4)):
    for j in range(0, len(junction4[i]) - 1):
        for k in range(0, len(junction4[i][j])):
            for l in range(0, len(junction4[i][j][k])):
                x_newsum_j4 = x_newsum_j4 + (junction4[i][j][k][l][24][0] + junction4[i][j][k][l][25][0])/2.0
                y_newsum_j4 = y_newsum_j4 + (junction4[i][j][k][l][24][1] + junction4[i][j][k][l][25][1])/2.0
                z_newsum_j4 = z_newsum_j4 + (junction4[i][j][k][l][24][2] + junction4[i][j][k][l][25][2])/2.0
                x_newsum_j5 = x_newsum_j5 + (junction5[i][j][k][l][24][0] + junction5[i][j][k][l][25][0])/2.0
                y_newsum_j5 = y_newsum_j5 + (junction5[i][j][k][l][24][1] + junction5[i][j][k][l][25][1])/2.0
                z_newsum_j5 = z_newsum_j5 + (junction5[i][j][k][l][24][2] + junction5[i][j][k][l][25][2])/2.0
                x_newsum_j6 = x_newsum_j6 + (junction6[i][j][k][l][24][0] + junction6[i][j][k][l][25][0])/2.0
                y_newsum_j6 = y_newsum_j6 + (junction6[i][j][k][l][24][1] + junction6[i][j][k][l][25][1])/2.0
                z_newsum_j6 = z_newsum_j6 + (junction6[i][j][k][l][24][2] + junction6[i][j][k][l][25][2])/2.0
                x_newsum_j7 = x_newsum_j7 + (junction7[i][j][k][l][24][0] + junction7[i][j][k][l][25][0])/2.0
                y_newsum_j7 = y_newsum_j7 + (junction7[i][j][k][l][24][1] + junction7[i][j][k][l][25][1])/2.0
                z_newsum_j7 = z_newsum_j7 + (junction7[i][j][k][l][24][2] + junction7[i][j][k][l][25][2])/2.0
                divisor += 1
x_new_j4 = x_newsum_j4/float(divisor); y_new_j4 = y_newsum_j4/float(divisor); z_new_j4 = z_newsum_j4/float(divisor)
x_new_j5 = x_newsum_j5/float(divisor); y_new_j5 = y_newsum_j5/float(divisor); z_new_j5 = z_newsum_j5/float(divisor)
x_new_j6 = x_newsum_j6/float(divisor); y_new_j6 = y_newsum_j6/float(divisor); z_new_j6 = z_newsum_j6/float(divisor)
x_new_j7 = x_newsum_j7/float(divisor); y_new_j7 = y_newsum_j7/float(divisor); z_new_j7 = z_newsum_j7/float(divisor)

translation_j4 = np.matrix([[1, 0, 0, x_store_j4 - x_new_j4], [0, 1, 0, y_store_j4 - y_new_j4], [0, 0, 1, z_store_j4 - z_new_j4], [0, 0, 0, 1]])
for i in range(0, len(junction4)):
    for j in range(0, len(junction4[i])):
        for k in range(0, len(junction4[i][j])):
            for l in range(0, len(junction4[i][j][k])):
                for m in range(0, len(junction4[i][j][k][l])):
                    junction4[i][j][k][l][m].append(1)
                    x = np.dot(translation_j4, np.array(junction4[i][j][k][l][m]))
                    junction4[i][j][k][l][m] = [x[0, 0], x[0, 1], x[0, 2]]
translation_j5 = np.matrix([[1, 0, 0, x_store_j5 - x_new_j5], [0, 1, 0, y_store_j5 - y_new_j5], [0, 0, 1, z_store_j5 - z_new_j5], [0, 0, 0, 1]])
for i in range(0, len(junction5)):
    for j in range(0, len(junction5[i])):
        for k in range(0, len(junction5[i][j])):
            for l in range(0, len(junction5[i][j][k])):
                for m in range(0, len(junction5[i][j][k][l])):
                    junction5[i][j][k][l][m].append(1)
                    x = np.dot(translation_j5, np.array(junction5[i][j][k][l][m]))
                    junction5[i][j][k][l][m] = [x[0, 0], x[0, 1], x[0, 2]]
translation_j6 = np.matrix([[1, 0, 0, x_store_j6 - x_new_j6], [0, 1, 0, y_store_j6 - y_new_j6], [0, 0, 1, z_store_j6 - z_new_j6], [0, 0, 0, 1]])
for i in range(0, len(junction6)):
    for j in range(0, len(junction6[i])):
        for k in range(0, len(junction6[i][j])):
            for l in range(0, len(junction6[i][j][k])):
                for m in range(0, len(junction6[i][j][k][l])):
                    junction6[i][j][k][l][m].append(1)
                    x = np.dot(translation_j6, np.array(junction6[i][j][k][l][m]))
                    junction6[i][j][k][l][m] = [x[0, 0], x[0, 1], x[0, 2]]
translation_j7 = np.matrix([[1, 0, 0, x_store_j7 - x_new_j7], [0, 1, 0, y_store_j7 - y_new_j7], [0, 0, 1, z_store_j7 - z_new_j7], [0, 0, 0, 1]])
for i in range(0, len(junction7)):
    for j in range(0, len(junction7[i])):
        for k in range(0, len(junction7[i][j])):
            for l in range(0, len(junction7[i][j][k])):
                for m in range(0, len(junction7[i][j][k][l])):
                    junction7[i][j][k][l][m].append(1)
                    x = np.dot(translation_j7, np.array(junction7[i][j][k][l][m]))
                    junction7[i][j][k][l][m] = [x[0, 0], x[0, 1], x[0, 2]]

superjunction1 = [junction4, junction5]
superjunction2 = [junction6, junction7]
x_storesum_sj1 = 0; y_storesum_sj1 = 0; z_storesum_sj1 = 0
x_storesum_sj2 = 0; y_storesum_sj2 = 0; z_storesum_sj2 = 0
divisor = 0
for m in range(0, len(superjunction1)):
    for i in range(0, len(superjunction1[m])):
        for j in range(0, len(superjunction1[m][i]) - 1):
            for k in range(0, len(superjunction1[m][i][j])):
                for l in range(0, len(superjunction1[m][i][j][k])):
                    x_storesum_sj1 = x_storesum_sj1 + superjunction1[m][i][j][k][l][24][0]
                    y_storesum_sj1 = y_storesum_sj1 + superjunction1[m][i][j][k][l][24][1]
                    z_storesum_sj1 = z_storesum_sj1 + superjunction1[m][i][j][k][l][24][2]
                    x_storesum_sj2 = x_storesum_sj2 + superjunction2[m][i][j][k][l][24][0]
                    y_storesum_sj2 = y_storesum_sj2 + superjunction2[m][i][j][k][l][24][1]
                    z_storesum_sj2 = z_storesum_sj2 + superjunction2[m][i][j][k][l][24][2]
                    divisor += 1
x_store_sj1 = x_storesum_sj1/float(divisor); y_store_sj1 = y_storesum_sj1/float(divisor); z_store_sj1 = z_storesum_sj1/float(divisor)
x_store_sj2 = x_storesum_sj2/float(divisor); y_store_sj2 = y_storesum_sj2/float(divisor); z_store_sj2 = z_storesum_sj2/float(divisor)

u = math.sqrt(3)/2.0
w = -1/2.0
Rx_ideal_sj1 = np.zeros((3, 3))  # makes a 3 x 3 zero matrix
Rx_ideal_sj1[0, 0] = math.cos(theta_ideal) + u**2*(1 - math.cos(theta_ideal))
Rx_ideal_sj1[0, 1] = -w*math.sin(theta_ideal)
Rx_ideal_sj1[0, 2] = u*w*(1 - math.cos(theta_ideal))
Rx_ideal_sj1[1, 0] = w*math.sin(theta_ideal)
Rx_ideal_sj1[1, 1] = math.cos(theta_ideal)
Rx_ideal_sj1[1, 2] = -u*math.sin(theta_ideal)
Rx_ideal_sj1[2, 0] = w*u*(1 - math.cos(theta_ideal))
Rx_ideal_sj1[2, 1] = u*math.sin(theta_ideal)
Rx_ideal_sj1[2, 2] = math.cos(theta_ideal) + w**2*(1 - math.cos(theta_ideal))
for n in range(0, len(superjunction1)):
    for i in range(0, len(superjunction1[n])):
        for j in range(0, len(superjunction1[n][i])):
            for k in range(0, len(superjunction1[n][i][j])):
                for l in range(0, len(superjunction1[n][i][j][k])):
                    for m in range(0, len(superjunction1[n][i][j][k][l])):
                        x = np.array(superjunction1[n][i][j][k][l][m])
                        rotation_sj1 = np.dot(Rx_ideal_sj1, x)
                        superjunction1[n][i][j][k][l][m] = [float(rotation_sj1[0]), float(rotation_sj1[1]), float(rotation_sj1[2])]
u = -math.sqrt(3)/2.0
w = -1/2.0
Rx_ideal_sj2 = np.zeros((3, 3))  # makes a 3 x 3 zero matrix
Rx_ideal_sj2[0, 0] = math.cos(theta_ideal) + u**2*(1 - math.cos(theta_ideal))
Rx_ideal_sj2[0, 1] = -w*math.sin(theta_ideal)
Rx_ideal_sj2[0, 2] = u*w*(1 - math.cos(theta_ideal))
Rx_ideal_sj2[1, 0] = w*math.sin(theta_ideal)
Rx_ideal_sj2[1, 1] = math.cos(theta_ideal)
Rx_ideal_sj2[1, 2] = -u*math.sin(theta_ideal)
Rx_ideal_sj2[2, 0] = w*u*(1 - math.cos(theta_ideal))
Rx_ideal_sj2[2, 1] = u*math.sin(theta_ideal)
Rx_ideal_sj2[2, 2] = math.cos(theta_ideal) + w**2*(1 - math.cos(theta_ideal))
for n in range(0, len(superjunction2)):
    for i in range(0, len(superjunction2[n])):
        for j in range(0, len(superjunction2[n][i])):
            for k in range(0, len(superjunction2[n][i][j])):
                for l in range(0, len(superjunction2[n][i][j][k])):
                    for m in range(0, len(superjunction2[n][i][j][k][l])):
                        x = np.array(superjunction2[n][i][j][k][l][m])
                        rotation_sj2 = np.dot(Rx_ideal_sj2, x)
                        superjunction2[n][i][j][k][l][m] = [float(rotation_sj2[0]), float(rotation_sj2[1]), float(rotation_sj2[2])]

x_newsum_sj1 = 0; y_newsum_sj1 = 0; z_newsum_sj1 = 0
x_newsum_sj2 = 0; y_newsum_sj2 = 0; z_newsum_sj2 = 0
divisor = 0
for m in range(0, len(superjunction1)):
    for i in range(0, len(superjunction1[m])):
        for j in range(0, len(superjunction1[m][i]) - 1):
            for k in range(0, len(superjunction1[m][i][j])):
                for l in range(0, len(superjunction1[m][i][j][k])):
                    x_newsum_sj1 = x_newsum_sj1 + superjunction1[m][i][j][k][l][24][0]
                    y_newsum_sj1 = y_newsum_sj1 + superjunction1[m][i][j][k][l][24][1]
                    z_newsum_sj1 = z_newsum_sj1 + superjunction1[m][i][j][k][l][24][2]
                    x_newsum_sj2 = x_newsum_sj2 + superjunction2[m][i][j][k][l][24][0]
                    y_newsum_sj2 = y_newsum_sj2 + superjunction2[m][i][j][k][l][24][1]
                    z_newsum_sj2 = z_newsum_sj2 + superjunction2[m][i][j][k][l][24][2]
                    divisor += 1
x_new_sj1 = x_newsum_sj1/float(divisor); y_new_sj1 = y_newsum_sj1/float(divisor); z_new_sj1 = z_newsum_sj1/float(divisor)
x_new_sj2 = x_newsum_sj2/float(divisor); y_new_sj2 = y_newsum_sj2/float(divisor); z_new_sj2 = z_newsum_sj2/float(divisor)

translation_sj1 = np.matrix([[1, 0, 0, x_store_sj1 - x_new_sj1], [0, 1, 0, y_store_sj1 - y_new_sj1], [0, 0, 1, z_store_sj1 - z_new_sj1], [0, 0, 0, 1]])
for n in range(0, len(superjunction1)):
    for i in range(0, len(superjunction1[n])):
        for j in range(0, len(superjunction1[n][i])):
            for k in range(0, len(superjunction1[n][i][j])):
                for l in range(0, len(superjunction1[n][i][j][k])):
                    for m in range(0, len(superjunction1[n][i][j][k][l])):
                        superjunction1[n][i][j][k][l][m].append(1)
                        x = np.dot(translation_sj1, np.array(superjunction1[n][i][j][k][l][m]))
                        superjunction1[n][i][j][k][l][m] = [x[0, 0], x[0, 1], x[0, 2]]
translation_sj2 = np.matrix([[1, 0, 0, x_store_sj2 - x_new_sj2], [0, 1, 0, y_store_sj2 - y_new_sj2], [0, 0, 1, z_store_sj2 - z_new_sj2], [0, 0, 0, 1]])
for n in range(0, len(superjunction2)):
    for i in range(0, len(superjunction2[n])):
        for j in range(0, len(superjunction2[n][i])):
            for k in range(0, len(superjunction2[n][i][j])):
                for l in range(0, len(superjunction2[n][i][j][k])):
                    for m in range(0, len(superjunction2[n][i][j][k][l])):
                        superjunction2[n][i][j][k][l][m].append(1)
                        x = np.dot(translation_sj2, np.array(superjunction2[n][i][j][k][l][m]))
                        superjunction2[n][i][j][k][l][m] = [x[0, 0], x[0, 1], x[0, 2]]

# To redefine each junction, so that arms can be removed, to match the unit cell image.
# Junctions 2, 4 and 7 will lose their outermost arms:
    # Junction2: arms 1 and 3, junction4: arms 1 and 2, junction7: arms 2 and 3
# Junctions 1, 3, 5 and 6 will remain the same.
unitjunction = copyjunction(junction)
unitjunction3 = copyjunction(junction3)
unitjunction5 = copyjunction(junction5)
unitjunction6 = copyjunction(junction6)

unitjunction2 = []
for i in range(0, len(junction2) - 2):
    unitjunction2.append([])
    for j in range(0, len(junction2[i + 1])):
        unitjunction2[i].append([])
        for k in range(0, len(junction2[i + 1][j])):
            unitjunction2[i][j].append([])
            for l in range(0, len(junction2[i + 1][j][k])):
                unitjunction2[i][j][k].append([])
                for m in range(0, len(junction2[i + 1][j][k][l])):
                    unitjunction2[i][j][k][l].append([])
                    unitjunction2[i][j][k][l][m] = junction2[i + 1][j][k][l][m]
unitjunction4 = []
for i in range(0, len(junction4) - 2):
    unitjunction4.append([])
    for j in range(0, len(junction4[i + 2])):
        unitjunction4[i].append([])
        for k in range(0, len(junction4[i + 2][j])):
            unitjunction4[i][j].append([])
            for l in range(0, len(junction4[i + 2][j][k])):
                unitjunction4[i][j][k].append([])
                for m in range(0, len(junction4[i + 2][j][k][l])):
                    unitjunction4[i][j][k][l].append([])
                    unitjunction4[i][j][k][l][m] = junction4[i + 2][j][k][l][m]
unitjunction7 = []
for i in range(0, len(junction7) - 2):
    unitjunction7.append([])
    for j in range(0, len(junction7[i])):
        unitjunction7[i].append([])
        for k in range(0, len(junction7[i][j])):
            unitjunction7[i][j].append([])
            for l in range(0, len(junction7[i][j][k])):
                unitjunction7[i][j][k].append([])
                for m in range(0, len(junction7[i][j][k][l])):
                    unitjunction7[i][j][k][l].append([])
                    unitjunction7[i][j][k][l][m] = junction7[i][j][k][l][m]

final = [unitjunction, unitjunction2, unitjunction3, unitjunction4, unitjunction5, unitjunction6, unitjunction7]

theta_final_y = -math.pi/6.0
Rot_final_y = Rot_y(theta_final_y)
for n in range(0, len(final)):
    for i in range(0, len(final[n])):
        for j in range(0, len(final[n][i])):
            for k in range(0, len(final[n][i][j])):
                for l in range(0, len(final[n][i][j][k])):
                    for m in range(0, len(final[n][i][j][k][l])):
                        x = np.array(final[n][i][j][k][l][m])
                        x = [x[0], x[1], x[2]]
                        rotation_final = np.dot(Rot_final_y, x)
                        final[n][i][j][k][l][m] = [float(rotation_final[0]), float(rotation_final[1]), float(rotation_final[2])]
# ?????
"""theta_final_x = math.pi/6.0
Rot_final_x = Rot_x(theta_final_x)
for n in range(0, len(final)):
    for i in range(0, len(final[n])):
        for j in range(0, len(final[n][i])):
            for k in range(0, len(final[n][i][j])):
                for l in range(0, len(final[n][i][j][k])):
                    for m in range(0, len(final[n][i][j][k][l])):
                        x = np.array(final[n][i][j][k][l][m])
                        x = [x[0], x[1], x[2]]
                        rotation_final = np.dot(Rot_final_x, x)
                        final[n][i][j][k][l][m] = [float(rotation_final[0]), float(rotation_final[1]), float(rotation_final[2])]

theta_final_z = -math.pi/4.0
Rot_final_z = Rot_z(theta_final_z)
for n in range(0, len(final)):
    for i in range(0, len(final[n])):
        for j in range(0, len(final[n][i])):
            for k in range(0, len(final[n][i][j])):
                for l in range(0, len(final[n][i][j][k])):
                    for m in range(0, len(final[n][i][j][k][l])):
                        x = np.array(final[n][i][j][k][l][m])
                        x = [x[0], x[1], x[2]]
                        rotation_final = np.dot(Rot_final_z, x)
                        final[n][i][j][k][l][m] = [float(rotation_final[0]), float(rotation_final[1]), float(rotation_final[2])]"""

x_max = 0; x_min = 0; y_max = 0; y_min = 0; z_max = 0; z_min = 0
for n in range(0, len(final)):
    for i in range(0, len(final[n])):
        for j in range(0, len(final[n][i]) - 1):
            for k in range(0, len(final[n][i][j])):
                for l in range(0, len(final[n][i][j][k])):
                    for m in range(0, no_atoms - no_ions):
                        if final[n][i][j][k][l][m][0] > x_max:
                            x_max = final[n][i][j][k][l][m][0]
                        if final[n][i][j][k][l][m][0] < x_min:
                            x_min = final[n][i][j][k][l][m][0]
                        if final[n][i][j][k][l][m][1] > y_max:
                            y_max = final[n][i][j][k][l][m][1]
                        if final[n][i][j][k][l][m][1] < y_min:
                            y_min = final[n][i][j][k][l][m][1]
                        if final[n][i][j][k][l][m][2] > z_max:
                            z_max = final[n][i][j][k][l][m][2]
                        if final[n][i][j][k][l][m][2] < z_min:
                            z_min = final[n][i][j][k][l][m][2]
translation_final = np.matrix([[1, 0, 0, -x_min - 10*dist_periodic/2.0], [0, 1, 0, -y_min - 10*dist_periodic/2.0], [0, 0, 1, -z_min - 10*dist_periodic/2.0], [0, 0, 0, 1]])
for n in range(0, len(final)):
    for i in range(0, len(final[n])):
        for j in range(0, len(final[n][i])):
            for k in range(0, len(final[n][i][j])):
                for l in range(0, len(final[n][i][j][k])):
                    for m in range(0, len(final[n][i][j][k][l])):
                        if len(final[n][i][j][k][l][m]) == 3:
                            final[n][i][j][k][l][m].append(1)
                        x = np.dot(translation_final, np.array(final[n][i][j][k][l][m]))
                        final[n][i][j][k][l][m] = [x[0, 0], x[0, 1], x[0, 2]]

sys_atoms = 0
for n in range(0, len(final)):
    for i in range(0, len(final[n])):
        for j in range(0, len(final[n][i])):
            for k in range(0, len(final[n][i][j])):
                for l in range(0, len(final[n][i][j][k])):
                    for m in range(0, len(final[n][i][j][k][l])):
                        sys_atoms += 1
print sys_atoms
count_monomer = 1
count_atom = 1
for n in range(0, len(final)):
    for i in range(0, len(final[n])):
        for j in range(0, len(final[n][i]) - 1):
            for k in range(0, len(final[n][i][j])):
                for l in range(0, len(final[n][i][j][k])):
                    for m in range(0, no_atoms - no_ions):
                        print'{:5d}{:5s}{:>5s}{:5d}{:8.3f}{:8.3f}{:8.3f}'.format(count_monomer, name, identity[m], count_atom, final[n][i][j][k][l][m][0]/10.0,
                                                                                 final[n][i][j][k][l][m][1]/10.0, final[n][i][j][k][l][m][2]/10.0)
                        count_atom += 1
                        if count_atom == 100000:
                            count_atom = 1
                    count_monomer += 1
for n in range(0, len(final)):
    for i in range(0, len(final[n])):
        for j in range(0, len(final[n][i][2])):
            for k in range(0, len(final[n][i][2][j])):
                for l in range(0, len(final[n][i][2][j][k])):
                    print'{:5d}{:5s}{:>5s}{:5d}{:8.3f}{:8.3f}{:8.3f}'.format(count_monomer, name_GLC, identity_gly[l], count_atom, final[n][i][2][j][k][l][0]/10.0,
                                                                             final[n][i][2][j][k][l][1]/10.0, final[n][i][2][j][k][l][2]/10.0)
                    count_atom += 1
                    if count_atom == 100000:
                        count_atom = 1
                count_monomer += 1
for n in range(0, len(final)):
    for i in range(0, len(final[n])):
        for j in range(0, len(final[n][i]) - 1):
            for k in range(0, len(final[n][i][j])):
                for l in range(0, len(final[n][i][j][k])):
                    for m in range(no_atoms - no_ions, no_atoms):
                        print'{:5d}{:5s}{:>5s}{:5d}{:8.3f}{:8.3f}{:8.3f}'.format(count_monomer, identity[m], identity[m], count_atom, final[n][i][j][k][l][m][0]/10.0,
                                                                                 final[n][i][j][k][l][m][1]/10.0, final[n][i][j][k][l][m][2]/10.0)
                        count_atom += 1
                        if count_atom == 100000:
                            count_atom = 1
                        count_monomer += 1
print '  ', (x_max - x_min)/10.0 - dist_periodic,'  ', (y_max - y_min)/10.0 - dist_periodic,'  ', (z_max - z_min)/10.0 - dist_periodic,'   0.00000   0.00000  -0.00000   0.00000  -0.00000  -0.00000'
