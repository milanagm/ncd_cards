---
id: anagram-canonical-key
type: concept
mistakes: [hashability, wrong-variable]
evidence: [anagram-groups#19-20, anagram-groups#21-22]
tags: [hashmap, strings]
---
## Front
Group Anagrams: Welcher Key bringt `"eat"`, `"tea"` und `"ate"` in dieselbe Gruppe? Und warum geht `sorted(word)` nicht direkt als Key?

## Back
Ein **kanonischer Key**, der für alle Anagramme gleich ist:

- `"".join(sorted(word))` → `"aet"`, O(k log k)
- oder ein Tupel mit 26 Buchstaben-Zählern, O(k)

`sorted()` liefert immer eine **Liste** (dein eigener Kommentar: „sorted gibt immer eine Liste zurück!“), und Listen sind als Key nicht erlaubt.

```python
groups = defaultdict(list)
for w in strs:
    groups["".join(sorted(w))].append(w)
return list(groups.values())
```
