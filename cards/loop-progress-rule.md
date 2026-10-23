---
id: loop-progress-rule
type: concept
mistakes: [loop-progress, pointer-movement]
evidence: [three-integer-sum#11, three-integer-sum#12-13, three-integer-sum#20, longest-consecutive-sequence#0]
tags: [loops]
---
## Front
Woran erkennst du **vor** dem Abschicken, dass eine `while`-Schleife terminiert?

## Back
Jeder Pfad durch den Schleifenkörper muss die Abbruchbedingung **näher bringen**, z. B. den Abstand `r - l` verkleinern. Prüfe jeden Zweig einzeln:

- Zweig ohne Update? → Endlosschleife (3Sum: nach einem Treffer kein `l += 1` / `r -= 1`)
- Update in die falsche Richtung? → Endlosschleife (`p_r += 1`)
- `continue` vor dem Update? → Endlosschleife (`if v > 0: continue`)
- Bedingung hängt gar nicht von den Daten ab? → `while (i+1) - i == 1` ist immer wahr

Alle 5 deiner Timeouts waren genau das.
