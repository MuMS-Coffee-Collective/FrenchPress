import sys
import random

current = map(float, sys.argv[1:])
maxes = [5.0, 5.0, 10.0]

new_vals = [0, 0, 0]
for i, vals in enumerate(zip(current, maxes)):
    current_val = vals[0]
    max_val = vals[1]
    new_vals[i] = int(current_val + (2 * random.random() * max_val - max_val))

print new_vals
