# ncd_cards

Lernkarten aus Milanas NeetCode-Submissions (`milanagm/ncd_subs`). Die Karten sollen sich an ihren echten
Fehlern orientieren: Jede Behauptung über ihren Code muss belegbar sein.

## Setup in einer frischen Session

```bash
python3 -m venv .venv && .venv/bin/pip install -q -r requirements.txt
git clone https://github.com/milanagm/ncd_subs ../ncd_subs   # existiert es schon: git -C ../ncd_subs pull
```

Alle Befehle laufen im Repo-Root als `.venv/bin/python -m pipeline.<modul>`. `../ncd_subs` ist der
Standardpfad, sonst `--subs PFAD`.

## Täglicher Lauf

1. `git -C ../ncd_subs pull`
2. `python -m pipeline.extract`: aktualisiert `data/submissions.json` und listet nicht analysierte Submissions.
   Gibt es keine, ist der Lauf hier fertig.
3. Neues Problem ohne Spec: `pipeline/verify/specs/<slug_mit_unterstrichen>.py` anlegen, nach dem Muster
   der vorhandenen (`METHOD`, `COMPARE`, `reference`, `CASES`, `random_case`). Fixe und zufällige Fälle
   müssen in den Constraints des Problems auf neetcode.io bleiben, sonst werden korrekte Lösungen rot.
4. `python -m pipeline.verify.run`: beurteilt neue Submissions.
5. `python -m pipeline.digest`: zeigt pro Problem den Verlauf der neuen Submissions mit Status und Diff zum
   Vorgänger. Das ist die Grundlage der Analyse.
6. Analyse in `data/ledger.json`:
   - Jeden Fehlversuch einer Kategorie zuordnen; eine neue Kategorie nur, wenn keine passt.
   - `snippet` ist wörtlicher Code (Whitespace egal) und muss in **jeder** Submission der Referenz stehen.
   - Eigene Kommentare in Submissions (Fragen, „nicht gecheckt“, Ideen) kommen nach `self_notes`.
   - Gelöste Probleme kommen nach `patterns` (Pattern und lösende Submission).
7. Karten in `cards/` anlegen oder ergänzen (Regeln unten). Kehrt ein Fehler wieder, die bestehende Karte
   um den neuen Beleg erweitern statt eine Dublette zu schreiben.
8. `python -m pipeline.build`: validiert alles und baut `dist/`. Bei Validierungsfehlern wird nichts gebaut.
9. `python -m pipeline.digest --mark`: markiert die Submissions als analysiert.
10. Commit und Push auf `main`. Zum Schluss eine kurze Zusammenfassung auf Deutsch: neue Submissions mit Status,
    neue und erweiterte Karten, wiederkehrende Fehler (Kategorie, wie oft, wann zuletzt).

## Kartenregeln

- Deutsch, Fachbegriffe englisch (Two Pointers, Hashmap, Off-by-one).
- Eine Karte, ein Gedanke. Die Frage muss eine eindeutige Antwort haben.
- Typen: `gotcha` (Python-Detail), `bug` (Finde den Bug), `concept`, `pattern`, `trace` (mit Visualisierung).
- `bug`-Karten zeigen einen gekürzten Ausschnitt aus dem echten Fehlversuch; die Rückseite erklärt Ursache,
  Fix und die Regel dahinter.
- `evidence` zeigt auf die Submissions, in denen der Fehler steckt. Zahlen im Kartentext („17 von 33“) gegen
  `data/submissions.json` nachzählen.
- Einmalige Tippfehler kommen nur ins Ledger. Eine Karte gibt es, sobald ein Fehler wiederkehrt oder ein
  Konzept dahintersteckt.
- Wo Positionen oder Bewegung wichtig sind, ein ```` ```viz ````-Block (`array`, `grid`, `rows`, siehe
  `pipeline/viz.py`).
- Python-Blöcke müssen parsen; absichtlich kaputte Syntax als ```` ```python-nocheck ````.

## Nicht ändern

- Karten-IDs (= Dateinamen): Die Anki-GUID hängt daran, umbenennen verwaist den Lernfortschritt.
- `DECK_ID`, `MODEL_ID` und die Feldreihenfolge in `pipeline/build.py`: sonst legt Anki Deck und Notiztyp neu an.
