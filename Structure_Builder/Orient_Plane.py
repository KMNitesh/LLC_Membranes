# Orient plane with origin
import numpy as np
import math

f = open("Monomer_Configurations/monomer10.pdb", "r")
a = []
for line in f:
    a.append(line)

no_monomers = 6  # number of monomers packed per layer around a pore
no_atoms = 138  # number of atoms in one monomer excluding sodium ion
pore_radius = 4  # Radius of pore (unsure of units right now)
no_pores = 4  # number of pores to be simulated
dist_bw = 40  # distance between pores (units tbd)
no_layers = 20  # Number of layers in a pore
dist = 10 # distance between layers (units tbd)
lines_of_text = 4  # lines of text at top of .pdb file


x_values_inp = []  # list to hold input values of x stored from .pdb file
y_values_inp = []  # list to hold input values of y stored from .pdb file
z_values_inp = []  # list to hold input values of z stored from .pdb file
positions_inp = []  # holds x, y, z coordinates of input .pdb file
identity = []  # holds the names of atom in the order that they appear in the .pdb file
# read specific entries in a text file
for i in range(lines_of_text, lines_of_text + no_atoms):  # searches relevant lines of text in file, f, being read
    # There are 137 atoms excluding sodium
    x_values_inp.append(float(a[i][26:38]))  # Use this to read specific entries in a text file
    y_values_inp.append(float(a[i][38:46]))  # makes sure I backtrack far enough to get all digits(i.e.38 instead of 42)
    z_values_inp.append(float(a[i][46:54]))
    positions_inp.append([x_values_inp[i - lines_of_text], y_values_inp[i - lines_of_text], z_values_inp[i - lines_of_text]])
    identity.append(a[i][13:16])  # hold name of atom (C, H or O)

# Now rotate plane to align with xy plane

# Arrays to hold x,y,z values of each point of interest
# [pt1, pt2, pt3]
plane_x = np.zeros((3, 1))
plane_y = np.zeros((3, 1))
plane_z = np.zeros((3, 1))
# This loop only works because of the way the atoms are spaced in the coordinate file. I am looking at atoms C, C2 and
# C4. Theoretically this will work with any three atoms but I am trying to align the plane of benzene
for i in range(0, 3):
    plane_x[i] = float(a[lines_of_text + 2*i][26:38])
    plane_y[i] = float(a[lines_of_text + 2*i][38:46])
    plane_z[i] = float(a[lines_of_text + 2*i][46:54])

# vector pointing from point 1 to point 2
v12 = [float(plane_x[1]-plane_x[0]), float(plane_y[1]-plane_y[0]), float(plane_z[1]-plane_z[0])]
v13 = [float(plane_x[2]-plane_x[0]), float(plane_y[2]-plane_y[0]), float(plane_z[2]-plane_z[0])]  # same idea as above

# The cross product of v12 and v13 give a vector that is perpendicular to the plane:
N = np.cross(v12, v13)

N_desired = [0, 0, 1]  # We want the normal vector to be perpendicular to a horizontal plane at the origin

RotationAxis = np.cross(N, N_desired)
theta = math.acos(np.dot(N, N_desired)/(np.linalg.norm(N)*np.linalg.norm(N_desired)))  #  Rotation Angle (radians)

L = [RotationAxis[0]/np.linalg.norm(RotationAxis), RotationAxis[1]/np.linalg.norm(RotationAxis),
                   RotationAxis[2]/np.linalg.norm(RotationAxis)]  # normalized Rotation Axis
# to avoid mistakes: L = [u, v, w]

u = L[0]
v = L[1]
w = L[2]

# Rotation Matrix to rotate a plane:
R = np.zeros((4, 4))
R[3, 3] = 1
R[0, 0] = u**2 + (v**2 + w**2)*math.cos(theta)  # math.cos takes theta in radians by default
R[0, 1] = u*v*(1 - math.cos(theta)) - w*math.sin(theta)
R[0, 2] = u*w*(1 - math.cos(theta)) + v*math.sin(theta)
R[1, 0] = u*v*(1 - math.cos(theta)) + w*math.sin(theta)
R[1, 1] = v**2 + (u**2 + w**2)*math.cos(theta)
R[1, 2] = v*w*(1 - math.cos(theta)) - u*math.sin(theta)
R[2, 0] = u*w*(1 - math.cos(theta)) - v*math.sin(theta)  # math.cos takes theta in radians by default
R[2, 1] = w*v*(1 - math.cos(theta)) + u*math.sin(theta)
R[2, 2] = w**2 + (u**2 + v**2)*math.cos(theta)

for i in range(0, len(positions_inp)):
    positions_inp[i].append(1)
    x = np.dot(R, np.array(positions_inp[i]))
    positions_inp[i] = [x[0], x[1], x[2]]

