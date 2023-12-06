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

INPUT_FILE='6-input.txt'
INPUT_FILE='6a-example.txt'

input = [line for line in get_file_contents(INPUT_FILE)[0]]

overall_time = int(input[0].split(':')[1].replace(' ', ''))
overall_distance = int(input[1].split(':')[1].replace(' ', ''))

# Find the roots via quadratic formula
#(t +- sqrt(t**2 - 4d))/2
sqrt_discriminent = math.sqrt(overall_time**2 - 4*overall_distance)
start = math.ceil((overall_time - sqrt_discriminent) / 2)
end = math.ceil((overall_time + sqrt_discriminent) / 2)

print('2: ', end - start)
