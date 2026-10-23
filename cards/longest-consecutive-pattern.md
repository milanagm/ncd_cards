---
id: longest-consecutive-pattern
type: pattern
mistakes: []
evidence: [longest-consecutive-sequence#11]
tags: [hashset]
---
## Front
Longest Consecutive Sequence in O(n): Welcher Kniff verhindert, dass du jede Sequenz mehrfach abläufst?

## Back
Nur an **Sequenzanfängen** zählen. Eine Zahl `n` startet eine Sequenz genau dann, wenn `n - 1` **nicht** im Set ist. Von dort zählst du hoch, solange der Nachfolger im Set ist.

Jede Zahl wird höchstens zweimal angefasst, einmal in der äußeren Schleife und einmal beim Hochzählen → O(n). Ohne den Check wäre es O(n²).

Sortieren ist nicht nötig. Dass ein Set keine Reihenfolge hat (dein Kommentar: „set erzeugt beliebige Reihenfolge!“), spielt hier keine Rolle.
