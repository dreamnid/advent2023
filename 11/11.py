#!/usr/bin/env python3
from collections import defaultdict
from collections.abc import Iterable, Sequence
from functools import partial, reduce
from itertools import chain, cycle, takewhile, combinations
import math
from operator import mul, itemgetter
import os
import pprint
import re
from time import time

from humanize import intcomma
import pandas

# Fix path so we can do a relative import: https://stackoverflow.com/a/27876800
if __name__ == '__main__':
    if not __package__:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

        # Relative imports here
        from util import *

INPUT_FILE='11-input.txt'
# INPUT_FILE='11a-example.txt'

input = [line for line in get_file_contents(INPUT_FILE)[0]]
# print(pandas.DataFrame(input))

row_idx_to_expand = []
col_idx_to_expand = []
for i, line in enumerate(input):
    if all(a == '.' for a in line):
        row_idx_to_expand.append(i)

width = len(input[0])
for i in range(width):
    if all(line[i] == '.' for line in input):
        col_idx_to_expand.append(i)


def expand_rows(row_idx: int | Iterable[int], my_array: Sequence[Sequence], value='.'):
    if isinstance(row_idx, int):
        row_idx = [row_idx]

    row_to_insert = value * len(my_array[0])

    for offset, cur_idx in enumerate(row_idx):
        my_array.insert(cur_idx + offset, row_to_insert)


def expand_cols(col_idx: int | Iterable[int], my_array: Sequence[Sequence], value='.'):
    if isinstance(col_idx, int):
        col_idx = [col_idx]

    for row_idx, row in enumerate(my_array):
        # print(row, col_idx)
        row_list = list(row)
        for offset, cur_col_idx in enumerate(col_idx):
            row_list.insert(cur_col_idx + offset, value)
        my_array[row_idx] = ''.join(row_list)
        

expand_rows(row_idx_to_expand, input)
expand_cols(col_idx_to_expand, input)

# print(pandas.DataFrame(input))

galaxies: list[tuple[int, int]] = []
for row_idx, row in enumerate(input):
    for col_idx, col in enumerate(row):
        if col == '#':
           galaxies.append((row_idx, col_idx)) 

distances = [abs(cur_pair[0][0] - cur_pair[1][0]) + abs(cur_pair[0][1] - cur_pair[1][1]) for cur_pair in combinations(galaxies, 2)]
print('1:', sum(distances))

