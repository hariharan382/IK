import numpy as np
import math

def ik(x,y,z):
    R=math.sqrt(y**2+z**2)
    phi=math.atan2(abs(y),abs(z))
    Q=math.sqrt(R**2 -l1**2)
    theta1=phi + np.pi - math.atan2(Q,l1)
    if off1<x:
        P=math.sqrt(Q**2 + (x-off1)**2)
        M=(p**2 -l2**2-l3**2)/(2*l2*l3)
        theta3=math.atan2(math.sqrt(1-M**2),M)
        gamma=math.atan2((x-off1),Q)
        N=(P**2 + l2**2 -l3**2)/(2*P*l2)
        theta2=gamma + math.atan2(N,math.atan2(1-N**2))
    if x<off1:
        P=math.sqrt(Q**2 + (off-x)**2)
        M=(p**2 -l2**2-l3**2)/(2*l2*l3)
        theta3=math.atan2(math.sqrt(1-M**2),M)
        gamma=math.atan2((off1-x),Q)
        N=(P**2 + l2**2 -l3**2)/(2*P*l2)
        theta2=gamma + math.atan2(N,math.atan2(1-N**2))
    return np.array([theta1,theta2,theta3])