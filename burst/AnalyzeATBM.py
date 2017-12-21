# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 21:53:04 2017

@author: User
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 16:02:25 2016

@author: User
"""
import sys
sys.path.append("D:/anaconda/project/utils")
import numpy as np
from utils import WRFile
from memory_profiler import profile
import math
import os
from openpyxl import load_workbook
from openpyxl import Workbook
class EvaluateBurst:
    @profile(precision = 4)
    def __init__(self):
        #完成计算的初始化
        filePath = "F:/test/workload.xlsx"
        self.workload =self.getData(filePath)
        
        self.time = np.arange(0,len(self.workload))
        self.sampleLen = 60              
        self.r = np.percentile(self.workload[0:self.sampleLen],90)
        self.b = np.max(self.workload[0:self.sampleLen])
        queue_num = 1
        self.q = 100*queue_num
        self.c0 = 0
        self.t0 = -1
        self.T = 1
        self.space = self.q
        self.windows = len(self.workload)#根据突发的强度，动态调整窗口大小
        self.C = 400
        #阻塞队列
        self._block_q = np.zeros(self.windows)
        self._block_q1 = np.zeros(self.windows)
        self.ck_list = np.zeros(self.windows)
        self.dk_list = np.zeros(self.windows)
        self.ck_list[0] = self.c0
        self.r_list = np.zeros(self.windows)
        self.layers_list = np.zeros(self.windows)
        
        #分析数据：获得缓存、阻塞、延迟、r、d的列表
        
        self.processWorkload(r = self.r,b = self.b)
        self.computeM()
        #plt.plot(self.time,self._block_q,"g",label="cached requests")
        #plt.plot(self.time,self._block_q1,"r",label="blocked requests")
        
    def anlayzeDelay(self):
        pass
    def computeM(self):
        c0=1
        c1 = 0.5
        c2 = 0.5
        self.m = np.abs(c0*self.r_list/self.C+c1*self.dk_list+c2*self._block_q1/self.workload-c0*np.ones(self.windows)) 
        
    def getData(self,filePath):
        wrFile = WRFile()
        data = wrFile.readDataFromExcel(filePath,cols=1)
        return data
    def sendBlockQ(self,token,k):
        '''
        系统当前有剩余的token发送被阻塞的请求
        首先获取block队头阻塞的请求
        依次向队尾迁移
        '''
        #获取队头阻塞的请求
        #print("send token",token)
        if token>0:
            requests = self._block_q[k-1]
            if requests==0:#阻塞队列中无请求
                return token
                        
            if token>=requests:#请求足以发送time时刻阻塞的请求
               token-=requests
               self._block_q[k] = 0
               self.space+=requests#释放空间
            else:               
               self._block_q[k]=self._block_q[k-1]-token
               self.space+=token
               token = 0
        return token #返回剩余的token数
        
    def processWorkload(self,r,b):
        '''
        给定r和b后，计算
        qk_list：请求pk到达之后，队列存储的请求数
        ck_list:请求到达之前系统剩余的token数
        说明:如果当前token不足以发送所有请求，则把剩余的部分存放到队列中。
        '''  
        self.b = b
        self.r = r
        self.r_list[0] = r
        for i in range(0,self.windows):
           begin = i-self.sampleLen+1#计算指数平滑的起点
           if begin<0:
               begin=0
           if begin!=i:
               self.r = max(np.percentile(self.workload[begin:i],90),self.C)
               self.b = np.max(self.workload[begin:i])
               self.r_list[i] = self.r
           #单独分析workload[0]
           if i==0:
               token = min(self.ck_list[0]+self.C*(self.time[0]-self.t0),self.b)
           else:
                #系统当前的token数 
               token = min(self.ck_list[i-1]+self.C*(self.time[i]-self.time[i-1]),self.b)
           #最新到达的请求
           currentRequest = self.workload[i]
           #首先发送队列中阻塞的请求
           tokenLeft = self.sendBlockQ(token,i)#剩余的token数
           
           '''当前的token在发送完阻塞队列中的请求时，无法发送当下请求'''
           if tokenLeft<=currentRequest:#token不够发送当前的请求
              self.ck_list[i] = 0
              blockRequests = currentRequest-tokenLeft#待阻塞的请求
              self.storeRequests(i,blockRequests)#存储该请求
              tokenLeft = 0
              #计算当前请求的延迟，最好是使用指数平滑综合前边的结果
              dk = self.getDelay(blockRequests,i)
              self.dk_list[i] = dk
              
           #当前请求在发送完阻塞队列中的请求后，足以发送当前剩余的请求
           elif tokenLeft>currentRequest: #当前的token足以发送
               tokenLeft-=currentRequest 
               self.ck_list[i] = tokenLeft#剩余的token数
               self.dk_list[i] = 0

           if i+1<self.windows:    
               self.r_list[i+1] = self.r
    def storeRequests(self,k,requests):
        '''
        根据系统当前一级队列的剩余情况，进行存储
        如果当前第一队列空间充足，存储该请求
        如果不充足，当多余的部分存放到第二梯队
        '''
        
        if requests==0:
            return        
        if self.space>=requests:#当前第一梯队的存储空间充足
           
           self._block_q[k]=self._block_q[k]+requests
           self.space-=requests
       
        elif self.space<requests:#第一梯队空间不足，向第二梯队存储
        
           #利用剩余的token
           temp = self._block_q[k]#目前阻塞的请求
           if self.space>0:
               temp += self.space
           
           self._block_q[k] = temp
           self._block_q1[k] = requests-self.space
           self.space = 0           
 
        
    def getDelay(self,request,cur):
        
        cacheR = self._block_q[cur]    
        cacheD = cacheR/self.r#本周期缓存入得请求
        #print("******")
        #print("缓存的请求",cacheR)
        blockR = self._block_q1[cur]
        #print("阻塞的请求",blockR)
        blockD = 0
        layers = math.ceil(blockR/self.q)
        #print("层数为",layers)
        i = 1
        if layers==1:
            blockD = blockR/self.r
        elif layers>1:
             while i<layers:
                blockD+=i*self.q/self.r
                i+=1
             if i==layers:
                 blockD += (blockR-(i-1)*self.q)/self.r
        delay = cacheD+blockD
        if delay is None:
            delay = 0
        self.layers_list[cur] = layers
        #print("异常",type(delay))
        return delay
    
EvaluateBurst()

