"""Koko Eating Bananas: smallest speed k that finishes all piles within h hours."""
from ._gen import ints

METHOD = "minEatingSpeed"
COMPARE = "exact"


def hours(piles, k):
    return sum((p + k - 1) // k for p in piles)


def reference(piles, h):
    lo, hi = 1, max(piles)
    while lo < hi:
        k = (lo + hi) // 2
        if hours(piles, k) <= h:
            hi = k
        else:
            lo = k + 1
    return lo


CASES = [
    ([1, 4, 3, 2], 9), ([25, 10, 23, 4], 4), ([3, 6, 7, 11], 8), ([30, 11, 23, 4, 20], 5),
    ([30, 11, 23, 4, 20], 6), ([1], 1), ([5], 10), ([312884470], 312884469),
    ([1000000000], 2), ([1000000000, 1000000000], 3),
]


def random_case(rng):
    piles = ints(rng, 1, 8, 1, 30)
    return (piles, rng.randint(len(piles), 3 * sum(piles) // 2 + 1))
