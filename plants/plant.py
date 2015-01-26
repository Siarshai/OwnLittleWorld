import random
from bitarray import *
from bitarray import bitarray
from bitstring import BitArray

class Plant:
    def __init__(self, dna={}):
        #Copying dna
        self.dna = {}
        for key in PlantDNALibrary.basic.keys():
            self.dna[key] = dna[key] if key in dna else random.randint()
        #Decoding dna

        pass


class PlantDNALibrary:
    #white is for reproduction
    #black is for parasitism
    #red is for bushiness
    #green is for health and endurance
    #blue is for longevity
    basic =   {'dna_white': BitArray(random.randint()),
               'dna_black': BitArray(random.randint()),
               'dna_red':   BitArray(random.randint()),
               'dna_green': BitArray(random.randint()),
               'dna_blue':  BitArray(random.randint())}



    @staticmethod
    def decode_basic_white(dna_white):
        """
        Decodes white dna of plant and returns its number of seeds and reproduction time
        :param dna_white: int representing 32 white genes
        :return: [number_of_seeds, reproduction_time]
        """
        mask = dna_white&PlantDNALibrary.basic["white"]