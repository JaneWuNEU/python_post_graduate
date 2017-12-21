# -*- coding: utf-8 -*-
"""
Created on Sun Jan  8 11:03:59 2017

@author: User
"""
'''
这里需要验证T0和p以及延迟sigma之间的关系
'''
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
from matplotlib.ticker import LinearLocator, FormatStrFormatter
sigma =  np.linspace(0.1,0.1,500)
C = 400
p = np.linspace(0.5*C,1*C,500)
T = np.linspace(0.5,1,500)
distance = (5*p*T-sigma*p+sigma**2*C-7*C*T*sigma)/2/p
print(distance)
T0 = (p*sigma-sigma*sigma*C)/(5*p-7*C*sigma)
#print(T0)
'''
fig = plt.figure()
ax = fig.gca(projection = '3d')

x =sigma
y = p
x,y = np.meshgrid(x,y)
z = T0
surf = ax.plot_surface(x, y, z, rstride=1, cstride=1, cmap=cm.coolwarm,
                       linewidth=0, antialiased=False)
ax.set_zlim(-1, 1)

ax.zaxis.set_major_locator(LinearLocator(10))
ax.zaxis.set_major_formatter(FormatStrFormatter('%.02f'))

fig.colorbar(surf, shrink=0.5, aspect=5)
'''
#plt.show()