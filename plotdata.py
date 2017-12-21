# -*- coding: utf-8 -*-
"""
Created on Wed Jul 26 08:22:59 2017

@author: User
"""
import numpy as np
import matplotlib.pylab as plt
class PlotData:
    def _autolabel(self,barList):
        for rect in barList:
            height = rect.get_height()
            height_text = '%s' % float(height)
            print(height_text)
            if height_text == '0.0':
                height_text = '0'
            plt.text(rect.get_x(), 1.03*height, height_text)
        
    def plotBar(self,data,colors,labels,title,legend,xlabel="X",ylabel="Y",bar_width = 0.8,index = None,xticks=None,alpha=0.4,ylimit = None):
        if index== None:
            index = np.arange(len(data[0]))
        #print(index)
        fig, ax = plt.subplots()  
        for i in range(len(data)):
            print(i*(bar_width/2))
            bar = plt.bar(index+i*(bar_width/2),data[i],bar_width/2,alpha = alpha,color = colors[i],label = labels[i])
            self._autolabel(bar)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        if ylimit!=None:
            plt.ylim(0,ylimit)
        plt.title(title)
        if xticks!=None:
            plt.xticks(index+0.5*bar_width,xticks)
        plt.legend()
        plt.show()
    def plotPie(self,labels,data,title,colors):

           '''
           fileQ = [q]
           data = []
           file = []           
           for i in fileQ:
               if "ATBM" == Type:
                   file = "F:\data\experiment/Seperate_Delay_ATBM_q"+str(q)+".xlsx"
               else:
                   file = "F:\data\experiment/Seperate_Delay_SQ_q"+str(q)+".xlsx"
                   for j in range(4,10):
                       data.append(caculateSumOfSeperateDelay(file,j))
           '''
           sizes = data
           #explode = (0.1,0)  # only "explode" the 2nd slice (i.e. 'Hogs')
           fig1, ax1 = plt.subplots()
           textprops = {"fontsize":18}
           #explode=explode,
           ax1.pie(sizes, colors = colors,labels=labels, autopct='%1.1f%%',
                  shadow=True,textprops=textprops)
           ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
           plt.title(title)
           plt.show()  
    def plot4DSeperate(self,x,y,z,a,q):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        sp=ax.scatter(x,y,z,c = a,marker="o")
        ax.set_xlim(0,q)
        ax.set_zlim(0,q)
        ax.set_ylim(0,q)
        ax.set_xlabel('C1',fontsize=15)
        ax.set_ylabel('C2',fontsize=15)
        ax.set_zlabel('C3',fontsize=15)
        #plt.legend(["ACM","ACM*1.05","ACM*1.1","ACM*1.2","Q_Len"],fontsize=18)
        plt.grid(True)
        fig.colorbar(sp)
        plt.title(u""+str(q)+"级队列时SQ的请求延迟",fontsize=18)
        #plt.legend(["dis = 1:+","dis = -1:*"])  
    def plot4D(self,x,y,z,a,q):
       fig = plt.figure()
       ax = fig.add_subplot(111, projection='3d')
       for i in range(len(a)):
           if a[i]==1:
               ax.scatter([x[i]], [y[i]], [z[i]], s=100,c="r",marker = "_")
           elif a[i]==-1:
               ax.scatter([x[i]], [y[i]], [z[i]], s=100,c="k",marker = "*")        
       ax.set_xlim(0,q)
       ax.set_zlim(0,q)
       ax.set_ylim(0,q)
       ax.set_xlabel('C1',fontsize=15)
       ax.set_ylabel('C2',fontsize=15)
       ax.set_zlabel('C3',fontsize=15)
       #plt.legend(["ACM","ACM*1.05","ACM*1.1","ACM*1.2","Q_Len"],fontsize=18)
       plt.grid(True)
       plt.title(u""+str(q)+"级队列时ATBM和SQ请求延迟的差值",fontsize=16)
       plt.legend(["A<S:-","A>S:*"],fontsize=14)

