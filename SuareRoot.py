########################################################################################################################
#                                                                                                                      #
#                                  DIAGNOSTIC FRACTURE INJECTION TESTS ANALYSIS PROGRAM                                #
#                                                        Version 1.0                                                   #
#                                 Written for Python by : Fahd Siddiqui and Aqsa Qureshi                               #
#                                  https://github.com/DrFahdSiddiqui/DFITAnalysis-Python            				   #
#                                                                                                                      #
# ==================================================================================================================== #
# LICENSE: MOZILLA 2.0                                                                                                 #
#   This Source Code Form is subject to the terms of the Mozilla Public License, v. 2.0.                               #
#   If a copy of the MPL was not distributed with this # file, You can obtain one at http://mozilla.org/MPL/2.0/.      #
########################################################################################################################

########################################################################################################################

import numpy as np
import matplotlib.pyplot as plt
from BCAnalysis import BCAnalysis


# -------------------------------------------------------------------------------------------------------------------- #
class SquareRoot(BCAnalysis):
    """Class inherits from Analysis and defines functions specific to G-Function analysis."""

    # ---------------------------------------------------------------------------------------------------------------- #
    def __init__(self):
        """Constructor instantiates the variables to be used"""

        BCAnalysis.__init__(self)  # Super class constructor
        self.St = None  # Square root of dim'less time
        self.dSt = None  # Pressure derivative wrt sqrt time
        self.StdSt = None  # Pressure derivative wrt log of sqrt time

    # ---------------------------------------------------------------------------------------------------------------- #
    def analysis(self, well, dwindow):
        """Computes Square root time functions and derivative """
        self.St = np.sqrt(well.tD)
        self.dSt = SquareRoot.smoothDerivative(self.St, well.p_shut, dwindow)
        self.StdSt = self.St * self.dSt

    # ---------------------------------------------------------------------------------------------------------------- #
    def plotData(self, well, xmin, xmax, y1min, y1max, y2min, y2max, y3min, y3max):
        """Plots cartesian of p and St.dp/dSt vs St"""

        super().threeAxesFigure()
        # Ensures that the straight line and vertical lines are removed out if for each new figure.
        self.stLnPlot = None
        self.clsrPtPlot = None

        self.pressPlot, = self.yaxis1.plot(self.St, well.p_shut, 'b-')
        self.logDerPlot, = self.yaxis2.plot(self.St, self.StdSt, 'r-')
        self.derPlot, = self.yaxis3.plot(self.St, self.dSt, 'g-')

        self.fig.canvas.set_window_title('SquareRoot')
        self.fig.suptitle('Square Root Time Plot')
        self.yaxis1.set_xlabel('$t_D^{0.5}$')
        self.yaxis1.set_ylabel('Pressure [psi]')
        self.yaxis2.set_ylabel('$t_D^{0.5}.dp/dt_D^{0.5}$ [psi]')
        self.yaxis3.set_ylabel('$dp/dt_D^{0.5}$ [psi]')

        super().setAxesLims(xmin, xmax, y1min, y1max, y2min, y2max, y3min, y3max)

        # Displaying the plots in a non-blocking way
        plt.ion()
        plt.show()
        plt.ioff()

    # ---------------------------------------------------------------------------------------------------------------- #
    def identifyClosure(self, well):
        """Adapts the super (Analysis) class method for SRT. Asks user to select straight line through origin,
        select departure from line as closure pressure. Annotates the figure and prints closure pressure and stress
        to console"""

        super().identifyClosure(well)
        self.tClosure = (self.xClosure**2 * well.tp)/3600
        # TODO: Implement piecewise interpolation to get closure pressure
        idx = np.argmin(np.abs(self.St - self.xClosure))
        self.pClosure = well.p_shut[idx]

        super().annotateClosure()
        print('Square Root Time Analysis Results')
        print('Closure Pressure = {pc:.1f} psi '.format(pc=self.pClosure))
        print('Closure Time (after s/i) = {tc:.2f} hrs '.format(tc=self.tClosure))

########################################################################################################################
