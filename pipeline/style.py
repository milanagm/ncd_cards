"""Card CSS shared by the Anki note type, cards.json and the preview page.

Dark mode: Anki desktop and AnkiMobile add `nightMode`, AnkiDroid adds `night_mode`, either on the
card element itself or on an ancestor, so every dark rule covers all four combinations.
"""
from pygments.formatters import HtmlFormatter

DARK = [".card.nightMode", ".card.night_mode", ".nightMode .card", ".night_mode .card"]

BASE = """
.card {
  --fg: #1f2328; --bg: #ffffff; --muted: #59636e; --border: #d1d9e0; --code-bg: #f6f8fa;
  --hl: rgba(255, 190, 0, .30); --mark: rgba(9, 105, 218, .85);
  --p0: #0969da; --p1: #cf222e; --p2: #8250df;
  --pass: #1a7f37; --fail: #cf222e; --crash: #bc4c00; --timeout: #8250df;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  font-size: 18px; line-height: 1.45; text-align: left; color: var(--fg); background: var(--bg);
}
%(dark)s {
  --fg: #e6edf3; --bg: #0d1117; --muted: #9198a1; --border: #3d444d; --code-bg: #161b22;
  --hl: rgba(255, 190, 0, .22); --mark: rgba(88, 166, 255, .85);
  --p0: #58a6ff; --p1: #ff7b72; --p2: #d2a8ff;
  --pass: #3fb950; --fail: #ff7b72; --crash: #ffa657; --timeout: #d2a8ff;
}
.wrap { max-width: 720px; margin: 0 auto; padding: 4px 2px; }
.typ { font-size: 12px; font-weight: 600; letter-spacing: .06em; text-transform: uppercase; color: var(--muted); margin-bottom: 6px; }
p { margin: 8px 0; }
ul, ol { margin: 6px 0; padding-left: 22px; }
li { margin: 3px 0; }
code { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace; font-size: .86em;
  background: var(--code-bg); border: 1px solid var(--border); border-radius: 5px; padding: 0 4px; }
.codehilite { background: var(--code-bg) !important; border: 1px solid var(--border); border-radius: 8px;
  padding: 8px 12px; margin: 10px 0; overflow-x: auto; }
.codehilite pre { margin: 0; font-size: 14px; line-height: 1.5; }
.codehilite code { background: none; border: none; padding: 0; font-size: inherit; }
hr#answer { border: none; border-top: 1px solid var(--border); margin: 16px 0 12px; }
table { border-collapse: collapse; margin: 8px 0; font-size: 15px; }
th, td { border: 1px solid var(--border); padding: 4px 8px; }
.viz { margin: 12px 0; }
.viz svg { display: block; max-width: 100%%; height: auto; margin: 0 auto; }
.viz .cap { text-align: center; font-size: 13px; color: var(--muted); margin-top: 4px; }
.viz .cell { fill: none; stroke: var(--muted); stroke-width: 1.2; }
.viz .cell.hl, .viz .hlfill { fill: var(--hl); }
.viz .markfill { fill: var(--mark); }
.viz .line { stroke: var(--border); stroke-width: 1; }
.viz .line.strong { stroke: var(--fg); stroke-width: 2; }
.viz .t { fill: var(--fg); }
.viz .idx, .viz .lbl { fill: var(--muted); }
.viz .ptr { font-weight: 700; }
.viz .p0 { fill: var(--p0); } .viz .p1 { fill: var(--p1); } .viz .p2 { fill: var(--p2); }
.verlauf { margin-top: 18px; padding-top: 8px; border-top: 1px dashed var(--border); font-size: 13px; color: var(--muted); }
.verlauf .title { font-weight: 600; margin-bottom: 2px; }
.verlauf ul { list-style: none; padding: 0; margin: 0; }
.verlauf li { margin: 4px 0; }
.verlauf a { color: inherit; }
.verlauf code { font-size: 12px; }
.badge { display: inline-block; font-size: 11px; font-weight: 600; border: 1px solid currentColor;
  border-radius: 9px; padding: 0 6px; margin: 0 4px; }
.badge.pass { color: var(--pass); } .badge.fail { color: var(--fail); }
.badge.crash { color: var(--crash); } .badge.timeout { color: var(--timeout); }
"""


def css():
    light = HtmlFormatter(style="xcode").get_style_defs(".codehilite")
    dark = HtmlFormatter(style="github-dark").get_style_defs([f"{sel} .codehilite" for sel in DARK])
    return BASE % {"dark": ", ".join(DARK)} + "\n" + light + "\n" + dark + "\n"
