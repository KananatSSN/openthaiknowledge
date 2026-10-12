"""Which sets an older test file covers, named by the module they were built in.

The sets moved from ``otk/core/types/<module>.py`` into one file per curriculum
unit under ``otk/sets/`` (reorganisation, 2026-10). Tests written per build
module keep testing the same sets through this frozen list, which
``scripts/reorg/map_units.py`` produced from its map.
"""

from __future__ import annotations

import json
from pathlib import Path

ORIGINS: dict[str, list[str]] = json.loads(
    (Path(__file__).with_name("set_origins.json")).read_text("utf-8"))


def keys_from(module: str) -> list[str]:
    """The sets that used to live in ``otk/core/types/<module>.py``."""
    return list(ORIGINS[module])
