"""The layout of ``otk/sets``: one file per curriculum unit, and guides that match.

A set's file is ``otk/sets/<subject>/<level>/<unit>.py``. A new unit file must
be imported in its level's ``__init__.py``; a file that registers nothing is
either not imported or empty.
"""

from __future__ import annotations

from pathlib import Path

from otk.tools import sets_index

SETS = sets_index.SETS


def _unit_files() -> list[Path]:
    return sorted(p.resolve() for p in SETS.glob("*/*/*.py") if p.name != "__init__.py")


def test_every_unit_file_is_imported_and_registers_sets():
    found = sets_index.units()
    silent = [str(p.relative_to(SETS)) for p in _unit_files() if p not in found]
    assert not silent, f"import these in their level's __init__.py: {silent}"


def test_folders_are_known_subjects_and_levels():
    for path in _unit_files():
        subject, level = path.parent.parent.name, path.parent.name
        assert subject in sets_index.SUBJECTS, path
        assert level in sets_index.LEVELS, path


def test_index_and_readmes_are_current():
    stale = [str(path.relative_to(SETS)) for path, text in sets_index.documents().items()
             if not path.exists() or path.read_text("utf-8") != text]
    assert not stale, f"run `python -m otk.tools.sets_index`; stale: {stale}"
