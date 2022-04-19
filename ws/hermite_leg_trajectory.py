import numpy as np
import matplotlib.pyplot as plt
import math

import mpl_toolkits.mplot3d
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

M=np.array([[-8,     18, -11,      0, 1],
            [-8,     14,  -5,      0, 0],
            [   16,    -32,  16,      0, 0],
            [   -1,    2.5,  -2,    0.5, 0],
            [    2,     -3,   1,      0, 0]])
h=5
stepLength=7

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




def point_matrix(P1,DC1,DC2,theta):
    right = 1
    x=10
    theta=90-theta
    P3 = np.array([h, stepLength * np.cos(np.radians(theta)) * 0.5, stepLength * np.sin(np.radians(theta)) * 0.5])
    P2 = np.array([0, stepLength * np.cos(np.radians(theta)), stepLength * np.sin(np.radians(theta))])
    T1 = np.array([np.cos(np.radians(45)), -x * np.cos(np.radians(theta)) * np.sin(np.radians(45)),
                   -x * np.sin(np.radians(theta)) * np.sin(np.radians(45))])
    T2 = np.array([-np.cos(np.radians(45)), -x * np.cos(np.radians(theta)) * np.sin(np.radians(45)),
                   -x * np.sin(np.radians(theta)) * np.sin(np.radians(45))])

    return np.array([P1,P2,P3,T1,T2])

P1=np.array([0,0,0])

def hermite(theta,right):
    """x:  -16.97    y:  2.0    z1:  2.0 # right
---
x:  -16.97    y:  -2.0    z1:  2.0     # left"""
    home=np.matrix([[1,0,0,-16.97],
                    [0,1,0,right*2],
                    [0,0,1,2],
                    [0,0,0,1]])
    for u in np.arange(0,1.05,0.05):

        U = np.array([u ** 4, u ** 3, u ** 2, u, 1])
        B = np.dot(M, U)
        DC1 = 1 / 1.432
        DC2 = 0
        P1 = np.array([0, 0, 0])
        L=point_matrix(P1,DC1,DC2,theta)
        #print(L)
        cf=L[0][:]*(1-u) + L[1][:]*(u)
        #if u == 0:
            #print(L[1][:][0],' -- ',L[1][:][1],' -- ',L[1][:][2])
            #print(L[2][:][0], ' -- ', L[2][:][1], ' -- ', L[2][:][2])
        #ax.scatter(L[1][:][0],L[1][:][1],L[1][:][2],linewidths=2,cmap='Greens')
        #ax.scatter(L[2][:][0], L[2][:][1], L[2][:][2], linewidths=2,cmap='Greens')
        df = np.dot(B, L)
        print(df)
        df=np.array([df[0],df[1],df[2],1])

        fp=np.dot(home,df)
        #print(fp)

        ax.scatter(fp.item(0),fp.item(1),fp.item(2), linewidths=2, cmap='Greens')
        #print(fp.item(0),"<---> ",fp.item(1),"<--->",fp.item(2))


        final_array=ik(fp.item(0),fp.item(1),fp.item(2),right)
        #print(final_array)
        #print("====")

        yh = FK(final_array.item(0), final_array.item(1), final_array.item(2))
        yh.fk(final_array.item(0), final_array.item(1), final_array.item(2), right)  # --- right works



        #ax.plot3D([0,3*np.cos(np.radians(theta))*np.sin(np.radians(45))],[0,3*np.sin(np.radians(theta))*np.sin(np.radians(45))],[0,3*np.cos(np.radians(45))],'b')

def ik(x,y,z,right):
    phi = math.atan(abs(x) / abs(y))
    P = math.sqrt(x ** 2 + y ** 2)
    Q = math.sqrt(P ** 2 - l1 ** 2)
    #print(np.degrees(phi))
    if right == 1:
        theta1 = math.atan2(x,y) + math.atan(Q/l1)

        #print(np.degrees(math.atan2(y,x)- np.pi/2))

        #print(np.degrees(math.atan(Q/l1)))
        #print(".................")
    else:
        a=0
        #print("////-------////")
        theta1 = math.atan(Q / l1) -np.pi -math.atan2(x,y)
        #print(np.degrees(math.atan(Q / l1)))
        #print("=========")
        #print(np.degrees(math.atan2(x,y)))

    gamma= math.atan2(-Q,z-off1)
    R=math.sqrt((z-off1)**2+Q**2)
    N=(R**2-l2**2-l3**2)/(2*l2*l3)
    M=(l3**2-l2**2-R**2)/(2*l2*R)
    #print("gamma :" , np.degrees(gamma))
    theta2=gamma+math.atan2((math.sqrt(1-M**2)),M)
    #print("theta2: ",np.degrees(math.atan2((math.sqrt(1-M**2)),M)))
    theta3=math.atan2((math.sqrt(1-N**2)),N)

    #return np.array([np.degrees(theta1),np.degrees(theta2),np.degrees(theta3)])



    #print(np.round(np.degrees(theta1)), "   ----   ", np.round(np.degrees(theta2)), "   ---   ", np.round(np.degrees(theta3)))
    if right == -1:
        print(np.round(np.degrees(theta1),1), "   ----   ", -45+ np.round(np.degrees(theta2),1), "   ---   ",
              180 - 45 - np.round(np.degrees(theta3),1))
        return np.array([np.round(np.degrees(theta1), 1), np.round(np.degrees(theta2)), np.round(np.degrees(theta3), 1)])

    if right ==1:
        print(np.round(np.degrees(theta1),0), " --- ", np.round(np.degrees(theta2),0), " --- ", np.round(np.degrees(theta3),0))
        return np.array([np.round(np.degrees(theta1),1), np.round(np.degrees(theta2),1), np.round(np.degrees(theta3),1)])



    #return theta1,theta2,theta3
    #return np.array([np.degrees(theta1), np.degrees(theta2), np.degrees(theta3)])

yh=FK(0,0,0)
yh.fk(0,50,80,1)
#x:  -16.39    y:  -2.0    z1:  -14.39
#x:  -20.49    y:  -2.0    z1:  -6.49
#print(ik(-16.97,2,2,1))

#print(ik(-20.49,-2,-6.49,-1))
#x:  -12.0    y:  2.0    z1:  14.0
#print(ik(-12,-2,14,1))
#hermite(0,1)
#hermite(45,-1)
#hermite(45,1)
x=3
theta=0
#ax.plot3D([0,-x * np.cos(np.radians(theta))],[0,-x * np.sin(np.radians(theta)) * np.cos(np.radians(45))],[0,-x * np.sin(np.radians(theta)) * np.cos(np.radians(45))],'b')
#yh=FK(0,0,0)
#yh.fk(0,68,83,1)
#fk(0,45,90,1)
print("///////////////////")
#x:  -20.49    y:  2.0    z1:  -6.49
print(ik(-20.78,2,2,1))


#plt.plot([0,5],[0,5],[0,5])
#plt.show()