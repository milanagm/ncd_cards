"""3Sum: all unique triplets summing to zero."""
import itertools

from ._gen import ints

METHOD = "threeSum"
COMPARE = "groups"


def reference(nums):
    return sorted({tuple(sorted(c)) for c in itertools.combinations(nums, 3) if sum(c) == 0})


CASES = [
    ([-1, 0, 1, 2, -1, -4],), ([0, 1, 1],), ([0, 0, 0],), ([0, 0, 0, 0],), ([-2, 0, 1, 1, 2],),
    ([1, -1, -1, 0],), ([-4, -2, -2, -2, 0, 1, 2, 2, 2, 3, 3, 4, 4, 6, 6],),
    ([7, 7, -3, -1, 0, 1],),  # duplicate check against the unsorted list skips the -1
    ([3, -2, 1, 0],), ([-1, 0, 1, 0],),
]


def random_case(rng):
    return (ints(rng, 3, 12, -5, 5),)
