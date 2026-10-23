---
id: unhashable-list
type: concept
mistakes: [hashability]
evidence: [three-integer-sum#4, three-integer-sum#6]
tags: [python, hashing]
---
## Front
Warum crasht `set(answer)`, wenn `answer` eine Liste von Tripeln wie `[-1, 0, 1]` ist? Wie dedupliziert man Tripel stattdessen?

## Back
Set-Elemente und Dict-Keys müssen **hashbar** sein, also unveränderlich. Listen sind veränderlich → `TypeError: unhashable type: 'list'`.

- Tupel statt Listen: `set(tuple(t) for t in answer)`
- bei 3Sum besser: Duplikate gar nicht erst erzeugen (sortieren, gleiche Werte überspringen)

Dasselbe gilt für Dict-Keys: `sorted(word)` liefert eine Liste → als Key `tuple(sorted(word))` oder `"".join(sorted(word))`.
