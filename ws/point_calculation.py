import numpy as np

front_length = 55
back_length = 55
width = 80

Trb = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, width / 2],
    [0, 0, 1, -back_length],
    [0, 0, 0, 1]])
Trf = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, width / 2],
    [0, 0, 1, front_length],
    [0, 0, 0, 1]])
Tlf = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, -width / 2],
    [0, 0, 1, front_length],
    [0, 0, 0, 1]])
Tlb = np.array([
    [1, 0, 0, 0],
    [0, 1, 0, -width / 2],
    [0, 0, 1, -back_length],
    [0, 0, 0, 1]])

front_right_leg_foot_coordinates=np.array([-16.97,2,2,1])
front_left_leg_foot_coordinates=np.array([-16.97,-2,2,1])
back_right_leg_foot_coordinates=np.array([-16.97,2,2,1])
back_left_leg_foot_coordinates=np.array([-16.97,-2,2,1])

front_right=Trf@front_right_leg_foot_coordinates
front_left=Tlf@front_left_leg_foot_coordinates
back_right=Trb@back_right_leg_foot_coordinates
back_left=Tlb@back_left_leg_foot_coordinates

print("front_right:  ",front_right)
print("-------------------------------------------------")
print("front_left:  ",front_left)
print("-------------------------------------------------")
print("back_right:  ",back_right)
print("-------------------------------------------------")
print("back_left:  ",back_left)
print("-------------------------------------------------")