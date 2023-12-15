#!/usr/bin/env python3
from collections import defaultdict
from enum import Enum
from functools import partial, reduce
from itertools import chain, cycle, takewhile
import math
from operator import mul, itemgetter
import os
import pprint
import re
from time import time
from typing import Literal

from humanize import intcomma
from pandas import *


# Fix path so we can do a relative import: https://stackoverflow.com/a/27876800
if __name__ == '__main__':
    if not __package__:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

        # Relative imports here
        from util import *

INPUT_FILE='10-input.txt'
# INPUT_FILE='10a-example1.txt'
# INPUT_FILE='10a-example2.txt'

input = [f'.{line}.' for line in get_file_contents(INPUT_FILE)[0]]
width_padded = len(input[0]) 

# Pad input with '.'
input.insert(0, '.' * (width_padded))
input.append('.' * (width_padded))

# print(DataFrame(input))
# Find start
start = None
for row, line in enumerate(input):
    if 'S' in line:
        start = row, line.index('S')
        break

SYMBOLS = Literal['.', '|', '-', 'L', 'J', '7', 'F', '.', 'S']
COORD = tuple[int, int]

visited: set[COORD] = {start} 


class DIR(Enum):
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'


def next_step(cur_node: COORD, came_from: DIR, cur_step: int):
    while True:
        if cur_node in visited:
            # print(cur_node, 'visited already')
            return cur_step
        else:
            # print(cur_node)
            cur_step += 1
            visited.add(cur_node)

        cur_symbol = input[cur_node[0]][cur_node[1]]
        match cur_symbol:
            case '|':
                match came_from:
                    case DIR.UP:
                        next_node = cur_node[0]+1, cur_node[1]
                        came_from = DIR.UP
                        # return next_step((cur_node[0]+1, cur_node[1]), DIR.UP, cur_step)
                    case DIR.DOWN:
                        next_node = cur_node[0]-1, cur_node[1]
                        came_from = DIR.DOWN
                        # return next_step((cur_node[0]-1, cur_node[1]), DIR.DOWN, cur_step)
            case '-':
                match came_from:
                    case DIR.LEFT:
                        next_node = cur_node[0], cur_node[1] + 1
                        came_from = DIR.LEFT
                        # return next_step((cur_node[0], cur_node[1]+1), DIR.LEFT, cur_step)
                    case DIR.RIGHT:
                        next_node = cur_node[0], cur_node[1] - 1
                        came_from = DIR.RIGHT
                        # return next_step((cur_node[0], cur_node[1]-1), DIR.RIGHT, cur_step)
            case 'L':
                match came_from:
                    case DIR.UP:
                        next_node = cur_node[0], cur_node[1] + 1
                        came_from = DIR.LEFT
                        # return next_step((cur_node[0], cur_node[1]+1), DIR.LEFT, cur_step)
                    case DIR.RIGHT:
                        next_node = cur_node[0]-1, cur_node[1]
                        came_from = DIR.DOWN
                        # return next_step((cur_node[0]-1, cur_node[1]), DIR.DOWN, cur_step)
            case 'J':
                match came_from:
                    case DIR.UP:
                        next_node = cur_node[0], cur_node[1] - 1
                        came_from = DIR.RIGHT
                        # return next_step((cur_node[0], cur_node[1]-1), DIR.RIGHT, cur_step)
                    case DIR.LEFT:
                        next_node = cur_node[0] - 1, cur_node[1]
                        came_from = DIR.DOWN
                        # return next_step((cur_node[0]-1, cur_node[1]), DIR.DOWN, cur_step)
            case '7':
                match came_from:
                    case DIR.DOWN:
                        next_node = cur_node[0], cur_node[1] - 1
                        came_from = DIR.RIGHT
                        # return next_step((cur_node[0], cur_node[1]-1), DIR.RIGHT, cur_step)
                    case DIR.LEFT:
                        next_node = cur_node[0] + 1, cur_node[1]
                        came_from = DIR.UP
                        # return next_step((cur_node[0]+1, cur_node[1]), DIR.UP, cur_step)
            case 'F':
                match came_from:
                    case DIR.DOWN:
                        next_node = cur_node[0], cur_node[1] + 1
                        came_from = DIR.LEFT
                        # return next_step((cur_node[0], cur_node[1]+1), DIR.LEFT, cur_step)
                    case DIR.RIGHT:
                        next_node = cur_node[0] + 1, cur_node[1]
                        came_from = DIR.UP
                        # return next_step((cur_node[0]+1, cur_node[1]), DIR.UP, cur_step)
            case '.':
                return cur_step
        cur_node = next_node

def process_start(start_node):
    if input[start_node[0]-1][start_node[1]] in ('|', '7', 'F'):
        return next_step((start_node[0]-1, start_node[1]), DIR.DOWN, 0)
    elif input[start_node[0]][start_node[1]-1] in ('-', 'F', 'L'):
        return next_step((start_node[0], start_node[1]-1), DIR.RIGHT, 0)
    elif input[start_node[0]][start_node[1]+1] in ('-', 'J', '7'):
        return next_step((start_node[0], start_node[1]+1), DIR.LEFT, 0)
    elif input[start_node[0]+1][start_node[1]] in ('|', 'J', 'L'):
        return next_step((start_node[0]+1, start_node[1]), DIR.UP, 0)


print('1: ', math.ceil(process_start(start) / 2))
