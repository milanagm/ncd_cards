"""Card files: YAML frontmatter, then '## Front' and '## Back' sections in Markdown.

Frontmatter keys: id (= file name), type (see config.CARD_TYPES), mistakes (ledger category ids),
evidence (submission references like 'three-integer-sum#12-13'), tags (optional).
"""
import re

import yaml

from . import config

SECTION_RE = re.compile(r"^## (Front|Back)[ \t]*$", re.M)


def parse(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{path.name}: must start with '---' frontmatter")
    _, frontmatter, body = text.split("---\n", 2)
    meta = yaml.safe_load(frontmatter) or {}
    parts = SECTION_RE.split(body)
    sections = {name.lower(): content.strip() for name, content in zip(parts[1::2], parts[2::2])}
    return {
        "id": meta.get("id"),
        "type": meta.get("type"),
        "mistakes": meta.get("mistakes") or [],
        "evidence": meta.get("evidence") or [],
        "tags": meta.get("tags") or [],
        "front": sections.get("front", ""),
        "back": sections.get("back", ""),
        "file": path.name,
    }


def load_all():
    return [parse(path) for path in sorted(config.CARDS.glob("*.md"))]
