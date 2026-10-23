---
id: bug-items-tuples
type: bug
mistakes: [index-vs-value]
evidence: [top-k-elements-in-list#9-11, top-k-elements-in-list#12, top-k-elements-in-list#13]
tags: [python, dict]
---
## Front
Erwartet `[3, 2]`, zurück kommt `[(3, 3), (2, 2)]`. Wo liegt der Fehler?

```python
counter = defaultdict(int)
for n in nums:
    counter[n] += 1
s_counter = sorted(counter.items(), key=lambda x: x[1], reverse=True)
answer = []
for i in range(k):
    answer.append(s_counter[i])
```

## Back
`counter.items()` liefert **(Wert, Anzahl)-Tupel**, nach dem Sortieren ist jedes Element so ein Tupel. Gebraucht wird nur der Wert: `answer.append(s_counter[i][0])`, kürzer `[v for v, _ in s_counter[:k]]`.

Davor bei dir: `s_counter.index(i)` sucht die *Position* eines Elements `i`, statt das Element an Position `i` zu lesen → `ValueError: 0 is not in list`.
