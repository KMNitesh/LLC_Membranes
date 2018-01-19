#!/usr/bin/env python

import argparse
import mdtraj as md
import numpy as np
import Atom_props
import tqdm
import matplotlib.pyplot as plt
from matplotlib import ticker
from llclib import physical
from place_solutes import trace_pores


def initialize():

    parser = argparse.ArgumentParser(description='Run Cylindricity script')

    parser.add_argument('-t', '--traj', default='traj_whole.xtc', type=str, help='Trajectory file. Make sure to '
                                                                            'preprocess with gmx trjconv -pbc whole')
    parser.add_argument('-g', '--gro', default='wiggle.gro', type=str, help='Name of coordinate file')
    parser.add_argument('-a', '--atoms', nargs='+', default=['C', 'C1', 'C2', 'C3', 'C4', 'C5'], help='Name of atoms to calculate'
                        'correlation function with respect to. The center of mass will be used')
    parser.add_argument('--itp', default='/home/bcoscia/PycharmProjects/GitHub/HII/top/Monomer_Tops/NAcarb11V.itp')
    parser.add_argument('-b', '--begin', default=0, type=int, help='Start frame')
    parser.add_argument('-bins', default=100, type=int, help='Number of bins in histogram')
    parser.add_argument('-m', '--monomers_per_layer', default=5, type=int, help='Number of monomers per layer')
    parser.add_argument('-ax', '--axis', default='xy', help='Slice to be visualized')
    parser.add_argument('--layers', default=20, type=int, help='Number of layers')
    parser.add_argument('--range', nargs='+', help='Range for histogram plot. A list of the form:'
                        '[dimension 1 lower, dimension 1 upper, dimension 2 lower, dimension 2 upper ...]')
    parser.add_argument('--save', type=str, help='Follow flag with filename to save plot by')

    args = parser.parse_args()

    return args


def com(pos, mass):
    """
    Calculate center of mass of groups of atoms. Assumes groups are sequentially numbered.
    :param pos: Positions of all atoms for all frames in mdtraj format
    :param mass: mass of each atom in the group whose center of mass will be calculated
    :return: trajectory of center of mass coordinates
    """

    n = len(mass)  # number of atoms
    nT = pos.shape[0]  # number of frames
    ncom = int(pos.shape[1]/n)  # number of centers of mass to calculate at each frame
    mres = np.sum(mass)

    centers = np.zeros([pos.shape[0], ncom, 3])  # will hold positions of all centers of masses

    for f in range(pos.shape[0]):  # loop through all trajectory frames
        for i in range(ncom):
            w = (pos[f, i*n:(i+1)*n, :].T * mass).T  # weight each atom in the residue by its mass
            centers[f, i, :] = np.sum(w, axis=0) / mres  # sum the coordinates and divide by the mass of the residue

    return centers


def duplicate_periodically(pts, box):
    """
    Duplicate points periodically in the +/- xyz directions. Assumes y box vector is angled with respect to x and
    the z vector points straight up
    :param pts: pts to be duplicated
    :param box: unitcell vectors in mdtraj format (use t.unitcell_vectors)
    :return: periodically extended system
    """

    nT = pts.shape[0]
    npts = pts.shape[1]
    p = np.zeros([nT, npts*27, 3])

    p[:, :npts, :] = pts

    for t in range(nT):

        p[t, npts:2*npts, :] = pts[t, :, :] + box[t, 2, :]
        p[t, 2*npts:3*npts, :] = pts[t, :, :] - box[t, 2, :]

        for i in range(3, 6):
            p[t, i*npts:(i+1)*npts, :] = p[t, (i-3)*npts:(i-2)*npts] + box[t, 0, :]

        for i in range(6, 9):
            p[t, i*npts:(i+1)*npts, :] = p[t, (i-6)*npts:(i-5)*npts] - box[t, 0, :]

        for i in range(9, 18):
            p[t, i*npts:(i+1)*npts, :] = p[t, (i-9)*npts:(i-8)*npts] + box[t, 1, :]

        for i in range(18, 27):
            p[t, i*npts:(i+1)*npts, :] = p[t, (i-18)*npts:(i-17)*npts] - box[t, 1, :]

    return p

