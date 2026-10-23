---
id: bug-twosum-index-vs-value
type: bug
mistakes: [index-vs-value, duplicates-order]
evidence: [two-integer-sum#11-15]
tags: [two-sum]
---
## Front
`nums = [5, 5]`, `target = 10` → Ergebnis `[0, 0]`. Warum?

```python
for i, v in enumerate(nums):
    if (target - v) in nums and i != (target - v):
        return [i, nums.index(target - v)]
```

## Back
`i != (target - v)` vergleicht einen **Index** (`0`) mit einem **Wert** (`5`). Das ist hier immer wahr, also wird dasselbe Element doppelt benutzt: `nums.index(5)` ist wieder `0`.

Auch mit echtem Index-Vergleich (`nums.index(target - v) != i`) bleibt es heikel: `index()` findet immer das **erste** Vorkommen und kostet O(n). Sauber ist die Hashmap, siehe Two-Sum-Pattern.
