# -*- coding: utf-8 -*-
"""
Created on Sun May 22 16:29:46 2016

@author: user
"""
import numpy as np
from sklearn.svm import SVR
import matplotlib.pyplot as plt
import pandas as pd
from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import GradientBoostingRegressor    
#
#dataSet = [18, 16, 17, 18, 15, 19, 15, 17, 17, 17, 15, 15, 18, 20, 20, 21, 19, 21, 23, 17, 19, 20, 22, 18, 22, 20,
#               22, 21, 22, 24, 21, 22, 20, 22, 21, 21, 19, 19, 18, 17, 20, 18, 18, 20, 16, 21, 17, 19, 19, 19, 17, 17,
#               20, 22, 22, 23, 21, 23, 26, 19, 21, 23, 24, 20, 24, 23, 25, 23, 24, 26, 23, 24, 23, 24, 23, 23, 21, 21,
#               20, 19, 22, 20, 20, 23, 18, 23, 19, 21, 21, 21, 18, 18, 22, 25, 24, 25, 24, 25, 28, 21, 23, 25, 27, 22,
#               26, 25, 27, 25, 26, 28, 25, 27, 25, 26, 25, 25, 23, 23, 22, 20, 24, 22, 22, 25, 20, 25, 21, 23, 23, 23,
#               20, 20, 24, 27, 26, 27, 26, 27, 31, 23, 25, 27, 29, 24, 28, 27, 30, 27, 29, 31, 28, 29, 27, 28, 27, 27,
#               25, 25, 24, 22, 26, 24, 24, 27, 22, 27, 22, 25, 25, 25, 22, 22, 26, 29, 29, 30, 28, 30, 33, 25, 27, 29,
#               31, 25, 31, 29, 32, 29, 31, 33, 30, 31, 29, 30, 29, 29, 27, 27, 26, 24, 28, 25, 26, 29, 23, 29, 24, 27,
#               27, 27, 23, 24, 29, 31, 31, 32, 30, 32, 36, 26, 29, 31, 34, 27, 33, 31, 34, 32, 33, 36, 32, 34, 31, 33,
#               31, 31, 29, 29, 28, 26, 30, 27, 28, 31, 25, 31, 26, 29, 28, 29, 25, 25, 31, 33, 33, 34, 32, 34, 38, 28,
#               31, 33, 36, 29, 35, 33, 37, 34, 35, 38, 34, 36, 33, 35, 33, 33, 31, 31, 29, 27, 32, 29, 30, 33, 27, 33,
#               28, 31, 30, 31, 27, 27, 33, 36, 35, 36, 34, 36, 40, 30, 33, 36, 38, 31, 38, 36, 39, 36, 38, 41, 36, 38,
#               35, 37, 35, 36, 33, 33, 31, 29, 35, 31, 32, 35, 28, 36, 29, 33, 32, 33, 28, 29, 35, 38, 37, 38, 36, 38,
#               43, 32, 35, 38, 41, 33, 40, 38, 41, 38, 40, 43, 39, 40, 37, 39, 38, 38, 35, 35, 33, 31, 37, 33, 34, 37,
#               30, 38, 31, 35, 34, 35, 30, 30, 37, 40, 39, 41, 38, 41, 45, 34, 37, 40, 43, 35, 42, 40, 44, 40, 42, 45,
#               41, 43, 40, 42, 40, 40, 37, 37, 35, 33, 39, 35, 35, 39, 32, 40, 33, 37, 36, 37, 32, 32, 39, 42, 42, 43,
#               40, 43, 48, 36, 39, 42, 45, 37, 44, 42, 46, 43, 44, 48, 43, 45, 42, 44, 42, 42, 39, 39, 37, 34, 41, 36,
#               37, 41, 33, 42, 34, 39, 38, 38, 33, 34, 41, 44, 44, 45, 42, 45, 50, 38, 41, 44, 47, 39, 47, 44, 48, 45,
#               47, 50, 45, 47, 44, 46, 44, 44, 41, 41, 39, 36, 43, 38, 39, 43, 35, 44, 36, 41, 40, 40, 35, 35, 43, 47,
#               46, 47, 44, 47, 53, 39, 43, 46, 50, 41, 49, 46, 51, 47, 49, 53, 47, 50, 46, 48, 46, 46, 43, 43, 41, 38,
#               45, 40, 41, 45, 37, 46, 38, 43, 42, 42, 37, 37, 45, 49, 48, 50, 47, 50, 55, 41, 45, 49, 52, 43, 51, 49,
#               53, 49, 51, 55, 50, 52, 48, 51, 48, 48, 44, 45, 43, 40, 47, 42, 43, 47, 38, 48, 40, 45, 44, 44, 38, 39,
#               47, 51, 50, 52, 49, 52, 58, 43, 47, 51, 54, 45, 54, 51, 55, 51, 54, 58, 52, 54, 50, 53, 50, 50, 46, 47,
#               44, 41, 49, 44, 45, 49, 40, 50, 41, 47, 46, 46, 40, 40, 49, 53, 52, 54, 51, 54, 60, 45, 49, 53, 57, 47,
#               56, 53, 58, 53, 56, 60, 54, 56, 52, 55, 53, 53, 48, 49, 46, 43, 51, 46, 47, 51, 42, 52, 43, 49, 47, 48,
#               42, 42, 51, 55, 55, 56, 53, 56, 63, 47, 51, 55, 59, 48, 58, 55, 60, 56, 58, 62, 56, 59, 54, 57, 55, 55,
#               50, 51, 48, 45, 53, 48, 49, 54, 44, 55, 45, 51, 49, 50, 43, 44, 53, 57, 57, 59, 55, 59, 65, 49, 53, 57,
#               61, 50, 60, 57, 63, 58, 60, 65, 58, 61, 57, 59, 57, 57, 52, 53, 50, 47, 55, 49, 51, 56, 45, 57, 47, 52,
#               51, 52, 45, 45, 55, 60, 59, 61, 57, 61, 68, 51, 55, 59, 64, 52, 63, 59, 65, 60, 63, 67, 61, 63, 59, 62,
#               59, 59, 54, 55]
#               
dataset = [18, 16, 17, 18, 15, 19, 15, 17, 17, 17, 15, 15, 18, 20, 20, 21, 19, 21, 23, 17, 19, 20, 22, 18, 22, 20,
               22, 21, 22, 24, 21, 22, 20, 22, 21, 21, 19, 19, 18, 17, 20, 18, 18, 20, 16, 21, 17, 19, 19, 19, 17, 17,
               20, 22, 22, 23, 21, 23, 26, 19, 21, 23, 24, 20, 24, 23, 25, 23, 24, 26, 23, 24, 23, 24, 23, 23, 21, 21,
               20, 19, 22, 20, 20, 23, 18, 23, 19, 21, 21, 21, 18, 18, 22, 25, 24, 25, 24, 25, 28, 21, 23, 25, 27, 22,
               26, 25, 27, 25, 26, 28, 25, 27, 25, 26, 25, 25, 23, 23, 22, 20, 24, 22, 22, 25, 20, 25, 21, 23, 23, 23,
               20, 20, 24, 27, 26, 27, 26, 27, 31, 23, 25, 27, 29, 24, 28, 27, 30, 27, 29, 31, 28, 29, 27, 28, 27, 27,
               25, 25, 24, 22, 26, 24, 24, 27, 22, 27, 22, 25, 25, 25, 22, 22, 26, 29, 29, 30, 28, 30, 33, 25, 27, 29,
               31, 25, 31, 29, 32, 29, 31, 33, 30, 31, 29, 30, 29, 29, 27, 27, 26, 24, 28, 25, 26, 29, 23, 29, 24, 27,
               27, 27, 23, 24, 29, 31, 31, 32, 30, 32, 36, 26, 29, 31, 34, 27, 33, 31, 34, 32, 33, 36, 32, 34, 31, 33,
               31, 31, 29, 29, 28, 26, 30, 27, 28, 31, 25, 31, 26, 29, 28, 29, 25, 25, 31, 33, 33, 34, 32, 34, 38, 28,
               31, 33, 36, 29, 35, 33, 37, 34, 35, 38, 34, 36, 33, 35, 33, 33, 31, 31, 29, 27, 32, 29, 30, 33, 27, 33,
               28, 31, 30, 31, 27, 27, 33, 36, 35, 36, 34, 36, 40, 30, 33, 36, 38, 31, 38, 36, 39, 36, 38, 41, 36, 38,
               35, 37, 35, 36, 33, 33, 31, 29, 35, 31, 32, 35, 28, 36, 29, 33, 32, 33, 28, 29, 35, 38, 37, 38, 36, 38,
               43, 32, 35, 38, 41, 33, 40, 38, 41, 38, 40, 43, 39, 40, 37, 39, 38, 38, 35, 35, 33, 31, 37, 33, 34, 37,
               30, 38, 31, 35, 34, 35, 30, 30, 37, 40, 39, 41, 38, 41, 45, 34, 37, 40, 43, 35, 42, 40, 44, 40, 42, 45,
               ]   
