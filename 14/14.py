#!/usr/bin/env python3
from collections import defaultdict, Counter
import copy
from functools import partial, reduce
from itertools import chain, cycle, takewhile
import math
from operator import mul, itemgetter
import os
import pprint
import re
from time import time

from humanize import intcomma
import numpy as np
import pandas

# Fix path so we can do a relative import: https://stackoverflow.com/a/27876800
if __name__ == '__main__':
    if not __package__:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

        # Relative imports here
        from util import *

INPUT_FILE='14-input.txt'
# INPUT_FILE='14a-example.txt'

input = [line for line in get_file_contents(INPUT_FILE)[0]]

input = add_padding(input, '#')

def transpose(matrix):
    np_array = np.array([list(line) for line in matrix]) 
    return [''.join(line) for line in np_array.transpose()]

transposed = transpose(input)

# print(transposed)


def rotate_cw(matrix):
    np_array = np.array([list(line) for line in matrix]) 
    return [''.join(line) for line in np.rot90(np_array)]


seen = {}
def tilt(matrix):
    res_array = []
    res_sum = 0
    seen_key = tuple(matrix)

    if seen_key in seen:
        return seen[seen_key]

    for line in matrix:
        res_string = ''
        buff = ''
        for i, cur_char in enumerate(line):
            if cur_char in ('O', '.'):
                buff += cur_char
            else:
                if buff:
                    c = Counter(buff)
                    res_string += f"{'O' * c['O']}{'.' * c['.']}"
                    buff = ''
                res_string += '#'

        if buff:
            c = Counter(buff)
            res_string += f"{'O' * c['#']}{'.' * c['.']}"

        res_array.append(res_string)
        str_len = len(res_string)
        for i, cur_char in enumerate(res_string):
            if cur_char == 'O':
                res_sum += str_len-i-1 # subtract 1 to account for padding

    seen[seen_key] = res_array, res_sum    
    return res_array, res_sum

print('1:', tilt(transposed)[1])

cycle_seen = {}
def cycle(matrix, num_times=1):
    for i in range(num_times):
        cycle_seen_key = tuple(matrix.copy())
        # print(cycle_seen_key)
        if cycle_seen_key in cycle_seen:
            # print('hi')
            # return cycle_seen[cycle_seen_key]
            pass
        for i in range(4):
            matrix, _ = tilt(matrix)
            # print(i, pandas.DataFrame(transpose(matrix)))
            # print(i, 'calc load', calc_load(matrix))
            matrix = rotate_cw(matrix)

        # print(cycle_seen_key)
        cycle_seen[cycle_seen_key] = matrix.copy()
    # print('calc_load', calc_load(matrix))
    return matrix

def calc_load(matrix):
    res_sum = 0

    for line in matrix:
        str_len = len(line)
        for i, cur_char in enumerate(line):
            if cur_char == 'O':
                res_sum += str_len-i-1 # subtract 1 to account for padding
    
    return res_sum


# print(np.array(transposed))
# # print()

res_seen = defaultdict(list) 
seen_in_a_row_count = 0
seen_in_a_row_start = None
seen_in_a_row_res = None
check_idx = 0
el_in_cycle = []
for i in range(0, 300):
    res = calc_load(cycle(transposed, i))
    if res in res_seen:
        if seen_in_a_row_count:
            seen_in_a_row_count += 1
            el_in_cycle.append(res)

            if seen_in_a_row_count > 3:
                # print('i', i, 'done', seen_in_a_row_res, el_in_cycle)
                if res == el_in_cycle[check_idx]:
                    check_idx += 1
                    if check_idx > 3:
                        # Matched 3 elements, so assume we're good 
                        cycle_len = i - check_idx - seen_in_a_row_start + 1
                        # print('cycle', cycle_len)
                        # print(f'i: {i} check_idx: {check_idx} seen_in_row_start: {seen_in_a_row_start}')
                        print('2:', el_in_cycle[(1000000000 - seen_in_a_row_start) % cycle_len])
                        break
                else:
                    check_idx = 0
        else:
            seen_in_a_row_start = i
            seen_in_a_row_count = 1
            seen_in_a_row_res = res
            el_in_cycle = [res]
        # print('Seen res', res, f'seeen_row_start: {seen_in_a_row_start}', f'seen_row_count: {seen_in_a_row_count}', res_seen[res])
    else:
        seen_in_a_row_start = None
        seen_in_a_row_count = 0
    res_seen[res].append(i)
    # print(i, res, i % 4)
