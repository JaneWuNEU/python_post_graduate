# -*- coding: utf-8 -*-
"""
Created on Thu Jul  6 20:30:15 2017

@author: User
"""
import sys
sys.path.append("D:/anaconda/project/utils")
import numpy as np
from utils import WRFile
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
def splitOnlineData():
    shopName = ["京东商城","天猫商城","亚马逊商城","淘宝商城"]
    #读出所有数据，然后都存放到
    # 1.生成日期数据
    
    wrFile = WRFile()
    data = wrFile.readDataFromExcel(filePath = "F:\\data\\orginal\\online.xlsx",sheet_name="online",cols=3)
    #2. 对数据进行切片
    jingdong = []
    tmall = []
    amazon = []   
    taobao = []
    for i in range(len(data)):
        count = i%4
        if count ==0:
            if data[i]>0:
                jingdong.append(data[i])
            else:
                jingdong.append(data[i-4])
        elif count==1:
            if data[i]>0:
                tmall.append(data[i])
            else:
                tmall.append(data[i-4])
        elif count ==2:
            if data[i]>0:
                amazon.append(data[i])
            else:
                amazon.append(data[i-4])
        elif count ==3:
            if data[i]>0:
                taobao.append(data[i])
            else:
                taobao.append(data[i-4])
    #3.将数据写入excel
    fileRoot ="F:\\data\\online/"
    filesuffix =".xlsx"
    wrFile.writeDataIntoExcel(data = jingdong,filePath=fileRoot+"jingdong"+filesuffix)
    wrFile.writeDataIntoExcel(data = tmall,filePath=fileRoot+"tmall"+filesuffix)
    wrFile.writeDataIntoExcel(data = amazon,filePath=fileRoot+"amazon"+filesuffix)
    wrFile.writeDataIntoExcel(data = taobao,filePath=fileRoot+"taobao"+filesuffix)
    
wrFile = WRFile()
fileName ="taobao"
data = wrFile.readDataFromExcel(filePath="F:\\data\\online/"+fileName+".xlsx", sheet_name="Sheet1",cols=2)
pre = wrFile.readDataFromExcel(filePath="F:\\data\\online\\predict/exp.xlsx", sheet_name="Sheet1",cols=3)
plt.plot(np.arange(len(data)),data)
plt.plot(np.arange(len(pre)),pre)
plt.legend(["r","p"])