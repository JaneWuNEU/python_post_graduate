import matplotlib
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
'''
# domains
x = np.logspace(-1.,np.log10(5),50) # [0.1, 5]
y = np.linspace(6,9,50)             # [6, 9]
z = np.linspace(-1,1,50)            # [-1, 1]

# convert to 2d matrices
Z = np.outer(z.T, z)        # 50x50
X, Y = np.meshgrid(x, y)    # 50x50
# fourth dimention - colormap
# create colormap according to x-value (can use any 50x50 array)
color_dimension = X # change to desired fourth dimension
print(X.size)
minn, maxx = color_dimension.min(), color_dimension.max()
norm = matplotlib.colors.Normalize(minn, maxx)
m = plt.cm.ScalarMappable(norm=norm, cmap='jet')
m.set_array([])
fcolors = m.to_rgba(color_dimension)

# plot
fig = plt.figure()
ax = fig.gca(projection='3d')
ax.plot_surface(X,Y,Z, rstride=1, cstride=1, facecolors=fcolors, vmin=minn, vmax=maxx, shade=False)
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
fig.canvas.show()
'''
  
n_groups = 5  
   
means_men = (20, 35, 30, 35, 27) 
means_women = (25, 32, 34, 20, 25)  
 
fig, ax = plt.subplots()  
index = np.arange(n_groups)  
bar_width = 0.35  
 
opacity = 0.4 
rects1 = plt.bar(index, means_men, bar_width,alpha=opacity, color='b',label=    'Men')  
rects2 = plt.bar(index + bar_width, means_women, bar_width,alpha=opacity,color='r',label='Women')  

plt.xlabel('Group')  
plt.ylabel('Scores')  
plt.title('Scores by group and gender')  
plt.xticks(index + bar_width, ('A', 'B', 'C', 'D', 'E'))  
plt.ylim(0,40)  
plt.legend()     
#plt.tight_layout()  
plt.show()