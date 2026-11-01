---
id: binary-search-template
type: concept
mistakes: [binary-search-mid]
evidence: [binary-search#0-1, binary-search#2-6, search-2d-matrix#1-2, search-2d-matrix#2-3, search-2d-matrix#4, search-2d-matrix#11-12, search-2d-matrix#13-16, search-2d-matrix#17]
tags: [binary-search]
---
## Front
Binary Search auf einem sortierten Array: Wie berechnest du `mid`, und was änderst du nach dem Vergleich, `mid` oder die Grenzen?

## Back
```python
l, r = 0, len(nums) - 1
while l <= r:
    mid = (l + r) // 2
    if nums[mid] == target:
        return mid
    if nums[mid] < target:
        l = mid + 1
    else:
        r = mid - 1
return -1
```

`mid` wird in **jeder Runde neu** aus `l` und `r` berechnet. Verschoben werden nur die **Grenzen**, so halbiert sich der Suchbereich: O(log n).

```viz
kind: array
values: [-1, 0, 2, 4, 6, 8]
pointers: {l: 3, mid: 4, r: 5}
highlight: [3, 4, 5]
caption: "target 8: nach Runde 1 (mid = 2, nums[2] = 2 < 8) ist l = 3; jetzt mid = (3 + 5) // 2 = 4"
```

Deine Versuche am 28.10.:

- Binary Search #0–6: `mitte -= 1` bzw. `i -= 1` läuft in Einerschritten, also O(n). #6 besteht so, ist aber keine Binary Search.
- Search 2D Matrix #1–2: `mid -= 1` statt `r_row = mid - 1`
- #2–3: `(l_row - r_row) / 2` ist negativ, #4: `(r_row - l_row) / 2` vergisst das `l_row +`

Am 31.10. bei Search 2D Matrix noch einmal: `l_col + (l_col + r_col) // 2` (#11–12), dann `l_col + (l_col - r_col) // 2`, wieder negativ (#13–16), und `r_col = r_col - 1` statt `col - 1` (#11–14). #17 ✔
