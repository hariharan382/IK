import numpy as np
import matplotlib.pyplot as plt
import math
import  mpl_toolkits.mplot3d
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d

limit=10
fig = plt.figure()
ax=fig.add_subplot(111,projection='3d')
ax.set_xlim(-limit,limit)
ax.set_ylim(-limit,limit)
ax.set_zlim(-limit,limit)
ax.set_xlabel('X-fk')
ax.set_ylabel("Y")
ax.set_zlabel("Z")



class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)

o=np.matrix([[0,0,0,1]])

l1=2
l2=12
l3=12
off1=2

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

class FK:
    def __init__(self, theta1, theta2,theta3):
        self.theta1=theta1
        self.theta2=theta2
        self.theta3=theta3


    def point(self,x):
        df=x@np.transpose(o)
        ax.scatter(df.item(0),df.item(1),df.item(2),cmap='Greens',linewidths=4)
        return df

    def lin_plot(self,x,y):
        a=x
        b=y
        plt.plot([a.item(0),b.item(0)],[a.item(1),b.item(1)],[a.item(2),b.item(2)],linewidth=2)

    def dh(self,a, q, d, t):

        z = np.matrix([[np.cos(math.radians(t)), -np.sin(math.radians(t)), 0, q],
                    [np.sin(math.radians(t)) * np.cos(math.radians(a)), np.cos(math.radians(t)) * np.cos(math.radians(a)),
                    -np.sin(math.radians(a)), -d * np.sin(math.radians(a))],
                    [np.sin(math.radians(t)) * np.sin(math.radians(a)), np.cos(math.radians(t)) * np.sin(math.radians(a)),
                    np.cos(math.radians(a)), d * np.cos(math.radians(a))],
                    [0, 0, 0, 1]])
        return z

    def fk(self,theta1, theta2, theta3,i):
        #dh(self,a, q, d, t):
        if (i==-1):
            theta1=theta1
            theta2=-theta2
            theta3=-theta3
        """fg = self.dh(0, 0, off1, -i*theta1)
        a = self.dh(0, i*90, l1, -i*(90-theta2))
        b = self.dh(l2, 0, 0, -i*theta3)
        c = self.dh(l3, 0, 0, 0)
        #fg = self.dh(off1, 0, 0, -i * theta1)"""

        #right
        """fg = self.dh(0, 0, off1, -theta1)
        a = self.dh(-90, 0, l1, 90+theta2)
        b = self.dh(0, l2, 0, theta3)
        c = self.dh(0, l3, 0, 0) """
         #left
        if i==-1:
            g=1
        else:
            g=0
        """fg = self.dh(0, 0, off1, theta1)
        a = self.dh(90, 0, l1,-g*180+ (90 + theta2))
        b = self.dh(0, l2, 0, theta3)
        c = self.dh(0, l3, 0, 0)"""

        #hybrid

        fg = self.dh(0, 0, off1, -i*theta1)
        a = self.dh(-i*90, 0, l1,-g*180 + (90 + theta2))
        b = self.dh(0, l2, 0, theta3)
        c = self.dh(0, l3, 0, 0)


        self.lin_plot(o, self.point(fg))
        self.lin_plot(self.point(fg), self.point(fg @ a))
        self.lin_plot(self.point(fg @ a), self.point(fg @ a @ b))
        self.lin_plot(self.point(fg @ a @ b), self.point(fg @ a @ b @ c))
        #print(fg @ a @ b @ c @np.transpose(o))
        q=fg @ a @ b @ c @np.transpose(o)
        x1 = q.item(0)
        y1 = q.item(1)
        z1 = q.item(2)
        print("x: ", np.round(x1,2), "   y: ", np.round(y1,2), "   z1: ", np.round(z1,2))


"""

z=FK(0,45,90)
z.fk(0,45,90)
print("-----------------------------------")
yh=FK(45,45,90)
yh.fk(45,45,90)
plt.show()
"""
yh=FK(45,0,0)
#yh.fk(0,45,90,1) #--- right works good
print("left_leg_below --------------------------------")
yh.fk(0,45,90,-1)
print("right_leg_below==========================")
yh.fk(0,45,90,1)
#x:  -17.38    y:  -0.49    z1:  -12.5

#x:  -12.0    y:  2.0    z1:  14.0
#plt.show()



