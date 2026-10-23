---
id: sudoku-box-loops
type: concept
mistakes: [skip-irrelevant]
evidence: [valid-sudoku#3, valid-sudoku#9-10]
tags: [sudoku, grid]
---
## Front
Wie iterierst du mit verschachtelten Schleifen über alle 9 Boxen und ihre 9 Zellen? Warum `range(0, 9, 3)`?

## Back
```python
for br in range(0, 9, 3):          # 0, 3, 6
    for bc in range(0, 9, 3):      # 0, 3, 6
        seen = set()
        for r in range(br, br + 3):
            for c in range(bc, bc + 3):
                val = board[r][c]
                if val == ".":
                    continue
                if val in seen:
                    return False
                seen.add(val)
```

`range(0, 9, 3)` liefert die **linken oberen Ecken** der Boxen: 0, 3, 6. Von dort laufen die inneren Schleifen je 3 Zellen weit. `seen` wird pro Box **neu** angelegt, leere Zellen `.` werden übersprungen (das hatte in #3 gefehlt).

Ohne verschachtelte Boxen-Schleifen geht es mit dem Schlüssel `(r // 3, c // 3)`, siehe Karte zum Box-Index.
