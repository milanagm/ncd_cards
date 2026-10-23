---
id: bug-always-true-condition
type: bug
mistakes: [loop-progress]
evidence: [longest-consecutive-sequence#0, longest-consecutive-sequence#1]
tags: [loops]
---
## Front
Was ist mit dieser Schleifenbedingung los?

```python
for i in nums_s:
    sub_seq.append(i)
    while (i+1) - i == 1:
        sub_seq.append(i+1)
        i += 1
```

## Back
`(i+1) - i` ist **immer** 1. Die Bedingung prüft nichts über die Daten → Endlosschleife.

Gemeint war: Gibt es den Nachfolger? → `while i + 1 in num_set:`. Das hast du im nächsten Versuch direkt korrigiert.
