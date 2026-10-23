---
id: parse-multidigit-length
type: bug
mistakes: [length-prefix-parsing]
evidence: [string-encode-and-decode#3, string-encode-and-decode#4, string-encode-and-decode#5]
tags: [strings, parsing]
---
## Front
Welche Eingabe bricht diesen Decoder?

```python
while i < len(s):
    l_w = int(s[i])
    i += 2
    word = ""
    for j in range(l_w):
        word += s[i]
        i += 1
    decoded.append(word)
```

## Back
Jedes Wort mit **10 oder mehr** Zeichen. Die Länge hat dann zwei Ziffern, `int(s[i])` liest nur die erste, und danach verrutscht alles, bis `int("x")` crasht.

Auch falsch: Ziffern addieren (`l_w += int(s[i])`), dann wird aus „12“ eine 3. Richtig ist, bis zum `#` zu lesen und den ganzen Teilstring umzuwandeln:

```python
j = i
while s[j] != "#":
    j += 1
n = int(s[i:j])
decoded.append(s[j + 1 : j + 1 + n])
i = j + 1 + n
```
