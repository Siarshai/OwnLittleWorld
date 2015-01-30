from mpl_toolkits.mplot3d.axes3d import Axes3D
import numpy as np
import matplotlib.colors as cm
import matplotlib.pyplot as plt
from worldmap.heightgenerator import *
from worldmap.speckgenerator import *
import pylab
import scipy
import common_utils
import plants.plant as pp

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

    sg_K = SpeckGenerator(x_cells_size=X_CELL_SIZE, y_cells_size=Y_CELL_SIZE,
                          centers_number_low=common_utils.MINERALS_CENTERS_NUMBER_LOW,
                          amplitude_density_low=common_utils.MINERALS_AMPLITUDE_DENSITY_LOW,
                          amplitude_wideness_low=common_utils.MINERALS_AMPLITUDE_WIDENESS_LOW,
                          centers_dice=common_utils.MINERALS_CENTERS_DICE,
                          amplitude_density_dice=common_utils.MINERALS_DENSITY_DICE,
                          amplitude_wideness_dice=common_utils.MINERALS_WIDENESS_DICE,
                          threshold=common_utils.MINERALS_TRESHOLD)

    sg_P = SpeckGenerator(x_cells_size=X_CELL_SIZE, y_cells_size=Y_CELL_SIZE,
                      centers_number_low=common_utils.MINERALS_CENTERS_NUMBER_LOW,
                      amplitude_density_low=common_utils.MINERALS_AMPLITUDE_DENSITY_LOW,
                      amplitude_wideness_low=common_utils.MINERALS_AMPLITUDE_WIDENESS_LOW,
                      centers_dice=common_utils.MINERALS_CENTERS_DICE,
                      amplitude_density_dice=common_utils.MINERALS_DENSITY_DICE,
                      amplitude_wideness_dice=common_utils.MINERALS_WIDENESS_DICE,
                      threshold=common_utils.MINERALS_TRESHOLD)

    sg_N = SpeckGenerator(x_cells_size=X_CELL_SIZE, y_cells_size=Y_CELL_SIZE,
                      centers_number_low=common_utils.MINERALS_CENTERS_NUMBER_LOW,
                      amplitude_density_low=common_utils.MINERALS_AMPLITUDE_DENSITY_LOW,
                      amplitude_wideness_low=common_utils.MINERALS_AMPLITUDE_WIDENESS_LOW,
                      centers_dice=common_utils.MINERALS_CENTERS_DICE,
                      amplitude_density_dice=common_utils.MINERALS_DENSITY_DICE,
                      amplitude_wideness_dice=common_utils.MINERALS_WIDENESS_DICE,
                      threshold=common_utils.MINERALS_TRESHOLD)

    wm = hg.generate_map()
    speck_map_minerals = sg_K.remap(None, X_CELL_SIZE, Y_CELL_SIZE)
    speck_map_P = sg_P.remap(None, X_CELL_SIZE, Y_CELL_SIZE)
    speck_map_N = sg_N.remap(None, X_CELL_SIZE, Y_CELL_SIZE)

    wm.apply_map(speck_map_minerals, "minerals")
    wm.recompute_map_h2o()
    wm.recompute_map_hv()

    X = np.linspace(0, X_CELL_SIZE, X_CELL_SIZE)
    Y = np.linspace(0, Y_CELL_SIZE, Y_CELL_SIZE)
    X, Y = np.meshgrid(X, Y)

    world_map_mock = np.array(wm.recompute_clean_map('h'))
    speck_map_minerals_mock = np.array(speck_map_minerals)

    fig = plt.figure(figsize=(20, 5))

    ax_main_h = fig.add_subplot(1, 3, 1, projection='3d')

    # Контурный график с проекциями на оси
    ax_main_h.plot_surface(X, Y, world_map_mock, rstride=4, cstride=4, alpha=0.25)
    cset = ax_main_h.contour(X, Y, world_map_mock, zdir='z', offset=-1, cmap=plt.get_cmap("coolwarm"))
    cset = ax_main_h.contour(X, Y, world_map_mock, zdir='x', offset=-1, cmap=plt.get_cmap("coolwarm"))
    cset = ax_main_h.contour(X, Y, world_map_mock, zdir='y', offset=-1, cmap=plt.get_cmap("coolwarm"))

    ax_main_h.set_xlim3d(0, X_CELL_SIZE)
    ax_main_h.set_ylim3d(0, Y_CELL_SIZE)
    ax_main_h.set_zlim3d(0, 10)

    ax_aux_h = fig.add_subplot(1, 3, 2)
    p = ax_aux_h.pcolor(X/X_CELL_SIZE, Y/Y_CELL_SIZE, world_map_mock, cmap=plt.get_cmap("terrain"),
                  vmin=abs(world_map_mock).min(),
                  vmax=abs(world_map_mock).max())
    cb = fig.colorbar(p, ax=ax_aux_h)


    ax_minerals = fig.add_subplot(1, 3, 3)
    p = ax_minerals.pcolor(X/X_CELL_SIZE, Y/Y_CELL_SIZE, speck_map_minerals_mock, cmap=plt.get_cmap("gnuplot2"),
                  vmin=abs(speck_map_minerals_mock).min(),
                  vmax=abs(speck_map_minerals_mock).max())
    cb = fig.colorbar(p, ax=ax_minerals)

    plt.show()


    wm[0, 0].plants_list.append(pp.Plant())
    wm[10, 10].plants_list.append(pp.Plant())
    wm[20, 20].plants_list.append(pp.Plant())
    wm[30, 30].plants_list.append(pp.Plant())
    wm[40, 40].plants_list.append(pp.Plant())
    wm[50, 50].plants_list.append(pp.Plant())
    wm[60, 60].plants_list.append(pp.Plant())

    fig = plt.figure(figsize=(8, 7))
    ax_plants = fig.add_subplot(1, 1, 1)
    plant_map_mock = np.array(wm.recompute_clean_map('plant'))
    p = ax_plants.pcolor(X/X_CELL_SIZE, Y/Y_CELL_SIZE, plant_map_mock, cmap=plt.get_cmap("BuGn"),
                  vmin=abs(plant_map_mock).min(),
                  vmax=abs(plant_map_mock).max())
    cb = fig.colorbar(p, ax=ax_plants)
    plt.show()

    for i in range(10):

        for i in range(20):
            wm.plants_turn()

        fig = plt.figure(figsize=(8, 7))
        ax_plants = fig.add_subplot(1, 1, 1)
        plant_map_mock = np.array(wm.recompute_clean_map('plant'))
        p = ax_plants.pcolor(X/X_CELL_SIZE, Y/Y_CELL_SIZE, plant_map_mock, cmap=plt.get_cmap("BuGn"),
                      vmin=abs(plant_map_mock).min(),
                      vmax=abs(plant_map_mock).max())
        cb = fig.colorbar(p, ax=ax_plants)
        plt.show()
