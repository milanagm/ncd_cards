---
id: ceil-division
type: gotcha
mistakes: [ceil-division]
evidence: [eating-bananas#1-2, eating-bananas#3-6, eating-bananas#7]
tags: [python, binary-search]
---
## Front
Koko isst mit Tempo `k` pro Stunde. Wie viele Stunden braucht sie für einen Stapel mit `i` Bananen, als Ganzzahl-Ausdruck? Und was rechnet `i + (k-1) // k`?

## Back
`(i + k - 1) // k`, also `i / k` **aufgerundet**. Ebenso `math.ceil(i / k)`.

`i + (k-1) // k` rechnet etwas anderes: `//` bindet stärker als `+`, also `i + ((k-1) // k)`. Weil `k - 1 < k`, ist der zweite Teil immer 0, das Ergebnis ist `i`.

Deine Versuche am 31.10.:

- #1–2: `i // k` rundet ab (Kommentar: „rundet wohl ab“)
- #3–6: `i + (k-1) // k` („der ganzzahl trick“), bei `[1, 4, 3, 2]`, h = 9 kam deshalb immer 4 statt 2
- #7: `(i + (k-1)) // k` ✔
