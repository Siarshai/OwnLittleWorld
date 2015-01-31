__author__ = 'Siarshai'

import matplotlib.colors
import common_utils
import random
# from plants.plant import Plant

class WorldMap:

    class Cell:
        def __init__(self, x, y, h=0, **kwargs): #h2o=0, hv=0, minerals=0
            self.x = x
            self.y = y
            self.h = h
            self.plant = None
            self.animal = None
            self.resources = {}
            for attribute in common_utils.plants_basic_resources:
                self.resources[attribute] = kwargs[attribute] if attribute in kwargs.keys() else 0

    def __init__(self, x_cells_size, y_cells_size):
        self.x_cells_size = x_cells_size
        self.y_cells_size = y_cells_size
        self.world_map = [[WorldMap.Cell(x, y) for x in range(self.x_cells_size)] for y in range(self.y_cells_size)]
        self.clean_maps = {}

    #Намного удобнее, чем на C++
    #Правда, не работает =)
    def __getitem__(self, tup):
        x, y = tup
        return self.world_map[x][y]

    def recompute_clean_map(self, attribute):
        if not WorldMap.validate_attribute(attribute):
            if attribute == "plant":
                specks_x = []
                specks_y = []
                specks_colors = []
                for x in range(self.x_cells_size):
                    for y in range(self.y_cells_size):
                        if not self.world_map[x][y].plant is None:
                            red = common_utils.number_of_trues(self.world_map[x][y].plant.dna["red"])/32
                            green = common_utils.number_of_trues(self.world_map[x][y].plant.dna["green"])/32
                            blue = common_utils.number_of_trues(self.world_map[x][y].plant.dna["blue"])/32
                            specks_x.append(x)
                            specks_y.append(y)
                            specks_colors.append((red, green, blue))
                return specks_x, specks_y, specks_colors
            else:
                print("apply_map attribute error: ", attribute)
                return None
        else:
            if attribute == "h":
                self.clean_maps[attribute] = [[self.world_map[x][y].h for x in range(self.x_cells_size)] for y in range(self.y_cells_size)]
            else:
                self.clean_maps[attribute] = [[self.world_map[x][y].resources[attribute] for x in range(self.x_cells_size)] for y in range(self.y_cells_size)]
        return self.clean_maps[attribute]

    def apply_map(self, applied_map, attribute):
        if not WorldMap.validate_attribute(attribute):
            print("apply_map attribute error: ", attribute)
            return None
        for x in range(self.x_cells_size):
            for y in range(self.y_cells_size):
                self.world_map[x][y].resources[attribute] = applied_map[x][y]

    def recompute_map_h2o(self):
        """
        temp stub
        """
        for x in range(self.x_cells_size):
            for y in range(self.y_cells_size):
                self.world_map[x][y].resources["h2o"] = common_utils.H2O_BASIC - common_utils.H2O_PER_H_REDUCE*self.world_map[x][y].h

    def recompute_map_hv(self):
        """
        temp stub
        """
        for x in range(self.x_cells_size):
            for y in range(self.y_cells_size):
                self.world_map[x][y].resources["hv"] = common_utils.HV_BASIC + common_utils.HV_PER_H_GAIN*self.world_map[x][y].h

    def adjust_point_to_map_borders(self, x, y):
        if x < 0:
            x = 0
        else:
            if x >= self.x_cells_size:
                x = self.x_cells_size - 1
        if y < 0:
            y = 0
        else:
            if y >= self.y_cells_size:
                y = self.y_cells_size - 1
        return x, y

    def plants_turn(self):
        for x in range(self.x_cells_size):
            for y in range(self.y_cells_size):
                plant = self.world_map[x][y].plant
                if plant is not None:
                    if not plant.process_resources(self.world_map[x][y]):
                        self.world_map[x][y].plant = None
                    else:
                        if plant.ready_to_reproduce:
                            plant.reproduction_discard_resources()
                            plant.ready_to_reproduce = False
                            target_x = x + random.randint(-2, 2)
                            target_y = y + random.randint(-2, 2)
                            target_x, target_y = self.adjust_point_to_map_borders(target_x, target_y)
                            spawn = plant.spawn_child()
                            if self.world_map[target_x][target_y].plant is None:
                                self.world_map[target_x][target_y].plant = spawn
                                # Note, that child plant will be actually born if target cell is empty,
                                # but resources are taken anyway

    @staticmethod
    def validate_attribute(attribute):
        if attribute in common_utils.plants_basic_resources or attribute == "h":
            return True
        return False
