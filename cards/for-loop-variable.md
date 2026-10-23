---
id: for-loop-variable
type: gotcha
mistakes: [for-loop-variable]
evidence: [string-encode-and-decode#3-4]
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