if __name__ == "__main__":

    args = initialize()

    dimensions = []
    for i in args.axis:
        if i == 'x':
            dimensions.append(0)
        elif i == 'y':
            dimensions.append(1)
        elif i == 'z':
            dimensions.append(2)

    ndimensions = len(dimensions)

    t = md.load(args.traj, top=args.gro)[args.begin:]

    mass = [Atom_props.mass[i] for i in args.atoms]  # mass of reference atoms

    L = np.zeros([3])  # average box vectors in each dimension
    for i in range(3):
        L[i] = np.mean(np.linalg.norm(t.unitcell_vectors[:, i, :], axis=1))

    if args.range:
        hist_range = []
        for i in range(ndimensions):
            hist_range.append([])
            hist_range[i].append(float(args.range[i*2]))
            hist_range[i].append(float(args.range[i*2 + 1]))
    else:
        hist_range = [[-L[dimensions[0]], L[dimensions[0]]], [-L[dimensions[1]], L[dimensions[1]]]]

    keep = [a.index for a in t.topology.atoms if a.name in args.atoms]  # indices of atoms to keep

    pore_spline = np.zeros([t.n_frames, 4*args.layers, 3])

    for frame in range(t.n_frames):
        pore_spline[frame, :, :] += trace_pores(t.xyz[frame, keep, :], t.unitcell_vectors[frame, :2, :2], args.layers)

    pore_centers = physical.avg_pore_loc(4, t.xyz[:, [a.index for a in t.topology.atoms if a.name in args.atoms], :])  # can be further improved with a pore center spline

    ################### 1D Center of mass method ###################
    keep = [a.index for a in t.topology.atoms if a.name in args.atoms]  # indices of atoms to keep

    center_of_mass = com(t.xyz[:, keep, :], mass)  # calculate centers of mass of atom groups

    periodic_pts = duplicate_periodically(center_of_mass, t.unitcell_vectors)

    z = np.zeros([args.bins])

    for frame in tqdm.tqdm(range(t.n_frames)):
        for i in range(400):
            H, edges = np.histogram(periodic_pts[frame, i, 2] - periodic_pts[frame, :, 2], bins=args.bins, range=(0, 4))
            # H, edges = np.histogramdd(center_of_mass[i, :, :], bins=bins)
            z += H

    centers = [edges[i] + ((edges[i + 1] - edges[i])/2) for i in range(args.bins)]

    plt.plot(centers, z)
    plt.show()
    exit()
    ##################################################################

    ###################### 2D center of mass #########################
    ######## specialized for rings surrounding pore center ###########
    # keep = [a.index for a in t.topology.atoms if a.name in args.atoms]  # indices of atoms to keep
    #
    # center_of_mass = com(t.xyz[:, keep, :], mass)  # calculate centers of mass of atom groups
    #
    # periodic_pts = duplicate_periodically(center_of_mass, t.unitcell_vectors)
    #
    # z = np.zeros([args.bins, args.bins])
    #
    # for frame in tqdm.tqdm(range(t.n_frames)):
    #     for p in range(4*args.layers):
    #         # H, xedges, yedges = np.histogram2d(periodic_pts[frame, i, 0] - periodic_pts[frame, :, 0],
    #         #                         periodic_pts[frame, i, 1] - periodic_pts[frame, :, 1],
    #         #                         bins=args.bins, range=[[-L[0], L[0]], [-L[1], L[1]]])
    #         # H, xedges, yedges = np.histogram2d(pore_spline[frame, p, frame] - periodic_pts[frame, :, dimensions[0]],
    #         #         pore_centers[dimensions[1], p, frame] - periodic_pts[frame, :, dimensions[1]],
    #         #         bins=args.bins, range=[[-L[dimensions[0]], L[dimensions[0]]], [-L[dimensions[1]], L[dimensions[1]]]])
    #         H, xedges, yedges = np.histogram2d(pore_spline[frame, p, dimensions[0]] - periodic_pts[frame, :, dimensions[0]],
    #                 pore_spline[frame, p, dimensions[1]] - periodic_pts[frame, :, dimensions[1]],
    #                 bins=args.bins, range=hist_range)
    #         # H, edges = np.histogramdd(center_of_mass[i, :, :], bins=bins)
    #         z += H
    #
    # xcenters = [xedges[i] + ((xedges[i + 1] - xedges[i])/2) for i in range(args.bins)]
    # ycenters = [yedges[i] + ((yedges[i + 1] - yedges[i])/2) for i in range(args.bins)]
    #
    # Imax = np.amax(z)
    #
    # heatmap = plt.imshow(z.T/Imax, extent=[xcenters[0], xcenters[-1], ycenters[0], ycenters[-1]])
    # plt.imshow(z.T/729.0, extent=[xcenters[0], xcenters[-1], ycenters[0], ycenters[-1]])
    #
    # cbar = plt.colorbar(heatmap)
    # tick_locator = ticker.MaxNLocator(nbins=5)
    # cbar.locator = tick_locator
    # cbar.update_ticks()
    # cbar.ax.set_yticklabels(['0', '0.2', '0.4', '0.6', '0.8', '1'])
    # plt.xlabel('%s dimension (nm)' % args.axis[0])
    # plt.ylabel('%s dimension (nm)' % args.axis[1])
    #
    # # plt.plot(centers, z)
    # plt.tight_layout()
    # plt.savefig('%s' % args.save)
    # plt.show()
    # exit()
    #####################################################################

    ################### 1D Averaging Method ##########################
    # z = np.zeros([len(args.atoms), 1000])
    #
    # for j, atom in enumerate(args.atoms):
    #
    #     #keep = [a.index for a in t.topology.atoms if a.name in args.atoms]  # indices of atoms to keep
    #     keep = [a.index for a in t.topology.atoms if a.name == atom]  # indices of atoms to keep
    #
    #     # center_of_mass = com(t.xyz[:, keep, :], mass)  # calculate centers of mass of atom groups
    #
    #     periodic_pts = duplicate_periodically(t.xyz[:, keep, :], t.unitcell_vectors)
    #
    #     nbins = args.bins
    #     # bins = [nbins, int(nbins*np.sin(np.pi/3)), 20*nbins]
    #     # g = np.zeros(bins)
    #     # z = np.zeros([len(args.atoms), 1000])
    #
    #     # for t in tqdm.tqdm(range(t.n_frames)):
    #     #     for i in range(400):
    #     #         H, edges = np.histogramdd(periodic_pts[t, :, :] - periodic_pts[t, i, :], bins=bins)
    #     #         # H, edges = np.histogramdd(center_of_mass[i, :, :], bins=bins)
    #     #         g += H
    #     for frame in tqdm.tqdm(range(t.n_frames)):
    #         for i in range(400):
    #             H, edges = np.histogram(periodic_pts[frame, i, 2] - periodic_pts[frame, :400, 2], bins=1000, range=(0, 4))
    #             # H, edges = np.histogramdd(center_of_mass[i, :, :], bins=bins)
    #             z[j, :] += H
    #
    #     z[j, :] /= (400 * t.n_frames)
    #
    # z_avg = np.mean(z, axis=0)
    #
    # centers = [edges[i] + ((edges[i + 1] - edges[i])/2) for i in range(1000)]
    #
    # plt.plot(centers, z_avg)
    # plt.show()
    # exit()
    #####################################################################

    ############################## Animation ############################
    # g /= t.n_frames
    # # fig = plt.figure()
    #
    # from matplotlib import animation
    #
    # fig = plt.figure()
    # hmap = plt.imshow(g[:, 15, :])
    # plt.show()
    #
    # def update(i):
    #
    #     if bins[0] > i:
    #         hmap = plt.imshow(g[i, :, :].T)
    #     elif (bins[1] + bins[0]) > i >= bins[0]:
    #         hmap = plt.imshow(g[:, i - bins[0], :].T)
    #     else:
    #         hmap = plt.imshow(g[:, :, i - bins[0] - bins[1]].T)
    #
    #     return hmap,
    #
    # # call the animator.  blit=True means only re-draw the parts that have changed.
    # anim = animation.FuncAnimation(fig, update, frames=sum(bins), interval=50, blit=True)
    #
    # plt.show()








