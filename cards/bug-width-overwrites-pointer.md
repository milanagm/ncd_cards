---
id: bug-width-overwrites-pointer
type: bug
mistakes: [wrong-variable]
evidence: [max-water-container#6, max-water-container#7, max-water-container#8]
tags: [two-pointers, shadowing]
---
## Front
Container With Most Water, `heights = [1, 7, 2, 5, 4, 7, 3, 6]`: Erwartet 36, zurück kommt 7. Warum?

```python
l = 0
r = len(heights)-1
current_max = 0
while l < r:
    h = min(heights[l], heights[r])
    l = r - l
    current_max = max(current_max, h * l)
    if heights[l] < heights[r]:
        l += 1
    else:
        r -= 1
```

## Back
`l = r - l` speichert die **Breite** in `l` und überschreibt damit den linken Pointer. Runde 1: `h = 1`, `l = 7`, Fläche 7. Danach steht `l` hinter `r`, die Schleife endet.

Fix in #8: eigener Name `w = r - l`. Regel: ein Name, eine Bedeutung. `l`/`r` sind bei Two Pointers für die Pointer reserviert.

Im Versuch davor hießen die Pointer noch `i` und `p_l`, aber der Vergleich benutzte schon `l` und `r` → UnboundLocalError.
