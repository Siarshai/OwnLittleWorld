import common_utils
from common_utils import get_random_sequence

__author__ = 'Siarshai'


class PlantDNALibrary:

    TTR_BASIC = 64
    HEALTH_BASIC = 5
    TURNS_TO_LIVE_BASIC = 20

    TTR_REDUCE = TTR_BASIC/32
    HEALTH_GAIN = 5
    TURNS_TO_LIVE_GAIN = 5

    HEALTH_GAIN_EXTRA_BONUS = 52
    TURNS_TO_LIVE_EXTRA_BONUS = 62

    #dna red is for reproduction
    #dna green is for health
    #dna blue is for longevity
    decode_basic_dna_dict = dict()
    for color in common_utils.colors:
        if color == "red":
            decode_basic_dna_dict[color] = [True]*32 # Every bit matters
        else:
            decode_basic_dna_dict[color] = common_utils.get_random_sequence() # Some bits are just junk

    @staticmethod
    def decode_basic_red(dna_red):
        """
        Decodes red dna of plant and returns its turns before plant can reproduce
        :param dna_red: int representing 32 white genes
        :return: turns to reproduce
        """
        ttr = PlantDNALibrary.TTR_BASIC - PlantDNALibrary.TTR_REDUCE*common_utils.number_of_trues(dna_red)
        return ttr

    @staticmethod
    def decode_basic_green(dna_green):
        """
        Decodes green dna of plant and returns its health
        :param dna_green: int representing 32 white genes
        :return: health
        """
        result = common_utils.and_sequence(dna_green, PlantDNALibrary.decode_basic_dna_dict["green"])
        health = PlantDNALibrary.HEALTH_BASIC + PlantDNALibrary.HEALTH_GAIN*common_utils.number_of_trues(result)
        for i in range(8):
            if common_utils.get_all_trues_in_four(dna_green, i):
                health += PlantDNALibrary.HEALTH_GAIN_EXTRA_BONUS
            else:
                break
        return health

    @staticmethod
    def decode_basic_blue(dna_blue):
        """
        Decodes white dna of plant and returns its longevity
        :param dna_blue: int representing 32 white genes
        :return: turns to live
        """
        result = common_utils.and_sequence(dna_blue, PlantDNALibrary.decode_basic_dna_dict["blue"])
        turns_to_live = PlantDNALibrary.TURNS_TO_LIVE_BASIC + PlantDNALibrary.TURNS_TO_LIVE_GAIN*common_utils.number_of_trues(result)
        for i in range(8):
            if common_utils.get_all_trues_in_four(dna_blue, i):
                turns_to_live += PlantDNALibrary.TURNS_TO_LIVE_EXTRA_BONUS
            else:
                break
        return turns_to_live


