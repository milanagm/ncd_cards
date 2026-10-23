---
id: bug-shadowing-input
type: bug
mistakes: [wrong-variable]
evidence: [duplicate-integer#13, duplicate-integer#14, duplicate-integer#15]
tags: [shadowing]
---
## Front
Diese Funktion gibt **immer** `False` zurück. Warum?

```python
def hasDuplicate(self, nums):
    nums = set()
    for i in nums:
        if i in nums:
            return True
        nums.add(i)
    return False
```

## Back
`nums = set()` **überschreibt den Input**. Die Schleife läuft über ein leeres Set, betritt nie den Körper und landet bei `return False`.

Im nächsten Versuch hieß das Set richtig `seen`, aber die Prüfung war noch `if i in nums:`, und die ist immer wahr, weil `i` aus `nums` kommt. Regel: Input-Parameter nie neu belegen, Hilfsstrukturen bekommen eigene Namen.
