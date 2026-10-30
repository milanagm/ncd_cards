---
id: continue-at-end
type: gotcha
mistakes: [loop-progress]
evidence: [longest-substring-without-duplicates#8]
tags: [python, loops]
---
## Front
Muss am Ende eines `while`-Körpers ein `continue` stehen?

```python
while p == e:
    len_sub += 1
    p += 1
    continue
```

## Back
Nein. Am Ende des Körpers springt die Schleife ohnehin zurück zur Bedingung. `continue` dort ist wirkungslos.

Sinnvoll ist `continue` nur **mitten** im Körper, um den Rest zu überspringen. Genau dort ist es gefährlich: Steht das Pointer-Update dahinter, wird es übersprungen → Endlosschleife (3Sum #20).

Deine Frage im Code: „muss mans am ende der while schleife immer haben?“
