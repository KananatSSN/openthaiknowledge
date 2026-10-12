"""Digested exam sheets — one package per sheet, one solver module per question.

Sheets also ship their **figures**: a question whose picture carries part of the
statement keeps that picture as ``<sheet_id>/figures/qNN.png``, cut out of the
source PDF by ``sheetpipe figures``. This module is the small bit of plumbing
that lets the rest of the app reach them — the id ↔ path mapping — so that
:mod:`otk.sets._support.olympiad` can put a figure in a stem and
:mod:`otk.core.render.assets` can resolve it, without either importing the other or
the extraction tool.

Only *draw-invariant* figures live here. A generated question redraws its
constants, so a picture is safe to reuse exactly when it shows what every draw
shares — the arrangement of a geometry diagram, the labels on a plan. A picture
that depicts the constants themselves would contradict the stem the moment they
change; ``sheetpipe figures`` refuses to attach those.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

SHEETS_DIR = Path(__file__).resolve().parent
FIGURES = "figures"

#: ``sheet-<sheet_id>-qNN``. Kept inside ``assetstore.ASSET_ID_RE``'s alphabet
#: so a sheet figure is just another asset id to everything downstream.
FIGURE_ID_RE = re.compile(r"^sheet-([A-Za-z0-9_]+)-q(\d{2})$")


def figure_asset_id(sheet_id: str, number: int) -> str:
    return f"sheet-{sheet_id}-q{number:02d}"


def figure_file(sheet_id: str, number: int) -> Path:
    return SHEETS_DIR / sheet_id / FIGURES / f"q{number:02d}.png"


def figure_path(asset_id: str) -> Path | None:
    """The PNG behind a sheet-figure asset id, or None if it isn't one.

    The id's alphabet excludes ``/``, ``\\`` and ``.``, so a parsed id cannot
    escape the sheets directory.
    """
    m = FIGURE_ID_RE.fullmatch(asset_id)
    if not m:
        return None
    path = figure_file(m.group(1), int(m.group(2)))
    return path if path.is_file() else None


def figure_attachments(sheet_id: str) -> dict[str, tuple[str, str]]:
    """``generator key → (asset id, alt text)`` for this sheet's shipped figures.

    Read straight from ``sheet.json`` so that attaching a figure is a one-step
    change: no generator has to name its own picture, and none can go stale.
    """
    raw = json.loads((SHEETS_DIR / sheet_id / "sheet.json").read_text("utf-8"))
    return {it["generator"]: (it["figure_asset"],
                              it.get("figure") or it.get("title", ""))
            for it in raw.get("items", [])
            if it.get("figure_asset") and it.get("generator")}
