---
id: list-length-and-backwards
type: gotcha
mistakes: []
evidence: [products-of-array-discluding-self#2, daily-temperatures#4]
tags: [python, list]
---
## Front
Zwei Fragen aus deinem eigenen Code-Kommentar:

1. Wie erzeugst du eine Liste der Länge `n` voller Einsen?
2. Wie läufst du die Indizes **rückwärts** von `n - 1` bis `0`?

## Back
1. `[1] * n`
2. `for i in range(n - 1, -1, -1):`. Das Ende ist exklusiv, deshalb `-1` als Stopp, damit die `0` noch drankommt. Alternative: `for i in reversed(range(n)):`

Am 1.11. bei Daily Temperatures hast du `[0] * len(temperatures)` richtig geschrieben und dazu notiert: „anlegen von arrays einer bestimmten länge vergesse ich immer“.

Vorsicht bei 2D: `[[0] * m] * n` erzeugt n Verweise auf **dieselbe** Zeile. Richtig ist `[[0] * m for _ in range(n)]`.
