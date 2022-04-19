import matplotlib.pyplot as plt
import numpy as np
import mpl_toolkits.mplot3d
import math

limit=10
fig = plt.figure()
ax=fig.add_subplot(111,projection='3d')
ax.set_xlim(-limit,limit)
ax.set_ylim(-limit,limit)
ax.set_zlim(-limit,limit)
ax.set_xlabel('"X')
ax.set_ylabel("Y")
ax.set_zlabel("Z")


l = 8
b = 4
FR = np.matrix([[1, 0, 0, l / 2],
                [0, 0, 0, b / 2],
                [0, 0, 0, 0],
                [0, 0, 0, 1]])
bl = np.matrix([[1, 0, 0, -l / 2],
                [0, 1, 0, -b / 2],
                [0, 0, 1, 0],
                [0, 0, 0, 1]])
br = np.matrix([[1, 0, 0, l / 2],
                [0, 0, 0, -b / 2],
                [0, 0, 0, 0],
                [0, 0, 0, 1]])
fl = np.matrix([[1, 0, 0, -l / 2],
                [0, 1, 0, b / 2],
                [0, 0, 1, 0],
                [0, 0, 0, 1]])
o=np.matrix([[0,0,0,1]])
def point(x):
    df=x@np.transpose(o)
    ax.scatter(df.item(0),df.item(1),df.item(2),cmap='Greens')
    return df


def dh(q, a, d, t):

    z = np.matrix([[np.cos(math.radians(t)), -np.sin(math.radians(t)), 0, q],
                  [np.sin(math.radians(t)) * np.cos(math.radians(a)), np.cos(math.radians(t)) * np.cos(math.radians(a)),
                   -np.sin(math.radians(a)), -d * np.sin(math.radians(a))],
                  [np.sin(math.radians(t)) * np.sin(math.radians(a)), np.cos(math.radians(t)) * np.sin(math.radians(a)),
                   np.cos(math.radians(a)), d * np.cos(math.radians(a))],
                  [0, 0, 0, 1]])
    return z

l1=2
l2=4
l3=4
f = dh(0, -90, 20, l1)
#a,b,c=1,2,3
#z=np.matrix([a,b,c])

#print(np.sin(math.radians(90)))
#print(f)
#print(f.round(3))

point(FR)
point(bl)
point(br)
point(fl)
def lin_plot(x,y):
    a=point(x)
    b=point(y)
    plt.plot([a.item(0),b.item(0)],[a.item(1),b.item(1)],[a.item(2),b.item(2)],linewidth=0.5)
    #print("[",a.item(0),", ",a.item(1)," ,",a.item(2),"]")
    #print("[", b.item(0), ", ",b.item(1) , " ,", b.item(2), "]")

    """plt.plot([0,0,1],[1,2,3],linewidth=1)
    print(a)
    print("---------------------------")
    print(a[0][0])
    print(b)#"""

#print(point(FR))

lin_plot(FR,fl)
lin_plot(fl,bl)
lin_plot(br,FR)
lin_plot(br,bl)
"""lin_plot(point(FR),point(br))
lin_plot(point(br),point(bl))
lin_plot(point(bl),point(fl))#"""
l1=2
l2=5
l3=5
#Ik

def fk(theta1,theta2,theta3):

    r1=l2*math.sin(math.radians(theta2))
    r2=l3*math.sin(math.radians(theta3-theta2))
    X2=-l2*math.cos(math.radians(theta2))
    Y2=l1*math.cos(math.radians(theta1)) + r1*math.sin(math.radians(theta1))
    Z2=r1*math.sin(math.radians(theta1))  - l1*math.sin(math.radians(theta1))
    link1=[0,l1*math.cos(theta1),-l1*math.sin(math.radians(theta1))]
    link2=[X2,Y2,Z2]
    link3=[r2*math.cos(math.radians(theta2-theta3))-X2,Y2+r2*math.cos(math.radians(theta1)),Z2+r2*math.sin(math.radians(theta1))]
    plt.plot([0,link1[0],link2[0],link3[0]], [0,link1[1],link2[1],link3[1]], [0,link1[2],link2[2],link3[2]], linewidth=0.5)
    return link3





z = fk(20,45,120)

m=np.matrix([[2,-2,1,1]
            ,[-3,3,-2,-1]
            ,[0,0,1,0]
            ,[0,0,0,0]])
b=np.matrix([[z[0],z[0]+3,6/np.sqrt(2),-6/np.sqrt(2)]
            ,[z[1],0,0,0]
            ,[z[2],0,6/np.sqrt(2),-6/np.sqrt(2)]])

"""fig=plt.figure()
ax=plt.axes(projection='3d')"""

for u in np.arange(0,1,0.01):
    Y = np.matrix([u ** 3, u ** 2, u, 1])
    df=Y@m@b.transpose()
    ax.scatter(df.item(0),df.item(1),df.item(2),cmap='Greens')
    if u<0.5:
        print(df)



plt.show()
