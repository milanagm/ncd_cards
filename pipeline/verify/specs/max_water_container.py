"""Container With Most Water: max (j - i) * min(h[i], h[j])."""
from ._gen import ints

METHOD = "maxArea"
COMPARE = "exact"


def reference(heights):
    n = len(heights)
    return max((j - i) * min(heights[i], heights[j]) for i in range(n) for j in range(i + 1, n))


CASES = [
    ([1, 7, 2, 5, 4, 7, 3, 6],), ([2, 2, 2],), ([1, 1],), ([0, 0],), ([1, 8, 6, 2, 5, 4, 8, 3, 7],),
    ([1, 2, 4, 3],), ([5, 1, 1, 1, 5],), ([1, 1000, 1000, 1],),
]


def random_case(rng):
    return (ints(rng, 2, 10, 0, 20),)
