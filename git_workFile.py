'''
Created on 30. jul. 2018

@author: Ole-Martin
'''
import numpy as np
import git_FDDtools

import git_mainPlotModeShapes
from matplotlib import pyplot as plt



plt.figure()
leftEdge = [988.31323349475, 102774.89610296187]
rightEdge = [237.20618390647, -4065.89048708391]
plt.plot(leftEdge,rightEdge,'g')

plt.show()