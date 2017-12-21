# -*- coding: utf-8 -*-
"""
Created on Tue Jul 12 15:06:51 2016

@author: wj
"""
import numpy
import matplotlib.pyplot as plt
import xlrd
import math
import random
def caculCorrelation(X,Y):
   X_mean = numpy.mean(X)
   Y_mean = numpy.mean(Y)
   N = len(X)
   result = 0
   temp_sum = 0
   for i in range(0,len(X)):
       temp_sum = temp_sum+(X[i]-X_mean)*(Y[i]-Y_mean)
   result = temp_sum/(N*math.sqrt(numpy.var(X))*math.sqrt(numpy.var(Y)))
   return result  
#计算order阶差分
'''
--------------------------------------------------
result[0:order-1]都是无效数据0
order是指定的阶数
--------------------------------------------------
''' 
def caculDifference(data,order):
    temp_result = numpy.array(data)#对原始数据进行复制，不可对其修改
    result = numpy.zeros(len(data))
    for j in range(0,order):  
        for i in range(0,len(data)):
            if i<=j:
                result[i] = 0
                continue
            result[i] = temp_result[i]-temp_result[i-1]
        temp_result = result[:]
    return result
    
def caculTestDif(data):
    temp_result = numpy.array(data)
    result = numpy.zeros(len(data))  
    for i in range(0,len(data)):
        if i== 0:
            continue
        result[i] = (temp_result[i]-temp_result[i-1])
    return result
'''

--------------------------------------------------
对数据进行归一化处理，处理方法如下
(data_cur-data_min)/(data_max-data_min)
--------------------------------------------------
'''    
def normalization_IDC(data):
    print(len(data))
    result = []
    data = numpy.array(data)
    '''设定阈值，采用3sigma原则'''
    for i in range(0,len(data)):
        if i==0:
            result.append(0)
            continue
        temp = data[0:i+1]
        temp = numpy.array(temp)
        result.append(20*(data[i]-numpy.min(temp))/(numpy.max(temp)-numpy.min(temp)))
        mean = numpy.mean(temp)
        var = math.sqrt(numpy.var(temp))
        threshold = mean+3*var
        if data[i]>threshold:
            data[i] = 0
    return result
def normalization(data):
    print(len(data))
    result = []
    data = numpy.array(data)
    '''设定阈值，采用3sigma原则'''
    for i in range(0,len(data)):
        if i==0:
            result.append(0)
            continue
        temp = data[0:i+1]
        temp = numpy.array(temp)
        result.append((data[i]-numpy.min(temp))/(numpy.max(temp)-numpy.min(temp)))
    return result
def writeData():
    file_path 
    
#设定指定阈值，作为当前的归一化分布，但是阈值的选择是难点
def caculIDC_normalB(data):
    threth = 0.0001
    idc_prior = 0
    idc_data = numpy.zeros(len(data))
    idc_cur = 0
    cal_start = 0
    for i in range(0,len(data)):
        if i==0:
            continue
        mean = numpy.mean(data[cal_start:i+1])
        var= numpy.var(data[cal_start:i+1])
        idc_cur = var/mean
        if(abs(idc_cur-idc_prior)<threth):
            print("第i个位数idc收敛",i,"idc的收敛值为",idc_cur)
        idc_data[i]=idc_cur
        idc_prior = idc_cur
    #print("原始数据",numpy.array(idc_data))
    firstOrderDif = caculDifference(idc_data,1)
    #print("一阶差分",firstOrderDif)
    
    #归一化处理
    firstOrderDif = normalization_IDC(firstOrderDif)
    data_normal = normalization(data)
    #print("原始数据",data)
    #print("原始数据归一化处理",len(data_normal))
    #计算相关系数
    #print("idc的差分结果和原始数据的相关系数为",caculCorrelation(idc_data,data))
    
    #显示结果
    plt.title("IDC[1] is shown by blue,and data is painted in red")
    plot_dif1 = plt.plot(range(3,len(data)),firstOrderDif[3:len(data)],"b")
    #plot_data_normal = plt.plot(range(3,len(data)),data_normal[3:len(data)],"g")
    plot_data = plt.plot(range(3,len(data)),data[3:len(data)],"r")
    
    
    
    
#将当前计算得到的idc_max作为归一化分母，计算效果不理想
def caculIDC_normalA():
    
    threth = 0.0001
    data = [97, 94, 85, 90, 85, 94, 86, 91, 95, 87, 
            96, 89, 86, 99, 85, 100, 93, 94, 100, 98,
            88, 93, 99, 91, 94, 94, 88, 86, 94, 86, 88,
            89, 96, 100, 99, 100, 93, 92, 99, 96, 85, 88, 
            100, 99, 88, 94, 98, 91, 88, 95, 102, 107, 101, 110, 107, 111, 112, 113, 116, 125, 123, 126, 141,
            138, 132, 136, 148, 142, 154, 149, 151, 161, 167, 171, 171, 173, 174, 181, 186, 190, 90, 92, 97, 86, 95, 89, 90, 87, 86, 88, 92, 88, 94, 100, 99, 93, 96, 91, 91, 95, 88, 94, 85, 86, 86, 97, 98, 87, 85, 93, 88, 93, 85, 94, 100, 89, 89, 95, 90, 87, 85, 86, 86, 96, 86, 87, 98, 95, 93, 95, 100, 89, 92, 92, 88, 91, 96, 95, 86, 86, 100, 85, 90, 89, 91, 99, 100, 90, 98, 100, 100, 104, 99, 106, 111, 112, 118, 117, 115, 121, 125, 129, 131, 119, 128, 129, 138, 142, 132, 140, 139, 148, 148, 144, 147, 158, 150, 158, 153, 155, 96, 86, 86, 99, 95, 87, 93, 99, 97, 92, 92, 87, 88, 88, 92, 86, 96, 85, 99, 100]
    
    #data =  dataPreprocess()
    print(len(data))
    idc_prior = 0
    idc_data = []
    idc_max = 0
    idc_min = 0
    idc_cur = 0
    for i in range(80,len(data)):
        if i==0:
            idc_data.append(0)
            continue
        mean = numpy.mean(data[0:i])
        var= numpy.var(data[0:i])
        idc_cur = var/mean
        
        #确定最大最小值
        if(idc_cur>idc_max):
            idc_max = idc_cur
        if(idc_cur<idc_min):
            idc_min = idc_cur
        #进行归一化处理
        idc_cur = (idc_cur-idc_min)/(idc_max-idc_min)
        if(abs(idc_cur-idc_prior)<threth):
            print("第i个位数idc收敛",i,"idc的收敛值为",idc_cur)
        idc_data.append(idc_cur*100)  
        idc_prior = idc_cur
    
    plt.plot(range(0,len(idc_data)),idc_data)
    plt.plot(range(0,len(data)),data)
    plt.show()
'''createBurstyData(num,data,times,intensity)'''
data = [0,]
data = createBurstyData(200,data,20,20)
caculIDC_normalB(data)

