---
id: binary-search-answer
type: pattern
mistakes: [binary-search-mid]
evidence: [eating-bananas#0-3, eating-bananas#7, eating-bananas#8, eating-bananas#9, eating-bananas#10]
tags: [binary-search]
---
## Front
Koko Eating Bananas: Binary Search über das Tempo `k`. Ein `k` reicht. Was merkst du dir, welche Grenze verschiebst du, und was gibst du am Ende zurück?

## Back
Das gültige `k` merken und **links weitersuchen**, ob ein kleineres auch reicht:

```python
lo, hi = 1, max(piles)
best = hi
while lo <= hi:
    k = (lo + hi) // 2
    if sum((p + k - 1) // k for p in piles) <= h:
        best = k
        hi = k - 1
    else:
        lo = k + 1
return best
```

Gesucht ist nicht irgendein Wert, sondern der **kleinste gültige**. Deshalb kein `return` beim ersten Treffer, und am Ende nicht das `k` der letzten Runde: das kann ungültig sein.

Deine Versuche: `return k` beim ersten Treffer (#0–3, dein Kommentar in #4: „das gibt nicht den minimalen zurück“), `return k` nach der Schleife (#7: 1 statt 2), `legit_k` nie bzw. mit `max_try` statt `k` gesetzt (#8–9: 4 statt 2). #10 mit `legit_k = k` ✔
