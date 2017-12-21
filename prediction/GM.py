# -*- coding: utf-8 -*-
"""
Created on Tue Mar 14 10:25:13 2017

@author: User
"""
import sys
sys.path.append("D:/anaconda/project/utils")
import numpy as np
from utils import WRFile
import math
import os
from scipy.optimize import leastsq
import matplotlib.pyplot as plt 
from scipy import  stats
import statsmodels.api as sm
#from  FFTModel import FFTPredict
from scipy.stats.stats import pearsonr
from statsmodels.stats.diagnostic import acorr_ljungbox
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import explained_variance_score
class ModifiedGreyForecastModel:
    def __init__(self,periods):
        self.changeRate = None
        self.periods = periods
        self.predictSeris = np.zeros(1440)
        
    def getAGO(self,x_0):
        data_volume = len(x_0)# if the dtype of x_0 is numpy, transform it into list fro simplifying the computation
        x_1 = []
        for i in range(data_volume):
            temp = 0
            k = 0
            while k<=i:
                temp+=x_0[k] # accumate the data
                k+=1
            x_1.append(temp)
        return np.array(x_1)
    
    '''get the coefficients a and b of the grey model'''
    def func(self,p,x):
        a,b = p
        return -a*x+b
    def error(self,p,x,y):
        return self.func(p,x)-y
    
    def coefficientAandB(self):
        z = np.zeros(self.n)
        for i in range(1,self.n):
            #temp = 0.5*self.
            z[i] = (self.x_1[i]+self.x_1[i-1])/2
            
        # create the matirx U
        U_max = []
        for j in range(0,self.n-1):
            U_max.append([-z[j],1])
        y = self.x_0[1:]
        x = z[1:]
        p0 = [5,5]   
        Para = leastsq(self.error,p0,args=(x,y))
        return Para
    
    
    #利用最小二乘法求解残差中的系数
    def caculPforFResidual(self):
        #构造x
        T = self.periods-1#T
        z = int((self.periods-1)/2)-1
        n = self.periods
        P = np.ones((z*2+1)*(self.periods-1)).reshape(n-1,z*2+1)/2       
        for row in range(n-1):
            collum = 1
            for k in range(1,z+1):
                P[row][collum] = math.cos((row+2)*2*math.pi*k/T)
                P[row][collum+1] = math.sin((row+2)*2*math.pi*k/T)             
                collum+=2
        return P
        
#==============================================================================
#     计算使用傅里叶优化的残差的系数   
#     输入的x_0是上个窗口内实际的并发量,x_p是预测值
#==============================================================================
    def funcForFResidual(self,p,x):
        c = p #c为系数[a0,a1,b1,a2,b2,...,az,bz]
        result = np.array(x).dot(c.T)
        
        return  result
    def errorForFResidual(self,p,x,y):
        return self.funcForFResidual(p,x)-y
        
    def caculCoffofFResidual(self,x_0,x_p):
        #获得残差
        x_r = x_0-x_p
        y = x_r[1:]
        x = self.caculPforFResidual()
        p0 = np.ones((int((self.periods-1)/2)-1)*2+1)
        coff = leastsq(self.errorForFResidual,p0,args = (x,y))[0]
        #print("the length of coff is",len(coff))
        return np.array(coff)
   
    def predictGMValue(self,x_0):
        
        n = len(x_0)#the volume of training data,and it must be more than or equal to 4
        if n<4:
            print("training data is less than 4 that can not meet the model's minimun demand")
            return 
        self.n = n
        self.x_0 = x_0
        self.x_1 = self.getAGO(self.x_0)#get the "one time accumated generating operation"
        #print(self.x_1)
        
        Para = self.coefficientAandB()
        a = Para[0][0]
        b = Para[0][1]
        predict = (1-math.exp(a))*(self.x_0[0]-b/a)*math.exp(-a*self.n)        
        return predict
    
