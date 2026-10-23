---
id: bug-3sum-match-no-move
type: bug
mistakes: [loop-progress, pointer-movement]
evidence: [three-integer-sum#11, three-integer-sum#12-13, three-integer-sum#16]
tags: [three-sum, two-pointers]
---
## Front
Was fehlt im Treffer-Zweig?

```python
while l < r:
    s = nums[i] + nums[l] + nums[r]
    if s < 0:
        l += 1
    elif s > 0:
        r -= 1
    else:
        res.append([nums[i], nums[l], nums[r]])
```

## Back
Nach einem Treffer bewegt sich kein Pointer, dieselbe Summe wird endlos wieder gefunden → Timeout. Beide Pointer müssen nach innen, gleiche Werte werden übersprungen:

```python
while l < r:
    s = nums[i] + nums[l] + nums[r]
    if s < 0:
        l += 1
    elif s > 0:
        r -= 1
    else:
        res.append([nums[i], nums[l], nums[r]])
        l += 1
        r -= 1
        while l < r and nums[l] == nums[l - 1]:
            l += 1
```

Dein Verlauf zeigt beide Stufen: erst gar keine Bewegung (#11), dann `p_r += 1` in die falsche Richtung (#12–13).
