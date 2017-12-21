# -*- coding: utf-8 -*-
"""
在这个类中主要完成数据清理工作

"""
import numpy as np
class DataProcess:
    def cellNumber(self,sourcedata):
        data = np.copy(sourcedata)
        np.sort(data)#进行排序
        #获取分位数
        firstquarter = data[int(0.25*np.size(data))]
        print("the firstquarter is ",firstquarter)
        thirdquarter = data[int(0.75*np.size(data))]
        print("the thirdquarter is ",thirdquarter)
        #计算跨度
        length = thirdquarter-firstquarter
        #保证cell的个数向上取整
        cell_amount = int((2*length+np.size(data)**(1.0/3.0)-1)/(np.size(data)**(1.0/3.0)))
        print("cell_amount is ",cell_amount)
        return cell_amount
        
    def normalize(self,data,step):
        result = []
        
        return result
