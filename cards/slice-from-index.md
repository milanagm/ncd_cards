---
id: slice-from-index
type: gotcha
mistakes: [window-shrink]
evidence: [longest-substring-without-duplicates#7]
tags: [python, slicing]
---
## Front
`sub = ["d", "v"]`, das nächste Zeichen ist `"d"`. Was ergibt `sub[sub.index("d") + 1:] + ["d"]`?

## Back
`["v", "d"]`.

- `sub.index("d")` → 0, die Position des alten `d`
- `sub[1:]` → alles **ab** Index 1 bis zum Ende: `["v"]`
- `+ ["d"]` hängt das neue Zeichen an

Slice-Schreibweise: `xs[start:stop]`, `start` inklusive, `stop` exklusiv; fehlt eine Grenze, gilt Anfang bzw. Ende. Ergebnis ist eine **neue** Liste.

Damit hast du Longest Substring am 26.10. gelöst (#7), mit der Notiz „lerne wie man sliced! schreibweise merken!“
