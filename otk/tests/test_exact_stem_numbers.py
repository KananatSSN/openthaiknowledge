"""A stem states its numbers exactly: ``exact`` never rounds, unlike ``show``."""

from fractions import Fraction
from random import Random
import re

import pytest

from otk.core import generate
from otk.kit.answer_choices import exact


@pytest.mark.parametrize(
    "value, text",
    [
        (Fraction(1, 3), "1/3"),
        (Fraction(-5, 12), "-5/12"),
        (Fraction(1, 8), "0.125"),
        (Fraction(9, 4), "2.25"),
        (Fraction(3, 100000), "3×10⁻⁵"),
        (200 / 3, "200/3"),
        (0.25, "0.25"),
        (1200, "1,200"),
    ],
)
def test_exact_text(value, text):
    assert exact(value) == text


# Sets whose stems once printed a rounded value: 1/3 as 0.33, 5/12 as 0.42,
# 40/3 N as 13.33 N, and an expansion coefficient of 3×10⁻⁵ as 0.
FIXED = ("phys.posn2560_q07", "phys.posn2562_q04", "phys.posn2562_q08", "phys.posn2562_q20")
REPEATING = re.compile(r"(?<![\d.])\d+\.(33|67|17|83|14|29|43|57|71|86|42|58)(?!\d)")


@pytest.mark.parametrize("key", FIXED)
def test_fixed_stems_print_no_rounded_number(key):
    for seed in range(80):
        stem = generate(key, Random(seed)).stem[0].text
        assert not REPEATING.search(stem), (key, stem)
        assert not re.search(r"(?<![\d.])0 K⁻¹", stem), (key, stem)
