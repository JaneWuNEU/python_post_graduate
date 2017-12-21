# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 10:26:33 2017

@author: User
"""
import numpy as np
from scipy import stats
import pandas as pd
from pandas import Series,DataFrame
import matplotlib as plt
import statsmodels as sm
from statsmodels.graphics.api import qqplot
data = sm.datasets.sunspots.load_pandas().data
del data['YEAR']
data = data['SUNACTIVITY']
print(data)
time = list(range(1700,2008,1))
print(time)
data = Series(data = data,index = time)
print(data)
