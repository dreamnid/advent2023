#!/usr/bin/env python3
from collections import defaultdict, Counter
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

INPUT_FILE='7-input.txt'
# INPUT_FILE='7a-example.txt'

input = [line for line in get_file_contents(INPUT_FILE)[0]]


def get_hand_type(cards, joker=False):
    c = Counter(cards)
    counts = c.values()
    if joker:
        # Jokers can be any card to makes the highest hand
        count_jokers = c['J']
        if count_jokers == 5:
            return 6

        filtered_cards = [card for card in cards if card != 'J']
        counts = sorted(list(Counter(filtered_cards).values()))
        # Add the joker count to the highest count
        counts[-1] += count_jokers
        # print('j new counts', counts)
    if 5 in counts:
        return 6
    elif 4 in counts:
        return 5
    elif 3 in counts and 2 in counts:
        return 4
    elif 3 in counts:
        return 3
    elif 2 in counts:
        num_pairs = Counter(counts).values()
        if 2 in num_pairs:
            # 2 pair
            return 2
        else:
            return 1
    else:
        return 0

# print('hand_type', get_hand_type(['1', '3', 'J', 'J', '3'], joker=True))
# print('hand_type', get_hand_type(['Q', 'J', 'J', 'J', 'J'], joker=True))

def card_value(card: str, joker=False):
    match card:
        case 'A':
            return 14
        case 'K':
            return 13
        case 'Q':
            return 12
        case 'J':
            if joker:
                # Jokers are the lowest value card
                return 0
            return 11
        case 'T':
            return 10
        case _:
            return int(card)

players = []
for x in input:
    cards, bids = x.split(' ')
    bids = int(bids)
    cards = [card for card in cards]

    players.append((cards, int(bids),))


players.sort(key=lambda x: (get_hand_type(x[0]), card_value(x[0][0]), card_value(x[0][1]), card_value(x[0][2]), card_value(x[0][3]), card_value(x[0][4])))
res = 0
for rank, player in enumerate(players, start=1):
    res += rank * player[1]

print('1:', res)

players.sort(key=lambda x: (get_hand_type(x[0], joker=True), card_value(x[0][0], joker=True), card_value(x[0][1], joker=True), card_value(x[0][2], joker=True), card_value(x[0][3], joker=True), card_value(x[0][4], joker=True)))
res = 0
for rank, player in enumerate(players, start=1):
    res += rank * player[1]

# pprint.pprint(players)
print('2:', res)
