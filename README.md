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

## In Anki: automatisch per Add-on

1. [`dist/ncd_sync.ankiaddon`](https://github.com/milanagm/ncd_cards/raw/main/dist/ncd_sync.ankiaddon) herunterladen
   und doppelklicken, oder in Anki am Desktop *Extras → Erweiterungen → Aus Datei installieren …*. Anki neu starten.
2. Ab jetzt holt das Add-on neue und geänderte Karten selbst: nach jedem Sync (also direkt nach dem Start),
   alle 6 Stunden und auf Knopfdruck über *Extras → NeetCode Insights aktualisieren*. Beim allerersten Lauf
   importiert es das Deck *NeetCode Insights* selbst.
3. Nach Änderungen synchronisiert es sofort mit AnkiWeb, damit die Karten aufs Handy kommen. Dafür muss Anki
   am Desktop bei AnkiWeb angemeldet sein.

Was das Add-on sonst tut:

- Wiederholst du einen Fehler, wird die passende Karte **heute fällig**, sofern du sie schon gelernt hast.
- Karten, die du in Anki änderst, bleiben so, bis sich die Karte im Repo ändert. Gelöschte Karten kommen nicht wieder.
- Jedes Update ist ein einzelner Schritt, den *Rückgängig* (Strg+Z) zurücknimmt.

Ohne Add-on geht es auch von Hand: [`dist/ncd_cards.apkg`](https://github.com/milanagm/ncd_cards/raw/main/dist/ncd_cards.apkg)
herunterladen und in Anki öffnen (*Datei → Importieren*). Ein erneuter Import aktualisiert die Karten, der
Lernfortschritt bleibt.

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
| `dist/` | Anki-Deck, Add-on, `cards.json` und `preview.html` mit allen Karten (generiert) |
| `anki_addon/ncd_sync/` | Quellcode des Anki-Add-ons |
| `tests/` | Tests des Add-ons gegen echte Anki-Collections (`requirements-dev.txt`) |
