def ik(x,y,z,right):
    phi = math.atan(x / y)
    P = math.sqrt(x ** 2 + y ** 2)
    Q = math.sqrt(P ** 2 - l1 ** 2)
    if right == -1:
        theta1 = math.atan(Q / l1) - phi  # + np.pi
    else:
        a=0
        theta1 = phi +np.pi - math.atan(Q / l1)   # + np.pi
    #print(math.degrees(phi))

    R=math.sqrt(Q**2 + (z-off1)**2)
    if off1<z:
        gamma=math.atan((z-off1)/Q)
    else:
        gamma = math.atan((off1-z) / Q)
        print("-----")
        print(np.degrees(gamma))
    M=(R**2-l2**2-l3**2)/(2*l2*l3)
    theta2=math.atan((math.sqrt(1-M**2))/M) + gamma +3*np.pi/4
    N=(R**2+l2**2-l3**2)/(2*R*l2)
    theta3=-math.atan(N/(math.sqrt(1-N**2)))+3*np.pi/4
    if right == -1:
        print(180 - np.degrees(theta1), "   ----   ", 255 - np.degrees(theta2), "   ---   ",
              180 - 45 - np.degrees(theta3))
        return np.array([180-np.degrees(theta1),255 - np.degrees(theta2), 135-np.degrees(theta3)])

    if right ==1:
        print(np.degrees(theta1), " --- ", np.degrees(theta2), " --- ", np.degrees(theta3))
        return np.array([np.degrees(theta1), np.degrees(theta2), np.degrees(theta3)])

    print(180-np.degrees(theta1),"   ----   ",255- np.degrees(theta2), "   ---   ",180-45-np.degrees(theta3))
    #return theta1,theta2,theta3
    #return np.array([np.degrees(theta1), np.degrees(theta2), np.degrees(theta3)])
