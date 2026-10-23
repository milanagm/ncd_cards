---
id: encode-length-prefix
type: concept
mistakes: [length-prefix-parsing]
evidence: [string-encode-and-decode#0, string-encode-and-decode#1]
tags: [strings, encoding]
---
## Front
Warum reicht ein Trennzeichen wie `#` nicht, um `["a#b", "12#"]` in einen String zu kodieren? Wie geht es robust?

## Back
Das Trennzeichen kann im Inhalt vorkommen: `a#b#12##` lässt sich nicht eindeutig zurückübersetzen.

**Längenpräfix:** vor jedes Wort `str(len(wort)) + "#"`. Der Decoder liest Ziffern bis zum `#` und danach **genau so viele** Zeichen. Was im Wort steht, ist egal, auch `#` und Ziffern.

`["a#b", "12#"]` → `3#a#b3#12#`
