#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

class Radar(object):

    def __init__(self, figure, title, labels, nlines=5, rect=None):

        if rect is None:
            rect = [0.05, 0.05, 0.9, 0.9]

        self.n = len(title)
        self.angles = np.arange(0, 360, 360.0/self.n)

        self.axes = [figure.add_axes(rect, projection='polar', label='axes%d' % i) for i in range(self.n)]

        self.ax = self.axes[0]
        self.ax.set_thetagrids(self.angles, labels=title, fontsize=16)

        for ax in self.axes[1:]:
            ax.patch.set_visible(False)
            ax.grid(False)
            ax.xaxis.set_visible(False)

        for ax, angle, label in zip(self.axes, self.angles, labels):
            ax.set_rgrids(range(1, nlines + 1), angle=angle, labels=label)
            ax.spines['polar'].set_visible(False)
            ax.set_ylim(0, nlines + 1)

    def plot(self, values, *args, **kw):
        angle = np.deg2rad(np.r_[self.angles, self.angles[0]])
        values = np.r_[values, values[0]]
        self.ax.plot(angle, values, *args, **kw)


if __name__ == '__main__':

    fig = plt.figure(figsize=(8, 8))

    res = ['URE', 'GCL', 'MET', 'ACH']
    nlines = 5
    opacity = 0.6
    lw = 0 

    titles = [r'$P(\mathbf{\alpha_d})$', r'$P_T(\mathbf{\alpha_d}, \lambda)$', r'$P_T(\alpha_d, \mathbf{\lambda})$', r'$\mathcal{N}(\mathbf{\sigma})$', r'$L(\mathbf{\sigma}, \alpha_h)$', r'$L(\sigma, \mathbf{\alpha_h}$)', '$H$']

    # order: URE, GCL, MET, ACH
    P_alphad_1 = [0.57, 0.69, 0.90, 0.58]
    PT_alphad_1 = [0.56, 0.62, 1.04, 0.41]
    PT_lambda_1 = [3.7, 2.6, .6, 2.6]
    N_sigma_1 = [0.35, 0.38, 0.45, 0.32]
    L_sigma_1 = [0.24, 0.26, 0.31, 0.21]
    L_alphah_1 = [1.91, 1.99, 1.97, 1.91]
    H_1 = [0.37, 0.40, 0.30, 0.34]

    params = np.array((P_alphad_1, PT_alphad_1, PT_lambda_1, N_sigma_1, L_sigma_1, L_alphah_1, H_1))
    precision = [2, 2, 1, 2, 2, 2, 2]
    m = np.zeros(params.shape[0])
    b = np.zeros(params.shape[0])
    
    lab = []
    for i in range(7):
        if precision[i] == 2:
            lab.append(["%.2f" %i for i in np.linspace(params[i, :].min(), params[i, :].max(), nlines)])
        elif precision[i] == 1:
            lab.append(["%.1f" %i for i in np.linspace(params[i, :].min(), params[i, :].max(), nlines)])
        m[i] = (params[i, :].max() - params[i, :].min()) / (nlines - 1)
        b[i] = params[i, :].min()
       
    radar = Radar(fig, titles, lab, rect=[0.1, 0.1, 0.8, 0.8], nlines=nlines)

    colors = {'URE': 'xkcd:blue', 'GCL': 'xkcd:orange', 'MET': 'xkcd:green', 'ACH': 'xkcd:magenta'}
    names = {'URE': 'Urea', 'GCL': 'Ethylene Glycol', 'MET': 'Methanol', 'ACH': 'Acetic Acid'}
    for i, r in enumerate(res):
        data1 = 1 + ((params[:, i] - b) / m)
        radar.plot(data1,  '-', lw=lw, color=colors[r], alpha=opacity, label=names[r], marker='o', markersize=10)

    #for i in range(params.shape[0]):
        #radar.axes[i].tick_params(labelsize=12)
    #plt.draw()   
    leg = radar.ax.legend(fontsize=14, bbox_transform=radar.ax.transAxes, loc=3, bbox_to_anchor=(-0.1, -0.075))

    # https://stackoverflow.com/questions/49488018/radar-plot-matplotlib-python-how-to-set-label-alignment
    angle = 360 / len(titles)
    #ticks = [i*angle for i in range(len(titles))]
    alignment = ["left", "left", "right", "right", "right", "left"]
    for label, align in zip(radar.ax.get_xticklabels(), alignment):
        label.set_horizontalalignment(align)
        #label.set_rotation(ticks)
    plt.tight_layout()
    if lw == 0:
        plt.savefig('1mode_radar_nolines.pdf')
    else:
        plt.savefig('1mode_radar.pdf')
    plt.show()
