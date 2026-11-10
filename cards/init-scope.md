---
id: init-scope
type: concept
mistakes: [init-scope]
evidence: [longest-repeating-substring-with-replacement#0, max-water-container#5, max-water-container#1-2, longest-substring-without-duplicates#12, eating-bananas#0-1, top-k-elements-in-list#17-18]
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
- Heimtückischer: `while i < k:` ohne `i = 0`, aber vorher lief `for i in nums` (Top K #17–18, 9.11.). `i` hat noch den letzten Wert aus `nums`, also kein NameError. Bei `[1, 2, 2, 3, 3, 3]` ist `i = 3`, `3 < 2` ist falsch, das Ergebnis ist leer
- `p_l = len(heights) - 1` vor der `for`-Schleife: ab dem zweiten `i` läuft die innere Schleife nie wieder (#1–2)
- `seen = set()` und `sub_len = 0` **in** der Schleife: das Fenster ist nie länger als 1 (Longest Substring #12)
- `needed_t = 0` **in** der Schleife über die Stapel: gezählt wird nur der letzte (Koko #0–1)

Deine Frage dazu: „wird bei for i dann zurückgesetzt bei i + 1 ?“ Nur die Schleifenvariable selbst. Alles andere behält seinen Wert, bis du es neu setzt.
