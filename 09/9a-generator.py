#!/usr/bin/env python3
from collections import defaultdict, deque
from functools import partial, reduce
from itertools import chain, cycle, pairwise, starmap, takewhile
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

INPUT_FILE='9-input.txt'
# INPUT_FILE='9a-example.txt'

input = [list(map(lambda x: int(x), line.split(' '))) for line in get_file_contents(INPUT_FILE)[0]]

## Inspiration from Kotlin: https://www.youtube.com/watch?v=wMjKUxW7g3o
def next_layer(layer):
    yield layer
    while any((a != 0 for a in layer)):
        # print('next_layer layer', layer)
        # Need to convert to list in order to get while condition working, not sure if there is a better way
        layer = list(b-a for a, b in pairwise(layer))
        yield layer 


def predict_next(cur_history):
    differences = (layer for layer in next_layer(cur_history))
    last_values = map(lambda cur_history: deque(cur_history, maxlen=1).pop(), differences)
    return sum(last_values)


print('1:', sum((predict_next(cur_history) for cur_history in input)))
