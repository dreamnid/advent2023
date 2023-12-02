#!/usr/bin/env python3
from collections import defaultdict
from collections.abc import Callable, Collection, Iterable
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

INPUT_FILE='1-input.txt'
#INPUT_FILE='1a-example.txt'
#INPUT_FILE='1b-example.txt'

RE_DIGIT = re.compile(r'\d')

def convert_word_with_digit(mystr: str):
    """
    Return the numerical digit of the starting word

    E.g.
    two3eight will return '2' (the string)
    atwo3eight will return None
    """
    # assume mystr has the same casing
    trans_table = (('zero', '0'),
                   ('one', '1'),
                   ('two', '2'),
                   ('three', '3'),
                   ('four', '4'),
                   ('five', '5'),
                   ('six', '6'),
                   ('seven', '7'),
                   ('eight', '8'),
                   ('nine', '9'),
                  )

    for trans in trans_table:
        if mystr.startswith(trans[0]):
            return trans[1]

    return None


def get_calibration_values(parse_digits=False):
    nums = []
    for line in get_file_contents(INPUT_FILE)[0]:
        buf = ''
        for i, cur_char in enumerate(line):
            if parse_digits:
                if (word_to_digit := convert_word_with_digit(line[i:])):
                    cur_char = word_to_digit

            if RE_DIGIT.match(cur_char):
                buf += cur_char

        if len(buf) > 0:
            nums.append(int(buf[0]+buf[-1]))
    return nums

print('1:', sum(get_calibration_values()))
print('2:', sum(get_calibration_values(parse_digits=True)))
