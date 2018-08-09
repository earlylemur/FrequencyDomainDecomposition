'''
Created on 30. jul. 2018

@author: Ole-Martin
'''
import numpy as np
import git_FDDtools

import git_mainPlotModeShapes
from matplotlib import pyplot as plt
#Creating empty lists to hold the different values.
realValues = []
imagValues = []
sensorID = ['1','2','3','4']
modeShape = git_FDDtools.createMatrixFromCsv("figTitleIn_Result.txt")


#Filling the lists of imaginary and real numbers, now, if we only take into account that we are handling singl
for i in range(2,len(modeShape)):
    number = complex(modeShape[i])
    realValues.append(number.real)
    imagValues.append(number.imag)
    

print("Length of real: "+str(len(realValues)))
print("Length of Im: "+str(len(imagValues)))

newArrRe = np.zeros((len(realValues)*2))
newArrIm = np.zeros((len(realValues)*2))
oldArrIndex = 0
for i in range(1,len(newArrIm),2):
    newArrRe[i] = realValues[oldArrIndex]
    newArrIm[i] = imagValues[oldArrIndex]
    oldArrIndex +=1
    
#plt.figure(title)
for i in range(0,len(newArrIm)-1):
    print(newArrRe[i])
    plt.plot([newArrRe[i],newArrRe[i+1]],[newArrIm[i],newArrIm[i+1]],'g')


for i in range(len(imagValues)):
    plt.text(realValues[i], imagValues[i], '%s' % sensorID[i] ,size = 10)

plt.plot(realValues,imagValues,'o')
plt.grid()
plt.xlabel('Re', size = 16)
plt.ylabel('Im', size = 16)
plt.ylim(-0.7,0.7)
plt.xlim(-0.7,0.7)
plt.axhline(y=0, color='k')
plt.axvline(x=0, color='k')
plt.show()