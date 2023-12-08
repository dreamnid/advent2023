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

INPUT_FILE='8-input.txt'
# INPUT_FILE='8a-example.txt'

input = [line for line in get_file_contents(INPUT_FILE)[0]]

node_lines = [line for line in get_file_contents(INPUT_FILE)[1]]

nodes: dict[str, tuple[str, str]] = {}
for node_line in node_lines:
    node_id, node_children_str = node_line.split(' = ')
    children = node_children_str.replace('(', '').replace(')', '').split(', ')
    nodes[node_id] = children

instructions = cycle(input[0])


cur_node = 'AAA'
num_steps = 0
for instruct in instructions:
    num_steps += 1
    match instruct:
        case 'L':
            cur_node = nodes[cur_node][0]
        case 'R':
            cur_node = nodes[cur_node][1]
    if cur_node == 'ZZZ':
        break

print(num_steps)
