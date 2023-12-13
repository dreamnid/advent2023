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

def find_reflect(maze):
    res_count = 0 
    res_idx = None
    for i in range(0, len(maze)):
        found = False
        for j in range(0, min(i+1, len(maze) - i - 1)):
            # print(i, j, i-j, i+j+1, maze[i-j], maze[i+j+1], maze[i-j] == maze[i+j+1])

            if maze[i-j] == maze[i+j+1]:
                found = True
            else:
                found = False
                break
        if found:
            return i + 1 #num of rows above reflection point
    return None 

def add_padding(maze): 
    cur_res= [f'.{maze[i]}.' for i in range(len(cur_maze))]

    row_pad = '.' * len(cur_res[0])
    cur_res.insert(0, row_pad)
    cur_res.append(row_pad)
    return cur_res


res = []
for cur_maze_id, cur_maze in enumerate(get_file_contents(INPUT_FILE)):
    # cur_maze = get_file_contents(INPUT_FILE)[4]
    row_idx = find_reflect(cur_maze)
    if row_idx:
        res.append(100*row_idx)
        continue

    np_array = np.array([list(line) for line in cur_maze]) 
    transposed = [''.join(line) for line in np_array.transpose()]
    col_idx = find_reflect(transposed)
    if col_idx:
        res.append(col_idx)
        continue

# print(res, len(get_file_contents(INPUT_FILE)), len(res))
print('1:', sum(res))
