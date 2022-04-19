import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d

limit=10
fig = plt.figure()
ax=fig.add_subplot(111,projection='3d')
ax.set_xlim(-limit,limit)
ax.set_ylim(-limit,limit)
ax.set_zlim(-limit,limit)
ax.set_xlabel('"X')
ax.set_ylabel("Y")
ax.set_zlabel("Z")

m=np.matrix([[2,-2,1,1]
            ,[-3,3,-2,-1]
            ,[1,0,1,0]
            ,[0,0,0,0]])
b=np.matrix([[0,5,6/np.sqrt(2),6/np.sqrt(2)]
            ,[0,0,0,0]
            ,[0,0,6/np.sqrt(2),-6/np.sqrt(2)]])

#fig=plt.figure()
#ax=plt.axes(projection='3d')

for u in np.arange(0,1,0.01):
    Y = np.matrix([u ** 3, u ** 2, u, 1])
    df=Y@m@b.transpose()
    ax.scatter(df.item(0),df.item(1),df.item(2),cmap='Greens')
    if u<0.5:
        print(df)


ax.scatter(0,0,0,cmap='Greens')
ax.scatter(5,5,5,cmap='Greens')
x=Y@m@b.transpose()
print(x)

plt.show()