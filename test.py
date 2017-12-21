# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 10:13:42 2017

@author: User
"""

import matplotlib.pyplot as plt 
import sys
sys.path.append("D:/anaconda/project/utils")
sys.path.append("D:/anaconda/project/prediction")
import numpy as np
from utils import WRFile
from GM import ModifiedGreyForecastModel
def testGM():
    wrFile = WRFile()
    part0 = "F:\\one\\predict\\traindata/workload"
    part1 = "inmin.xlsx"
    data = wrFile.readDataFromExcel(filePath=part0+str(53)+part1,cols=1)
    
    data_start = 1020
    data_end = 1050
    burst= [62521, 62039, 61101, 66726, 64129, 61820, 63928, 63368, 61212, 60820, 59900, 62070, 62238, 61918, 61982, 64066, 65818, 63337, 65027, 64501, 68320,80460,63368, 61212, 60820, 59900, 62070,62521, 62039, 61101, 66726]
    x = np.arange(0,len(burst))
    #使用GM进行预测
    periods = 5
    GM = ModifiedGreyForecastModel(periods =periods)
    
    
    start = data_start
    pre_list = []
    start = 1
    for i in range(periods,len(burst)):
        x_0 = burst[start:i]
        
        pre = GM.predictGMValue(x_0)
        
        pre_list.append(pre)
        start += 1
   
    plt.plot(x,burst,"b-*")
    plt.plot(np.arange(periods,periods+len(pre_list)),pre_list,"r-*")
    plt.legend(["real","predict"])
    plt.xlabel("time in minutes")
    plt.ylabel("workloads")
    plt.title("Prediction With GM")
def testY():
    x = np.arange(0,1,0.1)
    y = np.arange(0,10)
    z = y-y*x-x
    print(z)
testY()