#!/usr/bin/env python3
from collections import Counter, defaultdict, deque
from collections.abc import Callable, Collection, Iterable, Sequence
from dataclasses import dataclass
from functools import partial, reduce
from itertools import chain, cycle, takewhile
import math
from operator import mul, ge, gt, itemgetter, le, lt
import os
import pprint
import re
from time import time
from typing import NamedTuple

from humanize import intcomma
import numpy as np
import pandas as pd

# Fix path so we can do a relative import: https://stackoverflow.com/a/27876800
if __name__ == '__main__':
    if not __package__:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

        # Relative imports here
        from util import *

INPUT_FILE='21-input.txt'
INPUT_FILE='21a-example.txt'

input = [line for line in get_file_contents(INPUT_FILE)[0]]

height = len(input)
width = len(input[0])

class Pos(NamedTuple):
    row_idx: int
    col_idx: int

start_pos: None | Pos = None
for row_idx, row in enumerate(input):
    if 'S' in row:
        break

start_pos = Pos(row_idx, row.index('S'))
input[start_pos.row_idx] = f'{row[:start_pos.col_idx]}.{row[start_pos.col_idx+1:]}'

q: deque[set[Pos]] = deque([{start_pos}])
visited: set[Pos] = set()

steps = 0
# MAX_STEPS = 26501365
MAX_STEPS = 1000 
wraps = True
next_pos: set[Pos]
min_row_idx = 0
min_col_idx = 0
max_row_idx = 0
max_col_idx = 0

while q and steps < MAX_STEPS:
    next_pos = set()

    for cur_pos in q.pop():
        visited.add(cur_pos)
        if min_row_idx > cur_pos.row_idx:
            min_row_idx = cur_pos.row_idx - 1
        if max_row_idx  < cur_pos.row_idx:
            max_row_idx = cur_pos.row_idx + 1
        if min_col_idx > cur_pos.col_idx:
            min_col_idx = cur_pos.col_idx - 1
        if max_col_idx < cur_pos.col_idx:
            max_col_idx = cur_pos.col_idx + 1

        modded_row_idx = cur_pos.row_idx % height
        modded_col_idx = cur_pos.col_idx % width

        # Up
        tmp_idx = modded_row_idx
        if wraps and tmp_idx == 0:
            # Wrap to bottom
            tmp_idx = height
        if input[tmp_idx - 1][modded_col_idx] in ['.', 'S']:
            next_pos.add(Pos(cur_pos.row_idx - 1, cur_pos.col_idx))

        # Left
        tmp_idx = modded_col_idx 
        if wraps and tmp_idx == 0:
            # Wrap to right side
            tmp_idx = width
        if input[modded_row_idx][tmp_idx - 1] in ['.', 'S']:
            next_pos.add(Pos(cur_pos.row_idx, cur_pos.col_idx - 1))

        # Down
        tmp_idx = modded_row_idx
        if wraps and tmp_idx == height - 1:
            # Wrap to top
            tmp_idx = -1
        if input[tmp_idx + 1][modded_col_idx] in ['.', 'S']:
            next_pos.add(Pos(cur_pos.row_idx + 1, cur_pos.col_idx))

        # Right 
        tmp_idx = modded_col_idx 
        if wraps and tmp_idx == width - 1:
            # Wrap to left side
            tmp_idx = -1 
        if input[modded_row_idx][tmp_idx + 1] in ['.', 'S']:
            next_pos.add(Pos(cur_pos.row_idx, cur_pos.col_idx + 1))

    steps += 1
    q.append(next_pos) 
    if steps % 100 == 0 and steps != 0:
        print(f'{steps}/{MAX_STEPS}')


if False:
    for row_idx in range(math.floor(min_row_idx / height) * height, math.ceil(max_row_idx / height) * height):
        for col_idx in range(math.floor(min_col_idx / width) * width, math.ceil(max_col_idx / width) * width):
            if Pos(row_idx, col_idx) in next_pos:
                print('O', end='')
            else:
                print(input[row_idx % height][col_idx % width], end='')

        print()
    print('-' * 10)

print(width)
print(min_col_idx, max_col_idx, math.floor(min_col_idx / width) * width, math.ceil(max_col_idx / width) * width)
print('1:', len(next_pos)) 