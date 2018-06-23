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

from DFITAnalysis import DFITAnalysis

# GET INPUT DATA FROM DATA FILE -------------------------------------------------------------------------------------- #
# Define input data file parameters
filename = 'DFITData.csv'
t_col = 1  # Time column number
p_col = 2  # Pressure column number
r_col = 3  # Rate column number
tp = 518  # Injection time in seconds
skip_rows = 1  # Number of header rows to skip
dwindow = 10  # Smoothing window for the derivative

# Object creation and data loading ----------------------------------------------------------------------------------- #
print('Loading data...')
Well_1 = DFITAnalysis(filename, skip_rows, t_col - 1, p_col - 1, r_col - 1, tp)
print('done')

# Analysis calculations and plots ------------------------------------------------------------------------------------ #
print('Performing DFIT analysis...')
Well_1.runAll(dwindow)  # Perform both G-function and Square root analyses

# Can also do the following interactively for G-Function
# Well_1.GFunction.analysis(Well_1, dwindow)
# Well_1.GFunction.plotData(Well_1, 0, 0, 0, 0, 0, 1000, 0, 40)
# Well_1.GFunction.identifyClosure(Well_1)

print('done')

########################################################################################################################
