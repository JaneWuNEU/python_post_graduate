# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 15:52:02 2016

@author: User
"""
class Bucket:
    '''
     每个Bucket有3个重要指标:创建队列，token的更新速率，token的最大尺寸
     队列存放的请求的比例数prop也不可变
    '''
    def __init__(self,replenishRate,maxSize,prop):
      self._replenishRate = replenishRate
      self.__maxSize = maxSize
      #self._queue = queue.Queue()
      self._queue = [0,]
      self.__prop = prop
      self._LastUpdateTime = 0
      self._ElapsedTime = 0
      self._tokenNum = maxSize
    #每个bucket的最大长度不可修改
      '''
    @property
    def __maxSize(self):
        return self.__maxSize
    #队列存放的请求对应的比例不能变
    @property
    def __prop(self):
        return self.__prop
        '''
#********获取bucket对应的各项参数****************************
        
    #获取当前token的更新速率
    def getReplenishRate(self):
        return self._replenishRate
    #获取当前bucket对应的token的最大个数
    def getMaxTokenNum(self):
        return self.__maxSize
    #获取该bucket对应的要求存放的请求数
    def getProp(self):
        return self.__prop
    #获取bucket对应的队列
    def getQueue(self):
        return self._queue
        
    def getTokenNum(self):
        return self._tokenNum
#*********************************************************
        
#***********更新bucket中的token个数************************  
    def updateBucket(self,time):
        ElapsedTime = time-self._LastUpdateTime
        self._LastUpdateTime = time
        self._tokenNum += ElapsedTime*self.getReplenishRate()
        if self._tokenNum>self.getMaxTokenNum():
            self._tokenNum = self.getMaxTokenNum()
#*********************************************************
         
    
class ClassifyBurst:
    def __init__(self,bucketList):
        self._bucketList = bucketList
        self.__bucketNum = len(bucketList)   
    def storeRequest(self,workload,time):
#        temp = None
        discardQueue = 0 
       #更新bucket
        for bucketId in range(self.__bucketNum-1,-1,-1):
            self._bucketList[bucketId].updateBucket(time)
            print("第",bucketId,"个bucket的token个数为",self._bucketList[bucketId].getTokenNum())
        for j in range(0,workload):
            for bucketId in range(self.__bucketNum-1,-1,-1):
                temp = bucketId
                bucket = self._bucketList
                #print("tokens in bucket ",bucketId,"is ",bucket[temp].getTokenNum(),"when request",j,"arrive")
                if bucket[temp].getTokenNum()>=1:
                    bucket[temp]._tokenNum-=1
                else:
                    #print("at time",time,"there is no token in bucket ",temp,"current request is",j)
                    break

            if temp==self.__bucketNum-1:
                pass
                discardQueue+=1
            else:
                q = bucket[temp+1].getQueue()
                if time==len(q)-1:
                    q[time]+=1
                elif time==len(q):
                    q.append(1)
                elif time>len(q):
                    while len(q)<time:
                        q.append(0)
                    q.append(1)
                    #print("error---->time is ",time,"queue size is ",len(q))
        self.showQueueStore(discardQueue)
    def showQueueStore(self,discardQueue):
        for bucketId in range(self.__bucketNum-1,-1,-1):
            print("token num is",self._bucketList[bucketId]._tokenNum)
            print("in bucket ",bucketId,"stores ",self._bucketList[bucketId].getQueue())
        print("discard requests is ",discardQueue)
        
    def storeAnalyze(self):
        for bucketId in range(self.__bucketNum-1,-1,-1):
            tempSum = 
            
bucket3 = Bucket(50,70,1)
bucket2 = Bucket(30,50,0.9)
bucket1 = Bucket(20,30,0.8)
bucket0 = Bucket(0,0,0)
bucketList = list()
bucketList.append(bucket0)
bucketList.append(bucket1)
bucketList.append(bucket2)
bucketList.append(bucket3)
workload = [20,30,100,35,40,70,100]
#workload = [40,100,100]
classifyBurst = ClassifyBurst(bucketList)
for i in range(0,len(workload)):
    classifyBurst.storeRequest(workload[i],i)

























