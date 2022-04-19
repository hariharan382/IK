import matplotlib as mpl
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from mpl_toolkits.mplot3d import proj3d


class Arrow3D(FancyArrowPatch):
    def __init__(self, xs, ys, zs, *args, **kwargs):
        FancyArrowPatch.__init__(self, (0, 0), (0, 0), *args, **kwargs)
        self._verts3d = xs, ys, zs

    def draw(self, renderer):
        xs3d, ys3d, zs3d = self._verts3d
        xs, ys, zs = proj3d.proj_transform(xs3d, ys3d, zs3d, renderer.M)
        self.set_positions((xs[0], ys[0]), (xs[1], ys[1]))
        FancyArrowPatch.draw(self, renderer)


if __name__ == '__main__':
    center = [0, 0, 0]
    length = 1
    width = 1
    height = 1
    fig = plt.figure()
    ax1 = fig.add_subplot(111, projection='3d')
    ax1.set_xlabel('X')
    ax1.set_xlim(-1, 1)
    ax1.set_ylabel('Y')
    ax1.set_ylim(-1, 1)
    ax1.set_zlabel('Z')
    ax1.set_zlim(-1, 1)

    # Here we create the arrows:
    arrow_prop_dict = dict(mutation_scale=20, arrowstyle='->', shrinkA=0, shrinkB=0)

    a = Arrow3D([0, 1], [0, 0], [0, 0], **arrow_prop_dict, color='r')
    ax1.add_artist(a)
    a = Arrow3D([0, 0], [0, 1], [0, 0], **arrow_prop_dict, color='b')
    ax1.add_artist(a)
    a = Arrow3D([0, 0], [0, 0], [0, 1], **arrow_prop_dict, color='g')
    ax1.add_artist(a)

    # Give them a name:
    ax1.text(0.0, 0.0, -0.1, r'$0$')
    ax1.text(1.1, 0, 0, r'$x$')
    ax1.text(0, 1.1, 0, r'$y$')
    ax1.text(0, 0, 1.1, r'$z$')

    plt.show()