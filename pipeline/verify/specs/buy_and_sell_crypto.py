"""Best Time to Buy and Sell Stock: max profit of one buy followed by one sell, 0 if none."""
from ._gen import ints

METHOD = "maxProfit"
COMPARE = "exact"


def reference(prices):
    return max([0] + [prices[j] - prices[i] for i in range(len(prices)) for j in range(i + 1, len(prices))])


CASES = [
    ([10, 1, 5, 6, 7, 1],), ([10, 8, 7, 5, 2],), ([1],), ([2, 4, 1],), ([3, 3, 3],), ([7, 1, 5, 3, 6, 4],),
    ([2, 1, 2, 1, 0, 1, 2],), ([0, 100],),
]


def random_case(rng):
    return (ints(rng, 1, 10, 0, 100),)
