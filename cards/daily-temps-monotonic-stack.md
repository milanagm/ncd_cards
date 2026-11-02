---
id: daily-temps-monotonic-stack
type: trace
mistakes: []
evidence: [daily-temperatures#2, daily-temperatures#3]
tags: [stack]
---
## Front
Daily Temperatures mit Stack, `[30, 38, 30, 36, 35, 40, 28]`. Bei `i = 5` (40) liegen die Indizes `1, 3, 4` auf dem Stack. Was passiert jetzt?

```viz
kind: array
values: [30, 38, 30, 36, 35, 40, 28]
pointers: {i: 5}
highlight: [1, 3, 4]
caption: "auf dem Stack: Tage, die noch auf einen wärmeren warten"
```

## Back
Solange oben ein **kälterer** Tag liegt, wird er herausgenommen und bekommt seine Antwort `i - j`: Index 4 → 1, Index 3 → 2, Index 1 → 4. Dann kommt 5 selbst auf den Stack.

```python
result = [0] * len(temperatures)
waiting = []
for i, v in enumerate(temperatures):
    while waiting and v > temperatures[waiting[-1]]:
        j = waiting.pop()
        result[j] = i - j
    waiting.append(i)
```

Die Temperaturen auf dem Stack fallen von unten nach oben (**monotoner Stack**). Jeder Index kommt einmal hinein und einmal heraus: O(n) statt O(n²) wie bei deinem Doppelschleifen-Ansatz (#2).
