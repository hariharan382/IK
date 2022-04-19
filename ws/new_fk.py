#!/usr/bin/env python3
import numpy as np
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

limit = 10
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.set_xlim(-limit, limit)
ax.set_ylim(-limit, limit)
ax.set_zlim(-limit, limit)
ax.set_xlabel('X')
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.quiver(0, 0, 0, 0, -3, 0,
          arrow_length_ratio=0.1)
ax.quiver(0, 0, 0, 3, 0, 0,
          arrow_length_ratio=0.1)
ax.quiver(0, 0, 0, 0, 0, 3,
          arrow_length_ratio=0.1)

class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)

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



o = np.matrix([[0, 0, 0, 1]])
def rotx(alpha):
    rx = np.array([[1, 0,          0,         ],
                   [0, cos(alpha), -sin(alpha)],
                   [0, sin(alpha), cos(alpha) ]])

    return rx

def roty(beta):
    ry = np.array([[cos(beta),   0, sin(beta)],
                   [0,           1, 0        ],
                   [-sin(beta),  0, cos(beta)]])
    return ry

def rotz(gamma):
    rz = np.array([[cos(gamma), -sin(gamma), 0],
                   [sin(gamma), cos(gamma),  0],
                   [0,          0,           1]])

    return rz
def rotxyz(alpha, beta, gamma):
    return rotx(alpha).dot(roty(beta)).dot(rotz(gamma))
def homog_transxyz(dx, dy, dz):
    trans = np.array([[1, 0, 0, dx],
                      [0, 1, 0, dy],
                      [0, 0, 1, dz],
                      [0, 0, 0, 1 ]])
    return trans
def homog_transform(dx,dy,dz,alpha,beta,gamma):
    rot4x4 = np.eye(4)
    rot4x4[:3,:3] = rotxyz(alpha,beta,gamma)
    return np.dot(homog_transxyz(dx,dy,dz),rot4x4)

def lin_plot(x, y):
    a = x
    b = y
    plt.plot([a.item(0), b.item(0)], [a.item(1), b.item(1)], [a.item(2), b.item(2)], linewidth=5)

def point(x):
    df = x @ o
    # print(df)
    ax.scatter(df.item(0), df.item(1), df.item(2), cmap='Greens')
    # print(df.item(0),"------",df.item(1),"------",df.item(2))
    return df
def deg_to_rad(x):
    p=np.radians(x)
    return p



def fk(theta1,theta2,theta3):
    theta1=deg_to_rad(theta1)
    theta2 = deg_to_rad(theta2)
    theta3 = deg_to_rad(theta3)
    p=homog_transform(off1,0,0,0,0,0)@homog_transform(0,l1,0,theta1,0,0)@homog_transform(-l2,0,0,0,theta2,0)@homog_transform(-l3,0,0,0,theta3,0)
    lin_plot(o, homog_transform(off1,0,0,0,0,0))
    lin_plot(homog_transform(off1,0,0,0,0,0), homog_transform(off1,0,0,0,0,0)@homog_transform(0,l1,0,theta1,0,0))
    lin_plot(homog_transform(off1,0,0,0,0,0)@homog_transform(0,l1,0,theta1,0,0), homog_transform(off1,0,0,0,0,0)@homog_transform(0,l1,0,theta1,0,0)@homog_transform(-l2,0,0,0,theta2,0))
    lin_plot(homog_transform(off1,0,0,0,0,0)@homog_transform(0,l1,0,theta1,0,0)@homog_transform(-l2,0,0,0,theta2,0), homog_transform(off1,0,0,0,0,0)@homog_transform(0,l1,0,theta1,0,0)@homog_transform(-l2,0,0,0,theta2,0)@homog_transform(-l3,0,0,0,theta3,0))

#fk(0,45,90)
fk(0,60,60)
plt.show()