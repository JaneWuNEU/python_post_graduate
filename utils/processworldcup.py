# -*- coding: utf-8 -*-
"""
Created on Fri Jan 13 16:19:14 2017

@author: User
"""
'''
filePath = "F:/worldcup/test.txt"
file = open(filePath,'r')
lines = len(file.readlines())
print(lines)

data = []
file = open(filePath,'r')
for i in range(0,lines):
    temp = file.readline()
    if i%5==0:
        temp = temp[7:21]
        temp = temp.replace(" ","")
        data.append(temp)
file.close()
print(data)
'''
import urllib 
import numpy as np
def downloadData():
    fileList = dataList()
    url = 'ftp://ita.ee.lbl.gov/traces/WorldCup/'
    for i in range(0,len(fileList)):
        data = urllib.request.urlretrieve(url+fileList[i] ,"F:/worldcup/"+fileList[i])
       
def dataList():
    dataList =[]

    begin = "wc_day"
    end = ".gz"
    subFile = [4,9,6,6,6,5]
    mainFile = np.arange(50,56).tolist()
    print(mainFile)
    time3 = []
    for i in range(0,6):
        k = 0
        while k<subFile[i]:
            time3.append(str(mainFile[i])+"_"+str(k+1))      
            k+=1
    fileName = begin
    for j in range(0,len(time3)):
        fileName = fileName+time3[j]+end
        dataList.append(fileName)
        fileName = begin
    print(len(dataList))
    print(dataList)
    return dataList
def parseFile():
    dataList =[]

    begin = "gzip -dc input/wc_day"
    middle = ".gz | bin/recreate state/object_mappings.sort > output/wc_day"
    end = ".out"
    subFile = [4,9,6,6,6,5]
    mainFile = np.arange(50,56).tolist()
    print(mainFile)
    time3 = []
    for i in range(0,6):
        k = 0
        while k<subFile[i]:
            fileName = str(mainFile[i])+"_"+str(k+1)
            print(begin+fileName+middle+fileName+end)
            k+=1

    
#downloadData()
dataList()