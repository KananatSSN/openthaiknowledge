"""Every IPST Foundation and Fluency set shows a strategy after answering.

The hint table is checked here; that every draw carries its hint is checked
per set in ``test_per_set.py``.
"""

from __future__ import annotations

from otk.core import catalog
from otk.sets._support.math_hints import MATH_HINTS

IPST = {"สสวท. พื้นฐาน", "สสวท. เพิ่มเติม"}
EARLY = sorted(
    row["key"] for row in catalog()
    if row["subject"] == "คณิตศาสตร์" and row["course_type"] in IPST
    and row["learning_stage"] in (1, 2)
)


def test_every_hint_names_an_early_ipst_set():
    early = set(EARLY)
    assert set(MATH_HINTS) <= early, sorted(set(MATH_HINTS) - early)


def test_hints_are_well_formed():
    for key, hint in MATH_HINTS.items():
        assert hint.count("$") % 2 == 0, key
        assert '"' not in hint and hint == hint.strip() and hint, key


def test_no_thai_inside_mathematics():
    """A MathBlock is notation only; Thai inside TeX has no glyphs in print."""
    import re
    for key, hint in MATH_HINTS.items():
        for tex in re.findall(r"\$([^$]+)\$", hint):
            assert not re.search("[\u0e00-\u0e7f]", tex), key
