"""Longest Repeating Character Replacement: longest window that becomes one letter after <= k changes."""
from ._gen import text

METHOD = "characterReplacement"
COMPARE = "exact"


def reference(s, k):
    best = 0
    for i in range(len(s)):
        for j in range(i, len(s)):
            window = s[i:j + 1]
            if len(window) - max(window.count(c) for c in set(window)) <= k:
                best = max(best, len(window))
    return best


CASES = [
    ("XYYX", 2), ("AAABABB", 1), ("ABAB", 2), ("AABABBA", 1), ("A", 0), ("ABCD", 0), ("AAAA", 0),
    ("ABBB", 2), ("BAAAB", 2),
]


def random_case(rng):
    s = text(rng, "ABC", 1, 10)
    return (s, rng.randint(0, len(s)))
