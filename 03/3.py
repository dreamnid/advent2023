#!/usr/bin/env python3
from collections import defaultdict
from functools import partial, reduce
from itertools import chain, cycle, takewhile
import math
from operator import mul
import os
import pprint
import re
from time import time

from humanize import intcomma

# Fix path so we can do a relative import: https://stackoverflow.com/a/27876800
if __name__ == '__main__':
    if __package__ is None:
        import sys
        from os import path
        sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))

        # Relative imports here
        from util import *

INPUT_FILE='3-input.txt'
INPUT_FILE='3a-example.txt'

input = [line for line in get_file_contents(INPUT_FILE)[0]]