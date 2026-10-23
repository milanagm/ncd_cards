"""Markdown → HTML for card fields: fenced code with Pygments classes, ```viz blocks as inline SVG."""
import ast
import re
import textwrap

import markdown
import yaml

from . import viz

VIZ_RE = re.compile(r"^```viz[ \t]*\n(.*?)^```[ \t]*$", re.S | re.M)
CODE_RE = re.compile(r"^```(python(?:-nocheck)?)[ \t]*\n(.*?)^```[ \t]*$", re.S | re.M)
EXTENSIONS = ["fenced_code", "codehilite", "tables", "sane_lists"]
EXTENSION_CONFIG = {"codehilite": {"guess_lang": False, "css_class": "codehilite"}}


def to_html(text):
    def viz_block(m):
        return '\n\n<div class="viz">' + viz.render(yaml.safe_load(m.group(1))) + "</div>\n\n"

    text = VIZ_RE.sub(viz_block, text).replace("```python-nocheck", "```python")
    return markdown.markdown(text, extensions=EXTENSIONS, extension_configs=EXTENSION_CONFIG)


def inline_html(text):
    """Markdown for a single line (ledger notes): inline code and emphasis, no wrapping <p>."""
    html = markdown.markdown(text)
    return html.removeprefix("<p>").removesuffix("</p>")


def python_blocks(text):
    """Python code blocks that should parse; ```python-nocheck opts out."""
    return [code for lang, code in CODE_RE.findall(text) if lang == "python"]


def parses(code):
    """True if the snippet is valid Python on its own or as a loop body inside a function."""
    for candidate in (code, "def _snippet():\n    while True:\n" + textwrap.indent(code, " " * 8)):
        try:
            ast.parse(candidate)
            return True
        except SyntaxError:
            pass
    return False


def viz_specs(text):
    return [yaml.safe_load(block) for block in VIZ_RE.findall(text)]
