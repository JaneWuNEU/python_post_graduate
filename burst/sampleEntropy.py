# -*- coding: utf-8 -*-


import math
import numpy as np
class SampleEntropy:
   def sampen2(self,data, m=2, r=0.2):

    n = len(data)

    if n == 0:
        raise ValueError("Parameter `data` contains an empty list")

    if m > n / 2:
        raise ValueError(
            "Maximum epoch length of %d too large for time series of length "
            "%d (mm > n / 2)" % (
                m,
                n,
            )
        )
    #print("m is",m," r is",r)
    #以秒为单位统计数据
    data = np.array(data)
    B = 1
    for i in range(0,n-m+1):
        for j in range(i+1,n-m+1):
            temp = np.max(np.abs(data[i:i+m])-data[j:j+m])
            if temp<=r:
                B+=1
    m+=1
    A = 1
    for i in range(0,n-m+1):
        for j in range(i+1,n-m+1):
            temp = np.max(np.abs(data[i:i+m])-data[j:j+m])
            if temp<=r:
                A+=1
    result = abs(-math.log(A/B))
    return result