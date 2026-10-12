"""The sheet spec and the solver-module contract.

``sheet.json`` is the durable record of one digested exam sheet: where it came
from, and one entry per question holding the Thai source text, the constants the
sheet itself used, the answer, and the keys of whatever got built from it. It is
plain JSON so it survives independently of this code.

Two fields cover a question's picture, and they are not the same thing.
``figure`` is prose: how the diagram was read, for whoever writes the solver.
``figure_asset`` is an id — set only once someone has confirmed the crop shows
nothing that a redraw changes — and is what puts the picture back on screen in
the generated question. See :mod:`otk.sheets`.

A **solver module** (``qNN.py``) is the executable half. The contract is
deliberately tiny — four names — because every extra requirement is another
thing thirty hand-written files can drift on:

``PARAMS``   the sheet's own constants, as ``{name: value}``. Every key must be
             a keyword argument of ``solve``. These are what "change the
             constant" means: the tunables.
``ANSWER``   the answer for exactly those constants, as a plain Python value
             (int/Fraction/str/tuple). Recorded once, then defended by tests.
``solve()``  the method — closed form where one exists. Must accept every key of
             ``PARAMS`` as a keyword and work for other values of them.
``check()``  an *independently written* verification of the same quantity:
             brute force, a numeric/geometric simulation, a different identity.
             Optional only when no second method exists (then say why in the
             module docstring); :mod:`.verify` reports those separately.

``solve`` and ``check`` must agree. That is the whole safety argument: a
closed-form ``solve`` is what makes a generator fast enough to run per question,
and ``check`` is what makes it trustworthy at constants nobody looked at.
"""

from __future__ import annotations

import importlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from types import ModuleType

# Where digested sheets live: otk/sheets/<sheet_id>/
SHEETS_ROOT = Path(__file__).resolve().parents[2] / "sheets"


@dataclass
class ItemSpec:
    """One question of a sheet, as recorded in ``sheet.json``."""

    number: int                      # question number as printed on the sheet
    solver: str                      # module name inside the sheet package, e.g. "q07"
    title: str = ""                  # short Thai label for the UI
    source: str = ""                 # verbatim Thai text as printed
    page: int = 0                    # 1-based page it appears on
    figure: str = ""                 # how a diagram was digitized, if any
    figure_asset: str = ""           # asset id of the shipped crop, if attached
    topic: str = ""                  # Thai topic string (drives leaderboards)
    answer: str = ""                 # printed form of the answer for PARAMS
    generator: str = ""              # registry key of the generator built from it
    note: str = ""                   # caveats: non-unique answers, added conditions

    @property
    def label(self) -> str:
        return f"ข้อ {self.number}"


@dataclass
class SheetSpec:
    """A whole digested sheet."""

    sheet_id: str                    # package name under otk/sheets/
    title: str = ""
    source_pdf: str = ""
    subject: str = "คณิตศาสตร์"
    level: str = ""
    items: list[ItemSpec] = field(default_factory=list)
    note: str = ""

    @property
    def package(self) -> str:
        return f"otk.sheets.{self.sheet_id}"

    def item(self, number: int) -> ItemSpec:
        for it in self.items:
            if it.number == number:
                return it
        raise KeyError(f"{self.sheet_id}: no item {number}")

    def to_json(self) -> str:
        return json.dumps(
            {"sheet_id": self.sheet_id, "title": self.title,
             "source_pdf": self.source_pdf, "subject": self.subject,
             "level": self.level, "note": self.note,
             "items": [vars(it) for it in self.items]},
            ensure_ascii=False, indent=2) + "\n"


def load_sheet(sheet_id: str) -> SheetSpec:
    """Read ``otk/sheets/<sheet_id>/sheet.json``."""
    raw = json.loads((SHEETS_ROOT / sheet_id / "sheet.json").read_text("utf-8"))
    items = [ItemSpec(**it) for it in raw.pop("items", [])]
    return SheetSpec(items=items, **raw)


def solver_module(sheet: SheetSpec, item: ItemSpec) -> ModuleType:
    return importlib.import_module(f"{sheet.package}.{item.solver}")


def solver_modules(sheet: SheetSpec) -> list[tuple[ItemSpec, ModuleType]]:
    return [(it, solver_module(sheet, it)) for it in sheet.items]


def sheet_ids() -> list[str]:
    """Every digested sheet on disk."""
    if not SHEETS_ROOT.is_dir():
        return []
    return sorted(p.name for p in SHEETS_ROOT.iterdir()
                  if (p / "sheet.json").is_file())
