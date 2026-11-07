---
id: iterate-index-value
type: concept
mistakes: [index-vs-value]
evidence: [three-integer-sum#1-6, three-integer-sum#7, products-of-array-discluding-self#2-4, valid-sudoku#2-5, longest-substring-without-duplicates#8, eating-bananas#0, two-integer-sum#36, buy-and-sell-crypto#4]
tags: [python, loops]
---
## Front
Du brauchst in der Schleife Index **und** Wert. Was liefern die ersten drei Schleifen, und warum crasht die vierte?

```python
for x in nums: ...
for i in range(len(nums)): ...
for i, x in enumerate(nums): ...
for i, x in nums: ...
```

## Back
1. nur Werte
2. nur Indizes
3. Paare aus Index und Wert ✔
4. Python versucht jeden **Wert** in zwei Teile zu entpacken → `TypeError: cannot unpack non-iterable int object`. Genau das bei 3Sum #7 und am 4.11. bei Two Sum #36; eine Minute später lief #37 mit `enumerate`.

Einer deiner häufigsten Fehler (9 von 25 Problemen): `for i in nums_s:` und danach `nums_s[i]`. Am 27.10. andersherum: `for e in s:` und dann `p = e + 1`, mit deiner Frage im Code „iterieren über elements oder index?“ Antwort: `for x in s` liefert Elemente. Am 31.10. bei Koko wieder: `for i in piles:` und dann `piles[i] // k` → IndexError. Am 6.11. bei Buy and Sell: `for i in prices:` und dann `range(i+1, ...)`, also ein Preis als Startindex → 3 statt 0 bei `[10, 8, 7, 5, 2]`. Dort ist `i` ein Wert, kein Index. Konvention gegen die Verwechslung: `i`, `j` nur für Indizes, Werte heißen `v`, `x` oder `num`.
