import random
import common_utils
from bitarray import *


class PlantDNALibrary:

    @staticmethod
    def get_random_sequence(number=32):
        return bitarray([[False, True][random.randint(0, 1)] for j in range(number)])

    @staticmethod
    def decode_basic_white(dna_white):
        """
        Decodes white dna of plant and returns its number of seeds and reproduction time
        :param dna_white: int representing 32 white genes
        :return: [number_of_seeds, reproduction_time]
        """
        result = dna_white&PlantDNALibrary.basic["dna_white"]
        reproduction_turns = 40 #100 turns, TODO: wrap in const
        while result:
            if result.pop():
                reproduction_turns -= 1
        return reproduction_turns

    #dna_white is for reproduction
    #dna_black is for parasitism
    #dna_red is for bushiness
    #dna_green is for health and endurance
    #dna_blue is for longevity
    basic = dict()
    for color in common_utils.colors:
        basic["dna_" + color] = get_random_sequence.__func__()


class Plant:
    def __init__(self, dna={}):
        #Copying dna
        self.dna = {}
        for key in PlantDNALibrary.basic.keys():
            self.dna[key] = dna[key] if key in dna else PlantDNALibrary.get_random_sequence()
        #Decoding dna
        self.reproduction_turns = PlantDNALibrary.decode_basic_white(self.dna["dna_white"])

