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
import configurer

X_CELL_SIZE = 64
Y_CELL_SIZE = 64
CELL_DIVISOR = Y_CELL_SIZE/2
AMPLITUDE = 5
PERSISTENCE = 0.55
GENERATORS_NUMBER = 5

if __name__ == "__main__":

    configurer.configure_from_file("config.txt")

    hg = HeightGenerator(x_cells_size=X_CELL_SIZE, y_cells_size=Y_CELL_SIZE, base_points_divisor=CELL_DIVISOR,
                         amplitude=AMPLITUDE, persistence=PERSISTENCE, generators_number=GENERATORS_NUMBER,
                         regular_constituent_function_closure=hill_map_height_regular_constituent_closure)

    minerals_speck_generator = SpeckGenerator(x_cells_size=X_CELL_SIZE, y_cells_size=Y_CELL_SIZE,
                          centers_number_low=common_utils.MINERALS_CENTERS_NUMBER_LOW,
                          amplitude_density_low=common_utils.MINERALS_AMPLITUDE_DENSITY_LOW,
                          amplitude_wideness_low=common_utils.MINERALS_AMPLITUDE_WIDENESS_LOW,
                          centers_dice=common_utils.MINERALS_CENTERS_DICE,
                          amplitude_density_dice=common_utils.MINERALS_DENSITY_DICE,
                          amplitude_wideness_dice=common_utils.MINERALS_WIDENESS_DICE,
                          threshold=common_utils.MINERALS_THRESHOLD)

    wm = hg.generate_map()

    speck_map_minerals = minerals_speck_generator.remap(None, X_CELL_SIZE, Y_CELL_SIZE)
    wm.apply_map(speck_map_minerals, "minerals")

    wm.recompute_map_h2o()
    wm.recompute_map_hv()

    X = np.linspace(0, X_CELL_SIZE, X_CELL_SIZE)
    Y = np.linspace(0, Y_CELL_SIZE, Y_CELL_SIZE)
    X, Y = np.meshgrid(X, Y)

    world_map_mock = np.array(wm.recompute_clean_map('h'))
    speck_map_minerals_mock = np.array(speck_map_minerals)

    for x in range(20):
        for y in range(20):
            wm.world_map[3*x][3*y].plant = pp.Plant()

    specks_x, specks_y, specks_colors = wm.recompute_clean_map('plant')
    specks_x, specks_y, specks_colors = np.array(specks_x), np.array(specks_y), np.array(specks_colors)

    fig = plt.figure(figsize=(19, 5))

    ax_aux_h = fig.add_subplot(1, 3, 1)
    p = ax_aux_h.pcolor(X/X_CELL_SIZE, Y/Y_CELL_SIZE, world_map_mock, cmap=plt.get_cmap("terrain"),
                  vmin=abs(world_map_mock).min(),
                  vmax=abs(world_map_mock).max())
    cb = fig.colorbar(p, ax=ax_aux_h)


    ax_minerals = fig.add_subplot(1, 3, 2)
    p = ax_minerals.pcolor(X/X_CELL_SIZE, Y/Y_CELL_SIZE, speck_map_minerals_mock, cmap=plt.get_cmap("gnuplot2"),
                  vmin=abs(speck_map_minerals_mock).min(),
                  vmax=abs(speck_map_minerals_mock).max())
    cb = fig.colorbar(p, ax=ax_minerals)

    ax_plants = fig.add_subplot(1, 3, 3)
    ax_plants.scatter(specks_x, specks_y, 100, specks_colors)
    plt.xlim(0, X_CELL_SIZE)
    plt.ylim(0, Y_CELL_SIZE)
    plt.show()

    for i in range(100):

        for j in range(150000): #100*(2**i)
            wm.plants_turn()
            if wm.number_of_plants == 0:
                print("Everything died =(")
                exit(-1)

        ideality_full_ticks = np.array(wm.ideality_full_ticks)
        ideality_match_ticks = np.array(wm.ideality_match_ticks)
        turns_ticks = np.array(wm.turns_ticks)

        stats = wm.gather_stats(['ttl_max', 'ttr_max', 'health_max'])
        specks_x, specks_y, specks_colors = wm.recompute_clean_map('plant')

        fig = plt.figure(figsize=(20, 9))

        ax_aux_h = fig.add_subplot(3, 4, 1)
        p = ax_aux_h.pcolor(X/X_CELL_SIZE, Y/Y_CELL_SIZE, world_map_mock, cmap=plt.get_cmap("terrain"),
                      vmin=abs(world_map_mock).min(),
                      vmax=abs(world_map_mock).max())
        cb = fig.colorbar(p, ax=ax_aux_h)

        ax_minerals = fig.add_subplot(3, 4, 2)
        p = ax_minerals.pcolor(X/X_CELL_SIZE, Y/Y_CELL_SIZE, speck_map_minerals_mock, cmap=plt.get_cmap("gnuplot2"),
                      vmin=abs(speck_map_minerals_mock).min(),
                      vmax=abs(speck_map_minerals_mock).max())
        cb = fig.colorbar(p, ax=ax_minerals)

        ax_ideality = fig.add_subplot(3, 4, 5)
        ax_ideality.plot(turns_ticks, ideality_full_ticks, label='full')
        ax_ideality.plot(turns_ticks, ideality_match_ticks, label='match')
        ax_ideality.legend(loc='upper left')

        ax_generations = fig.add_subplot(3, 4, 6)
        ax_generations.bar(stats['ttl_max'].keys(), stats['ttl_max'].values(), label='ttl_max')
        ax_generations.legend(loc='upper right')

        ax_ttr = fig.add_subplot(3, 4, 9)
        ax_ttr.bar(stats['ttr_max'].keys(), stats['ttr_max'].values(), label='ttr_max')
        ax_ttr.legend(loc='upper right')

        ax_health = fig.add_subplot(3, 4, 10)
        ax_health.bar(stats['health_max'].keys(), stats['health_max'].values(), label='health_max')
        ax_health.legend(loc='upper right')

        ax_plants = fig.add_subplot(1, 2, 2)
        ax_plants.scatter(specks_x, specks_y, 100, specks_colors)
        plt.xlim(0, X_CELL_SIZE)
        plt.ylim(0, Y_CELL_SIZE)

        plt.show()
