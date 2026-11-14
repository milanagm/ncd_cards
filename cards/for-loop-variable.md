---
id: for-loop-variable
type: gotcha
mistakes: [for-loop-variable]
evidence: [string-encode-and-decode#3-4, buy-and-sell-crypto#8, buy-and-sell-crypto#9]
tags: [python, loops]
---
## Front
Was bewirkt `j += 1` in dieser Schleife?

```python
for j in range(l_w):
    word += s[i]
    i += 1
    j += 1
```

## Back
Nichts. `for` holt sich in jeder Runde den **nächsten Wert aus `range`** und überschreibt `j`. Änderungen an `j` im Körper sind wirkungslos, anders als in C oder Java.

Wer den Index selbst steuern will, zum Beispiel bei Pointern mit unterschiedlichen Sprüngen, nimmt `while`. `i += 1` ist hier dagegen nötig, denn `i` ist keine Schleifenvariable.

Dasselbe gilt **vor** der Schleife: Bei Buy and Sell #8 (13.11.) stand `p_l = i + 1` direkt vor `for p_l in range(len(prices)):`. Die Zuweisung ist wirkungslos, `p_l` läuft wieder ab 0, und frühere Tage zählen als Verkaufstag (9 statt 6). #9: `for p_l in range(i + 1, len(prices)):`
