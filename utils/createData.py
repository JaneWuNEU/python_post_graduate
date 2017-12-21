# -*- coding: utf-8 -*-
"""
Created on Thu Sep  8 19:03:09 2016

@author: User
"""
import numpy as np
import random
import matplotlib.pyplot as plt
import sys
sys.path.append("D:/anaconda/project/")
from utils import WRFile
class CreateData:
    """
    create the data with special characteristics
    including 
    whitenoise data
    period data
    trend data
    compound data
    """

    """
    to create the data fitting Normal Distribution
    @mean  the mean of the data
    @var   the variance of the data
    @num   the quantity of the data
    """
    def createWhiteNosie(self,mean,var,num):
        result = numpy.random.normal(mean,var,size = num)
        print(len(result))
        return result
        
    """
    to create the bursty data,and the user provides the times and
    intensity of the burst
    """
    def createBurtyData(self,times,intensity,original_data):
        result = list(original_data)
        num = len(original_data)
        for i in range(0,times):
            burstPoint = random.randint(0,num-1)
            result[burstPoint] = result[burstPoint]*random.randint(1,intensity)
        plt.plot(range(0,len(result)),result[0:len(result)],"b")
                                                       
        return result
    def sinData():
        x = np.linspace(1, 20, 100)
        f = 20*np.sin(x)-(x-10)**2+100#+np.random.normal(5,2,100)
        return [x,f]
    def getDerivate():
        x = np.linspace(1, 50, 100)
        f = 20*np.sin(x)-(x-25)**2+100#+createWhiteNosie(mean = 4,var = 2,size = 100)
        f1 = 20*np.cos(x)-2*x+20
        return f1
    def createRandomInt(self,low,high,amount):
        result = []
        for i in range(amount):
            result.append(random.randint(low,high))
        return result
#data = CreateData()
#result = data.createRandomInt(19,22,30)
#result = data.createBurtyData(times=2,intensity=2,original_data = result)
#data = [22, 20, 19, 21, 22, 19, 22, 20, 38, 15, 20, 20, 22, 22, 22, 21, 21, 19, 20, 22, 22, 19, 20, 22, 19, 22, 20, 22, 19, 19]
#plt.plot(np.arange(len(data)),data)