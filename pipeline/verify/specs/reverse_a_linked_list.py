"""Reverse Linked List: head comes in as a ListNode chain, the reversed chain is compared as a list."""
from ._gen import ints

METHOD = "reverseList"
COMPARE = "linked_list"


def reference(values):
    return values[::-1]


CASES = [([0, 1, 2, 3],), ([],), ([1],), ([1, 2],), ([5, 5, 7],), ([-1000, 0, 1000],)]


def random_case(rng):
    return (ints(rng, 0, 8, -1000, 1000),)
