"""The add-on's collection logic against real collections (official `anki` package, no GUI).

Run: pip install -r requirements-dev.txt && python -m pipeline.build && python -m pytest tests
"""
import copy
import importlib.util
import json
from pathlib import Path

import pytest
from anki.collection import Collection
from anki.consts import CARD_TYPE_NEW, CARD_TYPE_REV, QUEUE_TYPE_REV

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"

# Load core.py on its own: the add-on package's __init__ needs the Anki GUI.
_spec = importlib.util.spec_from_file_location("ncd_core", ROOT / "anki_addon" / "ncd_sync" / "core.py")
core = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(core)


@pytest.fixture
def payload():
    return json.loads((DIST / "cards.json").read_text(encoding="utf-8"))


@pytest.fixture
def col(tmp_path):
    collection = Collection(str(tmp_path / "collection.anki2"))
    yield collection
    collection.close()


@pytest.fixture
def synced(col, payload):
    """A collection after the first run: deck package imported, cards.json applied."""
    core.bootstrap(col, DIST / "ncd_cards.apkg")
    core.apply(col, payload)
    return col


def note_for(col, card):
    return col.get_note(col.db.scalar("select id from notes where guid = ?", card["guid"]))


def card_by_id(payload, card_id):
    return next(c for c in payload["cards"] if c["id"] == card_id)


def test_first_run_needs_the_deck_package(col, payload):
    with pytest.raises(core.NeedsBootstrap):
        core.apply(col, payload)
    assert col.note_count() == 0


def test_bootstrap_keeps_note_type_id_and_matches_cards_json(col, payload):
    core.bootstrap(col, DIST / "ncd_cards.apkg")
    assert col.models.get(payload["note_type"]["id"])["name"] == payload["note_type"]["name"]
    assert col.decks.id(payload["deck"]["name"], create=False)  # imported decks get a new id, matched by name

    summary = core.apply(col, payload).summary
    assert (summary.added, summary.updated, summary.due_today) == ([], [], [])
    assert col.note_count() == len(payload["cards"])


def test_second_run_changes_nothing(synced, payload):
    summary = core.apply(synced, payload).summary
    assert not summary.changed
    assert summary.message() == "NeetCode Insights: alles aktuell"


def test_new_card_is_added_to_the_deck(synced, payload):
    new = copy.deepcopy(payload["cards"][0])
    new["id"], new["guid"] = "brand-new-card", "brandnewguid"
    payload["cards"].append(new)

    summary = core.apply(synced, payload).summary
    assert summary.added == ["brand-new-card"]
    note = note_for(synced, new)
    assert note["ID"] == "brand-new-card"
    assert note.cards()[0].did == synced.decks.id(payload["deck"]["name"], create=False)


def test_local_edit_survives_until_the_source_changes(synced, payload):
    card = card_by_id(payload, "missing-return")
    note = note_for(synced, card)
    note["Back"] = "meine eigene Notiz"
    synced.update_note(note)

    assert core.apply(synced, payload).summary.updated == []
    assert note_for(synced, card)["Back"] == "meine eigene Notiz"

    card["back_html"] = "<p>neue Rückseite aus dem Repo</p>"
    assert core.apply(synced, payload).summary.updated == ["missing-return"]
    assert note_for(synced, card)["Back"] == "<p>neue Rückseite aus dem Repo</p>"


def test_card_deleted_in_anki_is_not_added_again(synced, payload):
    card = card_by_id(payload, "max-empty-default")
    synced.remove_notes([note_for(synced, card).id])

    summary = core.apply(synced, payload).summary
    assert summary.deleted_in_anki == ["max-empty-default"]
    assert summary.added == []
    assert synced.note_count() == len(payload["cards"]) - 1


def test_recurring_mistake_makes_review_card_due_today(synced, payload):
    reviewed = card_by_id(payload, "two-pointer-rule")
    unseen = card_by_id(payload, "empty-set-literal")
    card = note_for(synced, reviewed).cards()[0]
    card.type, card.queue, card.ivl, card.due = CARD_TYPE_REV, QUEUE_TYPE_REV, 10, synced.sched.today + 10
    synced.update_card(card)

    for c in (reviewed, unseen):
        c["last_evidence"] = "2099-01-01T00:00:00+00:00"
    summary = core.apply(synced, payload).summary

    assert summary.due_today == ["two-pointer-rule"]
    card = synced.get_card(card.id)
    assert (card.queue, card.due) == (QUEUE_TYPE_REV, synced.sched.today)
    assert note_for(synced, unseen).cards()[0].type == CARD_TYPE_NEW  # new cards stay in the new queue


def test_design_changes_reach_the_note_type(synced, payload):
    payload["note_type"]["css"] += "\n.card { letter-spacing: .01em; }"
    assert core.apply(synced, payload).summary.note_type_updated
    assert synced.models.get(payload["note_type"]["id"])["css"] == payload["note_type"]["css"]


def test_one_undo_step_reverts_notes_and_bookkeeping(synced, payload):
    card = card_by_id(payload, "missing-return")
    original = note_for(synced, card)["Back"]
    card["back_html"] = "<p>geändert</p>"
    core.apply(synced, payload)
    assert synced.undo_status().undo == "NeetCode Insights aktualisieren"

    synced.undo()
    assert note_for(synced, card)["Back"] == original
    assert core.apply(synced, payload).summary.updated == ["missing-return"]


def test_rejects_unknown_format(synced, payload):
    payload["version"] = 99
    with pytest.raises(ValueError):
        core.apply(synced, payload)
