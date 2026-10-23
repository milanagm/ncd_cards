---
id: membership-complexity
type: concept
mistakes: [list-lookup-complexity]
evidence: [duplicate-integer#1-3, duplicate-integer#4, duplicate-integer#8, duplicate-integer#11, two-integer-sum#1-8]
tags: [complexity, set]
---
## Front
Laufzeit von `x in xs`, wenn `xs` eine Liste, ein Set oder ein Dict ist? Was heißt das in einer Schleife über n Elemente?

## Back
| Container | `x in ...` |
|---|---|
| Liste | O(n), linear durchsuchen |
| Set | O(1) im Mittel (Hash) |
| Dict (Keys) | O(1) im Mittel (Hash) |

In einer Schleife: Liste → **O(n²)**, Set oder Dict → **O(n)**. Für „habe ich das schon gesehen?“ also immer `seen = set()` und `seen.add(x)`.

Bei Contains Duplicate hast du sechsmal eine Liste als Gedächtnis benutzt, bei Two Sum 29-mal `in nums`.
