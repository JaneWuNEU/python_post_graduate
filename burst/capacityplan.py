# -*- coding: utf-8 -*-
"""
Created on Thu Jan  5 10:37:56 2017

@author: Jane Wu
"""
import sys
sys.path.append("D:/anaconda/project/utils")
import numpy as np
from utils import WRFile
import matplotlib.pyplot as plt
import math 
class CapacityPlan:
    
    def __init__(self,filePath):
        #完成计算的初始化
        self.workload =self.getData(filePath)
        self.workload=np.array(self.workload)
        self.window = len(self.workload)
        self.time = np.arange(0,len(self.workload))
        self.sampleLen = 40
        self.c0 = 3
        self.t0 = -1
        self.T = 1
        
        
        #初始化核心参数
        self.C = 400
        self.C1 = self.C
        self.limitsDe = 0.2#允许的最大延迟
        #队列的长度
        self.q = self.C*(self.limitsDe+0.2)
        self.q1 = self.C*self.limitsDe
        self.q2 = 0.8*self.q1
        self.q3 = 0.6*self.q1
        self.q4 = 0.4*self.q1
        self.q5 = 0.2*self.q1
        
        #队列的可用空间
        self.q_space = self.q
        self.q1_space = self.q1
        self.q2_space = self.q2
        self.q3_space = self.q3
        self.q4_space = self.q4
        self.q5_space = self.q5
        #记录当前阻塞的层级layer
        self.layers = 0
        
        self.cacheq = np.zeros(self.window)
        self.blockq1 = np.zeros(self.window)
        self.blockq2 = np.zeros(self.window)
        self.blockq3 = np.zeros(self.window)
        self.blockq4 = np.zeros(self.window)
        self.blockq5 = np.zeros(self.window)
        self.discard = np.zeros(self.window)
        self.sentq = np.zeros(self.window)
        self.ck_list = np.zeros(self.window)
        self.r_list = np.zeros(self.window)
        self.b_list = np.zeros(self.window)
        self.c1_list = np.zeros(self.window)
        
       
        self.processWorkd()
        
        print("w ",self.workload)
        print("q",self.cacheq)
        print("q1",self.blockq1)
        print("q2",self.blockq2)
        print("q3",self.blockq3)
        print("q4",self.blockq4)
        print("q5",self.blockq5)
        print("st",self.sentq)
        print("dis",self.discard)
        print(self.blockq1/self.q1)
        
        '''
        plt.plot(self.time,self.cacheq,"c",label="q")
        plt.plot(self.time,self.blockq1/self.q1,"g",label="q1")
        plt.plot(self.time,self.blockq2,"y",label="q2")
        plt.plot(self.time,self.blockq3,"b",label="q3")
        plt.plot(self.time,self.blockq4,"m",label="q4")
        plt.plot(self.time,self.blockq5,"r",label="q5")
        plt.plot(self.time,self.c1_list,"r",label="c1")
        plt.plot(self.time,self.workload,"g",label="workload")
        plt.legend()
        '''

        
    def sendCachedRequests(self,token,k):
        #发送缓存的请求
          
        if token>0:
            requests = self.cacheq[k-1]
            if requests==0:#阻塞队列中无请求
                self.q_space=self.q
                self.cacheq[k] = 0
                return token
                 
            if token>=requests:#请求足以发送time时刻阻塞的请求
               token-=requests
               self.cacheq[k] = 0
               self.q_space=self.q#释放空间
            else:               
               self.cacheq[k]=self.cacheq[k-1]-token
               self.q_space+=token
               token = 0
        return token #返回剩余的token数
        
    def sendBlockedRequests(self,k):
        #根据layers进行调整C1
        
        threshold = self.limitsDe
        levels = self.layers
        if levels==0:#当前没有阻塞
            return
        if levels<=1+threshold:#阻塞的层级达到q2
           self.C1 = (0.8*threshold+1)*self.C
           token = self.C1
           
           token-=self.blockq1[k]
           #发送q1中的请求
           self.blockq1[k] = 0
           self.q1_space = self.q1
           #发送q2中的请求
           if token>self.blockq2[k]:
               token = 0
               self.blockq2[k] = 0
               self.q2_space = self.q2
           else:
               self.blockq2[k] -= token
               self.q2_space += token
               
               
           
        elif levels<=2+threshold:#阻塞到了第q3
           self.C1 = (0.6*threshold+1.8)*self.C
           token = self.C1
           
           token-=self.blockq1[k]
           token-=self.blockq2[k]
           #发送q1中的请求
           self.blockq1[k] = 0
           self.q1_space = self.q1
           #发送q2中的请求
           self.blockq2[k] = 0
           self.q2_space = self.q2
           #发送q3中的请求
           if token>self.blockq3[k]:
               token = 0
               self.blockq3[k] = 0
               self.q3_space = self.q3
           else:
               self.blockq3[k] -= token
               self.q3_space += token
               
        elif levels<=3+threshold:#阻塞到了第q4
           self.C1 =  (0.4*threshold+2.4)*self.C
           token = self.C1          
           token-=self.blockq1[k]
           token-=self.blockq2[k]
           token-=self.blockq3[k]
           #发送q1中的请求
           self.blockq1[k] = 0
           self.q1_space = self.q1
           #发送q2中的请求
           self.blockq2[k] = 0
           self.q2_space = self.q2
           #发送q3中的请求
           self.blockq3[k] = 0
           self.q3_space = self.q3
           #发送q4中的请求
           if token>self.blockq4[k]:
               token = 0
               self.blockq4[k] = 0
               self.q4_space = self.q4
           else:
               self.blockq4[k] -= token
               self.q4_space += token     
        else:
           self.C1 =  (0.2*threshold+2.8)*self.C
           token = self.C1
           
           token-=self.blockq1[k]
           token-=self.blockq2[k]
           token-=self.blockq3[k]
           token-=self.blockq4[k]
           #发送q1中的请求
           self.blockq1[k] = 0
           self.q1_space = self.q1
           #发送q2中的请求
           self.blockq2[k] = 0
           self.q2_space = self.q2
           #发送q3中的请求
           self.blockq3[k] = 0
           self.q3_space = self.q3
           #发送q4中的请求
           self.blockq4[k] = 0
           self.q4_space = self.q4
           #发送q5中的请求
           if token>self.blockq5[k]:
               token = 0
               self.blockq5[k] = 0
               self.q5_space = self.q5
           else:
               self.blockq5[k] -= token
               self.q5_space += token 
        self.c1_list[k] = self.C1
        self.layers = 0
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
                                                                                                                                                                                                                                                                                                                                                                                                     
            
        
           
            
        
    
    def processWorkd(self):
        self.r = np.percentile(self.workload[0:self.sampleLen],90)
        self.b = np.max(self.workload[0:self.sampleLen])
        self.r_list[0] = self.r
        self.b_list[0] = self.b
        
        for i in range(0,self.window):
           begin = i-self.sampleLen+1#计算指数平滑的起点
           if begin<0:
               begin=0
           if begin!=i:
               self.r = np.percentile(self.workload[begin:i],90)
               self.b = np.max(self.workload[begin:i])
               self.b_list[i] = self.b
               self.r_list[i] = self.r
           

           if i==0:
               #token = min(self.ck_list[0]+self.C*(self.time[0]-self.t0),self.b)
               token = self.C*(self.time[0]-self.t0)
           else:
                #系统当前的token数 
               #token = min(self.ck_list[i-1]+self.C*(self.time[i]-self.time[i-1]),self.b)
               token = self.C*(self.time[i]-self.time[i-1])
           
           '''发送系统中的请求'''  
           #最新到达的请求
           currentRequest = self.workload[i]
           #首先发送队列中阻塞的请求
           
           tokenLeft = self.sendCachedRequests(token,i)#剩余的token数
           self.sentq[i]=token-tokenLeft
           
           '''当前的token在发送完阻塞队列中的请求时，无法发送当下请求'''
           if tokenLeft<=currentRequest:#token不够发送当前的请求
              self.ck_list[i] = 0
              blockRequests = currentRequest-tokenLeft#待阻塞的请求
              self.storeData(i,blockRequests)#存储该请求
              tokenLeft = 0
                 
              
           #当前请求在发送完阻塞队列中的请求后，足以发送当前剩余的请求
           elif tokenLeft>currentRequest: #当前的token足以发送
               tokenLeft-=currentRequest 
               blockRequests = 0
               self.storeData(i,blockRequests)
               
               #处理被阻塞的请求
               self.ck_list[i] = tokenLeft#剩余的token数
               #self.dk_list[i] = 0
           
           #记录发送的请求数
           self.sentq[i]=token-tokenLeft   
           #调整r和b
           if i+1<self.window:    
               self.r_list[i+1] = self.r
           
           #根据阻塞队列的阻塞情况调整C1
           self.sendBlockedRequests(i)
               
               
               
    def getData(self,filePath):
        wrFile = WRFile()
        data = wrFile.readDataFromExcel(filePath,cols=1)
        return data
        
    def storeData(self,i,blockRequests):
            temp = blockRequests#无法处理的请求
            
            if temp<=0:
                self.blockq1[i] = self.blockq1[i-1]
                self.blockq2[i] = self.blockq2[i-1]
                self.blockq3[i] = self.blockq3[i-1]
                self.blockq4[i] = self.blockq4[i-1]
                self.blockq5[i] = self.blockq5[i-1]
                return
            if temp<=self.q_space:
                self.cacheq[i] = temp+self.cacheq[i]
                #print("i",i,"self.cacheq[i-1]",self.cacheq[i-1],"self.cacheq[i]",self.cacheq[i])
                self.q_space-=temp
                self.blockq1[i] = self.blockq1[i-1]
                self.blockq2[i] = self.blockq2[i-1]
                self.blockq3[i] = self.blockq3[i-1]
                self.blockq4[i] = self.blockq4[i-1]
                self.blockq5[i] = self.blockq5[i-1]
            else:
                temp-=self.q_space #需要阻塞的请求
                self.cacheq[i] = self.q_space
                self.q_space=0
                
                if temp<=self.q1_space:
                    
                    self.blockq1[i] = temp+self.blockq1[i-1]
                    
                    self.layers = self.blockq1[i]/self.q1
                    self.q1_space-=temp                
                    self.blockq2[i] = self.blockq2[i-1]
                    self.blockq3[i] = self.blockq3[i-1]
                    self.blockq4[i] = self.blockq4[i-1]
                    self.blockq5[i] = self.blockq5[i-1]
                elif temp<=(self.q1_space+self.q2_space): 
                     self.blockq1[i] = self.q1_space+self.blockq1[i-1]
                     self.blockq2[i] = temp-self.q1_space+self.blockq2[i-1] 
                     
                     self.layers = 1 + self.blockq2[i]/self.q2
                     
                     temp = temp-self.q1_space#剩下的请求数
                     self.q2_space -= temp
                     self.q1_space =0
                     self.blockq3[i] = self.blockq3[i-1]
                     self.blockq4[i] = self.blockq4[i-1]
                     self.blockq5[i] = self.blockq5[i-1]                     
                       
                elif temp<=(self.q1_space+self.q2_space+self.q3_space):
                     
                     
                     self.blockq1[i] = self.q1_space+self.blockq1[i-1]
                     self.blockq2[i] = self.q2_space+self.blockq2[i-1]
                     self.blockq3[i] = temp-self.q1_space-self.q2_space+self.blockq3[i-1] 
                     
                     self.layers = 2+ self.blockq3[i]/self.q3
                     
                     temp = temp-self.q1_space-self.q2_space#剩下的请求数
                     self.q3_space -= temp
                     self.q1_space = self.q2_space =0
                     self.blockq4[i] = self.blockq4[i-1]
                     self.blockq5[i] = self.blockq5[i-1]                     
                      
                elif temp<=(self.q1_space+self.q2_space+self.q3_space+self.q4_space):
                     
                     
                     self.blockq1[i] = self.q1_space+self.blockq1[i-1]
                     self.blockq2[i] = self.q2_space+self.blockq2[i-1]
                     self.blockq3[i] = self.q3_space+self.blockq3[i-1]
                     self.blockq4[i] = temp-self.q1_space-self.q2_space-self.q3_space+self.blockq4[i-1]
                     
                     self.layers = 3 + self.blockq4[i]/self.q4
                     
                     temp = temp-self.q1_space-self.q2_space-self.q3_space#剩下的请求数
                     self.q4_space -= temp
                     self.q1_space = self.q2_space = self.q3_space =0
                     self.blockq5[i] = self.blockq5[i-1]                     
                      
                else:
                     
                     self.blockq1[i] = self.q1_space+self.blockq1[i-1]
                     self.blockq2[i] = self.q2_space+self.blockq2[i-1]
                     self.blockq3[i] = self.q3_space+self.blockq3[i-1]
                     self.blockq4[i] = self.q4_space+self.blockq4[i-1]
                     temp = temp-self.q1_space-self.q2_space-self.q3_space-self.q4_space#剩下的请求数
                     
                     if temp>self.q5_space:
                         self.discard[i] = temp-self.q5_space
                         self.blockq5[i] = self.q5_space+self.blockq5[i-1]
                         self.q5_space = 0
                     else:
                         self.blockq5[i] = temp+self.blockq5[i-1]
                         self.q5_space -= temp
                         
                     self.layers = 4 + self.blockq5[i]/self.q5 + self.discard[i]/self.q5
                     self.q1_space = self.q2_space = self.q3_space =self.q4_space = 0
                
filePath = "F:/burst.xlsx"
burst = CapacityPlan(filePath)