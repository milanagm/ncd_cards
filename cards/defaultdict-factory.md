---
id: defaultdict-factory
type: gotcha
mistakes: [call-vs-subscript]
evidence: [anagram-groups#14-16, anagram-groups#17-18, anagram-groups#25-26, anagram-groups#27]
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

Mit einem normalen Dict geht es mit `setdefault`: `groups.setdefault(key, []).append(w)` legt beim ersten Mal die leere Liste an. Das war die Antwort auf deine Frage „wie war hier die richtige syntax?“ (Anagram Groups #25, gelöst in #27). `groups[groups.get(key, 0)]` benutzt dagegen das Ergebnis von `get` als Key.
