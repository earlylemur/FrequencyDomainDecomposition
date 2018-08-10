'''
Created on 28. jul. 2018

@author: Ole-Martin
'''


import numpy as np
import pandas as pd
import os, errno
import sys


def createVerticalModeShapeFDD(mat1,mat2,mat3,mat4):
    #This function creates the FDD input matrix only including the coordinates deemed necessary for the visualization of th evertical mode shapes.
    #Only te 
    
    listOfMat = [mat1,mat2,mat3,mat4]
    listOfMatIndex = [0,1,2,3]
    
    matRdy4FDD = np.empty((len(mat1),8))
    matRdyIndex = [0,2,4,6]
    curMatColIndex = [2,4]
    for i in range(0,len(listOfMat)):
        for j in range(2):
            currentMat = listOfMat[listOfMatIndex[i]]
            matRdy4FDD[:,matRdyIndex[i]+j] = currentMat[:,curMatColIndex[j]]
    
    
    return matRdy4FDD       
          
def makeHorizontalFDDmatrix(mat1,mat2,mat3,mat4):
    
    FDDmatIn = np.empty((len(mat1),8),dtype=object)
    
    FDDmatIn[:,0:2] = mat1[:,2:4]
    FDDmatIn[:,2:4] = mat2[:,2:4]
    FDDmatIn[:,4:6] = mat3[:,2:4]
    FDDmatIn[:,6:] = mat4[:,2:4]
    
    return FDDmatIn

def makeVerticalFDDmatrix(mat1,mat2,mat3,mat4):
    listOfMat = [mat1,mat2,mat3,mat4]
    FDDmatIn = np.empty((len(mat1),8),dtype=object)
    verticalIndex = [2,4]
    FDDmatInCount = 0 
    for i in range(len(listOfMat)):
        for j in range(2):
            FDDmatIn[:,FDDmatInCount] = listOfMat[i][:,verticalIndex[j]]
            FDDmatInCount+=1
            
            
            
    
    
    return FDDmatIn
            

def makeFDDmatrix(mat0,mat1,mat2,mat3):
    
    
    if(len(np.shape(mat0)) == 1):
        colmat0 = 1
    else: colmat0 = np.size(mat0,1)
    
    if(len(np.shape(mat1)) == 1):
        colmat1 = 1
    else: colmat1 = np.size(mat1,1)
   
    if(len(np.shape(mat2)) == 1):
        colmat2 = 1
    else: colmat2 = np.size(mat2,1)
    
    if(len(np.shape(mat3)) == 1):
        colmat3 = 1
    else: colmat3 = np.size(mat3,1)
    
    columnSum = colmat0+colmat1+colmat2+colmat3
    
    FDDmatIn = np.empty((len(mat0),columnSum),dtype = object)
    FDDmatIn[:,0:colmat0] = np.vstack(mat0)
    FDDmatIn[:,colmat0:colmat0+colmat1] = np.vstack(mat1)
    FDDmatIn[:,colmat0+colmat1:colmat0+colmat1+colmat2]= np.vstack(mat2)
    FDDmatIn[:,colmat0+colmat1+colmat2:colmat0+colmat1+colmat2+colmat3] = np.vstack(mat3)
    
    return FDDmatIn


def createMatrixFromCsv(nameAndLoc): 
    
    #Takes in a .txt-file with ; as delimiter.
    #/sensorID/Timestamp dtype=str /X/Y/Z/isGap
    dfReadXX = pd.read_csv(nameAndLoc, index_col=False, header=None, delimiter=";") #reads the csvfile as a dataframe
    matFillXX = dfReadXX.as_matrix()                                                #creates a numpy-matrix from the dataframe.

    return matFillXX


def createCsvFromMatrix(mat2,outputFileAndName):    
    outputMatDf = pd.DataFrame(mat2)
    pd.DataFrame.to_csv(outputMatDf,outputFileAndName,sep=";",header=None, index=None)
    

def createFolder(folderPathAndName):

    try:
        os.makedirs(folderPathAndName)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    
    
def git_setCurrentDirectory():
    sys.path.insert(0,'C:/Users/Ole-Martin/Documents/00 - Master/Python/FDD_project/src/FrequencyDomainDecomposition')


git_setCurrentDirectory()