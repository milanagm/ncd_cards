---
id: buy-sell-running-min
type: pattern
mistakes: [problem-model, pointer-movement]
evidence: [buy-and-sell-crypto#0-2, buy-and-sell-crypto#3]
tags: [sliding-window]
---
## Front
Best Time to Buy and Sell: Warum passen Two Pointers von außen nach innen hier nicht? Wie geht es in einem Durchlauf?

## Back
Gekauft wird **vor** dem Verkauf. Von außen nach innen gibt es keine Regel, welcher Pointer sich bewegen darf, ohne das beste Paar zu verpassen.

Stattdessen von links nach rechts: das **bisherige Minimum** merken und an jedem Tag den Verkauf dagegen rechnen.

```python
buy = 0
profit = 0
for sell in range(1, len(prices)):
    profit = max(profit, prices[sell] - prices[buy])
    if prices[sell] < prices[buy]:
        buy = sell
return profit
```

So hast du es in #3 gelöst. Davor: `prices[p_l] -= 1` änderte die Preise statt der Pointer → Timeout (#0–1), dann liefen beide Pointer nach außen → IndexError (#2).
