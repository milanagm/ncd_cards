---
id: empty-stack-peek
type: gotcha
mistakes: [edge-cases]
evidence: [validate-parentheses#0-2, minimum-stack#6, minimum-stack#7]
tags: [stack, edge-cases]
---
## Front
Was passiert bei `stack[-1]`, wenn `stack` leer ist? Wie schreibst du den Vergleich mit dem obersten Element sicher?

## Back
`IndexError: list index out of range`. Ein leerer Stack hat kein oberstes Element.

```python
if stack and stack[-1] == "(":
    ...
```

`and` wertet von links aus: Ist `stack` leer, wird `stack[-1]` gar nicht mehr gelesen.

Zweimal bei dir: Valid Parentheses #0–2 (`open_plain[-1]` bei `")"`), Min Stack #6 (`self.min_stack[-1]` beim allerersten `push`, #7 prüft `if self.min_stack:`).
