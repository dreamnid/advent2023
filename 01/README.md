# Day 1

## Issues encountered
### Common letters
I thought it wanted to prioritize the first digit word

But actually, common letters can be for either case.

### Lines with fewer than 2 numbers
The puzzle clearly states the calibration value is 2 digits, but does not clarify if the line only contains 1 numerical value. 
Apparently, if there is only one number, it should be used twice.

## Tricky test cases

```
1eightwo -> 12
beightwo4 -> 84
```


## Performance
```bash
(adventofcode) ➜  01 git:(main) ✗ time python 1.py 
1: 56049
2: 54530
python 1.py  0.05s user 0.01s system 98% cpu 0.063 total
```