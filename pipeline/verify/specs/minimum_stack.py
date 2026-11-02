"""Min Stack: push, pop, top and getMin; pop/top/getMin are only called on a non-empty stack."""
METHOD = None
CLASS = "MinStack"
COMPARE = "design"


def reference(ops, params):
    stack, out = [], [None]
    for op, p in zip(ops[1:], params[1:]):
        if op == "push":
            stack.append(p[0])
            out.append(None)
        elif op == "pop":
            stack.pop()
            out.append(None)
        elif op == "top":
            out.append(stack[-1])
        else:
            out.append(min(stack))
    return out


def ops_case(*calls):
    ops, params = ["MinStack"], [[]]
    for call in calls:
        op, *p = call.split()
        ops.append(op)
        params.append([int(x) for x in p])
    return (ops, params)


CASES = [
    ops_case("push 1", "push 2", "push 0", "getMin", "pop", "top", "getMin"),
    ops_case("push -2", "push 0", "push -3", "getMin", "pop", "top", "getMin"),
    ops_case("push 0", "push 1", "push 0", "getMin", "pop", "getMin"),       # duplicate minimum
    ops_case("push 5", "getMin", "pop", "push 7", "getMin", "top"),
    ops_case("push 2147483647", "push -2147483648", "getMin", "pop", "getMin"),
]


def random_case(rng):
    calls, size = [], 0
    for _ in range(rng.randint(1, 14)):
        op = "push" if size == 0 else rng.choice(["push", "push", "pop", "top", "getMin"])
        if op == "push":
            calls.append(f"push {rng.randint(-5, 5)}")
            size += 1
        else:
            calls.append(op)
            size -= op == "pop"
    return ops_case(*calls)
