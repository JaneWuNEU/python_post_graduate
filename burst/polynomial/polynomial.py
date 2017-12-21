# -*- coding: utf-8 -*-
"""
Created on Thu Oct 27 20:42:36 2016

@author: User
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
def createFunction():
    original_data = [97, 94, 85, 90, 85, 94, 86, 91, 95, 87, 96, 89, 86, 99, 85, 100, 93, 94, 100, 98, 88, 93, 99, 91, 94, 94, 88, 86, 94, 86, 88, 89, 96, 100, 99, 100, 93, 92, 99, 96, 85, 88, 100, 99, 88, 94, 98, 91, 88, 95, 102, 107, 101, 110, 107, 111, 112, 113, 116, 125, 123, 126, 141, 138, 132, 136, 148, 142, 154, 149, 151, 161, 167, 171, 171, 173, 174, 181, 186, 190, 90, 92, 97, 86, 95, 89, 90, 87, 86, 88, 92, 88, 94, 100, 99, 93, 96, 91, 91, 95, 88, 94, 85, 86, 86, 97, 98, 87, 85, 93, 88, 93, 85, 94, 100, 89, 89, 95, 90, 87, 85, 86, 86, 96, 86, 87, 98, 95, 93, 95, 100, 89, 92, 92, 88, 91, 96, 95, 86, 86, 100, 85, 90, 89, 91, 99, 100, 90, 98, 100, 100, 104, 99, 106, 111, 112, 118, 117, 115, 121, 125, 129, 131, 119, 128, 129, 138, 142, 132, 140, 139, 148, 148, 144, 147, 158, 150, 158, 153, 155, 96, 86, 86, 99, 95, 87, 93, 99, 97, 92, 92, 87, 88, 88, 92, 86, 96, 85, 99, 100]
    np.array(original_data)
    #plt.plot(original_data)
    #把数据划分成两个阶段 A[0,47] [48,83] B[84,140][141,181]
    
    #首先分析A,获取每个phase中的cell个数
    '''
    phaseA_0 = original_data[0:47]
    cell_amount_A0 = cellNumber( phaseA_0)
    cell_sum_A0 = totalLoadsInCell(phaseA_0,cell_amount_A0)
    print("the cell data in the phase0\n",cell_sum_A0)
    interpolateData(cell_sum_A0,phaseA_0)
    '''
    '''
    phaseA_1 = original_data[48:83]
    cell_amount_A1 = cellNumber( phaseA_1)
    cell_sum_A1 = totalLoadsInCell(phaseA_1,cell_amount_A1)
    print("the cell data in the phase1\n",cell_sum_A1)
    interpolateData(cell_sum_A1,phaseA_1)
    '''
  
    phaseB_0 = original_data[84:140]
    cell_amount_B0 = cellNumber( phaseB_0)
    cell_sum_B0 = totalLoadsInCell(phaseB_0,cell_amount_B0)
    print("the cell data in the phase2\n",cell_sum_B0)
    #interpolateData(cell_sum_B0,phaseB_0)
    
    
    phaseB_1 = original_data[141:181]
    cell_amount_B1 = cellNumber(phaseB_1)
    cell_sum_B1 = totalLoadsInCell(phaseB_1,cell_amount_B1)
    print("the cell data in the phase3\n",cell_sum_B1)    
    interpolateData(cell_sum_B1,phaseB_1)
    
    
'''
carry out the interpolate to get the result
'''
def interpolateData(cell_sum,phase_data):
    data = np.copy(cell_sum)
    measured_time = np.linspace(0, 1,np.size(data))
    measures = data
    linear_interp = interp1d(measured_time,measures)
    computed_time = np.linspace(0,1,np.size(phase_data))
    linear_results = linear_interp(computed_time)
    plt.plot(computed_time, linear_results,"--")
    plt.plot(computed_time, phase_data)
    print("result\n",linear_results)



'''
'''
def totalLoadsInCell(sourcedata,cell_number):
    data = np.copy(sourcedata)
    print("source data is ",data,"data size is",np.size(data))
    width = 0
    cell_sum = []
    #计算cell的宽度时采用的是向上取整的策略
    width = int((np.size(sourcedata)+cell_number-1)/cell_number)
    
    begin = 0
    end = begin+width 
    cell_num_threshold = int(width/2)
    
    while(begin<np.size(data)):
        #get the cell data
        cell = data[begin:end]
        print("cell data is \n",cell)
        #sum the data in each cell,then divide it with the width
        cell_sum_temp = np.sum(cell)
        if(np.size(cell)<cell_num_threshold):#最后一个区间内的个数过少
            cell_sum.append(cell_sum_temp/np.size(cell))
        else:
            cell_sum.append(cell_sum_temp/width)
        begin = end
        end = end+width
        if(end>=np.size(data)):
            end = np.size(data)
    return tuple(cell_sum)
        
'''
cell的个数在确定的时候保证是向上取整
'''
def cellNumber(sourcedata):
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
    
createFunction()