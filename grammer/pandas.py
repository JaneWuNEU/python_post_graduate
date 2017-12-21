# -*- coding: utf-8 -*-
"""
Created on Mon Feb 13 11:19:22 2017

@author: User
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
s = pd.Series([1,2,4])
dates = pd.date_range('20140101',periods = 5,freq='M')
print(dates)
print(s)