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

INPUT_FILE='18-input.txt'
# INPUT_FILE='18a-example.txt'

input = [line for line in get_file_contents(INPUT_FILE)[0]]


class Dir(Enum):
    UP = 'U'
    DOWN = 'D'
    LEFT = 'L'
    RIGHT = 'R'


class Pos(NamedTuple):
    row_idx: int
    col_idx: int


land: dict[int, dict[int, str]] = defaultdict(lambda: defaultdict(lambda: '.'))

cur_pos = Pos(0, 0)
land[0][0] = '#'

col_idx_start = 0
col_idx_end = 0
row_idx_start = 0
row_idx_end = 0
for line in input:
    dir_str, count_str, rgb = line.split(' ')
    dir = Dir(dir_str)
    count = int(count_str)

    match dir:
        case Dir.UP:
            for i in range(count):
                land[cur_pos.row_idx - i][cur_pos.col_idx] = '#'
            cur_pos = Pos(cur_pos.row_idx - count, cur_pos.col_idx)
        case Dir.LEFT:
            for i in range(count):
                land[cur_pos.row_idx][cur_pos.col_idx - i] = '#'
            cur_pos = Pos(cur_pos.row_idx, cur_pos.col_idx - count)
        case Dir.DOWN:
            for i in range(count):
                land[cur_pos.row_idx + i][cur_pos.col_idx] = '#'
            cur_pos = Pos(cur_pos.row_idx + count, cur_pos.col_idx)
        case Dir.RIGHT:
            for i in range(count):
                land[cur_pos.row_idx][cur_pos.col_idx + i] = '#'
            cur_pos = Pos(cur_pos.row_idx, cur_pos.col_idx + count)

    if cur_pos.col_idx < col_idx_start:
        col_idx_start = cur_pos.col_idx
    elif cur_pos.col_idx > col_idx_end:
        col_idx_end = cur_pos.col_idx 

    if cur_pos.row_idx < row_idx_start:
        row_idx_start = cur_pos.row_idx
    elif cur_pos.row_idx > row_idx_end:
        row_idx_end = cur_pos.row_idx

height = row_idx_end - row_idx_start + 1
width = col_idx_end - col_idx_start + 1
# print(row_idx_start, row_idx_end, col_idx_start, col_idx_end)
# print(height, width)

def fill(start_row_idx, start_col_idx, land):
    count = 0
    q = [(start_row_idx, start_col_idx)]

    while q:
        cur_pos = q.pop(0)
        if land[cur_pos[0]][cur_pos[1]] == '.':
            land[cur_pos[0]][cur_pos[1]] = '/'
        else:
            continue
        
        q.append((cur_pos[0]-1, cur_pos[1]))
        q.append((cur_pos[0], cur_pos[1]-1))
        q.append((cur_pos[0]+1, cur_pos[1]))
        q.append((cur_pos[0], cur_pos[1]+1))

fill(-143, 102, land)

counter = 0
for row_idx in range(row_idx_start, row_idx_end + 1):
    inside = False
    print(f'{row_idx:3d}', end='')
    edge_count = 0
    for col_idx in range(col_idx_start, col_idx_end + 1):
        if land[row_idx][col_idx] == '#':
            counter += 1
            edge_count += 1

            if not inside and land[row_idx][col_idx + 1] == '.' and [tmp_col_idx for tmp_col_idx in list(land[row_idx].keys()) if isinstance(tmp_col_idx, int) and tmp_col_idx > col_idx + 1]:
                inside = True
            elif inside and land[row_idx][col_idx - 1] == '.':
                inside = False 
            print('#', end='')
        elif land[row_idx][col_idx] == '/':
            print('/', end='')
            counter += 1
        else:
            if col_idx > 100:
                # break
                pass
            if inside and False:
                # counter += 1
                print('/', end='')
            else:
                print('.', end='')
    print()

    
print('1:', counter)