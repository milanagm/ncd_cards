---
id: bug-anagram-copy-paste
type: bug
mistakes: [wrong-variable]
evidence: [is-anagram#0, is-anagram#2]
tags: [copy-paste]
---
## Front
`isAnagram("jar", "jam")` liefert `True`. Wo ist der Fehler?

```python
dict_count_s = {}
for letter in s:
    dict_count_s[letter] = dict_count_s.get(letter, 0) + 1

dict_count_t = {}
for letter in s:
    dict_count_t[letter] = dict_count_t.get(letter, 0) + 1

return dict_count_s == dict_count_t
```

## Back
Die zweite Schleife läuft über `s` statt `t`. Beide Dicts zählen dieselben Buchstaben und sind immer gleich, ein klassischer **Copy-Paste-Fehler**.

Vorbeugen: doppelten Code in eine Funktion auslagern (`count(word)`, hast du in #2 gemacht) oder gleich `Counter(s) == Counter(t)`.
