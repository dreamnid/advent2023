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

from humanize import intcomma

# Fix path so we can do a relative import: https://stackoverflow.com/a/27876800
if __name__ == '__main__':
    if not __package__:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

        # Relative imports here
        from util import *

INPUT_FILE='4-input.txt'
#INPUT_FILE='4a-example.txt'

pts = 0
card_copies = defaultdict(int)
for line in get_file_contents(INPUT_FILE)[0]:
    line_split = line.split(' | ')
    card_num = int(line_split[0].split(':')[0].replace(' ', '')[len('Card'):])
    card_copies[card_num] += 1

    winning = set(int(x) for x in line_split[0].split(': ')[1].strip().split(' ') if x)
    our_nums = set(int(x) for x in line_split[1].strip().split(' ') if x)
    num_matching_nums = len(our_nums.intersection(winning))
    for x in range(num_matching_nums):
        card_copies[card_num + x + 1] += card_copies[card_num]

    pts += 2 ** (num_matching_nums - 1) if num_matching_nums else 0

print('1: ', pts)
print('2: ', sum(card_copies.values()))

