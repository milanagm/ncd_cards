"""Shared paths and fixed identifiers."""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CARDS = ROOT / "cards"
DIST = ROOT / "dist"

SUBMISSIONS = DATA / "submissions.json"
LEDGER = DATA / "ledger.json"
STATE = DATA / "state.json"

SUBS_REPO = "milanagm/ncd_subs"
SUBS_BRANCH = "main"
SUBS_URL = f"https://github.com/{SUBS_REPO}"
DEFAULT_SUBS_PATH = ROOT.parent / "ncd_subs"

# Never change these: Anki would treat the note type as new and the review history would be orphaned.
# (Imported decks get a fresh id and are matched by name, so DECK_NAME matters as much as DECK_ID.)
DECK_ID = 2014888813
MODEL_ID = 2092628527
DECK_NAME = "NeetCode Insights"
MODEL_NAME = "NCD Karte"
GUID_NAMESPACE = "ncd-cards"

CARD_TYPES = {
    "gotcha": "Python-Gotcha",
    "bug": "Finde den Bug",
    "concept": "Konzept",
    "pattern": "Pattern",
    "trace": "Trace",
}
