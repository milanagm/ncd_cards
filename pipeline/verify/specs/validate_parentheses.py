"""Valid Parentheses: every bracket closed by the same type in the right order."""
from ._gen import text

METHOD = "isValid"
COMPARE = "exact"


def reference(s):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for c in s:
        if c in pairs:
            if not stack or stack.pop() != pairs[c]:
                return False
        else:
            stack.append(c)
    return not stack


CASES = [
    ("[]",), ("([{}])",), ("[(])",), ("(",), (")",), ("()[]{}",), ("(]",), ("((",), ("){",), ("([)]",),
    ("{[]}",), ("[]]",), ("(()",),
]


def random_case(rng):
    if rng.random() < 0.5:  # build a valid string, then maybe break it
        s = ""
        for _ in range(rng.randint(1, 5)):
            o, c = rng.choice(["()", "[]", "{}"])
            s = rng.choice([o + s + c, s + o + c])
        return (s,)
    return (text(rng, "()[]{}", 1, 8),)
