"""Binary Search: index of target in a sorted list of distinct ints, -1 if missing."""
METHOD = "search"
COMPARE = "exact"


def reference(nums, target):
    return nums.index(target) if target in nums else -1


CASES = [
    ([-1, 0, 2, 4, 6, 8], 4), ([-1, 0, 2, 4, 6, 8], 3), ([5], 5), ([5], -5), ([1, 2], 1), ([1, 2], 2),
    ([1, 3, 5, 7, 9], 1), ([1, 3, 5, 7, 9], 9), ([1, 3, 5, 7, 9], 10), ([1, 3, 5, 7, 9], 0),
    (list(range(-9999, 9999, 3)), 9996),
]


def random_case(rng):
    nums = sorted(rng.sample(range(-50, 50), rng.randint(1, 12)))
    target = rng.choice(nums) if rng.random() < 0.6 else rng.randint(-51, 51)
    return (nums, target)
