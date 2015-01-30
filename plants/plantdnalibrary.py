import common_utils
from common_utils import get_random_sequence

__author__ = 'Siarshai'


class PlantDNALibrary:

    REPRODUCTION_TURNS_BASIC = 40
    HEALTH_BASIC = 50
    TURNS_TO_LIVE_BASIC = 200

    REPRODUCTION_TURNS_REDUCE = 1
    HEALTH_GAIN = 10
    TURNS_TO_LIVE_GAIN = 10

    #dna red is for reproduction
    #dna green is for health
    #dna blue is for longevity
    decode_basic_dna_dict = dict()
    for color in common_utils.colors:
        decode_basic_dna_dict[color] = common_utils.get_random_sequence()

    @staticmethod
    def decode_basic_red(dna_red):
        """
        Decodes red dna of plant and returns its reproduction time (in turns)
        :param dna_red: int representing 32 white genes
        :return: reproduction_turns
        """
        result = dna_red&PlantDNALibrary.decode_basic_dna_dict["red"]
        reproduction_turns = PlantDNALibrary.REPRODUCTION_TURNS_BASIC
        while result:
            if result.pop():
                reproduction_turns -= PlantDNALibrary.REPRODUCTION_TURNS_REDUCE
        return reproduction_turns

    @staticmethod
    def decode_basic_green(dna_green):
        """
        Decodes green dna of plant and returns its health
        :param dna_green: int representing 32 white genes
        :return: health (hits)
        """
        health = PlantDNALibrary.HEALTH_BASIC
        for i in range(4):
            result = dna_green[i*8:(i+1)*8]&PlantDNALibrary.decode_basic_dna_dict["red"][i*8:(i+1)*8]
            if common_utils.number_of_trues(result) >= 6:
                health += PlantDNALibrary.HEALTH_GAIN
        return health

    @staticmethod
    def decode_basic_blue(dna_blue):
        """
        Decodes white dna of plant and returns its longevity
        :param dna_blue: int representing 32 white genes
        :return: [number_of_seeds, reproduction_time]
        """
        result = dna_blue&PlantDNALibrary.decode_basic_dna_dict["blue"]
        turns_to_live = PlantDNALibrary.TURNS_TO_LIVE_BASIC
        while result:
            if result.pop():
                turns_to_live += PlantDNALibrary.TURNS_TO_LIVE_GAIN
        return turns_to_live


