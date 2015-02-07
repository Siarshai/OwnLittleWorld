import random
from bitarray import bitarray

__author__ = 'Siarshai'

colors = ['red', 'green', 'blue']
colors_short = ['R', 'G', 'U']
plants_basic_resources = ['hv', 'minerals', 'h2o']
plants_basic_resources_min_consumption_per_turn = [0, 0, 0]
plants_basic_resources_consumption_increase_per_gene = [0.1, 0.05, 0.1]

colors_to_short = dict(zip(colors, colors_short))
colors_to_basic_resources = dict(zip(colors, plants_basic_resources))
colors_to_consumption = dict(zip(colors,
        zip(plants_basic_resources_min_consumption_per_turn, plants_basic_resources_consumption_increase_per_gene)))

# One may override default values by calling confugurer.configure_from_file

REPRODUCTION_DIVISOR = 5
REPRODUCTION_BIT_CHANGE_CHANCE = 1.0/32.0

H2O_BASIC = 7
H2O_PER_H_REDUCE = 1

HV_BASIC = 1
HV_PER_H_GAIN = 1

# See speckgenerator
MINERALS_CENTERS_NUMBER_LOW = 6
MINERALS_AMPLITUDE_DENSITY_LOW = 6
MINERALS_AMPLITUDE_WIDENESS_LOW = 15
MINERALS_CENTERS_DICE = 0.25
MINERALS_DENSITY_DICE = 0.5
MINERALS_WIDENESS_DICE = 0.5
MINERALS_THRESHOLD = 30

DISASTER_PROBABILITY = 0.5
DISASTER_AMPLITUDE = 30

HUGE_DISASTER_PROBABILITY = 0.05
HUGE_DISASTER_AMPLITUDE_LOW = 40
HUGE_DISASTER_AMPLITUDE_DICE = 40


def number_of_trues(bitarray):
    result = 0
    for bit in bitarray:
        result += bit
    return result


def get_random_sequence(number=32):
    return list([[False, True][random.randint(0, 1)] for j in range(number)])


def get_all_trues_in_four(bitarray, number):
    result = 0
    for bit in bitarray[4*number: 4*(number+1)]:
        result += bit
    return result == 4


def and_sequence(seq1, seq2):
    result = [tup[0] and tup[1] for tup in zip(seq1, seq2)]
    return result
