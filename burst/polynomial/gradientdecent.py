# -*- coding: utf-8 -*-
"""
Created on Sat Oct 29 21:44:35 2016

@author: User
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d as interp
import sys
import scipy.optimize
'''
data 为原始数据
theta为每次的补偿，循环的终止条件是前后的梯度插值小于设置的阈值
'''
def getAllLocalValue(precision,dx,y):
    '''
    functionality:
    using difference to get the derivate of the data
    
    parameter:
    precision:there is no value that is absolutely equal to zero
              ,and we can only using a small value to nearly expression
               zero
               
    return:
    result = {"local_max":local_max,
    "local_min":local_min,"local_platform":local_platform}
    the value of every key is a list storing the index
    
    '''
    dydx = np.diff(y,dx)
    plt.plot(dydx,"--")
    plt.plot(y)
    limit = np.argwhere(abs(dydx)<precision)
    neibor = 5
    local_max = []
    local_min = []
    local_platform = []
    result = {"local_max":local_max,"local_min":local_min,"local_platform":local_platform};
    for i in range(len(limit)):
        temp = limit[i][0]
        left = sum(dydx[temp-neibor:temp-1])/neibor
        right = sum(dydx[temp+1:temp+neibor])/neibor
        #进入平台区
        if(np.abs(right)<precision):
            print("enter the platform from the current position",temp)
            result["local_platform"].append(temp)
        elif( left>precision and right<precision and np.abs(right)>precision):
            print(temp,"is the local max")
            result["local_max"].append(temp)
        elif(left<precision and abs(left)>precision and right>precision):
            print(temp," is the local min")
            result["local_min"].append(temp)
    return result
def getFirstLLocalMin(y,dx,precision,windows = 30,neibor = 3):
    '''
    functionality:
    find the first local min on the left of the last one in the y
    then continue to search the neigbor values from the local min to check
    whether there is a smaller one
    
    parameter:
    steps has a default value 5
    windows has a default value 30,whitch means that we only need
    to check the 30 values on the left of the last one of y
    
    return: 
    a dictionary,the key of which is the index of the local min
    '''
    dydx = np.diff(y[len(y)-windows:len(y)-1],dx)
    plt.plot(y)
    limits = np.argwhere(abs(dydx)<precision)
    local_min_value = y[len(y)-windows]
    local_min_index = 0
    
    end = len(limits)
    j = end-1
    reversedLimits = []
    while j>0:
        reversedLimits.append(limits[j][0])
        
    for i in range(len(reversedLimits)):
        temp = reversedLimits[j]    
        #caculate the neigborhood fields
        left = sum(dydx[temp-neibor:temp-1])/neibor
        right = sum(dydx[temp+1:temp+neibor])/neibor
        #check if satisfy the limit rules
        if(left<precision and abs(left)>precision and right>precision):
            if y[temp+1]<local_min_value:
                local_min_index = temp+1
                local_min_value = y[temp]
                print("相对位置是", local_min_index,"局部最小值是",local_min_value)
    relative_location = len(dydx)-local_min_index
    print("相对位置是", local_min_index,"局部最小值是",local_min_value)
    return{"fl_relative_index":relative_location,"fl_value":local_min_value}

    
sys.path.append("D:/anaconda/project/utils")
from createData import CreateData as cd
y = cd.sinData()[1][0:50]
#y = [97, 94, 85, 90, 85, 94, 86, 91, 95, 87, 96, 89, 86, 99, 85, 100, 93, 94, 100, 98, 88, 93, 99, 91, 94, 94, 88, 86, 94, 86, 88, 89, 96, 100, 99, 100, 93, 92, 99, 96, 85, 88, 100, 99, 88, 94, 98, 91, 88, 95, 102, 107, 101, 110, 107, 111, 112, 113, 116, 125, 123, 126, 141, 138, 132, 136, 148, 142, 154, 149, 151, 161, 167, 171, 171, 173, 174, 181, 186, 190, 90, 92, 97, 86, 95, 89, 90, 87, 86, 88, 92, 88, 94, 100, 99, 93, 96, 91, 91, 95, 88, 94, 85, 86, 86, 97, 98, 87, 85, 93, 88, 93, 85, 94, 100, 89, 89, 95, 90, 87, 85, 86, 86, 96, 86, 87, 98, 95, 93, 95, 100, 89, 92, 92, 88, 91, 96, 95, 86, 86, 100, 85, 90, 89, 91, 99, 100, 90, 98, 100, 100, 104, 99, 106, 111, 112, 118, 117, 115, 121, 125, 129, 131, 119, 128, 129, 138, 142, 132, 140, 139, 148, 148, 144, 147, 158, 150, 158, 153, 155, 96, 86, 86, 99, 95, 87, 93, 99, 97, 92, 92, 87, 88, 88, 92, 86, 96, 85, 99, 100]
#print(y)

dx = 0.01
getFirstLLocalMin(y,dx,precision = 0.8,windows = 50,neibor = 3)

