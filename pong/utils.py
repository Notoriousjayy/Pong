# pong/utils.py

import math

def normalised(x, y):
    length = math.hypot(x, y)
    if length == 0:
        return 0, 0
    return x / length, y / length
