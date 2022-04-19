#! /usr/binenv python3
from logging import exception
from math import sin
import math
from numpy.lib.polynomial import poly1d

from numpy.matrixlib.defmatrix import matrix

import numpy as np
import matplotlib.pyplot as plt
import rospy
#import  std_msgs.msg import Int32

from matplotlib.animation import FuncAnimation

from mpl_toolkits.mplot3d import Axes3D

import matplotlib.pyplot as mpl

mpl.rcParams['font.size'] = 30

o = np.matrix([[0, 0, 0, 1]])


class FK:
    def __init__(self, theta1, theta2, theta3):
        self.theta1 = theta1
        self.theta2 = theta2
        self.theta3 = theta3

    def point(self, x):
        df = x @ np.transpose(o)
        # ax.scatter(df.item(0),df.item(1),df.item(2),cmap='Greens')
        return df

    def lin_plot(self, x, y):
        a = x
        b = y
        plt.plot([a.item(0), b.item(0)], [a.item(1), b.item(1)], [a.item(2), b.item(2)], linewidth=0.5)

    def dh(self, q, a, d, t):
        z = np.matrix([[np.cos(math.radians(t)), -np.sin(math.radians(t)), 0, q],
                       [np.sin(math.radians(t)) * np.cos(math.radians(a)),
                        np.cos(math.radians(t)) * np.cos(math.radians(a)),
                        -np.sin(math.radians(a)), -d * np.sin(math.radians(a))],
                       [np.sin(math.radians(t)) * np.sin(math.radians(a)),
                        np.cos(math.radians(t)) * np.sin(math.radians(a)),
                        np.cos(math.radians(a)), d * np.cos(math.radians(a))],
                       [0, 0, 0, 1]])
        return z

    def fk(self, theta1, theta2, theta3):
        fg = self.dh(0, theta1, 0, 0)
        a = self.dh(0, -90, 2, theta2)
        b = self.dh(l2, 0, 0, theta3)
        c = self.dh(l3, 0, 0, 0)

        self.lin_plot(o, self.point(fg))
        self.lin_plot(self.point(fg), self.point(fg @ a))
        self.lin_plot(self.point(fg @ a), self.point(fg @ a @ b))
        self.lin_plot(self.point(fg @ a @ b), self.point(fg @ a @ b @ c))
        # print(fg @ a @ b @ c @np.transpose(o))
        T = fg @ a @ b @ c @ np.transpose(o)
        """x1 = q.item(0)
        y1 = q.item(1)
        z1 = q.item(2) """
        #return x1, y1, z1
        return T


def point(x):
    df = x @ o
    # print(df)
    ax.scatter(df.item(0), df.item(1), df.item(2), cmap='Greens')
    # print(df.item(0),"------",df.item(1),"------",df.item(2))
    return df


def dh(q, a, d, t):
    z = np.matrix([[np.cos(math.radians(t)), -np.sin(math.radians(t)), 0, q],
                   [np.sin(math.radians(t)) * np.cos(math.radians(a)),
                    np.cos(math.radians(t)) * np.cos(math.radians(a)),
                    -np.sin(math.radians(a)), -d * np.sin(math.radians(a))],
                   [np.sin(math.radians(t)) * np.sin(math.radians(a)),
                    np.cos(math.radians(t)) * np.sin(math.radians(a)),
                    np.cos(math.radians(a)), d * np.cos(math.radians(a))],
                   [0, 0, 0, 1]])
    return z


def ik(x, y, z):
    h=math.sqrt(y**2+z**2)
    phi=math.degrees(math.atan( abs(y)/ abs(z)))
    w = math.sqrt(h ** 2 - l1 ** 2)
    psi=math.degrees(math.atan(abs(x) / w))
    r= math.sqrt(w ** 2 + x ** 2)
    P=(r**2 -l2**2-l3**2)/(2*l2*l3)
    Q = (l2 ** 2 + r ** 2 - l3 ** 2) / (2 * l2 * r)
    """  try:
        alpha = math.degrees(math.atan(y / z))
        phi = math.degrees(math.atan(x / z))
        # r=math.sqrt(z**2+x**2)
    except ZeroDivisionError:
        alpha = 90
        phi = 90
        # r=1 """

    theta1= phi - math.degrees(math.atan2(l1,w))
    if x> 0:
        theta2 = math.degrees(math.atan2(Q, math.sqrt(1 - Q ** 2))) -  psi
    else:
        theta2 = psi + math.degrees(math.atan2(Q, math.sqrt(1 - Q ** 2)))


    theta3 = math.degrees(math.atan2(math.sqrt(1 - P ** 2), P))
    return theta1, theta2, theta3


"""
l1 = 2
l2 = 4
l3 = 4"""
l1=2
l2=12.35
l3=12

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

h = 7
s = 10


def rotz(gamma):
    rz = np.matrix([[np.cos(gamma), -np.sin(gamma), 0, 0],
                    [np.sin(gamma), np.cos(gamma), 0, 0],
                    [0, 0, 1, 0],
                    [0, 0, 0, 1]])

    return rz


