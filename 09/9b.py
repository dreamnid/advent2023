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

INPUT_FILE='9-input.txt'
# INPUT_FILE='9a-example.txt'

input = [list(map(lambda x: int(x), line.split(' '))) for line in get_file_contents(INPUT_FILE)[0]]

overall = []
sums = []
for history_idx, history in enumerate(input):
    cur_stack = history
    overall.append([history])
    while any([a != 0 for a in cur_stack]):
        next_stack = [cur_stack[i+1] - cur_stack[i] for i in range(len(cur_stack)-1)]
        overall[history_idx].append(next_stack)
        cur_stack = next_stack

    sums.append(0)
    for cur_history in reversed(overall[history_idx]):
        sums[history_idx] = cur_history[0] - sums[history_idx]

# pprint.pprint(sums)
print('1:', sum(sums))
