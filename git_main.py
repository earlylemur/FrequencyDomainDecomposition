'''
Created on 4. aug. 2018

@author: Ole-Martin
'''



import git_FDDtools
import sys
git_FDDtools.git_setCurrentDirectory()
from matplotlib import pyplot as plt
import numpy as np
import git_mainFDD
import git_mainPlotModeShapes



points = git_FDDtools.createMatrixFromCsv("sensorPointLocations.txt")

totMat1 = git_FDDtools.createMatrixFromCsv('sensor1.txt')
totMat2 = git_FDDtools.createMatrixFromCsv('sensor2.txt')
totMat3 = git_FDDtools.createMatrixFromCsv('sensor3.txt')
totMat4 = git_FDDtools.createMatrixFromCsv('sensor4.txt')


axis = 3




FDD_matrix_input = git_FDDtools.makeFDDmatrix(totMat1[:,axis+1],totMat2[:,axis+1],totMat3[:,axis+1],totMat4[:,axis+1])


#horizontalMat = git_FDDtools.makeHorizontalFDDmatrix(totMat1, totMat2, totMat3, totMat4)

title = "FDD plot Z-axis"       
figTitleIn = "Z-axis"  
FDDsolverTitle = 'FDD Z-axis' 

samplingFreq = 128
Frequencies, dbs1, chosenPeaksFreq, chosenPeaksMag, chosenPeaksMS = git_mainFDD.mainFDD(FDD_matrix_input,samplingFreq,title,figTitleIn,FDDsolverTitle,writeToFile = 1,peakThresh=-40)


git_FDDtools.createCsvFromMatrix(chosenPeaksMS, "chosenPeaksMS.txt")

mode = chosenPeaksMS[:,0]




if(axis == 2):
    git_mainPlotModeShapes.plotModeShapes_subPlot_horizontal(chosenPeaksMS,points)

elif(axis == 3):
    git_mainPlotModeShapes.plotModeShapes_subPlot_vertical(chosenPeaksMS, points)
    

plt.show()  

