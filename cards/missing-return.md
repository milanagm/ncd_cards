---
id: missing-return
type: gotcha
mistakes: [edge-cases]
evidence: [valid-sudoku#5-6]
tags: [python]
---
## Front
Was gibt eine Python-Funktion zurück, die ohne `return` am Ende ankommt? Und warum ist das bei `isValidSudoku` ein Fehler?

## Back
`None`. Der Judge erwartet `True` für ein gültiges Board, und `None` ist nicht `True`. Das Ergebnis ist also falsch, obwohl alle Prüfungen korrekt durchlaufen.

Check vor dem Abschicken: Endet **jeder** Pfad mit einem `return` des richtigen Typs?
