"""Daily Temperatures: days until a warmer temperature, 0 if none."""
from ._gen import ints

METHOD = "dailyTemperatures"
COMPARE = "exact"


def reference(temperatures):
    n = len(temperatures)
    return [next((j - i for j in range(i + 1, n) if temperatures[j] > temperatures[i]), 0) for i in range(n)]


CASES = [
    ([30, 38, 30, 36, 35, 40, 28],), ([22, 21, 20],), ([1],), ([73, 74, 75, 71, 69, 72, 76, 73],),
    ([30, 30, 31],), ([50, 40, 30, 60],), ([100, 1, 100],),
]


def random_case(rng):
    return (ints(rng, 1, 10, 1, 8),)
