---
id: empty-set-literal
type: gotcha
mistakes: [container-choice]
evidence: [valid-sudoku#0, valid-sudoku#1-4, duplicate-integer#1]
tags: [python, set]
---
## Front
Welche Zeile erzeugt ein leeres Set?

```python
seen = {}
seen = ()
seen = []
seen = set()
```

## Back
Nur `set()`.

`{}` ist ein leeres **Dict**, `()` ein leeres **Tupel**, `[]` eine leere **Liste**. Mit Inhalt ist `{1, 2}` zwar ein Set, aber leere geschweifte Klammern gehören dem Dict.

Methoden: `seen.add(x)` beim Set, `xs.append(x)` bei der Liste. Dict und Tupel haben kein `add` → `AttributeError`. Dein Kommentar beim ersten Versuch: „ich glaube falsche syntax“.
