from mpl_toolkits.mplot3d.axes3d import Axes3D
import numpy as np
import matplotlib.colors as cm
import matplotlib.pyplot as plt
from mapgenerator.heightgenerator import *
from mapgenerator.speckgenerator import *
import pylab
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

    sg = SpeckGenerator(x_cells_size=X_CELL_SIZE, y_cells_size=Y_CELL_SIZE, centers_number_low=6,
                        amplitude_density_low=5, amplitude_wideness_low=10,
                 centers_dice=0.5, amplitude_density_dice=0.5, amplitude_wideness_dice=0.5, threshold=30)

    wm = hg.generate_map()
    speck_map = sg.remap(None, X_CELL_SIZE, Y_CELL_SIZE)

    X = np.linspace(0, X_CELL_SIZE, X_CELL_SIZE)
    Y = np.linspace(0, Y_CELL_SIZE, Y_CELL_SIZE)
    X, Y = np.meshgrid(X, Y)

    world_map_mock = np.array(wm.world_map)
    speck_map_mock = np.array(speck_map)

    fig = plt.figure(figsize=(18, 5))

    ax = fig.add_subplot(1, 3, 1, projection='3d')

    # Контурный график с проекциями на оси
    ax.plot_surface(X, Y, world_map_mock, rstride=4, cstride=4, alpha=0.25)
    cset = ax.contour(X, Y, world_map_mock, zdir='z', offset=-1) #, cmap=cm.coolwarm
    cset = ax.contour(X, Y, world_map_mock, zdir='x', offset=-1) #, cmap=cm.coolwarm)
    cset = ax.contour(X, Y, world_map_mock, zdir='y', offset=-1) #, cmap=cm.coolwarm)

    ax.set_xlim3d(0, X_CELL_SIZE)
    ax.set_ylim3d(0, Y_CELL_SIZE)
    ax.set_zlim3d(0, 10)

    ax1 = fig.add_subplot(1, 3, 2)
    p = ax1.pcolor(X/X_CELL_SIZE, Y/Y_CELL_SIZE, world_map_mock, cmap=plt.get_cmap("terrain"),
                  vmin=abs(world_map_mock).min(),
                  vmax=abs(world_map_mock).max())
    cb = fig.colorbar(p, ax=ax1)

    ax2 = fig.add_subplot(1, 3, 3)
    p = ax2.pcolor(X/X_CELL_SIZE, Y/Y_CELL_SIZE, speck_map_mock, cmap=plt.get_cmap("gnuplot2"),
                  vmin=abs(speck_map_mock).min(),
                  vmax=abs(speck_map_mock).max())
    cb = fig.colorbar(p, ax=ax2)



    plt.show()
