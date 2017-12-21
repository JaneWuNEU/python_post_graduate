# -*- coding: utf-8 -*-
"""
Created on Thu Feb 16 10:33:36 2017

@author: User
"""
import numpy as np
import matplotlib.pyplot as plt 
import sys
sys.path.append("D:/anaconda/project/utils")
from utils import WRFile
from scipy.stats.stats import pearsonr
import scipy.fftpack as fft
import pandas as pd

'''设置初始的数据值'''
fileStart = "F:\\one\\final\\inmin/knots/workload"
fileEnd = "inmin_knots.xlsx"
wrFile = WRFile()
data51 = wrFile.readDataFromExcel(filePath = fileStart+"51"+fileEnd)
data52 = wrFile.readDataFromExcel(filePath = fileStart+"52"+fileEnd)     
data53 = wrFile.readDataFromExcel(filePath = fileStart+"53"+fileEnd)
data54 = wrFile.readDataFromExcel(filePath = fileStart+"54"+fileEnd)
data_volume = len(data51)
x = np.arange(0,data_volume)

def useAverage(dataA = data51,dataB = data52,dataC = data53):
    predict = (dataA+dataB)/2
    #plt.plot(x,predict)
    #plt.plot(x,dataC)
    #plt.legend(["p_w","r_w"])
    #plt.title("use average of dataA and dataB")
    presicion = pearsonr(predict.real,dataC)
    return [predict,presicion]
    
def findBurstEnd(freqA,freqB):
    
    corr_imag = pearsonr(freqA.imag,freqB.imag)
    corr_real = pearsonr(freqA.real,freqB.real)
    total_corr = (corr_imag[0]+corr_real[0])/2
    data_volume = len(freqA)
    
    print("thredhold-> ",total_corr)
    
    thredHold = 0.95
    if total_corr>thredHold:
        end = 1
    else:
        percent = 0.2
        end = int(data_volume/2)
        while True:
            '''
            corr_imag = pearsonr(freqA.imag[0:end],freqB.imag[0:end])
            corr_real = pearsonr(freqA.real[0:end],freqB.real[0:end])
            corr_f = (corr_imag[0]+corr_real[0])/2
            print("former p_value",corr_f)
            '''
            corr_imag = pearsonr(freqA.imag[end:],freqB.imag[end:])
            corr_real = pearsonr(freqA.real[end:],freqB.real[end:])
            corr_l = (corr_imag[0]+corr_real[0])/2
            
            #print("latter p_value",corr_l)
                         
            if corr_l>total_corr:
                end = int(data_volume-end/2)
            else:
                break
    return end 
    
    

def FFTofHFiB(dataA = data51,dataB = data52,dataC = data53):
    #对数据进行FFT转换
    freqA = np.fft.fft(dataA)
    freqB = np.fft.fft(dataB) 
    middle = len(dataA)/2
    #获取突发的终止点
    end = findBurstEnd(freqA,freqB)
    print("HFiB   ",end)
    #使用频率更高的部分进行预测，这样过分配的可能性增大
    for i in range(end,data_volume):
        if freqB[i]<freqA[i]:
            freqB[i] = freqA[i] 
    freqB[:end] = (freqA[:end]+freqB[:end])/2
    predict = np.fft.ifft(freqB)
    '''
    plt.plot(x,predict)
    plt.plot(x,dataC)
    plt.legend(["p_w","r_w"])
    plt.title("use higher frequency of workload period")
    print("预测精度",pearsonr(predict.real,dataC))
    '''
    presicion = pearsonr(predict.real,dataC)
    return [predict,presicion]
    
def FFTofWFD(dataA = data51,dataB = data52,dataC = data53):
    #对数据进行FFT转换
    freqA = np.fft.fft(dataA)
    freqB = np.fft.fft(dataB) 
    #获取突发的终止点
    end = findBurstEnd(freqA,freqB)

    factor = 0.8
    freqB[end:data_volume] = (1-factor)*freqA[end:data_volume]+factor*freqB[end:data_volume]
    freqB[:end] = (freqA[:end]+freqB[:end])/2
    predict = np.fft.ifft(freqB)
    '''
    plt.plot(x,predict)
    plt.plot(x,dataC)
    plt.legend(["p_w","r_w"])
    plt.title("use weight factor of workload period")
    print("预测精度",pearsonr(predict.real,dataC))
    '''
    presicion = pearsonr(predict.real,dataC)
    return [predict,presicion]
def showData():
    
    data = wrFile.readDataFromExcel(filePath = "F:\\one\\final\\inmin\\knots/workload51_70inmin_knots.xlsx")
    amp = wrFile.readDataFromExcel(filePath = "F:\\one\\final\\inmin\\knots\\amplitude/amp51_70.xlsx")
     
    x = np.arange(0,len(amp))
    plt.plot(x,data)
    plt.plot(x,amp)
    fileList = ["amplitude","real_workload"]
    plt.legend(fileList)
    plt.grid(True)
    plt.title("amplitude of day 51 to 70")


