---
id: bug-sorted-copy-name
type: bug
mistakes: [wrong-variable]
evidence: [three-integer-sum#22, three-integer-sum#23, three-integer-sum#1]
tags: [three-sum]
---
## Front
Dieses 3Sum findet bei `[7, 7, -3, -1, 0, 1]` gar nichts. Warum?

```python
nums_s = sorted(nums)
for i, v in enumerate(nums_s):
    if i > 0 and nums[i] == nums[i - 1]:
        continue
    ...
```

## Back
Der Duplikat-Check schaut in `nums` (**unsortiert**) statt in `nums_s`. Bei `i = 1` ist `nums[1] == nums[0]` (7 == 7), also wird übersprungen, und zwar `nums_s[1] = -1`, genau der Start von `[-1, 0, 1]`.

Vorbeugen: in place sortieren mit `nums.sort()`, dann gibt es nur **einen** Namen. Derselbe Fehlertyp bei dir: `target` aus Two Sum landete in 3Sum (#1).
