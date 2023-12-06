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

# Fix path so we can do a relative import: https://stackoverflow.com/a/27876800
if __name__ == '__main__':
    if not __package__:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

        # Relative imports here
        from util import *

INPUT_FILE='6-input.txt'
#INPUT_FILE='6a-example.txt'

input = [line for line in get_file_contents(INPUT_FILE)[0]]

times = [int(x) for x in input[0].split(' ')[1:] if x]
distance = [int(x) for x in input[1].split(' ')[1:] if x]

all_res = []
for cur_time, cur_distance in zip(times, distance):
    res = 0
    for idx in range(cur_time):
        if (cur_time - idx) * idx > cur_distance:
            res += 1
    all_res.append(res)

print('1: ', reduce(mul, all_res))