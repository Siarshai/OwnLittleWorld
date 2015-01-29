import random
import common_utils

from plants.plantdnalibrary import PlantDNALibrary


class Plant:
    def __init__(self, dna={}):
        #Copying dna
        self.dna = {}
        for color in common_utils.colors:
            self.dna[color] = dna[color] if color in dna else PlantDNALibrary.get_random_sequence()
        #Decoding dna
        self.ttr = self.reproduction_turns = PlantDNALibrary.decode_basic_white(self.dna["dna_white"])
        self.parasitism_percent = PlantDNALibrary.decode_basic_black(self.dna["dna_black"])
        self.feed_radius = PlantDNALibrary.decode_basic_red(self.dna["dna_red"])
        self.health = PlantDNALibrary.decode_basic_green(self.dna["dna_green"])*(0.75 + random.random()/2)
        self.turns_to_live = PlantDNALibrary.decode_basic_blue(self.dna["dna_blue"])*(0.75 + random.random()/2)
        #Setting initial resources
        self.resources = {}
        self.resources_consumption = {}
        for color in common_utils.colors:
            self.resources[color] =  self.resources_consumption[color] = common_utils.colors_to_consumption[color][0] + common_utils.number_of_trues(self.dna[color])*common_utils.colors_to_consumption[color][1]


