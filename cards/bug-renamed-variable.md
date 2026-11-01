---
id: bug-renamed-variable
type: bug
mistakes: [wrong-variable]
evidence: [binary-search#0-1, reverse-a-linked-list#3, reverse-a-linked-list#13, reverse-a-linked-list#14]
tags: [python, naming]
---
## Front
Wo crasht das, und mit welchem Fehler?

```python
prev, current = None, head

while curr != None:
    temp = current.next
    current.next = prev
    prev = current
    current = temp

return prev
```

## Back
Gleich in der Bedingung: `NameError: name 'curr' is not defined`. Die Variable heißt `current`.

Regel: Nach dem Umbenennen oder Abtippen einer Lösung jeden Namen einmal gegen seine Definition lesen.

Der gleiche Crash bei dir: `return i`, während der Index noch `mitte` hieß (Binary Search #0–1), und `while p > 0` statt `p_next` (Reverse Linked List #3).
