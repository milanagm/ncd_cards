"""Valid Palindrome: only alphanumeric characters count, case-insensitive."""
from ._gen import text

METHOD = "isPalindrome"
COMPARE = "exact"


def reference(s):
    t = [c.lower() for c in s if c.isalnum()]
    return t == t[::-1]


CASES = [
    ("Was it a car or a cat I saw?",), ("tab a cat",), (" ",), ("a.",), ("ab",), ("0P",), (".,",),
    ("A man, a plan, a canal: Panama",), ("race a car",), ("aa",), ("abba",), ("abcba",), ("ab_a",),
]


def random_case(rng):
    if rng.random() < 0.5:
        return (text(rng, "aAbB1 ,.:", 1, 10),)
    half = text(rng, "abAB1", 0, 5)
    core = half + text(rng, "ab", 0, 1) + half[::-1].swapcase()
    return ("".join(c + text(rng, " ,.:", 0, 1) for c in core) or " ",)
