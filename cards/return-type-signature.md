---
id: return-type-signature
type: concept
mistakes: [return-type]
evidence: [reverse-a-linked-list#2, reverse-a-linked-list#0-11, evaluate-reverse-polish-notation#1-6, evaluate-reverse-polish-notation#9]
tags: [python]
---
## Front
`def evalRPN(self, tokens) -> int:`. Dein Stack am Ende ist `[5]`. Was gibst du zurück, und was kommt bei `return stack` heraus?

## Back
`return stack[-1]` (oder `stack.pop()`), also die Zahl 5. `return stack` liefert die Liste `[5]`, und `[5] != 5`.

Die Signatur sagt, was zurückkommt. Vor dem Abschicken das `return` gegen `-> ...` lesen:

- Evaluate RPN: ganzer Stack zurück (#2, #9: `[5]`)
- Reverse Linked List, `-> Optional[ListNode]`: `reversed(initial)` ist ein Iterator (#2), `return []` für die leere Liste statt `None` (#11)
