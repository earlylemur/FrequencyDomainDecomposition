'''
Created on 4. aug. 2018

@author: Ole-Martin
'''
import numpy as np
import git_mainFDD
import git_mainFDD_HV
import git_FDDtools
from matplotlib import pyplot as plt
import sys
import git_mainPlotModeShapes
points = git_FDDtools.createMatrixFromCsv("sensorPointLocations.txt")

totMat1 = git_FDDtools.createMatrixFromCsv('sensor1.txt')
totMat2 = git_FDDtools.createMatrixFromCsv('sensor2.txt')
totMat3 = git_FDDtools.createMatrixFromCsv('sensor3.txt')
totMat4 = git_FDDtools.createMatrixFromCsv('sensor4.txt')


axis = 2

#chagnes



FDD_matrix_input = git_FDDtools.makeFDDmatrix(totMat1[:,axis+1],totMat2[:,axis+1],totMat3[:,axis+1],totMat4[:,axis+1])


#horizontalMat = git_FDDtools.makeHorizontalFDDmatrix(totMat1, totMat2, totMat3, totMat4)

title = "FDD plot"       
figTitleIn = "figTitleIn"  
FDDsolverTitle = 'FDDsolverTitle' 

samplingFreq = 128
Frequencies, dbs1, chosenPeaksFreq, chosenPeaksMag, chosenPeaksMS = git_mainFDD.mainFDD(FDD_matrix_input,samplingFreq,title,figTitleIn,FDDsolverTitle,writeToFile = 1,peakThresh=-40)


def plotModeShape(modeResult):
    #I want to 
    #plot mode shape complexity
    #    use the mode shape complexity functions?
    #plot mode shapes
    #    plot points
    #    Scale points
    
    
    modeResShape = np.shape(modeResult)
    numberOfModes = modeResShape[1]
    numberOfNodes = modeResShape[0]
    for i in range(numberOfModes):
        plt.figure("Mode Shape Complexity, Mode #"+str(i+1))
        git_mainPlotModeShapes.git_plotModeShapeComplexityHorizontal(modeResult[:,i])
        
        
    
    


mode = chosenPeaksMS[:,0]



git_mainPlotModeShapes.scalePoints(mode, points, 20000)

plt.ylim([-20000,20000])

plotModeShape(chosenPeaksMS)


print(chosenPeaksMS)
plt.show()  

