#!/usr/bin/env python3
from __future__ import annotations
from collections import Counter, defaultdict, deque
from collections.abc import Callable, Collection, Container, Iterable, Sequence
from copy import copy
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
from termcolor import colored, cprint

# Fix path so we can do a relative import: https://stackoverflow.com/a/27876800
if __name__ == "__main__":
    if not __package__:
        import sys
        from os import path

        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

        # Relative imports here
        from util import *

INPUT_FILE = "23-input.txt"
# INPUT_FILE = "23a-example.txt"
# INPUT_FILE = "23b-example.txt"
# INPUT_FILE = "23c-example.txt"

input = [line for line in get_file_contents(INPUT_FILE)[0]]


class Pos(NamedTuple):
    row: int
    col: int


Path = deque[Pos]


class Data(NamedTuple):
    pos: Pos
    path: Path
    last_split_path: Path


class Junction(NamedTuple):
    paths: deque[Path]
    final_path: deque[Path] | None = None


def next_node(
    cur_data: Data, next_pos: Pos, next_last_split_path: Path, queue: deque[Data]
):
    next_path = copy(cur_data.path)
    next_path.append(cur_data.pos)
    queue.append(Data(next_pos, next_path, next_last_split_path))


def next_junction(cur_data: Data, path_segment: Path, queue: deque[Data]):
    # print("next junction", f"pos: {cur_data.pos}", f"path: {path_segment}")
    next_path = copy(cur_data.path) + path_segment
    # compare_puzzle_paths(path_segment, cur_data.path, cur_data.pos)
    queue.append(Data(path_segment[-1], next_path, None))
    pass


def get_input_value(cur_pos: Pos):
    return input[cur_pos.row][cur_pos.col]


def print_puzzle(path: Container[Pos], cur_pos: Pos | None = None):
    for row_idx, row in enumerate(input):
        print_puzzle_row(path, row_idx, row, cur_pos)
        print()
    print()


def compare_puzzle_paths(
    path1: Container[Pos], path2: Container[Pos], cur_pos: Pos | None = None
):
    for row_idx, row in enumerate(input):
        print_puzzle_row(path1, row_idx, row, cur_pos)
        print(" " * 4, end="")
        print_puzzle_row(path2, row_idx, row, cur_pos)
        print()
    print()


def print_puzzle_row(
    path: Container[Pos], row_idx: int, row: Iterable, cur_pos: Pos | None = None
):
    for col_idx, col in enumerate(row):
        if cur_pos and Pos(row_idx, col_idx) == cur_pos:
            print(f"{colored('X', 'red')}", end="")
        elif Pos(row_idx, col_idx) in path:
            print(f"{colored('O', 'green')}", end="")
        else:
            print(col, end="")


final_pos = Pos(len(input) - 1, len(input[0]) - 2)
assert get_input_value(final_pos) == "."


