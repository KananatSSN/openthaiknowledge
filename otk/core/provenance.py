"""Where a problem set came from.

Every set says whether it is **original** — written for otk, whatever books
taught its author the method — or **adapted** from specific source questions,
which then must be cited. Adapted sets are what the publication review (which
source material may be released openly) has to look at; the license itself is
project-wide.

A set declares it with ``PROVENANCE`` on its class or in its module::

    PROVENANCE = Provenance("original")
    PROVENANCE = Provenance("adapted", sources=("สอวน. 2568 รอบ 1, ข้อ 6",))

A digested paper's sets never declare it: ``sheet.json`` already names the
paper and item, so they are adapted from that. Every other set declares its
own, which ``otk/tests/test_provenance.py`` checks.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass
from functools import lru_cache
from typing import Literal

KINDS = ("original", "adapted")


@dataclass(frozen=True)
class Provenance:
    kind: Literal["original", "adapted"]
    # Citations a reader can follow: a source bank path, or title + item.
    sources: tuple[str, ...] = ()
    # Set when the provenance was derived rather than declared.
    derived: bool = False

    def __post_init__(self):
        if self.kind not in KINDS:
            raise ValueError(f"provenance kind must be one of {KINDS}, not {self.kind!r}")
        if self.kind == "adapted" and not self.sources:
            raise ValueError("an adapted set cites what it was adapted from")

    def as_dict(self) -> dict:
        return {"kind": self.kind, "sources": list(self.sources), "derived": self.derived}


def declared(key: str) -> Provenance | None:
    """The provenance the set's class or module states, if any."""
    from .registry import REGISTRY

    cls = type(REGISTRY[key])
    explicit = getattr(cls, "PROVENANCE", None)
    if explicit is None:
        explicit = getattr(sys.modules[cls.__module__], "PROVENANCE", None)
    return explicit


@lru_cache(maxsize=None)
def _sheet_items(sheet_id: str) -> tuple[str, dict[str, str]]:
    """The paper's citation and ``generator key -> item number`` for a digested sheet."""
    from ..sheets import SHEETS_DIR

    raw = json.loads((SHEETS_DIR / sheet_id / "sheet.json").read_text("utf-8"))
    paper = f"{raw.get('title', sheet_id)} ({raw.get('source_pdf', f'otk/sheets/{sheet_id}')})"
    return paper, {it["generator"]: str(it.get("number", "")) for it in raw.get("items", [])
                   if it.get("generator")}


def _sheet_citation(sheet_id: str, key: str) -> str:
    paper, numbers = _sheet_items(sheet_id)
    number = numbers.get(key)
    return f"{paper}, ข้อ {number}" if number else paper


def provenance(key: str) -> Provenance:
    """The set's provenance: declared, else derived from a digested paper.

    Raises ``LookupError`` for any other set that declares none.
    """
    from .registry import REGISTRY

    explicit = declared(key)
    if explicit is not None:
        return explicit
    question_type = REGISTRY[key]
    if question_type.sheet_id:
        return Provenance("adapted", (_sheet_citation(question_type.sheet_id, key),),
                          derived=True)
    raise LookupError(f"{key} declares no PROVENANCE")
