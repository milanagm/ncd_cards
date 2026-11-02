---
id: min-stack-pattern
type: pattern
mistakes: [problem-model]
evidence: [minimum-stack#1-3, minimum-stack#5, minimum-stack#7]
tags: [stack]
---
## Front
Min Stack mit `getMin` in O(1): Was speicherst du zusätzlich? Und warum reicht ein Set der gesehenen Werte nicht?

## Back
Einen zweiten Stack, der auf jeder Ebene das **Minimum bis dahin** hält:

```python
def push(self, val):
    self.stack.append(val)
    self.min_stack.append(min(val, self.min_stack[-1]) if self.min_stack else val)

def pop(self):
    self.stack.pop()
    self.min_stack.pop()

def getMin(self):
    return self.min_stack[-1]
```

Mit `pop` verschwindet auch das Minimum dieser Ebene, darunter liegt automatisch das alte.

Das Set (#1–3) vergisst nichts: Nach `push 1, 2, 0` und `pop` liefert `min(self.seen)` weiter 0 statt 1. Doppelte Werte zählt es außerdem nur einmal. #5 bestand mit `min(self.stack)`, das ist aber O(n) pro Aufruf.
