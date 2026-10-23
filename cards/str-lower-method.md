---
id: str-lower-method
type: gotcha
mistakes: [method-api]
evidence: [is-palindrome#4, is-palindrome#5]
tags: [python, strings]
---
## Front
Du willst `s` kleinschreiben. Was ist an den beiden Versuchen jeweils falsch?

```python
s = lower(s)
s = s.lower(s)
```

## Back
- `lower` ist eine **String-Methode**, kein Builtin → `NameError: name 'lower' is not defined`
- Eine Methode bekommt das Objekt automatisch als `self`. `s.lower(s)` übergibt es ein zweites Mal → `TypeError: str.lower() takes no arguments (1 given)`

Richtig: `s = s.lower()`. Strings sind unveränderlich, die Methode liefert einen **neuen** String, deshalb die Zuweisung.
