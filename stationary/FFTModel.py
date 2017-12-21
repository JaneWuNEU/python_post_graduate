# -*- coding: utf-8 -*-
"""
Created on Sun Feb 19 21:15:50 2017

@author: User
"""
import numpy as np
import matplotlib.pyplot as plt 
import sys
sys.path.append("D:/anaconda/project/utils")
from utils import WRFile
from scipy.stats.stats import pearsonr
import scipy.fftpack as fft
import pandas as pd

class FFTPredict:
    
        
    def FFTofNoBurst(self,dataA , dataB ):
        #对数据进行FFT转换
        freqA = np.fft.fft(dataA)
        freqB = np.fft.fft(dataB) 
        factor = 0.5
        freq_p = (1-factor)*freqA[1:]+factor*freqB[1:]
        predict = np.fft.ifft(freq_p)
        predict += np.ones(len(dataA)-1)*(np.mean(dataA)+np.mean(dataB))/2
        return predict
        
    def FFTofWFD(self,dataA ,dataB ):
         #对数据进行FFT转换
        freqA = np.fft.fft(dataA)
        freqB = np.fft.fft(dataB) 
        #获取突发的终止点
        factor = 0.8
        freqB = (1-factor)*freqA+factor*freqB
        predict = np.fft.ifft(freqB)
        return predict
