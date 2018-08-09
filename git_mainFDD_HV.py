'''
Created on 1. jun. 2018

@author: Ole-Martin
'''

import git_FDDtools
import numpy as np
import pandas as pd
import sys
from matplotlib import pyplot as plt
from scipy.signal import csd
from numpy.linalg import svd

from matplotlib.axes._axes import Axes






def mainFDD_HV(mat1,mat2,mat3,mat4,sampleFreq,title,figTitle,FDDsolverTitle, peakThresh=-10000, frequencyThresh = 30, writeToFile = 0, horizontal = 1):
    # Frequency Domain Decomposition
    # Input:
    #     inputMatrix        -    [m,n] matrix where each column n contains m sample measurements from one channel
    #     sampleFreq         -    Number of samples per second in Hz
    #     peakThresh         -    Only the peaks with values above this threshold will be enumerated.
    #
    # Output: 
    #     Frequencies        -    Array of frequencies corresponding to the FDD-plot
    #     dbs1               -    Array of the absolute value of the identified singular values given in decibel.
    #     chosenPeaksFreq    -    Array of the frequencies corresponding to the peaks chosen by the user
    #     chosenPeaksMag     -    Array of the magnitude of the peaks chosen by the user
    #     chosenPeaksMS      -    Matrix [n,k] containing k modeshapes. Each row in n corresponds to the channel position n in inputMatrix.
    
    inputMatrix = np.empty((len(mat1),8),dtype = object)
    
    if(horizontal == 1):
        
        inputMatrix = git_FDDtools.makeHorizontalFDDmatrix(mat1, mat2, mat3, mat4)
    elif(horizontal == 0):
        inputMatrix = git_FDDtools.makeVerticalFDDmatrix(mat1, mat2, mat3, mat4)
    
    
    
    
    #Allocating space
    inputMatrixShape = np.shape(inputMatrix)
    rows = inputMatrixShape[0]
    cols = inputMatrixShape[1]
    trial = csd(inputMatrix[:,0],inputMatrix[:,1],sampleFreq)
    depth = len(trial[0])
    PSD_matrix = np.empty((rows,cols,depth),dtype='complex64')
    freq_matrix = np.empty((rows,cols,depth),dtype='float')
    Frequencies = np.empty(np.size(freq_matrix,2),dtype='float')
    Frequencies[:] = trial[0]
    
    
    #Compute PSD matrix, PSD_matrix[i,j,k]  where [i,j,:] contain the cross-spectra density of input channel i and j. 
    #    Each k corresponds to a frequency step derived from the given sample rate, so there is a 2D PSD matrix for each frequency step k.
    
    for i in range(np.size(inputMatrix,1)):
        for j in range(np.size(inputMatrix,1)):
            f,Pxy = csd(inputMatrix[:,i],inputMatrix[:,j],sampleFreq)
            PSD_matrix[i,j,:] = Pxy
            freq_matrix[i,j,:] = f
            
    
    #Allocating space
    testMat = PSD_matrix[:,:,1]
    testSVD = svd(testMat)
    u_svd = testSVD[0]
    
    
    s1 = np.empty(np.size(PSD_matrix,2),dtype='float')
    s2 = np.empty(np.size(PSD_matrix,2),dtype='float')
    ms = np.empty((np.size(u_svd,0),np.size(PSD_matrix,2)),dtype='complex64')
    ms2 = np.empty((np.size(u_svd,0),np.size(PSD_matrix,2)),dtype='complex64')
    
    #Performing Singular-value decomposition on the PSD-matrix.
    #By default, based on the assumption that the vibration of frequency k is dominated by a single mode, 
    #only the first and most prominent singular value, s1 ,is collected. The mode shape corresponding to s1 is collected in ms.
    for i in range(np.size(PSD_matrix,2)):
        u,s,vh = svd(PSD_matrix[:,:,i])
        s1[i] = s[0]
        s2[i] = s[1]
        ms[:,i] = u[:,0]
        
        #If the second singular values are to be examined.
        #s2[i] = s[1]
        #ms2[:,i] = u[:,1]
    
    
    #Creating array of magnitudes in decibel.
    dbs1 = np.empty(len(s1),dtype='float')
    for i in range(len(s1)):
        dbs1[i] = 5*np.log10(np.abs(s1[i]))
   
    #Simple peak identification. If a value is larger than both its neighbours, it is determined to be a peak.
    maxList =[]
    maxList_pos = []
    for i in range(1,len(s1)-1):
        if(s1[i-1] < s1[i] and s1[i+1]<s1[i] and s1[i] >= peakThresh):
            
            maxList.append(s1[i])
            maxList_pos.append(i)
            
    peakFreq = Frequencies[maxList_pos]
    peakMag = s1[maxList_pos] 
    
    
    #Mark peak with both circle and number, where the number can be used later for peak identification.
    xs = peakFreq
    ys = peakMag
    index = []
    for i in range(1,len(ys)+1):
        index.append(i)

    maxListDB =[]
    maxList_posDB = [] #This is a list of the index i at where the max frequencies are identified.
    for i in range(1,len(dbs1)-1):
        
        if(dbs1[i-1] < dbs1[i] and dbs1[i+1]<dbs1[i] and dbs1[i] >= peakThresh and Frequencies[i]< frequencyThresh):
            maxListDB.append(dbs1[i])
            
            maxList_posDB.append(i)
            
    
    
    peakFreqDB_globalIndex = np.empty((len(maxList_posDB),2),dtype=float)
    peakMagDB = np.empty(len(maxList_posDB),dtype=float)   
    peakMS = np.empty((len(ms),len(maxList_posDB)),dtype = complex)
   
       
    for i in range(len(maxList_posDB)):
        peakFreqDB_globalIndex[i,0] = maxList_posDB[i]
        peakFreqDB_globalIndex[i,1] = Frequencies[maxList_posDB[i]] #PeakfreqDb now contain the primary [globalIndex,thatpeakFrequency]
        
        peakMagDB[i] = dbs1[maxList_posDB[i]] 
        peakMS[:,i] = ms[:,maxList_posDB[i]]
    
    
    peakFrequencies = peakFreqDB_globalIndex[:,1]

    indexDB = []
    for i in range(1,len(peakMagDB)+1):
        indexDB.append(i)    
    
    peakFreqDataframe = pd.DataFrame(peakFrequencies,columns=['Frequencies[Hz]'])
    peakFreqDataframe.index +=1
    peakFreqDataframe.index.name = "#"
    peakFreqDataframe.columns.name = 'Peak no.'

    print(peakFreqDataframe)
    
    
    #Plot plot of the 1st singular values
    suggestedValuesPlotTitle =  FDDsolverTitle + "_Suggested 1st singular values, peak treshold = " + str(peakThresh)
    plt.figure(suggestedValuesPlotTitle)
    plt.plot(Frequencies,dbs1)
    plt.title(suggestedValuesPlotTitle,size = 16)
    for i in range(len(peakFrequencies)):
        plt.text(peakFrequencies[i], peakMagDB[i], '%s' % indexDB[i] ,size = 22)
    plt.plot(Frequencies[maxList_posDB],dbs1[maxList_posDB],'+')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('1st Singular Values [dB]')
    plt.grid()
    plt.show()

    
    peakMagDB_hstack = np.hstack(peakMagDB)
    peakFreqDB_hstack = np.hstack(peakFreqDB_globalIndex[:,1])
    
       
    numofpeaks = input('Enter desired number of peaks : ')
    numofpeaks = int(numofpeaks)
    selectedPeakIndex = np.empty(0,dtype = int)

    count = 0
    
    while(count < numofpeaks): #Betyr, så lenge tellingen er under eller lik numofpeaks, så vi skal iterere oss igjennom antall peaks
        
        print(str(numofpeaks-count) + ' peak(s) remaining')
        peak = input('Enter the ID number of the peak you would like to include: ')
        foundSame = 0
        for i in range(len(selectedPeakIndex)):
            if(int(peak) == selectedPeakIndex[i]):
                print("You have already selected peak :"+str(peak))
                print("Please select new peak")
                foundSame = 1
                break
        
        if(foundSame == 0):
            selectedPeakIndex = np.append(selectedPeakIndex,int(peak))
            count+=1
        
            
            
        
        
        
    selectedPeakIndex = np.sort(selectedPeakIndex)
    
    print('you have Chosen the following peaks..:')
    print(selectedPeakIndex)
    print("The selected peaks have been given new enumeration based on their ascending order")
    
    chosenPeaksFreq = np.empty(len(selectedPeakIndex),dtype=float)
    chosenPeaksMag = np.empty(len(selectedPeakIndex),dtype = float)
    chosenPeaksMS = np.empty((len(peakMS),len(selectedPeakIndex)),dtype = complex)
    
    
    for i in range(len(selectedPeakIndex)):
        chosenPeaksFreq[i] = peakFreqDB_hstack[selectedPeakIndex[i]-1]
        chosenPeaksMag[i] = peakMagDB_hstack[selectedPeakIndex[i]-1]
        chosenPeaksMS[:,i] = peakMS[:,selectedPeakIndex[i]-1]
    
    
    #Compute mode shapes
    outCols = np.size(chosenPeaksMS,1)
    outRows = (np.size(chosenPeaksMS,0)+2)
    outputWriteMatrix = np.empty((outRows,outCols),dtype=object)
    
    
    textArray = np.empty(outCols,dtype=object)
    for i in range(outCols):
        textArray[i] = str('Mode #'+str(i+1))
        
    outputWriteMatrix[2:,:] = chosenPeaksMS
    outputWriteMatrix[1,:] = chosenPeaksFreq
    outputWriteMatrix[0,:] = textArray

    if(writeToFile == 1):
        git_FDDtools.createCsvFromMatrix(outputWriteMatrix, figTitle+'_Result.txt')

    plt.figure(figTitle)
    plt.plot(Frequencies,dbs1)
    
    
    
    for i in range(len(chosenPeaksFreq)):
        plt.text(chosenPeaksFreq[i], chosenPeaksMag[i], '%s' % "#"+str(i+1), fontsize = 18 )
        
        
    
    
    plt.plot(Frequencies[maxList_posDB],dbs1[maxList_posDB],'+')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('1st Singular values [dB]')
    plt.grid()
    plt.show()
    
    return Frequencies, dbs1, chosenPeaksFreq, chosenPeaksMag, chosenPeaksMS
    


