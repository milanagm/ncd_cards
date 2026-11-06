---
id: tokens-are-strings
type: gotcha
mistakes: [str-int]
evidence: [evaluate-reverse-polish-notation#1, evaluate-reverse-polish-notation#8, evaluate-reverse-polish-notation#12]
tags: [python, strings]
---
## Front
`tokens = ["1", "2", "+", "3", "*"]`. Was ergibt `tokens[1] + tokens[0]`, und was danach `"3" * "21"`?

## Back
`"21"`: `+` hängt Strings aneinander. Und `"3" * "21"` ist ein `TypeError: can't multiply sequence by non-int of type 'str'`. `str * int` wiederholt, `str * str` gibt es nicht.

Tokens sind Strings. Beim Lesen einmal `int(t)` und nur Zahlen auf den Stack legen.

Genau so in Evaluate RPN #1 und am 5.11. noch einmal in #12. In #8 wurde nur beim Rechnen umgewandelt, deshalb lieferte `["7"]` den String `"7"` statt 7.
