"""Where drawn diagrams are written, and how, so a half-written PNG is never served.

Generated math diagrams are not committed: the generator draws one the first
time it is asked for (see ``otk.pictures.registry``) and keeps it here.
``GENERATOR_DIAGRAM_DIR`` overrides the default under the system temp dir.
"""

from __future__ import annotations

import os
import tempfile
from pathlib import Path


def output_dir() -> Path:
    path = Path(os.environ.get("GENERATOR_DIAGRAM_DIR")
                or Path(tempfile.gettempdir()) / "tutorrank-diagrams")
    path.mkdir(parents=True, exist_ok=True)
    return path


def save_image(img, asset_id: str) -> Path:
    """Write a PIL image atomically: to a temporary name, then renamed into place."""
    out = output_dir() / f"{asset_id}.png"
    tmp = out.with_name(f".{asset_id}.{os.getpid()}.tmp")
    img.save(tmp, format="PNG", optimize=True)
    os.replace(tmp, out)
    return out
