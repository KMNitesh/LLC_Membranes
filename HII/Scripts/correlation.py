#!/usr/bin/env python

import argparse
import mdtraj as md
import numpy as np
import Atom_props
import tqdm
import matplotlib.pyplot as plt
from matplotlib import ticker
from llclib import fast_rotate
from place_solutes import trace_pores
from scipy.optimize import curve_fit
import detect_peaks
from scipy.interpolate import RegularGridInterpolator


def initialize():

    parser = argparse.ArgumentParser(description='Run Cylindricity script')

    parser.add_argument('-t', '--traj', default='traj_whole.xtc', type=str, help='Trajectory file. Make sure to '
                                                                            'preprocess with gmx trjconv -pbc whole')
    parser.add_argument('-g', '--gro', default='wiggle.gro', type=str, help='Name of coordinate file')
    parser.add_argument('-a', '--atoms', nargs='+', default=['C', 'C1', 'C2', 'C3', 'C4', 'C5'], help='Name of atoms to calculate'
                        'correlation function with respect to. The center of mass will be used')
    parser.add_argument('-r', '--res', help='Residue to create correlation function with respect to. Will use center of'
                                            'mass. Will override atoms. NOT IMPLEMENTED YET')
    parser.add_argument('--itp', default='/home/bcoscia/PycharmProjects/GitHub/HII/top/Monomer_Tops/NAcarb11V.itp')
    parser.add_argument('-b', '--begin', default=0, type=int, help='Start frame')
    parser.add_argument('-bins', nargs='+', default=100, type=int, help='Integer or array of bin values. If more than'
                        'one value is used, order the inputs according to the order given in args.axis')
    parser.add_argument('-m', '--monomers_per_layer', default=5, type=int, help='Number of monomers per layer')
    parser.add_argument('-s', '--slice', default='xy', help='Slice to be visualized')
    parser.add_argument('--layers', default=20, type=int, help='Number of layers')
    parser.add_argument('--range', nargs='+', help='Range for histogram plot. A list of the form:'
                        '[dimension 1 lower, dimension 1 upper, dimension 2 lower, dimension 2 upper ...]')
    parser.add_argument('--save', type=str, help='Follow flag with name to save plot by (Not including file extension)')
    parser.add_argument('--scale', type=float, default=1, help='Scale color bar by this factor')
    parser.add_argument('-br', '--block_radius', default=0.25, type=float, help='radius of circle around origin to zero out')
    parser.add_argument('--noshow', action="store_true", help='If this flag is entered, plots will not be shown')
    parser.add_argument('--load', action="store_true", help='load previously calculated correlation function')
    parser.add_argument('-pr', '--plot_range', nargs='+', help='range to plot. A list of the form: '
                        '[dimension 1 lower, dimension 1 upper, dimension 2 lower, dimension 2 upper ...]')
    parser.add_argument('-com', '--center_of_mass', action="store_true", help='Calculate based on center of mass of'
                                                                               'args.atoms')
    parser.add_argument('-offset', action="store_true", help='If system is in offset configuration, correlation length'
                                                             'will be calculated using every other peak')
    parser.add_argument('-aa', '--angle_average', action="store_true", help='Angle average the 3D correlation function'
                                                                            'about z-axis')
    parser.add_argument('-notraj', action="store_true", help='Calculate correlation function based on single frame.'
                                                             'Useful for test configurations..maybe')
    parser.add_argument('-invert', action="store_true", help='Invert correlation function at end to get structure'
                                                             'factor')

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


def sinusoidal_decay(x, a, b, c, d):
    """
    :param p: parameters: [period of oscillations, correlation time, amplitude, phase shift]
    :param x: x axis values
    :return: exponential function that sinusoidially decays to one
    """

    return 1 + c*np.sin(a*x + d)*np.exp(-x/b)


def exponential_decay(x, L):

    return 1 + np.exp(-x / L)


