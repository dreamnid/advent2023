# Day 13

Originally I thought you had to look for the spot which gives you the highest depth
(i.e the count of how rows/columns were reflected) but was coming across cases
that the mirror had mutiple points with the same depth.

kkevinchou pointed out that one side of the reflection must run to the end of the maze.

## Performance
```bash
# part 1
(.venv) vscode ➜ /workspaces/2023/13 (main) $ time python 13.py
1: 34993

real    0m0.279s
user    0m0.497s
sys     0m1.422s

# part 1 + 2
(.venv) vscode ➜ /workspaces/2023/13 (main) $ time python 13.py
1: 34993
2: 29341

real    0m0.276s
user    0m0.476s
sys     0m1.423s
```