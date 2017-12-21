# -*- coding: utf-8 -*-
"""
Created on Thu Mar 02 16:15:55 2017

@author: User
"""

import pandas as pd
import numpy as np
from scipy import  stats
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.graphics.api import qqplot
dta=[10930,10318,10595,10972,7706,6756,9092,10551,9722,10913,11151,8186,6422, 
6337,11649,11652,10310,12043,7937,6476,9662,9570,9981,9331,9449,6773,6304,9355, 
10477,10148,10395,11261,8713,7299,10424,10795,11069,11602,11427,9095,7707,10767, 
12136,12812,12006,12528,10329,7818,11719,11683,12603,11495,13670,11337,10232, 
13261,13230,15535,16837,19598,14823,11622,19391,18177,19994,14723,15694,13248, 
9543,12872,13101,15053,12619,13749,10228,9725,14729,12518,14564,15085,14722, 
11999,9390,13481,14795,15845,15271,14686,11054,10395]
dta=pd.Series(dta)
dta.index = pd.Index(sm.tsa.datetools.dates_from_range('2001','2090'))
fig = plt.figure(figsize=(12,8))
dta.plot(figsize=(12,8))
#差分平稳化
ax1= fig.add_subplot(111)
diff1 = dta.diff(1)
diff1.plot(ax=ax1)#一阶差分
diff1.dropna(inplace=True)
dta=diff1
#fig = plt.figure(figsize=(12,8))
#用函数选择最佳阶数
'''ax2= fig.add_subplot(111)
diff2 = diff1.diff(2)#二阶差分
diff2.dropna(inplace=True)
diff2.plot(ax=ax2)

res=sm.tsa.arma_order_select_ic(dta,ic=['aic', 'bic'], trend='nc')
print(res.aic_min_order)
print(res.bic_min_order)
'''
#画acf  pacf图  选择阶数
fig = plt.figure(figsize=(12,8))
ax1=fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(diff1,lags=40,ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(diff1,lags=40,ax=ax2)

#定阶
arma_mod70 = sm.tsa.ARMA(dta,(7,0)).fit()
'''print(arma_mod70.aic,arma_mod70.bic,arma_mod70.hqic)
arma_mod30 = sm.tsa.ARMA(dta,(3,2)).fit()
print(arma_mod30.aic,arma_mod30.bic,arma_mod30.hqic)
arma_mod71 = sm.tsa.ARMA(dta,(7,1)).fit()
print(arma_mod71.aic,arma_mod71.bic,arma_mod71.hqic)
arma_mod80 = sm.tsa.ARMA(dta,(8,0)).fit()
print(arma_mod80.aic,arma_mod80.bic,arma_mod80.hqic)'''
#残差序列检验
#看到序列基本为白噪声
resid = arma_mod70.resid #原文把这个变量赋值语句漏了，所以老是出错
fig = plt.figure(figsize=(12,8))
ax1 = fig.add_subplot(211)
fig = sm.graphics.tsa.plot_acf(resid.values.squeeze(), lags=40, ax=ax1)
ax2 = fig.add_subplot(212)
fig = sm.graphics.tsa.plot_pacf(resid, lags=40, ax=ax2)

#D-W检验:证明残差序列不存在自相关性
print(sm.stats.durbin_watson(arma_mod70.resid.values))

#观察是否符合正态分布
print(stats.normaltest(resid))
fig = plt.figure(figsize=(12,8))
ax = fig.add_subplot(111)
fig = qqplot(resid, line='q', ax=ax, fit=True)

#残差序列Ljung-Box检验，也叫Q检验（prob 均大于0.05，所以序列不存在自相关性）
r,q,p = sm.tsa.acf(resid.values.squeeze(), qstat=True)
data = np.c_[range(1,41), r[1:], q, p]
table = pd.DataFrame(data, columns=['lag', "AC", "Q", "Prob(>Q)"])
print(table.set_index('lag'))

#预测
predict_dta = arma_mod70.predict('2090', '2100', dynamic=True)
print(predict_dta)


fig, ax = plt.subplots(figsize=(12, 8))
ax = dta.ix['2000':].plot(ax=ax)
fig = arma_mod70.plot_predict('2090', '2100', dynamic=True, ax=ax, plot_insample=False)





