---
id: longest-consecutive-pattern
type: pattern
mistakes: [problem-model]
evidence: [longest-consecutive-sequence#11, longest-consecutive-sequence#15-18, longest-consecutive-sequence#19, longest-consecutive-sequence#21-23, longest-consecutive-sequence#24]
tags: [hashset]
---
## Front
Longest Consecutive Sequence in O(n): Welcher Kniff verhindert, dass du jede Sequenz mehrfach abläufst?

## Back
Nur an **Sequenzanfängen** zählen. Eine Zahl `n` startet eine Sequenz genau dann, wenn `n - 1` **nicht** im Set ist. Von dort zählst du hoch, solange der Nachfolger im Set ist.

Jede Zahl wird höchstens zweimal angefasst, einmal in der äußeren Schleife und einmal beim Hochzählen → O(n). Ohne den Check wäre es O(n²).

Beim zweiten Anlauf am 14.11. stand im Check `... not in seen` statt `... - 1 not in seen` (#15–18). Nach `seen = set(nums)` ist jede Zahl drin, der Check ist also immer falsch, und es wird nie gezählt (#18 lieferte 0). #19 prüft den Vorgänger ✔

Zweimal blieb das Set dabei leer: `seen = set()` (#13–14) und zwei Tage später `seen = []` (#21–23). Dann fehlt jeder Vorgänger, jede Zahl gilt als Sequenzanfang, und es wird nie weitergezählt. Das Set muss vorher alle Zahlen enthalten: `seen = set(nums)` (#24).

Sortieren ist nicht nötig. Dass ein Set keine Reihenfolge hat (dein Kommentar: „set erzeugt beliebige Reihenfolge!“), spielt hier keine Rolle.
