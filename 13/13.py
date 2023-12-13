#!/usr/bin/env python3
from collections import defaultdict
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

INPUT_FILE='13-input.txt'
# INPUT_FILE='13a-example.txt'

def find_reflect(maze, max_num_diff=0):
    res_idx = None
    for i in range(0, len(maze)):
        found = False
        mismatch_count = 0
        for j in range(0, min(i+1, len(maze) - i - 1)):
            # print(i, j, i-j, i+j+1, maze[i-j], maze[i+j+1], maze[i-j] == maze[i+j+1])

            if maze[i-j] == maze[i+j+1]:
                found = True
            else:
                mismatch_count += sum([1 for a, b in zip(maze[i-j], maze[i+j+1]) if a != b])
                if mismatch_count == max_num_diff:
                    found = True
                else:
                    found = False
                    break
        if found and mismatch_count == max_num_diff:
            return i + 1 #num of rows above reflection point
    return None 

def add_padding(maze): 
    cur_res= [f'.{maze[i]}.' for i in range(len(maze))]

    row_pad = '.' * len(cur_res[0])
    cur_res.insert(0, row_pad)
    cur_res.append(row_pad)
    return cur_res


def solver(max_num_diff=0):
    res = []
    for cur_maze_id, cur_maze in enumerate(get_file_contents(INPUT_FILE)):
        # cur_maze = get_file_contents(INPUT_FILE)[4]
        row_idx = find_reflect(cur_maze, max_num_diff)
        if row_idx:
            res.append(100*row_idx)
            continue

        np_array = np.array([list(line) for line in cur_maze]) 
        transposed = [''.join(line) for line in np_array.transpose()]
        col_idx = find_reflect(transposed, max_num_diff)
        if col_idx:
            res.append(col_idx)
            continue
    return res

# print(solver(), len(get_file_contents(INPUT_FILE)), len(solver()))
print('1:', sum(solver()))
print('2:', sum(solver(1)))
