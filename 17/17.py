#!/usr/bin/env python3
from collections import defaultdict
from enum import Enum
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

INPUT_FILE='17-input.txt'
INPUT_FILE='17a-example.txt'

input = [line for line in get_file_contents(INPUT_FILE)[0]]
class Dir(Enum):
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'

type Pos = list[int, int]
type Node = list[Pos, Dir]

input = add_padding(input, float('inf'))

start_pos = ((1, 1), Dir.RIGHT)
q = []
dist = defaultdict(lambda: float('inf'))
prev = {}

dist[start_pos[0]] = 0
cur_dir = Dir.RIGHT

