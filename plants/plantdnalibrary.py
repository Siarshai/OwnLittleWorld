import random
from bitarray import bitarray
import common_utils

__author__ = 'Siarshai'


class PlantDNALibrary:

    HEALTH_BASIC = 100
    REPRODUCTION_TURNS_BASIC = 40
    TURNS_TO_LIVE_BASIC = 200

    REPRODUCTION_TURNS_REDUCE = 1
    HEALTH_GAIN = 10
    PARASITISM_GAIN = 0.02
    TURNS_TO_LIVE_GAIN = 10

    @staticmethod
    def get_random_sequence(number=32):
        return bitarray([[False, True][random.randint(0, 1)] for j in range(number)])

    #dna_white is for reproduction
    #dna_black is for parasitism
    #dna_red is for bushiness
    #dna_green is for health and endurance
    #dna_blue is for longevity
    basic = dict()
    for color in common_utils.colors:
        basic[color] = get_random_sequence.__func__()

    @staticmethod
    def decode_basic_white(dna_white):
        """
        Decodes white dna of plant and returns its reproduction time (in turns)
        :param dna_white: int representing 32 white genes
        :return: reproduction_turns
        """
        result = dna_white&PlantDNALibrary.basic["white"]
        reproduction_turns = PlantDNALibrary.REPRODUCTION_TURNS_BASIC
        while result:
            if result.pop():
                reproduction_turns -= PlantDNALibrary.REPRODUCTION_TURNS_REDUCE
        return reproduction_turns

    @staticmethod
    def decode_basic_black(dna_black):
        """
        Decodes black dna of plant and returns its parasitism inclination
        :param dna_black: int representing 32 white genes
        :return: stealing percent of nearby other plants
        """
        result = dna_black&PlantDNALibrary.basic["black"]
        parasitism_inclination = 0
        parasitism_percent = 0
        while result:
            if result.pop():
                parasitism_inclination += 1
                if parasitism_inclination > 16:
                    parasitism_percent += PlantDNALibrary.PARASITISM_GAIN
        return parasitism_percent

    @staticmethod
    def decode_basic_red(dna_red):
        """
        Decodes red dna of plant and returns its feed radius
        :param dna_red: int representing 32 white genes
        :return: feed_radius
        """
        feed_radius = 0
        for i in range(4):
            result = dna_red[i*8:(i+1)*8]&PlantDNALibrary.basic["red"][i*8:(i+1)*8]
            number_of_concurs = 0
            while result:
                if result.pop():
                    number_of_concurs += 1
            if number_of_concurs >= 6:
                feed_radius += 1
        return feed_radius

    @staticmethod
    def decode_basic_green(dna_green):
        """
        Decodes white dna of plant and returns its health
        :param dna_green: int representing 32 white genes
        :return: health (hits)
        """
        result = dna_green&PlantDNALibrary.basic["green"]
        health = PlantDNALibrary.HEALTH_BASIC
        while result:
            if result.pop():
                health += PlantDNALibrary.HEALTH_GAIN
        return health

    @staticmethod
    def decode_basic_blue(dna_blue):
        """
        Decodes white dna of plant and returns its longevity
        :param dna_blue: int representing 32 white genes
        :return: [number_of_seeds, reproduction_time]
        """
        result = dna_blue&PlantDNALibrary.basic["blue"]
        turns_to_live = PlantDNALibrary.TURNS_TO_LIVE_BASIC
        while result:
            if result.pop():
                turns_to_live += PlantDNALibrary.TURNS_TO_LIVE_GAIN
        return turns_to_live