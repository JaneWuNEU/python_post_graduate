# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 20:10:20 2016

@author: User
"""
import sys
import numpy
import math
sys.path.append("D:/anaconda/project/utils")
from utils import WRFile
from memory_profiler import profile
class AnalyseIDC:
   
    def  __init__(self,filePath):
        wrFile = WRFile()
        self.data = numpy.array(wrFile.readDataFromExcel(filePath = filePath,cols = 1))
    #计算order阶差分
    burstThreshold = 0.6
    idc1Weight = 0.8
    idcWeight = 0.2
    def caculIDC(self):
        data = self.data
        timeIncrement = 60*40
        
        num = len(data)
        idc_data = numpy.zeros(num)
        start = 0
        J = 0
        thresh = 0.8
        tol=thresh+0.1
        Y = [1,]
        end = 0
        while end!=num:
            while tol>thresh:
                begin = J*timeIncrement
                end = (J+1)*timeIncrement
                if end>num:
                    end = num
                day_begin = max(end-60*60,0)
                m = numpy.mean(data[begin:end])
                v =  numpy.var(data[begin:end])
                Y.append(v/m)                
                tol = abs(1-Y[len(Y)-1]/Y[len(Y)-2])
                J+=1
            idc_data[start:end] = Y[len(Y)-1]
            #print("收敛的idc",Y[len(Y)-1],"end",end)
            tol=1
            start = end
        '''
        plt.plot(numpy.arange(0,len(self.data)),self.data/400,"g-",label = "workload/400")
        plt.plot(numpy.arange(0,len(idc_data)),idc_data,"m",label = "IDC")
        plt.legend(loc = "upper right")
        plt.title("Bursty Evaluation of IDC")
        plt.xlabel("Time(seconds)")
        plt.ylabel("Bursty Intensity")
        plt.grid(True)
        '''
        return idc_data         

filePath = "F:/test/workload.xlsx"
burstResult = "F:/test/idc_burst.xlsx"
data = AnalyseIDC(filePath).caculIDC()
wrFile = WRFile()
wrFile.writeDataIntoExcel(data = data,filePath = burstResult)