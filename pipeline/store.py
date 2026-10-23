"""Reading and writing the JSON data files, and resolving submission references like 'three-integer-sum#12-13'."""
import json
import re

from . import config

REF_RE = re.compile(r"^(?P<problem>[a-z0-9-]+)#(?P<first>\d+)(?:-(?P<last>\d+))?$")


def load_json(path, default=None):
    if not path.exists():
        return default
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")


def load_submissions():
    return load_json(config.SUBMISSIONS, {"source": {}, "problems": {}})


def key(problem, n):
    return f"{problem}#{n}"


def resolve_ref(ref, submissions):
    """Expand a reference into the submission entries it names (ranges skip numbers that were never synced).

    Raises ValueError for malformed references or references that match nothing.
    """
    m = REF_RE.match(ref)
    if not m:
        raise ValueError(f"malformed reference {ref!r} (expected 'problem#N' or 'problem#A-B')")
    problem = m["problem"]
    first = int(m["first"])
    last = int(m["last"] or first)
    entries = submissions["problems"].get(problem, {}).get("submissions", [])
    found = [s for s in entries if first <= s["n"] <= last]
    if not found:
        raise ValueError(f"reference {ref!r} matches no submission")
    return problem, found
