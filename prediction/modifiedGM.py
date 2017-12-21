# -*- coding: utf-8 -*-
"""
Created on Sat Feb 25 08:43:58 2017

@author: User
"""
import sys
sys.path.append("D:/anaconda/project/")
import numpy as np
from utils import WRFile
import math
import os
from scipy.optimize import leastsq
import matplotlib.pyplot as plt 
import matplotlib
from scipy import  stats
import statsmodels.api as sm
#from  FFTModel import FFTPredict
from scipy.stats.stats import pearsonr
from statsmodels.stats.diagnostic import acorr_ljungbox
from sklearn.metrics import mean_absolute_error
from sklearn.metrics import explained_variance_score
import timeit
import pandas as pd
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签 
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
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
        #print("AGO后的值",x_1)
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
        #print("系数",Para)
        return Para
    
    
    
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
   
    def predictGMValue(self,x_0,t):
        
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
        return math.ceil(predict)
    
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
        predictSeris = np.array(predictSeris)
        x_0 = np.array(x_0)
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
        #print("预测值",predict)
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
        #print("day---->",day)
        day = int(day)
        windows = 3
        part0 = "F:\\FIFA\\predict\\traindata/inmin/workload"
        part1 = "inmin.xlsx"
        
        if day <=53:
            data = wrFile.readDataFromExcel(part0+str(53)+part1)
            #print("filepath--->",part0+str(53)+part1,"len()---->",len(data))
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
            
#==============================================================================
#     分析过预测和不足预测的相关统计量
#==============================================================================
def analyzeUnderandOver(data,predict,Under = True):
    #data = data[3:]
    original = data
    dis = (predict-data)/data*100
    #首先获取过分配的部分
   # equal = np.where(dis==0)[0]
    if Under:
        index = np.where(dis<0)[0]
        sym = -1
    else:
        index = np.where(dis>0)[0]
        sym = 1
    count = len(index)#过分配的个数
    data = []
    print("count is ",count)
    for i in range(0,count):
        data.append(sym*dis[index[i]])#过分配的数量   
    del dis  #释放空间
    if len(data)==0:
        print("return none")
        stats_res = {"ratio":0,"mean":0,"median":0,"Q1":0,"Q3":0,"95th":0,"max":0,"min":0}
        #return stats_res
    '''stats_res = {"ratio":float("%.5f"%float(count/len(predict))),"mean":float("%.5f"% float(np.mean(data))),"median":float("%.5f"%float(np.median(data))),
    "Q1":float("%.5f"%np.percentile(data,25)),"Q3":float("%.5f"%np.percentile(data,75)),
    "95th":float("%.5f"%np.percentile(data,95)),"max":float("%.5f"%np.max(data)),"min":float("%.5f"%np.min(data)),"scale":float("%.5f"%(np.max(data)/np.max(original)))}
    '''
    stats_res = {"ratio":float("%.5f"%float(count/len(predict))),"mean":float("%.5f"% float(np.mean(data))),"max":float("%.5f"%np.max(data))}
    #print(stats_res)
    return stats_res 
#==============================================================================
#     分别分析每天的预测精度，采用的分析方法是explained_variance 和 MAE
#==============================================================================
def analyzePrecision():
    fileList = ["RGM/","FGM/","FFGM/","GM/","MGM/","MRGM/"]
    part0 = "F:\\one\\predict\\"
    part1 = ".xlsx"
    
    part2 = "F:\\one\\predict\\traindata/workload"
    part3 = "inmin.xlsx"
    
    wrFile = WRFile()
    k = 0
    title = ["MAE","EVS"]
    rows = 9
    cols = 3
    while k<6:
        result = []
        for day in range(53,61):
            data = wrFile.readDataFromExcel(filePath = part2+str(day)+part3)
            predict = wrFile.readDataFromExcel(filePath = part0+fileList[k]+"wc"+str(day)+part1)
            MAE = mean_absolute_error(y_true = data, y_pred = predict)
            EVS =explained_variance_score(y_true = data, y_pred = predict)
            result.append({"MAE":MAE,"EVS":EVS})
        
        wrFile.writeDictIntoTable(data = result,filePath= part0+fileList[k]+"precision.docx" ,title = title ,cols = cols,rows = rows)
        k+=1
    #return result
    
def testMGM():
    periods = 5
    grey = ModifiedGreyForecastModel(periods)
    day = 55
    wrFile = WRFile()
    #data = wrFile.readDataFromExcel(filePath = "F:\\FIFA\\predict\\traindata/inmin/workload"+str(day)+"inmin.xlsx",sheet_name = "1")
    data = [22, 20, 19, 21, 22, 19, 22, 20, 38, 15, 20, 20, 22, 22, 22, 21, 21, 19, 20, 22, 22, 19, 20, 22, 19, 22, 20, 22, 19, 19]
    predict = []
    predictf = []
    for k in range(0,periods):
        predict.append(data[k])
        predictf.append(data[k])
    MGM_predict = False
    if MGM_predict:
        grey.learnChangeRate(day = day)    
    for i in range(periods,len(data)):
        #we set n as 4
        x = data[i-periods:i]
        #predict.append(grey.predictFGMValue(x)) #使用固定倍数进行预测
        #predict.append(grey.predictRGMValue(x,i,predict)) #使用残差序列和进行预测
        #predict.append(grey.predictMGMValue(x,i))# 要预测第i时刻的并发量
        #predict.append(grey.predictGMValue(x,i))
        predict.append(math.ceil(grey.predictMRGMValue(x,i,predict)))
        #result = grey.predictFFGMValue(x,predict,i)
    #wrFile.writeDataIntoExcel(data = predict,filePath = "F:\\FIFA\\predict\\MGM/test.xlsx")
    return predict
