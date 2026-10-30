---
id: bug-binary-search-single
type: bug
mistakes: [edge-cases]
evidence: [binary-search#2-5, binary-search#6]
tags: [binary-search, edge-cases]
---
## Front
Binary Search: Erwartet `-1` für `nums = [5]`, `target = -5`. Was kommt zurück?

```python
def search(self, nums, target):
    if len(nums)< 2:
        return 0
    i = int(len(nums)/ 2)
    ...
```

## Back
`0`. Der Sonderfall für ein Element gibt **ungeprüft** Index 0 zurück, auch wenn `target` gar nicht drin ist.

Fix in #6: `if nums[0] == target: return 0`, sonst weiter bis `return -1`. Mit einer echten Binary Search (`while l <= r`) braucht es den Sonderfall gar nicht, ein Element ist dann einfach `l == r`.

Vier Versuche (#2–5) liefen an diesem Testfall vorbei, während du an den Schleifen gearbeitet hast.
