"""One module per NeetCode problem: METHOD, COMPARE, reference(), CASES and random_case(rng).

COMPARE is one of: exact | unordered (list order irrelevant) | groups (order of groups and inside
groups irrelevant) | codec (decode(encode(x)) must equal x) | linked_list (the first argument is passed as
a ListNode chain, the returned chain is compared as a list; write inputs and reference with plain lists).
Fixed CASES and random cases must stay within the problem's constraints, otherwise correct
submissions get flagged.
"""
import importlib
import inspect


def module_name(slug):
    return f"{__name__}.{slug.replace('-', '_')}"


def load(slug):
    """Return the spec module for a problem slug, or None if nobody has written one yet."""
    name = module_name(slug)
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError as e:
        if e.name == name:
            return None
        raise


def fingerprint(spec):
    """Changes whenever the spec source changes, so verdicts made with an older spec get re-run."""
    import hashlib
    return hashlib.sha1(inspect.getsource(spec).encode()).hexdigest()[:12]
