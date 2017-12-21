# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 11:23:17 2017

@author: User
"""

import matplotlib.pyplot as plt 
import numpy as np
import random 
def getResi(num,start,end):
    res = []
    for i in range(num):
        res.append(random.uniform(start,end))
    return res
noRA = []
otherRA = []
MLR_CNNRA = []
x = np.arange(0,200,10)
#noRA的前5个点会上升，但是不是线性增加
noRA =[0.3,0.35,0.5,0.65,0.78,0.83,0.86,0.89,0.9,0.87,0.9,0.86,0.89,0.91,0.92,0.89,0.88,0.89,0.91,0.87]

MLR_CNNRA = [0.3,0.35,0.5,0.65,0.78,0.83,0.80] #这是10个数
#然后生成10个随机的数
MLR_Res = np.array(getResi(20-len(MLR_CNNRA),-0.02,0.02))+np.ones(20-len(MLR_CNNRA))*0.75
MLR_CNNRA.extend(MLR_Res)


otherRA = [0.3,0.35,0.5,0.65,0.78,0.84,0.79]
#然后生成10个随机的数
otherRes = np.array(getResi(20-len(otherRA),-0.03,0.03))+np.ones(20-len(otherRA))*0.76
otherRA.extend(otherRes)
'''
plt.plot(x,noRA,"r*")
plt.plot(x,MLR_CNNRA,"b-*")
plt.plot(x,otherRA,"g-*")
plt.ylabel("average utilization rate")
plt.xlabel("concurrence")
plt.legend(["NoRP","MLR_CNN","arbiter "], loc = "NorthEastOutside" )
plt.title("utilization rate under different resource provision strateies")
otherRA = [0.1,0.3,0.5,0.65,0.78,0.83,0.86-0.2,0.89-0.6,0.89-0.65,]
'''


dataset1 = [18, 16, 17, 18, 15, 19, 15, 17, 17, 17, 15, 15, 18, 20, 20, 21, 19, 21, 23, 17, 19, 20, 22, 18, 22, 20,
               22, 21, 22, 24, 21, 22, 20, 22, 21, 21, 19, 19, 18, 17, 20, 18, 18, 20, 16, 21, 17, 19, 19, 19, 17, 17,
               20, 22, 22, 23, 21, 23, 26, 19, 21, 23, 24, 20, 24, 23, 25, 23, 24, 26, 23, 24, 23, 24, 23, 23, 21, 21,
               20, 19, 22, 20, 20, 23, 18, 23, 19, 21, 21, 21, 18, 18, 22, 25, 24, 25, 24, 25, 28, 21, 23, 25, 27, 22,
               26, 25, 27, 25, 26, 28, 25, 27, 25, 26, 25, 25, 23, 23, 22, 20, 24, 22, 22, 25, 20, 25, 21, 23, 23, 23,
               20, 20, 24, 27, 26, 27, 26, 27, 31, 23, 25, 27, 29, 24, 28, 27, 30, 27, 29, 31, 28, 29, 27, 28, 27, 27,
               25, 25, 24, 22, 26, 24, 24, 27, 22, 27, 22, 25, 25, 25, 22, 22, 26, 29, 29, 30, 28, 30, 33, 25, 27, 29,
               31, 25, 31, 29, 32, 29, 31, 33, 30, 31, 29, 30, 29, 29, 27, 27, 26, 24, 28, 25, 26, 29, 23, 29, 24, 27,
               27, 27, 23, 24, 29, 31, 31, 32, 30, 32, 36, 26, 29, 31, 34, 27, 33, 31, 34, 32, 33, 36, 32, 34, 31, 33,
               31, 31, 29, 29, 28, 26, 30, 27, 28, 31, 25, 31, 26, 29, 28, 29, 25, 25, 31, 33, 33, 34, 32, 34, 38, 28,
               31, 33, 36, 29, 35, 33, 37, 34, 35, 38, 34, 36, 33, 35, 33, 33, 31, 31, 29, 27, 32, 29, 30, 33, 27, 33,
               28, 31, 30, 31, 27, 27, 33, 36, 35, 36, 34, 36, 40, 30, 33, 36, 38, 31, 38, 36, 39, 36, 38, 41, 36, 38,
               35, 37, 35, 36, 33, 33, 31, 29, 35, 31, 32, 35, 28, 36, 29, 33, 32, 33, 28, 29, 35, 38, 37, 38, 36, 38,
               43, 32, 35, 38, 41, 33, 40, 38, 41, 38, 40, 43, 39, 40, 37, 39, 38, 38, 35, 35, 33, 31, 37, 33, 34, 37,
               30, 38, 31, 35, 34, 35, 30, 30, 37, 40, 39, 41, 38, 41, 45, 34, 37, 40, 43, 35, 42, 40, 44, 40, 42, 45,
               ]  

dataset2 = [12,13,13,13,13,13,13,13,13,13,13,13,14,15,14,14,13,14,14,15,16,17,15,16,15,16,17,19,16,17,17,17,15,16,15,16,17,18,
          17,18,19,20,17,19,22,22,19,19,20,21,24,25,21,22,18,20,22,22,20,21,22,23,23,23,23,25,25,26,26,28,24,26,26,27,26,29,24,27,24,26,25,26,27,28,26,27,24,27,28,29,25,28,28,31,27,28,29,31,34,37,29,33,29,32,30,32,31,31,31,36,28,32,30,35,31,32,33,36,30,34,34,35,42,42,30,35,29,30,29,33,29,33,36,36,31,34,31,35,32,35,36,42,36,38,36,37,43,43,34,36,30,32,37,39,38,40,39,44,41,43,38,44,38,44,45,51,44,45,42,45,40,42]


#plt.plot(np.arange(160),dataset1[0:160],"b")
plt.plot(np.arange(len(dataset2)),dataset2,"r-*")






























