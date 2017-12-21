# -*- coding: utf-8 -*-
"""
Created on Sun Jan 15 18:08:21 2017

@author: User
"""
import os
filePath = "F:/worldcup"
fileList = os.listdir(filePath)#获取文件列表
print(len(fileList))
result = []
begin= "gzip -dc input/"
middle = ".gz | bin/recreate state/object_mappings.sort > output/"
end = ".out"
for i in range(0,len(fileList)):
    fileName = str(fileList[i])
    split = fileName.rfind("_")
    
    day = int(fileName[6:split])
    if day<57:        
        fileName = fileName.replace(".gz","")
        fileName = begin+fileName+middle+fileName+end
    elif day>63:
        fileName = fileName.replace(".gz","")
        fileName = begin+fileName+middle+fileName+end
    else:
        continue
    print(fileName)
    
    