"""Render all cards into dist/: ncd_cards.apkg (Anki), cards.json (add-on, app) and preview.html.

Usage: python -m pipeline.build [--subs ../ncd_subs]

Refuses to build while validation reports errors. Note GUIDs derive from card ids, so re-importing
the deck updates existing notes in place and keeps their review history; never rename a card id.
"""
import argparse
import datetime
import html
import json
import sys
import warnings
import zipfile
from collections import Counter
from pathlib import Path
from urllib.parse import quote

import genanki

from . import config, render, store, style, validate

FIELDS = ["Front", "Back", "Typ", "Verlauf", "ID"]
FRONT_TEMPLATE = '<div class="wrap"><div class="typ">{{Typ}}</div>{{Front}}</div>'
BACK_TEMPLATE = ('{{FrontSide}}<div class="wrap"><hr id="answer">{{Back}}'
                 '{{#Verlauf}}<div class="verlauf">{{Verlauf}}</div>{{/Verlauf}}</div>')

STATUS = {
    "PASS": ("ok", "pass"),
    "WRONG_ANSWER": ("falsch", "fail"),
    "RUNTIME_ERROR": ("Crash", "crash"),
    "LOAD_ERROR": ("Crash", "crash"),
    "CRASH": ("Crash", "crash"),
    "TIMEOUT": ("Timeout", "timeout"),
}


def shorten(text, limit=72):
    return text if len(text) <= limit else text[:limit - 1] + "…"


def submission_url(sub):
    return f"{config.SUBS_URL}/blob/{config.SUBS_BRANCH}/{quote(sub['path'])}"


def verdict_detail(verdict):
    status = verdict.get("status")
    if status == "WRONG_ANSWER":
        return f"erwartet {verdict.get('expected')}, bekommen {verdict.get('got')}"
    if status == "TIMEOUT":
        return f"Eingabe {verdict.get('input')}"
    return verdict.get("error", "")


def ledger_notes(ledger):
    return {(cat["id"], occ["ref"]): occ["note"] for cat in ledger["categories"] for occ in cat["occurrences"]}


def history_html(card, submissions, notes):
    """'Dein Verlauf': one line per evidence reference with its outcomes and what went wrong.

    The explanation comes from the ledger occurrence with the same reference (preferring the card's
    own categories); without one, a single submission falls back to the judge's message.
    """
    items = []
    for ref in card["evidence"]:
        problem, subs = store.resolve_ref(ref, submissions)
        first, last = subs[0], subs[-1]
        numbers = f"#{first['n']}" if first is last else f"#{first['n']}–{last['n']}"
        outcomes = Counter(STATUS.get(s.get("verdict", {}).get("status"), ("?", "fail")) for s in subs)
        badges = "".join(f'<span class="badge {cls}">{f"{n}× " if n > 1 else ""}{label}</span>'
                         for (label, cls), n in outcomes.items())
        date = "" if first["bulk_sync"] else f" {first['date'][8:10]}.{first['date'][5:7]}."
        note = next((notes[(m, ref)] for m in card["mistakes"] if (m, ref) in notes), None)
        note = note or next((text for (_, r), text in notes.items() if r == ref), None)
        if note:
            detail = render.inline_html(note)
        elif len(subs) == 1 and first.get("verdict", {}).get("status") != "PASS":
            detail = f"<code>{html.escape(shorten(verdict_detail(first['verdict'])))}</code>"
        else:
            detail = ""
        items.append(f'<li><a href="{submission_url(first)}">{problem} {numbers}</a>{badges}{date}'
                     + (f" · {detail}" if detail else "") + "</li>")
    if not items:
        return ""
    return '<div class="title">Dein Verlauf</div><ul>' + "".join(items) + "</ul>"


def card_problems(card, submissions):
    return sorted({store.resolve_ref(ref, submissions)[0] for ref in card["evidence"]})


def last_failure(card, submissions):
    """UTC time of the newest failed submission in the card's evidence. When a later run adds a newer
    failure, the add-on takes it as "the mistake happened again" and makes the card due today."""
    times = [datetime.datetime.fromisoformat(sub["date"]).astimezone(datetime.timezone.utc).isoformat()
             for ref in card["evidence"] for sub in store.resolve_ref(ref, submissions)[1]
             if sub.get("verdict", {}).get("status") not in (None, "PASS")]
    return max(times, default=None)


