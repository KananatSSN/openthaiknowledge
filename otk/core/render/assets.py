"""Resolve image-asset ids to the files that ship with otk.

Three sources, none needing configuration: the committed pictures in
``otk/pictures``, the diagrams ``otk.pictures.registry`` draws on demand
from the question types' specs, and the figures digested alongside an exam
sheet. The offline CLI and the generator service resolve ids the same way; the
service adds user uploads on top.
"""

from __future__ import annotations

import re
from pathlib import Path

from ... import sheets

ASSET_ID_RE = re.compile(r"^[A-Za-z0-9_.-]{1,64}$")


def builtin_dir() -> Path:
    """Directory holding the committed picture PNGs."""
    return Path(__file__).resolve().parents[2] / "pictures"


def shipped_files() -> dict[str, Path]:
    """Every committed image a question can show, by its path inside the package.

    Keys look like ``pictures/<id>.png`` and ``sheets/<sheet>/figures/qNN.png``.
    """
    package = builtin_dir().parent
    files = [*sorted(builtin_dir().glob("*.png")),
             *sorted(sheets.SHEETS_DIR.glob("*/figures/*.png"))]
    return {path.relative_to(package).as_posix(): path for path in files}


def shipped_asset(asset_id: str) -> Path | None:
    """Path to a built-in or sheet figure for ``asset_id``, or None."""
    if not ASSET_ID_RE.fullmatch(asset_id):
        return None
    candidate = builtin_dir() / f"{asset_id}.png"
    if candidate.exists():
        return candidate
    drawn = _draw_on_demand(asset_id)
    return drawn if drawn is not None else sheets.figure_path(asset_id)


def _draw_on_demand(asset_id: str) -> Path | None:
    """A generated diagram, drawn now if not drawn before."""
    from ...pictures.registry import diagram_path

    return diagram_path(asset_id)


def is_diagram(asset_id: str) -> bool:
    """Whether ``asset_id`` names a shipped or drawable diagram, without drawing it."""
    if (builtin_dir() / f"{asset_id}.png").exists():
        return True
    from ...pictures.registry import knows

    return knows(asset_id)
