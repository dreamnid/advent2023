#!/usr/bin/env python3
from collections import defaultdict
from collections.abc import Callable, Container, Sequence
from enum import Enum
from functools import partial, reduce
from itertools import chain, cycle, takewhile
import math
from operator import mul, itemgetter
import os
import pprint
import re
from time import time
from typing import NamedTuple

from humanize import intcomma
from termcolor import colored, cprint

# Fix path so we can do a relative import: https://stackoverflow.com/a/27876800
if __name__ == '__main__':
    if not __package__:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

        # Relative imports here
        from util import *

INPUT_FILE='17-input.txt'
# INPUT_FILE='17a-example.txt'

input = [[int(x) for x in line] for line in get_file_contents(INPUT_FILE)[0]]
import pandas as pd


class Dir(Enum):
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'


class Pos(NamedTuple):
    row_idx: int
    col_idx: int


class Movement(NamedTuple):
    dir: Dir
    same_dir_count: int


class Node(NamedTuple):
    pos: Pos
    movement: Movement
    dist: int = 0
    prev: list[Pos] = []


input = add_padding(input, float('inf'))

start_pos = Pos(1, 1)
finish_pos = Pos(len(input) - 2, len(input[0]) - 2)

dist: dict[Pos, float | int] = defaultdict(lambda: float('inf'))
pending_visit: set[tuple[Pos, Movement]] = set()
visited: set[tuple[Pos, Movement]] = set()
prev: dict[Pos, list[Pos]] = defaultdict(list)


def is_same_movement_allowed(dir: Dir, movement: Movement):
    if movement.dir == dir and movement.same_dir_count < MAX_SAME_DIR_COUNT:
        return True

    if movement.dir != dir:
        return True

    return False


def get_val(pos: Pos, matrix):
    return matrix[pos.row_idx][pos.col_idx]


def is_valid_pos(pos: Pos, matrix):
    return get_val(pos, matrix) != float('inf')


def process_dir(cur_node: Node, next_dir: Dir, next_pos: Pos, matrix, visited):
    next_movement_count = cur_node.movement.same_dir_count + 1 if cur_node.movement.dir == next_dir else 1
    next_movement = Movement(next_dir, next_movement_count)
    if is_valid_pos(next_pos, matrix) and (next_pos, next_movement) not in pending_visit and is_same_movement_allowed(next_dir, cur_node.movement):
        neighbor_distance = cur_node.dist + get_val(next_pos, matrix)

        if neighbor_distance <= dist[next_pos]:
            dist[next_pos] = neighbor_distance
            prev[next_pos] = cur_node.prev

        pending_visit.add((next_pos, next_movement))
        return Node(next_pos, next_movement, neighbor_distance, [*cur_node.prev, cur_node.pos])
    
    return None


MAX_SAME_DIR_COUNT = 3

# Initialization
# Set the distances of the neighbors to dist
right_pos = Pos(row_idx=1, col_idx=2)
down_pos = Pos(row_idx=2, col_idx=1)

# Add neighbors of start_pos to q
dist[right_pos] = get_val(right_pos, input)
dist[down_pos] = get_val(down_pos, input)
q: list[Node] = [Node(right_pos, Movement(Dir.RIGHT, 1), dist[right_pos]), Node(down_pos, Movement(Dir.DOWN, 1), dist[down_pos])]

while q:
    # q.sort(key=lambda cur_node: dist[cur_node.pos])
    q.sort(key=lambda cur_node: cur_node.dist)

    if (ab := [cur_node for cur_node in q if cur_node.pos == Pos(2, 6)]):
        if len(ab) > 1:
            pass
    # Get the next node with the lowest heat cost
    cur_node = q.pop(0)
    visited.add((cur_node.pos, cur_node.movement))
    
    neighbors = []

    # Up
    if cur_node.movement.dir != Dir.DOWN:
        if (next_node := process_dir(cur_node, Dir.UP, Pos(cur_node.pos.row_idx-1, cur_node.pos.col_idx), input, visited)):
            neighbors.append(next_node)
    # Left
    if cur_node.movement.dir != Dir.RIGHT:
        if (next_node := process_dir(cur_node, Dir.LEFT, Pos(cur_node.pos.row_idx, cur_node.pos.col_idx-1), input, visited)):
            neighbors.append(next_node)
    # Down
    if cur_node.movement.dir != Dir.UP:
        if (next_node := process_dir(cur_node, Dir.DOWN, Pos(cur_node.pos.row_idx+1, cur_node.pos.col_idx), input, visited)):
            neighbors.append(next_node)
    # Right
    if cur_node.movement.dir != Dir.LEFT:
        if (next_node := process_dir(cur_node, Dir.RIGHT, Pos(cur_node.pos.row_idx, cur_node.pos.col_idx+1), input, visited)):
            neighbors.append(next_node)

    q.extend(neighbors) 

print('1:', dist[finish_pos])

# print(get_val(Pos(1, 1), input), is_valid_pos(Pos(1, 1), input))
# print(pd.DataFrame(input))

def get_traversal_path(prev: dict[Pos, Node], input):
    seq: list[Pos] = []
    u = finish_pos
    if prev.get(u) or u == start_pos:
        while u:
            seq.insert(0, u)
            if (has_prev := prev.get(u)): 
                u = has_prev.pos
    
    return seq

# traversal_path = get_traversal_path(cur_node.prev, [])
traversal_path = prev[finish_pos] 
# pprint.pprint(traversal_path)
for row_idx, row in enumerate(input):
    for col_idx, col in enumerate(row):
        print(f'{colored(col, 'green')} ' if Pos(row_idx, col_idx) in traversal_path else f'{col} ', end='')
    print()

#46

# row 2, col 10 - 35 vs 32
# pprint.pprint(dist)