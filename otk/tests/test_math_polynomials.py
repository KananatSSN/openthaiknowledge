"""The ม.2 เอกนามและพหุนาม ladder: order, and answers checked independently.

For the operation sets the problem and the answer TeX are both evaluated at
several points and must agree, and no distractor may agree with the problem.
The recognition sets are re-read from their TeX: what kind of expression each
choice is, and a monomial's coefficient and degree.
"""

from __future__ import annotations

import re
from collections import Counter
from fractions import Fraction
from random import Random

import pytest

from otk.core import REGISTRY, catalog, generate

LADDER = [
    "math.classify_monomial_polynomial",
    "math.monomial_coefficient_degree",
    "math.monomial_like_addsub",
    "math.negate_polynomial",
    "math.combine_like_terms",
    "math.polynomial_addsub",
    "math.polynomial_addsub_quadratic",
    "math.monomial_product",
    "math.monomial_times_polynomial",
    "math.negative_monomial_times_polynomial",
    "math.monomial_quotient",
    "math.simplify_polynomial",  # the older คูณ-หารเอกนาม set
    "math.polynomial_div_monomial",
    "math.distribute_and_simplify",
]
OPERATIONS = LADDER[2:]
NEW = [k for k in OPERATIONS
       if k not in {"math.polynomial_addsub", "math.monomial_times_polynomial"}]
POINTS = [(Fraction(2), Fraction(3)), (Fraction(-3), Fraction(5)),
          (Fraction(7, 2), Fraction(-2))]


def _py(tex: str) -> str:
    """The small TeX subset these generators emit, as a Python expression."""
    s = re.sub(r"\^\{(-?\d+)\}", r"**(\1)", tex)
    s = re.sub(r"\\frac\{([^{}]*)\}\{([^{}]*)\}", r"((\1)/(\2))", s)
    s = s.replace(r"\div", "/")
    # Juxtaposition is multiplication: 3x, x(y), )(, 2(.
    s = re.sub(r"(?<=[\dxyz)])\s*(?=[xyz(])", "*", s)
    return s


def _value(tex: str, x: Fraction, y: Fraction, z: Fraction = Fraction(1)) -> Fraction:
    return eval(_py(tex), {"__builtins__": {}}, {"x": x, "y": y, "z": z})


def _tex(content) -> str:
    return "".join(b.tex for b in content)


def test_ladder_is_one_topic_in_teaching_order():
    rows = [r["key"] for r in catalog() if r["topic"] == "เอกนามและพหุนาม"
            and r["level"] == "ม.2"]
    # The ladder, then the word-problem application set (math_apply_basic),
    # which is not an expression to simplify and so stays out of OPERATIONS.
    assert rows == LADDER + ["math.polynomial_area_m2"]
    stages = [REGISTRY[k].learning_stage for k in LADDER]
    assert stages == sorted(stages) and set(stages) == {1, 2, 3}


def test_tex_reader_itself():
    assert _value(r"-(-3x + 5)", Fraction(2), Fraction(0)) == 1
    assert _value(r"\frac{-8x^{3}y}{2x^{2}}", Fraction(2), Fraction(1)) == -8
    assert _value(r"(12x^{3}) \div (-4x)", Fraction(1), Fraction(0)) == -3


@pytest.mark.parametrize("key", OPERATIONS)
def test_answer_equals_problem_and_distractors_do_not(key):
    for seed in range(150):
        q = generate(key, Random(seed))
        problem = q.stem[-1].tex
        answer = _tex(q.choices[q.answer].content)
        for x, y in POINTS:
            assert _value(problem, x, y) == _value(answer, x, y), (seed, problem, answer)
        for i, choice in enumerate(q.choices):
            if i == q.answer:
                continue
            wrong = _tex(choice.content)
            assert any(_value(problem, x, y) != _value(wrong, x, y)
                       for x, y in POINTS), (seed, problem, wrong)