def getWorkloadsChangeRate():
    wrFile = WRFile()
    result = []
    plt.ylabel("change rate")
    plt.xlabel("time in minutes")
    plt.title("workloads change rate from day 53 to 60")
    for day in range(53,61):
        result.extend(wrFile.getChangeRate(day = day))
    plt.plot(np.arange(0,len(result)),result)
    #plt.legend(["53","54","55","56"])
def plotData(method):
   wrFile = WRFile()
   data_filePath = "F:\\FIFA\\predict\\traindata/day53_60inmin.xlsx"
   data = wrFile.readDataFromExcel(filePath = data_filePath)

   predict_filePath = "F:\\FIFA\\predict\\"+method+"/wc53_60.xlsx"
   if method=="lr":
       method = "LinearRegression"
   elif method=="gbdt":
       method = "Gradient Boosting Decision Tree"
   elif method=="svr_lr":
       method = "Support Vector Regression-linear"
   elif method=="svr_rbf":
       method = "Support Vector Regression-rbf"       
   predict = np.floor(np.array(wrFile.readDataFromExcel(filePath = predict_filePath)))
   plt.plot(np.arange(len(data)),data,"m",LineWidth=2)
   plt.plot(np.arange(len(predict)),predict,"g",LineWidth=2)
   plt.title("prediction results of "+method,fontsize = 20)
   plt.xlabel("time(minute)",fontsize= 18)
   plt.ylabel("workload(times)",fontsize=18)
   plt.legend(["real","predict"],loc = "upper left",fontsize=18)
   
def analyzeTimeit():
    number = 1
    t1 = timeit.repeat(stmt = testMGM,repeat = 3,number = number)
    print(np.round(np.array(t1),3))
def analyzePredictionPrecision():
    objFileName = "svr_rbf"
    precision = []# 列表头分别为 ratio,max,mean
    wrFile = WRFile()
    objFilePath = "F:\\FIFA\\predict\\"+objFileName+"/precision_over.xlsx"
    predict = wrFile.readDataFromExcel(objFilePath,min_cols = 1,max_cols = 3)
    predict = predict.reshape(3,8)
    result = [np.average(predict[0]),np.average(predict[1]),np.average(predict[2])]
    wrFile.writeDataIntoExcel(data = result,filePath = "F:\\FIFA\\predict\\"+objFileName+"/precision_over_evaluate.xlsx" )
def anaylzeDelayDistribution():
    wrFile = WRFile()
    #process_type = "SQ"
    filePath_head = "D:\\cloudsim\\log\\"+process_type+"_q"+"/"+process_type+"_q"
    QL_delay_result =[]
    for QL in [55,60,66,70,75]:#以文件为单位进行分析
        delay_result = np.zeros(6)
        filePath = filePath_head+str(QL)+"/Cloudlet/"+process_type+"53cloudlet.xlsx"
        print(filePath)
        delay = wrFile.readDataFromExcel(filePath = filePath,sheet_name = "sheet",min_cols = 9,max_cols = 9)
        for element in delay: #分析每个请求的延迟情况
            if element==-1:
                continue
            elif element<=0.11:
                delay_result[0]+=1
            elif element<=0.22:
                delay_result[1]+=1
            elif element<=0.33:
                delay_result[2]+=1            
            elif element<=0.44:
                delay_result[3]+=1  
            elif element<=0.55:
                delay_result[4]+=1  
            else:
                delay_result[5]+=1         
        delay_result[0] = round(1.0*delay_result[0]/len(delay),3)
        delay_result[1] = round(1.0*delay_result[1]/len(delay),3)
        delay_result[2] = round(1.0*delay_result[2]/len(delay),3)
        delay_result[3] = round(1.0*delay_result[3]/len(delay),3)
        delay_result[4] = round(1.0*delay_result[4]/len(delay),3)
        delay_result[5] = round(1.0*delay_result[5]/len(delay),3)
        delay_result = delay_result.tolist()
        QL_delay_result.append(delay_result)
    return QL_delay_result
'''wrFile = WRFile()
process_type = "ATBM"
data = anaylzeDelayDistribution()
wrFile.writeDataIntoExcel(data =  data,filePath ="D:\\cloudsim\\log\\"+process_type+"_q"+"/"+process_type+"_delay_distribution.xlsx" )
'''
wrFile = WRFile()
predict_type="lr"
data = wrFile.readDataFromExcel(filePath="F:\\FIFA\\final\\inmin/workload53_60inmin.xlsx")
predict = wrFile.readDataFromExcel(filePath="F:\\FIFA\\predict\\"+predict_type+"/wc53_60.xlsx")
plt.plot(np.arange(len(data)),data,"k")
plt.plot(np.arange(len(data)),predict,"wo")
plt.legend(["real","predict"],fontsize=16,loc="upper left")
plt.title("prediction results of "+predict_type,fontsize=20)
plt.xlabel("time(minute)",fontsize=18)
plt.xticks(fontsize = 16)
plt.ylabel("workloads",fontsize=18)
plt.yticks(fontsize = 16)
plt.savefig("E:\\"+ u"日常工作"+"\\"+u"下一代计算机技术"+"\\"+u"重要照片"+"\\"+u"各类算法的预测结果"+"/"+predict_type+".jpeg")
