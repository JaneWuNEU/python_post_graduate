# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 09:52:19 2016

@author: User
"""
class Problem:
        def computeJ_k(self,r,k,b = None,T = 1):
        '''
        the largest index that can be sent out
        before the kth requests
        T:当token不足时，补充token的强度和规模
        '''
        #**********计算前k个时段内积累的token个数***************
        if b==None:
            b = np.min(self.workload)
        tokenList = [0,]
        tokenList[0] = min(self.c0+r*(self.time[0]-self.t0),b)
        for i in range(1,k+1):
            tokenList.append(min(r*(self.time[i]-self.time[i-1]),b))
        tokens = np.sum(tokenList)
        
        #**********第k个请求到达后，系统要处理的请求数********
        requests = np.sum(self.workload[0:k+1])
        J_k = k
        #print("initial tokens is",tokens)
        #print("total requests are",requests)
        while tokens-requests<=0:
            tokens+=min(r*T,b)
            J_k+=1
            #print("token is ",tokens)
        #print("J_k is",J_k)
        return J_k

