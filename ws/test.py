import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()

ax=plt.axes(projection='3d')
ax.scatter(0,0,0,cmap='Greens')
ax.scatter(6,6,6,cmap='Greens')
plt.plot([1,2,3],
         [1,2,3],
         [1,2,3],'bo-',lw=2)
#ax.plot_wireframe(x,y,z)
plt.show()