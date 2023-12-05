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

INPUT_FILE='5-input.txt'
#INPUT_FILE='5a-example.txt'

input = get_file_contents(INPUT_FILE)
seeds = [int(seed) for seed in input[0][0].split(': ')[1].split(' ')]
seed_pairs = sorted(list(zip(seeds[::2], seeds[1::2])), key=lambda x: x[0])


def in_range(target, start, size):
    return start <= target < start+size


def get_mapper(cur_input):
    input_split = [x.split(' ') for x in cur_input]
    return sorted([[int(dest), int(src), int(size)] for dest, src, size in input_split], key=itemgetter(1))


def remap_range(mappings, range):
    res = []
    no_overlap = [range]

    for dest, src, len in mappings:
        overlap = calc_overlap((src, src+len-1), range)
        if overlap is None:
            continue
        offset = overlap[0] - src
        overlap_size = overlap[1] - overlap[0]
        res.append([dest + offset, dest + offset + overlap_size])

        # Totally covers, so do early return
        if overlap[0] <= no_overlap[-1][0] and no_overlap[-1][1] <= overlap[1]:
            return res

        # overlap doesn't cover the beginning
        elif no_overlap[-1][0] < overlap[0] and no_overlap[-1][1] <= overlap[1]:
            no_overlap[-1][1] = overlap[0] - 1

        # overlap doesn't cover the end
        elif overlap[0] <= no_overlap[-1][0] and overlap[1] < no_overlap[-1][1]:
            no_overlap[-1][0] = overlap[1] + 1
        
        # overlap doesn't cover beginning and end
        elif no_overlap[-1][0] < overlap[0] and overlap[1] < no_overlap[-1][1]:
            no_overlap[-1][1] = overlap[0] - 1
            no_overlap.append((overlap[1] + 1, range[1]))

    res.extend(no_overlap)
    return res


def calc_overlap(range1, range2):
    range1_start, range1_end = range1
    range2_start, range2_end = range2
    if range2_start > range1_start:
        temp_range1_start, temp_range1_end = range1_start, range1_end
        temp_range2_start, temp_range2_end = range2_start, range2_end
    else:
        temp_range1_start, temp_range1_end = range2_start, range2_end
        temp_range2_start, temp_range2_end = range1_start, range1_end

    if temp_range1_start <= temp_range2_start <= temp_range1_end:
        return temp_range2_start, min(temp_range1_end, temp_range2_end)

# Load the seeds into the ranges
ranges = [[seed_start, seed_start+seed_size-1] for seed_start, seed_size in seed_pairs]

for i in range(1, len(input)):
    # Start idx at 1 since idx 0 are the seeds
    cur_mapping = get_mapper(input[i][1:])
    ranges = list(chain(*[remap_range(cur_mapping, cur_range) for cur_range in ranges]))
print('2: ', sorted(ranges, key=itemgetter(0))[0][0])
