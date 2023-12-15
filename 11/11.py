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

# print(pandas.DataFrame(input))

def sum_shortest_distances(input, expand_time):
    galaxies: list[tuple[int, int]] = []
    for row_idx, row in enumerate(input):
        for col_idx, col in enumerate(row):
            if col == '#':
                row_mult = len([cur_row_idx_to_expand for cur_row_idx_to_expand in row_idx_to_expand if cur_row_idx_to_expand < row_idx])
                col_mult = len([cur_col_idx_to_expand for cur_col_idx_to_expand in col_idx_to_expand if cur_col_idx_to_expand < col_idx])
                # print(row_idx, col_idx, '|', row_mult, col_mult)
                galaxies.append((row_idx + (expand_time * row_mult), col_idx + (expand_time * col_mult))) 

    # print(galaxies)

    distances = [abs(cur_pair[0][0] - cur_pair[1][0]) + abs(cur_pair[0][1] - cur_pair[1][1]) for cur_pair in combinations(galaxies, 2)]
    return sum(distances)

print ('1:', sum_shortest_distances(input, 1))

# print ('2-ex1:', sum_shortest_distances(input, 10 - 1))
# print ('2-ex2:', sum_shortest_distances(input, 100 - 1))
print ('2:', sum_shortest_distances(input, 1000000 - 1))
