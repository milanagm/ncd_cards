"""Collection logic of the add-on, free of GUI code so it can be tested with the plain `anki` package.

apply() upserts the cards from cards.json by GUID:
- new cards go into the deck,
- a note is only rewritten when its source changed since the last run, so edits made in Anki
  survive until the source card changes,
- a card deleted in Anki is not added again,
- when a card's last failed submission gets newer (the mistake happened again), its review cards
  become due today.
The bookkeeping lives in the collection config, so it travels with AnkiWeb sync.
"""
import hashlib
import json
from dataclasses import dataclass, field

from anki.consts import CARD_TYPE_REV, QUEUE_TYPE_SUSPENDED

STATE_KEY = "ncd_sync"
SUPPORTED_VERSION = 1


class NeedsBootstrap(Exception):
    """The note type is missing: the deck package has to be imported once (it carries the fixed ids)."""


@dataclass
class Summary:
    added: list = field(default_factory=list)
    updated: list = field(default_factory=list)
    due_today: list = field(default_factory=list)
    deleted_in_anki: list = field(default_factory=list)
    gone_upstream: list = field(default_factory=list)
    note_type_updated: bool = False
    imported: int = 0  # set by the GUI after a first-run import of the deck package

    @property
    def changed(self):
        return bool(self.imported or self.added or self.updated or self.due_today or self.note_type_updated)

    def message(self):
        parts = []
        if self.imported:
            parts.append(f"Deck mit {self.imported} Karten importiert")
        if self.added:
            parts.append(f"{len(self.added)} neue Karten")
        if self.updated:
            parts.append(f"{len(self.updated)} aktualisiert")
        if self.due_today:
            parts.append(f"{len(self.due_today)} heute wieder fällig (Fehler wiederholt)")
        if self.note_type_updated and not parts:
            parts.append("Kartendesign aktualisiert")
        return "NeetCode Insights: " + (", ".join(parts) if parts else "alles aktuell")


@dataclass
class Result:
    changes: object  # OpChanges; the name lets aqt's CollectionOp refresh the UI
    summary: Summary


def source_hash(values, tags):
    return hashlib.sha1(json.dumps([values, sorted(tags)], sort_keys=True).encode()).hexdigest()


def find_note_type(col, spec):
    notetype = col.models.get(spec["id"]) or col.models.by_name(spec["name"])
    if notetype is None:
        raise NeedsBootstrap()
    names = [f["name"] for f in notetype["flds"]]
    if names != spec["fields"]:
        raise ValueError(f"Notiztyp '{notetype['name']}' hat die Felder {names}, erwartet {spec['fields']}")
    return notetype


def sync_note_type(col, notetype, spec):
    """Bring CSS and template text up to date. Adding fields or templates would need a full sync, so it is refused."""
    changed = notetype["css"] != spec["css"]
    notetype["css"] = spec["css"]
    templates = {t["name"]: t for t in notetype["tmpls"]}
    for wanted in spec["templates"]:
        current = templates.get(wanted["name"])
        if current is None:
            raise ValueError(f"Kartenvorlage '{wanted['name']}' fehlt im Notiztyp")
        if (current["qfmt"], current["afmt"]) != (wanted["qfmt"], wanted["afmt"]):
            current["qfmt"], current["afmt"] = wanted["qfmt"], wanted["afmt"]
            changed = True
    if changed:
        col.models.update_dict(notetype)
    return changed


def deck_id(col, spec):
    deck = col.decks.get(spec["id"], default=False)
    return deck["id"] if deck else col.decks.id(spec["name"])


def apply(col, payload, reschedule_recurring=True):
    if payload.get("version") != SUPPORTED_VERSION:
        raise ValueError(f"cards.json Version {payload.get('version')} wird nicht unterstützt, Add-on aktualisieren")
    spec = payload["note_type"]
    notetype = find_note_type(col, spec)  # raises before anything is changed

    undo_start = col.add_custom_undo_entry("NeetCode Insights aktualisieren")
    summary = Summary(note_type_updated=sync_note_type(col, notetype, spec))
    target_deck = deck_id(col, payload["deck"])
    state = col.get_config(STATE_KEY, None) or {}
    hashes = dict(state.get("hashes", {}))
    last_seen = dict(state.get("last_evidence", {}))

    for card in payload["cards"]:
        card_id = card["id"]
        values = {name: str(card[source]) for name, source in spec["field_sources"].items()}
        digest = source_hash(values, card["tags"])
        nid = col.db.scalar("select id from notes where guid = ?", card["guid"])
        if nid is None:
            if card_id in hashes:
                summary.deleted_in_anki.append(card_id)
                continue
            note = col.new_note(notetype)
            note.guid = card["guid"]
            for name, value in values.items():
                note[name] = value
            note.tags = list(card["tags"])
            col.add_note(note, target_deck)
            summary.added.append(card_id)
        else:
            note = col.get_note(nid)
            source_changed = hashes.get(card_id) != digest
            differs = any(note[n] != v for n, v in values.items()) or sorted(note.tags) != sorted(card["tags"])
            if source_changed and differs and note.mid == notetype["id"]:
                for name, value in values.items():
                    note[name] = value
                note.tags = list(card["tags"])
                col.update_note(note)
                summary.updated.append(card_id)
            last, seen = card.get("last_evidence"), last_seen.get(card_id)
            if reschedule_recurring and last and seen and last > seen:
                review_cards = [c.id for c in note.cards()
                                if c.type == CARD_TYPE_REV and c.queue != QUEUE_TYPE_SUSPENDED]
                if review_cards:
                    col.sched.set_due_date(review_cards, "0")
                    summary.due_today.append(card_id)
        hashes[card_id] = digest
        if card.get("last_evidence"):
            last_seen[card_id] = card["last_evidence"]

    summary.gone_upstream = sorted(set(hashes) - {c["id"] for c in payload["cards"]})
    col.set_config(STATE_KEY, {"hashes": hashes, "last_evidence": last_seen,
                               "source_head": payload.get("source", {}).get("head")}, undoable=True)
    return Result(changes=col.merge_undo_entries(undo_start), summary=summary)


def bootstrap(col, package_path):
    """Import the deck package once. Unlike creating the note type by hand, this keeps its fixed id."""
    from anki.collection import ImportAnkiPackageOptions, ImportAnkiPackageRequest
    from anki.import_export_pb2 import ImportAnkiPackageUpdateCondition as Condition

    never = Condition.IMPORT_ANKI_PACKAGE_UPDATE_CONDITION_NEVER
    options = ImportAnkiPackageOptions(with_scheduling=False, with_deck_configs=False, merge_notetypes=False,
                                       update_notes=never, update_notetypes=never)
    return col.import_anki_package(ImportAnkiPackageRequest(package_path=str(package_path), options=options))
