---
id: float-division-index
type: gotcha
mistakes: [float-division, binary-search-mid]
evidence: [search-2d-matrix#1, search-2d-matrix#2-3, search-2d-matrix#4]
tags: [python, binary-search]
---
## Front
`matrix` hat 4 Zeilen. Was ist `mid`, und was passiert in der zweiten Zeile?

```python
mid = len(matrix) / 2
if target == matrix[mid][0]:
    ...
```

## Back
`mid` ist `2.0`, ein **float**. `/` liefert in Python 3 immer float, auch wenn die Division aufgeht. Als Index → `TypeError: list indices must be integers or slices, not float`.

Fix: Ganzzahldivision `//`, also `mid = (l + r) // 2`.

Bei Search a 2D Matrix sind alle vier Versuche (#1–4) an genau dieser Zeile gescheitert. Eine halbe Stunde vorher hattest du bei Binary Search noch `int(len(nums)/ 2)` geschrieben, `//` macht das in einem Schritt.
