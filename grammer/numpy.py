# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 15:17:19 2016

@author: User
"""
import numpy as np
from scipy.optimize import leastsq
'''
a = np.arange(15).reshape(3,5)
print(a)
print(a.shape,a.ndim)
print(a.size)#数组的个数

b = np.array([6,7,8])
c = np.array([(1,2),(4,5),(4,5)])
d = c.reshape(2,3)

#用来进行初始化的函数
a = np.zeros((3,2))
b = np.ones((4,3))
c = np.empty((2,3))

#以矩阵单位的对各个数组元素进行操作
c = a-b
d = b**2
e = 10*np.sin(a)
f = a<35


# 进行矩阵间的运算
np.dot(a,b)
a*b
a = np.ones(3,dtype = np.int32)
b = np.linspace(0,5,5)
c = a+b
d = np.exp(c)

#生成随机函数
a = np.array([20,30,40,50])
b = np.arange(4)
a = np.ones((2,3),dtype = int)
b = np.random.random((2,3))
a+=3
b+=a

#以轴为单位进行操作
b = np.arange(12).reshape(3,4)
c = b.sum(axis = 0)
a = b.min(axis = 1)

#常用的数据函数：指数、开方;所有的这些函数都会生成一个新的ndarray
a = np.arange(3)
b = np.exp(a)
c = np.sqrt(a)
d = b+c
'''
#***********进行索引和切片***************************
def f(x,y):
    return x
'''
b = np.fromfunction(f,(5,2),dtype = int)
b[1,0] = 30
c = (4,5)
print(c[0])

a = np.arange(15).reshape(5,3)
print(a)
print(a[:][0])
'''

                                                                                                                                                                                                                  
a = np.array([-2,1,1,1,-2,1,1,1,-2]).reshape(3,3)
b = np.array([2,1,0,0,2,2,1,0,2,2,2,1]).reshape(3,4)
f = a.dot(b)
print(f)



























