---
id: stack-brackets
type: pattern
mistakes: [problem-model, edge-cases]
evidence: [validate-parentheses#0-2, validate-parentheses#3-4, validate-parentheses#5, validate-parentheses#6]
tags: [stack]
---
## Front
Valid Parentheses mit **einem** Stack: Was passiert bei einer schließenden Klammer, und was muss am Ende gelten?

## Back
```python
pairs = {")": "(", "]": "[", "}": "{"}
stack = []
for c in s:
    if c in pairs:
        if not stack or stack.pop() != pairs[c]:
            return False
    else:
        stack.append(c)
return not stack
```

Schließende Klammer: Der Stack darf nicht leer sein, und oben muss die **passende** öffnende liegen. Am Ende muss der Stack leer sein.

Deine drei Stolpersteine am 31.10.:

- `open_plain[-1]` auf leerem Stack → IndexError bei `")"` (#0–2)
- ein Stack pro Klammertyp: die Reihenfolge zwischen den Typen geht verloren, `"[(])"` liefert True (#3–4)
- `return True` ohne Leer-Check: `"("` liefert True (#5)
