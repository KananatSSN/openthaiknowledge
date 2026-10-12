"""Unit coefficients are written bare, and nothing else is touched."""

from otk.core.texfmt import tidy_unit_coefficients as tidy


def test_unit_coefficients_are_dropped():
    assert tidy("1x + 2y = 2") == "x + 2y = 2"
    assert tidy("y = -1x + 3") == "y = -x + 3"
    assert tidy("e^{1x}") == "e^{x}"
    assert tidy(r"\sin 1x") == r"\sin x"
    assert tidy(r"f(x) = 1 \cdot 2^{x}") == "f(x) = 2^{x}"
    assert tidy("a^{1n}") == "a^{n}"


def test_other_ones_are_kept():
    for tex in ("11x", "0.1x", r"\frac{1}{x}", "x + 1", "10^{1}", "21y", r"\log_{1}", "1"):
        assert tidy(tex) == tex
