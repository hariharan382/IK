import matplotlib.pyplot as plt
import numpy as np
from sympy import symbols

# bezier plotting
#t=symbols('t')

mat=np.matrix([[1,-6,15,-20,15,-6,1],
               [-6,30,-60,60,-30,6,0],
               [15,-60,90,-60,15,0,0],
               [-20,60,-60,20,0,0,0],
               [15,-30,15,0,0,0,0],
               [-6,6,0,0,0,0,0],
               [1,0,0,0,0,0,0]])
points=np.matrix([[0,0],
                  [5,0],
                  [5,5],
                  [0,5],
                  [-5,5],
                  [-5,0],
                  [0,0]])
x=points[:,0]
y=points[:,1]
#print(p.shape)
print(mat.shape)
print(x.shape)
ls=[]
el=[]
for t in np.arange(0,1,0.05):
    #el.clear()
    p = np.matrix([t ** 6, t ** 5, t ** 4, t ** 3, t ** 2, t, 1])
    x1=p@mat@x
    y1=p@mat@y
    el=[np.asscalar(x1),np.asscalar(y1)]
   # print(el)
    #print(np.asscalar(x1)," ",np.asscalar(y1))
    ls.append(el)

r=points.squeeze()
print(r.tolist())

print(ls)
for x,y in ls:
    plt.scatter(x,y,marker='o')
for x,y in r.tolist():
    plt.scatter(x,y,marker="*",c='b')
plt.show()