# Now translate the structure to the origin
# matrix to translate molecule to origin based on the position of atom 10 (Carbonyl carbon coming off benzene)
translation = np.matrix([[1, 0, 0,-(positions_inp[9][0])], [0, 1, 0,-(positions_inp[9][1])],\
                         [0, 0, 1, -(positions_inp[9][2])], [0, 0, 0, 1]])
for i in range(0, len(positions_inp)):
    positions_inp[i].append(1)
    x = np.dot(translation, np.array(positions_inp[i]))
    positions_inp[i] = [x[0, 0], x[0, 1], x[0, 2]]


# Now rotate the xy coordinates so that the molecule is pointing towards the origin

pt1 = [positions_inp[0][0], positions_inp[0][1]]  # location of C
pt2 = [positions_inp[3][0], positions_inp[3][1]]  # location of C3
pt3 = [positions_inp[9][0], positions_inp[9][1]]  # location of carbonyl carbon
origin = [0, 0]

# find slope between two points
def slope(pt1, pt2):
    m = (pt1[1] - pt2[1])/(pt1[0] - pt2[0])  # slope
    return m

m1 = slope(pt1, pt2)
m2 = 0  # slope of line y = 0

# find angle between lines

theta = -math.atan((m1 - m2)/(1 + m1*m2))

# Find out which quadrant of the xy plane the monomer is sitting in

#   II    |    I
#         |
#   -------------
#         |
#   III   |    IV

def quadrant(pt):  # looks at [x,y] values and determines which quadrant the point is in
    if pt[0] > 0 and pt[1] > 0:
        return 1
    elif pt[0] < 0 and pt[1] < 0:
        return 3
    elif pt[1] < 0 < pt[0] :
        return 4
    elif pt[0] < 0 < pt[1] :
        return 2
    else:
        return 0  # the case where the point lies on the x or y axis

# C and C3 are assumed to be on a line so they should lie in the same quadrant
# Translation matrix
# figure out in which direction the coordinates will be shifted. They are always shift away from the origin
if quadrant(pt1) == 1:  # e.g. in quadrant 1, the x's are shifted in the positive x and positive y directions
    vx = 1
    vy = 1
elif quadrant(pt1) == 2:  # in quadrant 2, the x's are shifted negative and the y's are shifted positive
    vx = -1
    vy = 1
elif quadrant(pt1) == 3:  # in quadrant 3, the x's and y's are shifted down
    vx = -1
    vy = -1
elif quadrant(pt1) == 4:  # in quadrant 4, the x's are shifted positive and the y's are shifted negative
    vx = 1
    vy = -1
# These next three conditionals are very unlikely but are included for completeness and to avoid future errors
elif quadrant(pt1) == 0 and pt1[0] == 0:  # i.e., it lies on the y - axis
    if pt1[1] > 0:  # the point is on the positive y-axis
        vx = 0  # no x-shift
        vy = 1  # shift in the positive y direction
    if pt1[1] < 0:  # the point is on the negative y-axis
        vx = 0  # no x-shift
        vy = -1  # shift in the negative y direction
elif quadrant(pt1) == 0 and pt1[1] == 0:  # i.e., it lies on the x - axis
    if pt1[0] > 0:  # the point is on the positive x-axis
        vx = 1  # shift in the positive x direction
        vy = 0  # no y-shift
    if pt1[0] < 0:  # the point is on the negative y-axis
        vx = -1  # shift in the negative x direction
        vy = 0  # no y-shift

translation = np.matrix([[1, 0, 0, vx*pore_radius*math.cos(theta)], [0, 1, 0, vy*pore_radius*math.sin(theta)],\
                         [0, 0, 1, 0], [0, 0, 0, 1]])

# print translation
# Apply matrix to all points
for i in range(0, len(positions_inp)):
    positions_inp[i].append(1)
    x = np.dot(translation, np.array(positions_inp[i]))
    positions_inp[i] = [x[0, 0], x[0, 1], x[0, 2]]


positions1 = []  # will hold the x,y,z coordinates of each atom of monomer 1
positions2 = []  # will hold the x,y,z coordinates of each atom of monomer 2
positions3 = []  # will hold the x,y,z coordinates of each atom of monomer 3
positions4 = []  # will hold the x,y,z coordinates of each atom of monomer 4
positions5 = []  # will hold the x,y,z coordinates of each atom of monomer 5
positions6 = []  # will hold the x,y,z coordinates of each atom of monomer 6
positions7 = []  # here for the case where 7 monomers pack
positions = [positions1, positions2, positions3, positions4, positions5, positions6, positions7]  # list of lists
x_values = []  # will hold x_values in the order that they appear in the positions matrix
y_values = []  # will hold y_values in the order that they appear in the positions matrix
z_values = []  # will hold z_values in the order that they appear in the positions matrix

# rotate coordinates and store each rotated coordinate as a separate list:

