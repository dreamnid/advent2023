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
from typing import Literal

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
INPUT_FILE='8b-example.txt'
INPUT_FILE='8b-test.txt'

input = [line for line in get_file_contents(INPUT_FILE)[0]]

node_lines = [line for line in get_file_contents(INPUT_FILE)[1]]

nodes: dict[str, tuple[str, str]] = {}
for node_line in node_lines:
    node_id, node_children_str = node_line.split(' = ')
    children = node_children_str.replace('(', '').replace(')', '').split(', ')
    nodes[node_id] = children

instructions = cycle(input[0])

cur_nodes = list(filter(lambda x: x[-1] == 'A', nodes.keys())) 
print(cur_nodes)

def instruction_idx(instruct: Literal['L', 'R']) -> Literal[0, 1]:
    match instruct:
        case 'L':
            return 0
        case 'R':
            return 1

num_steps = 0
for instruct in instructions:
    num_steps += 1

    cur_nodes = list(map(lambda x: nodes[x][instruction_idx(instruct)], cur_nodes))
    # print(num_steps, cur_nodes)
    if all([cur_node[-1] == 'Z' for cur_node in cur_nodes]):
        break

print('2:', num_steps)
