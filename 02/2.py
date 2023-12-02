#!/usr/bin/env python3
from collections import defaultdict
from functools import partial, reduce
from itertools import accumulate, chain, cycle, takewhile
import math
from operator import mul
import os
import pprint
import re
from time import time

from humanize import intcomma

# Fix path so we can do a relative import: https://stackoverflow.com/a/27876800
if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

        # Relative imports here
        from util import *

INPUT_FILE='2-input.txt'
#INPUT_FILE='2a-example.txt'
#INPUT_FILE='2b-example.txt'

valid_games: list[int] = []
game_powers: list[int] = []
for line in get_file_contents(INPUT_FILE)[0]:
    is_valid = True 
    line_split = line.split(':')
    game_num = int(line_split[0].split(' ')[1])
    dice_sets = line_split[1].split(';')

    min_die_needed = {'red': 0, 'green': 0, 'blue': 0}

    for dice_set in dice_sets:
        dice_set_split = dice_set.split(',')
        for dice_info in dice_set_split:
            dice_info_split = dice_info.split(' ')
            # Note leading space so index starts at 1
            num_die = int(dice_info_split[1])
            die_color = dice_info_split[2] 
            match die_color:
                case 'red':
                    if num_die > 12:
                        is_valid = False
                case 'green':
                    if num_die > 13:
                        is_valid = False
                case 'blue':
                    if num_die > 14:
                        is_valid = False
                case _:
                    raise ValueError(f'{die_color} not recognized')

            if num_die > min_die_needed[die_color]:
                min_die_needed[die_color] = num_die

    if is_valid:
        valid_games.append(game_num)

    game_powers.append(reduce(mul, min_die_needed.values()))

print('1: ', sum(valid_games))
print('2: ', sum(game_powers))
