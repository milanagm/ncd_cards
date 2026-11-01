---
id: reverse-list-pointers
type: trace
mistakes: [linked-list-nodes, return-type]
evidence: [reverse-a-linked-list#2, reverse-a-linked-list#4-5, reverse-a-linked-list#6-9, reverse-a-linked-list#14]
tags: [linked-list]
---
## Front
Reverse Linked List in place: Welche vier Zuweisungen machst du pro Schritt mit `prev` und `curr`, in welcher Reihenfolge? Was gibst du zurück?

```viz
kind: array
values: [0, 1, 2, 3]
pointers: {prev: 1, curr: 2}
highlight: [0, 1]
caption: "nach 2 Schritten: 1 → 0 → None ist umgedreht, ab 2 noch nicht"
```

## Back
```python
prev, curr = None, head
while curr:
    nxt = curr.next
    curr.next = prev
    prev = curr
    curr = nxt
return prev
```

Erst `curr.next` sichern, sonst ist der Rest der Liste nach dem Umhängen verloren. Am Ende ist `curr` gleich `None`, der neue Kopf ist `prev`.

Am 31.10. hast du zuerst die Werte in eine Python-Liste kopiert und daraus neu gebaut. Dabei: `head.next = p_next` hängt eine Zahl statt eines Knotens an (#4–5), `head.next = initial[p_next]` einen Wert (#6–9), `return reversed(initial)` liefert einen Iterator statt einer Linked List (#2). Neue Knoten gibt es nur mit `ListNode(v)`, der Wert heißt `val`, nicht `value`. Am Abend dann die Lösung oben (#14).
