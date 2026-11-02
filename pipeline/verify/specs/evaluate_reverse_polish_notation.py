"""Evaluate Reverse Polish Notation: + - * /, division truncates toward zero."""
METHOD = "evalRPN"
COMPARE = "exact"


def apply(op, a, b):
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    return int(a / b)


def reference(tokens):
    stack = []
    for t in tokens:
        if t in "+-*/":
            b, a = stack.pop(), stack.pop()
            stack.append(apply(t, a, b))
        else:
            stack.append(int(t))
    return stack[0]


CASES = [
    (["1", "2", "+", "3", "*", "4", "-"],), (["4", "13", "5", "/", "+"],),
    (["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"],), (["7"],), (["-7"],),
    (["3", "-4", "/"],), (["7", "-3", "/"],), (["2", "5", "-"],), (["12", "4", "/"],), (["100", "-100", "*"],),
]


def random_case(rng):
    """Random expression tree; divisors are never 0."""
    def build(depth):
        if depth == 0 or rng.random() < 0.3:
            v = rng.randint(-20, 20)
            return [str(v)], v
        left, lv = build(depth - 1)
        right, rv = build(depth - 1)
        ops = ["+", "-", "*"] + (["/"] if rv != 0 else [])
        op = rng.choice(ops)
        return left + right + [op], apply(op, lv, rv)
    return (build(3)[0],)
