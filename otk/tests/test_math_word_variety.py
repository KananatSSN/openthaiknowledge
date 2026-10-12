"""Word problems tell more than one story: each set below draws its numbers
the same way but frames them in several situations. The answer is re-derived
from whichever situation the learner is shown."""

from __future__ import annotations

import math
import re
from fractions import Fraction
from random import Random

import pytest

from otk.core import generate

SEEDS = range(200)

# Sets that used to repeat one sentence. Concept checks with no natural
# story (pick_irrational, determine_quadratic, binomial_coefficient,
# gcd_lcm_relation_p6) are left as they are.
VARIED = (
    "previous_number", "time_elapsed", "time_to_hour", "convert_weight_p3", "convert_volume_p3",
    "read_fraction", "decimal_place_value", "angle_complement_supplement", "angles_around_point_p4",
    "clock_angle_p4", "quadrilateral_angle", "parallelogram_area", "parallelogram_perimeter_p5",
    "trapezoid_area", "percent_of_number", "percent_two_step_p5", "parallel_angles",
    "triangle_missing_angle", "composite_box_volume_p6", "cube_surface_area", "prism_volume",
    "water_level_p6", "triangle_area", "triangle_missing_side_p6", "circle_area_circumference",
    "circle_radius_from_circumference", "gcd", "lcm", "equivalent_ratio_p6", "map_scale",
    "pattern_nth_term_p6", "angle_bisector", "angle_bisector_measure", "perpendicular_bisector",
    "mode_from_data", "solve_proportion", "scientific_notation", "translate_point",
    "pythagoras_diagonal", "cylinder_surface_area_m2", "cylinder_volume", "boxplot_iqr",
    "cointerior_angle", "similar_ratio_area", "similar_triangle", "cone_volume", "pyramid_volume_m3",
    "sphere_volume", "central_inscribed_angle", "cyclic_quadrilateral", "inscribed_angle_semicircle",
    "tangent_length_m3", "circular_permutation_m5", "probability_complement", "expected_value_dice",
    "regular_saving_m5", "present_value_m5", "loan_instalment_m5", "standard_deviation", "variance",
    "percentile_position", "quartile", "linear_regression", "regression_slope",
    "mean_frequency_table_m6", "z_score", "infinite_geometric_series",
)


def _b(block) -> str:
    return getattr(block, "text", None) or getattr(block, "tex", "") or ""


def _stem(q) -> str:
    return " ".join(_b(b) for b in q.stem)


def _answer(q) -> str:
    return " ".join(_b(b) for b in q.choices[q.answer].content)


def _nums(s: str) -> list[int]:
    return [int(n) for n in re.findall(r"\d+", s.replace(",", ""))]


def _each(key):
    for seed in SEEDS:
        yield generate(f"math.{key}", Random(seed))


def _skeleton(q) -> str:
    return re.sub(r"-?\d[\d,]*(\.\d+)?", "#", " | ".join(_b(b) for b in q.stem))


@pytest.mark.parametrize("key", VARIED)
def test_at_least_three_situations(key):
    assert len({_skeleton(q) for q in _each(key)}) >= 3


