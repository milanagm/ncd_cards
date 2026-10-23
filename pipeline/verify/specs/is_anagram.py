"""Valid Anagram."""
from ._gen import text

METHOD = "isAnagram"
COMPARE = "exact"


def reference(s, t):
    return sorted(s) == sorted(t)


CASES = [("racecar", "carrace"), ("jar", "jam"), ("a", "ab"), ("ab", "a"), ("aacc", "ccac"), ("anagram", "nagaram")]


def random_case(rng):
    return (text(rng, "abc", 1, 6), text(rng, "abc", 1, 6))
