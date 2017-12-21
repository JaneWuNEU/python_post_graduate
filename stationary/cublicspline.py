# -*- coding: utf-8 -*-
"""
Created on Wed Feb 15 18:31:15 2017

@author: User
"""
import sys
import math
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.interpolate import spline
from scipy.interpolate import UnivariateSpline
import pandas as pd
import statsmodels.api as sm
sys.path.append("D:/anaconda/project/utils")
from utils import WRFile
def useCubicSplineFitData():
    
    #读取数据
    wrFile = WRFile()
    filePath = "F:/one/final/spline/workload51inmin_knots.xlsx"
    yaxis = np.array(wrFile.readDataFromExcel(filePath))
    period = 5
    
   #使用cubic spline进行拟合
    data_volume = len(yaxis)
    xaxis = np.arange(0,data_volume,1)*period
    s = UnivariateSpline(x = xaxis,y = yaxis)
    
  #使用spline的拟合结果对每分钟的并发量进行预测，并获取残差
    y = wrFile.readDataFromExcel(filePath = "F:/one/final/inmin/workload51inmin.xlsx")
    xnew =  np.arange(0,len(y),1)
    ynew = s(xnew)
    residual = ynew-y
    plt.plot(xnew,residual)
    #analyzeResidulUseARMA(residual)
  
def analyzeResidulUseARMA(residual):
    data = pd.Series(residual)
    data_diff1 = data.diff(1)
    x = np.arange(0,len(data_diff1),1)
    data_diff2 = data_diff1- np.ones(len(data_diff1))*np.mean(data_diff1)
    
    
    #sm.graphics.tsa.plot_acf(data_diff1,lags = 10)
useCubicSplineFitData()