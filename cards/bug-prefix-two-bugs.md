---
id: bug-prefix-two-bugs
type: bug
mistakes: [index-vs-value, wrong-variable]
evidence: [products-of-array-discluding-self#2-4, products-of-array-discluding-self#5]
tags: [prefix-sum]
---
## Front
Präfixprodukte für `nums = [1, 2, 4, 6]`: Wo stecken die zwei Fehler?

```python
reli = [1] * len(nums)
prev = 1
for i in reli:
    reli[i] = prev
    prev *= reli[i]
```

## Back
1. `for i in reli` liefert **Werte** (lauter `1`), keine Indizes. Geschrieben wird also immer `reli[1]`. Richtig: `for i in range(len(nums)):`
2. `prev *= reli[i]` multipliziert mit dem eigenen Präfix statt mit dem **Eingabewert** → `prev *= nums[i]`

```python
prefix = [1] * len(nums)
prev = 1
for i in range(len(nums)):
    prefix[i] = prev
    prev *= nums[i]
```
