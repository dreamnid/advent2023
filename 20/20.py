#!/usr/bin/env python3
from collections import Counter, defaultdict, deque
from collections.abc import Callable, Collection, Iterable, Sequence
from dataclasses import dataclass
from functools import partial, reduce
from itertools import chain, cycle, takewhile, accumulate
import math
from operator import mul, ge, gt, itemgetter, le, lt
import os
import pprint
import re
from time import time
from typing import NamedTuple

from humanize import intcomma
import numpy as np
import pandas as pd

# Fix path so we can do a relative import: https://stackoverflow.com/a/27876800
if __name__ == '__main__':
    if not __package__:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

        # Relative imports here
        from util import *

INPUT_FILE='20-input.txt'
# INPUT_FILE='20a-example.txt'
# INPUT_FILE='20a-example2.txt'

modules_dest: dict[str, list[str]] = {}
modules_type: dict[str, str] = {'output': 'output'}
modules_value: dict[str, bool] = {}
modules_in_value: dict[str, dict[str, bool]] = defaultdict(lambda: defaultdict(bool))
modules_in_src: dict[str, list[str]] = defaultdict(list) 
for line in get_file_contents(INPUT_FILE)[0]:
    line_split = line.split(' -> ')
    destinations = line_split[1].split(', ')
    if line_split[0] == 'broadcaster':
        modules_dest['broadcaster'] = destinations
        modules_type['broadcaster'] = 'broadcaster'
    else:
        module_name = line_split[0][1:]
        modules_dest[module_name] = destinations
        for cur_dest in destinations:
            modules_in_value[cur_dest][module_name] = False
            modules_in_src[cur_dest].append(module_name)

        match line_split[0][0]:
            case '%':
                modules_type[module_name] = 'flip'
                modules_value[module_name] = False
            case '&':
                modules_type[module_name] = 'conj'
                modules_value[module_name] = False

# pprint.pprint(modules_in_src)

def flip(input: bool, cur_value: bool):
    if input:
        return cur_value
    return not cur_value

def conj(input: list[bool]):
    if all(input):
        return False
    return True

class Step(NamedTuple):
    module_name: str
    input: bool
    src_module_name: str

loop_count = defaultdict(list)

def button(*, break_on_rx=False, it=None):
    process: list[Step] = deque([])
    lo_pulses = 1 # start at 1 due to button
    hi_pulses = 0
    for dest in modules_dest['broadcaster']:
        lo_pulses += 1
        process.append(Step(dest, False, 'broadcaster'))

    while process:
        # pprint.pprint(process)
        cur_module, cur_input, src_module = process.popleft()

        if break_on_rx and cur_module == 'rx' and cur_input is False:
            return None

        match modules_type.get(cur_module):
            case 'flip':
                if cur_input:
                    continue
                new_value = flip(cur_input, modules_value[cur_module])
            case 'conj':
                modules_in_value[cur_module][src_module] = cur_input
                new_value = conj(modules_in_value[cur_module].values())
            case _:
                # print('output', cur_input)
                continue

        if cur_module in modules_in_src['qt'] and new_value:
            loop_count[cur_module].append(it)

            if all([len(loop_count[tmp_module]) > 1 for tmp_module in modules_in_src['qt']]) and break_on_rx:
                return None

        modules_value[cur_module] = new_value
        for next_dest in modules_dest[cur_module]:
            if new_value:
                hi_pulses += 1
            else:
                lo_pulses += 1
            process.append(Step(next_dest, new_value, cur_module))
    # print('-' * 10) 
    return lo_pulses, hi_pulses

print('1:', reduce(mul, (map(sum, zip(*(button() for _ in range(1000)))))))

# Part 2 requires us to find the number of button presses when rx is low. Since the source of rx is qt which is
# a conjection module, rx will only be low when all the inputs are high.
#
# Loop until we get a None which indicates we found the cycle count for all the inputs for qt when it was True
i = 1
while True:
    if button(break_on_rx=True, it=i) is None:
        break

    i += 1
print('2:', math.lcm(*map(lambda x: x[1] - x[0], loop_count.values())))
