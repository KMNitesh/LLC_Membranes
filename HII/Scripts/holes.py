#!/usr/bin/env python

import numpy as np
from llclib import file_rw
import subprocess
import mdtraj as md
import argparse
import math
import matplotlib.pyplot as plt
import scipy.stats
from scipy import spatial
import tqdm


def initialize():

    parser = argparse.ArgumentParser(description='Apply flat-bottomed position restraints based on a reference position')

    parser.add_argument('-xy', '--xy', default=8, type=float, help='box vector length in x and y direction')
    parser.add_argument('-z', '--z', default=8, type=float, help='box vector in z direction')
    parser.add_argument('-r', '--radius', default=0.5, type=float, help='radius of pores')
    parser.add_argument('-rows', default=2, type=int, help='Number of rows of pores. This will also be number of columns')
    parser.add_argument('-n', '--npoints', default=10000, type=int, help='number of atoms to try put in the system')
    parser.add_argument('-f', '--nframes', default=100, type=int, help='number of frames')
    parser.add_argument('--gaussian', action="store_true", help='Allow points in the pore with a gaussian probability')
    parser.add_argument('--pores', action="store_true", help='build a system with pores')
    parser.add_argument('--layers', action="store_true", help='build a system with layers')
    parser.add_argument('--uniform', action="store_true", help='build a system with a uniform distribution of points')
    parser.add_argument('-lw', '--layer_width', default=0.1, type=float, help='width of layers')
    parser.add_argument('-dbwl', default=0.37, type=float, help='Distance between layers (nm)')
    parser.add_argument('--disks', action="store_true", help='Create a system with stacked disks')
    parser.add_argument('-m', '--min_dist', default=0.1, type=float, help='Minimum distance points must be from each other (nm)')

    args = parser.parse_args()

    return args


def position_restraints(file, atoms, axis, fconst):
    """
    Restrain the selected atoms in desired directions
    :param file: a list where each entry is a line from a coordinate file (.gro)
    :param atoms: indices of the atoms to position restrain
    :param axis: which direction to restrain
    :return: an array of position restraints formatted for easy writing into the topology (.itp)
    """

    # define force constants in their respective directions
    fcx = 0
    fcy = 0
    fcz = 0
    if 'x' in axis:
        fcx = fconst  # a large enough restraint to cause a large movement penalty
    if 'y' in axis:
        fcy = fconst
    if 'z' in axis:
        fcz = fconst

    atom_numbers = []  # find the numbers of the atoms which we are restraining
    with open(file, 'r') as f:
        for line in f:
            if str.strip(line[10:15]) in atoms:
                atom_numbers.append(int(line[15:20]))

    restraints = np.zeros([5, len(atom_numbers)])  # organize them into a list which can be translated to a topology
    for i in range(len(atom_numbers)):
        restraints[:, i] = [atom_numbers[i], 1, fcx, fcy, fcz]  # See: http://www.gromacs.org/Documentation/How-tos/Position_Restraints

    return restraints


def translate(pt, translation):
    """
    :param pt: 3D coordinates of points to translate
    :param translation: How far to translate the point in each direction
    :return: translated point
    """
    translation = np.array(translation)
    t = np.append(translation, [1])
    T = np.zeros([4, 4])
    for i in range(4):
        T[i, i] = 1

    T[:3, 3] = pt

    return np.dot(T, t.T)[:3]


def Rz(pt, theta):
    """
    :param pt: 3D coordinates of point to be rotated
    :param theta: angle to rotate with respect z axis
    :return: rotated point
    """

    R = np.zeros([3, 3])
    R[2, 2] = 1
    R[0, 0] = math.cos(theta)
    R[0, 1] = -math.sin(theta)
    R[1, 0] = math.sin(theta)
    R[1, 1] = math.cos(theta)

    return np.dot(R, pt)


def nn(pt, all_pts):

    if all_pts.shape[0] > 0:
        neighbor = spatial.KDTree(all_pts).query(pt)[1]
        ld = np.linalg.norm(pt - all_pts[neighbor, :])

        if ld >= min_dist:
            return True
        else:
            return False
    else:
        return True


def check_pores(pt, pores, r, all_pts):
    """
    :param pt: point which we are checking
    :param pores: coordinates of pore locations
    :param r: radius of pores
    :param all_pts: coordinates of all points placed so far in this frame
    :return: True/False - whether pt is contained in one of the pore regions
    """

    contained = False
    npores = pores.shape[0]
    global rs
    for i in range(npores):
        radius = np.linalg.norm(pores[i] - pt[:2])
        if radius <= r:
            if args.gaussian:
               # allow points inside the pores based on a gaussian probability
               # The full cdf sums to 1. We are using half the pdf so the max the cdf will get is 0.5. So multiply by 2
                probability = 2*scipy.stats.norm(r, r/2).cdf(radius)
                if np.random.rand() >= probability:  # generate random number between 0 and 1 as a test
                    contained = True  # Will only be excluded if it meets the condition
                else:
                    rs.append(radius)
            else:
                contained = True
            break

        elif not nn(pt, all_pts):
            contained = True

    return contained


