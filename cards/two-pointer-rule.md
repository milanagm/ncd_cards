---
id: two-pointer-rule
type: concept
mistakes: [pointer-movement]
evidence: [is-palindrome#0, is-palindrome#15-16, three-integer-sum#12-13, buy-and-sell-crypto#2]
tags: [two-pointers]
---
## Front
Two Pointers von außen nach innen: Wie lauten Schleifenbedingung und Updates? Und warum nicht `while l != r`?

## Back
```python
l, r = 0, len(s) - 1
while l < r:
    ...
    l += 1
    r -= 1
```

`l` läuft nach rechts, `r` nach links. Bei **gerader** Länge springen sie aneinander vorbei, ohne je gleich zu sein. `!=` wird dann nie falsch, und die Schleife läuft über die Grenzen hinaus.

```viz
kind: array
values: [a, b, b, a]
pointers: {l: 2, r: 1}
highlight: [1, 2]
caption: "nach 2 Schritten: l = 2, r = 1, gekreuzt, aber nie gleich"
```

Am 22.10. hast du zweimal am selben Vormittag `p_r += 1` geschrieben, erst bei Palindrome und eine halbe Stunde später bei 3Sum. Am 25.10. bei Buy and Sell wieder: `p_l -=1` und `p_r +=1`, beide nach außen → IndexError.
