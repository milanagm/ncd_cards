"""Encode and Decode Strings: judged by decode(encode(strs)) == strs."""
from ._gen import text

METHOD = None
COMPARE = "codec"


def reference(strs):
    return strs


CASES = [
    (["neet", "code", "love", "you"],), (["we", "say", ":", "yes"],), ([],), ([""],), (["", ""],),
    (["a#b", "12#"],), (["x" * 12, "y"],), (["#", "##", "3#abc"],), (["hello world", "!@#$%"],),
]


def random_case(rng):
    return ([text(rng, "a#1 2", 0, 12) for _ in range(rng.randint(0, 5))],)
