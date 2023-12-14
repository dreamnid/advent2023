# Day 14

Part 2, I looked at the output until I detect it is looping and look at the seen_row_start value being printed out
I look for when the cycle repeats again, then subtract to get the cycle length.
Then use the following formula to calculate the index that you have calculated already: (1000000000 - `seen_row_start`) mod `cycle_length` + `seen_start`

Then look up the value in being referred to the calculated index.

For part b, I saw that `seen_row_start` is 154 whose result is 99146
The next time that 99146 appears again and we confirmed the cycle starts over is 226
226 - 154 = 72 which is the cycle length
(1000000000 - 154) = 999999846 mode 72 = 54
154 + 54 = 208 whose value is *99118*

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

# part 2 with cycle detection
(.venv) vscode ➜ /workspaces/2023/14 (main) $ time python 14.py
1: 108792
2: 99118

real    4m35.543s
user    4m35.679s
sys     0m1.472s
```