#dataset = [12,13,13,13,13,13,13,13,13,13,13,13,14,15,14,14,13,14,14,15,16,17,15,16,15,16,17,19,16,17,17,17,15,16,15,16,17,18,
#           17,18,19,20,17,19,22,22,19,19,20,21,24,25,21,22,18,20,22,22,20,21,22,23,23,23,23,25,25,26,26,28,24,26,26,27,26,29,24,27,24,26,25,26,27,28,26,27,24,27,28,29,25,28,28,31,27,28,29,31,34,37,29,33,29,32,30,32,31,31,31,36,28,32,30,35,31,32,33,36,30,34,34,35,42,42,30,35,29,30,29,33,29,33,36,36,31,34,31,35,32,35,36,42,36,38,36,37,43,43,34,36,30,32,37,39,38,40,39,44,41,43,38,44,38,
#           44,45,51,44,45,42,45,40,42]



#
data1 = []
data2 = []
i = 0
j = 1
while i <len(dataset):
    data1.append(dataset[i])
    i = i+2
while j <len(dataset):
    data2.append(dataset[j])
    j = j+2



#print data1
#print data2

#    
X = np.arange(len(data1)).reshape(-1, 1)#相当于时间点
y = np.array(data1)#每个时刻对应的并发量的值
XX = np.arange(len(data2)).reshape(-1, 1)#相当于少了一个时间点
#
def svr_rbf(X, y, XX):
    svr_rbf = SVR(kernel='rbf', C=1e5, gamma=1)
    y_rbf = svr_rbf.fit(X, y).predict(XX)
    return y_rbf
def svr_lr(X, y, XX):
    svr_rbf = SVR(kernel='rbf', C=1e3, gamma=5)
    y_rbf = svr_rbf.fit(X, y).predict(XX)
    return y_rbf

def lr(X, y, XX):
    regr1 = linear_model.LinearRegression()#
    
    y_regr1 = regr1.fit(X, y).predict(XX)
    return y_regr1

def tree(X, y, XX):
    tree1 = RandomForestRegressor(n_estimators=2, max_depth=20)#
    
    y_tree1 = tree1.fit(X, y).predict(XX)
    return y_tree1

def gbdt(X, y, XX):
    tree1 = GradientBoostingRegressor()#
    
    y_tree1 = tree1.fit(X, y).predict(XX)
    return y_tree1




pre = svr_lr(X, y, XX)
print(pre)

fig = plt.figure(figsize=(12, 8))
plt.plot(XX,data2)  #对应的原始数据 
plt.plot(XX, pre,'r')

#fig = plt.figure(figsize=(12, 8))
#plt.plot(dataSet)