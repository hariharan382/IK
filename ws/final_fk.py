def fk(self, theta1, theta2, theta3, i):
    # dh(self,a, q, d, t):
    if (i == -1):
        theta1 = -theta1
        theta2 = -theta2
        theta3 = -theta3
    """fg = self.dh(0, 0, off1, -i*theta1)
    a = self.dh(0, i*90, l1, -i*(90-theta2))
    b = self.dh(l2, 0, 0, -i*theta3)
    c = self.dh(l3, 0, 0, 0) """
    # fg = self.dh(off1, 0, 0, -i * theta1)

    # right
    """fg = self.dh(0, 0, off1, -theta1)
    a = self.dh(-90, 0, l1, 90+theta2)
    b = self.dh(0, l2, 0, theta3)
    c = self.dh(0, l3, 0, 0) """
    # left
    if i == -1:
        a = 1
    else:
        a = 0
    """fg = self.dh(0, 0, off1, theta1)
    a = self.dh(90, 0, l1,-a*180+ (90 + theta2))
    b = self.dh(0, l2, 0, theta3)
    c = self.dh(0, l3, 0, 0)"""

    # hybrid

    fg = self.dh(0, 0, off1, -i * theta1)
    a = self.dh(-i * 90, 0, l1, -a * 180 + (90 + theta2))
    b = self.dh(0, l2, 0, theta3)
    c = self.dh(0, l3, 0, 0)

    self.lin_plot(o, self.point(fg))
    self.lin_plot(self.point(fg), self.point(fg @ a))
    self.lin_plot(self.point(fg @ a), self.point(fg @ a @ b))
    self.lin_plot(self.point(fg @ a @ b), self.point(fg @ a @ b @ c))
    # print(fg @ a @ b @ c @np.transpose(o))
    q = fg @ a @ b @ c @ np.transpose(o)
    x1 = q.item(0)
    y1 = q.item(1)
    z1 = q.item(2)
    print("x: ", np.round(x1, 2), "   y: ", np.round(y1, 2), "   z1: ", np.round(z1, 2))