mat = np.matrix([[1, -6, 15, -20, 15, -6, 1],
                 [-6, 30, -60, 60, -30, 6, 0],
                 [15, -60, 90, -60, 15, 0, 0],
                 [-20, 60, -60, 20, 0, 0, 0],
                 [15, -30, 15, 0, 0, 0, 0],
                 [-6, 6, 0, 0, 0, 0, 0],
                 [1, 0, 0, 0, 0, 0, 0]])
# ang=45
z = FK(0, 45, 90)
hp = z.fk(0, 45, 90)
#hp=[0,0,0]
"""
print("----------------------")
print(np.round(hp, 3))
#plt.scatter(hp[0],hp[1],hp[2],linewidths=15,c='b')
print("x:  ",round(hp[0],0),"  y: ",hp[1]," z: ",hp[2])
print("====================")
hp = np.round(hp, 3)
#print(type(hp))
#print(ik(hp[0], hp[1], hp[2]))
plt.scatter(3,3,3,linewidths=15,c='g')
plt.scatter(0, 2, -5.65, linewidths=-1, c='b')
#print("-----------------------------")
# ANGLE 
r_z = rotz(np.radians(0))
#print(r_z)

point_matrix = r_z @ np.transpose(p1) """

def point_matrix(P1,DC1,DC2,theta):
    right = 1
    x=5
    P3 = np.array([stepLength*np.cos(np.radians(theta))*0.5, stepLength*np.sin(np.radians(theta))*0.5,h])
    P2 = np.array([stepLength*np.cos(np.radians(theta)),stepLength*np.sin(np.radians(theta)),0])
    T1 = np.array([-x*np.cos(np.radians(theta))*np.sin(np.radians(45)),-x*np.sin(np.radians(theta))*np.sin(np.radians(45)),np.cos(np.radians(45))])
    T2 = np.array([-x*np.cos(np.radians(theta))*np.sin(np.radians(45)),-x*np.sin(np.radians(theta))*np.sin(np.radians(45)),-np.cos(np.radians(45))])

    return np.array([P1,P2,P3,T1,T2])
#print(np.transpose(p1))
#print("/////////////////////////////////")
#print(point_matrix)

home_transform=np.matrix([[1,0,0,0],
                          [0,1,0,2],
                          [0,0,1,-5.65654],
                          [0,0,0,1]])

def rot_bez(angle,hp):
    r_z = rotz(np.radians(angle))

    M = np.array([[-8, 18, -11, 0, 1],
                  [-8, 14, -5, 0, 0],
                  [16, -32, 16, 0, 0],
                  [-1, 2.5, -2, 0.5, 0],
                  [2, -3, 1, 0, 0]])

    p_m =home_transform @ r_z @ np.transpose(p1)
    for t in np.arange(0, 1, 0.05):
        p = np.matrix([t ** 6, t ** 5, t ** 4, t ** 3, t ** 2, t, 1])

        x1 = p @ mat @ np.transpose(p_m[0, :])
        y1 = p @ mat @ np.transpose(p_m[1, :])
        z1 = p @ mat @ np.transpose(p_m[2, :])
        # print("x1:  ",x1,"  ","y1:  ",y1,"z1  ",z1)

        ax.scatter(np.asscalar(x1), np.asscalar(y1), np.asscalar(z1), cmap='Greens')
        theta1, theta2, theta3 = ik(np.asscalar(x1), np.asscalar(y1), np.asscalar(z1))
        # print("x:",np.asscalar(x1),"y: ",np.asscalar(y1),"z: ",np.asscalar(z1))

        g = FK(round(theta1, 0), round(theta2, 0), round(theta3, 0))
        g.fk(theta1, theta2, theta3)

def matrix_expander(mat):
    e=np.pad(a, [(0, 1), (0, 1)], mode='constant',constant_values=0)
    e[-1][-1]=1
    return e

def hermite(theta):
    for u in np.arange(0,1,0.01):

        U = np.array([u ** 4, u ** 3, u ** 2, u, 1])
        B = np.dot(M, U)
        L=point_matrix(P1,DC1,DC2,theta)
        cf=L[0][:]*(1-u) + L[1][:]*(u)
        df=np.dot(B,L)
        g=matrix_expander(df)
        df = home_transform @ g
        ax.scatter(df.item(0),df.item(1),df.item(2),cmap='Greens')
        ax.scatter(cf.item(0), cf.item(1), cf.item(2), cmap='Greens')
        if u == 0.99:
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
            ax.plot3D([0, 3 * np.cos(np.radians(theta)) * np.sin(np.radians(45))],
                      [0, 3 * np.sin(np.radians(theta)) * np.sin(np.radians(45))], [0, 3 * np.cos(np.radians(45))], 'b')
        theta1, theta2, theta3 = ik(df.item(0),df.item(1),df.item(2))
        theta1, theta2, theta3 = ik(cf.item(0), cf.item(1), cf.item(2))
        g = FK(round(theta1, 0), round(theta2, 0), round(theta3, 0))
        g.fk(theta1, theta2, theta3)



plt.tight_layout()
plt.show()


