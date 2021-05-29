import math
from functools import reduce

def _lcm(a,b): return int(abs(a * b) / math.gcd(a,b)) if a and b else 0

def lcm(a):
    return reduce(_lcm, a)