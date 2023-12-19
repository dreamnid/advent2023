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
bool_op = pp.one_of('> <')
filter_expr = pp.Word(pp.alphas) + bool_op + pp.Word(pp.nums) + ':' + pp.Word(pp.alphas) ^ pp.Word(pp.alphas)

workflows: dict[str, any] = {}
for line in get_file_contents(INPUT_FILE)[0]:
    filter_start = line.index('{')
    filters = [filter_expr.parse_string(cur_filter) for cur_filter in line[filter_start + 1: -1].split(',')]
    
    workflows[line[:filter_start]] = filters

# print(workflows)

accepted = []
item_filter = pp.Word(pp.alphas) + '=' + pp.Word(pp.nums)
for line in get_file_contents(INPUT_FILE)[1]:
    item = {item_filter.parse_string(cur_spec)[0]: int(item_filter.parse_string(cur_spec)[2]) for cur_spec in line[1:-1].split(',')}

    next_workflow_key = 'in'
    processing = True
    while processing:
        for cur_step in workflows[next_workflow_key]:
            field_val = None
            if len(cur_step) == 1:
                field_val = cur_step[0]
                if cur_step[0] == 'A':
                    accepted.append(item)
                    processing = False
                    break
                elif cur_step[0] == 'R':
                    processing = False
                    break
                else:
                    next_workflow_key = cur_step[0]
                    break
            else:
                field_spec, operator, value = cur_step[0], cur_step[1], int(cur_step[2])
                match operator:
                    case '>':
                        math_op = lambda x, y: x > y
                    case '<':
                        math_op = lambda x, y: x < y
                
                if math_op(item[field_spec], value):
                    field_val = cur_step[4] 
            
            if field_val:
                match field_val:
                    case 'A':
                        accepted.append(item)
                        processing = False 
                        break
                    case 'R':
                        processing = False
                        break
                    case _:
                        next_workflow_key = field_val 
                        break

print('1:', sum((sum(rating.values()) for rating in accepted)))
                            
        
                