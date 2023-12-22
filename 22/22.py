#!/usr/bin/env python3
from collections import Counter, defaultdict, deque
from collections.abc import Callable, Collection, Iterable, Sequence
from dataclasses import dataclass
from functools import partial, reduce
from itertools import chain, cycle, takewhile
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

INPUT_FILE='22-input.txt'
# INPUT_FILE='22a-example.txt'
# INPUT_FILE='22b-example.txt'


class Pos(NamedTuple):
    row: int
    col: int
    height: int


class Block(NamedTuple):
    id: int
    start: Pos
    end: Pos


blocks: list[Block] = []
for idx, line in enumerate(get_file_contents(INPUT_FILE)[0]):
    line_split = line.split('~')
    blocks.append(Block(idx, Pos(*[int(x) for x in line_split[0].split(',')]), Pos(*[int(x) for x in line_split[1].split(',')])))

# blocks.sort(key=lambda x: (x.start.height, x.id))

grid: dict[int, dict[int, deque[Block | None]]] = defaultdict(lambda: defaultdict(deque))
supported_by: dict[Block, set[Block]] = defaultdict(set)
supports: dict[Block, set[Block]] = defaultdict(set)

def find_start_height(block: Block):
    if block.start.height == block.end.height:
        if block.start.row == block.end.row:
            return max((len(grid[block.start.row][i]) for i in range(min(block.start.col, block.end.col), max(block.start.col, block.end.col) + 1)))
        elif block.start.col == block.end.col:
            return max([len(grid[i][block.start.col]) for i in range(min(block.start.row, block.end.row), max(block.start.row, block.end.row) + 1)])
        else:
            tmp = sorted([block.start, block.end], key=lambda x: x.row)
            cur_slope = int((tmp[1].col - tmp[0].col)/(tmp[1].row - tmp[0].row))
            num_steps = min(abs(tmp[1].col - tmp[0].col), abs(tmp[1].row - tmp[0].row)) + 1
            return max([len(grid[tmp[0].row + i][tmp[0].col + i * cur_slope]) for i in range(num_steps)])
    else:
        return len(grid[block.start.row][block.start.col])

for block in blocks:
    start_height = find_start_height(block)

    if block.start.height == block.end.height:
        if block.start.row == block.end.row:
            for i in range(min(block.start.col, block.end.col), max(block.start.col, block.end.col) + 1):
                if start_height > 0 and len(grid[block.start.row][i]) == start_height:
                    supported_by[block].add(grid[block.start.row][i][-1])
                    supports[grid[block.start.row][i][-1]].add(block)
                while len(grid[block.start.row][i]) < start_height:
                    grid[block.start.row][i].append(None)

                grid[block.start.row][i].append(block)
        elif block.start.col == block.end.col:
            for i in range(min(block.start.row, block.end.row), max(block.start.row, block.end.row) + 1):
                if start_height > 0 and len(grid[i][block.start.col]) == start_height:
                    supported_by[block].add(grid[i][block.start.col][-1])
                    supports[grid[i][block.start.col][-1]].add(block)
                while len(grid[i][block.start.col]) < start_height:
                    grid[i][block.start.col].append(None)
                grid[i][block.start.col].append(block)
        else:
            tmp = sorted([block.start, block.end], key=lambda x: x.row)
            cur_slope = int((tmp[1].col - tmp[0].col)/(tmp[1].row - tmp[0].row))
            num_steps = min(abs(tmp[1].col - tmp[0].col), abs(tmp[1].row - tmp[0].row)) + 1
            for i in range(num_steps):
                if start_height > 0 and len(grid[tmp[0].row + i * cur_slope][tmp[0].col + i * cur_slope]) == start_height:
                    supported_by[block].add(grid[tmp[0].row + i * cur_slope][tmp[0].col + i * cur_slope][-1])
                    supports[grid[tmp[0].row + i * cur_slope][tmp[0].col + i * cur_slope][-1]].add(block)
                while len(grid[tmp[0].row + i][tmp[0].col + i * cur_slope]) < start_height:
                    grid[tmp[0].row + i][tmp[0].col + i * cur_slope].append(None)
                grid[tmp[0].row + i][tmp[0].col + i * cur_slope].append(block)
    else:
        if len(grid[block.start.row][block.start.col]) > 0:
            supported_by[block].add(grid[block.start.row][block.start.col][-1])
        for i in range(min(block.start.height, block.end.height), max(block.start.height, block.end.height) + 1):
            grid[block.start.row][block.start.col].append(block)

safe_to_remove: list[Block] = []
for block in blocks:
    if block.start.height == block.end.height:
        if block.start.row == block.end.row:
            if all((grid[block.start.row][i][-1].id == block.id or len(supported_by[grid[block.start.row][i][-1]]) > 1 for i in range(min(block.start.col, block.end.col), max(block.start.col, block.end.col) + 1))):
                safe_to_remove.append(block)
        elif block.start.col == block.end.col:
            if all((grid[i][block.start.col][-1].id == block.id or len(supported_by[grid[i][block.start.col][-1]]) > 1 for i in range(min(block.start.row, block.end.row), max(block.start.row, block.end.row) + 1))):
                safe_to_remove.append(block)
        else:
            tmp = sorted([block.start, block.end], key=lambda x: x.row)
            cur_slope = int((tmp[1].col - tmp[0].col)/(tmp[1].row - tmp[0].row))
            num_steps = min(abs(tmp[1].col - tmp[0].col), abs(tmp[1].row - tmp[0].row)) + 1
            if all((grid[tmp[0].row + i][tmp[0].col + i * cur_slope][-1].id == block.id or len(supported_by[grid[tmp[0].row + i][tmp[0].col + i * cur_slope][-1]]) > 1 for i in range(num_steps))):
                safe_to_remove.append(block)
    else:
        if grid[block.start.row][block.start.col][-1].id == block.id or len(supported_by[grid[block.start.row][block.start.col][-1]]) > 1:
            safe_to_remove.append(block)


pprint.pprint(grid)
# pprint.pprint(supported_by)
# pprint.pprint(safe_to_remove)

print('1:', len(safe_to_remove))