                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                        # -*- coding: utf-8 -*-
"""
Created on Wed Oct 26 11:22:48 2016

@author: User
"""
import matplotlib.pyplot as plt
from utils import WRFile

wrFile = WRFile();

filePath = "F:/lab/source/data/library/1.xlsx"
cols = 1
original_data = wrFile.readDataFromExcel(filePath=filePath,cols=cols,sheet_name = "1")
print(original_data)
#把数据以100为单位进行切分
'''segement = -1
segement_data = []
for i in range(len(original_data)):
    if i%500==0:
        segement = segement+1
        if(segement!=1):
            wrFile.writeDataIntoExcel(data = segement_data,filePath = filePath,cols = segement,sheet_index = 1)
            segement_data.clear()
        print(segement)
    segement_data.append(original_data[i])
'''    