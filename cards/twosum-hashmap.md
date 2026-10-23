---
id: twosum-hashmap
type: pattern
mistakes: [duplicates-order, list-lookup-complexity]
evidence: [two-integer-sum#0, two-integer-sum#1-4, two-integer-sum#5-6, two-integer-sum#35]
tags: [hashmap, two-sum]
---
## Front
Two Sum in O(n): Wie sieht die Schleife aus, und warum heißt es „erst prüfen, dann einfügen“?

## Back
```python
seen = {}  # Wert -> Index
for i, v in enumerate(nums):
    if target - v in seen:
        return [seen[target - v], i]
    seen[v] = i
```

- **Erst prüfen:** `seen` enthält nur *frühere* Elemente, ein Element wird also nie mit sich selbst gepaart. `[5, 5]` klappt trotzdem, denn bei `i = 1` steht die erste 5 schon drin.
- **Reihenfolge gratis:** `seen[...]` ist immer ein früherer Index, der kleinere steht also vorne, ohne `sorted()`.
- **O(n):** Dict-Lookup ist O(1). `in nums` plus `nums.index()` kosten O(n) pro Schritt.

Diese Lösung hattest du schon in #0. Danach liefen 29 von 33 Versuchen über `in nums` (O(n²)), und 17 scheiterten an `[5, 5]` oder an der Reihenfolge.
