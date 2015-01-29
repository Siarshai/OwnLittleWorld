__author__ = 'Siarshai'

import common_utils

class WorldMap:

    class Cell:
        def __init__(self, x, y, h=0, **kwargs): #h2o=0, hv=0, P=0, K=0, N=0
            self.x = x
            self.y = y
            self.h = h
            self.plants_list = []
            self.animals_list = []
            self.resources = {}
            for attribute in common_utils.plants_basic_resources:
                if attribute in kwargs.keys():
                    self.resources[attribute] = kwargs[attribute]

    def __init__(self, x_cells_size, y_cells_size):
        self.x_cells_size = x_cells_size
        self.y_cells_size = y_cells_size
        self.world_map = [[WorldMap.Cell(x, y) for x in range(self.x_cells_size)] for y in range(self.y_cells_size)]
        self.clean_maps = {}

    #Намного удобнее, чем на C++
    def __getitem__(self, tup):
        x, y = tup
        return self.world_map[x][y]

    def recompute_clean_map(self, attribute):
        if not WorldMap.validate_attribute(attribute):
            print("apply_map attribute error: ", attribute)
            return None
        self.clean_maps[attribute] = [[self.world_map[x][y].__dict__[attribute] for x in range(self.x_cells_size)] for y in range(self.y_cells_size)]
        return self.clean_maps[attribute]

    def apply_map(self, applied_map, attribute):
        if not WorldMap.validate_attribute(attribute):
            print("apply_map attribute error: ", attribute)
            return None
        for x in range(self.x_cells_size):
            for y in range(self.y_cells_size):
                self.world_map[x][y].__dict__[attribute] = applied_map[x][y]

    def recompute_map_h2o(self):
        """
        temp stub
        """
        for x in range(self.x_cells_size):
            for y in range(self.y_cells_size):
                self.world_map[x][y].h2o = common_utils.H2O_BASIC - common_utils.H2O_PER_H_REDUCE*self.world_map[x][y].h

    def recompute_map_hv(self):
        """
        temp stub
        """
        for x in range(self.x_cells_size):
            for y in range(self.y_cells_size):
                self.world_map[x][y].hv = common_utils.HV_BASIC + common_utils.HV_PER_H_GAIN*self.world_map[x][y].h

    def plants_turn(self):
        for x in range(self.x_cells_size):
            for y in range(self.y_cells_size):
                for plant in self.world_map[x][y].plants_list:
                    plant.consume(self.world_map[x][y])


    @staticmethod
    def validate_attribute(attribute):
        if attribute in common_utils.plants_basic_resources or attribute == "h":
            return True
        return False

