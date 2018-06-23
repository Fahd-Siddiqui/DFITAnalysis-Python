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
from math import pi
import matplotlib.pyplot as plt
from BCAnalysis import BCAnalysis


# -------------------------------------------------------------------------------------------------------------------- #
class GFunction(BCAnalysis):
    """Class inherits from Analysis and defines functions specific to G-Function analysis."""

    # ---------------------------------------------------------------------------------------------------------------- #
    def __init__(self):
        """Constructor instantiates the variables to be used"""

        BCAnalysis.__init__(self)  # Super class constructor
        self.G = None  # G-function
        self.dG = None  # Derivative of pressure with G = dp/dG
        self.GdG = None  # Log derivative of pressure = G.dp/dG

    # ---------------------------------------------------------------------------------------------------------------- #
    def analysis(self, well, dwindow):
        """Computes G - Function and derivative """

        tD = well.tD
        self.G = 4 / pi * 4 / 3 * (np.power((1 + tD), 3 / 2) - np.power(tD, 3 / 2) - 1)
        self.dG = super().smoothDerivative(self.G, well.p_shut, dwindow)
        self.GdG = self.G * self.dG

    # ---------------------------------------------------------------------------------------------------------------- #
    def plotData(self, well, xmin, xmax, y1min, y1max, y2min, y2max, y3min, y3max):
        """Plots cartesian of p and G.dp/dG vs G"""

        super().threeAxesFigure()
        # Ensures that the straight line and vertical lines are removed out if for each new figure.
        self.stLnPlot = None
        self.clsrPtPlot = None

        self.pressPlot, = self.yaxis1.plot(self.G, well.p_shut, 'b-')
        self.logDerPlot, = self.yaxis2.plot(self.G, self.GdG, 'r-')
        self.derPlot, = self.yaxis3.plot(self.G, self.dG, 'g-')

        self.fig.canvas.set_window_title('G-Function')
        self.fig.suptitle('G-Function Plot')
        self.yaxis1.set_xlabel('G-Function')
        self.yaxis1.set_ylabel('Pressure [psi]')
        self.yaxis2.set_ylabel('$G.dp/dG$ [psi]')
        self.yaxis3.set_ylabel('$dp/dG$ [psi]')

        super().setAxesLims(xmin, xmax, y1min, y1max, y2min, y2max, y3min, y3max)
        plt.draw()

    # ---------------------------------------------------------------------------------------------------------------- #
    def identifyClosure(self, well):
        """Adapts the super (Analysis) class method for SRT. Asks user to select straight line through origin,
        select departure from line as closure pressure. Annotates the figure and prints closure pressure and stress
        to console"""

        super().identifyClosure(well)
        # TODO: Implement a better way/interpolation to get closure pressure and time
        idx = np.argmin(np.abs(self.G - self.xClosure))
        self.pClosure = well.p_shut[idx]
        idx = np.argmin(np.abs(well.p - self.pClosure))
        self.tClosure = (well.t[idx] - well.tp) / 3600
        super().annotateClosure()
        print('G-Function Analysis Results')
        print('Closure Pressure = {pc:.1f} psi '.format(pc=self.pClosure))
        print('Closure Time (after s/i) = {tc:.2f} hrs '.format(tc=self.tClosure))

########################################################################################################################
