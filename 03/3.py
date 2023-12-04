#!/usr/bin/env python3
from collections import defaultdict
from functools import partial, reduce
from itertools import chain, cycle, takewhile
import math
from operator import mul
import os
import pprint
import re
from time import time


# Fix path so we can do a relative import: https://stackoverflow.com/a/27876800
if __name__ == '__main__':
    if not __package__:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

        # Relative imports here
        from util import *

INPUT_FILE='3-input.txt'
#INPUT_FILE='3a-example.txt'
#INPUT_FILE='3a-test1.txt'

input = [line for line in get_file_contents(INPUT_FILE)[0]]

RE_DIGIT = re.compile(r'\d')
SYMBOL = re.compile(r'[^\w\s.]') # Exclude non word/space char and periods

star: dict[tuple[int, int], list[int]] = defaultdict(list)

nums = []
for row, line in enumerate(input):
    cur_buf = ''
    is_valid = False
    neighboring_star_positions: set[tuple[int, int]] = set()
    for col, cur_char in enumerate(line):
        if RE_DIGIT.match(cur_char):
            cur_buf += cur_char
            is_valid |= any([SYMBOL.match(x) for x in get_neighbors(input, row, col)])
            neighboring_star_positions |= {x[1] for x in get_neighbors_with_pos(input, row, col) if x[0] == '*'}
        else:
            if cur_buf:
                if is_valid:
                    nums.append(int(cur_buf))
                if neighboring_star_positions:
                    for cur_star_pos in neighboring_star_positions:
                        star[cur_star_pos].append(int(cur_buf))
                cur_buf = ''
                is_valid = False
                neighboring_star_positions = set()
        # print(cur_char, get_neighbors(input, row, col),[SYMBOL.match(x) for x in get_neighbors(input, row, col)]) 

    # Handle last column that has a valid number
    if cur_buf and is_valid:
        nums.append(int(cur_buf))

    if cur_buf and neighboring_star_positions:
        for cur_star_pos in neighboring_star_positions:
            star[cur_star_pos].append(int(cur_buf))

    # print(row+1, nums)
    # nums = []
    # print('----')

print('1:', sum(nums))
print('2:', sum([reduce(mul, j) for j in star.values() if len(j) == 2]))