def solver(is_slopes_slippery=True):
    """
    Set is_slopes_slippey to True for part 1
    """
    completed: deque[Data] = deque()
    queue: deque[Data] = deque([Data(Pos(1, 1), deque([Pos(0, 1)]), None)])
    junctions: dict[Pos, Junction] = dict()
    # paths: dict[Pos, Path] = dict()
    bad_pos: set(Pos) = set()
    bad_path_pos: dict[Pos, set[Pos]] = defaultdict(set)
    start_path_to_first_junction: deque[Path] = deque([Pos(0, 1)])
    first_junction_pos: Pos | None = None
    idx = 0

    # Build data structure via bfs
    while queue:
        idx += 1
        cur_data = queue.popleft()
        cur_pos = cur_data.pos

        cur_val = get_input_value(cur_pos)
        if not is_slopes_slippery and cur_val in (">", "<", "v", "^"):
            cur_val = "."

        match cur_val:
            case ".":
                if cur_pos == final_pos:
                    # completed.append(cur_data)
                    last_junction = cur_data.last_split_path.popleft()
                    junctions[last_junction] = junctions[last_junction]._replace(
                        final_path=cur_data.last_split_path
                    )
                    # print_puzzle(cur_data.path)
                    continue
                elif cur_pos in junctions:
                    # We've been to this junction before
                    if cur_data.last_split_path:
                        cur_data.last_split_path.append(cur_pos)
                        cur_data.last_split_path.popleft()
                    continue
                neighbors = [
                    cur_pos._replace(row=cur_pos.row - 1),
                    cur_pos._replace(col=cur_pos.col - 1),
                    cur_pos._replace(row=cur_pos.row + 1),
                    cur_pos._replace(col=cur_pos.col + 1),
                ]
            case ">":
                neighbors = [cur_data.cur_pos._replace(col=cur_pos.col + 1)]
            case "<":
                neighbors = [cur_data.cur_pos._replace(col=cur_pos.col - 1)]
            case "v":
                neighbors = [cur_data.cur_pos._replace(row=cur_pos.row + 1)]
            case "^":
                neighbors = [cur_data.cur_pos._replace(row=cur_pos.row - 1)]

        valid_neighbors = [
            cur_neighbor
            for cur_neighbor in neighbors
            if (
                (
                    (
                        cur_data.last_split_path
                        and cur_neighbor not in cur_data.last_split_path
                    )
                    or not cur_data.last_split_path
                )
                and get_input_value(cur_neighbor) != "#"
            )
        ]
        match len(valid_neighbors):
            case 0:
                # detect if deadend
                if (
                    len([val for val in map(get_input_value, neighbors) if val == "#"])
                    == 3
                ):
                    prev_pos = None
                    for tmp_pos in reversed(cur_pos):
                        if tmp_pos in junctions:
                            bad_path_pos[prev_pos].add(tmp_pos)
                            break
                        prev_pos = tmp_pos
                    cur_data.last_split_path.clear()
                    # print_puzzle(cur_data.path, cur_data.cur_pos)
                    for tmp_pos in reversed(cur_pos):
                        if tmp_pos in junctions:
                            break
                        bad_pos.add(cur_pos)
                continue
            case 1:
                if cur_data.last_split_path:
                    cur_data.last_split_path.append(cur_pos)
                else:
                    start_path_to_first_junction.append(cur_pos)
                next_node(cur_data, valid_neighbors[0], cur_data.last_split_path, queue)
            case _:
                # New Junction
                cur_junction = Junction(paths=deque())
                junctions[cur_pos] = cur_junction
                if not first_junction_pos:
                    first_junction_pos = cur_pos
                    start_path_to_first_junction.append(cur_pos)
                # Add recipricol path
                if cur_data.last_split_path:
                    tmp_path = copy(cur_data.last_split_path)
                    cur_junction.paths.append(deque(reversed(tmp_path)))
                    cur_data.last_split_path.append(cur_pos)
                    cur_data.last_split_path.popleft()

                # Add remaining paths
                for cur_neighbor in valid_neighbors:
                    new_path = deque([cur_pos])
                    cur_junction.paths.append(new_path)
                    next_node(cur_data, cur_neighbor, new_path, queue)

        if idx % 1 == 0 and False:
            print(f"idx {idx}")
            print_puzzle(cur_data.path, cur_pos)

    if False:
        for junc_pos, junction in junctions.items():
            print(f"junc_pos {junc_pos} ")
            pprint.pprint(junction.paths)
    print("Finished creating graph")
    print("*" * 80)

    # Traverse segments via dfs to get longest path
    queue: deque[Data] = deque(
        [Data(first_junction_pos, start_path_to_first_junction, None)]
    )
    idx = 0
    while queue:
        idx += 1
        cur_data = queue.pop()
        cur_pos = cur_data.pos
        # print('cur_pos', cur_pos, 'cur_path', cur_data.path)

        if junctions[cur_pos].final_path:
            cur_data.path.extend(junctions[cur_pos].final_path)
            completed.append(cur_data)
            continue

        for junction_path in junctions[cur_pos].paths:
            if not junction_path:
                continue
            if junction_path[-1] in cur_data.path:
                continue
            next_junction(cur_data, junction_path, queue)

        if idx % 1 == 0 and False:
            print(f"idx {idx}")
            print_puzzle(cur_data.path, cur_pos)

    # pprint.pprint(junctions[Pos(1, 1)].paths)
    # pprint.pprint(junctions[Pos(1, 1)].paths)
    print("*" * 30)
    # pprint.pprint(junctions[Pos(3, 2)].paths)
    # pprint.pprint(junctions[Pos(5, 3)].final_path)
    return completed


# completed = sorted(list(solver()), key=lambda x: len(x.path), reverse=True)
# print([len(x.path) for x in completed])
# pprint.pprint(completed)
# print_puzzle(completed[0].path)
# print("1", len(completed[0].path))

completed = sorted(
    list(solver(is_slopes_slippery=False)), key=lambda x: len(x.path), reverse=True
)
# print([len(x.path) for x in completed])
# for cur_complete in completed:
    # pprint.pprint(cur_complete.path)
# print_puzzle(completed[0].path)
# print('completed[0]')
# pprint.pprint(completed[0].path)
print("2", len(completed[0].path))
