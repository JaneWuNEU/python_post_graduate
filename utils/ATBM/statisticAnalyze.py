# -*- coding: utf-8 -*-
"""
Created on Fri Jul 14 17:44:10 2017

@author: wujing
"""

import numpy as np
import sys
sys.path.append("E:\\project\\python/")
import numpy as np
from utils import WRFile
import math
import matplotlib.pylab as plt
def getStatisticAttribute(data):   
    data = np.array(data)
    P25th = np.percentile(data,25)
    median = np.percentile(data,50)
    means = np.round(np.mean(data),3)
    P75th = np.percentile(data,75)
    P90th = np.percentile(data,90)
    P95th = np.percentile(data,95)
    Max = np.max(data)
    print("1/4 ",P25th)
    print("median ",median)
    print("means ",means)
    print("3/4 ",P75th)
    print("90 ",P90th)
    print("95 ",P95th)
    print("max ",Max)
    result = [P25th,median,means,P75th,P90th,P95th,Max]
    return result
def analyzeStats():
    qList = [2,3,4,5,6]
    wrFile = WRFile()
    result = []
    for q in qList:
        fileName = "F:\data\experiment/Delay_SQ_q"+str(q)+".xlsx"
        data = wrFile.readDataFromExcel(filePath=fileName,sheet_name = "1",min_cols = 4,max_cols = 4)
        r = getStatisticAttribute(data)
        result.append(r)
    #print("ATBM is",result)
    wrFile.writeDataIntoExcel(result,filePath = "F:\data\experiment/Delay_SQ_stats.xlsx")
def moveDown(c):
    c1 = c[0]
    c2 = c[1]
    c3 = c[2]
    if c1>0:
        c1a = c1-0.5
    else:
        c1a = c1
        
    if c2>0:
        c2a = c2-0.5
    else:
        c2a = c2      
        
    if c3>0:
        c3a = c3-0.5
    else:
        c3a = c3
    c1a = math.floor(c1a) 
    c2a = math.floor(c2a)
    c3a = math.floor(c3a)
    return [c1a,c2a,c3a]
def analyzeResult(q,better,worse):
    axeRange = q
    record = []
    print(axeRange)
    for x in range(axeRange):
        for y in range(axeRange):
            for z in range(axeRange):
                if better[x][y][z]>0 or worse[x][y][z]>0:
                    print()
                    #print("better:"+str(better[x][y][z]))
                    #print("worse:"+str(worse[x][y][z]))
                    record.append([str(x)+"<c1<="+str(x+1)+","+str(y)+"<c2<="+str(y+1)+","+str(z)+"<c3<="+str(z+1),better[x][y][z],worse[x][y][z]])
                    #print("=======================")
    wrFile = WRFile()
    filePath = "F:\\data\\experiment/Delay_distribute_q"+str(q)+".xlsx"
    wrFile.writeDataIntoExcel(data = record,filePath = filePath)
def divideSpace(q):
    #以数据为中心，然后把每个点定位到一个立方体中。立方体用一个三维数组表示。
    better = np.zeros(q**3).reshape(q,q,q)
    worse = np.zeros(q**3).reshape(q,q,q)
    equal = np.zeros(q**3).reshape(q,q,q)
    wrFile = WRFile()
    #用正方体左下角的点代替整个正方体
    fileKind = "F:\\data\\experiment/Delay_q"
    #fileKind = "F:\\data\\experiment/Delay_q"
    x = wrFile.readDataFromExcel(filePath = fileKind+str(q)+".xlsx",min_cols = 1,max_cols = 1)
    y = wrFile.readDataFromExcel(filePath = fileKind+str(q)+".xlsx",min_cols = 2,max_cols = 2)
    z = wrFile.readDataFromExcel(filePath = fileKind+str(q)+".xlsx",min_cols = 3,max_cols = 3)
    a = wrFile.readDataFromExcel(filePath = fileKind+str(q)+".xlsx",min_cols = 5,max_cols = 5)
    for i in range(len(x)):
        c = [x[i],y[i],z[i]]
        c = moveDown(c) 
        result = a[i]
        if result==0:
            equal[c[0]][c[1]][c[2]]+=1
        elif result==1:
            better[c[0]][c[1]][c[2]]+=1
        else:
            worse[c[0]][c[1]][c[2]]+=1
    
    #print("better is",better)
    #print("worse is",worse)
    #print("equal is",equal)
    analyzeResult(q,better,worse)


#divideSpace(q)
#getStatisticAttribute(q)   
#analyzeStats()  

wrFile = WRFile()
data = wrFile.readDataFromExcel(filePath = "D:\\cloudsim\\log\\workload1/taobao.xlsx",min_cols = 1,max_cols =1,sheet_name = "1") 
data =  np.floor((np.array(data)/100))
#print(data)
wrFile.writeDataIntoExcel(data = data,filePath="D:\\cloudsim\\log\\workload1/deplete_taobao.xlsx")
print(np.percentile(np.array(data),80))


