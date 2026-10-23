---
id: prefix-suffix-products
type: pattern
mistakes: []
evidence: [products-of-array-discluding-self#0, products-of-array-discluding-self#5]
tags: [prefix-sum]
---
## Front
Product of Array Except Self ohne Division in O(n): Was ist die Idee?

## Back
Für jede Position gilt: **Produkt links davon × Produkt rechts davon**. Zwei Durchläufe, vorwärts für die Präfixe und rückwärts für die Suffixe.

```viz
kind: rows
rows:
  - {label: nums, values: [1, 2, 4, 6]}
  - {label: links, values: [1, 1, 2, 8]}
  - {label: rechts, values: [48, 24, 6, 1]}
  - {label: Ergebnis, values: [48, 24, 12, 8]}
highlight_col: 2
caption: "Index 2: links 1·2 = 2, rechts 6, Ergebnis 12"
```

```python
out = [1] * len(nums)
prefix = 1
for i in range(len(nums)):
    out[i] = prefix
    prefix *= nums[i]
suffix = 1
for i in range(len(nums) - 1, -1, -1):
    out[i] *= suffix
    suffix *= nums[i]
```