def check_layers(pt, layers, width):
    """
    :param pt: point which we are checking
    :param pores: coordinates of pore locations
    :param r: radius of pores
    :return: True/False - whether pt is contained in one of the pore regions
    """

    contained = False
    nlayers = layers.shape[0]
    r = 0.5*width

    for i in range(nlayers):
        radius = abs(pt[2] - layers[i])
        if radius <= r:
            if args.gaussian:
                # allow points inside the pores based on a gaussian probability
                # The full cdf sums to 1. We are using half the pdf so the max the cdf will get is 0.5. So multiply by 2
                probability = 2*scipy.stats.norm(r, r/2).cdf(radius)
                if np.random.rand() >= probability:  # generate random number between 0 and 1 as a test
                    contained = True  # Will only be excluded if it meets the condition
            else:
                contained = True
            break

    return contained


def check_disks(pt, disk_locations, layer_width, disk_radius):
    """
    :param pt: point which we are checking
    :param pores: coordinates of pore locations
    :param r: radius of pores
    :return: True/False - whether pt is contained in one of the pore regions
    """

    contained = False
    ndisks = disk_locations.shape[0]

    for i in range(ndisks):
        radius = np.linalg.norm(disk_locations[i, :2] - pt[:2])
        width = abs(disk_locations[i, 2] - pt[2])
        if radius <= disk_radius and width <= 0.5*layer_width:
            if args.gaussian:
                # allow points inside the pores based on a gaussian probability
                # The full cdf sums to 1. We are using half the pdf so the max the cdf will get is 0.5. So multiply by 2
                probability = 2*scipy.stats.norm(r, r/2).cdf(radius)
                if np.random.rand() >= probability:  # generate random number between 0 and 1 as a test
                    contained = True  # Will only be excluded if it meets the condition
            else:
                contained = True
            break

    return contained


