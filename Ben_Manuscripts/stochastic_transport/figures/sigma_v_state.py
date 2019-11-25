#!/usr/bin/env python

""" Test how the predicted MSD changes as a function of the transition matrix using
the Markov State-Dependent model
"""

from LLC_Membranes.analysis.markov_state_dependent_dynamics import States 
from LLC_Membranes.llclib import file_rw
import numpy as np
import matplotlib.pyplot as plt

def transition_matrix(t):
	""" Make a 2D transition matrix with off diagonals 't' """

	T = np.zeros([2, 2])
	for i in range(2):
		for j in range(2):
			if i == j:
				T[i, j] = t
			else:
				T[i, j] = 1 - t
	return T

#sol = ['URE', 'GCL', 'MET', 'ACH']
sol = ['MET', 'ACH', 'URE', 'GCL']
names = {'URE': 'urea', 'GCL': 'ethylene glycol', 'MET': 'methanol', 'ACH': 'acetic acid'}
colors = {'URE':'xkcd:blue', 'GCL':'xkcd:orange', 'MET':'xkcd:green', 'ACH':'xkcd:magenta'}
path = '/home/bcoscia/Documents/Gromacs/Transport/NaGA3C11'
bar_width = 0.18
bar_locations = np.arange(1, 10)
alpha = 0.7

# each of the following rows corresponds to a residue
sigma = [
    [0.034, 0.033, 0.030, 0.027, 0.048, 0.040, 0.032, 0.028, 0.036],
    [0.045, 0.037, 0.030, 0.028, 0.062, 0.040, 0.040, 0.030, 0.045],
    [0.052, 0.043, 0.036, 0.036, 0.074, 0.042, 0.043, 0.037, 0.057],
    [0.035, 0.032, 0.030, 0.027, 0.048, 0.038, 0.031, 0.030, 0.040],
    ]

for i, res in enumerate(sol):
	heights = sigma[i]
	plt.bar(bar_locations + (i - 1)*bar_width - bar_width/2, heights, bar_width, label=names[res], color=colors[res], edgecolor='black', alpha=alpha)

plt.legend(fontsize=14)
plt.xticks(ticks=bar_locations, labels=[1, 2, 3, 4, 5, 6, 7, 8, 'T'])
plt.xlabel('State', fontsize=14)
plt.ylabel('$\sigma$', fontsize=14)
plt.ylim(0.02, 0.08)
plt.tick_params(labelsize=14)
plt.tight_layout()
plt.savefig('sigma_v_state.pdf')
plt.show()