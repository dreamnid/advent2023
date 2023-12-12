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

INPUT_FILE='12-input.txt'
# INPUT_FILE='12a-example.txt'

input = [line for line in get_file_contents(INPUT_FILE)[0]]

res = []

for line_idx, line in enumerate(input):
    springs, report = line.split(' ')
    required_springs = sum((int(x) for x in report.split(',')))
    matcher = re.compile(r'\.*' + r'[.]+'.join(rf'#{{{x}}}' for x in report.split(',')) + r'(\.+$|$)')

    # broke_runs_loc: dict[int, list[int]] = defaultdict(list)
    # broke_buf = ''
    # q_runs_loc: dict[int, list[int]] = defaultdict(list)
    # q_buf = ''
    # for idx, cur_char in enumerate(line+''):
    #     match cur_char:
    #         case '#':
    #             broke_buf += '#'

    #             if (q_buf_len := len(q_buf)):
    #                 q_runs_loc[q_buf_len].append(idx - q_buf_len)
    #                 q_buf = ''
    #         case '?':
    #             q_buf += '?'

    #             if (broke_buf_len := len(broke_buf)):
    #                 broke_runs_loc[broke_buf_len].append(idx - broke_buf_len)
    #             broke_buf = ''
    #         case _:
    #             if (broke_buf_len := len(broke_buf)):
    #                 broke_runs_loc[broke_buf_len].append(idx - broke_buf_len)
    #             broke_buf = ''

    #             if (q_buf_len := len(q_buf)):
    #                 q_runs_loc[q_buf_len].append(idx - q_buf_len)
    #             q_buf = ''

    in_progress_combos = []
    for idx, cur_char in enumerate(springs+''):
        if cur_char == '?':
            if not in_progress_combos:
                in_progress_combos = [springs[:idx]]
            new_springs = []
            for cur_springs in in_progress_combos:
                new_springs.append(cur_springs + '.')
                new_springs.append(cur_springs + '#')
            in_progress_combos = new_springs
        else:
            in_progress_combos = [f'{cur_springs}{cur_char}' for cur_springs in in_progress_combos]

    valid = [cur_springs for cur_springs in filter(lambda x: len(x) >= len(springs), in_progress_combos) if matcher.match(cur_springs)]
    # print(line_idx, 'valid', valid)
    # print('in_progress', in_progress_combos)
    res.append(len(valid))

    if line_idx == 5 and False:
        # pprint.pprint([cur_springs for cur_springs in filter(lambda x: len(x) >= len(springs), in_progress_combos)])
        # print(matcher.search('.#.#..###'))
        # print(springs, report, matcher, len(valid)) 
        # pprint.pprint(valid)

        break
    # print(springs, report, matcher, len(valid)) 
    # pprint.pprint(q_runs_loc)
    # pprint.pprint(broke_runs_loc)

print('1:', sum(res))