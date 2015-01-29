__author__ = 'Siarshai'

colors = ['white', 'black', 'red', 'green', 'blue']
colors_short = ['W', 'B', 'R', 'G', 'U']
plants_basic_resources = ['hv', 'K', 'P', 'N', 'h2o']
plants_basic_resources_min_consumption_per_turn = [10, 0, 0, 0, 10]
plants_basic_resources_consumption_increase_per_gene = [1, 0.1, 0.1, 0.1, 1]

colors_to_short = dict(zip(colors, colors_short))
colors_to_basic_resources = dict(zip(colors, plants_basic_resources))
colors_to_consumption = dict(zip(colors,
        zip(plants_basic_resources_min_consumption_per_turn, plants_basic_resources_consumption_increase_per_gene)))

H2O_BASIC = 75
H2O_PER_H_REDUCE = 10

HV_BASIC = 10
HV_PER_H_GAIN = 5

# K, P, N - generated random specks, see speckgenerator
K_CENTERS_NUMBER_LOW = 4
K_AMPLITUDE_DENSITY_LOW = 4
K_AMPLITUDE_WIDENESS_LOW = 10
K_CENTERS_DICE = 0.5
K_DENSITY_DICE = 0.5
K_WIDENESS_DICE = 0.5
K_TRESHOLD = 30

def number_of_trues(bitarray):
    result = 0
    while bitarray:
        result += bitarray.pop()
    return result