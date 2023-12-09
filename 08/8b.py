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
# INPUT_FILE='8b-example.txt'
# INPUT_FILE='8b-test.txt'

input = [line for line in get_file_contents(INPUT_FILE)[0]]

node_lines = [line for line in get_file_contents(INPUT_FILE)[1]]

nodes: dict[str, tuple[str, str]] = {}
for node_line in node_lines:
    node_id, node_children_str = node_line.split(' = ')
    children = node_children_str.replace('(', '').replace(')', '').split(', ')
    nodes[node_id] = children

instructions = cycle(input[0])

cur_nodes = list(filter(lambda x: x[-1] == 'A', nodes.keys())) 

def instruction_idx(instruct: Literal['L', 'R']) -> Literal[0, 1]:
    match instruct:
        case 'L':
            return 0
        case 'R':
            return 1

distances = [0] * len(cur_nodes)
num_steps = 0
for pc, instruct in enumerate(instructions, start=1):
    num_steps += 1

    cur_nodes = list(map(lambda x: nodes[x][instruction_idx(instruct)], cur_nodes))
    # print(num_steps, cur_nodes)
    for node_id, cur_node in enumerate(cur_nodes):
        if cur_node[-1] == 'Z':
            if not distances[node_id]:
                distances[node_id] = pc - distances[node_id]
            # print(f'Found Z, node_id: {node_id} {pc} {pc % len(input[0])} distance: {distances[node_id]}')

    if all(distances):
        break


print('2:', math.lcm(*distances))
