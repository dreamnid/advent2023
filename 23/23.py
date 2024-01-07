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
INPUT_FILE = "23a-example.txt"
# INPUT_FILE = "23b-example.txt"

input = [line for line in get_file_contents(INPUT_FILE)[0]]


class Pos(NamedTuple):
    row: int
    col: int


class Data(NamedTuple):
    cur_pos: Pos
    path: deque[Pos]


def next_node(cur_data: Data, next_pos: Pos, queue: deque[Data]):
    next_path = copy(cur_data.path)
    next_path.append(cur_data.cur_pos)
    queue.append(Data(next_pos, next_path))


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
    queue: deque[Data] = deque([Data(Pos(1, 1), deque([Pos(0, 1)]))])
    memo: dict[Pos, dict[Pos, int]] = defaultdict(lambda: defaultdict(int))
    memo_path: dict[Pos, dict[Pos, Iterable[Pos]]] = defaultdict(dict)
    splits: dict[Pos, int] = dict()
    bad_pos: set(Pos) = set()
    bad_path_pos: dict[Pos, set[Pos]] = defaultdict(set)
    bad_path_pos[Pos(131, 132)].add(Pos(131, 133))
    idx = 0

    while queue:
        idx += 1
        cur_data = queue.pop()
        path_len = len(cur_data.path)
        if cur_data.cur_pos in memo:
            pass
        if path_len and path_len < memo[cur_data.cur_pos][cur_data.path[-1]]:
            # print_puzzle(cur_data.path, cur_pos=cur_data.cur_pos)
            # print_puzzle(memo_path[cur_data.cur_pos], cur_pos=cur_data.cur_pos)
            compare_puzzle_paths(
                cur_data.path,
                memo_path[cur_data.cur_pos][cur_data.path[-1]],
                cur_pos=cur_data.cur_pos,
            )
            continue

        if path_len > 1 and cur_data.path[-1] in bad_path_pos[cur_data.cur_pos]:
            # This path leads to a dead end
            print("bad")
            continue

        cur_val = get_input_value(cur_data.cur_pos)
        if not is_slopes_slippery and cur_val in (">", "<", "v", "^"):
            cur_val = "."

        match cur_val:
            case ".":
                if cur_data.cur_pos == final_pos:
                    completed.append(cur_data)
                    print_puzzle(cur_data.path)
                    total_len = len(cur_data.path)
                    # Update memoization
                    prev_pos = None
                    last_split = None
                    for tmp_idx, tmp_pos in enumerate(cur_data.path, 0):
                        if tmp_idx == 0:
                            prev_pos = tmp_pos
                            continue
                        if tmp_pos in splits:
                            last_split = tmp_pos

                        if tmp_idx > memo[tmp_pos][prev_pos]:
                            memo[tmp_pos][prev_pos] = tmp_idx
                            memo_path[tmp_pos][prev_pos] = cur_data.path
                        prev_pos = tmp_pos

                    continue
                neighbors = [
                    cur_data.cur_pos._replace(row=cur_data.cur_pos.row - 1),
                    cur_data.cur_pos._replace(col=cur_data.cur_pos.col - 1),
                    cur_data.cur_pos._replace(row=cur_data.cur_pos.row + 1),
                    cur_data.cur_pos._replace(col=cur_data.cur_pos.col + 1),
                ]
            case ">":
                neighbors = [cur_data.cur_pos._replace(col=cur_data.cur_pos.col + 1)]
            case "<":
                neighbors = [cur_data.cur_pos._replace(col=cur_data.cur_pos.col - 1)]
            case "v":
                neighbors = [cur_data.cur_pos._replace(row=cur_data.cur_pos.row + 1)]
            case "^":
                neighbors = [cur_data.cur_pos._replace(row=cur_data.cur_pos.row - 1)]

        added_new_node = 0
        for cur_neighbor in neighbors:
            if (
                cur_neighbor not in cur_data.path
                and get_input_value(cur_neighbor) != "#"
            ):
                next_node(cur_data, cur_neighbor, queue)
                added_new_node += 1

        if added_new_node > 1:
            splits[cur_data.cur_pos] = added_new_node
        elif not added_new_node:
            # detect if deadend
            if len([val for val in map(get_input_value, neighbors) if val == "#"]) == 3:
                prev_pos = None
                for tmp_pos in reversed(cur_data.cur_pos):
                    if tmp_pos in splits:
                        bad_path_pos[prev_pos].add(tmp_pos)
                        break
                    prev_pos = tmp_pos
            # print_puzzle(cur_data.path, cur_data.cur_pos)
            for tmp_pos in reversed(cur_data.cur_pos):
                if tmp_pos in splits:
                    break
                bad_pos.add(cur_data.cur_pos)

        if idx % 200 == 0 and False:
            print(f"idx {idx}")
            print_puzzle(cur_data.path, cur_data.cur_pos)
    pprint.pprint(memo)
    return completed


# completed = sorted(list(solver()), key=lambda x: len(x.path), reverse=True)
# print([len(x.path) for x in completed])
# pprint.pprint(completed)
# print_puzzle(completed[0].path)
# print("1", len(completed[0].path))

completed = sorted(
    list(solver(is_slopes_slippery=False)), key=lambda x: len(x.path), reverse=True
)
print([len(x.path) for x in completed])
# pprint.pprint(completed)
print_puzzle(completed[0].path)
print("2", len(completed[0].path))
