---
id: sudoku-box-index
type: trace
mistakes: []
evidence: [valid-sudoku#9-10]
tags: [sudoku, grid]
---
## Front
In welcher 3×3-Box liegt die Zelle `(r=4, c=7)`? Wie lautet die Formel für die Boxnummer 0–8?

```viz
kind: grid
mark: [4, 7]
caption: "Zelle (4, 7)"
```

## Back
Box `(r // 3, c // 3) = (1, 2)`, als Nummer `(r // 3) * 3 + c // 3 = 5`.

```viz
kind: grid
mark: [4, 7]
shade_box: true
caption: "Box 5: Zeilen 3–5, Spalten 6–8"
```

`r // 3` sagt, im wievielten Dreierblock die Zeile liegt (0, 1 oder 2), `c // 3` dasselbe für die Spalte. Damit reicht **ein** Durchlauf über das Board: `boxes[(r // 3, c // 3)].add(val)`.

Dein Kommentar beim Boxen-Code war „das habe ich tbh nicht gecheckt“. Genau dafür ist diese Karte da.
