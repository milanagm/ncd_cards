"""Longest Substring Without Repeating Characters: length of the longest window with distinct chars."""
from ._gen import text

METHOD = "lengthOfLongestSubstring"
COMPARE = "exact"


def reference(s):
    best = 0
    for i in range(len(s)):
        for j in range(i, len(s)):
            if len(set(s[i:j + 1])) == j - i + 1:
                best = max(best, j - i + 1)
    return best


CASES = [
    ("zxyzxyz",), ("xxxx",), ("",), ("a",), ("abcabcbb",), ("pwwkew",), ("dvdf",), ("abba",), ("tmmzuxt",),
    ("ab cd!a",), ("au",),
]


def random_case(rng):
    return (text(rng, "abcd ", 0, 10),)