def angle_average(X, Y, Z, SF, ucell=None):

    ES = RegularGridInterpolator((X, Y, Z), SF, bounds_error=False)

    THETA_BINS_PER_INV_ANG = 20.
    MIN_THETA_BINS = 10  # minimum allowed bins
    RBINS = 100

    if ucell is not None:

        a1 = ucell[0]
        a2 = ucell[1]
        a3 = ucell[2]

        b1 = (np.cross(a2, a3)) / (np.dot(a1, np.cross(a2, a3)))
        b2 = (np.cross(a3, a1)) / (np.dot(a2, np.cross(a3, a1)))
        b3 = (np.cross(a1, a2)) / (np.dot(a3, np.cross(a1, a2)))

        b_inv = np.linalg.inv(np.vstack((b1, b2, b3)))

    ZBINS = Z.shape[0]  # 400

    XR = (X[-1] - X[0])
    YR = (Y[-1] - Y[0])

    Rmax = min(XR, YR) / 2.0
    Rmax *= 0.95

    rarr, rspace = np.linspace(0.0, Rmax, RBINS, retstep=True)
    zar = np.linspace(Z[0], Z[-1], ZBINS)

    oa = np.zeros((rarr.shape[0], zar.shape[0]))
    circ = 2.*np.pi*rarr  # circumference

    for ir in tqdm.tqdm(range(rarr.shape[0])):

        NTHETABINS = max(int(THETA_BINS_PER_INV_ANG*circ[ir]), MIN_THETA_BINS)  #calculate number of bins at this r
        thetas = np.linspace(0.0, np.pi*2.0, NTHETABINS, endpoint=False)  # generate theta array

        t, r, z = np.meshgrid(thetas, rarr[ir], zar)  # generate grid of cylindrical points

        xar = r*np.cos(t)  # set up x,y coords
        yar = r*np.sin(t)

        pts = np.vstack((xar.ravel(), yar.ravel(), z.ravel())).T  # reshape for interpolation

        if ucell is not None:
            # pts = mc_inv(pts, ucell)
            pts = np.matmul(pts, b_inv)

        oa[ir, :] = np.average(ES(pts).reshape(r.shape), axis=1)  # store average values in final array

    mn = np.nanmin(oa)
    oa = np.where(np.isnan(oa), mn, oa)

    rad_avg = np.average(oa)  # ???
    oa /= rad_avg  # normalize

    # set up data for contourf plot by making it symmetrical
    final = np.append(oa[::-1, :], oa[1:], axis=0)  # SF
    rfin = np.append(-rarr[::-1], rarr[1:])  # R
    zfin = np.append(z[:, 0, :], z[1:, 0, :], axis=0)  # Z

    return final, rfin, zfin


