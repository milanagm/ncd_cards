---
id: typehint-brackets
type: gotcha
mistakes: [call-vs-subscript]
evidence: [two-integer-sum#10-14, two-integer-sum#21]
tags: [python, typing]
---
## Front
Warum crasht diese Klasse schon beim Laden, bevor ein einziger Test läuft?

```python
class Solution:
    def twoSum(self, nums: List(int), target: int) -> List[int]:
        ...
```

## Back
Type-Hints werden mit **eckigen** Klammern parametrisiert: `List[int]`, ab Python 3.9 auch einfach `list[int]`.

`List(int)` *ruft* `typing.List` auf. Python wertet Annotationen schon beim Definieren der Funktion aus (bis Version 3.13), deshalb crasht es vor jedem Test → `TypeError: Type List cannot be instantiated`.

Faustregel: `()` ruft auf, `[]` indiziert oder parametrisiert. Derselbe Dreher bei dir: `sorted[i, j]` statt `sorted([i, j])`.
