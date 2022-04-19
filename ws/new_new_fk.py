#!/usr/bin/env python3
import numpy as np
import math
from math import sin, cos
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from numpy.lib.polynomial import poly1d
from mpl_toolkits.mplot3d import proj3d
from numpy.matrixlib.defmatrix import matrix

l1=2
l2=12.35
l3=12
off1=2

class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)


limit = 20
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)
ax.set_zlim(-limit, limit)
ax.set_xlabel('X')
ax.set_ylabel("Y")
ax.set_zlabel("Z")

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

def deg_to_rad(x):
    p=np.radians(x)
    return p

def lin_plot(x, y):
    a = x
    b = y
    plt.plot([a.item(0), b.item(0)], [a.item(1), b.item(1)], [a.item(2), b.item(2)], linewidth=6)

def fk(theta1,theta2,theta3,p):
    theta1 = deg_to_rad(theta1)
    theta2 = deg_to_rad(theta2)
    theta3 = deg_to_rad(theta3) - deg_to_rad(180)
    Q=l2*np.sin(theta2)+l3*np.sin(theta2+theta3)
    x1,y1,z1=off1,p*(l1*np.cos(theta1)),l1*np.sin(theta1)
    XYZ1=np.array([x1,y1,z1])
    x2,y2,z2=off1-l2*np.cos(theta2),p*(l1*np.cos(theta1)+l2*np.sin(theta2)*np.sin(theta1)),l1*np.sin(theta1)-l2*np.cos(theta1)*np.sin(theta2)
    XYZ2=np.array([x2,y2,z2])
    X,Y,Z=off1-l2*np.cos(theta2)+l3*np.cos(theta3+theta2),p*(l1*np.cos(theta1)+Q*np.sin(theta1)), (l1*np.sin(theta1)-Q*np.cos(theta1))
    XYZ=np.array([X,Y,Z])
    O=np.array([0,0,0])
    off=np.array([off1,0,0])
    ax.scatter3D(X, Y, Z, color="green", linewidths=5)

    lin_plot(O,off)
    lin_plot(off,XYZ1)
    lin_plot(XYZ1,XYZ2)
    lin_plot(XYZ2,XYZ)

def ik(x,y,z):
    R=math.sqrt(y**2+z**2)
    phi=math.atan2(abs(z),abs(y))
    Q=math.sqrt(R**2 -l1**2)
    theta1=phi + np.pi - math.atan2(Q,l1)
    if off1<x:
        P=math.sqrt(Q**2 + (x-off1)**2)
        M=(p**2 -l2**2-l3**2)/(2*l2*l3)
        theta3=math.atan2(math.sqrt(1-M**2),M)
        gamma=math.atan2((x-off1),Q)
        N=(P**2 + l2**2 -l3**2)/(2*P*l2)
        theta2=gamma + math.atan2(N,math.atan2(1-N**2))
    else:
        P=math.sqrt(Q**2 + (off1-x)**2)
        M=(P**2 -l2**2-l3**2)/(2*l2*l3)
        theta3=math.atan2(math.sqrt(1-M**2),M)
        gamma=math.atan2((off1-x),Q)
        N=(P**2 + l2**2 -l3**2)/(2*P*l2)
        theta2=gamma + math.atan2(N,math.sqrt(1-N**2))
    print(np.degrees(theta1), " --- ", np.degrees(theta2), " ---- ", np.degrees(theta3))
    return np.array([np.degrees(theta1), np.degrees(theta2), np.degrees(theta3)])



#fk(45,45,45,-1)
#fk(45,90,90,1)
a,b,c=off1,l1,-10
#a,b,c=deg_to_rad(a),deg_to_rad(b),deg_to_rad(c)
#fk(ik(a,b,c)[0],ik(a,b,c)[1],ik(a,b,c)[2],-1)
#fk(0,26,131.5,1)
fk(0,45,180,1)
#fk(0,45,90,-1)
ax.scatter(a,b,c, cmap='Greens',linewidths=5)
#fk(0,-45,-45,1)
#fk(-30,-75,-60,1)
#fk(0,45,45)
plt.show()