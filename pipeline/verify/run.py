"""Judge submissions and store the verdicts in data/submissions.json.

Usage: python -m pipeline.verify.run [--subs ../ncd_subs] [--all]

By default only submissions without a verdict, or whose spec changed since, are judged. Problems
without a spec are reported: write pipeline/verify/specs/<problem_slug>.py first.
"""
import argparse
import json
import random
import subprocess
import sys
from collections import Counter
from pathlib import Path

from .. import config, store
from . import specs

JUDGE = Path(__file__).with_name("judge.py")
RANDOM_CASES = 40


def build_cases(slug, spec):
    rng = random.Random(slug)  # seeded: the same cases on every run
    inputs = list(spec.CASES) + [spec.random_case(rng) for _ in range(RANDOM_CASES)]
    cases = [{"args": list(args), "expected": spec.reference(*args)} for args in inputs]
    return {"method": spec.METHOD, "compare": spec.COMPARE, "cases": cases}


def judge(path, payload):
    try:
        proc = subprocess.run([sys.executable, "-I", str(JUDGE), str(path)], input=payload,
                              capture_output=True, text=True, timeout=120)
        return json.loads(proc.stdout.strip().splitlines()[-1])
    except Exception as e:  # killed by the OS, garbage on stdout, ...
        return {"status": "CRASH", "error": repr(e)}


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--subs", type=Path, default=config.DEFAULT_SUBS_PATH, help="path to the ncd_subs clone")
    ap.add_argument("--all", action="store_true", help="re-judge every submission")
    args = ap.parse_args()

    data = store.load_submissions()
    statuses, missing_specs, judged = Counter(), [], 0
    for slug, problem in data["problems"].items():
        spec = specs.load(slug)
        if spec is None:
            missing_specs.append(slug)
            continue
        fingerprint = specs.fingerprint(spec)
        payload = None
        for sub in problem["submissions"]:
            verdict = sub.get("verdict")
            if args.all or verdict is None or verdict.get("spec") != fingerprint:
                payload = payload or json.dumps(build_cases(slug, spec))
                sub["verdict"] = {**judge(args.subs / sub["path"], payload), "spec": fingerprint}
                judged += 1
            statuses[sub["verdict"]["status"]] += 1
    store.save_json(config.SUBMISSIONS, data)

    print(f"judged {judged} submissions; totals: " + ", ".join(f"{k} {v}" for k, v in statuses.most_common()))
    for slug in missing_specs:
        print(f"  no spec for {slug}: write pipeline/verify/specs/{slug.replace('-', '_')}.py")


if __name__ == "__main__":
    main()
