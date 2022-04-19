import math
import numpy as np
width=8
front_length=9
Trf = np.array([
            [1,0,0,0],
            [0,1,0,width/2],
            [0,0,1,front_length],
            [0,0,0,1]])

rF=np.array(([-16.97,2,2,1]))

print(Trf@rF)
sol=np.array([-16.97,42,92,1])
#print(np.linalg.inv(Trf)@sol)