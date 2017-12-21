import sys
sys.path.append("D:\\anaconda\\project/")
import numpy as np
from utils import WRFile
import math
import os
import matplotlib.pylab as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib
from plotdata import PlotData

plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签 
plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
plt.rc('font', size=18) 
class DelayofATBMandSQ:
    def __init__(self,q):
        self.q = 1.0*q
    '''
    返回的结果
    result[0] = d
    result[1] = d1
    result[2] = d2
    result[3] = d3
    '''
    def fillDelay(self,dict_obj,key,values):
        if key in dict_obj:
            dict_obj[key] += values
        else:
            dict_obj.setdefault(key,values)
            
    def delayofSQ(self,c1,c2,c3):
        result = [0,0,0,0]
        q = 10       
        n1=math.floor(c1)
        m1=c1-n1
        
        n2=math.floor(c2)
        m2=c2-n2
        
        n3=math.floor(c3)
        m3=c3-n3
        dict_delay = {0:0}#所有延迟大于4的均归到5中
        if c1<=1:
             #----------------统计C1的各项延迟-------------------------#
            dict_delay[0] += q*c1
            if c2<=1:
                dict_delay[0] += q*c2#统计C2的延迟
                if c3<=1:#c1<1,c2<1,c3<1
                    dict_delay[0]+=q*c3
                elif c3>1:#c1<1,c2>1,c3<1
                    #print("c1<1,c2>1,c3<1")
                    result[3] = q/2*(n3-1)*n3+q*n3*m3
                    for i in range(n3):
                        if i in dict_delay:
                            dict_delay[i]+=q
                        else:
                            
                            dict_delay.setdefault(i, q)#完成了0到n2-1的统计
                        
                    if n3 in dict_delay:#完成了n2的统计
                       dict_delay[n3]+=q*m3
                    else:
                       dict_delay.setdefault(n3, q*m3)
                       
            else:#c2>1
                if c3<=1:#c1<1,c2>1,c3<1
                    #----------------统计C2的各项延迟-------------------------#
                    result[2] = q/2*(n2-1)*n2+q*n2*m2# q*0+q*1+..+q*(n2-1)+q*m2*n2
                    for i in range(n2):
                        if i in dict_delay:
                            dict_delay[i]+=q
                        else:
                            dict_delay.setdefault(i, q)#完成了0到n2-1的统计
                    if n2 in dict_delay:#完成了n2的统计
                       dict_delay[n2]+=q*m2
                    else:
                       dict_delay.setdefault(n2, q*m2)
                       
                    #----------------统计C3的各项延迟-------------------------#                     
                    if 1-m2<=c3:
                        result[3] = q*(1-m2)*(n2-1)+q*n2*(m2+c3-1)#1-m2+m2+c3-1 = c3
                        dict_delay[n2-1] += q*(1-m2)
                        dict_delay[n2]+= q*(m2+c3-1)
                    else:
                        result[3] = q*c3*(n2-1)
                        dict_delay[n2-1] += q*c3
                else:#c1<1,c2>1,c3>1
                    #print("c1<1,c2>1c3>1")
                    #----------------统计C2的各项延迟-------------------------#
                    result[2] = q/2*(n2-1)*n2+q*n2*m2# q*0+q*1+..+q*(n2-1)+q*m2*n2
                    for i in range(n2):
                        if i in dict_delay:
                            dict_delay[i]+=q
                        else:
                            dict_delay.setdefault(i, q)#完成了0到n2-1的统计
                    if n2 in dict_delay:#完成了n2的统计
                       dict_delay[n2]+=q*m2
                    else:
                       dict_delay.setdefault(n2, q*m2)
                    
                    #----------------统计C3的各项延迟-------------------------# 
                    if m2+m3>1:
                        #print("here")
                        result[3] = q*(1-m2)*(n2-1)+q/2*(2*n2+n3-2)*(n3-1)+q*(n3+n2-1)+q*(m2+m3-1)*(n2+n3)#1-m2+n3-1+1+m2+m3-1=n3+m3
                        dict_delay[n2-1] += q*(1-m2)
                        
                        for i in range(1,n3):# q*0+q*1+..+q*(n3-1)+q*m2*n2
                            if n2-1+i in dict_delay:
                                dict_delay[n2-1+i] += q
                            else:
                                dict_delay.setdefault(n2-1+i,q)
                                
                        if n3+n2-1 in dict_delay:
                            dict_delay[n3+n2-1] += q
                        else:
                            dict_delay.setdefault(n3+n2-1,q)
                            
                        if n3+n2 in dict_delay:
                            dict_delay[n3+n2] += q*(m2+m3-1)
                        else:
                            dict_delay.setdefault(n3+n2,q*(m2+m3-1))                        
                    else:
                        result[3] =  q*(1-m2)*(n2-1)+q/2*(2*n2+n3-2)*(n3-1)+q*(m2+m3)*(n2+n3-1)
                        
                        dict_delay[n2-1] += q*(1-m2)
                        for i in range(1,n3):# q*0+q*1+..+q*(n3-1)+q*m2*n2
                            if n2-1+i in dict_delay:
                                dict_delay[n2-1+i] += q
                            else:
                                dict_delay.setdefault(n2-1+i,q)
                                
                        if n3+n2-1 in dict_delay:
                            dict_delay[n3+n2-1] += q*(m2+m3)
                        else:
                            dict_delay.setdefault(n3+n2-1,q*(m2+m3))
         # ******************************time one      
        else:#c1>1
            if c2<=1:
                if c3<=1:
                    #print("c1>1,c2<=1,c3<=1")
                #------------统计C1的延迟----------------------------------#
                    result[1] = q/2*n1*(n1-1)+q*n1*m1
                    for i in range(n1):
                        if i in dict_delay:
                            dict_delay[i]+=q
                        else:
                            dict_delay.setdefault(i, q)#完成了0到n2-1的统计
                    if n1 in dict_delay:#完成了n2的统计
                       dict_delay[n1]+=q*m1
                    else:
                       dict_delay.setdefault(n1, q*m1)
                      
               #------------统计C2的延迟----------------------------------#       
                    if  1-m1<=c2:
                        result[2] = q*(n1-1)*(1-m1)+q*n1*(c2+m1-1)
                        dict_delay[n1-1] += q*(1-m1)
                        dict_delay[n1] += q*(c2+m1-1)
                        
               #------------统计C3的延迟----------------------------------#        
                        if 2-m1-c2<=c3:
                            result[3] = q*(2-c2-m1)*(n1-1)+q*(c3+c2+m1-2)*n1
                            dict_delay[n1-1] += q*(2-c2-m1)
                            dict_delay[n1] += q*(c3+c2+m1-2)
                            
                        else:
                            result[3] = c3*q*(n1-1)
                            dict_delay[n1-1] += q*c3
                    else:
                 #------------统计C2的延迟----------------------------------# 
                        result[2] = c2*q*(n1-1)
                        dict_delay[n1-1] += c2*q
                        
                 #------------统计C3的延迟----------------------------------#         
                        if 1-m1-c2<=c3:#c3<=1
                            if n1 == 1:
                                result[3]=0
                                dict_delay[0]+=q*c3
                            else:                                                                
                                result[3] = q*(1-m1-c2)*(n1-2)+q*(c3+c2+m1-1)*(n1-1)
                                dict_delay[n1-2]+= q*(1-m1-c2)
                                dict_delay[n1-1]+= q*(c3+c2+m1-1)
                        else:#1-m1-c2>c3
                             if n1==1:
                                 dict_delay[0]+=q*c3
                             else:
                                 result[3] = c3*q*(n1-2)
                                 dict_delay[n1-2]+=c3*q
                #******************************time two
                                 
                                 
                else:#c1>1,c2<=1,c3>=1
                    #print("c1>1,c2<1,c3>=1")
                #---------计算C1的延迟-------------------------
                    result[1] = q/2*n1*(n1-1)+q*m1*n1
                    for i in range(n1):
                        if i in dict_delay:
                            dict_delay[i]+=q
                        else:
                            dict_delay.setdefault(i, q)#完成了0到n2-1的统计
                    if n1 in dict_delay:#完成了n2的统计
                       dict_delay[n1]+=q*m1
                    else:
                       dict_delay.setdefault(n1, q*m1)  
                                              
                    if 1-m1<=c2:#1-m1<=c2
                    #----------------计算C2的延迟-------------------------
                        result[2] = q*(1-m1)*(n1-1)+q*(c2+m1-1)*n1
                        dict_delay[n1-1] += q*(1-m1)
                        dict_delay[n1] += q*(c2+m1-1)
                        
                        if n3==1:
                   #----------------计算C3的延迟-------------------------
                            if m1+m3+c2-1<=1:
                                result[3] = q*(n1-1)*(2-c2-m1)+q*(m1+c2+m3-1)*(n1+n3-1)
                                dict_delay[n1-1] += q*(2-c2-m1)
                                dict_delay[n1] += q*(m1+c2+m3-1)
                                
                            elif m1+m3+c2-1<=2:
                                result[3] = q*(n1-1)*(2-c2-m1)+q*n1+q*(m1+c2+m3-2)*(n1+1)
                                dict_delay[n1-1] += q*(2-c2-m1)
                                dict_delay[n1] += q
                                if n1+1 in dict_delay:
                                    dict_delay[n1+1] += q*(m1+c2+m3-2)
                                else:
                                    dict_delay.setdefault(n1+1,q*(m1+c2+m3-2))
                                
                        else:#n3>1
                            if m1+m3+c2<=1:                              
                                result[3] = q*(n1-1)*(2-c2-m1)+q/2*(2*n1+n3-3)*(n3-2)+q*(n1+n3-2)*(m1+m3+c2)
                                dict_delay[n1-1] += q*(2-c2-m1)
                                
                                for i in range(1,n3-2+1):#对n1-1+1,.....,n1-1+n3-2
                                    if n1-1+i in dict_delay:
                                        dict_delay[n1-1+i]+=q
                                    else:
                                        dict_delay.setdefault(n1-1+i,q)
                                
                                if n1+n3-2 in dict_delay:# 对n1+n3-2进行填补
                                    dict_delay[n1+n3-2]+= q*(m1+m3+c2)
                                else:
                                    dict_delay.setdefault(n1+n3-2, q*(m1+m3+c2))
                                          
                            elif m1+m3+c2<=2:
                                result[3] = q*(n1-1)*(2-c2-m1)+q/2*(2*n1+n3-3)*(n3-2)+q*(n1+n3-2)+q*(n1+n3-1)*(m1+m3+c2-1)
                                dict_delay[n1-1] += q*(2-c2-m1)
                                
                                for i in range(1,n3-2+1):#对n1-1+1,.....,n1-1+n3-2
                                    if n1-1+i in dict_delay:
                                        dict_delay[n1-1+i]+=q
                                    else:
                                        dict_delay.setdefault(n1-1+i,q)
                                if n1+n3-2 in dict_delay:# 对n1+n3-2进行填补
                                    dict_delay[n1+n3-2]+= q
                                else:
                                    dict_delay.setdefault(n1+n3-2, q)
                                    
                                if n1+n3-1 in dict_delay:# 对n1+n3-1进行填补
                                    dict_delay[n1+n3-1]+= q*(m1+m3+c2-1)
                                else:
                                    dict_delay.setdefault(n1+n3-1, q*(m1+m3+c2-1))                                                                          
                            else:
                                result[3] = q*(n1-1)*(2-c2-m1)+q/2*(2*n1+n3-3)*(n3-2)+q*(n1+n3-2)+q*(n1+n3-1)+q*(n1+n3)*(m1+m3+c2-2)
                                dict_delay[n1-1] += q*(2-c2-m1)                               
                                for i in range(1,n3-2+1):#对n1-1+1,.....,n1-1+n3-2
                                    if n1-1+i in dict_delay:
                                        dict_delay[n1-1+i]+=q
                                    else:
                                        dict_delay.setdefault(n1-1+i,q)
                                if n1+n3-2 in dict_delay:# 对n1+n3-2进行填补
                                    dict_delay[n1+n3-2]+= q
                                else:
                                    dict_delay.setdefault(n1+n3-2, q)
                                    
                                if n1+n3-1 in dict_delay:# 对n1+n3-1进行填补
                                    dict_delay[n1+n3-1]+= q
                                else:
                                    dict_delay.setdefault(n1+n3-1, q) 
                                
                                if n1+n3 in dict_delay:# 对n1+n3进行填补
                                    dict_delay[n1+n3]+= q*(m1+m3+c2-2)
                                else:
                                    dict_delay.setdefault(n1+n3, q*(m1+m3+c2-2)) 
                    else:#1-m1>c2
                    #-------------计算C2的延迟--------------------------
                        result[2] = c2*q*(n1-1)
                        if n1-1 in dict_delay:
                            dict_delay[n1-1] += q*c2
                        else:
                            dict_delay.setdefault(n1-1,q*c2)
                    #-------------计算C3的延迟--------------------------        
                        if n1==1:
                            result[3] = q/2*n3*(n3-1)+q*m3*n3# q*0+q*1+..+q*(n3-1)+q*m3*n3
                            for i in range(n3):
                                if i in dict_delay:
                                    dict_delay[i]+=q
                                else:
                                    dict_delay.setdefault(i,q)
                            if n3 in dict_delay:
                                dict_delay[n3] += q*m3
                            else:
                                dict_delay.setdefault(n3,q*m3)
                        else:#n1>1
                            if m1+m3+c2<=1:   
                                result[3] = q*(n1-2)*(1-m1-c2)+q/2*(2*n1+n3-4)*(n3-1)+q*(m1+c2+m3)*(n1+n3-2)#n1-2+n3-1+m1+c2+m3 = n3+m3
                                #***************整理到这里了*********************************
                                if n1-2 in dict_delay:
                                    dict_delay[n1-2] += q*(1-m1-c2)
                                else:
                                    dict_delay.setdefault(n1-2, q*(1-m1-c2))
                                
                                for i in range(1,n3):# q*(1+n1-1)+.....+q*(n3-1+n1-1)
                                    if (n1-2+i) in dict_delay:
                                        dict_delay[n1-2+i] += q
                                    else:
                                        dict_delay.setdefault(n1-2+i,q)
                                        
                                if n1+n3-2 in dict_delay:#添加尾项
                                    dict_delay[n1+n3-2]+= q*(m1+c2+m3)
                                else:
                                    dict_delay.setdefault(n1+n3-2,q*(m1+c2+m3))
                                        
                            elif m1+m3+c2<=2:
                                # 这里出现问题
                                
                                result[3] = q*(n1-2)*(1-m1-c2)+q/2*(2*n1+n3-4)*(n3-1)+q*(n1+n3-2)+q*(m1+c2+m3-1)*(n1+n3-1)
                                
                                if n1-2 in dict_delay:
                                    dict_delay[n1-2] += q*(1-m1-c2)
                                else:
                                    dict_delay.setdefault(n1-2, q*(1-m1-c2))  
                                    
                                for i in range(1,n3):# q*(1+n1-1)+.....+q*(n3-1+n1-1)
                                    if (n1-2+i) in dict_delay:
                                        dict_delay[n1-2+i] += q
                                    else:
                                        dict_delay.setdefault(n1-2+i,q)
                                        
                                if n1+n3-2 in dict_delay:#添加q*(n1+n3-2)
                                    dict_delay[n1+n3-2]+= q
                                else:
                                    dict_delay.setdefault(n1+n3-2,q)
                                    
                                if n1+n3-1 in dict_delay:#添加尾项
                                    dict_delay[n1+n3-1]+= q*(m1+c2+m3-1)
                                else:
                                    dict_delay.setdefault(n1+n3-1,q*(m1+c2+m3-1))                                    
                            else:
                                result[3] = q*(n1-2)*(1-m1-c2)+q/2*(2*n1+n3-4)*(n3-1)+q*(n1+n3-2)+q*(n1+n3-1)+q*(m1+c2+m3-2)*(n1+n3)
                                
                                if n1-2 in dict_delay:
                                    dict_delay[n1-2] += q*(1-m1-c2)
                                else:
                                    dict_delay.setdefault(n1-2, q*(1-m1-c2))  
                                    
                                for i in range(1,n3):# q*(1+n1-1)+.....+q*(n3-1+n1-1)
                                    if (n1-2+i) in dict_delay:
                                        dict_delay[n1-2+i] += q
                                    else:
                                        dict_delay.setdefault(n1-2+i,q)
                                        
                                if n1+n3-2 in dict_delay:#添加q*(n1+n3-2)
                                    dict_delay[n1+n3-2]+= q
                                else:
                                    dict_delay.setdefault(n1+n3-2,q)
                                    
                                if n1+n3-1 in dict_delay:#添加倒数第二项
                                    dict_delay[n1+n3-1]+= q
                                else:
                                    dict_delay.setdefault(n1+n3-1,q)
                                    
                                if n1+n3 in dict_delay:#添加尾项
                                    dict_delay[n1+n3]+= q*(m1+c2+m3-2)
                                else:
                                    dict_delay.setdefault(n1+n3,q*(m1+c2+m3-2)) 
                                    
                             #*****************************time three******************************                                                                            
            else:#c2>1
                if c3<=1:#c1>1,c2>1,c3<=1
                    #print("c1>1,c2>1,c3<=1")
                #------------------进行C1的填补----------------------------------
                    result[1] = q*n1*(n1-1)/2+q*m1*n1 #m1+n1-1+1
                    for i in range(n1):# q*0+q*1+...+q*(n1-1)
                        self.fillDelay(dict_obj = dict_delay,key = i,values = q)
                    self.fillDelay(dict_delay,n1,q*m1)
                    
                    if m1+m2<=1:
                    #------------------进行C2的填补----------------------------------
                        result[2] = q*(1-m1)*(n1-1)+q/2*(2*n1+n2-2)*(n2-1)+q*(m1+m2)*(n1+n2-1)
                        dict_delay[n1-1] += q*(1-m1)
                        
                        for i in range(1,n2):
                            self.fillDelay(dict_delay,n1-1+i,q)                           
                        self.fillDelay(dict_delay,n1+n2-1,q*(m1+m2))
                        
                        if 1-m1-m2<=c3:
                            result[3] = q*(1-m1-m2)*(n1+n2-2)+q*(c3+m1+m2-1)*(n1+n2-1)
                            self.fillDelay(dict_delay,n1+n2-2,q*(1-m1-m2))
                            self.fillDelay(dict_delay,n1+n2-1,q*(c3+m1+m2-1))
                        else:
                            result[3] = c3*q*(n1+n2-2)
                            self.fillDelay(dict_delay,(n1+n2-2),c3*q)
                    else:#m1+m2>1
                        
                        result[2] = q*(1-m1)*(n1-1)+q/2*(2*n1+n2-2)*(n2-1)+q*(n1+n2-1)+q*(m1+m2-1)*(n1+n2)
                        self.fillDelay(dict_delay,n1-1,q*(1-m1))
                        for i in range(1,n2):
                            self.fillDelay(dict_delay,n1-1+i,q)
                            
                        self.fillDelay(dict_delay,(n1+n2),q*(m1+m2-1)) 
                        self.fillDelay(dict_delay,(n1+n2-1),q)
                        if 2-m1-m2<=c3:
                            result[3] = q*(2-m1-m2)*(n1+n2-1)+q*(c3+m1+m2-2)*(n1+n2)
                            self.fillDelay(dict_delay,n1+n2-1,q*(2-m1-m2))
                            self.fillDelay(dict_delay,n1+n2,q*(c3+m1+m2-2))
                        else:
                            result[3] = q*c3*(n1+n2-1)
                            self.fillDelay(dict_delay,n1+n2-1,q*c3)
                else: #c1>1,c2>1,c3>1
                    #print("c1>1,c2>1,c3>1")
                    result[1] = q*n1*(n1-1)/2+q*m1*n1
                    for i in range(n1):# q*0+q*1+...+q*(n1-1)
                        self.fillDelay(dict_obj = dict_delay,key = i,values = q)
                    self.fillDelay(dict_delay,n1,q*m1)
                    
                    if m1+m2<=1:
                        result[2] = q*(1-m1)*(n1-1)+q/2*(2*n1+n2-2)*(n2-1)+q*(m1+m2)*(n1+n2-1)                        
                        dict_delay[n1-1] += q*(1-m1)                       
                        for i in range(1,n2):
                            self.fillDelay(dict_delay,n1-1+i,q)                           
                        self.fillDelay(dict_delay,n1+n2-1,q*(m1+m2))
                        
                        if m1+m2+m3<=1:
                            result[3] = q*(1-m1-m2)*(n1+n2-2)+q/2*(2*n1+2*n2+n3-4)*(n3-1)+q*(m1+m2+m3)*(n1+n2+n3-2)
                            self.fillDelay(dict_delay,n1+n2-2,q*(1-m1-m2))
                            
                            for i in range(1,n3):
                                self.fillDelay(dict_delay,n1+n2-2+i,q)
                                
                            self.fillDelay(dict_delay,n1+n2+n3-2,q*(m1+m2+m3))
                            
                        elif m1+m2+m3<=2:
                            result[3] = q*(1-m1-m2)*(n1+n2-2)+q/2*(2*n1+2*n2+n3-4)*(n3-1)+q*(n1+n2+n3-2)+q*(m1+m2+m3-1)*(n1+n2+n3-1)
                            self.fillDelay(dict_delay,n1+n2-2,q*(1-m1-m2))                            
                            for i in range(1,n3):
                                self.fillDelay(dict_delay,n1+n2-2+i,q)
                                
                            self.fillDelay(dict_delay,n1+n2+n3-2,q)
                            self.fillDelay(dict_delay,n1+n2+n3-1,q*(m1+m2+m3-1))
                        else:
                            print("c1>1,c2>1,c3>1,SQ,exception")
                    else:
                        result[2] = q*(1-m1)*(n1-1)+q/2*(2*n1+n2-2)*(n2-1)+q*(n1+n2-1)+q*(m1+m2-1)*(n1+n2)
                        
                        dict_delay[n1-1] += q*(1-m1)                       
                        for i in range(1,n2):
                            self.fillDelay(dict_delay,n1-1+i,q)                           
                        self.fillDelay(dict_delay,n1+n2-1,q)
                        self.fillDelay(dict_delay,n1+n2,q*(m1+m2-1))
                        
                        if m1+m2+m3-1<=1:
                            result[3] = q*(2-m1-m2)*(n1+n2-1)+q/2*(2*n1+2*n2+n3-2)*(n3-1)+q*(m3+m1+m2-1)*(n1+n2+n3-1)
                            dict_delay[n1+n2-1]+=q*(2-m1-m2)
                            
                            for i in range(1,n3):
                                self.fillDelay(dict_delay,n1+n2-1+i,q)
                                
                            self.fillDelay(dict_delay,n1+n2+n3-1,q*(m3+m1+m2-1))
                        elif m1+m2+m3-1<=2:
                            result[3] = q*(2-m1-m2)*(n1+n2-1)+q/2*(2*n1+2*n2+n3-2)*(n3-1)+q*(n1+n2+n3-1)+q*(m3+m1+m2-2)*(n1+n2+n3) 
                            dict_delay[n1+n2-1]+=q*(2-m1-m2)                            
                            for i in range(1,n3):
                                self.fillDelay(dict_delay,n1+n2-1+i,q)
                                
                            self.fillDelay(dict_delay,n1+n2+n3-1,q)
                            self.fillDelay(dict_delay,n1+n2+n3,q*(m3+m1+m2-2))
                        else:
                            print("sq+exception")
        if c1+c2+c3==0:
            result=[0,0,0,0]
        else:
            result[0] = (float("%.3f"%((result[1]+result[2]+result[3])/(c1+c2+c3)/q)))
        
        return result,dict_delay
    def produceX(self):
        c1 = np.arange(0,self.q,0.2)
        c2 = np.arange(0,self.q,0.2)
        c3 = np.arange(0,self.q,0.2)
        x=[]
        for i in c1:
            for j in c2:
                for k in c3:
                    temp = str(i)+"-"+str(j)+"-"+str(k)
                    x.append(temp)
        return x
            
    def delayofATBM(self,c1,c2,c3):
        result = [0,0,0,0]
        q = 10
        dict_delay = {0:0}
        n1=math.floor(c1)
        m1=c1-n1
        
        n2=math.floor(c2)
        m2=c2-n2
        
        n3=math.floor(c3)
        m3=c3-n3
        
        if c1<=1:
            if c2<=1:
                if c3<=1:#c1<=1,c2<=1,c3<=1
                    dict_delay[0]=q*(c1+c2+c3)
                else: #c1<=1,c2<=1,c3>1
                    #print("c1<=1,c2<=1,c3>1")
                    result[3] = (n3-1)*n3*q/2+m3*n3*q
                    dict_delay[0]+=q*(c1+c2)# 完成c1和C2的统计
                    for i in range(n3):#q*0+q*1+...+q*(n3-1)
                        self.fillDelay(dict_delay,i,q)
                    self.fillDelay(dict_delay,n3,q*m3)
            else:#c2>1
            #-----------------计算C1的延迟---------------------
                dict_delay[0]+= q*c1
                
                if c3<=1:#c1<=1,c2>1,c3<=1
            #-----------------计算C3的延迟---------------------
                    dict_delay[0]+= q*c3
                    if m2+c3>1:
           #-----------------计算C2的延迟---------------------
                        if n2==1:
                            result[2] = q*(1-c3)+ 2*q*(m2+c3-1) #1-c3+m2+c3-1  +  1 = 1+m2
                            dict_delay[0] += q
                            self.fillDelay(dict_delay,1,q*(1-c3))
                            self.fillDelay(dict_delay,2,q*(m2+c3-1))
                        else:#n2>1
                            result[2]=q*(1-c3)+q/2*(n2+1)*(n2-2)+n2*q+q*(n2+1)*(m2+c3-1)
                            dict_delay[0] += q 
                            self.fillDelay(dict_delay,1,q*(1-c3))
                            for i in range(1,n2-2+1):
                                self.fillDelay(dict_delay,1+i,q)
                                
                            self.fillDelay(dict_delay,n2,q)
                            self.fillDelay(dict_delay,n2+1,q*(m2+c3-1))
                    else:#m2+c3<=1                    
                        if n2==1:
                            
                            result[2] = q*m2
                            dict_delay[0] += q
                            self.fillDelay(dict_delay,1,q*m2)
                            
                        else:
                            result[2]=q*(1-c3)+q/2*(n2+1)*(n2-2)+q*(m2+c3)*n2
                            self.fillDelay(dict_delay,1,q*(1-c3))
                            dict_delay[0]+=q
                            for i in range(1,n2-2+1):
                                self.fillDelay(dict_delay,1+i,q)                               
                            self.fillDelay(dict_delay,n2,q*(m2+c3))
                
                
                else: #c1<=1,c2>1,c3>1
                    #print("c1<=1,c2>1,c3>1")
                #-----------------计算C2的延迟---------------------     
                    result[2]=q*(n2+2)*(n2-1)/2+q*(n2+1)*m2 
                    dict_delay[0] += q
                    
                    for i in range(1,n2-1+1):
                        self.fillDelay(dict_delay,1+i,q)
                    self.fillDelay(dict_delay,n2+1,q*m2)
                #-----------------计算C3的延迟--------------------- 
                    dict_delay[0]+= q
                    if m2+m3>1:
                        if n3==1:
                            
                            result[3]=q*(n2)*(1-m2)+q*(m2+m3-1)*(n2+1)
                            self.fillDelay(dict_delay,n2,q*(1-m2))
                            self.fillDelay(dict_delay,n2+1,q*(m2+m3-1))
                        else:
                            result[3]=q*(n2)*(1-m2)+q/2*(2*n2+n3-1)*(n3-2)+q*(n2+n3-1)+q*(m2+m3-1)*(n2+n3)
                            self.fillDelay(dict_delay,n2,q*(1-m2))
                            for i in range(1,n3-2+1):
                                self.fillDelay(dict_delay,n2+i,q)
                            self.fillDelay(dict_delay,n3+n2-1,q)
                            self.fillDelay(dict_delay,n3+n2,q*(m2+m3-1))
                    else:#m2+m3<=1
                        if n3==1:
                            result[3] = q*n2*m3
                            self.fillDelay(dict_delay,n2,q*m3)
                        else:
                            #n3-2层的发送时间是n2+n3-2，余项的发送时间是n2+n3-1
                            result[3]=q*(n2)*(1-m2)+q/2*(2*n2+n3-1)*(n3-2)+q*(m2+m3)*(n2+n3-1)   
                            self.fillDelay(dict_delay,n2,q*(1-m2))
                            for i in range(1,n3-2+1):
                                self.fillDelay(dict_delay,n2+i,q)
                            self.fillDelay(dict_delay,n3+n2-1,q*(m2+m3))
                                                      
        elif c1>1:             
             if c2<=1:                
                if c3<=1:#c1>1,c2<=1,c3<=1
                    #print("c1>1,c2<=1,c3<=1")
                    dict_delay[0]+= q
                    dict_delay[0]+= c2*q                    
                    dict_delay[0]+= c3*q
                    d1=0
                    if n1==1:
                        if m1<=1-c2:
                            d1=1*q*m1  
                            self.fillDelay(dict_delay,1,q*(m1))
                        elif m1>1-c2:#发生溢出
                            
                            d1 = q*(1-c2)#发送了一部分
                            self.fillDelay(dict_delay,1,q*(1-c2))
                            if 1-c2==0:
                                if 1-c3>0:
                                    if 1-c3>=m1:
                                        d1 = 2*m1*q
                                        self.fillDelay(dict_delay,2,m1*q)
                                    else:
                                        d1 = q*2*(1-c3)+q*3*(m1+c3-1)
                                        self.fillDelay(dict_delay,2,(1-c3)*q)
                                        self.fillDelay(dict_delay,3,(m1+c3-1)*q)
                                elif 1-c3<=0:
                                    d1 = 3*q*m1
                                    self.fillDelay(dict_delay,3,(m1)*q)
                            else:
                                if 1-c3>=(m1+c2-1):
                                    d1+=2*q*(m1+c2-1)
                                    self.fillDelay(dict_delay,2,q*(m1+c2-1))
                                elif 1-c3<(m1+c2-1):
                                    d1+=(2*q*(1-c3)+3*q*(m1+c3+c2-2))
                                    self.fillDelay(dict_delay,2,q*(1-c3))
                                    self.fillDelay(dict_delay,3,q*(m1+c3+c2-2))
                            
                    elif n1==2:
                        if c2+m1<=(1-c3):
                            d1=q*(1-c2)+2*q*(c2+m1)
                            self.fillDelay(dict_delay,1,q*(1-c2))
                            self.fillDelay(dict_delay,2,q*(c2+m1))
                        elif c2+m1<=1:
                            d1=q*(1-c2)+2*q*(1-c3)+3*q*(c2+m1+c3-1)
                            self.fillDelay(dict_delay,1,q*(1-c2))
                            self.fillDelay(dict_delay,2,q*(1-c3))
                            self.fillDelay(dict_delay,3,q*(c2+m1+c3-1))
                        else:
                            
                            d1=q*(1-c2)+2*q*(1-c3)
                            self.fillDelay(dict_delay,1,q*(1-c2))
                            self.fillDelay(dict_delay,2,q*(1-c3))                            
                            if m1+c2+c3-1<=1:
                                d1+=3*q*(m1+c2+c3-1)
                                self.fillDelay(dict_delay,3,q*(c2+m1+c3-1))
                            else:
                                d1+=3*q+4*q*(c2+m1+c3-2)
                                self.fillDelay(dict_delay,3,q)
                                self.fillDelay(dict_delay,4,q*(c2+m1+c3-2))
                    elif n1==3:
                        if c2+c3+m1<=1:
                            d1=q*(1-c2)+2*q*(1-c3)+3*q*(c2+c3+m1)
                            self.fillDelay(dict_delay,1,q*(1-c2))
                            self.fillDelay(dict_delay,2,q*(1-c3))  
                            self.fillDelay(dict_delay,3,q*(c2+c3+m1))                             
                        elif c2+c3+m1<=2:
                            d1=q*(1-c2)+2*q*(1-c3)+3*q+4*q*(c2+c3+m1-1)
                            self.fillDelay(dict_delay,1,q*(1-c2))
                            self.fillDelay(dict_delay,2,q*(1-c3))  
                            self.fillDelay(dict_delay,3,q) 
                            self.fillDelay(dict_delay,4,q*(c2+c3+m1-1))  
                        elif c2+c3+m1<3:
                            d1=q*(1-c2)+2*q*(1-c3)+3*q+4*(q)+5*q*(c2+c3+m1-2)
                            self.fillDelay(dict_delay,1,q*(1-c2))
                            self.fillDelay(dict_delay,2,q*(1-c3))  
                            self.fillDelay(dict_delay,3,q) 
                            self.fillDelay(dict_delay,4,q)
                            self.fillDelay(dict_delay,5,q*(c2+c3+m1-2))  
                    else:#n1>3
                        if c2+c3+m1<=1:
                            #d1=q*(1-c2)+2*q*(1-c3)+q*n1*(c2+c3+m1)+q/2*(n1+2)*(n1-3)
                            d1 = q*(1-c2)+2*q*(1-c3)+q/2*(n1+2)*(n1-3)+q*n1*(c2+c3+m1)
                            self.fillDelay(dict_delay,1,q*(1-c2))
                            self.fillDelay(dict_delay,2,q*(1-c3)) 
                            for i in range(1,n1-3+1):
                                self.fillDelay(dict_delay,2+i,q)
                            self.fillDelay(dict_delay,n1,q*(c2+c3+m1))
                            
                        elif c2+c3+m1<=2:
                            d1=q*(1-c2)+2*q*(1-c3)+q/2*(n1+2)*(n1-3)+q*n1+q*(n1+1)*(c2+c3+m1-1)
                            self.fillDelay(dict_delay,1,q*(1-c2))
                            self.fillDelay(dict_delay,2,q*(1-c3)) 
                            for i in range(1,n1-3+1):
                                self.fillDelay(dict_delay,2+i,q)
                            self.fillDelay(dict_delay,n1,q)
                            self.fillDelay(dict_delay,n1+1,q*(c2+c3+m1-1))
                            
                        elif c2+c3+m1<3:
                            d1=q*(1-c2)+2*q*(1-c3)+q/2*(n1+2)*(n1-3)+q*n1+q*(n1+1)+q*(c2+c3+m1-2)*(n1+2) 
                            self.fillDelay(dict_delay,1,q*(1-c2))
                            self.fillDelay(dict_delay,2,q*(1-c3)) 
                            for i in range(1,n1-3+1):
                                self.fillDelay(dict_delay,2+i,q)
                            self.fillDelay(dict_delay,n1,q)
                            self.fillDelay(dict_delay,n1+1,q)
                            self.fillDelay(dict_delay,n1+2,q*(c2+c3+m1-2))
                            
                    result[1] = d1
                else: #c1>1,c2<=1,c3>1
                    #print("c1>1,c2<=1,c3>1")
                #------------计算延迟为0的并发量个数------------------------
                    dict_delay[0]+= q
                    dict_delay[0]+= q
                    dict_delay[0]+= c2*q
                    if n1==1:
                       if m1<=1-c2:
                           result[1]=q*m1
                           self.fillDelay(dict_delay,1,q*m1)
                           result[3] = q/2*n3*(n3-1)+q*n3*m3                           
                           for i in range(1,n3):
                               self.fillDelay(dict_delay,i,q)                               
                           self.fillDelay(dict_delay,n3,q*m3)
                       else:#m1>1-c2
                           result[1] = q*(1-c2)+3*q*(m1+c2-1)
                           self.fillDelay(dict_delay,1,q*(1-c2))
                           self.fillDelay(dict_delay,3,q*(m1+c2-1))
                           if m1+m3+c2-1>1:
                               if n3==1:
                                   result[3] = q*(2-m1-c2)+q*2*(m1+m3+c2-2)
                                   self.fillDelay(dict_delay,1,q*(2-m1-c2))
                                   self.fillDelay(dict_delay,2,q*(m1+m3+c2-2))
                               else:
                                   result[3] = q*(2-m1-c2)+q/2*(n3+1)*(n3-2)+q*n3+q*(m1+m3+c2-2)*(n3+1)
                                   self.fillDelay(dict_delay,1,q*(2-m1-c2))
                                   for i in range(1,n3-2+1):
                                       self.fillDelay(dict_delay,1+i,q)
                                   self.fillDelay(dict_delay,n3,q)
                                   self.fillDelay(dict_delay,n3+1,q*(m1+m3+c2-2))
                           else:#m1+m3+c2-1<=1
                               if n3==1:
                                   result[3] = q*m3
                                   self.fillDelay(dict_delay,1,q*m3)
                               else:
                                   result[3] = q*(2-m1-c2)+q/2*(n3+1)*(n3-2)+q*(n3)*(m1+m3+c2-1)
                                   self.fillDelay(dict_delay,1,q*(2-m1-c2))
                                   for i in range(1,n3-2+1):
                                       self.fillDelay(dict_delay,1+i,q)
                                   self.fillDelay(dict_delay,n3,q*(m1+m3+c2-1))
                                   
                    else:#n1>1
                        if c2+m1<=1:
                            result[1] = q*(1-c2)+q/2*(n1+3)*(n1-2)+q*(c2+m1)*(n1+1)
                            self.fillDelay(dict_delay,1,q*(1-c2))
                            for i in range(1,n1-2+1):
                                self.fillDelay(dict_delay,2+i,q)                               
                            self.fillDelay(dict_delay,n1+1,q*(c2+m1))
                            
                            if m1+m3+c2<=1:
                                if n3==1:
                                    result[3] = q*(n1-1)*m3
                                    self.fillDelay(dict_delay,n1-1,q*m3)
                                else:
                                    result[3] = q*(n1-1)*(1-c2-m1)+q/2*(2*n1+n3-3)*(n3-2)+q*(m1+m3+c2)*(n1+n3-2)
                                    self.fillDelay(dict_delay,n1-1,q*(1-c2-m1))
                                    for i in range(1,n3-2+1):
                                        self.fillDelay(dict_delay,n1-1+i,q)
                                    self.fillDelay(dict_delay,(n1+n3-2),q*(m1+m3+c2))
                            else:#m1+m3+c2>1
                                if n3==1:
                                    result[3] = q*(n1-1)*(1-c2-m1)+q*n1*(m3+m1+c2-1)
                                    self.fillDelay(dict_delay,n1-1,q*(1-c2-m1))
                                    self.fillDelay(dict_delay,n1,q*(m3+m1+c2-1))
                                else:
                                    result[3] = q*(n1-1)*(1-c2-m1)+q/2*(2*n1+n3-3)*(n3-2)+q*(n1+n3-2)+q*(m1+m3+c2-1)*(n1+n3-1)
                                    self.fillDelay(dict_delay,n1-1,q*(1-c2-m1))
                                    for i in range(1,n3-2+1):
                                        self.fillDelay(dict_delay,n1-1+i,q)
                                    self.fillDelay(dict_delay,(n1+n3-2),q)
                                    self.fillDelay(dict_delay,(n1+n3-1),q*(m1+m3+c2-1))
                        else:#c2+m1>1
                            result[1] = q*(1-c2)+q/2*(n1+3)*(n1-2)+q*(n1+1)+q*(c2+m1-1)*(n1+2)
                            self.fillDelay(dict_delay,1,q*(1-c2))
                            for i in range(1,n1-2+1):
                                self.fillDelay(dict_delay,2+i,q)
                            self.fillDelay(dict_delay,n1+1,q)
                            self.fillDelay(dict_delay,n1+2,q*(c2+m1-1))
                            
                            if c2+m1+m3-1<=1:
                                if n3==1:
                                    result[3] = q*m3*n1
                                    self.fillDelay(dict_delay,n1,q*m3)
                                else:
                                    result[3] = q*(2-c2-m1)*n1+q/2*(2*n1+n3-1)*(n3-2)+q*(c2+m1+m3-1)*(n1+n3-1)
                                    self.fillDelay(dict_delay,n1,q*(2-c2-m1))
                                    for i in range(1,n3-2+1):
                                        self.fillDelay(dict_delay,n1+i,q)
                                    self.fillDelay(dict_delay,(n1+n3-1),q*(c2+m1+m3-1))
                            else:#c2+m1+m3-1>1
                                if n3==1:
                                    result[3] = q*(2-c2-m1)*n1+q*(n1+1)*(m3+m1+c2-2)
                                    self.fillDelay(dict_delay,n1,q*(2-c2-m1))
                                    self.fillDelay(dict_delay,n1+1,q*(m3+m1+c2-2))
                                else:
                                    result[3] = q*(2-c2-m1)*n1+q/2*(2*n1+n3-1)*(n3-2)+q*(n1+n3-1)+q*(c2+m1+m3-2)*(n1+n3)
                                    self.fillDelay(dict_delay,n1,q*(2-c2-m1))
                                    for i in range(1,n3-2+1):
                                        self.fillDelay(dict_delay,n1+i,q)
                                    self.fillDelay(dict_delay,(n1+n3-1),q)
                                    self.fillDelay(dict_delay,(n1+n3),q*(c2+m1+m3-2))
             else:#c2>1       
                 if c3<=1:#c1>1,c2>1,c3<=1
                     #print("c1>1,c2>1,c3<=1")
                     dict_delay[0]+= q+q+q*c3
                     if m1+c3<=1:
                         if n1==1:
                             result[1] = 2*q*m1
                             self.fillDelay(dict_delay,2,q*m1)
                         else:
                             result[1] = 2*q*(1-c3)+q/2*(n1+3)*(n1-2)+q*(n1+1)*(m1+c3)
                             self.fillDelay(dict_delay,2,q*(1-c3))
                             for i in range(1,n1-2+1):
                                 self.fillDelay(dict_delay,i+2,q)
                             self.fillDelay(dict_delay,n1+1,q*(m1+c3))
                         if m1+m2+c3<=1:
                             if n2==1:
                                 result[2] = q*m2*n1
                                 self.fillDelay(dict_delay,n1,q*m2)
                             else:
                                 result[2] = q*(1-m1-c3)*n1+q/2*(2*n1+n2-1)*(n2-2)+q*(m1+m2+c3)*(n1+n2-1)
                                 self.fillDelay(dict_delay,n1,q*(1-m1-c3))
                                 for i in range(1,n2-2+1):
                                     self.fillDelay(dict_delay,n1+i,q)
                                 self.fillDelay(dict_delay,(n1+n2-1),q*(m1+m2+c3))
                                     
                         else:
                             if n2==1:
                                 result[2] = q*(1-m1-c3)*n1+q*(n1+1)*(m1+m2+c3-1)
                                 self.fillDelay(dict_delay,n1,q*(1-m1-c3))
                                 self.fillDelay(dict_delay,(n1+1),q*(m1+m2+c3-1))
                             else:
                                 result[2] = q*(1-m1-c3)*n1+q/2*(2*n1+n2-1)*(n2-2)+q*(n1+n2-1)+q*(m1+m2+c3-1)*(n1+n2)
                                 self.fillDelay(dict_delay,n1,q*(1-m1-c3))
                                 for i in range(1,n2-2+1):
                                     self.fillDelay(dict_delay,n1+i,q)
                                 self.fillDelay(dict_delay,(n1+n2-1),q)
                                 self.fillDelay(dict_delay,(n1+n2),q*(m1+m2+c3-1))
                                 
                     else:#m1+c3>1
                         if n1==1:
                             result[1] = 2*q*(1-c3)+3*q*(m1+c3-1)
                             self.fillDelay(dict_delay,2,q*(1-c3))
                             self.fillDelay(dict_delay,3,q*(m1+c3-1))
                         else:
                             result[1] = 2*q*(1-c3)+q/2*(n1+3)*(n1-2)+q*(n1+1)+q*(m1+c3-1)*(n1+2)
                             self.fillDelay(dict_delay,2,q*(1-c3))
                             for i in range(1,n1-2+1):
                                 self.fillDelay(dict_delay,2+i,q)
                             self.fillDelay(dict_delay,n1+1,q)
                             self.fillDelay(dict_delay,n1+2,q*(m1+c3-1))
                             
                         if m1+m2+c3-1<=1:
                             if n2==1:
                                 result[2] = q*(n1+1)*m2
                                 self.fillDelay(dict_delay,n1+1,q*m2)
                             else:
                                 result[2] = q*(2-m1-c3)*(n1+1)+q/2*(2*n1+n2+1)*(n2-2)+q*(m1+m2+c3-1)*(n1+n2)
                                 self.fillDelay(dict_delay,n1+1,q*(2-m1-c3))
                                 for i in range(1,n2-2+1):
                                     self.fillDelay(dict_delay,n1+1+i,q)
                                 self.fillDelay(dict_delay,n1+n2,q*(m1+m2+c3-1))
                         else:#m1+m2+c3-1>1
                             if n2==1:
                                 result[2] = q*(2-m1-c3)*(n1+1)+q*(n1+2)*(m1+m2+c3-2)
                                 self.fillDelay(dict_delay,n1+1,q*(2-m1-c3))
                                 self.fillDelay(dict_delay,(n1+2),q*(m1+m2+c3-2))
                             else:
                                 result[2] = q*(2-m1-c3)*(n1+1)+q/2*(2*n1+n2+1)*(n2-2)+q*(n1+n2)+q*(m1+m2+c3-2)*(n1+n2+1)
                                 self.fillDelay(dict_delay,n1+1,q*(2-m1-c3))
                                 for i in range(1,n2-2+1):
                                     self.fillDelay(dict_delay,n1+1+i,q)
                                 self.fillDelay(dict_delay,n1+n2,q)
                                 self.fillDelay(dict_delay,n1+n2+1,q*(m1+m2+c3-2))
                 else:##c1>1,c2>1,c3>1
                     #print("c1>1,c2>1,c3>1")
                     dict_delay[0]+=3*q
                     result[1]=q/2*(n1+4)*(n1-1)+q*(n1+2)*m1
                     for i in range(1,n1-1+1):
                         self.fillDelay(dict_delay,2+i,q)
                     self.fillDelay(dict_delay,n1+2,q*m1)
                     if m1+m2<=1:
                         if n2==1:
                             result[2] = q*m2*(n1+1)
                             self.fillDelay(dict_delay,n1+1,q*m2)
                         else:
                             result[2] = q*(1-m1)*(n1+1)+q/2*(2*n1+n2+1)*(n2-2)+q*(m1+m2)*(n2+n1) 
                             self.fillDelay(dict_delay,n1+1,q*(1-m1))
                             for i in range(1,n2-2+1):
                                 self.fillDelay(dict_delay,n1+1+i,q)
                             self.fillDelay(dict_delay,(n2+n1),q*(m1+m2))
                         if  m1+m2+m3<=1:
                             if n3<2:
                                 result[3] = q*m3*(n1+n2-1)
                                 self.fillDelay(dict_delay,(n2+n1-1),q*(m3))
                             else:
                                 result[3] = q*(1-m1-m2)*(n1+n2-1)+q/2*(2*n1+2*n2+n3-3)*(n3-2)+q*(m1+m2+m3)*(n1+n2+n3-2)
                                 self.fillDelay(dict_delay,(n1+n2-1),q*(1-m1-m2))  
                                 for i in range(1,n3-2+1):
                                     self.fillDelay(dict_delay,n1+n2-1+i,q)
                                 self.fillDelay(dict_delay,(n1+n2+n3-2),q*(m1+m2+m3))
                         elif m1+m2+m3>1:
                             if n3<2:
                                 result[3] = q*(1-m1-m2)*(n1+n2-1)+q*(m1+m2+m3-1)*(n1+n2)
                                 self.fillDelay(dict_delay,(n2+n1-1),q*(1-m1-m2))
                                 self.fillDelay(dict_delay,(n2+n1),q*(m1+m2+m3-1))
                             else:
                                 result[3] = q*(1-m1-m2)*(n1+n2-1)+q/2*(2*n1+2*n2+n3-3)*(n3-2)+q*(n1+n2+n3-2)+q*(m1+m2+m3-1)*(n1+n2+n3-1)
                                 self.fillDelay(dict_delay,(n2+n1-1),q*(1-m1-m2))
                                 for i in range(1,n3-2+1):
                                     self.fillDelay(dict_delay,(n2+n1-1)+i,q)
                                 self.fillDelay(dict_delay,(n1+n2+n3-2),q)
                                 self.fillDelay(dict_delay,(n1+n2+n3-1),q*(m1+m2+m3-1))
                     else:#m1+m2>1
                         if n2==1:
                             result[2] = q*(1-m1)*(n1+1)+q*(m1+m2-1)*(n2+n1+1)
                             self.fillDelay(dict_delay,(n1+1),q*(1-m1))
                             self.fillDelay(dict_delay,(n2+n1+1),q*(m1+m2-1))
                         else:
                             
                             result[2] = q*(1-m1)*(n1+1)+q/2*(2*n1+n2+1)*(n2-2)+q*(n2+n1)+q*(m1+m2-1)*(n2+n1+1)
                             self.fillDelay(dict_delay,(n1+1),q*(1-m1))
                             for i in range(1,n2-2+1):
                                 self.fillDelay(dict_delay,(n1+1)+i,q)
                             self.fillDelay(dict_delay,(n2+n1+1),q*(m1+m2-1))
                             self.fillDelay(dict_delay,(n2+n1),q)
                         if m1+m2+m3-1<=1:
                             if n3-2<0:
                                 result[3]=q*(n1+n2)*m3
                                 self.fillDelay(dict_delay,(n2+n1),q*(m3))
                             else:
                                 result[3] = q*(n1+n2)*(2-m1-m2)+q/2*(2*n1+2*n2+n3-1)*(n3-2)+q*(m1+m2+m3-1)*(n1+n2+n3-1)
                                 self.fillDelay(dict_delay,(n2+n1),q*(2-m1-m2))
                                 for i in range(1,n3-2+1):
                                     self.fillDelay(dict_delay,(n2+n1)+i,q)
                                 self.fillDelay(dict_delay,(n1+n2+n3-1),q*(m1+m2+m3-1))
                             
                         elif m1+m2+m3-1>1:
                             if n3-2<0:
                                 result[3] = q*(n1+n2)*(2-m1-m2)+q*(n1+n2+1)*(m1+m2+m3-2)
                                 self.fillDelay(dict_delay,(n1+n2),q*(2-m1-m2))
                                 self.fillDelay(dict_delay,(n1+n2+1),q*(m1+m2+m3-2))
                             else:
                                 result[3] = q*(n1+n2)*(2-m1-m2)+q/2*(2*n1+2*n2+n3-1)*(n3-2)+q*(n1+n2+n3-1)+q*(m1+m2+m3-2)*(n1+n2+n3) 
                                 self.fillDelay(dict_delay,(n1+n2),q*(2-m1-m2))
                                 for i in range(1,n3-2+1):
                                     self.fillDelay(dict_delay,(n1+n2)+i,q)
                                 self.fillDelay(dict_delay,(n1+n2+n3-1),q)
                                 self.fillDelay(dict_delay,(n1+n2+n3),q*(m1+m2+m3-2))
        
        if c1+c2+c3==0:
            result=[0,0,0,0]
            
        else:
            result[0] = (float("%.3f"%((result[1]+result[2]+result[3])/(c1+c2+c3)/q)))
        return result,dict_delay
        