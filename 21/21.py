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
input = add_padding(input, 'X')

class Pos(NamedTuple):
    row_idx: int
    col_idx: int

start_pos: None | Pos = None
for row_idx, row in enumerate(input):
    if 'S' in row:
        start_pos = Pos(row_idx, row.index('S'))
        break

q: list[list[Pos]] = deque([[start_pos]])
visited: set[Pos] = set()

steps = -1

while q and steps < 6:
    next_pos: list[Pos] = []

    for cur_pos in q.pop():
        visited.add(cur_pos)

        if input[cur_pos.row_idx - 1][cur_pos.col_idx] == '.':
            next_pos.append(Pos(cur_pos.row_idx - 1, cur_pos.col_idx))

        if input[cur_pos.row_idx][cur_pos.col_idx - 1] == '.':
            next_pos.append(Pos(cur_pos.row_idx, cur_pos.col_idx - 1))

        if input[cur_pos.row_idx + 1][cur_pos.col_idx] == '.':
            next_pos.append(Pos(cur_pos.row_idx + 1, cur_pos.col_idx))
        
        if input[cur_pos.row_idx][cur_pos.col_idx + 1] == '.':
            next_pos.append(Pos(cur_pos.row_idx, cur_pos.col_idx + 1))

    steps += 1
    for row_idx, row in enumerate(input):
        for col_idx, col in enumerate(row):
            if Pos(row_idx, col_idx) in next_pos:
                print('O', end='')
            else:
                print(input[row_idx][col_idx], end='')

        print()

    print(len(next_pos))
    q.append(next_pos) 



print('1:', len(visited)) 