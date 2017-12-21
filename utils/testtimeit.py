# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 14:27:22 2017

@author: User
"""
import timeit



filePath = "F:/test/workload.xlsx"
num = [0.5,1,2,8]
for i in range(0,4):
    start(filePath=filePath,queue_num = num[i])
    fun_text = "start(self,filePath="+filePath+",queue_num="+str(num[i])+")"
    print(timeit.timeit(fun_text, 'from __main__ import start',number = 1))