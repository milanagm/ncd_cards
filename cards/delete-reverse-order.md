---
id: delete-reverse-order
type: gotcha
mistakes: [stack-ops]
evidence: [car-fleet#1, car-fleet#5]
tags: [python, list]
---
## Front
`xs` hat 4 Elemente, `remove = [1, 3]`. Warum crasht das, und wie löschst du richtig?

```python
for i in remove:
    del xs[i]
```

## Back
Nach `del xs[1]` hat `xs` nur noch 3 Elemente, alle dahinter sind **eine Position nach vorn gerutscht**. `xs[3]` gibt es nicht mehr → IndexError. Ginge es gut, würde das falsche Element gelöscht.

Fix: von hinten nach vorn löschen, dann verschiebt jedes `del` nur Elemente, die schon erledigt sind.

```python
for i in reversed(remove):    # remove aufsteigend sortiert
    del xs[i]
```

Oft einfacher: eine neue Liste bauen, `xs = [x for j, x in enumerate(xs) if j not in drop]`.

Deine Frage bei Car Fleet (#4): „how can I delete in reverse order?“ Genau so, mit `reversed(remove)` (#5). Dasselbe Verrutschen kennst du von Evaluate RPN: `del result[-1]` und danach `del result[-2]`.
