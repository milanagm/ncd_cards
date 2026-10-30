---
id: init-scope
type: concept
mistakes: [init-scope]
evidence: [longest-repeating-substring-with-replacement#0, max-water-container#5, max-water-container#1-2, longest-substring-without-duplicates#12]
tags: [loops]
---
## Front
Woran entscheidest du, ob eine Initialisierung **vor** oder **in** die Schleife gehört? Und was braucht eine `while`-Schleife, das eine `for`-Schleife nicht braucht?

## Back
- Gilt der Wert über alle Runden (Ergebnis, `seen`-Set eines Sliding Window)? → **vor** die Schleife
- Beginnt er in jeder Runde neu (innerer Pointer bei Brute Force)? → **in** die Schleife
- `while` setzt nichts selbst: der Laufindex muss vorher stehen. `for` setzt seine Variable in jeder Runde neu.

Deine Fälle:

- `while i < len(s):` ohne `i = 0` (Longest Repeating #0) und beim Umbau von `for` auf `while` bei Container With Most Water (#5) → NameError
- `p_l = len(heights) - 1` vor der `for`-Schleife: ab dem zweiten `i` läuft die innere Schleife nie wieder (#1–2)
- `seen = set()` und `sub_len = 0` **in** der Schleife: das Fenster ist nie länger als 1 (Longest Substring #12)

Deine Frage dazu: „wird bei for i dann zurückgesetzt bei i + 1 ?“ Nur die Schleifenvariable selbst. Alles andere behält seinen Wert, bis du es neu setzt.
