# -*- coding: utf-8 -*-
"""
Created on Sat Feb 18 11:08:16 2017

@author: User
"""
'''this file is the realization of grey prediction model in python'''
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
import plotly.plotly as py
import plotly.graph_objs as go
from  FFTModel import FFTPredict
from scipy.stats.stats import pearsonr
from statsmodels.stats.diagnostic import acorr_ljungbox
class GreyForecastModel:
        
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
    def predictValue(self,x_0):
        
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
def TestGreyModel(periods,filePath):
    grey = GreyForecastModel()
    wrFile = WRFile()
    data = wrFile.readDataFromExcel(filePath = filePath)
    predict = []
    predict[0:periods-1] = data[0:periods-1]
    
    for i in range(periods-1,len(data)):
        #we set n as 4
        x = data[i-(periods-1):i+1]
        #print(x)
        predict.append(grey.predictValue(x))
            
    return [data,predict]
def analyzePredict(data,predict,Under = True):
    #data = data[3:]
    dis = (predict-data)/data*100
    
    #首先获取过分配的部分
    if Under:
        index = np.where(dis<0)[0]
        sym = -1
    else:
        index = np.where(dis>0)[0]
        sym = 1
    count = len(index)#过分配的个数
    data = []
    for i in range(0,count):
        data.append(sym*dis[index[i]])#过分配的数量   
    del dis  #释放空间
     
    #然后进行统计分析
    data = np.array(data)
    stats_res = {"ratio":count/len(predict),"mean":np.mean(data)," medium":np.median(data),
    "1/4th":np.percentile(data,25),"3/4th":np.percentile(data,75),
    "95th":np.percentile(data,95),"max":np.max(data),"min":np.min(data)}
    #print(stats_res)
    return stats_res
        
def plotPredictError():
    filePart0 = ["F:\\one\\predict\\GM/wc","F:\\one\\final\\inmin/workload"]
    wrFile = WRFile()
    filePart1 = [".xlsx","inmin.xlsx"]
    x = []
    x_label = []
    k = 0
    for i in range(53,61):
        predict = wrFile.readDataFromExcel(filePath = filePart0[0]+str(i)+filePart1[0])
        data = wrFile.readDataFromExcel(filePath = filePart0[1]+str(i)+filePart1[1])
        dis = (predict-data)/data*100
        over = []
        under = []
        for j in range(len(dis)):
            if dis[j]>0:
                over.append(dis[j])
            else:
                under.append(-dis[j])
        #x.insert(k,over)
        k+=1
        x.insert(k,under)
        x_label.append(str(i)+"-o")
        #x_label.append(str(i)+"-u")
    
    plt.boxplot(x = x,labels = (53,54,55,56,57,58,59,60),notch=True, patch_artist=True)
    plt.grid(True)
    plt.title("analyze the under-prediction error of Grey Model")
'''
分析并发量的变化率
'''   
def analyzeChangeRateAndPrecition(data,predict):
    changeRateOfW = np.diff(data)/data[:len(data)-1]*100#计算负载的变化率
    precision = (predict-data)/data*100 #计算预测精度
    #precision_wn = acorr_ljungbox(x = precision)[0]
    #print("预测精度",np.min(precision_wn))
    begin = 0
    end = begin+60
    precision = precision[1:]
    k = 0
    p_coefficient = []
    for i in range(24):
        i*=60
        p_coefficient.append(pearsonr(changeRateOfW[i:i+60],precision[i:i+60])[0])
        if p_coefficient[k]>-0.6:
            print("Hour ",k,"P ",p_coefficient[k])
        k+=1
    return  p_coefficient
    '''
    periods = 30
    count = int(len(predict)/periods)
    for i in range(count):
        precision_wn = acorr_ljungbox(x = precision[i:i+periods],lags = 10)[0]
        print("预测精度",np.min(precision_wn))
    '''
    
    #changeRate_wn = acorr_ljungbox(x = changeRateOfW[begin:60*count],lags = 10)[1]
    #precision_wn = acorr_ljungbox(x = precision[begin:60*count],lags = 10)[1]
    #print("并发量变化率",changeRate_wn)
    #print("预测精度",precision_wn)
    
    #我们以120秒为单位分析pearsonr
    #print(len(predict))
    #for i in range(int(len(predict)/120)):
        
    #p = pearsonr(changeRate_wn,precision_wn)
    #print("pearsonr is ", p)
    #return p
    
