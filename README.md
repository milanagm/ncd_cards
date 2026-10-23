# ncd_cards

Karteikarten aus meinen eigenen NeetCode-Submissions. Quelle ist [`milanagm/ncd_subs`](https://github.com/milanagm/ncd_subs),
wohin NeetCode jede Submission automatisch committet, auch die fehlgeschlagenen. Genau die sind hier das Material:
wiederkehrende Fehler, Patterns und eigene Notizen werden zu Anki-Karten und später zu einer eigenen Lern-App.

## Wie es funktioniert

```
ncd_subs ──▶ extract ──▶ verify ──▶ Analyse (Claude) ──▶ Karten ──▶ build
             Index aller   jede Sub.    Fehler-Ledger mit    cards/*.md   dist/ncd_cards.apkg
             Submissions   gegen Tests  belegten Fundstellen              dist/cards.json
```

1. **extract**: indexiert alle Submissions (Problem, Nummer, Commit, Datum) in `data/submissions.json`.
2. **verify**: NeetCode speichert keinen Pass/Fail-Status. Deshalb läuft jede Submission gegen Testfälle
   (Referenzlösung plus Zufallstests, `pipeline/verify/specs/`) und bekommt einen Status:
   `PASS`, `WRONG_ANSWER`, `RUNTIME_ERROR`, `TIMEOUT` oder `LOAD_ERROR`, mit exakter Fehlermeldung und Zeile.
3. **Analyse**: Fehler werden Kategorien im Fehler-Ledger (`data/ledger.json`) zugeordnet. Jede Fundstelle
   zitiert den Code wörtlich, die Validierung prüft das gegen die echte Datei.
4. **Karten**: eine Markdown-Datei pro Karte in `cards/`, mit Verweisen auf Ledger und Submissions.
5. **build**: rendert Markdown, Syntax-Highlighting und SVG-Visualisierungen zu einem Anki-Deck und `cards.json`.

## In Anki importieren

1. [`dist/ncd_cards.apkg`](https://github.com/milanagm/ncd_cards/raw/main/dist/ncd_cards.apkg) herunterladen.
2. In Anki am Desktop: *Datei → Importieren* (oder Doppelklick auf die Datei). Danach synchronisieren,
   dann landet das Deck *NeetCode Insights* über AnkiWeb auch am Handy.
3. Neue Versionen genauso importieren: Bestehende Karten werden aktualisiert, der Lernfortschritt bleibt.

Jede Karte endet mit **Dein Verlauf**: die Submissions, in denen der Fehler steckt, mit Status und Link.

## Befehle

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
git clone https://github.com/milanagm/ncd_subs ../ncd_subs

.venv/bin/python -m pipeline.extract        # Index aktualisieren, neue Submissions anzeigen
.venv/bin/python -m pipeline.verify.run     # neue Submissions beurteilen
.venv/bin/python -m pipeline.digest         # Verlauf der neuen Submissions mit Status und Diffs
.venv/bin/python -m pipeline.validate       # Ledger und Karten gegen die echten Dateien prüfen
.venv/bin/python -m pipeline.build          # dist/ bauen (validiert vorher)
.venv/bin/python -m pipeline.digest --mark  # Submissions als analysiert markieren
```

Der Ablauf für die täglichen Läufe und die Kartenregeln stehen in [`CLAUDE.md`](CLAUDE.md).

## Aufbau

| Pfad | Inhalt |
|---|---|
| `pipeline/` | Extraktion, Verifier, Build |
| `pipeline/verify/specs/` | ein Testspec pro NeetCode-Problem |
| `data/submissions.json` | alle Submissions mit Status (generiert) |
| `data/ledger.json` | Fehlerkategorien mit Belegen |
| `data/state.json` | welche Submissions schon analysiert sind |
| `cards/` | Karten als Markdown |
| `dist/` | Anki-Deck, `cards.json` und `preview.html` mit allen Karten (generiert) |
