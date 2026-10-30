---
id: sliding-window-shrink
type: trace
mistakes: [window-shrink]
evidence: [longest-substring-without-duplicates#0-1, longest-substring-without-duplicates#2-4, longest-substring-without-duplicates#18, longest-substring-without-duplicates#19, longest-substring-without-duplicates#20, longest-substring-without-duplicates#21]
tags: [sliding-window, strings]
---
## Front
Longest Substring Without Repeating Characters, `s = "dvdf"`. Das Fenster ist `"dv"`, jetzt kommt bei `r = 2` das zweite `d`. Wohin springt `l`, und was passiert mit Set und Länge?

```viz
kind: array
values: [d, v, d, f]
pointers: {l: 0, r: 2}
highlight: [0, 1]
caption: "Fenster \"dv\", s[2] = d ist schon drin"
```

## Back
`l` rückt nur so weit, bis das alte `d` draußen ist, also auf 1. Das `v` bleibt im Fenster.

```viz
kind: array
values: [d, v, d, f]
pointers: {l: 1, r: 2}
highlight: [1, 2]
caption: "Fenster \"vd\", danach \"vdf\" mit Länge 3"
```

```python
while s[r] in seen:
    seen.remove(s[l])
    l += 1
seen.add(s[r])
best = max(best, r - l + 1)
```

Drei Schritte, in dieser Reihenfolge: schrumpfen, **dann** das neue Zeichen aufnehmen, Länge aus den Pointern berechnen. Deine Zwischenstände am 27.10.: neues Zeichen nicht ins Set (#18), `seen.add(v)` in der while-Schleife → KeyError (#19), Länge nicht neu berechnet (#20). Am Vortag hattest du das Fenster ganz verworfen (`sub = [i]`, #2–4) und bei `"dvdf"` 2 statt 3 bekommen.
