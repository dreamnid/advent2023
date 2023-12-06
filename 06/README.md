# Day 6

Brute forced the 2nd part

## Performance
```bash
(.venv) @dreamnid ➜ /workspaces/advent2023/06 (main) $ time python 6a.py
1:  5133600

real    0m0.079s
user    0m0.055s
sys     0m0.024s

(.venv) @dreamnid ➜ /workspaces/advent2023/06 (main) $ time python 6b.py
2:  40651271

real    0m9.564s
user    0m9.427s
sys     0m0.024s

(.venv) @dreamnid ➜ /workspaces/advent2023/06 (main) $ time python 6b2.py
2:  71503

real    0m0.080s
user    0m0.063s
sys     0m0.016s
```

Scratch
```
n * (t-n) - d > 0
nt - n^2 - d
n^2 -tn + d

quadratic formula:
a = 1, b=-t, c=d
t +- sqrt(t**2 - 4d)/2
```
