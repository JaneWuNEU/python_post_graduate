# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 08:13:06 2017

@author: User
"""
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from matplotlib.pylab import rcParams
filePath = "F:/test.xlsx"
sheetname = "1"
data = pd.read_excel(io = filePath,sheetname = sheetname )
print(data.head())
#print("data ",data)


