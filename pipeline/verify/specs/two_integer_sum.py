"""Two Integer Sum: indices of the unique pair summing to target, smaller index first."""
import itertools

from ._gen import ints

METHOD = "twoSum"
COMPARE = "exact"


def reference(nums, target):
    for i, j in itertools.combinations(range(len(nums)), 2):
        if nums[i] + nums[j] == target:
            return [i, j]


CASES = [
    ([3, 4, 5, 6], 7), ([4, 5, 6], 10), ([5, 5], 10), ([3, 2, 4], 6),
    ([1, 3, 4, 2], 6), ([2, 7, 11, 15], 9), ([-3, 4, 3, 90], 0), ([0, 4, 3, 0], 0),
]


def unique_pair_case(rng, sort=False):
    while True:
        nums = ints(rng, 2, 8, -9, 9)
        if sort:
            nums.sort()
        i, j = sorted(rng.sample(range(len(nums)), 2))
        target = nums[i] + nums[j]
        if sum(1 for a, b in itertools.combinations(nums, 2) if a + b == target) == 1:
            return (nums, target)


def random_case(rng):
    return unique_pair_case(rng)
