import random
from bitarray import bitarray

__author__ = 'Siarshai'

colors = ['red', 'green', 'blue'] #'white', 'black',
colors_short = ['R', 'G', 'U'] #'W', 'B',
plants_basic_resources = ['hv', 'minerals', 'h2o'] # 'K', 'P', 'N'
plants_basic_resources_min_consumption_per_turn = [1, 1, 1]
plants_basic_resources_consumption_increase_per_gene = [0.1, 0.1, 0.1]

colors_to_short = dict(zip(colors, colors_short))
colors_to_basic_resources = dict(zip(colors, plants_basic_resources))
colors_to_consumption = dict(zip(colors,
        zip(plants_basic_resources_min_consumption_per_turn, plants_basic_resources_consumption_increase_per_gene)))

MULTIPLIER_TO_REPRODUCE = 10

H2O_BASIC = 7.5
H2O_PER_H_REDUCE = 1

HV_BASIC = 1
HV_PER_H_GAIN = 1

# see speckgenerator
MINERALS_CENTERS_NUMBER_LOW = 6
MINERALS_AMPLITUDE_DENSITY_LOW = 4
MINERALS_AMPLITUDE_WIDENESS_LOW = 15
MINERALS_CENTERS_DICE = 0.25
MINERALS_DENSITY_DICE = 0.5
MINERALS_WIDENESS_DICE = 0.5
MINERALS_TRESHOLD = 40


def number_of_trues(bitarray):
    result = 0
    for bit in bitarray:
        result += bit
    return result


def get_random_sequence(number=32):
    return bitarray([[False, True][random.randint(0, 1)] for j in range(number)])