---
id: range-exact-n
type: gotcha
mistakes: [off-by-one]
evidence: [string-encode-and-decode#10-11, string-encode-and-decode#12]
tags: [off-by-one]
---
## Front
Du willst genau `n` Zeichen lesen. Wie oft läuft diese Schleife?

```python
c = 0
while c < n - 1:
    word += s[i]
    i += 1
    c += 1
```

## Back
**n − 1** Mal (c = 0 … n − 2), also ein Zeichen zu wenig. `<` schließt die Grenze schon aus, das `- 1` zieht ein zweites Mal ab.

Genau n Mal: `while c < n` oder `for _ in range(n)`. Noch einfacher per Slice: `word = s[i:i + n]`, dann `i += n`.

Dein Kommentar dazu: „< sorgt schon für kleiner, typisches leichtsinnsfehler“.
