__author__ = 'Siarshai'

import random as rnd
import math


class SpeckGenerator:
    def __init__(self, x_cells_size, y_cells_size, centers_number_low, amplitude_density_low, amplitude_wideness_low,
                 centers_dice=0.5, amplitude_density_dice=0.5, amplitude_wideness_dice=0.5, threshold=30):
        self.generating_list = []
        self.centers_number = int((1 + centers_dice*rnd.random())*centers_number_low)
        self.threshold = threshold
        for i in range(self.centers_number):
            x = (x_cells_size+1)*rnd.random()
            y = (y_cells_size+1)*rnd.random()
            amplitude_density = (1 + amplitude_density_dice*rnd.random())*amplitude_density_low
            amplitude_wideness = (1 + amplitude_wideness_dice*rnd.random())*amplitude_wideness_low
            self.generating_list.append(SpeckGenerator.get_density_function(x, y, amplitude_density, amplitude_wideness))

    def remap(self, map=None, x_cells_size=64, y_cells_size=64):
        inner_map = map if map is not None else [[0]*x_cells_size for y in range(y_cells_size)]
        for function in self.generating_list:
            x_min = int( 0 if function.x_center - self.threshold < 0 else function.x_center - self.threshold )
            x_max = int( len(inner_map[0]) if function.x_center + self.threshold > len(inner_map[0]) else function.x_center + self.threshold )
            y_min = int( 0 if function.y_center - self.threshold < 0 else function.y_center - self.threshold )
            y_max = int( len(inner_map) if function.y_center + self.threshold > len(inner_map) else function.y_center + self.threshold )
            for x in range(x_min, x_max):
                for y in range(y_min, y_max):
                    inner_map[x][y] += function(x, y) if math.hypot(x-function.x_center, y-function.y_center) < self.threshold else 0
        return inner_map

    @staticmethod
    def get_density_function(x_center, y_center, amplitude_density, amplitude_wideness):
        # Using closure like a pro
        def get_density(x, y):
            return amplitude_density*amplitude_wideness/(amplitude_wideness + math.hypot(x-x_center, y-y_center)**2)
        get_density.x_center = x_center
        get_density.y_center = y_center
        return get_density