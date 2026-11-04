---
id: min-on-nodes
type: gotcha
mistakes: [linked-list-nodes]
evidence: [merge-two-sorted-linked-lists#2, merge-two-sorted-linked-lists#3]
tags: [python, linked-list]
---
## Front
`list1` und `list2` sind `ListNode`s. Was liefert `min(list1, list2)`: den Knoten mit dem kleineren `val`?

## Back
Nein, einen `TypeError: '<' not supported between instances of 'ListNode' and 'ListNode'`. `min` vergleicht die Objekte selbst mit `<`, und `ListNode` definiert keinen Vergleich. Auf `.val` greift es nicht von allein zu.

Den Wert explizit vergleichen:

```python
if list1.val <= list2.val:
    current.next = list1
    list1 = list1.next
```

Oder `min(list1, list2, key=lambda n: n.val)`, wenn es unbedingt `min` sein soll.

Deine Frage im Code (Merge Two Sorted Lists #2): „greift er dann auf list.val zu?“ #3 vergleicht `.val` und besteht.
