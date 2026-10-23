"""Judge one submission in a child process: test spec as JSON on stdin, one JSON verdict line on stdout.

Run as a script with `python -I`, never imported, so the submission cannot shadow pipeline modules.
Statuses: PASS | WRONG_ANSWER | RUNTIME_ERROR | TIMEOUT | LOAD_ERROR. Like a judge, it stops at the
first failing case.
"""
import copy
import json
import resource
import signal
import sys
import traceback

# What NeetCode's Python runner has in scope without imports.
PREAMBLE = ("from typing import *\nfrom collections import *\n"
            "import collections, heapq, math, itertools, functools, bisect\n")
TIME_LIMIT_S = 2.0
MEMORY_LIMIT = 1 << 30


class Timeout(Exception):
    pass


def on_alarm(signum, frame):
    raise Timeout()


def location(exc, path):
    """Line of the submission where the exception surfaced."""
    frames = [f for f in traceback.extract_tb(exc.__traceback__) if f.filename == path]
    if not frames:
        return {}
    return {"line": frames[-1].lineno, "code": (frames[-1].line or "").strip()}


def short(value, limit=160):
    text = repr(value)
    return text if len(text) <= limit else text[:limit] + "…"


def normalize(compare, value):
    if compare == "groups":
        return sorted(sorted(group) for group in value)
    if compare == "unordered":
        return sorted(value)
    return value


def run(path, spec):
    namespace = {"__name__": "submission"}
    try:
        exec(PREAMBLE, namespace)
        exec(compile(open(path, encoding="utf-8").read(), path, "exec"), namespace)
        solution = namespace["Solution"]
    except BaseException as e:
        return {"status": "LOAD_ERROR", "error": f"{type(e).__name__}: {e}", **location(e, path)}

    compare, cases = spec["compare"], spec["cases"]
    for i, case in enumerate(cases):
        failed = {"passed": i, "total": len(cases), "input": short(case["args"])}
        args = copy.deepcopy(case["args"])
        signal.setitimer(signal.ITIMER_REAL, TIME_LIMIT_S)
        try:
            instance = solution()
            if compare == "codec":
                got = instance.decode(instance.encode(args[0]))
            else:
                got = getattr(instance, spec["method"])(*args)
        except Timeout:
            return {"status": "TIMEOUT", **failed}
        except MemoryError:
            return {"status": "TIMEOUT", **failed, "note": "MemoryError: the loop keeps growing a container"}
        except BaseException as e:
            return {"status": "RUNTIME_ERROR", **failed, "error": f"{type(e).__name__}: {e}", **location(e, path)}
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)

        expected = case["expected"]
        if got is not None and not isinstance(got, (list, bool, int)):
            return {"status": "WRONG_ANSWER", **failed, "expected": short(expected), "got": short(got),
                    "note": f"returns {type(got).__name__} instead of {type(expected).__name__}"}
        try:
            ok = got is not None and normalize(compare, got) == normalize(compare, expected)
        except TypeError:
            ok = False
        if not ok:
            return {"status": "WRONG_ANSWER", **failed, "expected": short(expected), "got": short(got)}
    return {"status": "PASS", "passed": len(cases), "total": len(cases)}


def main():
    resource.setrlimit(resource.RLIMIT_AS, (MEMORY_LIMIT, MEMORY_LIMIT))
    signal.signal(signal.SIGALRM, on_alarm)
    verdict = run(sys.argv[1], json.loads(sys.stdin.read()))
    sys.stdout.write("\n" + json.dumps(verdict) + "\n")


if __name__ == "__main__":
    main()
