"""Contains Duplicate."""
from ._gen import ints

METHOD = "hasDuplicate"
COMPARE = "exact"


def reference(nums):
    return len(set(nums)) != len(nums)


CASES = [([1, 2, 3, 3],), ([1, 2, 3, 4],), ([1],), ([1, 1],), ([3, 1, 3],), ([0, -1, -1, 5],)]


def random_case(rng):
    return (ints(rng, 1, 10, 0, 12),)
