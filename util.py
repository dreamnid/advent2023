import json
import time

def get_file_contents(file: str) -> list[list[str]]:
    """
    Process the input file

    Some of AoC puzzles formats the input file to use a blank line to designate a group.
    :param file: the name of the file
    :return:
    """
    with open(file) as fh:
        content = fh.read()
        return [block.strip().split('\n') for block in content.strip().split('\n\n')]


def find_var_parts_sum(input_list: list[int], desired_sum: int, num_addends=3, addends: list[int | None] = None, addend_idx=0) -> list[int] | None:
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


def deep_copy_json(myinput: str):
    # Uses json to deep copy
    return json.loads(json.dumps(myinput))


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


def get_neighbors(matrix, cur_row, cur_col):
    return [x[0] for x in get_neighbors_with_pos(matrix, cur_row, cur_col)]


def get_neighbors_with_pos(matrix, cur_row, cur_col):
    res = []

    num_rows = len(matrix)
    num_cols = len(matrix[0])
    # row on top
    if 0 < cur_row:
        if 0 < cur_col:
            res.append((matrix[cur_row-1][cur_col-1], (cur_row-1, cur_col-1)))
        res.append((matrix[cur_row-1][cur_col], (cur_row-1, cur_col)))
        if cur_col < num_cols-1:
            res.append((matrix[cur_row-1][cur_col+1], (cur_row-1, cur_col+1)))

    # same row
    if 0 < cur_col:
        res.append((matrix[cur_row][cur_col-1], (cur_row, cur_col-1)))
    if cur_col < num_cols-1:
        res.append((matrix[cur_row][cur_col+1], (cur_row, cur_col+1)))

    # row below
    if cur_row < num_rows-1:
        if 0 < cur_col:
            res.append((matrix[cur_row+1][cur_col-1], (cur_row+1, cur_col-1)))
        res.append((matrix[cur_row+1][cur_col], (cur_row+1, cur_col)))
        if cur_col < num_cols-1:
            res.append((matrix[cur_row+1][cur_col+1], (cur_row+1, cur_col+1)))

    return res


def add_padding(matrix, pad_value='.'): 
    """
    Surround the 2d array with the pad_value

    Helps with not worrying about boundaries
    """
    if isinstance(matrix[0], str):
        cur_res = [f'{pad_value}{matrix[i]}{pad_value}' for i in range(len(matrix))]
    else:
        cur_res = [[pad_value, *cur_row, pad_value] for cur_row in matrix]

    if not isinstance(pad_value, str):
        pad_value = [pad_value]

    row_pad = pad_value * len(cur_res[0])
    cur_res.insert(0, row_pad)
    cur_res.append(row_pad)
    return cur_res
