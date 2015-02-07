import random
from plants.plantdnalibrary import PlantDNALibrary
from worldmap.map import *
from bitarray import bitarray
import common_utils
from copy import deepcopy
from functools import reduce

class Plant:
    def __init__(self, dna=None, generation=0):
        #Copying dna
        inner_dna = dict() if dna is None else dict(dna)
        self.dna = {}
        for color in common_utils.colors:
            if color in inner_dna:
                self.dna[color] = deepcopy(inner_dna[color]) #just in case
                for j in range(len(self.dna[color])):
                    if random.random() < common_utils.REPRODUCTION_BIT_CHANGE_CHANCE:
                        self.dna[color][j] ^= True
            else:
                self.dna[color] = common_utils.get_random_sequence()
        #Decoding dna
        self.ttr_max = self.ttr = PlantDNALibrary.decode_basic_red(self.dna["red"])
        self.health_max = self.health = PlantDNALibrary.decode_basic_green(self.dna["green"])
        self.ttl_max = self.ttl = PlantDNALibrary.decode_basic_blue(self.dna["blue"])
        #Some other helpful information
        self.generation = generation
        self.ideality_full = 0
        self.ideality_match = 0
        for color in common_utils.colors:
            self.ideality_full += reduce(lambda x, y: x+y, self.dna[color])/32.0/len(common_utils.colors)
            self.ideality_match += reduce(lambda x, y: x+y, [self.dna[color][i]^PlantDNALibrary.decode_basic_dna_dict[color][i] for i in range(32)])/32.0/len(common_utils.colors)
        self.dead = False
        self.ready_to_reproduce = False
        #Setting initial resources
        self.resources_stored = {}
        self.resources_consumption = {}
        for color in common_utils.colors:
            res = common_utils.colors_to_basic_resources[color]
            self.resources_consumption[res] = common_utils.colors_to_consumption[color][0] + common_utils.number_of_trues(self.dna[color])*common_utils.colors_to_consumption[color][1]
            self.resources_stored[res] = self.resources_consumption[res]

    def process_resources(self, cell, divisor=1):
        if not isinstance(cell, WorldMap.Cell):
            raise AttributeError(cell + " is not a cell")
        self.ttr -= 1
        self.ttl -= 1
        self.ready_to_reproduce = self.ttr <= 0
        for key in common_utils.plants_basic_resources:
            self.resources_stored[key] += cell.resources_per_turn_provision[key]/divisor - self.resources_consumption[key]
            if self.resources_stored[key] < 0:
                self.health += self.resources_stored[key]
                self.resources_stored[key] = 0
            if self.resources_stored[key] <= common_utils.REPRODUCTION_DIVISOR*self.resources_consumption[key]:
                self.ready_to_reproduce = False
        self.dead = self.dead or self.ttl <= 0 or self.health <= 0
        return not self.dead

    def get_damage(self, dmg):
        self.health -= dmg
        self.dead = self.health <= 0
        return self.dead

    def reproduction_discard_resources(self):
        for key in common_utils.plants_basic_resources:
            self.resources_stored[key] /= common_utils.REPRODUCTION_DIVISOR

    def spawn_child(self):
        return Plant(self.dna, self.generation+1)