if __name__ == "__main__":

    args = initialize()

    npores = 4

    dimensions = []
    for i in args.slice:
        if i == 'x':
            dimensions.append(0)
        elif i == 'y':
            dimensions.append(1)
        elif i == 'z':
            dimensions.append(2)

    ndimensions = 3  # always do full 3d correlation function

    if not args.load:

        if type(args.bins) is list:
            if len(args.bins) > 1:
                bins = np.array(args.bins)
            else:
                bins = np.array([args.bins[0]]*ndimensions)
        else:
            bins = np.array([args.bins]*ndimensions)

        if args.notraj:
            t = md.load(args.gro)
            print('Configuration loaded')
        else:
            t = md.load(args.traj, top=args.gro)[args.begin:]
            print('Trajectory loaded')

        if args.atoms[0] == 'all':
            mass = [Atom_props.mass[a.name] for a in t.topology.atoms]
        else:
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
            hist_range = []
            for i in range(ndimensions):
                hist_range.append([-L[i]/2, L[i]/2])

        ###################### 3D center of mass #########################

        if args.atoms[0] == 'all':
            keep = [a.index for a in t.topology.atoms]
        else:
            keep = [a.index for a in t.topology.atoms if a.name in args.atoms]  # indices of atoms to keep
            # keep = [a.index for a in t.topology.atoms if a.residue.name == 'HOH' and a.name == 'O']  # indices of atoms to keep

        pore_spline = np.zeros([t.n_frames, npores*args.layers, 3])
        for frame in range(t.n_frames):
            pore_spline[frame, :, :] += trace_pores(t.xyz[frame, keep, :], t.unitcell_vectors[frame, :2, :2], args.layers)

        # natoms = len(args.atoms)
        # monomers_per_layer = int(len(keep) / args.layers / npores / len(args.atoms))  # divide by len(args.atoms) because of com
        monomers_per_layer = args.monomers_per_layer

        if args.center_of_mass:
            center_of_mass = com(t.xyz[:, keep, :], mass)  # calculate centers of mass of atom groups
        else:
            center_of_mass = t.xyz[:, keep, :]

        ncom = center_of_mass.shape[1]

        com_per_pore = int(center_of_mass.shape[1] / npores)

        periodic_pts = duplicate_periodically(center_of_mass, t.unitcell_vectors)

        correlation = np.zeros(bins)

        x = np.array([1, 0, 0])
        xnorm = np.linalg.norm(x)

    if args.load:

        if len(args.slice) == 2:
            corr = np.load('correlation_%s%s.npz' %(args.slice[0], args.slice[1]))
        else:
            corr = np.load('correlation_%s.npz' %(args.slice[0]))

        correlation = corr['correlation']
        edges = corr['edges']
        frames = corr['frames']
        ncom = corr['ncom']

    else:
        frames = t.n_frames

        if args.slice == 'xy' or args.slice == 'yx':
            for frame in tqdm.tqdm(range(frames), unit='Frame'):
                for p in range(npores):
                    for l in range(args.layers):
                        for a in range(monomers_per_layer):

                            pt = p*com_per_pore + l*monomers_per_layer + a  # index of center of mass reference point
                            point = periodic_pts[frame, pt, :]  # coordinates of center of mass reference point
                            v = pore_spline[frame, p*args.layers + l, :] - point  # vector from point to pore center
                            rot = fast_rotate.rotate_vector(periodic_pts[frame, :, :], v, x)  # rotate all points by angle
                            trans = rot - rot[pt, :]  # translate all point so reference point is at the origin
                            H, edges = np.histogramdd(trans, bins=bins, range=hist_range)
                            correlation += H
                            # middle_x = bins[0] // 2
                            # middle_y = bins[1] // 2
                            # plt.plot(correlation[middle_x, middle_y, :])
                            # plt.show()

        else:
            for frame in tqdm.tqdm(range(frames), unit='Frame'):
                for p in range(npores):
                    for l in range(args.layers):
                        for a in range(monomers_per_layer):
                            pt = p*com_per_pore + l*monomers_per_layer + a  # index of center of mass reference point
                            translated = periodic_pts[frame, :, :] - periodic_pts[frame, pt, :]  # make pt the origin
                            H, edges = np.histogramdd(translated, bins=bins, range=hist_range)
                            correlation += H
                            # middle_x = bins[0] // 2
                            # middle_y = bins[1] // 2
                            # #plt.plot(H[middle_x, middle_y, :])
                            # plt.plot(correlation[middle_x, middle_y, :])
                            # plt.show()

        if len(args.slice) > 1:
            np.savez_compressed('correlation_%s%s' % (args.slice[0], args.slice[1]), correlation=correlation, edges=edges, frames=frames, ncom=ncom)
        else:
            np.savez_compressed('correlation_%s' % (args.slice[0]), correlation=correlation, edges=edges, frames=frames, ncom=ncom)

    # Normalize 3D correlation function
    normalization = frames * ncom**2 / np.prod(correlation.shape)
    correlation /= normalization

    centers1 = [edges[dimensions[0]][i] + ((edges[dimensions[0]][i + 1] - edges[dimensions[0]][i])/2) for i in range(correlation.shape[dimensions[0]])]

    if len(dimensions) == 1:
        # only works for z slice currently
        centers_x = [edges[0][i] + ((edges[0][i + 1] - edges[0][i])/2) for i in range(correlation.shape[0])]
        centers_y = [edges[1][i] + ((edges[1][i + 1] - edges[1][i])/2) for i in range(correlation.shape[1])]
        middle_x = correlation.shape[0] // 2
        middle_y = correlation.shape[1] // 2
        r = 0.42
        avg = []
        for i, ix in enumerate(centers_x):
            for j, jy in enumerate(centers_y):
                if np.linalg.norm([ix, jy]) < r:
                    avg.append([i, j])

        zdf = np.zeros_like(centers1)
        for i in range(len(avg)):
            zdf += correlation[avg[i][0], avg[i][1], :]

        shift = 0
        while centers1[shift] < 0.2:
            shift += 1

        # plt.figure()
        # ft = np.abs(np.fft.fft(zdf[shift:] - np.mean(zdf[shift:])))**2
        # freq = np.fft.fftfreq(zdf[shift:].size, centers1[1] - centers1[0])
        # ndx = np.argsort(freq)
        # freq = freq[ndx]
        # ft = ft[ndx]
        # plt.plot(freq, ft)

        zdf /= np.mean(zdf)
        zdf = zdf[shift:]
        centers1 = np.array(centers1[shift:])

        peaks = detect_peaks.detect_peaks(zdf, mpd=12, show=False)  # adjust mpd if number of peaks comes out wrong

        if args.offset:
            peaks = peaks[1::2]  # every other peak starting at the second peak

        plt.figure()
        plt.plot(centers1, zdf, label='Raw data')
        plt.scatter(centers1[peaks], zdf[peaks], marker='+', c='r', s=200, label='Peak locations')

        # period = 0.438
        p = np.array([0.1])  # initial guess at parameters

        solp, cov_x = curve_fit(exponential_decay, centers1[peaks], zdf[peaks], p)

        # if args.plot_fit:
        #plt.plot(centers1[shift:], decay(np.array(centers1[shift:]), solp[0], solp[1], solp[2], solp[3]), '--', color='black', label='Least squares fit')
        plt.plot(centers1, exponential_decay(centers1, solp[0]), '--', c='black', label='Least squares fit')

        print('Correlation length = %1.2f +/- %1.2f angstroms' % (10*solp[0], 10*np.sqrt(cov_x[0, 0])))
        # print('Oscillation Period = %1.3f nm' % (10*(2*np.pi)/solp[0]))

        plt.xlabel('Z distance separation (nm)', fontsize=14)
        plt.ylabel('Count', fontsize=14)
        plt.axes().tick_params(labelsize=14)
        plt.tight_layout()
        plt.legend(loc=1, prop={'size': 16})
        plt.ylim(0, 1.2*np.amax(zdf))
        plt.tight_layout()
        # plt.savefig('zdf_overlay.png')
        plt.show()

        # plt.figure()
        # plt.plot(centers1[shift:], correlation[middle_x, middle_y, shift:]/np.mean(correlation[middle_x, middle_y, shift:]))
        # plt.ylabel('Normalized Count')
        # plt.xlabel('Distance (nm)')
        plt.show()

    if len(dimensions) > 1:

        if not args.angle_average:

            centers2 = [edges[1][i] + ((edges[dimensions[1]][i + 1] - edges[dimensions[1]][i])/2) for i in range(bins[1])]
            ax = sum(range(0, 3)) - sum(dimensions)  # see which axis is missing out of [0 1 2]. E.g. if we are looking at the
            # yz cross sections, then dimensions will equal [1 2]. We want to sum cross sections along the x-axis which is
            # also the 0 axis. So ax will equal 0
            twoD = np.mean(correlation, axis=ax)

            # remove center region of 2D histogram since it is brightest and contains no useful information
            # first find the center bins (index)

            for x in range(len(centers1)):
                for y in range(len(centers2)):
                    if np.linalg.norm([centers1[x], centers2[y]]) < args.block_radius:
                        twoD[x, y] = 0

            fig = plt.figure()
            ax1 = fig.add_subplot(111)

            if args.plot_range:

                extent = [float(i) for i in args.plot_range]
                dim_1_start = 0
                while centers1[dim_1_start] < extent[0]:
                    dim_1_start += 1
                dim_1_end = 0
                while centers1[dim_1_end] < extent[1]:
                    dim_1_end += 1
                dim_2_start = 0
                while centers1[dim_2_start] < extent[2]:
                    dim_2_start += 1
                dim_2_end = 0
                while centers1[dim_2_end] < extent[3]:
                    dim_2_end += 1

                twoD = twoD[dim_1_start:dim_1_end, dim_2_start:dim_2_end]
            else:
                extent = [centers1[0], centers1[-1], centers2[0], centers2[-1]]

            heatmap = ax1.imshow(twoD.T, extent=extent, cmap='jet', interpolation='gaussian')
            cbar = plt.colorbar(heatmap)
            cbar.ax.tick_params(labelsize=14)
            plt.xlabel('%s (nm)' % args.slice[0], fontsize=14)
            plt.ylabel('%s (nm)' % args.slice[1], fontsize=14)
            plt.gcf().get_axes()[0].tick_params(labelsize=14)
            ax = plt.axes()
            ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
            ax.xaxis.set_minor_locator(ticker.MultipleLocator(0.5))
            ax.yaxis.set_major_locator(ticker.MultipleLocator(1))
            ax.yaxis.set_minor_locator(ticker.MultipleLocator(0.5))
            plt.tight_layout()

            if args.save:
                plt.savefig('%s.png' % args.save)
            if not args.noshow:
                plt.show()

        else:

            x_centers = np.array([edges[0][i] + ((edges[0][i + 1] - edges[0][i])/2) for i in range(len(edges[0]) - 1)])
            y_centers = np.array([edges[1][i] + ((edges[1][i + 1] - edges[1][i])/2) for i in range(len(edges[1]) - 1)])
            z_centers = np.array([edges[2][i] + ((edges[2][i + 1] - edges[2][i])/2) for i in range(len(edges[2]) - 1)])

            # Fourier transform of 3d correlation function with angle averaging
            # fft = np.abs(np.fft.fftn(correlation))**2
            #
            # xbin = x_centers[1] - x_centers[0]
            # ybin = y_centers[1] - y_centers[0]
            # zbin = z_centers[1] - z_centers[0]
            #
            # freq_x = np.fft.fftfreq(x_centers.size - 1, d=xbin)
            # ndx = np.argsort(freq_x)
            # freq_x = freq_x[ndx]
            #
            # freq_y = np.fft.fftfreq(y_centers.size - 1, d=ybin)
            # ndy = np.argsort(freq_y)
            # freq_y = freq_y[ndy]
            #
            # freq_z = np.fft.fftfreq(z_centers.size - 1, d=zbin)
            # ndz = np.argsort(freq_z)
            # freq_z = freq_z[ndz]
            #
            # fft = fft[ndx, :, :]
            # fft = fft[:, ndy, :]
            # fft = fft[:, :, ndz]
            #
            # averaged, rfin, zfin = angle_average(freq_x, freq_y, freq_z, fft)
            #
            # # xlim = 0.4
            # # zlim = 0.4
            #
            # MAX = 0.001
            # MIN = 0
            #
            # NLEVELS = 200
            # lvls = np.linspace(MIN, MAX, NLEVELS)  # contour levels
            #
            # plt.figure()
            # cs = plt.contourf(rfin, zfin[0], averaged.T, levels=lvls, cmap='jet', extend='max')
            # plt.xlabel('$q_r$ ($\AA^{-1}$)')
            # plt.ylabel('$q_z$ ($\AA^{-1}$)')
            # # plt.gcf().get_axes()[0].set_ylim(-zlim, zlim)
            # # plt.gcf().get_axes()[0].set_xlim(-xlim, xlim)
            # plt.colorbar(format='%.1f')
            # plt.tight_layout()
            # plt.show()
            # exit()
            final, rfin, zfin = angle_average(x_centers, y_centers, z_centers, correlation)

            # convert to angstroms
            rfin *= 10
            zfin *= 10

            xlim = 15
            zlim = 15

            NLEVELS = 200

            lvls = np.linspace(np.amin(final), 0.35*np.amax(final), NLEVELS)  # contour levels

            plt.figure()
            cs = plt.contourf(rfin, zfin[0], final.T, levels=lvls, cmap='seismic', extend='max')
            plt.xlabel('$r$ ($\AA$)')
            plt.ylabel('$z$ ($\AA$)')
            plt.gcf().get_axes()[0].set_ylim(-zlim, zlim)
            plt.gcf().get_axes()[0].set_xlim(-xlim, xlim)
            plt.colorbar(format='%.1f')
            plt.tight_layout()
            plt.savefig('angle_averaged_correlation.png')

            if args.invert:

                # Fourier transform 2D angle averaged correlation function
                FT = np.abs(np.fft.fftn(final.T)) ** 2

                rbin = rfin[1] - rfin[0]
                freq_r = np.fft.fftfreq(rfin.size - 1, d=rbin)
                ndr = np.argsort(freq_r)
                freq_r = freq_r[ndr]

                zbin = zfin[0, 1] - zfin[0, 0]
                freq_z = np.fft.fftfreq(zfin[0].size - 1, d=zbin)
                ndz = np.argsort(freq_z)
                freq_z = freq_z[ndz]

                FT = FT[ndz, :]
                FT = FT[:, ndr]
                plt.figure()

                levels = np.linspace(0, 1000, 200)
                plt.contourf(freq_r, freq_z, FT, levels=levels, cmap='jet', extend='both')

            plt.show()

    ################### 1D Center of mass method ###################
    # keep = [a.index for a in t.topology.atoms if a.name in args.atoms]  # indices of atoms to keep
    #
    # center_of_mass = com(t.xyz[:, keep, :], mass)  # calculate centers of mass of atom groups
    #
    # periodic_pts = duplicate_periodically(center_of_mass, t.unitcell_vectors)
    #
    # z = np.zeros([args.bins])
    #
    # for frame in tqdm.tqdm(range(t.n_frames)):
    #     for i in range(400):
    #         H, edges = np.histogram(periodic_pts[frame, i, 2] - periodic_pts[frame, :, 2], bins=args.bins, range=(0, 4))
    #         # H, edges = np.histogramdd(center_of_mass[i, :, :], bins=bins)
    #         z += H
    #
    # centers = [edges[i] + ((edges[i + 1] - edges[i])/2) for i in range(args.bins)]
    #
    # plt.plot(centers, z)
    # plt.show()

    ##################################################################

    ###################### 2D center of mass #########################
    ######## specialized for rings surrounding pore center ###########
    # keep = [a.index for a in t.topology.atoms if a.name in args.atoms]  # indices of atoms to keep
    #
    # natoms = len(args.atoms)
    # monomers_per_layer = int(len(keep) / args.layers / npores / len(args.atoms))  # divide by len(args.atoms) because of com
    #
    # center_of_mass = com(t.xyz[:, keep, :], mass)  # calculate centers of mass of atom groups
    #
    # com_per_pore = int(center_of_mass.shape[1] / npores)
    #
    # periodic_pts = duplicate_periodically(center_of_mass, t.unitcell_vectors)
    #
    # z = np.zeros(bins)
    #
    # x = np.array([1, 0, 0])
    # xnorm = np.linalg.norm(x)
    #
    # if args.axis == 'xy' or args.axis == 'yx':
    #
    #     for frame in tqdm.tqdm(range(t.n_frames)):
    #         for p in range(npores):
    #             for l in range(args.layers):
    #                 for a in range(monomers_per_layer):
    #
    #                     pt = p*com_per_pore + l*monomers_per_layer + a  # index of center of mass reference point
    #                     point = periodic_pts[frame, pt, :]  # coordinates of center of mass reference point
    #                     v = pore_spline[frame, p*args.layers + l, :] - point  # vector from point to pore center
    #                     rot = transform.rotate_vector(periodic_pts[frame, :, :], v, x)  # rotate all points by angle
    #                     trans = rot - rot[pt, :]  # translate all point so reference point is at the center
    #                     H, xedges, yedges = np.histogram2d(trans[:, 0], trans[:, 1], bins=bins, range=hist_range)
    #                     z += H
    # else:
    #
    #     for frame in tqdm.tqdm(range(t.n_frames)):
    #         for p in range(npores):
    #             for l in range(args.layers):
    #                 for a in range(monomers_per_layer):
    #
    #                     pt = p*com_per_pore + l*monomers_per_layer + a  # index of center of mass reference point
    #                     translated = periodic_pts[frame, :, :] - periodic_pts[frame, pt, :]  # make pt the center
    #                     H, xedges, yedges = np.histogram2d(translated[:, dimensions[0]], translated[:, dimensions[1]],
    #                                                        bins=bins, range=hist_range)
    #
    #                     z += H
    #
    # z /= (t.n_frames*npores*args.layers*monomers_per_layer)  # normalize although this does nothing to the visualization
    # # z /= t.n_frames*npores
    #
    # xcenters = [xedges[i] + ((xedges[i + 1] - xedges[i])/2) for i in range(bins[0])]
    # ycenters = [yedges[i] + ((yedges[i + 1] - yedges[i])/2) for i in range(bins[1])]
    #
    # # remove center region of 2D histogram since it is brightest and contains no useful information
    # # first find the center bins (index)
    #
    # for x in range(len(xcenters)):
    #     for y in range(len(ycenters)):
    #         if np.linalg.norm([xcenters[x], ycenters[y]]) < args.block_radius:
    #             z[x, y] = 0
    #
    # print(np.mean(z))
    # # Imax = np.amax(z)
    #
    # # heatmap = plt.imshow(z.T/(args.scale*Imax), extent=[xcenters[0], xcenters[-1], ycenters[0], ycenters[-1]], cmap='jet')
    # # plt.imshow(z.T/Imax, extent=[xcenters[0], xcenters[-1], ycenters[0], ycenters[-1]], cmap='jet')
    #
    # heatmap = plt.imshow(z.T/np.mean(z), extent=[xcenters[0], xcenters[-1], ycenters[0], ycenters[-1]], cmap='jet')
    # plt.imshow(z.T/np.mean(z), extent=[xcenters[0], xcenters[-1], ycenters[0], ycenters[-1]], cmap='jet')
    #
    # cbar = plt.colorbar(heatmap)
    # tick_locator = ticker.MaxNLocator(nbins=5)
    # cbar.locator = tick_locator
    # cbar.update_ticks()
    # # cbar.ax.set_yticklabels(['0', '0.2', '0.4', '0.6', '0.8', '1'])
    # plt.xlabel('%s dimension (nm)' % args.axis[0])
    # plt.ylabel('%s dimension (nm)' % args.axis[1])
    #
    # # plt.plot(centers, z)
    # plt.tight_layout()
    # if args.save:
    #     plt.savefig('%s.png' % args.save)
    # if not args.noshow:
    #     plt.show()
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








