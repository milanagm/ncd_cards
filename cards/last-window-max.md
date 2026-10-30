---
id: last-window-max
type: concept
mistakes: [last-window]
evidence: [longest-substring-without-duplicates#0-2, longest-repeating-substring-with-replacement#3-6]
tags: [sliding-window]
---
## Front
Sliding Window: Du aktualisierst `max_len` nur dann, wenn das Fenster bricht (Duplikat gefunden, Ersetzungen aufgebraucht). Welche Eingaben gehen schief?

## Back
Alle, bei denen das beste Fenster **bis zum Ende** reicht: Dort bricht nichts mehr, also wird es nie gewertet. Bei `"abc"` kommt 0 heraus.

Regel: `max_len` nach **jeder** Erweiterung aktualisieren, nicht im Abbruchzweig.

Bei dir zweimal am 26.10.:

- Longest Substring #0–2: `max_len` nur im `else`; #3 ergänzt die Zeile nach der Schleife
- Longest Repeating Character Replacement #3–6: gewertet nur bei `k_sub == 0`; bei `"XYYX"`, k = 2 reicht das Fenster der Länge 4 bis ans Ende und geht verloren
