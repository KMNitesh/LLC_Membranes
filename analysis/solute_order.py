#!/usr/bin/env python

import argparse
import numpy as np
import mdtraj as md
from LLC_Membranes.llclib import topology


def initialize():

    parser = argparse.ArgumentParser(description='Measure the nematic order parameter based on the vectors extending'
                                                 'from a solute COM to the pore center and in the direction of the'
                                                 'of the solute as defined in the coordinate file.')

    parser.add_argument('-t', '--traj', default='PR.xtc', help='Name of system trajectory file (.trr or .xtc)')
    parser.add_argument('-g', '--gro', default='PR.gro', help='Name of structure file where water will be added')
    parser.add_argument('-b', '--build_monomer', default='NAcarb11V', help='Name of monomer used to build LLC membrane')
    parser.add_argument('-s', '--solute', default='ETH', help='Name of solute to be analysed')

    return parser


class System(object):

    def __init__(self, solute, gro, traj, build_monomer):

        print('Loading trajectory...', end='', flush=True)
        self.t = md.load(traj, top=gro)
        print('Done!')

        self.solute = topology.Solute(solute)
        self.nsolute = len([True for a in self.t.topology.atoms if a.residue.name == solute]) // self.solute.natoms
        self.solute_vectors = self.direction_vectors()

    def direction_vectors(self):

        v = np.zeros([self.t.n_frames, self.nsolute, 2])
        print(self.solute.name, self.solute.direction_vector[0])
        back_atom = [a.index for a in self.t.topology.atoms if a.residue.name == self.solute.name and
                      a.name in self.solute.direction_vector[0]]

        front_atom = [a.index for a in self.t.topology.atoms if a.residue.name == self.solute.name and
                      a.name in self.solute.direction_vector[1]]

        print(front_atom)
        print(back_atom)
        exit()
        # for t in range(self.t.n_frames):

        return v


if __name__ == "__main__":

    args = initialize().parse_args()

    sys = System(args.solute, args.gro, args.traj, args.build_monomer)