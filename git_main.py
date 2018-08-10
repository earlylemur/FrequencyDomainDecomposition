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


axis = 2




FDD_matrix_input = git_FDDtools.makeFDDmatrix(totMat1[:,axis+1],totMat2[:,axis+1],totMat3[:,axis+1],totMat4[:,axis+1])


#horizontalMat = git_FDDtools.makeHorizontalFDDmatrix(totMat1, totMat2, totMat3, totMat4)

title = "FDD plot"       
figTitleIn = "figTitleIn"  
FDDsolverTitle = 'FDDsolverTitle' 

samplingFreq = 128
Frequencies, dbs1, chosenPeaksFreq, chosenPeaksMag, chosenPeaksMS = git_mainFDD.mainFDD(FDD_matrix_input,samplingFreq,title,figTitleIn,FDDsolverTitle,writeToFile = 1,peakThresh=-40)


def plotModeShape(modeResult,points,scalefactor=20000):
    #I want to 
    #plot mode shape complexity
    #    use the mode shape complexity functions?
    #plot mode shapes
    #    plot points
    #    Scale points
    
    
    modeResShape = np.shape(modeResult)
    numberOfModes = modeResShape[1]
    numberOfNodes = modeResShape[0]

    print("complexity")     
    for i in range(numberOfModes):
        plt.figure("Mode Shape Complexity, Mode #"+str(i+1))
        git_mainPlotModeShapes.git_plotModeShapeComplexityHorizontal(modeResult[:,i])
        
    
    print("shapes")
    for i in range(numberOfModes):
        plt.figure("Modeshape #"+str(i+1))
        git_mainPlotModeShapes.plotSensorLocation_horizontal(points, plotRealSensors = 1)
        git_mainPlotModeShapes.scalePoints(modeResult[:,i].real, points, scalefactor, plotRealSensors = 1)
        plt.ylim([-20000,20000])
        
        
    
    


mode = chosenPeaksMS[:,0]





plotModeShape(chosenPeaksMS,points)



plt.show()  

