---
id: loop-progress-rule
type: concept
mistakes: [loop-progress, pointer-movement]
evidence: [three-integer-sum#11, three-integer-sum#12-13, three-integer-sum#20, longest-consecutive-sequence#0, buy-and-sell-crypto#0-1, longest-repeating-substring-with-replacement#2, longest-substring-without-duplicates#10-11]
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
- Wert statt Pointer geändert? → `prices[p_l] -= 1` lässt `p_l` stehen (Buy and Sell)
- Update nur in einer inneren Schleife? → läuft die nicht, hängt die äußere (`while p < len(s)`, Longest Substring)

Alle 10 deiner Timeouts waren genau das, zuletzt am 27.10.
