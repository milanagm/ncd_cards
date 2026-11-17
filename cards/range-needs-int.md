---
id: range-needs-int
type: gotcha
mistakes: [method-api]
evidence: [max-water-container#1, max-water-container#2, buy-and-sell-crypto#5, buy-and-sell-crypto#6, buy-and-sell-crypto#7, buy-and-sell-crypto#8, buy-and-sell-crypto#11, buy-and-sell-crypto#12, buy-and-sell-crypto#13, buy-and-sell-crypto#14]
tags: [python, loops]
---
## Front
Was passiert bei `for i in range(prices):`, wenn `prices` eine Liste ist? Was war gemeint?

## Back
`TypeError: 'list' object cannot be interpreted as an integer`. `range` braucht eine **Zahl**, keine Liste.

Gemeint waren die Indizes: `range(len(prices))`. Brauchst du Index und Wert, dann `for i, p in enumerate(prices):`.

Bei dir: `range(heights)` bei Container With Most Water (#1, 24.10.) und `range(prices)` bei Buy and Sell (#5 am 6.11., #7 am 13.11., #11 und #13 am 16.11.). Dazwischen `range(enumerate(prices))` (#12): `enumerate` liefert Paare, auch das ist keine Zahl. #14 mit `range(len(prices))` ✔