@pytest.mark.parametrize("key", NEW)
def test_new_sets_give_four_distinct_choices(key):
    for seed in range(150):
        q = generate(key, Random(seed))
        texts = [_tex(c.content) for c in q.choices]
        assert len(texts) == REGISTRY[key].max_choices == len(set(texts)), (seed, texts)


def test_negate_covers_every_sign_pattern():
    """-(±ax ± b): all four sign combinations of the two-term case occur."""
    seen = set()
    for seed in range(300):
        tex = generate("math.negate_polynomial", Random(seed)).stem[-1].tex
        m = re.fullmatch(r"-\((-?)\d*x ([+-]) \d+\)", tex)
        if m:
            seen.add(m.groups())
    assert seen == {("", "+"), ("", "-"), ("-", "+"), ("-", "-")}


# ── recognition: เอกนาม / พหุนาม, สัมประสิทธิ์ / ดีกรี ──────────────────────

def _kind(tex: str) -> str:
    """'nonpoly', 'mono' or 'multi', read straight off the TeX."""
    if (r"\sqrt{x}" in tex or "^{-" in tex or r"^{\frac" in tex
            or re.search(r"\\frac\{[^}]*\}\{[^}]*x", tex)):
        return "nonpoly"
    return "multi" if re.search(r" [+-] ", tex) else "mono"


IS = {
    "ข้อใดเป็นเอกนาม": lambda k: k == "mono",
    "ข้อใดไม่เป็นเอกนาม": lambda k: k != "mono",
    "ข้อใดเป็นพหุนามแต่ไม่เป็นเอกนาม": lambda k: k == "multi",
    "ข้อใดไม่เป็นพหุนาม": lambda k: k == "nonpoly",
}


def test_classify_has_exactly_one_right_choice():
    asked = set()
    for seed in range(300):
        q = generate("math.classify_monomial_polynomial", Random(seed))
        ask = q.stem[0].text
        asked.add(ask)
        texts = [_tex(c.content) for c in q.choices]
        assert len(texts) == REGISTRY["math.classify_monomial_polynomial"].max_choices == len(set(texts)), (seed, texts)
        fits = [i for i, t in enumerate(texts) if IS[ask](_kind(t))]
        assert fits == [q.answer], (seed, ask, texts)
    assert asked == set(IS)


def _coef_degree(mono: str) -> tuple[Fraction, int]:
    one = Fraction(1)
    return (_value(mono, one, one, one),
            sum(int(e or 1) for _, e in re.findall(r"([xyz])(?:\^\{(\d+)\})?", mono)))


def test_coefficient_and_degree_answers():
    asked = Counter()
    for seed in range(300):
        q = generate("math.monomial_coefficient_degree", Random(seed))
        prompt, mono = q.stem[0].text, q.stem[1].tex
        coef, deg = _coef_degree(mono)
        texts = [_tex(c.content) for c in q.choices]
        assert len(texts) == REGISTRY["math.monomial_coefficient_degree"].max_choices == len(set(texts)), (seed, texts)
        answer = texts[q.answer]
        if prompt.startswith("จงหาสัมประสิทธิ์และดีกรี"):
            asked["both"] += 1
            assert all(t.startswith("(") for t in texts), (seed, texts)
            k, d = answer.strip("()").split(r",\ ")
            assert (_value(k, 0, 0), int(d)) == (coef, deg), (seed, mono, answer)
        elif prompt.startswith("จงหาสัมประสิทธิ์"):
            asked["coef"] += 1
            assert _value(answer, 0, 0) == coef, (seed, mono, answer)
            assert all(_value(t, 0, 0) != coef for t in texts if t != answer)
        else:
            asked["deg"] += 1
            assert int(answer) == deg, (seed, mono, answer)
            assert not any(t.startswith("(") for t in texts), (seed, texts)
    assert min(asked.values()) > 50 and len(asked) == 3
