---
id: list-index-first
type: gotcha
mistakes: [list-lookup-complexity, duplicates-order]
evidence: [two-integer-sum#5-6, two-integer-sum#28-29]
tags: [python, list]
---
## Front
`nums = [5, 5]`: Was liefert `nums.index(5)`, und was kostet der Aufruf?

## Back
`0`: `index()` liefert immer das **erste** Vorkommen. Die zweite 5 findest du damit nie.

Kosten: **O(n)**, die Liste wird von vorne durchsucht. In einer Schleife über alle Elemente ergibt das O(n²). Besser: Positionen beim Durchlaufen in einem Dict merken, `seen[v] = i`.
