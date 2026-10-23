"""Product of Array Except Self."""
import math

from ._gen import ints

METHOD = "productExceptSelf"
COMPARE = "exact"


def reference(nums):
    return [math.prod(nums[:i] + nums[i + 1:]) for i in range(len(nums))]


CASES = [([1, 2, 4, 6],), ([-1, 0, 1, 2, 3],), ([2, 3],), ([0, 0],), ([1, 0],), ([5, 1, 1, 1],)]


def random_case(rng):
    return (ints(rng, 2, 8, -3, 3),)
