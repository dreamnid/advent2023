# Day 14

Part 2, I looked at the output until I detect it is looping and look at the seen_row_start value being printed out
I look for when the cycle repeats again, then subtract to get the cycle length.
Then use the following formula to calculate the index that you have calculated already: (1000000000 - `seen_row_start`) mod `cycle_length` + `seen_start`

Then look up the value in being referred to the calculated index

## Performance
```bash
(.venv) vscode ➜ /workspaces/2023/14 (main) $ time python 14.py
1: 108792

real    0m0.294s
user    0m0.464s
sys     0m1.392s

# part 2

Tried 99119 - answer too high

No timing since answer is calculated outside
```