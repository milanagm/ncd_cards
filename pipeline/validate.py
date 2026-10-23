"""Check ledger and cards against the real submissions before anything gets built.

Usage: python -m pipeline.validate [--subs ../ncd_subs]

Every ledger snippet and self note must literally occur (whitespace-insensitive) in each submission
it references, so the analysis cannot claim code that was never written.
"""
import argparse
import re
import sys
from pathlib import Path

from . import cards as card_files, config, render, store, viz


def normalize(text):
    return re.sub(r"\s+", " ", text).strip()


class Checker:
    def __init__(self, subs_root):
        self.subs_root = subs_root
        self.submissions = store.load_submissions()
        self.errors, self.warnings = [], []
        self._sources = {}

    def source(self, sub):
        if sub["path"] not in self._sources:
            self._sources[sub["path"]] = normalize((self.subs_root / sub["path"]).read_text(encoding="utf-8"))
        return self._sources[sub["path"]]

    def resolve(self, ref, where):
        try:
            return store.resolve_ref(ref, self.submissions)
        except ValueError as e:
            self.errors.append(f"{where}: {e}")
            return None, []

    def quoted(self, ref, text, where):
        _, subs = self.resolve(ref, where)
        for sub in subs:
            if normalize(text) not in self.source(sub):
                self.errors.append(f"{where}: {text!r} does not occur in {store.key(_, sub['n'])}")

    def ledger(self, ledger):
        ids = [c["id"] for c in ledger["categories"]]
        for dup in {i for i in ids if ids.count(i) > 1}:
            self.errors.append(f"ledger: duplicate category id {dup!r}")
        for cat in ledger["categories"]:
            where = f"ledger[{cat['id']}]"
            if not cat.get("title") or not cat.get("rule"):
                self.errors.append(f"{where}: needs title and rule")
            for occ in cat["occurrences"]:
                if "snippet" in occ:
                    self.quoted(occ["ref"], occ["snippet"], where)
                else:
                    self.resolve(occ["ref"], where)
        for note in ledger.get("self_notes", []):
            self.quoted(note["ref"], note["text"], "ledger.self_notes")
        for pattern in ledger.get("patterns", []):
            problem, subs = self.resolve(pattern["solved"], f"ledger.patterns[{pattern['problem']}]")
            if subs and subs[-1].get("verdict", {}).get("status") != "PASS":
                self.warnings.append(f"ledger.patterns: {pattern['solved']} is not judged PASS")
        return set(ids)

    def cards(self, cards, category_ids):
        seen = set()
        for card in cards:
            where = f"cards/{card['file']}"
            if card["id"] != card["file"].removesuffix(".md"):
                self.errors.append(f"{where}: id {card['id']!r} must match the file name")
            if card["id"] in seen:
                self.errors.append(f"{where}: duplicate id")
            seen.add(card["id"])
            if card["type"] not in config.CARD_TYPES:
                self.errors.append(f"{where}: type must be one of {sorted(config.CARD_TYPES)}")
            for section in ("front", "back"):
                if not card[section]:
                    self.errors.append(f"{where}: empty ## {section.title()}")
            for mistake in card["mistakes"]:
                if mistake not in category_ids:
                    self.errors.append(f"{where}: unknown ledger category {mistake!r}")
            for ref in card["evidence"]:
                self.resolve(ref, where)
            text = card["front"] + "\n" + card["back"]
            for code in render.python_blocks(text):
                if not render.parses(code):
                    self.errors.append(f"{where}: python block does not parse:\n{code}")
            for spec in render.viz_specs(text):
                try:
                    viz.render(spec)
                except Exception as e:
                    self.errors.append(f"{where}: viz block fails: {e}")
            if not card["evidence"] and card["type"] in ("bug", "gotcha"):
                self.warnings.append(f"{where}: no evidence; bug and gotcha cards should point to your submissions")


def check(subs_root):
    """Return (errors, warnings, ledger, cards)."""
    checker = Checker(subs_root)
    ledger = store.load_json(config.LEDGER, {"categories": []})
    category_ids = checker.ledger(ledger)
    cards = card_files.load_all()
    checker.cards(cards, category_ids)
    return checker.errors, checker.warnings, ledger, cards


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--subs", type=Path, default=config.DEFAULT_SUBS_PATH, help="path to the ncd_subs clone")
    args = ap.parse_args()
    errors, warnings, ledger, cards = check(args.subs)
    for w in warnings:
        print(f"warning: {w}")
    for e in errors:
        print(f"error: {e}")
    print(f"{len(ledger['categories'])} ledger categories, {len(cards)} cards, {len(errors)} errors, {len(warnings)} warnings")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
