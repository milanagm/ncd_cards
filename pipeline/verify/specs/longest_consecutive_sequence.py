"""Longest Consecutive Sequence."""
from ._gen import ints

METHOD = "longestConsecutive"
COMPARE = "exact"


def reference(nums):
    values, best = set(nums), 0
    for n in values:
        if n - 1 not in values:
            m = n
            while m + 1 in values:
                m += 1
            best = max(best, m - n + 1)
    return best


CASES = [
    ([2, 20, 4, 10, 3, 4, 5],), ([0, 3, 2, 5, 4, 6, 1, 1],), ([],), ([1],),
    ([9, 1, 4, 7, 3, -1, 0, 5, 8, -1, 6],), ([1, 2, 0, 1],), ([100, 4, 200, 1, 3, 2],), ([0, -1],), ([1, 3, 5],),
]


def random_case(rng):
    return (ints(rng, 0, 15, -10, 10),)
