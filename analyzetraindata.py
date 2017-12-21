# -*- coding: utf-8 -*-
"""
Created on Thu May  4 14:04:37 2017

@author: User
"""
import sys
sys.path.append("D:/anaconda/project/utils")
import numpy as np
from utils import WRFile
import matplotlib.pyplot as plt 
wrFile = WRFile()
def analyzedata():
    filePath = "D:\\cloudsim\\log\\workload/workload53modified.xlsx"
   
    data = wrFile.readDataFromExcel(filePath,cols = 1,sheet_name = "sheet")
    per = [50,90,95,100]
    for i in per:
        print(i,"th  is",np.percentile(data,i))
    plt.plot(np.arange(len(data)),data,"m-")
def showData(filePath,title,xlabel,ylabel,sheet):
    data = wrFile.readDataFromExcel(filePath = filePath,cols = 1,sheet_name = sheet)
    plt.plot(np.arange(len(data)),data,"B")
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    
def showSubPlot(axi,filePath,title,xlabel,ylabel,sheet,fontsize):
    data = wrFile.readDataFromExcel(filePath = filePath,cols = 1,sheet_name = sheet)

    axi.plot(np.arange(len(data)),data)
    axi.set_title(title,fontsize = fontsize)
    axi.set_xlabel(xlabel,fontsize = fontsize )
    axi.set_ylabel(ylabel,fontsize = fontsize)
filePath = "D:\\cloudsim\\log/vm.xlsx"
title = "vm amount"
xlabel = "time"
ylabel = "vm amount"
sheet="sheet"
showData(filePath,title,xlabel,ylabel,sheet)
