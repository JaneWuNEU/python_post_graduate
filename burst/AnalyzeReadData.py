# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 22:09:06 2017

@author: User
"""
import sys
sys.path.append("D:/anaconda/project/utils")
from utils import WRFile
import timeit
def analyzeReadData():
     filePath = "F:/test/workload63_69.xlsx"
     wrFile = WRFile()
     wrFile.readDataFromExcel(filePath = filePath,sheet_name="1")
fuc_test = "analyzeReadData()"
print(timeit.timeit(fuc_test,'from __main__ import analyzeReadData',number = 1))