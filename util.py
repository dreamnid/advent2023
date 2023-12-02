import json
import time
from typing import List, Union

def get_file_contents(file: str) -> List[List[str]]:
    """
    Process the input file

    Some of AoC puzzles formats the input file to use a blank line to designate a group.
    :param file: the name of the file
    :return:
    """
    with open(file) as fh:
        content = fh.read()
        return [block.strip().split('\n') for block in content.strip().split('\n\n')]

def find_var_parts_sum(input_list: List[int], desired_sum: int, num_addends=3, addends=None, addend_idx=0) -> Union[List[int], None]:
    """
    Find the combination of numbers in the input_list that adds up to desired_sum

    :param input_list: The *sorted* list of available numbers
    :param desired_sum: The target sum that the addends should add to
    :param num_addends: The desired number of addends that should add up to desired_sum. [e.g. 2 mean a+b, 3 means a+b+c, etc.]
    :param addends: private - buffer holding current result
    :param addend_idx: private - index of the addend list that is currently being worked on
    :return: The list of numbers that add up to the desired_sum or None if no solution found

    Note that this is a recursive call. Each recursion call works on the next addend hence why we pass
    the input_list without the first element and 1 is added to addend_idx
    """
    if not addends:
        # Using None as initial value to help assert if I'm doing something dumb later
        addends = [None] * num_addends

    if addend_idx == num_addends-1:
        # If we're looking at the last addend, we can calculate the last number needed instead of iterating through
        # the input_list
        input_set = set(input_list)
        cur_sum = sum(addends[:-1])
        desired_addend = desired_sum - cur_sum
        if desired_addend in input_set:
            addends[addend_idx] = desired_addend
            return addends

        return None

    for input in input_list:
        addends[addend_idx] = input

        if sum(addends[:addend_idx]) > desired_sum:
            # sum is too large, so don't need to recurse again since the rest of the list is bigger
            return None
        temp_res = find_var_parts_sum(input_list[1:], desired_sum, num_addends=num_addends, addends=addends, addend_idx=addend_idx+1)
        if temp_res:
            return temp_res

    if None not in addends and sum(addends) == desired_sum:
        return addends

    # Didn't find a result
    return None


def deep_copy_json(input):
    # Uses json to deep copy
    return json.loads(json.dumps(input))


class PrintTiming:
    """
    Context Manager that will time the context and print out the timing
    :return:
    """
    timer = None
    name = None

    def __init__(self, name: str | None = None):
        self.name = name

    def __enter__(self):
        self.timer = time()

    def __exit__(self, exc_type, exc_value, traceback):
        print('timer: ', time() - self.timer)