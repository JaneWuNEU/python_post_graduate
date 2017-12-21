# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 10:41:37 2016

@author: User
"""
import sys
sys.path.append("D:/anaconda/project/utils")
import numpy as np
from utils import WRFile
import matplotlib.pyplot as plt
class LagerRequest:
    def __init__(self,arrivalPattern,r):
        self._arrivalPattern = arrivalPattern
        self.workload = arrivalPattern[0,:]
        #print(sum(self.workload)/len(self.workload))
        self.M = max(self.workload)#最密集的请求
        self.time = arrivalPattern[1,:]
        self.c0 = 3
        self.t0 = -1
        """改进点"""+
        self.windows = len(self.workload)#根据突发的强度，动态调整窗口大小
        self.q = self.M #如果面对突发，这个值非常之大，非常之不合理
        self._Ik_list = np.zeros(self.windows)
        self._ck_list = np.zeros(self.windows)
        self._ck_list[0] = min(self.c0+r*(self.time[0]-self.t0),b)
        self._Ik_list[0] = -1
    def computeRRange(self):
        '''
        based on the length of q computes the range of the r
        and return the result with the format of list[Rmin,Rmax]
        '''
     #********获取R的最小值*****************
        Rmin =  0
        localMax = 0
        packetSum = 0
        for i in range(0,self.windows):
            packetSum+=self.workload[i]
            temp = (packetSum-self.c0-self.q+self.M)/(self.time[i]-self.t0)
            if temp>localMax:
               localMax = temp
        Rmin = localMax
        #print("rminx",Rmin)
     #********获取R的最大值*****************        
        Rmax = 0
        localMax = 0
        
        for i in range(1,len(self.workload)):
            temp = self.workload[i]/(self.time[i]-self.time[i-1])#这里是tk-tk-1(!这里做特殊声明)
            if temp>localMax:
                localMax = temp
            #print(temp)
        
        temp = (self.workload[0]-self.c0)/(self.time[0]-self.t0)
        if temp>localMax:
            localMax = temp
        Rmax = localMax
        #print("rminx",Rmax)
     #**********返回结果**************************
        return [Rmin,Rmax]
        
    def computeqk_listAndck_listWithB(self,r,b):
        qk_list = np.zeros(self.windows)#每个请求到达前，系统剩余的token数
        ck_list = np.zeros(self.windows)    
        ck_list[0] = min(self.c0+r*(self.time[0]-self.t0),b)

        for i in range(1,self.windows):
            #print("i is",i)
            request_upper = self.computeI_kWithB(r,i,b)#计算I(k)
            #print("I(",i,") is",request_upper)
            request_lower = self.computeI_kWithB(r,i-1,b)#计算I(k-1)
            #print("I(",i-1,") is",request_lower)
            if request_lower==0 and request_upper ==0:
                localSum = self.workload[0]
            else:
                localSum = np.sum(self.workload[request_lower+1:request_upper+1])
            #print("localsum is",localSum)
                
            ck_list[i] = min(ck_list[i-1]+r*(self.time[i]-self.time[i-1])-localSum,b)
            
            if request_upper==i-1 and ck_list[i]>=self.workload[i]:
                qk_list[i] = 0
            else:
                qk_list[i] = np.sum(self.workload[request_upper+1:i+1])
                
        #self._qk_list = qk_list#第k个请求离开后，队列中剩余的请求个数
        #self._ck_list = ck_list#每个请求到达前，系统剩余的token数
        return [qk_list,ck_list]
    
    def computeqk_listAndck_listNoB(self,r,):
       '''compute I(k)
       the largest index k'<=k-1
       '''
       ck_list = np.zeros(self.windows)#第k个请求离开后，队列中剩余的请求个数
       qk_list = np.zeros(self.windows)#每个请求到达前，系统剩余的token数
       for i in range(0,self.windows):
           temp_token = self.c0 + r*(self.time[i]-self.t0)
           temp_requests = 0
           I_k = 0
           
     #***********计算截止的时间tk，系统成功发生的请求个数I_k
           #print("the requests index is",i)
           
           if i==0:#对i ==0进行特殊处理
               temp_requests = 0
               I_k = -1
               ck_list[i] = temp_token
               if temp_token<self.workload[i]:
                   qk_list[i]= self.workload[i]
               #print("token is",temp_token)
               #print("workload is",self.workload[i])
               continue
           
           for j in range(0,i):
               temp_requests = np.sum(self.workload[0:j+1])
               #print("*  token is",temp_token)
               #print("*  workload is",temp_requests)
               if temp_token<temp_requests:#token数不足
                   #print("token lack,just",i,"th can be send out")
                   break
               else:
                   I_k = j
                   #print("token enough to send",i)

           
     #**********计算pk到达前，即系统成功发生I_k个请求后，剩余的token数************     
           ck_list[i] = temp_token-sum(self.workload[0:I_k+1])#加和时包括I_k但是不包括I_k+1
           
    #***********计算pk到达后系统，队列内存储的请求数************************************
           if temp_token<(temp_requests+self.workload[i]):
               qk_list[i] = sum(self.workload[I_k+1:i+1])
               #print("I_k is",I_k)
      
       #self._qk_list = qk_list#第k个请求离开后，队列中剩余的请求个数
       #self._ck_list = ck_list#每个请求到达前，系统剩余的token数
       return [qk_list,ck_list]
    def computeQ(self,r):
        q = np.max(self.computeqk_list)
        #print("max size of the requests",self.q)
        #print("compute the q given r",q)
        return q
        
    def computeI_kWithB(self,r,k,b):
        if k>=1: 
           #print("****k is****",k)
           self._Ik_list[k] = self._Ik_list[k-1]
           for i in range(int(self._Ik_list[k-1]+1),k):
               token = min(self._ck_list[k-1]+r*(self.time[k]-self.time[k-1]),b)
               #print("token is",token)
               requests = np.sum(self.workload[self._Ik_list[k-1]+1:i+1])
               #print("requests is",requests)
               temp = token - requests
               #print("the remining token is",temp)
               if temp>=0:
                   self._Ik_list[k] = i
               else:
                   break
           last = self._ck_list[k-1]+r*(self.time[k]-self.time[k-1])-np.sum(self.workload[self._Ik_list[k-1]+1:self._Ik_list[k]+1])
           self._ck_list[k] = min(last,b)
        return self._Ik_list[k]
         
    def computeI_kNoB(self,r,k):
        if k>=self.windows:
            print("输入的请求索引越界")
        else:
            temp_token = self.c0 + r*(self.time[k]-self.t0)
            
            temp_requests = 0
            I_k = 0
            #print("k is",k)
     #***********计算截止的时间tk，系统成功发生的请求个数I_k

            for j in range(0,k):
                temp_requests += self.workload[j]
                #print("token is",temp_token)
                #print("request is",temp_requests)
                if temp_token<temp_requests:#token数不足
                    break
                else:
                    I_k = j
            return I_k  
            
    def computeJ_k(self,r,k,b = None,T = 1):
        '''
        the largest index that can be sent out
        before the kth requests
        T:当token不足时，补充token的强度和规模
        '''
        #**********计算前k个时段内积累的token个数***************
        if b==None:
            b = np.min(self.workload)
        tokenList = [0,]
        tokenList[0] = min(self.c0+r*(self.time[0]-self.t0),b)
        for i in range(1,k+1):
            tokenList.append( min(r*(self.time[i]-self.time[i-1]),b))
        tokens = np.sum(tokenList)
        
        #**********第k个请求到达后，系统要处理的请求数********
        requests = np.sum(self.workload[0:k+1])
        J_k = k
        print("initial tokens is",tokens)
        print("total requests are",requests)
        while tokens-requests<0:
            tokens+= r*T
            J_k+=1
            print("token is ",tokens)
        print("J_k is",J_k)
        
        return J_k
    def computeBRange(self,r,b = None):
        '''
        compute the maxinum value of B
        '''
     #************计算B的max*******************************
        ck_r = np.copy(self.workload)
        self.computeDelay(r)#获取延迟
        for i in range(0,self.windows):
            #print("i is",i)
            temp = self.c0+r*(self._delayTime[i]-self.t0)
            #print("token is ",temp)
            localSum = sum(self.workload[0:i])
            #print("requests is ",localSum)
            temp = temp-localSum
            #print("remining token",temp)
            if temp>=self.workload[i]:
                ck_r[i] = temp
        Bmax = np.max(ck_r)
        
    #*************计算B的min*******************
        
        Bmin = np.max(self.workload)
        if self.c0>Bmin:
            Bmin = self.c0
        return[Bmin,Bmax]
        
    def computeOptimalB(self,r,q = None):
        if q==None:
            q = self.q
        #***********使用折半查找进行确定，保证qk<q****************

        bRange = self.computeBRange(r)
        bl = bRange[0]
        bu = bRange[1]
        b = bl
        ck_list = self.computeqk_listAndck_listWithB(r = r,b = b)
        while int(bl)!=int(bu):
            b = (bl+bu)/2
            ck_list = self.computeqk_listAndck_listWithB(r = r,b = b)[1]
            print("ck_list is ",ck_list)
            for i in range(0,self.windows):
                if self.workload[i]>ck_list[i]:
                    break
            if i==self.windows-1:
                bu = b
            else:
                bl = b  
            b = (bl+bu)/2
        return b
        
        
    def computeGrowPeriod(self,r,start,end):
        pass
    def computeDelay(self,r,b = None):
        '''
        compute the delay of every packet
        '''
        temp_requests = 0
        self._delayTime = np.copy(self.time)
        for i in range(0,self.windows):
            temp_requests+=self.workload[i]
            temp = (temp_requests-self.c0)/r-(self.time[i]-self.t0)
            if temp<0:
                temp = 0
            self._delayTime[i] += temp        
    
    
    def GiveQComputRB(self,q):
        pass
#*************创建测试数据集********************
wrFile = WRFile()
filePath = "F:/result.xlsx"
cols = 1
data = wrFile.readDataFromExcel(filePath,cols,sheet_name = 2)
#data[6] = 200
time = np.arange(0,len(data))
result = np.vstack([data,time])
r = 400
b = 450
print("r is ",r,"b is" ,b)
#*************测试请求切分效果***********************
lager = LagerRequest(result,r =r)
q = 50

        #请求达到后，队列的存储情况
rrange = lager.computeRRange()

sample = np.linspace(rrange[0],rrange[1],2)
b_result = []
for i in range(0,2):
    b_optimal = lager.computeOptimalB(sample[i])
    b_range = lager.computeBRange(r = sample[i])
    print("r is",sample[i])
    print("the range of b is",b_range)
    print("the optimal b is",b_optimal)
print("sample is ",sample)
print("b_result is",b_result)
#plt.plot(sample,b_result)

''''
J_k = lager.computeJ_k(r= r,b = b,k = 8)
print("J_k is",J_k)
qk_list = lager.computeqk_listWithB(r,b)
print("the requests stored in the queue after the requests pk arrives",qk_list)
print("the token left before the pk arrives",lager._ck_list)
print("I(k)",lager._Ik_list)
print("the arrival pattern of the requests",data)
'''    
'''
qk_list = lager.computeqk_listWithB(r,b)
print("the requests stored in the queue after the requests pk arrives",qk_list)
print("the token left before the pk arrives",lager._ck_list)
print("I(k)",lager._Ik_list)
print("the arrival pattern of the requests",data)
       队列的延迟分析
print("data[6]",data[6])
lager.computeDelay(r) 
print("the arrival pattern of the requests",lager.time)  
print("the delay time for every requests",lager._delayTime)

qk_list = lager.computeqk_list(r)
print("r is",r)
print("data[6]",data[6])
#print("the requests stored in the queue after the requests pk arrives",qk_list)
#print("the token left before the pk arrives",lager._ck_list)
#print("the arrival pattern of the requests",data)
b = lager.computeBRange(r)
print(b)
'''   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
