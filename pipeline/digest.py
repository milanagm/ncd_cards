"""Show the attempt history of problems with unanalyzed submissions: verdict plus diff to the previous attempt.

Usage:
  python -m pipeline.digest [--subs ../ncd_subs] [--problem SLUG] [--all]
  python -m pipeline.digest --mark      # after the analysis: record the listed submissions as analyzed

The previous (already analyzed) attempt is shown as context, so each diff is readable on its own.
"""
import argparse
import difflib
from pathlib import Path

from . import config, store

REWRITE_LINES = 40


def verdict_line(sub):
    v = sub.get("verdict", {})
    status = v.get("status", "NOT JUDGED")
    parts = [status]
    if "passed" in v:
        parts.append(f"{v['passed']}/{v['total']}")
    if v.get("error"):
        parts.append(v["error"])
    if v.get("line"):
        parts.append(f"line {v['line']}: {v.get('code', '')}")
    if status in ("WRONG_ANSWER", "TIMEOUT"):
        parts.append(f"input={v.get('input')}")
    if status == "WRONG_ANSWER":
        parts.append(f"expected={v.get('expected')} got={v.get('got')}")
    if v.get("note"):
        parts.append(v["note"])
    date = sub["date"][:16].replace("T", " ") + (" (bulk sync)" if sub["bulk_sync"] else "")
    return f"#{sub['n']} [{date}] " + " | ".join(parts)


def render(slug, subs, wanted, root):
    out = [f"## {slug}"]
    prev = None
    for sub in subs:
        lines = (root / sub["path"]).read_text(encoding="utf-8").rstrip().splitlines()
        if store.key(slug, sub["n"]) in wanted:
            out.append("### " + verdict_line(sub))
            diff = None if prev is None else [
                l for l in difflib.unified_diff(prev, lines, lineterm="", n=1) if not l.startswith(("---", "+++"))]
            if diff is None or len(diff) > REWRITE_LINES:
                out += ["```python", *lines, "```"]
            elif diff:
                out += ["```diff", *diff, "```"]
            else:
                out.append("(identical to the previous attempt)")
        prev = lines
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--subs", type=Path, default=config.DEFAULT_SUBS_PATH, help="path to the ncd_subs clone")
    ap.add_argument("--problem", help="only this problem")
    ap.add_argument("--all", action="store_true", help="include already analyzed submissions")
    ap.add_argument("--mark", action="store_true", help="mark the selected submissions as analyzed")
    args = ap.parse_args()

    data = store.load_submissions()
    state = store.load_json(config.STATE, {})
    analyzed = set(state.get("analyzed", []))
    selected = {
        slug: {store.key(slug, s["n"]) for s in p["submissions"]
               if args.all or store.key(slug, s["n"]) not in analyzed}
        for slug, p in data["problems"].items() if not args.problem or slug == args.problem
    }
    if args.mark:
        state["analyzed"] = sorted(analyzed.union(*selected.values()))
        store.save_json(config.STATE, state)
        print(f"marked {sum(map(len, selected.values()))} submissions as analyzed")
        return
    for slug, wanted in selected.items():
        if wanted:
            print("\n".join(render(slug, data["problems"][slug]["submissions"], wanted, args.subs)) + "\n")


if __name__ == "__main__":
    main()
