import random
from plants.plantdnalibrary import PlantDNALibrary
from worldmap.map import *
import common_utils

class Plant:
    def __init__(self, dna=None):
        #Copying dna
        inner_dna = dict() if dna is None else dict(dna)
        self.dna = {}
        for color in common_utils.colors:
            self.dna[color] = inner_dna[color] if color in inner_dna else common_utils.get_random_sequence()
        #Decoding dna
        self.ttr = self.reproduction_turns = PlantDNALibrary.decode_basic_red(self.dna["red"])
        self.health = PlantDNALibrary.decode_basic_green(self.dna["green"])*(0.75 + random.random()/2)
        self.ttl = int(PlantDNALibrary.decode_basic_blue(self.dna["blue"])*(0.75 + random.random()/2))
        self.dead = False
        self.ready_to_reproduce = False
        #Setting initial resources
        self.resources = {}
        self.resources_consumption = {}
        for color in common_utils.colors:
            self.resources[common_utils.colors_to_basic_resources[color]] = self.resources_consumption[common_utils.colors_to_basic_resources[color]] = common_utils.colors_to_consumption[color][0] + common_utils.number_of_trues(self.dna[color])*common_utils.colors_to_consumption[color][1]

    def process_resources(self, cell):
        if not isinstance(cell, WorldMap.Cell):
            raise AttributeError(cell + " is not a cell")
        self.ttl -= 1
        if self.dead or self.ttl <= 0 or self.health <= 0:
            self.dead = True
            return False
        self.ready_to_reproduce = True
        for key in common_utils.plants_basic_resources:
            self.resources[key] += cell.resources[key] - self.resources_consumption[key]
            if self.resources[key] < 0:
                self.health += self.resources[key]
                self.resources[key] = 0
            else:
                if self.resources[key] <= common_utils.MULTIPLIER_TO_REPRODUCE*self.resources_consumption[key]:
                    self.ready_to_reproduce = False
        if self.health <= 0:
            self.dead = True
            return False
        return True

    def reproduction_discard_resources(self):
        pass
        for key in common_utils.plants_basic_resources:
            self.resources[key] /= common_utils.REPRODUCTION_PENALTY_DIVISOR

    def spawn_child(self):
        return Plant(self.dna)