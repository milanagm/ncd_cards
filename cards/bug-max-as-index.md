---
id: bug-max-as-index
type: bug
mistakes: [index-vs-value]
evidence: [longest-consecutive-sequence#2]
tags: [python]
---
## Front
Was gibt diese Zeile für `all_seq_lengths = [1, 4, 1, 2, 3]` zurück, und was war gemeint?

```python
return all_seq_lengths[max(all_seq_lengths)]
```

## Back
`max(...)` ist `4`, und `all_seq_lengths[4]` ist `3`. Zurück kommt also **3** statt 4. Wäre das Maximum größer als die Liste lang ist, gäbe es einen `IndexError`.

`max()` liefert bereits den **Wert**. Gemeint war `return max(all_seq_lengths)`, bei möglicherweise leerer Liste `max(all_seq_lengths, default=0)`.
