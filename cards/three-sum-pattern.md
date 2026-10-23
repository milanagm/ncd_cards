---
id: three-sum-pattern
type: pattern
mistakes: []
evidence: [three-integer-sum#23]
tags: [two-pointers, three-sum]
---
## Front
3Sum: Wie sieht das Gerüst in vier Schritten aus, und welche Laufzeit hat es?

## Back
1. **Sortieren**
2. Für jedes `i`: gleiche Werte wie beim Vorgänger überspringen, bei `nums[i] > 0` abbrechen
3. **Two Pointers** `l = i + 1`, `r = n - 1` suchen Paare mit Summe `-nums[i]`
4. Bei einem Treffer speichern, **beide** Pointer bewegen und gleiche Werte überspringen

```viz
kind: array
values: [-4, -1, -1, 0, 1, 2]
pointers: {i: 1, l: 2, r: 5}
highlight: [1, 2, 5]
caption: "i = 1 fix: -1 + (-1) + 2 = 0 → Treffer"
```

Laufzeit O(n²). Durch das Überspringen braucht es weder ein Set noch `not in answer`.
