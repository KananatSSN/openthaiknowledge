"""Check an installed (not editable) otk from outside the source tree.

Run by CI after ``pip install .``: every set draws, every sheet loads its
figures, and the committed pictures resolve — the data files a consumer needs
are inside the built package.

    python scripts/check_installed.py
"""

from __future__ import annotations

import sys
from pathlib import Path
from random import Random

import otk
from otk.api import REGISTRY, catalog, provenance, sheets, shipped_asset
from otk.core.render.assets import builtin_dir

SOURCE = Path(__file__).resolve().parents[1]


def main() -> None:
    where = Path(otk.__file__).resolve()
    if SOURCE in where.parents:
        sys.exit(f"otk was imported from the source tree ({where}); run from elsewhere")
    for key, question_type in REGISTRY.items():
        question_type.generate(Random(1))
        provenance(key)
    pictures = sorted(builtin_dir().glob("*.png"))
    assert pictures, "no committed pictures in the package"
    assert all(shipped_asset(p.stem) for p in pictures)
    assert sheets(), "no sheets in the package"
    print(f"{len(REGISTRY)} sets drew, {len(catalog())} catalog rows, "
          f"{len(pictures)} pictures, {len(sheets())} sheets from {where.parent}")


if __name__ == "__main__":
    main()
