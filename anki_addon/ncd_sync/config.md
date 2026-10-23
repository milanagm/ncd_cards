**NeetCode Insights Sync** holt neue und geänderte Karten aus [milanagm/ncd_cards](https://github.com/milanagm/ncd_cards).

- `cards_url`, `deck_url`: Quelle der Karten. Das Deck wird nur beim allerersten Lauf importiert.
- `interval_hours`: wie oft das Add-on prüft, solange Anki offen ist. Zusätzlich läuft es nach jedem Sync.
- `min_minutes_between_runs`: Mindestabstand zwischen automatischen Läufen.
- `reschedule_recurring`: Kommt ein Fehler in einer neuen Submission wieder vor, wird die passende Karte heute fällig.
- `sync_after_update`: nach Änderungen sofort mit AnkiWeb synchronisieren, damit das Handy sie bekommt.

In Anki selbst geänderte Karten werden erst überschrieben, wenn sich die Karte im Repo ändert. Gelöschte Karten kommen nicht wieder.
