# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 15:13:30 2017

@author: User
"""
import os
import chardet
filePath = "F:/FIFA/data"
#获取文件列表
fileList = os.listdir(filePath)
data = []
for i in range(0,2):
    fileObject = open(filePath+"/"+fileList[i],'r',encoding = "utf-8")
    while True:
        try:
            file = fileObject.readline()
            if not file:
                break
            else:
                
        except UnicodeDecodeError:
            print("删除该条数据")
        
    #读取每行数据
    for j in range(0,):
        row = file[j]
        local = row.rfind(":")
    
    fileObject.close()#关闭当前文件夹