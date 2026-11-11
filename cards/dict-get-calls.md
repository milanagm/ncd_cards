---
id: dict-get-calls
type: gotcha
mistakes: [method-api]
evidence: [top-k-elements-in-list#23, top-k-elements-in-list#25, top-k-elements-in-list#27]
tags: [python, dict]
---
## Front
Zwei Zeilen mit `dict.get`. Was gehört an die Stellen mit `?`

```python-nocheck
counts[x] = counts.get(?) + 1          # zählen, fehlender Key zählt als 0
best = max(counts, key=?)              # Key mit dem größten Wert
```

## Back
```python
counts[x] = counts.get(x, 0) + 1
best = max(counts, key=counts.get)
```

1. Der Default ist das **zweite Positionsargument**. `counts.get(x, default=0)` ist ein `TypeError`, `dict.get` nimmt keine Keyword-Argumente.
2. `max` läuft über die **Keys** und vergleicht sie nach `counts.get(key)`. Übergeben wird die Methode selbst, ohne Klammern.

Am 10.11. bei Top K: erst `counts.append(...)` und `nums.get_values` (#23, beides gibt es nicht), dann `get(n, default = 0)` (#25). Deine Notiz dazu: „merken wie der aufruf gehT!“ #27 ✔
