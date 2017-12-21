# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 19:57:40 2017

@author: User
"""
from numpy.polynomial.polynomial import polyval
import numpy as np
import math
import matplotlib.pyplot as plt 


C = np.array([ 1,  3,  4, 3, 1])
B = [3,6,9.25,10.25,9.5,7.25,3.5,1.25,0.25]
A = [1,1,0,-1,1]
x1_list = []
x2_list = []
x3_list = []
x4_list= []
for x in np.linspace(2,10,50):
    a = 2*polyval(x,A)/polyval(x,C)
    b = -2*polyval(x,B)/polyval(x,C)/x
    x1 = x
    x2 = x*x
    x3 = x**3
    x4 = (1-b/a)*math.exp(-a*4)+b/a
    x1_list.append(x1)
    x2_list.append(x2)
    x3_list.append(x3)
    x4_list.append(x4)
plt.plot(np.linspace(-2,2,50),x3_list)
plt.plot(np.linspace(-2,2,50),x4_list)
plt.legend(["x3","x4"])