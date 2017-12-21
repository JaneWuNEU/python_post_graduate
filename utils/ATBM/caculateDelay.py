# -*- coding: utf-8 -*-
"""
Created on Tue Jul 11 09:17:46 2017

@author: User
"""
import sys
sys.path.append("D:\\anaconda\\project/")
sys.path.append("D:\\anaconda\\project/ATBM")
import numpy as np
from utils import WRFile
import math
import os
import matplotlib.pylab as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
from plotdata import PlotData
from CaculateDelayATBM_SQ import DelayofATBMandSQ
plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签 
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.rc('font', size=18)     
def translateDictIntoList(data_dict):
    keys = data_dict.keys()
    data_list = np.zeros(6)
    for key in keys:
        if key in [0,1,2,3,4]:
            data_list[key] = round(data_dict[key])
        else:
            data_list[5] += round(data_dict[key])
    return data_list.tolist()
    
def produceSeperateDelay(delay,x,y,z):
    w1 = [float("%.1f"%x),float("%.1f"%y),float("%.1f"%z)] 
    w2 = [float("%.1f"%x),float("%.1f"%y),float("%.1f"%z)]
    
    ATBM = delay.delayofATBM(x,y,z)[1] 
    ATBM = translateDictIntoList(ATBM)
    SQ  = delay.delayofSQ(x,y,z)[1]
    SQ = translateDictIntoList(SQ)
    w1.extend(ATBM)
    w2.extend(SQ)
    return w1,w2
    
def produceDelay(delay,x,y,z):
    workload = [float("%.1f"%x),float("%.1f"%y),float("%.1f"%z)]                        
    atbm = workload.copy()
    ATBM = delay.delayofATBM(x,y,z)[0]
    atbm.extend(ATBM)
    
    SQ  = delay.delayofSQ(x,y,z)[0]
    sq = [float("%.1f"%x),float("%.1f"%y),float("%.1f"%z),SQ[0],SQ[1],SQ[2],SQ[3]]
    
    d = ATBM[0]-SQ[0] 
    d = float("%.3f"%d)
    state = -1
    if d==0:
        state=0
    elif d<0:
        state=1
    workload.extend([d,state])
    return atbm,sq,workload
'''
比较不同访问模式下，各类不同延迟对应的请求数
例如 分别统计延迟为0,1,2,....,n的请求的数量
'''
def compareATBMandSQSeperateDelay(q=4):
    delay = DelayofATBMandSQ(q=q)
    c1 = np.arange(0,q,0.2)
    atbm_delay = []
    sq_delay = []
    for x in c1:
        if x<=1:
            Y = np.arange(0,q,0.2)
            for y in Y:
                if y<=1:
                    Z = np.arange(0,q,0.2)
                    for z in Z:
                        result = produceSeperateDelay(delay,x,y,z)                      
                        atbm_delay.append(result[0])
                        sq_delay.append(result[1])
                        
                else:#y>1
                    Z = np.arange(0,1+q-y,0.2)
                    for z in Z:
                        result = produceSeperateDelay(delay,x,y,z)
                        atbm_delay.append(result[0])
                        sq_delay.append(result[1])
                        
                    
        else:#x>1
            Y = np.arange(0,q+1-x,0.2)
            for y in Y:
                if y<=1:
                    if(1-y)>=(x-1):
                        Z = np.arange(0,q,0.2)
                        for z in Z:
                           result = produceSeperateDelay(delay,x,y,z)
                           atbm_delay.append(result[0])
                           sq_delay.append(result[1])
                           
                    else:#(1-y)<(x-1)
                        Z = np.arange(0,2+q-x-y,0.2)
                        for z in Z:
                           result = produceSeperateDelay(delay,x,y,z)
                           atbm_delay.append(result[0])
                           sq_delay.append(result[1])
                           
                else:#y>1
                    Z = np.arange(0,q+2-x-y,0.2)
                    for z in Z:
                           result = produceSeperateDelay(delay,x,y,z)
                           atbm_delay.append(result[0])
                           sq_delay.append(result[1])
                                                                              
    return atbm_delay,sq_delay   
