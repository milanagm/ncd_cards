---
id: stack-pop-operands
type: bug
mistakes: [stack-ops]
evidence: [evaluate-reverse-polish-notation#3, evaluate-reverse-polish-notation#4-7, evaluate-reverse-polish-notation#8, evaluate-reverse-polish-notation#11, evaluate-reverse-polish-notation#13-14, evaluate-reverse-polish-notation#15]
tags: [stack]
---
## Front
Evaluate RPN, `tokens = ["1", "2", "+", ...]`: Beim `+` steht `result = ["1", "2"]`. Wo crasht das?

```python
a= int(result[-1])
b= int(result[-2])
del result[-1]
del result[-2]
```

## Back
In der letzten Zeile. Nach `del result[-1]` ist nur noch `["1"]` übrig, `result[-2]` gibt es nicht mehr → IndexError. Negative Indizes zählen vom **aktuellen** Ende; jedes Löschen verschiebt sie.

Einfacher mit `pop()`, das liest und entfernt in einem Schritt:

```python
b = stack.pop()
a = stack.pop()
stack.append(a - b)
```

Das zuerst geholte Element ist der **rechte** Operand. Bei dir kostete das am 1.11. fünf Versuche (#3–7); #8 löscht zweimal `[-1]`.

Beim zweiten Anlauf am 5.11. beides noch einmal: `stack[-2]` nach dem `del` → IndexError (#11), dann landete das obere Element in `a`, also links: `4 - 9` ergab -5 statt 5 (#13–14). #15 holt zuerst `b` ✔
