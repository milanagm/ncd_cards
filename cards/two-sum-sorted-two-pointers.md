---
id: two-sum-sorted-two-pointers
type: pattern
mistakes: [constraint-ignored]
evidence: [two-integer-sum-ii#0-2, two-integer-sum-ii#3]
tags: [two-pointers, two-sum]
---
## Front
Two Sum II: Das Array ist **sortiert**, und du darfst nur **O(1) Extraspeicher** benutzen. Welches Pattern, und warum funktioniert es?

## Back
**Two Pointers** von beiden Enden:

- Summe zu klein → `l += 1` (nächstgrößerer Wert)
- Summe zu groß → `r -= 1` (nächstkleinerer Wert)
- getroffen → `[l + 1, r + 1]` (1-indexiert)

Warum nichts verloren geht: Ist `nums[l] + nums[r]` zu groß, passt `nums[r]` zu **keinem** verbleibenden Partner, denn alle sind mindestens `nums[l]`. Also darf `r` raus.

Deine ersten Lösungen (#0–2) nutzten ein Set: korrekt, aber O(n) Speicher, also gegen den Constraint. „Sortiert“ plus „O(1) Speicher“ heißt fast immer Two Pointers.
