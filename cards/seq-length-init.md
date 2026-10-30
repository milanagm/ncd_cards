---
id: seq-length-init
type: bug
mistakes: [off-by-one]
evidence: [longest-consecutive-sequence#7-9, longest-consecutive-sequence#10, longest-consecutive-sequence#11, longest-repeating-substring-with-replacement#2-5]
tags: [longest-consecutive]
---
## Front
Longest Consecutive: Bei manchen Eingaben ist das Ergebnis um 1 zu klein. Wo?

```python
length = 1
for n in num_set:
    if n - 1 not in num_set:
        while n + 1 in num_set:
            length += 1
            n += 1
        lengths.append(length)
        length = 0
```

## Back
Der Reset setzt `length = 0`, aber jede Sequenz enthält ihr **Startelement**, die Länge beginnt also bei 1. Nur die zuerst gefundene Sequenz stimmt. Ob das in Tests auffällt, hängt von der Reihenfolge im Set ab.

Robuster: den Zähler **dort** setzen, wo die Sequenz beginnt.

```python
for n in num_set:
    if n - 1 not in num_set:
        length = 1
        while n + length in num_set:
            length += 1
        best = max(best, length)
```

Das hat bei dir vier Versuche gekostet (#7–10). Am 26.10. wieder, bei Longest Repeating Character Replacement: `sub_len = 0` für ein Fenster, das schon sein Startzeichen enthält (#2–5); #6 startet mit 1.
