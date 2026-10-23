---
id: defaultdict-factory
type: gotcha
mistakes: [call-vs-subscript]
evidence: [anagram-groups#14-16, anagram-groups#17-18]
tags: [python, defaultdict]
---
## Front
Welche Zeile funktioniert, und warum crashen die anderen beiden?

```python
groups = defaultdict(list())
groups = defaultdict(List(str))
groups = defaultdict(list)
```

## Back
Nur `defaultdict(list)`.

`defaultdict` bekommt eine **Fabrik**: etwas Aufrufbares, das bei jedem fehlenden Key einen neuen Startwert erzeugt. `list` ist diese Fabrik. `list()` ist dagegen schon eine fertige Liste → `TypeError: first argument must be callable or None`. `List(str)` versucht `typing.List` aufzurufen → `TypeError: Type List cannot be instantiated`.

Gleiches Prinzip: `defaultdict(int)` zählt ab 0, `defaultdict(set)` sammelt ohne Duplikate.
