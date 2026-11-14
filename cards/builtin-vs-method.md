---
id: builtin-vs-method
type: gotcha
mistakes: [method-api]
evidence: [is-palindrome#4, is-palindrome#5, anagram-groups#25-26, anagram-groups#27, is-palindrome#24]
tags: [python, strings]
---
## Front
`s` ist ein String. Welche dieser Aufrufe gibt es, und was liefern sie?

```python-nocheck
sorted(s)
s.sorted()
s.sort()
s.lower()
lower(s)
```

## Back
- `sorted(s)` ✔ Builtin, nimmt jedes Iterable und liefert eine **Liste** der Zeichen. Zurück zum String mit `"".join(sorted(s))`.
- `s.sorted()` und `s.sort()` ✘ Strings haben keine Sortier-Methode → AttributeError. `.sort()` gibt es nur für Listen, sortiert in place und liefert `None`.
- `s.lower()` ✔ Methode des Strings.
- `lower(s)` ✘ Es gibt kein Builtin `lower` → NameError.

Faustregel: Builtins wie `len`, `sorted`, `max`, `sum` bekommen das Objekt als **Argument**. Methoden hängen am Objekt und gehören zu seinem Typ.

Bei dir: `lower(s)` und `s.lower(s)` (Palindrome #4–5), `i.sorted()` (Anagram Groups #25–26, 13.11.) und am selben Tag `l_p.allnum` und `.small()` (Palindrome #24). Die Methoden heißen `isalnum()` und `lower()`, und sie gehören an das Zeichen `s[l_p]`, nicht an den Index.
