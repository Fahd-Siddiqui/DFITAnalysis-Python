########################################################################################################################
#                                                                                                                      #
#                                 DIAGNOSTIC FRACTURE INJECTION TESTS ANALYSIS PROGRAM                                 #
#                                                     Version 1.0                                                      #
#                                Written for Python by : Fahd Siddiqui and Aqsa Qureshi                                #
#                                 https://github.com/DrFahdSiddiqui/DFITAnalysis-Python            				       #
#                                                                                                                      #
# ==================================================================================================================== #
# LICENSE: MOZILLA 2.0                                                                                                 #
#   This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.                               #
#   If a copy of the MPL was not distributed with this # file, You can obtain one at http://mozilla.org/MPL/2.0/.      #
########################################################################################################################

########################################################################################################################

import numpy as np
import matplotlib.pyplot as plt
from GFunction import GFunction
from SuareRoot import SquareRoot


# -------------------------------------------------------------------------------------------------------------------- #
class DFITAnalysis:
    """Defines the well object and loads the pressure data from the csv file. Plots the pressure and rate vs time."""

    # ---------------------------------------------------------------------------------------------------------------- #
    def __init__(self, filename, skip_rows, t_col, p_col, r_col, tp):
        """Constructs the class object and loads the data"""

        plt.ioff()
        self.filename = filename
        self.skip_rows = skip_rows
        self.t_col = t_col
        self.p_col = p_col
        self.r_col = r_col
        self.tp = tp

        self.data = np.loadtxt(filename, delimiter=',', skiprows=skip_rows)
        self.p = self.data[:, self.p_col]
        self.t = self.data[:, self.t_col]
        self.r = self.data[:, self.r_col]

        self.tp_row = np.min(np.nonzero(self.t >= tp)[0])
        self.p_shut = self.p[self.tp_row:-1]
        self.tD = (self.t[self.tp_row:-1] - tp) / tp

        # Plot the job plot
        self.jobPlot(0, 0, 0, 0, 0, 0, 0, 0)

        # Initialize the analyses
        self.GFunction = GFunction()
        self.SquareRoot = SquareRoot()

    # ---------------------------------------------------------------------------------------------------------------- #
    def jobPlot(self, xmin, xmax, y1min, y1max, y2min, y2max, y3min, y3max):
        """Plots the data and sets the x and y axes limits to the ones provided."""

        self.fig, yaxis1 = plt.subplots()
        yaxis2 = yaxis1.twinx()

        p1, = yaxis1.plot(self.t / 3600, self.p, 'b-')
        p2, = yaxis2.plot(self.t / 3600, self.r, 'r-')

        self.fig.suptitle('Job Plot')
        self.fig.canvas.set_window_title('JobPlot')
        yaxis1.set_xlabel('Time [hrs]')
        yaxis1.set_ylabel('Pressure [psi]')
        yaxis2.set_ylabel('Rate [bpm]')

        if (xmin == 0 or xmax == 0) and xmin < xmax:
            yaxis1.set_xlim(xmin, xmax)
        else:
            yaxis1.set_xlim(xmin=0)
        if (y1min == 0 or y1max == 0) and y1min < y1max:
            yaxis1.set_ylim(y1min, y1max)
        if (y2min == 0 or y2max == 0) and y2min < y2max:
            yaxis2.set_ylim(y2min, y2max)

        tkw = dict(size=4, width=1.5)
        yaxis1.tick_params(axis='x', **tkw)
        yaxis1.tick_params(axis='y', colors=p1.get_color(), **tkw)
        yaxis2.tick_params(axis='y', colors=p2.get_color(), **tkw)

        yaxis1.yaxis.label.set_color(p1.get_color())
        yaxis2.yaxis.label.set_color(p2.get_color())

        plt.draw()

    # ---------------------------------------------------------------------------------------------------------------- #
    def runAll(self, dwindow):
        """Runs all analyses and plots"""

        self.GFunction.analysis(self, dwindow)
        self.GFunction.plotData(self, 0, 0, 0, 0, 0, 4000, 0, 4000)
        self.GFunction.identifyClosure(self)

        self.SquareRoot.analysis(self, dwindow)
        self.SquareRoot.plotData(self, 0, 0, 0, 0, 0, 4000, 0, 4000)
        self.SquareRoot.identifyClosure(self)

        # TODO: Future features for after closure analysis
        # self.ACASoliman.analysis(self, dwindow)

        # Following line prevents the program from quiting until all plots are closed.
        plt.show()

########################################################################################################################
