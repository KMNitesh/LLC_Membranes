#!/usr/bin/env python

import numpy as np
import scipy.io as io
import matplotlib.pyplot as plt
from scipy.stats import norm
import argparse


def initialize():

    parser = argparse.ArgumentParser(description='Generate timeseries with different underlying models')

    parser.add_argument('-t', '--type', default='AR', type=str, help="Underlying dynamical model. 'Gaussian' and 'AR'"
                                                                     "(autoregressive) are implemented.")
    parser.add_argument('-d', '--ndraws', default=2000, type=str, help='Number of time steps to take')
    parser.add_argument('-n', '--ntraj', default=4, type=str, help='Number of trajetories to generate')

    # Define transition matrix. Either provide your own, or let this script generate one
    parser.add_argument('-T', '--transition_matrix', nargs='+', action='append', type=float, help='Define a transition '
                        'matrix. If provided, this will be used to determine the number of states. Each row of the '
                        'transition matrix should be passed with a separate -T flag')
    parser.add_argument('-s', '--nstates', default=2, type=int, help='Number of states to switch between')
    parser.add_argument('-slip', '--slip', default=0.01, type=float, help='Determines how frequently things will '
                        'switch states. A slip of 0 results in a transition matrix with only ones on the diagonal. '
                        'Higher values of slip will give smaller and smaller ratios of diagonals to the rest.')

    # Autoregressive parameters
    parser.add_argument('-r', '--order', default=1, type=int, help='Autoregressive order (number of time lags that '
                                                                   'yt depends on.')

    return parser


class StateError(Exception):
    """ Raised if an undefined reaction is attempted """

    def __init__(self, message):

        super().__init__(message)


