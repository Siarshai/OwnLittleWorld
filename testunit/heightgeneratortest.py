from mpl_toolkits.mplot3d.axes3d import Axes3D
import numpy as np
import matplotlib.pyplot as plt
from mapgenerator.heightgenerator import *
import scipy

X_CELL_SIZE = 64
Y_CELL_SIZE = 64
CELL_DIVISOR = 32
AMPLITUDE = 5
PERSISTENCE = 0.55
GENERATORS_NUMBER = 5

if __name__ == "__main__":

    hg = HeightGenerator(x_cells_size=X_CELL_SIZE, y_cells_size=Y_CELL_SIZE, base_points_divisor=CELL_DIVISOR,
                         amplitude=AMPLITUDE, persistence=PERSISTENCE, generators_number=GENERATORS_NUMBER,
                         regular_constituent_function_closure=hill_map_height_regular_constituent_closure)

    wm = hg.generate_map()

    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(1, 1, 1, projection='3d')

    X = np.linspace(0, X_CELL_SIZE-1, X_CELL_SIZE)
    Y = np.linspace(0, Y_CELL_SIZE-1, Y_CELL_SIZE)
    X, Y = np.meshgrid(X, Y)

    world_map_mock = np.array(wm.world_map)

    # Контурный график с проекциями на оси
    ax.plot_surface(X, Y, world_map_mock, rstride=4, cstride=4, alpha=0.25)
    cset = ax.contour(X, Y, world_map_mock, zdir='z', offset=-1) #, cmap=cm.coolwarm
    cset = ax.contour(X, Y, world_map_mock, zdir='x', offset=-1) #, cmap=cm.coolwarm)
    cset = ax.contour(X, Y, world_map_mock, zdir='y', offset=-1) #, cmap=cm.coolwarm)

    ax.set_xlim3d(0, X_CELL_SIZE)
    ax.set_ylim3d(0, Y_CELL_SIZE)
    ax.set_zlim3d(0, 10)

    plt.show()
