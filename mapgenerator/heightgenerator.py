__author__ = 'Siarshai'

import random
import math
import numpy as np
import numpy.linalg as lin
from scipy import interpolate


class WorldMap:
    # Пока что только высота
    def __init__(self, x_cells_size, y_cells_size):
        self.x_cells_size = x_cells_size
        self.y_cells_size = y_cells_size
        self.world_map = [[0]*self.x_cells_size for i in range(self.y_cells_size)]

# Just for fun
def hill_map_height_regular_constituent_closure(x_cells_size, y_cells_size, amplitude, alpha=None):
    x_midpoint = x_cells_size/2
    y_midpoint = y_cells_size/2
    if alpha is None:
        alpha = x_cells_size/4

    def hill_map_height_regular_constituent_function(x, y):
        return -amplitude*math.hypot((x_midpoint-x), (y_midpoint-y))/alpha

    return hill_map_height_regular_constituent_function


class HeightGenerator:

    def __init__(self, x_cells_size, y_cells_size, base_points_divisor,
                 amplitude=5, persistence=0.5, generators_number=3,
                 regular_constituent_function_closure=None):
        self.x_cells_size = x_cells_size
        self.y_cells_size = y_cells_size
        if regular_constituent_function_closure is None:
            self.regular_constituent_function = lambda x, y: 0
        else:
            self.regular_constituent_function = regular_constituent_function_closure(x_cells_size, y_cells_size,
                                                                                     amplitude, alpha=x_cells_size)
        self.amplitude = amplitude
        self.generators = []
        for i in range(generators_number):
            self.generators.append(PerlinGenerator2D(0, 0, x_cells_size, y_cells_size,
                                                     x_cells_size//base_points_divisor*(2**i),
                                                     y_cells_size//base_points_divisor*(2**i),
                                                     amplitude*(persistence**i)))

    def generate_map(self):
        # self.regular_base_points_mask = [[0]*self.x_dots_resolution for i in range(self.y_dots_resolution)]
        wm = WorldMap(self.x_cells_size, self.y_cells_size)
        for x in range(self.x_cells_size):
            for y in range(self.y_cells_size):
                for k in range(len(self.generators)):
                    wm.world_map[x][y] += self.generators[k].interpolate_linear(x, y)
                #print(self.regular_constituent_function(x, y))
                wm.world_map[x][y] += self.regular_constituent_function(x, y)
        return wm