def package_addon():
    """Zip anki_addon/ncd_sync into an .ankiaddon; fixed timestamps keep the file stable between builds."""
    source = config.ROOT / "anki_addon" / "ncd_sync"
    target = config.DIST / "ncd_sync.ankiaddon"
    with zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(source.iterdir()):
            if path.suffix in (".py", ".json", ".md"):
                info = zipfile.ZipInfo(path.name, date_time=(2026, 1, 1, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                zf.writestr(info, path.read_bytes())
    return target


def ledger_summary(ledger, submissions):
    summary = []
    for cat in ledger["categories"]:
        subs = [(problem, sub) for occ in cat["occurrences"]
                for problem, found in [store.resolve_ref(occ["ref"], submissions)] for sub in found]
        dated = [sub["date"][:10] for _, sub in subs if not sub["bulk_sync"]]
        summary.append({
            "id": cat["id"], "title": cat["title"], "rule": cat["rule"],
            "submissions": len({store.key(p, s["n"]) for p, s in subs}),
            "problems": sorted({p for p, _ in subs}),
            "last_seen": max(dated) if dated else None,
        })
    return summary


def build(subs_root):
    errors, warns, ledger, cards = validate.check(subs_root)
    for w in warns:
        print(f"warning: {w}")
    if errors:
        for e in errors:
            print(f"error: {e}")
        sys.exit(f"{len(errors)} validation errors, nothing built")

    submissions = store.load_submissions()
    notes = ledger_notes(ledger)
    model = genanki.Model(
        config.MODEL_ID, config.MODEL_NAME,
        fields=[{"name": name} for name in FIELDS],
        templates=[{"name": "Karte", "qfmt": FRONT_TEMPLATE, "afmt": BACK_TEMPLATE}],
        css=style.css(),
    )
    deck = genanki.Deck(config.DECK_ID, config.DECK_NAME, description=(
        "Karten aus meinen eigenen NeetCode-Submissions: wiederkehrende Fehler, Patterns, eigene Notizen. "
        '<a href="https://github.com/milanagm/ncd_cards">milanagm/ncd_cards</a>'))

    rendered = []
    for card in cards:
        problems = card_problems(card, submissions)
        tags = (set(card["tags"]) | {f"ncd::typ::{card['type']}"}
                | {f"ncd::fehler::{m}" for m in card["mistakes"]} | {f"ncd::problem::{p}" for p in problems})
        entry = {
            "id": card["id"],
            "guid": genanki.guid_for(config.GUID_NAMESPACE, card["id"]),
            "type": card["type"],
            "type_label": config.CARD_TYPES[card["type"]],
            "mistakes": card["mistakes"],
            "problems": problems,
            "evidence": card["evidence"],
            "tags": sorted(tags),
            "front_md": card["front"],
            "back_md": card["back"],
            "front_html": render.to_html(card["front"]),
            "back_html": render.to_html(card["back"]),
            "history_html": history_html(card, submissions, notes),
            "last_evidence": last_failure(card, submissions),
        }
        rendered.append(entry)
        deck.add_note(genanki.Note(
            model=model, guid=entry["guid"], tags=entry["tags"],
            fields=[entry["front_html"], entry["back_html"], entry["type_label"], entry["history_html"], entry["id"]],
        ))

    config.DIST.mkdir(exist_ok=True)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # genanki flags SVG tags it does not know as "invalid HTML"
        genanki.Package(deck).write_to_file(config.DIST / "ncd_cards.apkg")

    statuses = Counter(s.get("verdict", {}).get("status") for p in submissions["problems"].values()
                       for s in p["submissions"])
    export = {
        "version": 1,
        "deck": {"id": config.DECK_ID, "name": config.DECK_NAME},
        "note_type": {
            "id": config.MODEL_ID,
            "name": config.MODEL_NAME,
            "fields": FIELDS,
            "field_sources": dict(zip(FIELDS, ["front_html", "back_html", "type_label", "history_html", "id"])),
            "templates": [{"name": "Karte", "qfmt": FRONT_TEMPLATE, "afmt": BACK_TEMPLATE}],
            "css": style.css(),
        },
        "source": submissions["source"],
        "stats": {"submissions": sum(statuses.values()), "statuses": dict(statuses.most_common())},
        "ledger": ledger_summary(ledger, submissions),
        "cards": rendered,
    }
    store.save_json(config.DIST / "cards.json", export)
    (config.DIST / "preview.html").write_text(preview(rendered, export), encoding="utf-8")
    package_addon()

    by_type = Counter(c["type"] for c in rendered)
    print(f"built {len(rendered)} cards (" + ", ".join(f"{t} {n}" for t, n in sorted(by_type.items()))
          + ") → dist/ncd_cards.apkg, dist/cards.json, dist/preview.html, dist/ncd_sync.ankiaddon")


def preview(rendered, export):
    """All cards on one page, front and back, with a dark-mode toggle; for checking the design."""
    blocks = []
    for c in rendered:
        history = f'<div class="verlauf">{c["history_html"]}</div>' if c["history_html"] else ""
        blocks.append(
            f'<section class="card" id="{c["id"]}"><div class="wrap"><div class="typ">{c["type_label"]}'
            f' · {c["id"]}</div>{c["front_html"]}<hr id="answer">{c["back_html"]}{history}</div></section>')
    generated = datetime.date.today().isoformat()
    return f"""<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>NeetCode Insights · Vorschau</title>
<style>{export["note_type"]["css"]}
body {{ margin: 0; background: #eaeef2; }}
body.dark {{ background: #010409; }}
header {{ font: 14px -apple-system, Segoe UI, sans-serif; padding: 12px 16px; color: #59636e; }}
section.card {{ margin: 12px auto; max-width: 760px; border-radius: 12px; padding: 16px; box-sizing: border-box; }}
@media (max-width: 600px) {{ section.card {{ margin: 8px; padding: 12px; }} }}
</style></head>
<body><header>{len(rendered)} Karten · erzeugt {generated} ·
<button onclick="document.body.classList.toggle('dark');document.querySelectorAll('section.card').forEach(s=>s.classList.toggle('nightMode'))">Hell/Dunkel</button></header>
{"".join(blocks)}
</body></html>
"""


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--subs", type=Path, default=config.DEFAULT_SUBS_PATH, help="path to the ncd_subs clone")
    build(ap.parse_args().subs)


if __name__ == "__main__":
    main()
