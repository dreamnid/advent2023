#!/usr/bin/env python3

import argparse
import os
from pathlib import Path
import requests
import sys

if os.path.isfile(os.path.join(os.path.dirname(__file__), 'settings.py')):
    from settings import *
else:
    AOC_SESSION_COOKIE = None

parser = argparse.ArgumentParser(description='Create a level')
parser.add_argument('level', type=int)

args = parser.parse_args()

level = args.level
level_name = '%02d' % level

try:
    os.mkdir(level_name)
    print(f'Created: "{level_name}" directory')
except OSError:
    pass

script_file = os.path.join(level_name, '{}.py'.format(level))

# Safe guard that we don't accidentally write over good code
if os.path.isfile(script_file):
    print('Error - file exists')
    sys.exit(1)

with open(script_file, 'w') as fh:
    template_vars = {
        'level' : level,
    }

    with open('level.py.tmpl') as tmpl_fh:
        contents = tmpl_fh.read().format(**template_vars)

    fh.write(contents)

os.chmod(script_file, 0o755)
print(f'Created: {script_file}')

# Create README
readme_file = os.path.join(level_name, 'README.md')
with open(readme_file, 'w') as fh:
    template_vars = {
        'level' : level,
    }

    with open('README.md.tmpl') as tmpl_fh:
        contents = tmpl_fh.read().format(**template_vars)

    fh.write(contents)
print(f'Created: {readme_file}')

# Create empty example input file
Path(os.path.join(level_name, '{}a-example.txt'.format(level))).touch()
print(f'Created dummy input files')
# Create empty example input file

Path(os.path.join(level_name, 'puzzle.txt')).touch()

if AOC_SESSION_COOKIE:
    response = requests.get(f'https://adventofcode.com/{AOC_YEAR}/day/{level}/input', cookies={'session': AOC_SESSION_COOKIE})
    if response.status_code == 200:
        with open(os.path.join(level_name, f'{level}-input.txt'), 'w') as fh:
            fh.write(response.text)
    print('Level input file downloaded')
else:
    print('AOC_SESSION_COOKIE not defined, so can\'t auto download input file')
    print('This can be found while logged into the AoC website using the browser development console. Need the value of the session cookie')

print('Finished!')