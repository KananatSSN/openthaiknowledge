from __future__ import annotations

from functools import lru_cache


@lru_cache(maxsize=1)
def default_thai_font() -> str:
    """Return the legacy renderer's first installed Thai-capable font."""
    from matplotlib import font_manager

    installed = {font.name for font in font_manager.fontManager.ttflist}
    for candidate in (
        "Leelawadee UI",
        "Noto Sans Thai",
        "Garuda",
        "Loma",
        "Laksaman",
        "Waree",
        "Tahoma",
    ):
        if candidate in installed:
            return candidate
    return ""
