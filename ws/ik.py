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
ax.set_xlabel('X-ik')
ax.set_ylabel("Y")
ax.set_zlabel("Z")

o=np.matrix([[0,0,0,1]])

l1=2
l2=4
l3=4

def dh(q, a, d, t):

    z = np.matrix([[np.cos(math.radians(t)), -np.sin(math.radians(t)), 0, q],
                  [np.sin(math.radians(t)) * np.cos(math.radians(a)), np.cos(math.radians(t)) * np.cos(math.radians(a)),
                   -np.sin(math.radians(a)), -d * np.sin(math.radians(a))],
                  [np.sin(math.radians(t)) * np.sin(math.radians(a)), np.cos(math.radians(t)) * np.sin(math.radians(a)),
                   np.cos(math.radians(a)), d * np.cos(math.radians(a))],
                  [0, 0, 0, 1]])
    return z

def point(x):
    df=x@np.transpose(o)
    ax.scatter(df.item(0),df.item(1),df.item(2),cmap='Greens')
    return df

def ik(x,y,z):
    """alpha=math.degrees(math.atan(y/z))
    phi = math.degrees(math.atan(x / z))
    r=math.sqrt(z**2+x**2)
    w=r*np.cos(math.radians(phi))
    #r0=math.sqrt(h2**2-l1**2)
    h=math.sqrt(y**2+z**2)


    P=(l1**2+h**2-w**2)/(2*l1*h)
    Q=(l2**2 + r**2-l3**2)/(2*l2*r)
    R=(r**2 -l2**2-l3**2)/(2*l2*l3)  """

    h=math.sqrt(y**2+z**2)
    phi=math.degrees(math.atan( abs(y)/ abs(z)))
    w = math.sqrt(h ** 2 - l1 ** 2)
    psi=math.degrees(math.atan(abs(x) / w))
    r= math.sqrt(w ** 2 + x ** 2)
    P=(r**2 -l2**2-l3**2)/(2*l2*l3)
    Q = (l2 ** 2 + r ** 2 - l3 ** 2) / (2 * l2 * r)


    """
    z=math.degrees(math.acos(r0/h2))
    print((h**2-l2**2-l3**2))
    print(("----------"))
    print((2*l2*l3))
    #print(alpha-z)
    print("-------------")
    print(alpha,h2,r0,phi,h)
    print("------")
    print(math.acos((h2**2-l2**2-l3**2)/(2*l3*l2)))
    
    theta1=alpha + math.degrees(math.acos(r0/h))
    theta2=phi - math.degrees(math.asin((l3**2 -l2**2-h2**2)/(2*l2*h2)))
    theta3=math.degrees((math.acos((h2**2-l2**2-l3**2)/(2*l3*l2))))"""

    """theta1=alpha+math.degrees(math.atan2(P,math.sqrt(1-P**2)))
    theta2=phi+math.degrees(math.atan2(Q,math.sqrt(1-Q**2)))
    theta3=math.degrees(math.atan2(math.sqrt(1-R**2),R))
    return theta1,theta2,theta3"""
    theta1= phi - math.degrees(math.atan2(l1,w))
    if x> 0:
        theta2 = math.degrees(math.atan2(Q, math.sqrt(1 - Q ** 2))) -  psi
    else:
        theta2 = psi + math.degrees(math.atan2(Q, math.sqrt(1 - Q ** 2)))


    theta3 = math.degrees(math.atan2(math.sqrt(1 - P ** 2), P))
    return theta1, theta2, theta3





#x:  0.0    y:  2.0    z1:  -5.66 ------> home
#x:  0.0    y:  5.41    z1:  -2.59


def lin_plot(x,y):
    a=x
    b=y
    plt.plot([a.item(0),b.item(0)],[a.item(1),b.item(1)],[a.item(2),b.item(2)],linewidth=0.5)

theta1,theta2,theta3=ik(0,2,-5.66)

fg=dh(0,theta1,0,0)
a = dh(0, -90, 2, theta2)
b=dh(l2,0,0,theta3)
c=dh(l3,0,0,45)

print(round(theta1,0),round(theta2,0),round(theta3,0))

lin_plot(o,point(fg))
lin_plot(point(fg),point(fg @ a))
lin_plot(point(fg@a),point(fg @ a @ b))
lin_plot(point(fg @ a @ b),point(fg @ a @ b @ c))


##############################################
#x:  0.0    y:  5.41    z1:  -2.59
theta1,theta2,theta3=ik(0,5.41,-2)

fg=dh(0,theta1,0,0)
a = dh(0, -90, 2, theta2)
b=dh(l2,0,0,theta3)
c=dh(l3,0,0,45)

print(round(theta1,0),round(theta2,0),round(theta3,0))

lin_plot(o,point(fg))
lin_plot(point(fg),point(fg @ a))
lin_plot(point(fg@a),point(fg @ a @ b))
lin_plot(point(fg @ a @ b),point(fg @ a @ b @ c))
plt.show()