class GenData:

    def __init__(self, type, transition_matrix, nstates=None, slip=0.25, order=1, stds=None, stdmax=1):
        """ Given a transition matrix, generate timeseries using Markov Chains

        :param type: underlying dynamical model ('Gaussian' or 'AR' are currently implemented)
        :param transition_matrix: a list of N N-length lists. Each list represents a row of the transition matrix. If
        None or False is passed, a transition matrix will be generated randomly
        :param nstates: number of states
        :param slip: determines ratio of diagonal elements to the rest. A higher 'high' will give you a smaller ratio of
        diagonals to the rest and vice versa. A high of zero will result in an identity matrix, meaning there will be no
        transitions from the initial state
        :param order: autoregressive order. Only specified if type is 'AR'
        :param stds: standard deviation of Gaussian white noise for each state. If None, random stds will be generated
        :param stdmax: maximum standard deviation of Gaussian white noise. This is only used if stds=None

        :type type: str
        :type transition_matrix: list of lists
        :type nstates: int
        :type slip: float
        :type order: int
        :type stds: list
        :type stdmax: float
        """

        self.type = type

        self.T = None
        if transition_matrix:
            self.T = np.array(transition_matrix)
            self.nstates = self.T.shape[0]  # define number of states based on provided transition matrix
        else:
            if not nstates:
                raise StateError("If no transition matrix is provided, the number of states must be specified")

            self.nstates = nstates
            self.generate_transition_matrix(slip)

        if type == 'AR':

            self.phis = np.zeros([self.nstates, order])
            for s in range(self.nstates):
                self.phis[s, :] = generate_ar_parameters(order)

        if not stds:
            self.stds = np.random.uniform(0, stdmax, size=self.nstates)
        else:
            self.stds = stds

        self.state_labels = np.arange(self.nstates)

    def generate_transition_matrix(self, high):
        """ generate a semi-random transition matrix

        :param high: determines ratio of diagonal elements to the rest. A higher 'high' will give you a smaller ratio of
        diagonals to the rest and vice versa. A high of zero will result in an identity matrix, meaning there will be no
        transitions from the initial state

        :type high: float
        """

        T = np.eye(self.nstates)  # start with identify matrix
        T += np.random.uniform(0, high, size=(self.nstates, self.nstates))  # add random draws from uniform distribution
        self.T = T / T.sum(axis=1, keepdims=1)  # normalize so sum of rows is 1

    def gen_trajectory(self, ndraws):
        """ Generate time series with chosen underlying dynamics

        :param ndraws: number of sequential points to generate
        :return:
        """

        if self.type == 'AR':

            return self.gen_ar_hmm(ndraws)

    def gen_gaussian_hmm(self, ndraws, means=None, var=None):
        """ Unfinished

        :param ndraws:
        :param means:
        :param var:
        :return:
        """

        if means is None:
            state_means = np.arange(self.nstates)

        if var is None:
            state_variances = 0.01 * np.ones(self.nstates)
        else:
            state_variances = var * np.ones(self.nstates)

        data = np.zeros([ndraws])
        state = np.random.choice(self.states)  # random initial state
        data[0] = norm.rvs(loc=state_means[state], scale=state_variances[state])

        for i in range(1, ndraws):
            state = np.random.choice(states, p=T[state, :])
            data[i] = norm.rvs(loc=state_means[state], scale=state_variances[state])

        return data

    def gen_ar_hmm(self, ndraws):
        """ Generate a mean-zero autoregressive timeseries based on the transition matrix and autoregressive parameters.
        The timeseries is defined as:

        yt = \sum_{n=1}^{r} phi_n * y_{t-n} + \epsilon_t

        where r is autoregressive order and \epsilon_t is Gaussian white noise with state-dependent variance

        :param ndraws: number of points to generate for timeseries
        :param phis: autoregressive coefficients for each state (n_phis x n_states)

        :type ndraws: int
        :type phis: np.ndarray
        """

        order = self.phis.shape[1]  # autoregressive order
        data = np.zeros([ndraws + order])
        state_labels = np.zeros([ndraws])

        state = np.random.choice(self.state_labels)  # choose initial state with uniform probability
        for d in range(ndraws):
            state = np.random.choice(self.state_labels, p=self.T[state, :])  # choose state based on transition matrix
            state_labels[d] = state  # actual state labels for future comparison
            ar = sum([x * data[d + order - (i + 1)] for i, x in enumerate(self.phis[state, :])])
            data[d + order] = ar + norm.rvs(scale=self.stds[state])

        return data[order:], state_labels


def generate_ar_parameters(r):
    """ generate autoregressive parameters, phi_n as defined below

    yt = \sum_{n=1}^{r} phi_n * y_{t-n} + \epsilon_t

    NOTE: for stationarity to be achieved, the roots of 1 - phi_1*z - phi_2*z^2 ... phi_n * z^n must lie outside the
    unit circle

    :param r: autoregressive order

    :type r: int

    :return: vector of autoregressive coefficients, phi
    """

    phi = None
    in_unit_circle = True
    while in_unit_circle:
        phi = np.random.uniform(-1, 1, size=r)  # made negative for compatibility with np.roots
        phi_transformed = [1] + (-1 * phi).tolist()
        roots = np.roots(phi_transformed[::-1])  # list reverse for compatibilty with np.roots
        in_unit_circle = False if np.absolute(roots).min() > 1 else True

    return phi


if __name__ == "__main__":

    args = initialize().parse_args()

    # generate trajectories
    data = np.zeros([args.ndraws, args.ntraj, 3])
    state_labels = np.zeros([args.ndraws, args.ntraj])

    data_generator = GenData(args.type, args.transition_matrix, nstates=args.nstates, slip=args.slip, order=args.order)

    for i in range(args.ntraj):
        data[:, i, 2], state_labels[:, i] = data_generator.gen_trajectory(args.ndraws)

    io.savemat('%s_data.mat' % args.type.lower(), dict(traj=data, labels=state_labels, T=data_generator.T,
                                                       phis=data_generator.phis))

    plt.plot(data[:, 0, 2])

    plt.show()