#==============================================================================
#     利用傅里叶变化处理残差，以提高预测精度
#==============================================================================
    def predictFFGMValue(self,x_0,x_p,t):
        n = len(x_0)#the volume of training data,and it must be more than or equal to 4
        if n<4:
            print("training data is less than 4 that can not meet the model's minimun demand")
            return 
        self.n = n
        self.x_0 = x_0
        self.x_1 = self.getAGO(self.x_0)#get the "one time accumated generating operation"
        #print(self.x_1)
        
        Para = self.coefficientAandB()
        a = Para[0][0]
        b = Para[0][1]
        predict = (1-math.exp(a))*(self.x_0[0]-b/a)*math.exp(-a*self.n)    
        #获取残差
        x_p = x_p[t-self.periods:t]
        coff = self.caculCoffofFResidual(x_0,x_p)
        z = int((n-1)/2-1)
        T  = self.periods - 1
        resi = [1/2] 
        for i in range(1,z+1):
            a = math.cos(2*(self.periods+1)*math.pi/T)
            b = math.sin(2*(self.periods+1)*math.pi/T)
            resi.append(a)
            resi.append(b)
        resi = np.array(resi).dot(coff.T)
        #print("residual is",resi)
        if t == 10:
            #分析periods+1的情况
            resi = 0
            
        return predict,predict-resi
        
        
    def predictMGMValue(self,x_0,t):
        
        n = len(x_0)#the volume of training data,and it must be more than or equal to 4
        if n<4:
            print("training data is less than 4 that can not meet the model's minimun demand")
            return 
        self.n = n
        self.x_0 = x_0
        self.x_1 = self.getAGO(self.x_0)#get the "one time accumated generating operation"
        #print(self.x_1)
        
        Para = self.coefficientAandB()
        a = Para[0][0]
        b = Para[0][1]
        predict = (1-math.exp(a))*(self.x_0[0]-b/a)*math.exp(-a*self.n)
        
        CR = (1+self.changeRate[t-1])*x_0[len(x_0)-1]
        
        if CR>predict:
            predict = CR
        return predict    
    def predictFGMValue(self,x_0):
        
        n = len(x_0)#the volume of training data,and it must be more than or equal to 4
        if n<4:
            print("training data is less than 4 that can not meet the model's minimun demand")
            return 
        self.n = n
        self.x_0 = x_0
        self.x_1 = self.getAGO(self.x_0)#get the "one time accumated generating operation"
        #print(self.x_1)
        
        Para = self.coefficientAandB()
        a = Para[0][0]
        b = Para[0][1]
        predict = (1-math.exp(a))*(self.x_0[0]-b/a)*math.exp(-a*self.n)
        F = 1.2
        predict*=F
        return predict
        
    def predictRGMValue(self,x_0,t,predictSeris):
        
        n = len(x_0)#the volume of training data,and it must be more than or equal to 4
        if n<4:
            print("training data is less than 4 that can not meet the model's minimun demand")
            return 
        self.n = n
        self.x_0 = x_0
        self.x_1 = self.getAGO(self.x_0)#get the "one time accumated generating operation"
        
        Para = self.coefficientAandB()
        a = Para[0][0]
        b = Para[0][1]
        #预测的是t时刻的并发量
        predict = (1-math.exp(a))*(self.x_0[0]-b/a)*math.exp(-a*self.n)
        #计算t时刻前,窗口大小为periods的残差均值
        start = t-self.periods      
        residual = np.sum(predictSeris[start:t]-x_0)/self.periods
        predict+=residual
        return predict  
    def predictMRGMValue(self,x_0,t,predictSeris):
        
        n = len(x_0)#the volume of training data,and it must be more than or equal to 4
        if n<4:
            print("training data is less than 4 that can not meet the model's minimun demand")
            return 
        self.n = n
        self.x_0 = x_0
        self.x_1 = self.getAGO(self.x_0)#get the "one time accumated generating operation"
        
        Para = self.coefficientAandB()
        a = Para[0][0]
        b = Para[0][1]
        #预测的是t时刻的并发量
        predict = (1-math.exp(a))*(self.x_0[0]-b/a)*math.exp(-a*self.n)
        #计算t时刻前,窗口大小为periods的残差均值
        start = t-self.periods      
        residual = (predictSeris[start:t]-x_0)
        for i in range(self.periods):
            if residual[i]>0:
                residual[i] = 0
            else:
                residual[i]*=-1
        residual = np.sum(residual)/self.periods
        predict+=residual
        return predict       
        
        
    def learnChangeRate(self,day):
        wrFile = WRFile()
        day = int(day)
        windows = 3
        part0 = "F:\\one\\predict\\traindata/workload"
        part1 = "inmin.xlsx"
        
        if day <=53:
            data = wrFile.readDataFromExcel(part0+str(53)+part1)
            self.changeRate = np.zeros(len(data)-1)
        elif day>53:
            if (day-windows)<53:
                windows = day-53+1
            else:
                windows+=1
            cr = np.zeros(1440-1)
            #print("day is",day,"windows is",windows)
            
            for i in range(1,windows):
                data = wrFile.readDataFromExcel(part0+str(day-i)+part1)
                cr += np.diff(data)/data[:len(data)-1]
            self.changeRate = cr/(windows-1)
            #print("windows is",windows-1)
        #plt.plot(np.arange(len(self.changeRate)),self.changeRate)
            