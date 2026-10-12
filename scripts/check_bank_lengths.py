"""Measure authored bank rows while rewriting them for the ``longest`` cue.

Rows are ``(lead, correct, wrongs)``. A row passes when at least one wrong is
not visibly shorter than the correct and at least one is not visibly longer
(the same 10%/3-character gap the audit's ``stands_out`` uses). Run it after
each edit; it is much faster than the full audit.

    python -X utf8 scripts/check_bank_lengths.py otk.sets.computing.p3.search_keyword SEARCH_TROUBLE
    python -X utf8 scripts/check_bank_lengths.py otk.sets.chemistry.m1.atoms_elements_compounds AtomMolecule.ITEMS
"""

from __future__ import annotations

import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from otk.core.distractors import _length_gap  # noqa: E402


def main() -> None:
    module = importlib.import_module(sys.argv[1])
    bad = 0
    for name in sys.argv[2:]:
        bank = module
        for part in name.split("."):
            bank = getattr(bank, part)
        for row in bank:
            correct, wrongs = row[1], row[2]
            size = len(correct.strip())
            gap = _length_gap(size)
            lengths = [len(w.strip()) for w in wrongs]
            if not (any(n > size - gap for n in lengths) and any(n < size + gap for n in lengths)):
                bad += 1
                print(f"{name}: correct {size} (gap {gap:.0f}) wrongs {lengths}  :: {correct[:50]}")
    print("rows needing work:", bad)


if __name__ == "__main__":
    main()
