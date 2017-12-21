# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 10:14:36 2017

@author: User
"""
import numpy as np
import sys
sys.path.append("D:\\anaconda\\project/")
from utils import WRFile
import matplotlib.pylab as plt
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签 
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.rc('font', size=18)  
class ProduceData:
    def stationaryData(self,average,amount,fluctuation):
        data = np.ones(amount)*average+np.random.randint(-1*fluctuation,fluctuation+1,amount)
        return data
    def increaseData(self,average,amount,fluctuation):#20+0.1*X
        data = average+0.2*np.arange(amount)+np.random.randint(-1*fluctuation,fluctuation+1,amount)
        return data
    def decreaseData(self,average,amount,fluctuation):#22-0.1*X
        data = average-0.1*np.arange(amount)+np.random.randint(-1*fluctuation,fluctuation+1,amount)
        return data
    def flat_decrease(self,flat,amount,fluctuation):
        middle = amount/2
        data0 = np.ones(middle)*flat
        print(data0.size)
        data1 = flat+np.arange(middle,amount)*-0.1
        data0 = np.append(data0,data1)
        data0+=np.random.randint(-1*fluctuation,fluctuation+1,amount)
        print(data0)
        return data0
    def flat_increase(self,flat,amount,fluctuation):
        middle = amount/2
        data0 = np.ones(middle)*flat
        print(data0.size)
        data1 = flat+np.arange(middle,amount)*0.1
        data0 = np.append(data0,data1)
        data0+=np.random.randint(-1*fluctuation,fluctuation+1,amount)
        print(data0)
        return data0
    def inc_dec(self,begin,slope,fluctuation,amount):
        middle = amount/2
        data0 = begin +slope*np.arange(middle)
        data1 = np.max(data0)-slope*np.arange(middle,amount)
        data = np.append(data0,data1)+np.random.randint(-1*fluctuation,fluctuation+1,amount)       
        return data
    def dec_inc(self,begin,slope,fluctuation,amount):
        middle = amount/2
        data0 = begin -slope*np.arange(middle)
        data1 = np.min(data0)+slope*np.arange(middle,amount)
        data = np.append(data0,data1)+np.random.randint(-1*fluctuation,fluctuation+1,amount)       
        return data
wrFile =WRFile()
file_List = ["stationary","inc","dec","flat_dec","flat_inc","inc_dec","dec_inc"]
data = wrFile.readDataFromExcel(filePath = "D:\\cloudsim\\log\\workload1/synthetic/"+file_List[0]+".xlsx")
plt.plot(np.arange(len(data)),data,"k")
plt.title(u"平稳型并发量数据")
plt.xlabel(u"时间",fontsize = 18)
plt.ylabel(u"并发量数量",fontsize = 18)
plt.ylim(0,60)
plt.legend(["并发量"],loc='upper left')  
