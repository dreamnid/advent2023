# Day 18

Part 1 - I cheated by manually selecting where to fill

Part 2 - The main issue is we have ranges for left/right but not up/down.
           We can potentially optimize by copying the fill_range_count during the up/down steps 
## Performance
```bash
# Part 1
@dreamnid ➜ /workspaces/advent2023/18 (main) $ time python 18.py
1: 40761

real    0m0.296s
user    0m0.277s
sys     0m0.012s

# Part 2 (attempt 1)
(.venv) vscode ➜ /workspaces/2023/18 (main) $ time python 18b.py
populated count: 167690176
2: 106920098354636

real    3m3.031s
user    2m55.903s
sys     0m7.116s
```