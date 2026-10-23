"""Two Integer Sum II: sorted input, 1-indexed answer, O(1) extra space required (not checked here)."""
from .two_integer_sum import reference as zero_based, unique_pair_case

METHOD = "twoSum"
COMPARE = "exact"


def reference(numbers, target):
    i, j = zero_based(numbers, target)
    return [i + 1, j + 1]


CASES = [
    ([1, 2, 3, 4], 3), ([2, 7, 11, 15], 9), ([2, 3, 4], 6), ([-1, 0], -1),
    ([1, 1, 3], 2), ([0, 0, 3, 4], 0), ([-5, -3, 0, 2, 4, 6, 8], 5),
]


def random_case(rng):
    return unique_pair_case(rng, sort=True)
