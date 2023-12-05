#!/usr/bin/env python3
from collections import defaultdict
from collections.abc import Iterable
from functools import partial, reduce
from itertools import chain, cycle, takewhile
import math
from operator import mul
import os
import pprint
import re
from time import time
from typing import NamedTuple

from humanize import intcomma

# Fix path so we can do a relative import: https://stackoverflow.com/a/27876800
if __name__ == '__main__':
    if not __package__:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

        # Relative imports here
        from util import *

INPUT_FILE='5-input.txt'
# INPUT_FILE='5a-example.txt'

input = get_file_contents(INPUT_FILE)
seeds = [int(seed) for seed in input[0][0].split(': ')[1].split(' ')]


class Mapping(NamedTuple):
    dest: int # mapping to start pos
    src: int  # mapping from start pos
    size: int # range


def get_mapper(cur_input):
    input_split = [x.split(' ') for x in cur_input]
    return [[int(dest), int(src), int(size)] for dest, src, size in input_split]


def remap(mappings: Iterable[Mapping], id: int):
    for dest, src, len in mappings:
        if src <= id < src+len:
            return dest + id - src
    
    return id


seed_to_soil = get_mapper(input[1][1:])
soil_to_fertilizer = get_mapper(input[2][1:])
fertilizer_to_water = get_mapper(input[3][1:])
water_to_light = get_mapper(input[4][1:])
light_to_temperature = get_mapper(input[5][1:])
temperature_to_humidity = get_mapper(input[6][1:])
humidity_to_location = get_mapper(input[7][1:])

locations: list[int] = []
for seed in seeds:
    soil = remap(seed_to_soil, seed)
    fertilizer = remap(soil_to_fertilizer, soil)
    water = remap(fertilizer_to_water, fertilizer)
    light = remap(water_to_light, water)
    temperature = remap(light_to_temperature, light)
    humidity = remap(temperature_to_humidity, temperature)
    locations.append(remap(humidity_to_location, humidity))

print('1: ', min(locations))
