---
id: palindrome-two-pointers
type: pattern
mistakes: [skip-irrelevant, pointer-movement]
evidence: [is-palindrome#3-6, is-palindrome#8, is-palindrome#15-20, is-palindrome#21]
tags: [two-pointers, strings]
---
## Front
Valid Palindrome mit Two Pointers: Welche zwei Normalisierungen brauchst du, und wo genau prüfst du die Grenzen?

## Back
```python
l, r = 0, len(s) - 1
while l < r:
    while l < r and not s[l].isalnum():
        l += 1
    while l < r and not s[r].isalnum():
        r -= 1
    if s[l].lower() != s[r].lower():
        return False
    l += 1
    r -= 1
return True
```

1. **Alles** Nicht-Alphanumerische überspringen, nicht nur `.`
2. **Groß/Klein ignorieren**: `.lower()` beim Vergleich
3. Auch die inneren Skip-Schleifen brauchen `l < r`, sonst `IndexError` bei `".,"`

O(n) Zeit, O(1) Speicher, keine Hilfslisten.
