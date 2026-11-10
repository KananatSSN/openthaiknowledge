"""math.trig_equation_count_m5: λ = π is written as π x, never as the unknown command \\pix."""

from __future__ import annotations

import re
from random import Random

from otk.core import generate


def test_pi_times_x_is_valid_tex():
    seen_pi = False
    for seed in range(3000):
        q = generate("math.trig_equation_count_m5", Random(seed))
        for block in q.stem:
            if block.kind != "math":
                continue
            assert not re.search(r"\\pi[a-zA-Z]", block.tex), (seed, block.tex)
            seen_pi |= r"\tan(\pi x)" in block.tex
    assert seen_pi, "no draw used λ = π"
