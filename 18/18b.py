#!/usr/bin/env python3
from collections import defaultdict
from collections.abc import Sequence
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


def range_overlaps(row1_range: Sequence[int, int], row2_range: Sequence[int, int]):
    if row1_range[0] < row2_range[0]:
        row_a_range = row1_range
        row_b_range = row2_range
    else:
        row_a_range = row2_range
        row_b_range = row1_range

    # row_a_range covers row_b_range
    if row_a_range[0] <= row_b_range[0] and row_a_range[1] >= row_b_range[0]:
        return True

    # row_b_range covers row_a_range
    if row_a_range[0] >= row_b_range[0] and row_a_range[1] < row_b_range[0]:
        return True

    return False


land: dict[int, list[tuple[int, int]]] = defaultdict(list)

row_idx_start = 0
row_idx_end = 0
col_idx_start = 0
col_idx_end = 0
cur_pos = Pos(0, 0)
cur_count = 0

cur_stack_count = 1
for line in input:
    dir_str, count_str, rgb = line.split(' ')
    dir = Dir(dir_str)
    count = int(count_str)
    rgb = rgb[1:-1]

    if True:
        match rgb[-1]:
            case '0':
                dir = Dir.RIGHT
            case '1':
                dir = Dir.DOWN
            case '2':
                dir = Dir.LEFT
            case '3':
                dir = Dir.UP
        
        count = int(rgb[1:-1], base=16)

    cur_count += count
    match dir:
        case Dir.UP:
            for i in range(1, count):
                land[cur_pos.row_idx - i].append((cur_pos.col_idx, cur_pos.col_idx))
                land[cur_pos.row_idx - i].sort(key=lambda x: (x[1], x[0]))
            cur_pos = Pos(cur_pos.row_idx - count, cur_pos.col_idx)
        case Dir.LEFT:
            cur_stack_count += count
            land[cur_pos.row_idx].append((cur_pos.col_idx - count, cur_pos.col_idx))
            land[cur_pos.row_idx] = sorted(land[cur_pos.row_idx], key=lambda x: (x[1], x[0]))
            cur_pos = Pos(cur_pos.row_idx, cur_pos.col_idx - count)
        case Dir.DOWN:
            for i in range(1, count):
                land[cur_pos.row_idx + i].append((cur_pos.col_idx, cur_pos.col_idx))
                land[cur_pos.row_idx + i].sort(key=lambda x: (x[1], x[0]))
            cur_pos = Pos(cur_pos.row_idx + count, cur_pos.col_idx)
        case Dir.RIGHT:
            cur_stack_count += count
            land[cur_pos.row_idx].append((cur_pos.col_idx, cur_pos.col_idx + count))
            land[cur_pos.row_idx] = sorted(land[cur_pos.row_idx], key=lambda x: (x[1], x[0]))
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
print('populated', 'count:', cur_count)
# print('dim', row_idx_start, row_idx_end, col_idx_start, col_idx_end)
# print(height, width)


filled: dict[int, list[tuple[int, int]]] = defaultdict(list)

# find the upper left corner
# first_row  = sorted(land[row_idx_start], key=lambda x: x[1])
# print(first_row)

# Start at the 2nd row since nothing will need to be filled in
for row_idx in range(row_idx_start+1, row_idx_end + 1):
    row_contents = land[row_idx] 
    if len(row_contents) <= 1:
        continue

    for i in range(len(row_contents) - 1):
        fill_range = row_contents[i][1]+1, row_contents[i+1][0] - 1
        if any(cur_prev_range for cur_prev_range in filled[row_idx-1] if range_overlaps(cur_prev_range, fill_range)) or (
            any(cur_prev_range for cur_prev_range in land[row_idx-1] if range_overlaps(cur_prev_range, fill_range) and 
                not any(cur_prev_range for cur_prev_range in filled[row_idx-2] if range_overlaps(cur_prev_range, fill_range)) )
        ):
            fill_count = fill_range[1] - fill_range[0] + 1
            # print('row_idx:', row_idx, 'fill:', fill_range, 'fill count:', fill_count)
            filled[row_idx].append(fill_range)
            cur_count += fill_count

# Print out landfill plan
# for row_idx in range(row_idx_start, row_idx_end + 1):
#     inside = False
#     print(f'{row_idx:3d}', end='')
#     for col_idx in range(col_idx_start, col_idx_end + 1):
#         if any(cur_prev_range for cur_prev_range in land[row_idx] if range_overlaps(cur_prev_range, (col_idx, col_idx))):
#             print('#', end='')
#         elif any(cur_prev_range for cur_prev_range in filled[row_idx] if range_overlaps(cur_prev_range, (col_idx, col_idx))):
#             print('/', end='')
#         else:
#             if col_idx > 100:
#                 # break
#                 pass
#             if inside and False:
#                 # counter += 1
#                 print('/', end='')
#             else:
#                 print('.', end='')
#     print()

print('2:', cur_count)