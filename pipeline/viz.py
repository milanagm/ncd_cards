"""Small SVG diagrams for cards, declared in Markdown as ```viz blocks holding YAML.

kind: array  values, pointers {label: index}, highlight [indices], caption
kind: grid   size, box, mark [r, c], shade_box (bool), caption
kind: rows   rows [{label, values}], highlight_col, caption

Colors come from CSS classes (see style.py), so the diagrams follow Anki's light and dark mode.
Every diagram is emitted on a single line: Markdown only passes raw HTML through as a block when
it contains no blank lines.
"""
from html import escape

FONT = 'font-family="ui-monospace, Menlo, Consolas, monospace"'
POINTER_COLORS = {"l": 0, "r": 1, "i": 2}  # same pointer, same color on every card


def _text(x, y, s, cls="t", size=14, anchor="middle"):
    return (f'<text x="{x}" y="{y}" class="{cls}" font-size="{size}" text-anchor="{anchor}" '
            f'dominant-baseline="middle" {FONT}>{escape(str(s))}</text>')


def _svg(width, height, parts, caption):
    """Natural-size SVG (shrinks on narrow screens, never blows up) with an HTML caption that wraps."""
    body = "".join(parts)
    svg = (f'<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" '
           f'xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{escape(caption or "Diagramm")}">'
           f"{body}</svg>")
    return svg + (f'<div class="cap">{escape(caption)}</div>' if caption else "")


def array(values, pointers=None, highlight=(), caption=None):
    cell, pad, top = 46, 12, 22
    n = len(values)
    width = pad * 2 + n * cell
    labels_by_cell = {}
    for order, (label, idx) in enumerate((pointers or {}).items()):
        color = POINTER_COLORS.get(label, order % 3)
        labels_by_cell.setdefault(idx, []).append((label, color))
    pointer_rows = max((len(v) for v in labels_by_cell.values()), default=0)
    height = top + cell + 6 + pointer_rows * 22
    parts = []
    for i, v in enumerate(values):
        x = pad + i * cell
        cls = "cell hl" if i in highlight else "cell"
        parts.append(f'<rect x="{x}" y="{top}" width="{cell}" height="{cell}" class="{cls}"/>')
        parts.append(_text(x + cell / 2, top + cell / 2, v, size=16))
        parts.append(_text(x + cell / 2, top - 10, i, cls="idx", size=11))
    for idx, labels in labels_by_cell.items():
        x = pad + idx * cell + cell / 2
        for row, (label, color) in enumerate(labels):
            y = top + cell + 16 + row * 22
            parts.append(_text(x, y, f"▲ {label}", cls=f"ptr p{color}", size=14))
    return _svg(width, height, parts, caption)


def grid(size=9, box=3, mark=None, shade_box=False, caption=None):
    cell, pad = 30, 22
    width = pad + size * cell + 4
    height = pad + size * cell + 4
    parts = []
    if mark and shade_box:
        br, bc = (mark[0] // box) * box, (mark[1] // box) * box
        parts.append(f'<rect x="{pad + bc * cell}" y="{pad + br * cell}" width="{box * cell}" '
                     f'height="{box * cell}" class="hlfill"/>')
    if mark:
        r, c = mark
        parts.append(f'<rect x="{pad + c * cell + 3}" y="{pad + r * cell + 3}" width="{cell - 6}" '
                     f'height="{cell - 6}" rx="4" class="markfill"/>')
    for k in range(size + 1):
        cls = "line strong" if k % box == 0 else "line"
        offset = pad + k * cell
        parts.append(f'<line x1="{pad}" y1="{offset}" x2="{pad + size * cell}" y2="{offset}" class="{cls}"/>')
        parts.append(f'<line x1="{offset}" y1="{pad}" x2="{offset}" y2="{pad + size * cell}" class="{cls}"/>')
    for k in range(size):
        parts.append(_text(pad + k * cell + cell / 2, pad - 10, k, cls="idx", size=11))
        parts.append(_text(pad - 11, pad + k * cell + cell / 2, k, cls="idx", size=11))
    return _svg(width, height, parts, caption)


def rows(rows, highlight_col=None, caption=None):
    label_w, cell_w, cell_h, pad = 78, 52, 34, 10
    n = max(len(r["values"]) for r in rows)
    width = pad * 2 + label_w + n * cell_w
    height = pad + len(rows) * (cell_h + 6) + 4
    parts = []
    for ri, row in enumerate(rows):
        y = pad + ri * (cell_h + 6)
        parts.append(_text(pad + label_w - 10, y + cell_h / 2, row["label"], cls="lbl", size=13, anchor="end"))
        for ci, v in enumerate(row["values"]):
            x = pad + label_w + ci * cell_w
            cls = "cell hl" if ci == highlight_col else "cell"
            parts.append(f'<rect x="{x}" y="{y}" width="{cell_w}" height="{cell_h}" class="{cls}"/>')
            parts.append(_text(x + cell_w / 2, y + cell_h / 2, v, size=15))
    return _svg(width, height, parts, caption)


KINDS = {"array": array, "grid": grid, "rows": rows}


def render(spec):
    spec = dict(spec)
    kind = spec.pop("kind", None)
    if kind not in KINDS:
        raise ValueError(f"unknown viz kind {kind!r}; use one of {sorted(KINDS)}")
    return KINDS[kind](**spec)
