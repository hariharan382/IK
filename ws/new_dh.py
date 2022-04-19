import numpy as np
import math
import matplotlib.pyplot as plt
import  mpl_toolkits.mplot3d

limit=10
fig = plt.figure()
ax=fig.add_subplot(111,projection='3d')
ax.set_xlim(-limit,limit)
ax.set_ylim(-limit,limit)
ax.set_zlim(-limit,limit)
ax.set_xlabel('X-fk')
ax.set_ylabel("Y")
ax.set_zlabel("Z")

l1=2
l2,l3=4,4

o=np.matrix([[0,0,0,1]])

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

    def dh(self,q, a, d, t):

        z = np.matrix([[np.cos(math.radians(t)), -np.sin(math.radians(t)), 0, q],
                    [np.sin(math.radians(t)) * np.cos(math.radians(a)), np.cos(math.radians(t)) * np.cos(math.radians(a)),
                    -np.sin(math.radians(a)), -d * np.sin(math.radians(a))],
                    [np.sin(math.radians(t)) * np.sin(math.radians(a)), np.cos(math.radians(t)) * np.sin(math.radians(a)),
                    np.cos(math.radians(a)), d * np.cos(math.radians(a))],
                    [0, 0, 0, 1]])
        return z

    def fk(self,theta1, theta2, theta3):
        #dh(self,a, alpha, d, theta)
        fg = self.dh(0, 90, l1, theta1)
        a = self.dh(l2, 0, 0, theta2)
        b = self.dh(l3, 0, 0, theta3)
        #c = self.dh(l3, 0, 0, 45)

        self.lin_plot(o, self.point(fg))
        self.lin_plot(self.point(fg), self.point(fg @ a))
        self.lin_plot(self.point(fg @ a), self.point(fg @ a @ b))
        #self.lin_plot(self.point(fg @ a @ b), self.point(fg @ a @ b @ c))
        #print(fg @ a @ b @ c @np.transpose(o))
        q=fg @ a @ b @np.transpose(o)
        x1 = q.item(0)
        y1 = q.item(1)
        z1 = q.item(2)
        print("x: ", np.round(x1,2), "   y: ", np.round(y1,2), "   z1: ", np.round(z1,2))

yh=FK(45,0,90)
yh.fk(45,0,90)
plt.show()