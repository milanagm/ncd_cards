---
id: car-fleet-pattern
type: pattern
mistakes: [problem-model]
evidence: [car-fleet#0-6, car-fleet#7]
tags: [stack, sorting]
---
## Front
Car Fleet: Statt die Autos Schritt für Schritt fahren zu lassen, was rechnest du für jedes Auto aus? In welcher Reihenfolge gehst du die Autos durch, und wann beginnt eine neue Flotte?

## Back
Die **Ankunftszeit** ohne Hindernis: `(target - p) / s`.

Die Autos gehst du **von vorn nach hinten** durch, sortiert nach Position absteigend, als Paare: `sorted(zip(position, speed), reverse=True)`. Ein Auto, das später ankommen würde als die Flotte direkt vor ihm, kann sie nicht einholen und bildet eine **neue Flotte**. Kommt es früher oder gleichzeitig an, holt es sie ein und fährt in ihr mit.

```python
fleets, slowest = 0, 0
for p, s in sorted(zip(position, speed), reverse=True):
    t = (target - p) / s
    if t > slowest:
        fleets += 1
        slowest = t
return fleets
```

Beispiel: `target = 12`, Positionen 10, 8, 5, 3, 0 mit Zeiten 1, 1, 7, 3, 12 → neue Flotten bei 10, 5 und 0, also 3.

Deine Versuche #0–6 simulierten Schritt für Schritt und scheiterten an Indizes (`i+1` am Ende, Löschen beim Durchlaufen). In #3–5 wurden außerdem `position` und `speed` **einzeln** sortiert, dabei gehen die Paare verloren. #7 ✔
