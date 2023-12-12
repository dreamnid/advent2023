#!/usr/bin/env python3
from collections import defaultdict
from collections.abc import Sequence
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

INPUT_FILE='12-input.txt'
# INPUT_FILE='12a-example.txt'

input = [line for line in get_file_contents(INPUT_FILE)[0]]

res = []
expand = True 


def solver(springs: Sequence[str], report: Sequence[int], springs_idx: int, report_part_idx, memo):
    memo_key = (springs_idx, report_part_idx)
    if memo_key in memo:
        return memo[memo_key]

    if report_part_idx == len(report):
        # Ensure the rest of the springs are operational
        return 0 if any((cur_spring == '#' for cur_spring in springs[springs_idx:])) else 1

    if springs_idx == len(springs):
        return 0

    springs_required = report[report_part_idx]
    
    if len(springs) < springs_idx + springs_required:
        return 0

    # print([springs[i] for i in range(springs_idx, springs_idx+springs_required)])
    satisfy_report_part = not any((springs[i] == '.' for i in range(springs_idx, springs_idx+springs_required)))

    # Make sure we're at the end of string or there can be an operational spring afterwards
    if len(springs) != springs_idx + springs_required and springs[springs_idx + springs_required] == '#':
        satisfy_report_part = False

    take_total = 0
    if satisfy_report_part:
        # Note the plus 1 because we're assuming there is a period after
        take_total = solver(springs, report, springs_idx + springs_required + 1, report_part_idx + 1, memo)

    leave_total = 0

    if springs[springs_idx] in ['.', '?']:
        leave_total = solver(springs, report, springs_idx + 1, report_part_idx, memo)
    
    memo[memo_key] = take_total + leave_total
    return memo[memo_key]



for line_idx, line in enumerate(input):
    springs, report = line.split(' ')
    if expand:
        springs = '?'.join([springs] * 5)
        report = ','.join([report] * 5)
        # print(springs, report)
    report = list(int(x) for x in report.split(','))

    res.append(solver(springs, report, 0, 0, {}))

# pprint.pprint(res)
print('1:', sum(res))