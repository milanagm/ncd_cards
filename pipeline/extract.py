"""Index every submission in the ncd_subs clone: problem, number, the commit that added it, and its date.

Usage: python -m pipeline.extract [--subs ../ncd_subs]

Rewrites data/submissions.json, keeping verdicts whose file content is unchanged, and lists the
submissions that have not been analyzed yet (see data/state.json).
"""
import argparse
import hashlib
import re
import subprocess
from pathlib import Path

from . import config, store

SUB_RE = re.compile(r"^submission-(\d+)\.(\w+)$")


def git(subs, *args):
    cmd = ["git", "-c", "core.quotePath=false", "-C", str(subs), *args]
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def adding_commits(subs):
    """Map each path to (sha, author date, subject) of the most recent commit that added it."""
    out = git(subs, "log", "--diff-filter=A", "--no-renames", "--name-only", "--format=%x00%H%x1f%aI%x1f%s")
    added = {}
    for block in out.split("\x00")[1:]:
        header, _, files = block.partition("\n")
        sha, date, subject = header.split("\x1f")
        for path in files.splitlines():
            if path:
                added.setdefault(path, (sha, date, subject))
    return added


def scan(subs):
    added = adding_commits(subs)
    problems = {}
    for path in sorted(subs.glob("*/*/submission-*.*")):
        m = SUB_RE.match(path.name)
        if not m:
            continue
        rel = path.relative_to(subs).as_posix()
        if rel not in added:
            raise SystemExit(f"{rel} is not committed in {subs}; pull or commit first")
        sha, date, subject = added[rel]
        topic, problem = path.parent.parent.name, path.parent.name
        entry = problems.setdefault(problem, {"topic": topic, "submissions": []})
        entry["submissions"].append({
            "n": int(m[1]),
            "ext": m[2],
            "path": rel,
            "sha1": hashlib.sha1(path.read_bytes()).hexdigest(),
            "commit": sha,
            "date": date,
            "bulk_sync": subject.startswith("Bulk sync"),
        })
    for entry in problems.values():
        entry["submissions"].sort(key=lambda s: s["n"])
    return problems


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--subs", type=Path, default=config.DEFAULT_SUBS_PATH, help="path to the ncd_subs clone")
    args = ap.parse_args()

    old = store.load_submissions()
    old_verdicts = {
        (s["path"], s["sha1"]): s["verdict"]
        for p in old["problems"].values() for s in p["submissions"] if "verdict" in s
    }
    problems = scan(args.subs)
    for p in problems.values():
        for s in p["submissions"]:
            if (s["path"], s["sha1"]) in old_verdicts:
                s["verdict"] = old_verdicts[(s["path"], s["sha1"])]

    head = git(args.subs, "log", "-1", "--format=%H%x1f%aI").strip().split("\x1f")
    store.save_json(config.SUBMISSIONS, {
        "source": {"repo": config.SUBS_REPO, "head": head[0], "head_date": head[1]},
        "problems": dict(sorted(problems.items())),
    })

    analyzed = set(store.load_json(config.STATE, {}).get("analyzed", []))
    new = {name: [s["n"] for s in p["submissions"] if store.key(name, s["n"]) not in analyzed]
           for name, p in sorted(problems.items())}
    total = sum(len(p["submissions"]) for p in problems.values())
    print(f"{len(problems)} problems, {total} submissions, {sum(map(len, new.values()))} not analyzed yet")
    for name, numbers in new.items():
        if numbers:
            print(f"  {name}: " + ", ".join(f"#{n}" for n in numbers))


if __name__ == "__main__":
    main()
