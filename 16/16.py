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

from humanize import intcomma

# Fix path so we can do a relative import: https://stackoverflow.com/a/27876800
if __name__ == '__main__':
    if not __package__:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

        # Relative imports here
        from util import *

INPUT_FILE='16-input.txt'
# INPUT_FILE='16a-example.txt'

input = [line for line in get_file_contents(INPUT_FILE)[0]]

input = add_padding(input, 'X')

class Dir(Enum):
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'

type Pos = list[int, int]
type Node = list[Pos, Dir]

visited: set[Pos] = set()
visited_with_dir: set[Node] = set()

start_pos = [[1, 1], Dir.RIGHT]

process = [start_pos]

idx = 0
while (process):
    cur_node = process.pop(0)
    cur_row, cur_col = cur_node[0]
    # print(cur_node, input[cur_row][cur_col])

    if (tuple(cur_node[0]), cur_node[1],) in visited_with_dir:
        continue

    cur_dir = cur_node[1]

    match(input[cur_row][cur_col]):
        case '.':
            match cur_dir:
                case Dir.RIGHT:
                    process.append([[cur_row, cur_col + 1], Dir.RIGHT])
                case Dir.UP:
                    process.append([[cur_row - 1, cur_col], Dir.UP])
                case Dir.LEFT:
                    process.append([[cur_row, cur_col - 1], Dir.LEFT])
                case Dir.DOWN:
                    process.append([[cur_row + 1, cur_col], Dir.DOWN])
        case '\\':
            match cur_dir:
                case Dir.RIGHT:
                    process.append([[cur_row + 1, cur_col], Dir.DOWN])
                case Dir.UP:
                    process.append([[cur_row , cur_col - 1], Dir.LEFT])
                case Dir.LEFT:
                    process.append([[cur_row - 1, cur_col], Dir.UP])
                case Dir.DOWN:
                    process.append([[cur_row, cur_col + 1], Dir.RIGHT])
        case '|':
            match cur_dir:
                case Dir.RIGHT:
                    process.append([[cur_row - 1, cur_col], Dir.UP])
                    process.append([[cur_row + 1, cur_col], Dir.DOWN])
                case Dir.UP:
                    process.append([[cur_row - 1, cur_col], Dir.UP])
                case Dir.LEFT:
                    process.append([[cur_row - 1, cur_col], Dir.UP])
                    process.append([[cur_row + 1, cur_col], Dir.DOWN])
                case Dir.DOWN:
                    process.append([[cur_row + 1, cur_col], Dir.DOWN])
        case '/':
            match cur_dir:
                case Dir.RIGHT:
                    process.append([[cur_row - 1, cur_col], Dir.UP])
                case Dir.UP:
                    process.append([[cur_row, cur_col + 1], Dir.RIGHT])
                case Dir.LEFT:
                    process.append([[cur_row + 1, cur_col], Dir.DOWN])
                case Dir.DOWN:
                    process.append([[cur_row, cur_col - 1], Dir.LEFT])
        case '-':
            match cur_dir:
                case Dir.RIGHT:
                    process.append([[cur_row, cur_col + 1], Dir.RIGHT])
                case Dir.UP:
                    process.append([[cur_row, cur_col - 1], Dir.LEFT])
                    process.append([[cur_row, cur_col + 1], Dir.RIGHT])
                case Dir.LEFT:
                    process.append([[cur_row, cur_col - 1], Dir.LEFT])
                case Dir.DOWN:
                    process.append([[cur_row, cur_col - 1], Dir.LEFT])
                    process.append([[cur_row, cur_col + 1], Dir.RIGHT])
        case _:
            continue
    
    visited.add(tuple(cur_node[0]))
    visited_with_dir.add((tuple(cur_node[0]), cur_node[1],))

    if idx % 10 == 0 and False:
        for row_idx, row in enumerate(input):
            for col_idx, col in enumerate(row):
                if (row_idx, col_idx) in visited:
                    print('#', end='')
                else:
                    print('.', end='')
            print()
        
        print('---------------')
    
    idx += 1

print('1:', len(visited)) 