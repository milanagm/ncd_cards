---
id: iterate-index-value
type: concept
mistakes: [index-vs-value]
evidence: [three-integer-sum#1-6, three-integer-sum#7, products-of-array-discluding-self#2-4, valid-sudoku#2-5]
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
4. Python versucht jeden **Wert** in zwei Teile zu entpacken → `TypeError: cannot unpack non-iterable int object`

Dein häufigster Fehler überhaupt (6 von 12 Problemen): `for i in nums_s:` und danach `nums_s[i]`. Dort ist `i` ein Wert, kein Index. Konvention gegen die Verwechslung: `i`, `j` nur für Indizes, Werte heißen `v`, `x` oder `num`.