class PerlinGenerator2D:

    def __init__(self, x_min, y_min, x_max, y_max, x_base_cells, y_base_cells, amplitude,
                 type="linear", seed=None):
        if x_base_cells != int(x_base_cells) or y_base_cells != int(y_base_cells)\
                or x_base_cells <= 0 or y_base_cells <= 0:
            raise AttributeError("Number of base dots must be positive and integer")
        if x_min > x_max or y_min > y_max:
            raise AttributeError("Incorrect mapgenerator size")
        if seed is not None:
            random.seed(seed)
        self.set_cells_num(x_base_cells, y_base_cells)
        self.set_square(x_min, y_min, x_max, y_max)
        self.set_amplitude(amplitude)
        self.generate_base_points()

    def generate_base_points(self):
        # На самом деле нам нужно на одну опорную точку больше чем клеток
        self.base_points = [[0]*self.x_dots_resolution for i in range(self.y_dots_resolution)]
        for x in range(self.x_dots_resolution):
            for y in range(self.y_dots_resolution):
                self.base_points[x][y] += random.random()*self.amplitude

    def set_amplitude(self, amplitude):
        self.amplitude = amplitude

    def set_square(self, x_min, y_min, x_max, y_max):
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max
        self.x_step = (x_max - x_min)/(self.x_dots_resolution-1)
        self.y_step = (y_max - y_min)/(self.y_dots_resolution-1)

    def set_cells_num(self, x_base_cells, y_base_cells):
        self.x_dots_resolution = x_base_cells + 1
        self.y_dots_resolution = y_base_cells + 1

    def interpolate_linear(self, x, y):
        if x < self.x_min or x > self.x_max:
            raise AttributeError("x is out the preset range")
        if y < self.y_min or y > self.y_max:
            raise AttributeError("y is out the preset range")
        x_num = x/self.x_step
        y_num = y/self.y_step
        if x_num == int(x_num):
            x_n_med = int(x_num)
            if y_num == int(y_num):
                # Обе точки - опорные, не надо ничего интерполировать
                return self.base_points[x_n_med][int(y_num)]
            # x - опорная, y лежит между опорными
            # получаем опорные точки между которыми лежит y, интерполируем по y
            y_n_low = int(y_num)
            y_n_high = y_n_low + 1
            while y_n_high > self.y_dots_resolution:
                y_n_low -= 1
                y_n_high -= 1
            return PerlinGenerator2D.interpolate_linear_clean(y_n_low * self.y_step,
                                                               y_n_high * self.y_step,
                                                               self.base_points[x_n_med][y_n_low],
                                                               self.base_points[x_n_med][y_n_high],
                                                               y)
        else:
            x_n_low = int(x_num)
            x_n_high = x_n_low + 1
            while x_n_high > self.x_dots_resolution:
                x_n_low -= 1
                x_n_high -= 1
            if y_num == int(y_num):
                # y - опорная, x лежит между опорными
                # получаем опорные точки между которыми лежит x, интерполируем по x
                y_n_med = int(y_num)
                return PerlinGenerator2D.interpolate_linear_clean(x_n_low * self.x_step,
                                                   x_n_high * self.x_step,
                                                   self.base_points[x_n_low][y_n_med],
                                                   self.base_points[x_n_high][y_n_med],
                                                   x)
            # обе точки лежат между опорными значениями
            # интерполирем вспомогательные точки на сетке по оси ординат,
            # затем используем их, чтобы получить значение в требуемой точке
            y_n_low = int(y_num)
            y_n_high = y_n_low + 1
            while y_n_high > self.y_dots_resolution:
                y_n_low -= 1
                y_n_high -= 1
            f_prop_low = PerlinGenerator2D.interpolate_linear_clean(y_n_low * self.y_step,
                                                               y_n_high * self.y_step,
                                                               self.base_points[x_n_low][y_n_low],
                                                               self.base_points[x_n_low][y_n_high],
                                                               y)
            f_prop_high = PerlinGenerator2D.interpolate_linear_clean(y_n_low * self.y_step,
                                                   y_n_high * self.y_step,
                                                   self.base_points[x_n_high][y_n_low],
                                                   self.base_points[x_n_high][y_n_high],
                                                   y)
            return PerlinGenerator2D.interpolate_linear_clean(x_n_low * self.x_step,
                                                   x_n_high * self.x_step,
                                                   f_prop_low,
                                                   f_prop_high,
                                                   x)

    @staticmethod
    def interpolate_linear_clean(z1, z2, f1, f2, z):
        # решаем систему линейных уравнений, чтобы восстановаить коэффициенты
        # интерполирующей параболы и возвращаем значение в требуемой точке
        # print(z1, z2, f1, f2, z)
        row1 = [z1, 1]
        row2 = [z2, 1]
        fcolumn = [f1, f2]
        (k, b) = lin.solve([row1, row2], fcolumn) #necessary?
        return k*z + b

    def interpolate_bicube(self):
        # Писать бикубическую интерполяцию самостоятельно слишком морочно,
        # воспользуюсь готовой реализацией
        # TODO: поправить код, писалось ночью после кальяна
        self.grid_x, self.grid_y = np.mgrid[self.x_min:self.x_max:self.x_dots_resolution,
                                            self.y_min:self.y_max:self.y_dots_resolution]
        self.points = []
        self.values = []
        for i in range(self.x_dots_resolution):
            for j in range(self.y_dots_resolution):
                self.points.append((i*self.x_step, j*self.y_step))
                self.values.append(self.base_points[i][j])
        return interpolate.griddata(self.points, self.values, (self.grid_x, self.grid_y), method='cubic')