def analyzePandR():
    filePart0 = ["F:\\one\\predict\\GM/wc","F:\\one\\final\\inmin/workload","F:\\one\\final\inmin\\knots/workload"]
    wrFile = WRFile()
    filePart1 = [".xlsx","inmin.xlsx","inmin_knots.xlsx"]
    p_coefficient = []
    for i in range(53,61):
        predict = wrFile.readDataFromExcel(filePath = filePart0[0]+str(i)+filePart1[0])
        #result = TestGreyModel(periods = 4 ,filePath = filePart0[2]+str(i)+filePart1[2])
        data = wrFile.readDataFromExcel(filePath = filePart0[1]+str(i)+filePart1[1])
        print("day ",i)
        p_coefficient.extend(analyzeChangeRateAndPrecition(data,predict))
        #print("day ",i," p ", p)
        
        
        
def lowPearson():
    filePart0 = ["F:\\one\\predict\\GM/wc","F:\\one\\final\\inmin/workload","F:\\one\\final\inmin\\knots/workload"]
    wrFile = WRFile()
    filePart1 = [".xlsx","inmin.xlsx","inmin_knots.xlsx"]
    Hours = [[15,17,19,21],[15,17,21],[17],[14,22],[14,22],[17,19,22],[14,15,16,20,22],[14,16,21]]
    CRinLowP = []
    PRinLowP = []
    x = []
    DatainLowP = np.zeros(60*8*24)
    PredinLowP = np.zeros(60*8*24)
    for i in range(53,61):
        day = i-53
        predict = wrFile.readDataFromExcel(filePath = filePart0[0]+str(i)+filePart1[0])
        data = wrFile.readDataFromExcel(filePath = filePart0[1]+str(i)+filePart1[1])
        CR = np.diff(data)/data[:len(data)-1]*100#计算负载的变化率
        PR = (predict-data)/data*100 #计算预测精度
        PR = PR[1:]
        
        #定位到指定时刻
        h = 0
        while h<len(Hours[day]):
            time = (Hours[day])[h]*60
            CRinLowP.extend(CR[time:time+60])
            PRinLowP.extend(PR[time:time+60])
            #DatainLowP[time:time+60] = data[time:time+60]
            #PredinLowP[day*60*24+time:day*60*24+time+60] = predict[time:time+60]
            
            for minu in range(60):
                x.append(str(i)+"-"+str((Hours[day])[h])+":"+str(minu))
            h+=1

    plt.plot(np.arange(len(CRinLowP)),CRinLowP,"m-")
    plt.plot(np.arange(len(PRinLowP)),PRinLowP,"g*")
    #plt.plot(x,DatainLowP)
    #plt.plot(x,PredinLowP)
    plt.legend(["CR","PR"])
    plt.grid(True)
    plt.title("changement rate of workloads and prediction precision within low Pearson")
    return PredinLowP
    '''
    plt.plot(np.arange(len(DatainLowP)),DatainLowP,"m*-")
    plt.plot(np.arange(len(PredinLowP)),PredinLowP,"g*-")
    plt.legend(["r_w","p_w"])
    plt.grid(True)
    
    
    plt.plot(np.arange(len(PRinLowP)),PRinLowP)
    plt.legend(["precision"])
    plt.grid(True)
    plt.title("prediction precision within low Pearson")
    '''
def compareModel():
    fileStart = "F:\\one\\final\\inmin/workload"
    fileEnd = "inmin.xlsx"
    wrFile = WRFile()

    #fft = FFTPredict()
    #noBurst_pre = fft.FFTofNoBurst(data51 , data52 )
    #WFD_pre = fft.FFTofWFD(data51 , data52 )
    periods = 10
    for i in range(53,61):
        result = TestGreyModel(periods,filePath = fileStart+str(i)+fileEnd)
        predict = result[1]
        print(i)
        wrFile.writeDataIntoExcel(data = predict,filePath = "F:/one/predict/GM/wc"+str(i)+".xlsx")

#compareModel()

wrFile = WRFile()
#predict = wrFile.readDataFromExcel("F:\\one\\predict\\GM/wc53_60.xlsx")
data = wrFile.readDataFromExcel("F:\\one\\predict\\traindata/workload54inmin.xlsx")
predict =  wrFile.readDataFromExcel("F:\\one\\predict\\GM/wc54.xlsx")
plt.plot(np.arange(len(data)),data)
plt.plot(np.arange(len(predict)),predict)
plt.legend(["r-w","p-w"])
plt.title("prediction result for day 54 by GM ")















         
            
        