if __name__ == "__main__":

    args = initialize()
    # box dimensions
    x = args.xy  # nm
    y = args.xy
    z = args.z

    min_dist = args.min_dist
    pore_radius = args.radius
    angle = np.pi / 3
    npts = args.npoints
    rows = args.rows
    npores = rows**2
    frames = args.nframes

    if args.layers or args.disks:
        nlayers = z / args.dbwl
        z = nlayers * args.dbwl
        layer_locations = np.linspace(0, z, nlayers)

    corners = np.zeros([8, 3])

    corners[0, :] = [0, 0, 0]
    corners[1, :] = [y*np.cos(angle), y*np.sin(angle), 0]
    corners[2, :] = [y*np.cos(angle) + x, y*np.sin(angle), 0]
    corners[3, :] = [y, 0, 0]
    for i in range(4, 8):
        corners[i, :] = corners[i - 4, :] + [0, 0, z]

    A = corners[0, :]
    AB = corners[1, :] - corners[0, :]  # v2 (referring to gromacs box formatting)
    AD = corners[3, :] - corners[0, :]  # v1
    AE = corners[4, :] - corners[0, :]  # v3
    # A = np.array([0, 0, 0])
    # AB = np.array([x, 0, 0])
    # AD = np.array([0, y, 0])
    # AE = np.array([0, 0, z])

    pore_locations = np.zeros([npores, 2])
    p2p = x / rows

    for i in range(rows):
        for j in range(rows):
            pore_locations[i*rows + j, :] = [p2p*(0.5 + j) + p2p*(0.5 + i)*math.cos(angle), p2p/2*math.sin(angle) + i*p2p*math.sin(angle)]

    if args.disks:
        disks_per_layer = 6
        nlayers = int(z / args.dbwl)
        pore_radius = args.radius
        disk_radius = 0.1
        disk_locations = np.zeros([npores*nlayers*disks_per_layer, 3])
        for i in range(npores):
            for j in range(nlayers):
                for k in range(disks_per_layer):
                    theta = 2*np.pi*k / disks_per_layer  # angle by which to rotate about pore axis
                    pt = np.array([pore_radius, 0, 0])
                    pt = Rz(pt, theta)
                    pore = np.append(pore_locations[i, :], layer_locations[j])
                    disk_locations[i*nlayers*disks_per_layer + j*disks_per_layer + k, :] = translate(pt, pore)

    points = np.zeros([frames, npts, 3])
    rs = []
    # generate random points inside box
    for t in tqdm.tqdm(range(frames)):
        for i in tqdm.tqdm(range(npts)):
            u = np.random.rand()
            b = np.random.rand()
            h = np.random.rand()
            pt = A + u*AB + b*AD + h*AE  # places point inside 3D box defined by box vector AB, AD and AE
            if args.pores:
                while check_pores(pt, pore_locations, pore_radius, points[t, :i, :]):  # force all points outside the pore region
                    u = np.random.rand()
                    b = np.random.rand()
                    h = np.random.rand()
                    pt = A + u * AB + b * AD + h * AE
            if args.layers:  # force all points outside layer region
                while check_layers(pt, layer_locations, args.layer_width):
                    u = np.random.rand()
                    b = np.random.rand()
                    h = np.random.rand()
                    pt = A + u * AB + b * AD + h * AE
            if args.disks:
                while check_disks(pt, disk_locations, args.layer_width, disk_radius):
                    u = np.random.rand()
                    b = np.random.rand()
                    h = np.random.rand()
                    pt = A + u * AB + b * AD + h * AE

            points[t, i, :] = np.round(pt, 1)

    d = []
    tree = spatial.KDTree(points[0, :, :])
    for i in range(npts):
        pt = tree.query(points[0, i, :], k=2)[1][1]
        d.append(np.linalg.norm(points[0, pt, :] - points[0, i, :]))

    print sorted(d)[:10]
    print sorted(d)[-10:]
    # plt.hist(rs)
    # plt.show()

    box = [AD[0], AB[1], AE[2], AD[1], AD[2], AB[0], AB[2], AE[0], AE[1]]  # how its written in a .gro file

    unitcell_vectors = np.zeros([frames, 3, 3])
    for i in range(frames):
        # vectors don't change but need them as a trajectory
        unitcell_vectors[i, 0, :] = [AD[0], AD[1], AD[2]]
        unitcell_vectors[i, 1, :] = [AB[0], AB[1], AB[2]]
        unitcell_vectors[i, 2, :] = [AE[0], AE[1], AE[2]]

    file_rw.write_gro_pos(points[-1, :, :], 'holes.gro', box=box)
    traj = md.formats.TRRTrajectoryFile('holes.trr', mode='w', force_overwrite=True)
    time = np.linspace(0, 1000, frames)
    topology = md.load('holes.gro').topology  # needed to write in gro format..not used here
    traj.write(points, time=time, box=unitcell_vectors)

    exit()
    pore_locations[0, :] = [x*.25, y*.25, 0]
    pore_locations[1, :] = [x*.75, y*.25, 0]
    pore_locations[2, :] = [x*.25, y*.75, 0]
    pore_locations[3, :] = [x*.75, y*.75, 0]

    n_ions = 10000  # ions to place in each pore
    positions = np.zeros([4*n_ions, 3])

    for i in range(4):
        for j in range(n_ions):
            zpos = np.random.rand()*z
            t = 2*np.pi*np.random.rand()
            u = np.random.rand()*pore_radius + np.random.rand()*pore_radius
            if u > pore_radius:
                r = 2*pore_radius - u
            else:
                r = u
            xpos = r*np.cos(t)
            ypos = r*np.sin(t)
            positions[i*n_ions + j, :] = [xpos, ypos, zpos] + pore_locations[i, :]

    file_rw.write_gro_pos(positions, 'holes.gro', box=[x, y, z])

    # dt = 0.0000001
    # p1 = subprocess.Poepn(["input.py", "-d", "%s" % dt, "-l", "%s" % (dt * 50), "--solvate", "-f", "50"])
    p = subprocess.Popen(["gmx", "solvate", "-cp", "holes.gro", "-cs", "spc216.gro", "-o", "solv.gro"])
    p.wait()

    t = md.load('solv.gro')
    keep = [a.index for a in t.topology.atoms if a.name != 'NA']
    water = t.atom_slice(keep)

    file_rw.write_gro(water, 'holes.gro')

    # apply restraints to the water

    # restraints = position_restraints('holes.gro', ['OW'], 'xy', 1000)
    #
    # with open('restraints.itp', 'w') as f:
    #     f.write("[ position_restraints ]\n")
    #     for i in range(restraints.shape[1]):
    #         f.write('{:6d}{:6d}{:1s}{:9f}{:1s}{:9f}{:1s}{:9f}\n'.format(int(restraints[0, i]), int(restraints[1, i]),'',
    #                                                         restraints[2, i], '', restraints[3, i], '', restraints[4, i]))