# -*- coding: utf-8 -*-
"""
Created on Wed Jul 12 18:50:35 2017

@author: User
"""
#learn 3D plot
import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

sp = ax.scatter(np.arange(10),np.arange(10),np.arange(10),  c=np.arange(10))
plt.colorbar(sp)



# domains
x = np.logspace(-1.,np.log10(5),50) # [0.1, 5]
y = np.linspace(6,9,50)             # [6, 9]
z = np.linspace(-1,1,50)            # [-1, 1]

# convert to 2d matrices
Z = np.outer(z.T, z)        # 50x50
X, Y = np.meshgrid(x, y)    # 50x50
unit = np.ones(50)
Z1,unit = np.meshgrid(z,unit)

# fourth dimention - colormap
# create colormap according to x-value (can use any 50x50 array)
color_dimension = Z1 # change to desired fourth dimension
minn, maxx = color_dimension.min(), color_dimension.max()
print(minn.shape,maxx.shape)
norm = matplotlib.colors.Normalize(minn, maxx)
m = plt.cm.ScalarMappable(norm=norm, cmap='jet')
m.set_array([])
fcolors = m.to_rgba(color_dimension)
#print(x)
#print(X)
# plot
fig = plt.figure()
ax = fig.gca(projection='3d')
plt.colorbar(m)
sp = ax.plot_surface(X,Y,Z, rstride=1, cstride=1, facecolors=fcolors, vmin=minn, vmax=maxx, shade=False)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

fig.canvas.show()