for k in range(0, len(positions_inp)):
    x = np.array(positions_inp[k])
    for i in range(1, no_monomers + 1):
        theta = i * math.pi / (no_monomers / 2.0)  # angle to rotate about axis determined from no of monomers per layer
        # Creates a rotation matrix to rotate input vector about y-axis making a new coordinate at evenly spaced points.
        # Each rotation belongs to a different monomer's position.The no of points corresponds to the number of monomers
        Rx = np.zeros((3, 3))  # makes a 3 x 3 zero matrix
        Rx[0, 0] = math.cos(theta)  # This line and subsequent edits to Rx fills in entries needed for rotation matrix
        Rx[1, 0] = math.sin(theta)
        Rx[0, 1] = -math.sin(theta)
        Rx[1, 1] = math.cos(theta)
        Rx[2, 2] = 1
        rot = np.dot(Rx, x)  # multiplies atomic coordinates by the rotation vector to generate new coordinates
        rot = [float(rot[0]), float(rot[1]), float(rot[2])]  # converts matrix to a list of floats
        positions[i - 1].append(rot)  # appends the atomic coordinates to 'positions'

for l in range(0, no_pores):  # loop to create multiple pores
    theta = 30  # angle which will be used to do hexagonal packing
    if l == 0:  # unmodified coordinates
        b = 0
        c = 0
    elif l == 1:  # move a pore directly down
        b = - 1
        c = 0
    elif l == 2:  # moves pore up and to the right
        b = math.cos(math.radians(90 - theta))
        c = -math.sin(math.radians(90 - theta))
    elif l == 3:  # moves a pore down and to the right
        b = -math.sin(math.radians(theta))
        c = -math.cos(math.radians(theta))
    for k in range(0, no_layers):
        for j in range(0, no_monomers):  # iterates over each monomer to create coordinates
            for i in range(0, len(positions[j]) - 1):  #
                x_values.append(b*dist_bw + positions[j][i][0])
                y_values.append(c*dist_bw + positions[j][i][1])
                z_values.append(k*dist + positions[j][i][2])
                print '{:5s}{:6d}  {:4s} {:8d}   {:8.3f} {:8.3f}{:8.3f}  {:4.2f}  {:4.2f}          {:>2}{:2s}'\
                    .format('ATOM', i + 1 + (no_atoms - 1)*j + (no_atoms - 1)*no_monomers*k + (no_atoms - 1)*no_monomers*no_layers*l,
                    identity[i], 0, x_values[i+(no_atoms - 1)*j+(no_atoms - 1)*no_monomers*k+(no_atoms - 1)*no_monomers*no_layers*l],
                    y_values[i + (no_atoms - 1)*j + (no_atoms - 1)*no_monomers*k + (no_atoms - 1)*no_monomers*no_layers*l],
                    z_values[i + (no_atoms - 1)*j + (no_atoms - 1)*no_monomers*k + (no_atoms - 1)*no_monomers*no_layers*l], 0.00,
                    0.00, 'C', '+0')

# Next, we need to extract connectivity information from the .pdb file
# this was a pain so appreciate it!

for l in range(0, no_pores):  # loop to create multiple pores
    theta = 30  # angle which will be used to do hexagonal packing
    if l == 0:  # unmodified coordinates
        b = 0
        c = 0
    elif l == 1:  # move a pore directly down
        b = - 1
        c = 0
    elif l == 2:  # moves pore up and to the right
        b = math.cos(math.radians(90 - theta))
        c = -math.sin(math.radians(90 - theta))
    elif l == 3:  # moves a pore down and to the right
        b = -math.sin(math.radians(theta))
        c = -math.cos(math.radians(theta))
    for k in range(0, no_layers):
        for j in range(0, no_monomers):  # iterates over each monomer to create coordinates
            x_values.append(b*dist_bw + positions[j][no_atoms - 1][0])
            y_values.append(c*dist_bw + positions[j][no_atoms - 1][1])
            z_values.append(k*dist + positions[j][no_atoms -1][2])
            print '{:5s}{:6d}  {:4s} {:8d}   {:8.3f} {:8.3f}{:8.3f}  {:4.2f}  {:4.2f}          {:>2}{:2s}'\
                .format('ATOM', 1 + (no_atoms - 1)*no_layers*no_pores*no_monomers + j + k*no_monomers + l*no_layers*no_monomers,
                identity[no_atoms - 1], 0, x_values[(no_atoms - 1)*no_layers*no_pores*no_monomers + j + k*no_monomers + l*no_layers*no_monomers],
                y_values[(no_atoms - 1)*no_layers*no_pores*no_monomers + j + k*no_monomers + l*no_layers*no_monomers],
                z_values[(no_atoms - 1)*no_layers*no_pores*no_monomers + j + k*no_monomers + l*no_layers*no_monomers], 0.00,
                0.00, 'C', '+0')
