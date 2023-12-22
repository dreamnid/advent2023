# Day 22

Spent a long time with part 1 trying to work out issues
1. Didn't realize blocks can be diagonal in the x,y axis
2. When determining if the block supports any other block, I was looking at the top of the stack in the Z-axis

## Performance
```bash
# part 1
(.venv) vscode ➜ /workspaces/2023/22 (main) $ time python 22.py 
1: 428

real    0m0.293s
user    0m0.524s
sys     0m1.434s
```