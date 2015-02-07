__author__ = 'Siarshai'

import matplotlib.colors
import common_utils
import random
# from plants.plant import Plant

class WorldMap:

    class Cell:
        def __init__(self, x, y, h=0, **kwargs):
            self.x = x
            self.y = y
            self.h = h
            self.plant = None
            self.resources_per_turn_provision = {}
            for attribute in common_utils.plants_basic_resources:
                self.resources_per_turn_provision[attribute] = kwargs[attribute] if attribute in kwargs.keys() else 0

    def __init__(self, x_cells_size, y_cells_size):
        self.x_cells_size = x_cells_size
        self.y_cells_size = y_cells_size
        self.world_map = [[WorldMap.Cell(x, y) for x in range(self.x_cells_size)] for y in range(self.y_cells_size)]
        self.clean_maps = {}
        self.turns_ticks = []
        self.ideality_full_ticks = []
        self.ideality_match_ticks = []
        self.turn = 0
        self.number_of_plants = 0

    def recompute_clean_map(self, attribute):
        if not WorldMap.validate_attribute(attribute):
            print("apply_map attribute error: ", attribute)
            return None
        else:
            if attribute == "plant":
                specks_x = []
                specks_y = []
                specks_colors = []
                for x in range(self.x_cells_size):
                    for y in range(self.y_cells_size):
                        if not self.world_map[x][y].plant is None:
                            red = common_utils.number_of_trues(self.world_map[x][y].plant.dna["red"])/32.0
                            green = common_utils.number_of_trues(self.world_map[x][y].plant.dna["green"])/32.0
                            blue = common_utils.number_of_trues(self.world_map[x][y].plant.dna["blue"])/32.0
                            specks_x.append(x)
                            specks_y.append(y)
                            specks_colors.append((red, green, blue))
                return specks_x, specks_y, specks_colors
            if attribute == "h":
                self.clean_maps[attribute] = [[self.world_map[x][y].h for x in range(self.x_cells_size)] for y in range(self.y_cells_size)]
            else:
                self.clean_maps[attribute] = [[self.world_map[x][y].resources_per_turn_provision[attribute] for x in range(self.x_cells_size)] for y in range(self.y_cells_size)]
        return self.clean_maps[attribute]

    def apply_map(self, applied_map, attribute):
        if not WorldMap.validate_attribute(attribute):
            print("apply_map attribute error: ", attribute)
            return None
        for x in range(self.x_cells_size):
            for y in range(self.y_cells_size):
                self.world_map[x][y].resources_per_turn_provision[attribute] = applied_map[x][y]

    def recompute_map_h2o(self):
        """
        temp stub
        """
        for x in range(self.x_cells_size):
            for y in range(self.y_cells_size):
                self.world_map[x][y].resources_per_turn_provision["h2o"] = common_utils.H2O_BASIC - common_utils.H2O_PER_H_REDUCE*self.world_map[x][y].h
                if self.world_map[x][y].resources_per_turn_provision["h2o"] < 0: self.world_map[x][y].resources_per_turn_provision["h2o"] = 0

    def recompute_map_hv(self):
        """
        temp stub
        """
        for x in range(self.x_cells_size):
            for y in range(self.y_cells_size):
                self.world_map[x][y].resources_per_turn_provision["hv"] = common_utils.HV_BASIC + common_utils.HV_PER_H_GAIN*self.world_map[x][y].h
                if self.world_map[x][y].resources_per_turn_provision["hv"] < 0: self.world_map[x][y].resources_per_turn_provision["hv"] = 0

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
                            spawn = plant.spawn_child()
                            plant.reproduction_discard_resources()
                            plant.ready_to_reproduce = False
                            target_x = x + random.randint(-2, 2)
                            target_y = y + random.randint(-2, 2)
                            target_x, target_y = self.adjust_point_to_map_borders(target_x, target_y)
                            if self.world_map[target_x][target_y].plant is None:
                                self.world_map[target_x][target_y].plant = spawn
                                # Note, that child plant will be actually born if target cell is empty,
                                # but resources are taken anyway
        if random.random() < common_utils.DISASTER_PROBABILITY:
            target_x = random.randint(0, self.x_cells_size-1)
            target_y = random.randint(0, self.y_cells_size-1)
            for x in range(-5, 5):
                for y in range(-5, 5):
                    if 0 <= target_x+x < self.x_cells_size and 0 <= target_y+y < self.y_cells_size:
                        plant = self.world_map[target_x+x][target_y+y].plant
                        if plant is not None:
                            if plant.get_damage((common_utils.DISASTER_AMPLITUDE*random.random())/(abs(x) + abs(y) + 1)):
                                self.world_map[target_x+x][target_y+y].plant = None
        if random.random() < common_utils.HUGE_DISASTER_PROBABILITY:
            target_x, target_y = random.randint(0, self.x_cells_size-1), random.randint(0, self.y_cells_size-1)
            for x in range(-5, 5):
                for y in range(-5, 5):
                    if 0 <= target_x+x < self.x_cells_size and 0 <= target_y+y < self.y_cells_size:
                        plant = self.world_map[target_x+x][target_y+y].plant
                        if plant is not None:
                            if plant.get_damage((common_utils.HUGE_DISASTER_AMPLITUDE_LOW + common_utils.HUGE_DISASTER_AMPLITUDE_DICE*random.random())/(abs(x) + abs(y) + 1)):
                                self.world_map[target_x+x][target_y+y].plant = None
        self.check_for_ideal() #move to main cycle
        self.turn += 1

    def check_for_ideal(self):
        self.number_of_plants = 0
        ideality_full = 0
        ideality_match = 0
        for x in range(self.x_cells_size):
            for y in range(self.y_cells_size):
                if self.world_map[x][y].plant is not None:
                    self.number_of_plants += 1
                    ideality_full += self.world_map[x][y].plant.ideality_full
                    ideality_match += self.world_map[x][y].plant.ideality_match
        if self.number_of_plants == 0:
            ideality_full = ideality_match = 0
        else:
            ideality_full /= self.number_of_plants
            ideality_match /= self.number_of_plants
        self.ideality_full_ticks.append(ideality_full)
        self.ideality_match_ticks.append(ideality_match)
        self.turns_ticks.append(self.turn)

    def gather_stats(self, attribute_set):
        reply_dict = {}
        for attribute in attribute_set:
            reply_dict[attribute] = {}
        for x in range(self.x_cells_size):
            for y in range(self.y_cells_size):
                if self.world_map[x][y].plant is not None:
                    for attribute in attribute_set:
                        if self.world_map[x][y].plant.__getattribute__(attribute) in reply_dict[attribute].keys():
                            reply_dict[attribute][self.world_map[x][y].plant.__getattribute__(attribute)] += 1
                        else:
                            reply_dict[attribute][self.world_map[x][y].plant.__getattribute__(attribute)] = 1
        return reply_dict

    @staticmethod
    def validate_attribute(attribute):
        if attribute in common_utils.plants_basic_resources or attribute == "h" or attribute == "plant":
            return True
        return False
