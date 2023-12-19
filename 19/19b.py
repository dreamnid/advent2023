#!/usr/bin/env python3
from collections import defaultdict, deque
from collections.abc import Callable
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
import pyparsing as pp

# Fix path so we can do a relative import: https://stackoverflow.com/a/27876800
if __name__ == '__main__':
    if not __package__:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

        # Relative imports here
        from util import *

INPUT_FILE='19-input.txt'
# INPUT_FILE='19a-example.txt'

input = [line for line in get_file_contents(INPUT_FILE)[0]]

@dataclass
class Range:
    start: int = 1
    end: int = 4000


class Predicate(NamedTuple):
    field: str
    compare_op: Callable[[int, int], bool]
    value: int 

    def __repr__(self):
        match self.compare_op.__name__:
            case 'gt':
                op_str = '>'
            case 'ge':
                op_str = '>='
            case 'lt':
                op_str = '<'
            case 'le':
                op_str = '<='
            case _:
                raise ValueError(self.compare_op.__name__)
        return f'{self.field} {op_str} {self.value}'


class History(NamedTuple):
    next_workflow: str
    path: list[str] = []
    """list of path"""
    predicates: list[Predicate] = []
    """list of predicates"""


def parse_op(s):
    match s[0]:
        case '>':
            return gt
        case '<':
            return lt

# pyparsing schemas
bool_op = pp.one_of('> <').setParseAction(parse_op)
filter_expr = pp.Word(pp.alphas) + bool_op + pp.Word(pp.nums).setParseAction(lambda s: int(s[0])) + ':' + pp.Word(pp.alphas) ^ pp.Word(pp.alphas)

# Get the workspaces definitions
workflows: dict[str, any] = {}
for line in get_file_contents(INPUT_FILE)[0]:
    filter_start = line.index('{')
    filters = [filter_expr.parse_string(cur_filter) for cur_filter in line[filter_start + 1: -1].split(',')]
    workflow_name = line[:filter_start] 
    workflows[workflow_name] = filters

# Find all paths that leads to an accepted state
q = deque([History('in', ['in'])])
history_with_accept: list[History] = []

while q:
    cur_path = q.popleft()

    workflow_name = cur_path.next_workflow
    cur_workflow = workflows[workflow_name]
    prev_predicates: list[Predicate] = []
    for cur_step in cur_workflow:
        if len(cur_step) == 1:
            if cur_step[0] == 'A':
                history_with_accept.append(History(None, cur_path.path, cur_path.predicates + prev_predicates))
            elif cur_step[0] == 'R':
                pass
            else:
                q.append(History(cur_step[0], cur_path.path + [cur_step[0]], cur_path.predicates + prev_predicates))
        else:
            field_spec, math_comp, value, _, next_workflow = cur_step
            new_predicate = Predicate(field_spec, math_comp, value)
            match next_workflow:
                case 'A':
                    history_with_accept.append(History(None, cur_path.path, cur_path.predicates + [*prev_predicates, new_predicate]))
                case 'R':
                    pass
                case _:
                    q.append(History(next_workflow, cur_path.path + [next_workflow], cur_path.predicates + [*prev_predicates, new_predicate]))
            
            match math_comp.__name__:
                case 'lt':
                    neg_op = ge
                case 'gt':
                    neg_op = le
                # Don't need other cases as input only has > and <
            # Track the predicates that lead to this point. Note that we negate the comparison 
            # since if we did do this predicate, it would bail out to the next workflow
            prev_predicates.append(Predicate(field_spec, neg_op, value))

# pprint.pprint([(i, cur_hist.path) for i, cur_hist in enumerate(history_with_accept)])
# pprint.pprint([(i, cur_hist.predicates) for i, cur_hist in enumerate(history_with_accept)])

# Process the predicates in each accepted path
acc = []
for cur_history in history_with_accept:
    ranges = {'m': Range(), 's': Range(), 'a': Range(), 'x': Range()}

    for cur_pred in cur_history.predicates:
        match cur_pred.compare_op.__name__:
            case 'lt':
                ranges[cur_pred.field].end = cur_pred.value - 1
            case 'le':
                ranges[cur_pred.field].end = cur_pred.value
            case 'gt':
                ranges[cur_pred.field].start = cur_pred.value + 1
            case 'ge':
                ranges[cur_pred.field].start = cur_pred.value

    # print(ranges)
    acc.append(reduce(mul, map(lambda x: x.end - x.start + 1, ranges.values())))

print('2:', sum(acc))