'''使用更大的数据集进行测试，记录预测结果及分析精度'''
def trainData():
    
    firstFile = 51
    i = firstFile 
    pre_file = "F:/one/predict/"
    dataA = wrFile.readDataFromExcel(fileStart+str(i)+fileEnd)
    dataB = wrFile.readDataFromExcel(fileStart+str(i+1)+fileEnd)
    
    file_volume = 18
    pre_HFiB_list= []
    precision_avg =  np.zeros(file_volume)
    precision_HFiB =  np.zeros(file_volume)
    precision_WFD =  np.zeros(file_volume)
    rows = 0
    while i <(firstFile+file_volume):
        dataC = wrFile.readDataFromExcel(fileStart+str(i+2)+fileEnd)
        #pre_avg = useAverage(dataA = dataA,dataB = dataB,dataC = dataC)
        print("day is ",i)
        pre_HFiB = FFTofHFiB(dataA = dataA,dataB = dataB,dataC = dataC)
        print(pre_HFiB[1][0])
        #pre_WFD = FFTofWFD(dataA = dataA,dataB = dataB,dataC = dataC)
        #pre_HFiB_list.append(pre_HFiB[0])
        #将预测结果写入文件
        '''
        wrFile.writeDataIntoExcel(filePath = pre_file+"average/wc"+str(i+2)+".xlsx",data = pre_avg[0].real )
        wrFile.writeDataIntoExcel(filePath = pre_file+"HFiB/wc"+str(i+2)+".xlsx",data = pre_HFiB[0].real )
        wrFile.writeDataIntoExcel(filePath = pre_file+"WFD/wc"+str(i+2)+".xlsx",data = pre_WFD[0].real)
        
        #记录预测精度
        precision_avg[rows] = pre_avg[1][0]
        precision_HFiB[rows] =pre_HFiB[1][0]
        precision_WFD[rows] =pre_WFD[1][0]
        '''
        rows +=1
        i+=1
        del dataA
        dataA = dataB
        dataB = dataC
    #将预测精度写入文件中
    '''
    wrFile.writeDataIntoExcel(filePath = pre_file+"average/precision.xlsx",data = precision_avg)
    wrFile.writeDataIntoExcel(filePath = pre_file+"HFiB/precision.xlsx",data = precision_HFiB)
    wrFile.writeDataIntoExcel(filePath = pre_file+"WFD/precision.xlsx",data = precision_WFD)
    '''
    #data_real = wrFile.readDataFromExcel(filePath = "F:/one/predict/traindata/wc53_70inmin_knots.xlsx")
    #plt.plot(x,data_real)
    #plt.plot(x,pre_average)
    #plt.plot(np.arange(len(data_real)),pre_HFiB_list)
    #plt.grid(True)
    #plt.plot(x,pre_WFD)

def getAmplitude(filePath ):
    data = wrFile.readDataFromExcel(filePath = filePath)
    freq = np.fft.fft(data)
    a = freq.real
    b = freq.imag
    Amp = 2*np.sqrt(a*a+b*b)/len(freq)
    Amp[0]*=2
    return Amp
def analyzeAmplitude():
    firstFile = 69
    i = firstFile 
    pre_file = "F:\\one\\final\\inmin\\knots"
    file_volume = 2
    
    while i <(firstFile+file_volume):
        filePath = pre_file+"/workload"+str(i)+"inmin_knots.xlsx"
        Amp = getAmplitude(filePath )
        wrFile.writeDataIntoExcel(filePath = pre_file+"/amp"+str(i)+".xlsx",data = Amp )
        i+=1
def verify2_8():
    file_amp = "F:\\one\\final\\inmin\\knots\\amplitude/amp60.xlsx"
    file_data = "F:\\one\\final\\inmin\\knots\\workload60inmin_knots.xlsx"
    amp = np.array(wrFile.readDataFromExcel(filePath = file_amp))
    iamp = amp[::-1]
    data = wrFile.readDataFromExcel(filePath = file_data)
    
    freq = np.fft.fft(data)
    direct_cur = amp[0]
    data_volume = len(amp)
    bound = int(data_volume*1)
    start = 1
    
    base = np.ones(bound-start)*40000
    fir_80_p = np.fft.ifft(freq[start:bound])
    
    '''
    #las_90_p = np.fft.ifft(freq[bound:])
    x = np.arange(0,len(data))
    plt.plot(x[start:bound],data[start:bound])
    plt.plot(x[start:bound],fir_80_p)
    fileList = ["r_w","p_w"]
    plt.legend(fileList)
    plt.grid(True)
    plt.title("discard freq[1] to predict")
    #first80 = amp[0:bound]#前80
    #second20 = amp[bound:]#后20
    '''
    x = np.arange(0,len(amp))
    print(len(amp),len(iamp))
    #plt.plot(x,amp)
    #plt.plot(x,iamp)
    
    
    #fileList = ["workload","amplitude"]
    #plt.legend(fileList)
    plt.grid(True)
    plt.title("amplitude of day 51")    
    
    
#analyzeAmplitude()
verify2_8()










   