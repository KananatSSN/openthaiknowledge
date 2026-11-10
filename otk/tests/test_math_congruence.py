"""math.congruent_sides: the three given sides always make a real triangle."""

from __future__ import annotations

import re
from random import Random

from otk.core import generate


def _sides(seed: int) -> list[int]:
    q = generate("math.congruent_sides", Random(seed))
    stem = " ".join(b.text for b in q.stem if b.kind == "text")
    m = re.search(r"AB = (\d+), BC = (\d+) และ CA = (\d+)", stem)
    assert m, stem
    return sorted(int(v) for v in m.groups())


def test_given_sides_make_a_triangle():
    """Lengths such as 8, 22 and 6 cannot close up; every draw must satisfy the triangle inequality."""
    for seed in range(5000):
        a, b, c = _sides(seed)
        assert a + b > c, (seed, a, b, c)
        assert a >= 4 and c <= 25, (seed, a, b, c)
