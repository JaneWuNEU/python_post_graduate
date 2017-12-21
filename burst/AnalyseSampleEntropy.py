# -*- coding: utf-8 -*-
"""
Created on Tue Jan 17 15:55:36 2017

@author: User
"""
import sys
sys.path.append("D:/anaconda/project/utils")
import numpy as np
from utils import WRFile
import matplotlib.pyplot as plt
from sampleEntropy import SampleEntropy 
from memory_profiler import profile
class AnalyseSampleEntropy:
    
    def __init__(self):
        
        filePath = "F:/test/workload.xlsx"
        wrFile = WRFile()
        self.workload = wrFile.readDataFromExcel(filePath = filePath,sheet_name="1")
        data = self.evaluateBurst()
        data = data/np.max(data)
        wrFile.writeDataIntoExcel(data = data,filePath = "F:/test/avgsampEn.xlsx")
    def evaluateBurst(self):
        sam = SampleEntropy()
        burst = []
        for i in range(0,int(len(self.workload)/60)):
            data = self.workload[i*60:(i+1)*60]
            begin = int(i/(60*24))*60*60*24
            r = 0.3*np.percentile(self.workload[begin:(i+1)*60],70)
            temp = sam.sampen2(data,m =10,r = r)
            burst.append(temp)
        burst_sec = np.ones(len(self.workload))
        for i in range(0,len(self.workload)):
            k = int(i/60)
            burst_sec[i]*=burst[k]
        return np.array(burst_sec)
        '''
        plt.plot(np.arange(0,len(self.workload)),self.workload/400,"g-",label = "workload/400")
        plt.plot(np.arange(0,len(burst_sec)),burst_sec,"m",label = "AvgSampEn")
        plt.legend(loc = "upper right")
        plt.title("Bursty Evaluation of AvgSampEn")
        plt.xlabel("Time(seconds)")
        plt.ylabel("Bursty Intensity")
        plt.grid(True)
        '''
AnalyseSampleEntropy()
