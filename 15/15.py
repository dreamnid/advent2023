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

INPUT_FILE='15-input.txt'
# INPUT_FILE='15a-example.txt'

input = get_file_contents(INPUT_FILE)[0][0].split(',')

def hash(my_str: str):
    return reduce(lambda acc, y: ((acc + ord(y)) * 17) % 256, my_str, 0)

# print(hash('HASH') == 52)
hashed_step = [hash(step) for step in input]
print('1: ', sum(hashed_step))