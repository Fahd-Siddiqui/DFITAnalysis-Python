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


# -------------------------------------------------------------------------------------------------------------------- #
class BCAnalysis:
    """Super class for performing Before Closure Analyses"""

    # ---------------------------------------------------------------------------------------------------------------- #
    def __init__(self):
        """Constructor for initializing shared variables of sub classes"""
        self.fig = None  # Figure for selected analysis
        self.yaxis1 = None  # Handle for first y-axis for the figure
        self.yaxis2 = None  # Handle for second y-axis for the figure
        self.yaxis3 = None  # Handle for third y-axis for the figure
        self.pressPlot = None  # Handle for pressure plotted on first y-axis
        self.logDerPlot = None  # Handle for log derivative of pressure plotted on first y-axis
        self.derPlot = None  # Handle for primary derivative of pressure plotted on second y-axis
        self.stLnPlot = None  # Handle for line through origin plotted on second y-axis
        self.clsrPtPlot = None  # Handle for vertical line indicating closure plotted on second y-axis
        self.xClosure = None  # x-coordinate of the clicked point on the fig (closure on G or t^0.5)
        self.pClosure = 1  # Closure pressure in psi
        self.tClosure = 1  # Closure time in hours
        self.cidDraw = None  # Handle for connection id to connect mouse motion to figure
        self.cidClick = None  # Handle for connection id to connect mouse click to figure
        self.annClosure = None  # Handle for annotation on figure displaying closure pressure and time

    # ---------------------------------------------------------------------------------------------------------------- #
    @staticmethod
    def smoothDerivative(X, Y, dwindow):
        """ Computes smooth derivatives by obtaining slope of the least square line through the selected window"""

        dYdX = np.zeros((np.shape(Y)[0],))
        for i in range(0 + dwindow, np.shape(X)[0] - dwindow):
            x = X[i - dwindow:i + dwindow]
            y = Y[i - dwindow:i + dwindow]
            _, b = np.linalg.lstsq(np.column_stack((np.ones_like(x), x)), y, rcond=None)[0]
            dYdX[i] = abs(b)
        return dYdX

    # ---------------------------------------------------------------------------------------------------------------- #
    def threeAxesFigure(self):
        """Creates a blank formatted figure with three y-axes"""

        self.fig, yaxis1 = plt.subplots()
        self.fig.subplots_adjust(right=0.8)
        yaxis2 = yaxis1.twinx()
        yaxis3 = yaxis1.twinx()
        yaxis3.spines["right"].set_position(("axes", 1.15))

        self.pressPlot, = yaxis1.plot([None, None], [None, None], 'b-')
        self.logDerPlot, = yaxis2.plot([None, None], [None, None], 'r-')
        self.derPlot, = yaxis3.plot([None, None], [None, None], 'g-')

        tkw = dict(size=4, width=1.5)
        yaxis1.tick_params(axis='x', **tkw)
        yaxis1.tick_params(axis='y', colors=self.pressPlot.get_color(), **tkw)
        yaxis2.tick_params(axis='y', colors=self.logDerPlot.get_color(), **tkw)
        yaxis3.tick_params(axis='y', colors=self.derPlot.get_color(), **tkw)

        yaxis1.yaxis.label.set_color(self.pressPlot.get_color())
        yaxis2.yaxis.label.set_color(self.logDerPlot.get_color())
        yaxis3.yaxis.label.set_color(self.derPlot.get_color())

        self.yaxis1 = yaxis1
        self.yaxis2 = yaxis2
        self.yaxis3 = yaxis3

    # ---------------------------------------------------------------------------------------------------------------- #
    def setAxesLims(self, xmin, xmax, y1min, y1max, y2min, y2max, y3min, y3max):
        """Sets axes limits for the plot"""

        if (xmin == 0 or xmax == 0) and xmin < xmax:
            self.yaxis1.set_xlim(xmin, xmax)
        else:
            self.yaxis1.set_xlim(xmin=0)
        if (y1min == 0 or y1max == 0) and y1min < y1max:
            self.yaxis1.set_ylim(y1min, y1max)
        if (y2min == 0 or y2max == 0) and y2min < y2max:
            self.yaxis2.set_ylim(y2min, y2max)
        if (y3min == 0 or y3max == 0) and y3min < y3max:
            self.yaxis3.set_ylim(y3min, y3max)

    # ---------------------------------------------------------------------------------------------------------------- #
    def identifyClosure(self, well):
        """Identify closure pressure by drawing a straight line through the origin and selecting the closure point"""

        # Removes the vertical and straight lines from plot if the identify closure is called again on same figure.
        if self.stLnPlot is not None:
            self.yaxis2.lines.remove(self.stLnPlot)
        if self.clsrPtPlot is not None:
            self.yaxis2.lines.remove(self.clsrPtPlot)
        self.stLnPlot = None
        self.clsrPtPlot = None

        # Show plot and turn on interactivity
        plt.ion()
        plt.show()

        print('Click to draw the straight line through origin. \n')
        self.cidDraw = self.fig.canvas.mpl_connect('motion_notify_event', self.drawStraightLine)
        self.cidClick = self.fig.canvas.mpl_connect('button_press_event', self.drawStraightLine)
        self.fig.canvas.start_event_loop(timeout=-1)

        print('Click to select closure pressure. \n')
        self.cidDraw = self.fig.canvas.mpl_connect('motion_notify_event', self.drawVerticalLine)
        self.cidClick = self.fig.canvas.mpl_connect('button_press_event', self.drawVerticalLine)
        self.fig.canvas.start_event_loop(timeout=-1)

        plt.ioff()

    # ---------------------------------------------------------------------------------------------------------------- #
    def drawStraightLine(self, event):
        """Draw the straight line through origin by following the mouse pointer"""

        if event.inaxes is None:  # if event is within the axes bounds
            return
        if event.button == 1:  # If mouse left button is clicked
            self.fig.canvas.stop_event_loop()
            self.fig.canvas.mpl_disconnect(self.cidDraw)
            self.fig.canvas.mpl_disconnect(self.cidClick)

        # Ensure to obtain data from second y-axis instead of default (random?) axis
        x, xdydx = self.yaxis2.transData.inverted().transform((event.x, event.y))

        if self.stLnPlot is None:
            self.stLnPlot, = self.yaxis2.plot([0, x], [0, xdydx], 'k--')
        else:
            self.stLnPlot.set_ydata([0, xdydx])
            self.stLnPlot.set_xdata([0, x])
        self.fig.canvas.draw()

    # ---------------------------------------------------------------------------------------------------------------- #
    def drawVerticalLine(self, event):
        """Draw the Vertical line following the mouse pointer"""

        if event.inaxes is None:
            return
        if event.button == 1:
            self.fig.canvas.stop_event_loop()
            self.fig.canvas.mpl_disconnect(self.cidDraw)
            self.fig.canvas.mpl_disconnect(self.cidClick)

        # Only x-coordinate is needed to make a vertical line
        x, _ = self.yaxis2.transData.inverted().transform((event.x, event.y))

        if self.clsrPtPlot is None:
            self.clsrPtPlot, = self.yaxis2.plot([x, x], [0, self.yaxis2.axes.viewLim.ymax], 'k--')
        else:
            self.clsrPtPlot.set_ydata([0, self.yaxis2.axes.viewLim.ymax])
            self.clsrPtPlot.set_xdata([x, x])
        # x is closure on either G-function scale or square root time scale (not time)
        self.xClosure = x
        self.fig.canvas.draw()

    # ---------------------------------------------------------------------------------------------------------------- #
    def annotateClosure(self):
        """Annotates the figure with closure pressure and time with arrow indicating the coordinates."""

        annotationText = 'Closure Pressure = {pc:.1f} psi \nClosure Time (after s/i) = {tc:.2f}  hrs ' \
            .format(pc=self.pClosure, tc=self.tClosure)

        arrow_props = dict(facecolor='black',
                           connectionstyle='arc, angleA=-90, angleB=0, armA=0, armB=40, rad=0.0',
                           arrowstyle='->')

        # if annotation exists, remove it
        if self.annClosure is not None:
            self.fig.texts.pop()
        self.annClosure = self.yaxis1.annotate(annotationText,
                                               xy=(self.xClosure, self.pClosure), xycoords='data',
                                               xytext=(0.5, .8), textcoords='axes fraction',
                                               arrowprops=arrow_props, bbox=dict(boxstyle='round', alpha=0.2))

        self.fig.texts.append(self.yaxis1.texts.pop())
        # Updates the figure with annotation
        plt.draw()


# TODO: Future Code for ACA
# ACA Soliman: Plots log - log of p and t.dp / dt vs total time
#
#     well.figPt = figure;
#     AX = plotyy(well.t / 3600, well.p, well.t / 3600, well.tdpt);
#     set(AX, 'xscale', 'log', 'yscale', 'log');
#
#     xlabel('Total time [hrs]')
#     xlim(AX, [xmin / 3600 xmax])
#
#     ylabel('Pressure [psi]')
#     ylim([y1min y1max])
#
#     ylabel(AX(2), 't.dp/dt [psi]')
#     ylim(AX(2), [y2min y2max])
# end
##

########################################################################################################################
