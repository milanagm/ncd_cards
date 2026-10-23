---
id: top-k-bucket-sort
type: pattern
mistakes: []
evidence: [top-k-elements-in-list#0, top-k-elements-in-list#13]
tags: [bucket-sort, heap]
---
## Front
Top K Frequent Elements in **O(n)** statt O(n log n): Wie geht das?

## Back
**Bucket Sort nach Häufigkeit.** Eine Häufigkeit liegt immer zwischen 1 und n, also reichen n + 1 Eimer.

```python
count = Counter(nums)
buckets = [[] for _ in range(len(nums) + 1)]
for value, freq in count.items():
    buckets[freq].append(value)
result = []
for freq in range(len(buckets) - 1, 0, -1):
    for value in buckets[freq]:
        result.append(value)
        if len(result) == k:
            return result
```

Alle deine 12 Versuche haben nach Häufigkeit **sortiert** (O(n log n)). Das ist korrekt und im Interview oft okay, aber O(n) ist die typische Nachfrage. Mittelweg: `heapq.nlargest(k, count, key=count.get)` mit O(n log k).
