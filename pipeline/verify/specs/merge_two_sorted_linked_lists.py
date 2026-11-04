"""Merge Two Sorted Linked Lists: both inputs come in as ListNode chains, the merged chain is compared as a list."""
from ._gen import ints

METHOD = "mergeTwoLists"
COMPARE = "linked_list"
LIST_ARGS = [0, 1]


def reference(list1, list2):
    return sorted(list1 + list2)


CASES = [
    ([1, 2, 4], [1, 3, 5]), ([], [1, 2]), ([], []), ([1, 2], []), ([5], [1, 2, 3]), ([-100, 0], [-100, 100]),
    ([2, 2, 2], [2, 2]),
]


def random_case(rng):
    return (sorted(ints(rng, 0, 6, -10, 10)), sorted(ints(rng, 0, 6, -10, 10)))
