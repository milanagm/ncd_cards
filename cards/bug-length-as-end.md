---
id: bug-length-as-end
type: bug
mistakes: [off-by-one]
evidence: [string-encode-and-decode#13, string-encode-and-decode#17, string-encode-and-decode#18]
tags: [strings, encoding]
---
## Front
Decode, `s = "4#neet4#code..."`. Das Wort beginnt bei Index `i = 2` und hat die Länge `l = 4`. Was liest diese Schleife?

```python
word = ""
for p in range(i, l):
    word += s[p]
    i += 1
```

## Back
Nur `"ne"`, also die Positionen 2 und 3. `range(i, l)` endet an **Position** `l`, aber `l` ist eine **Länge**. Danach steht `i` mitten im Wort, und das nächste Längenfeld wird `"et4"` → `ValueError: invalid literal for int()`.

Fix: Das Ende ist Start plus Länge, `range(i, i + l)`. Noch einfacher per Slice: `word = s[i:i + l]`, dann `i += l`.

Genau dieser Crash, `int('et4')`, kam bei dir zweimal, auf den Tag einen Monat auseinander: am 17.10. mit `while j < int(l)` (#13) und am 17.11. mit `range(i, l)` (#17). #18 ✔
