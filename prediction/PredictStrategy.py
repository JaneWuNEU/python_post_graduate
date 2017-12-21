# -*- coding: utf-8 -*-
"""
Created on Sun Mar 12 09:51:29 2017

@author: User
"""
#==============================================================================
# 这里主要使用ANN、SVR和指数回归进行预测
#==============================================================================
import pandas as pd
import matplotlib.pyplot as plt 
import numpy as np
from sklearn.svm import SVR
import sys
sys.path.append("D:/anaconda/project/utils")
from GM import ModifiedGreyForecastModel
import numpy as np
from utils import WRFile
class PredictStrategy:
        
    def predictMGM(self):
            wrFile = WRFile()
    part0 = "F:\\one\\predict\\traindata/workload"
    part1 = "inmin.xlsx"
    data = wrFile.readDataFromExcel(filePath=part0+str(58)+part1,cols=1)
    burst= data[1250:1260]
    increase = data[1240:1250]
    decrease = data[1260:1270]
    x = np.arange(0,len(data))
    plt.plot(x,data)
    plt.xlabel("time in minutes")
    plt.ylabel("workloads")
    plt.title("workloads of 58 during FIFA in 1986")
        
pre = PredictStrategy()
pre.predictSVR()
