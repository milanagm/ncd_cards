---
id: max-empty-default
type: gotcha
mistakes: [edge-cases]
evidence: [longest-consecutive-sequence#3, longest-consecutive-sequence#4]
tags: [python, edge-cases]
---
## Front
Was passiert bei `max([])`, und wie fängst du die leere Liste ohne `if` ab?

## Back
`ValueError: max() iterable argument is empty`.

Ohne `if`: `max(lengths, default=0)`, genauso bei `min`. Bei Longest Consecutive ist die leere Eingabe ein erlaubter Testfall (`0 <= nums.length`).
