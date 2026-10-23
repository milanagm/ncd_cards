---
id: bug-continue-no-progress
type: bug
mistakes: [loop-progress]
evidence: [three-integer-sum#20, three-integer-sum#21]
tags: [three-sum, loops]
---
## Front
Warum hängt dieser 3Sum-Code bei `[-2, 0, 1, 1, 2]`?

```python
for i, v in enumerate(nums_s):
    p_l, p_r = i + 1, len(nums_s) - 1
    while p_l < p_r:
        if v > 0:
            continue
        ...
```

## Back
Sobald `v > 0` ist (hier bei `v = 1`), springt `continue` an den Schleifenanfang, **ohne** `p_l` oder `p_r` zu ändern. `p_l < p_r` bleibt für immer wahr → Timeout.

Fix: `break` statt `continue`, oder besser schon vor der `while`-Schleife `if v > 0: break`. Im sortierten Array kann ab einem positiven `v` keine Summe 0 mehr entstehen.
