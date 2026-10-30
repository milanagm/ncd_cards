---
id: max-water-pattern
type: pattern
mistakes: [problem-model]
evidence: [max-water-container#0, max-water-container#4, max-water-container#8]
tags: [two-pointers]
---
## Front
Container With Most Water in O(n): Wie berechnest du die Fläche zwischen `l` und `r`, und welchen Pointer bewegst du danach?

## Back
Fläche = **Breite × kleinere Höhe**: `(r - l) * min(h[l], h[r])`.

```python
l, r = 0, len(heights) - 1
best = 0
while l < r:
    best = max(best, (r - l) * min(heights[l], heights[r]))
    if heights[l] < heights[r]:
        l += 1
    else:
        r -= 1
return best
```

Bewegt wird die **kleinere** Seite. Die kleinere Höhe begrenzt die Fläche; die größere nach innen zu ziehen macht die Breite kleiner, ohne dass die Höhe steigen kann.

Dein erster Entwurf (#0) rechnete Höhe × Höhe. #4 bestand mit allen Paaren, also O(n²), #8 mit Two Pointers.
