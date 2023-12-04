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

nums = []
for row, line in enumerate(input):
    cur_buf = ''
    is_valid = False
    for col, cur_char in enumerate(line):
        if RE_DIGIT.match(cur_char):
            cur_buf += cur_char
            is_valid |= any([SYMBOL.match(x) for x in get_neighbors(input, row, col)])
        else:
            if cur_buf:
                if is_valid:
                    nums.append(int(cur_buf))
                cur_buf = ''
                is_valid = False
        # print(cur_char, get_neighbors(input, row, col),[SYMBOL.match(x) for x in get_neighbors(input, row, col)]) 

    # Handle last column has a valid number
    if cur_buf and is_valid:
        nums.append(int(cur_buf))

    # print(row+1, nums)
    # nums = []
    # print('----')

print('1:', sum(nums))