def compareATBMandSQofTotalDealy(q=4):
    '''
    result = compareATBMandSQofTotalDealy(q)
    wrFile = WRFile()
    ATBM_file = "F:\data\experiment/Delay_ATBM_q"+str(q)+".xlsx"
    SQ_file = "F:\data\experiment/Delay_SQ_q"+str(q)+".xlsx"
    dis_file = "F:\data\experiment/Delay_q"+str(q)+".xlsx"
    wrFile.writeDataIntoExcel(filePath = ATBM_file,data = result[1])
    wrFile.writeDataIntoExcel(filePath = SQ_file,data = result[2])
    wrFile.writeDataIntoExcel(filePath = dis_file,data = result[0])
    '''
    delay = DelayofATBMandSQ(q=q)
    c1 = np.arange(0,q,0.2)
    dis_delay=[]
    atbm_delay = []
    sq_delay = []
    for x in c1:
        if x<=1:
            Y = np.arange(0,q,0.2)
            for y in Y:
                if y<=1:
                    Z = np.arange(0,q,0.2)
                    for z in Z:
                        result = produceDelay(delay,x,y,z)
                        atbm_delay.append(result[0])
                        sq_delay.append(result[1])
                        dis_delay.append(result[2])
                else:#y>1
                    Z = np.arange(0,1+q-y,0.2)
                    for z in Z:
                        result = produceDelay(delay,x,y,z)
                        atbm_delay.append(result[0])
                        sq_delay.append(result[1])
                        dis_delay.append(result[2])
                    
        else:#x>1
            Y = np.arange(0,q+1-x,0.2)
            for y in Y:
                if y<=1:
                    if(1-y)>=(x-1):
                        Z = np.arange(0,q,0.2)
                        for z in Z:
                           result = produceDelay(delay,x,y,z)
                           atbm_delay.append(result[0])
                           sq_delay.append(result[1])
                           dis_delay.append(result[2])
                    else:#(1-y)<(x-1)
                        Z = np.arange(0,2+q-x-y,0.2)
                        for z in Z:
                           result = produceDelay(delay,x,y,z)
                           atbm_delay.append(result[0])
                           sq_delay.append(result[1])
                           dis_delay.append(result[2])
                else:#y>1
                    Z = np.arange(0,q+2-x-y,0.2)
                    for z in Z:
                           result = produceDelay(delay,x,y,z)
                           atbm_delay.append(result[0])
                           sq_delay.append(result[1])
                           dis_delay.append(result[2])                        
                            
    return dis_delay,atbm_delay,sq_delay
def analyzeCompareResult(q):
    wrFile = WRFile()
    #fileKind = "F:\\data\\experiment/Delay_SQ_q"
    fileKind = "F:\\data\\experiment/Delay_q"
    x = wrFile.readDataFromExcel(filePath = fileKind+str(q)+".xlsx",min_cols = 1,max_cols = 1)
    y = wrFile.readDataFromExcel(filePath = fileKind+str(q)+".xlsx",min_cols = 2,max_cols = 2)
    z = wrFile.readDataFromExcel(filePath = fileKind+str(q)+".xlsx",min_cols = 3,max_cols = 3)
    a = wrFile.readDataFromExcel(filePath = fileKind+str(q)+".xlsx",min_cols = 5,max_cols = 5)
    #plot4DSeperate(x,y,z,a,q)
    PlotData().plot4D(x,y,z,a,q)
def caculateSumOfSeperateDelay(filePath,cols):
    wrFile = WRFile()
    data  = np.array(wrFile.readDataFromExcel(filePath = filePath,min_cols = cols,max_cols = cols))
    data_sum = np.sum(data)
    return data_sum
def cumulateData(data):
    result = np.zeros(len(data))
    result[0] = data[0]
    for i in range(1,len(data)):
        result[i]=result[i-1]+data[i]
    return result
