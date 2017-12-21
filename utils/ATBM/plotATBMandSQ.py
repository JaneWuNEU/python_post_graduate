# -*- coding: utf-8 -*-
"""
Created on Sun Jul  9 14:45:19 2017

@author: wujing
"""
'''
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import numpy as np
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
sp = ax.scatter(np.arange(1,20,1),np.arange(5,24,1),np.sin(np.arange(2,21,1)), s=10, c=np.arange(-10,9,1))
fig.colorbar(sp)
'''

from sympy import *
x = Symbol("x")
y = Symbol("y")
z = Symbol("z")
r1= x*(y+z)
r2= y*(x+z)
r = r1+r2
print(expand(r))
#print(collect(r))
