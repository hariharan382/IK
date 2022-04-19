import numpy as np
import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

M=np.array([[-8,     18, -11,      0, 1],
            [-8,     14,  -5,      0, 0],
            [   16,    -32,  16,      0, 0],
            [   -1,    2.5,  -2,    0.5, 0],
            [    2,     -3,   1,      0, 0]])

stepLength=5
stepHeight=3
Height=8
DC1=1/1.432
DC2=0

limit=10
fig = plt.figure()
ax=fig.add_subplot(111,projection='3d')
ax.set_xlim(-limit,limit)
ax.set_ylim(-limit,limit)
ax.set_zlim(-limit,limit)
ax.set_xlabel('"X')
ax.set_ylabel("Y")
ax.set_zlabel("Z")

h=3

class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)

def point_matrix(P1,DC1,DC2,theta):
    right = 1
    x=5
    P3 = np.array([stepLength*np.cos(np.radians(theta))*0.5, stepLength*np.sin(np.radians(theta))*0.5,h])
    P2 = np.array([stepLength*np.cos(np.radians(theta)),stepLength*np.sin(np.radians(theta)),0])
    T1 = np.array([-x*np.cos(np.radians(theta))*np.sin(np.radians(45)),-x*np.sin(np.radians(theta))*np.sin(np.radians(45)),np.cos(np.radians(45))])
    T2 = np.array([-x*np.cos(np.radians(theta))*np.sin(np.radians(45)),-x*np.sin(np.radians(theta))*np.sin(np.radians(45)),-np.cos(np.radians(45))])

    return np.array([P1,P2,P3,T1,T2])

P1=np.array([0,0,0])


def hermite(theta):
    for u in np.arange(0,1,0.01):

        U = np.array([u ** 4, u ** 3, u ** 2, u, 1])
        B = np.dot(M, U)
        L=point_matrix(P1,DC1,DC2,theta)
        cf=L[0][:]*(1-u) + L[1][:]*(u)
        #print(L)
        #print(L[3:][])
        #ax.quiver(L[3:][0], L[3:][1], L[3:][0], 1, 1, 1, length=0.1, normalize=True)
        if u == 0:
            print(L[1][:][0],' -- ',L[1][:][1],' -- ',L[1][:][2])
            print(L[2][:][0], ' -- ', L[2][:][1], ' -- ', L[2][:][2])
        ax.scatter(L[1][:][0],L[1][:][1],L[1][:][2],linewidths=2,cmap='Greens')
        ax.scatter(L[2][:][0], L[2][:][1], L[2][:][2], linewidths=2,cmap='Greens')
        df=np.dot(B,L)
        print("----")
        print(df.shape)
        print("............")
        ax.scatter(df.item(0),df.item(1),df.item(2),cmap='Greens')
        #print(df.item(0),df.item(1),df.item(2))
        ax.scatter(cf.item(0), cf.item(1), cf.item(2), cmap='Greens')
        arrow_prop_dict = dict(mutation_scale=20, arrowstyle='->', shrinkA=0, shrinkB=0)
        a = Arrow3D([0, 3], [0, 0], [0, 0], **arrow_prop_dict, color='r')
        ax.add_artist(a)
        a = Arrow3D([0, 0], [0, 3], [0, 0], **arrow_prop_dict, color='b')
        ax.add_artist(a)
        a = Arrow3D([0, 0], [0, 0], [0, 3], **arrow_prop_dict, color='g')
        ax.add_artist(a)
        ax.text(0.0, 0.0, -0.1, r'$0$')
        ax.text(1.1, 0, 0, r'$x$')
        ax.text(0, 1.1, 0, r'$y$')
        ax.text(0, 0, 1.1, r'$z$')
        ax.plot3D([0,3*np.cos(np.radians(theta))*np.sin(np.radians(45))],[0,3*np.sin(np.radians(theta))*np.sin(np.radians(45))],[0,3*np.cos(np.radians(45))],'b')



hermite(0)
hermite(45)
hermite(90)


plt.show()