def caculateCumlateData(q):
    ATBM_data = []
    SQ_data = []           
    ATBM_file = "F:\data\experiment/Seperate_Delay_ATBM_q"+str(q)+".xlsx"
    SQ_file = "F:\data\experiment/Seperate_Delay_SQ_q"+str(q)+".xlsx"
    #获取各类延迟的数据
    for j in range(4,10):
        ATBM_data.append(caculateSumOfSeperateDelay(ATBM_file,j))    
        SQ_data.append(caculateSumOfSeperateDelay(SQ_file,j))
   #数据进行归于话处理
    ATBM_data = np.array(ATBM_data)
    SQ_data = np.array(SQ_data)
    ATBM_data = np.round(ATBM_data/np.sum(ATBM_data),2)
    SQ_data = np.round(SQ_data/np.sum(SQ_data),2)
    print("ATBM is",cumulateData(ATBM_data))
    print("SQ is",cumulateData(SQ_data))
def plotDelayDistribution(q):

    ATBM_data = []
    SQ_data = []           
    ATBM_file = "F:\data\experiment/Seperate_Delay_ATBM_q"+str(q)+".xlsx"
    SQ_file = "F:\data\experiment/Seperate_Delay_SQ_q"+str(q)+".xlsx"
    #获取各类延迟的数据
    for j in range(4,10):
        ATBM_data.append(caculateSumOfSeperateDelay(ATBM_file,j))    
        SQ_data.append(caculateSumOfSeperateDelay(SQ_file,j))
   #数据进行归于话处理
    ATBM_data = np.array(ATBM_data)
    SQ_data = np.array(SQ_data)
    ATBM_data = np.round(ATBM_data/np.sum(ATBM_data),2)
    SQ_data = np.round(SQ_data/np.sum(SQ_data),2)
    data = [ATBM_data,SQ_data]
    colors = ("k","w")
    labels=("ATBM","SQ")
    title = u"队列级数为"+str(q)+u"时ATBM和SQ下不同延迟的分布"
    xticks = []
    for i in range(5):
        xticks.append("d="+str(i))
    xticks.append("d>="+str(4))
    plot = PlotData()
    plot.plotBar(data,colors,labels,title,xlabel=u"请求延迟",ylabel=u"延迟对应的比例",ylimit=1,xticks=xticks)
    
    print("ATBM各级延迟",ATBM_data)
    print("SQ各级延迟",SQ_data)
    '''
    print("ATBM累计延迟",cumulateData(ATBM_data))
    print("SQ累计延迟",cumulateData(SQ_data))
    '''
def test(q):
    wrFile = WRFile()
    ATBM_file = "F:\data\experiment/Seperate_Delay_ATBM_q"+str(q)+".xlsx"
    SQ_file = "F:\data\experiment/Seperate_Delay_SQ_q"+str(q)+".xlsx"
    '''atbm = wrFile.readDataFromExcel2(filePath = ATBM_file)
    sq = wrFile.readDataFromExcel2(filePath = SQ_file)
    for i in range(len(atbm)):
        atbm_data = atbm[i]
        sq_data = sq[i]
        print(atbm_data)
        print(sq_data)
        print(np.sum(atbm_data[3:])-np.sum(sq_data[3:]))
        if np.sum(atbm_data[3:])!= np.sum(sq_data[3:]):
            print(atbm_data[:3])
    '''
wrFile = WRFile()
taobao = wrFile.readDataFromExcel(filePath = "D:\\cloudsim\\log\\workload1/taobao.xlsx")
FIFA = wrFile.readDataFromExcel(filePath = "F:\\FIFA\\predict\\traindata\\inmin/workload53inmin.xlsx")
plt.plot(np.arange(len(FIFA)),FIFA,"k")
plt.legend([u'并发量'],fontsize=18,loc="upper left")
plt.xlabel(u"时间/分钟",fontsize=18)
plt.ylabel(u"并发量/次",fontsize=18)
plt.grid(True)
plt.title(u"1998年世界杯期间5月17日的用户并发量数据")
#plotDelayDistribution(q)
#q = 6
#plotDelayDistribution(q)