# key -> expected answer from (stem, numbers in the stem)
_RULES = {
    "time_to_hour": lambda s, n: 60 - n[1],
    "convert_weight_p3": lambda s, n: 1000 * n[0],
    "convert_volume_p3": lambda s, n: 1000 * n[0],
    "angle_complement_supplement":
        lambda s, n: (180 if "สองมุมฉาก" in s or "มุมตรง" in s else 90) - n[0],
    "quadrilateral_angle": lambda s, n: 360 - sum(n[:3]),
    "parallelogram_area": lambda s, n: n[0] * n[1],
    "trapezoid_area": lambda s, n: (n[0] + n[1]) * n[2] // 2,
    "percent_of_number": lambda s, n: n[0] * n[1] // 100,
    "parallel_angles": lambda s, n: n[0] if "มุมแย้ง" in s else 180 - n[0],
    "triangle_missing_angle": lambda s, n: 180 - n[0] - n[1],
    "cube_surface_area": lambda s, n: 6 * n[0] ** 2,
    "prism_volume": lambda s, n: n[0] * n[1],
    "triangle_area": lambda s, n: n[0] * n[1] // 2,
    "circle_area_circumference":
        lambda s, n: 22 * n[0] ** 2 // 7 if "พื้นที่" in s else 44 * n[0] // 7,
    "circle_radius_from_circumference": lambda s, n: n[0] * 7 // 44,
    "gcd": lambda s, n: math.gcd(n[0], n[1]),
    "lcm": lambda s, n: math.lcm(n[0], n[1]),
    "map_scale": lambda s, n: n[1] * n[2],
    "angle_bisector": lambda s, n: n[0] // 2,
    "angle_bisector_measure": lambda s, n: n[0] // 2,
    "perpendicular_bisector": lambda s, n: n[0] // 2,
    "solve_proportion": lambda s, n: n[1] * n[2] // n[0],
    "pythagoras_diagonal": lambda s, n: math.isqrt(n[0] ** 2 + n[1] ** 2),
    "cylinder_volume": lambda s, n: 22 * n[0] ** 2 * n[1] // 7,
    "cointerior_angle": lambda s, n: 180 - n[0],
    "similar_ratio_area": lambda s, n: n[1] * n[0] ** 2,
    "similar_triangle": lambda s, n: n[2] * n[1] // n[0],
    "cone_volume": lambda s, n: 22 * n[0] ** 2 * n[1] // 21,
    "central_inscribed_angle": lambda s, n: 2 * n[0],
    "cyclic_quadrilateral": lambda s, n: 180 - n[0],
    "inscribed_angle_semicircle": lambda s, n: 90 - n[0],
    "z_score": lambda s, n: ((n[0] - n[1]) // n[2] if s.startswith("ถ้า x") else (n[2] - n[0]) // n[1]),
    "expected_value_dice": lambda s, n: Fraction(max(n), 6),
}


@pytest.mark.parametrize("key", sorted(_RULES))
def test_answer_matches_the_situation(key):
    rule = _RULES[key]
    for q in _each(key):
        s = _stem(q)
        got = _answer(q)
        want = rule(s, _nums(s))
        if isinstance(want, Fraction):
            m = re.fullmatch(r"\\frac\{(\d+)\}\{(\d+)\}", got)
            got_v = Fraction(int(m.group(1)), int(m.group(2))) if m else Fraction(got)
            assert got_v == want, s
        else:
            assert int(got) == want, s


def test_times_and_decimals():
    for q in _each("time_elapsed"):
        (h1, m1), (h2, m2) = [tuple(map(int, t)) for t in re.findall(r"(\d\d):(\d\d)", _stem(q))]
        assert int(_answer(q)) == (h2 * 60 + m2) - (h1 * 60 + m1)
    for q in _each("decimal_place_value"):
        s = _stem(q)
        whole, digits = re.search(r"(\d)\.(\d\d)", s).groups()
        assert _answer(q) == (digits[0] if "ส่วนสิบ" in s else digits[1])
    for q in _each("read_fraction"):
        d, n = _nums(_stem(q))[:2]
        assert _answer(q) == rf"\frac{{{n}}}{{{d}}}"


def test_data_sets():
    for q in _each("mode_from_data"):
        data = [int(x) for x in re.search(r"(\d+(?:, \d+){4})", _stem(q)).group(1).split(", ")]
        assert int(_answer(q)) == max(set(data), key=data.count)
    for q in _each("quartile"):
        s = _stem(q)
        data = [int(x) for x in re.search(r"(\d+(?:, \d+){6})", s).group(1).split(", ")]
        which = int(re.search(r"Q_(\d)", s).group(1))
        assert int(_answer(q)) == data[2 * which - 1]


def test_translate_point():
    for q in _each("translate_point"):
        texts = [_b(b) for b in q.stem]
        x, y = map(int, re.findall(r"-?\d+", texts[1]))
        s = texts[0]
        if "แกน x" in s:
            dx, dy = map(int, re.findall(r"-?\d+", s))
        else:
            mx, my = map(int, re.findall(r"\d+", s))
            dx = mx if "ขวา" in s else -mx
            dy = my if "ขึ้น" in s else -my
        assert _answer(q) == f"({x + dx}, {y + dy})", s


def test_linear_regression():
    for q in _each("linear_regression"):
        s = _stem(q)
        m = re.search(r"ŷ = (?:(-?\d+) ([+-]) )?(-?)(\d*)x", s)
        a = m.group(1) or 0
        slope = int(m.group(4) or 1) * (-1 if (m.group(2) or m.group(3)) == "-" else 1)
        x = _nums(s)[-1]                 # every situation names x last
        assert int(_answer(q)) == int(a) + slope * x, s
