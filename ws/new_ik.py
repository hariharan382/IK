import math

import numpy as np
from math import sin, cos
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from numpy.lib.polynomial import poly1d
from mpl_toolkits.mplot3d import proj3d
from numpy.matrixlib.defmatrix import matrix

def ik(x,y,z):
    phi=math.atan(abs(y)/abs(z))
    R=math.sqrt(y**2+z**2)
    Q=math.sqrt(R**2-l1**2)
    theta1=phi+math.atan(Q/l1)-np.pi/2
    print(phi)
    if off1<x:
        P=math.sqrt(Q**2+(x-off1)**2)
        gamma=math.atan((x-off1)/Q)
        M=(P**2-l2**2)/(2*l2*l3)
        theta3=math.atan(math.sqrt(1-M**2)/M)
        N=(R**2+l2**2-l3**2)/(2*l2*R)
        theta2 = math.atan(M/math.sqrt(1 - M ** 2))+gamma

    else:
        P = math.sqrt(Q ** 2 + (off1-x) ** 2)
        gamma = math.atan((off1-x) / Q)
        M = (P ** 2 - l2 ** 2) / (2 * l2 * l3)
        theta3 = math.atan(math.sqrt(1 - M ** 2) / M)
        N = (R ** 2 + l2 ** 2 - l3 ** 2) / (2 * l2 * R)
        theta2 = math.atan(M / math.sqrt(1 - M ** 2)) - gamma
    #print(np.degrees(theta1)," - - ",np.degrees(theta2)," - - ",np.degrees(theta3))
    return np.array([np.degrees(theta1),np.degrees(theta2),np.degrees(theta3)])



