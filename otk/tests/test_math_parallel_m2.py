"""The ม.2 parallel-line sets added with the bend, triangle, algebra, converse and reason questions.

Answers are checked by an independent route: the two picture sets by measuring the angle in the figure's
own coordinates, the algebra set by solving the equation the stem states, and the converse by the rule.
"""

from __future__ import annotations

import math
import re
from fractions import Fraction
from random import Random

from otk.core import generate
from otk.sets._support.math_diagrams_geo import PARALLEL_BENDS, PARALLEL_TRIANGLES

SEEDS = range(400)


def _text(blocks) -> str:
    return "".join(getattr(b, "text", None) or getattr(b, "tex", None) or "" for b in blocks)


def _answer(q) -> str:
    return _text(q.choices[q.answer].content)


def _angle(at, p, q) -> float:
    """The angle at ``at`` between the rays to ``p`` and ``q``, in degrees."""
    a1 = math.atan2(p[1] - at[1], p[0] - at[0])
    a2 = math.atan2(q[1] - at[1], q[0] - at[0])
    d = abs(math.degrees(a1 - a2)) % 360
    return min(d, 360 - d)


def test_bend_equals_the_sum_of_the_angles_at_the_lines():
    for s in PARALLEL_BENDS:
        # The figure's points: P between the lines, A on y = 0.9 and B on y = −0.9.
        P = (1.1, 0.0)
        A = (P[0] - 0.9 / math.tan(math.radians(s.a)), 0.9)
        B = (P[0] - 0.9 / math.tan(math.radians(s.b)), -0.9)
        assert round(_angle(A, (A[0] + 1, 0.9), P)) == s.a
        assert round(_angle(B, (B[0] + 1, -0.9), P)) == s.b
        assert round(_angle(P, A, B)) == s.a + s.b
    for seed in SEEDS:
        q = generate("math.parallel_bend_m2", Random(seed))
        asset = next(b.asset_id for b in q.stem if b.kind == "image")
        a, b, ask = asset.split("_")[1:]
        assert int(_answer(q)) == (int(a) + int(b) if ask == "x" else int(a))


def test_triangle_between_the_lines():
    for t in PARALLEL_TRIANGLES:
        left, right = 1.8 / math.tan(math.radians(t.p)), 1.8 / math.tan(math.radians(t.q))
        A = ((left - right) / 2, 0.9)
        B, C = (A[0] - left, -0.9), (A[0] + right, -0.9)
        assert round(_angle(A, (A[0] - 1, 0.9), B)) == t.p
        assert round(_angle(A, (A[0] + 1, 0.9), C)) == t.q
        apex, at_c = round(_angle(A, B, C)), round(_angle(C, A, B))
        assert apex == 180 - t.p - t.q and at_c == t.q
    for seed in SEEDS:
        q = generate("math.parallel_triangle_m2", Random(seed))
        asset = next(b.asset_id for b in q.stem if b.kind == "image")
        p, qq, ask = asset.split("_")[1:]
        expected = 180 - int(p) - int(qq) if ask == "apex" else int(qq)
        assert int(_answer(q)) == expected


def _parse(expr: str) -> tuple[int, int]:
    """(3x + 10)° → (3, 10); x° → (1, 0); (x − 20)° → (1, −20)."""
    m = re.fullmatch(r"\(?(\d*)x(?: ([+−]) (\d+))?\)?°", expr)
    assert m, expr
    coef = int(m.group(1) or 1)
    const = int(m.group(3) or 0) * (-1 if m.group(2) == "−" else 1)
    return coef, const


def test_algebra_answers_solve_the_stated_equation():
    for seed in SEEDS:
        q = generate("math.parallel_algebra_m2", Random(seed))
        stem = _text(q.stem)
        m = re.search(r"ถ้า (∠\w+) = (\S+(?: [+−] \d+\)°)?) และ (∠\w+) = (\S+(?: [+−] \d+\)°)?) แล้ว", stem)
        assert m, stem
        (m1, c1), (m2, c2) = _parse(m.group(2)), _parse(m.group(4))
        supplementary = (m.group(1), m.group(3)) == ("∠BGH", "∠GHD")
        x = Fraction(180 - c1 - c2, m1 + m2) if supplementary else Fraction(c2 - c1, m1 - m2)
        assert x.denominator == 1 and x > 0, stem
        first, second = m1 * x + c1, m2 * x + c2
        assert 0 < first < 180 and 0 < second < 180, stem
        expected = x if stem.endswith("x มีค่าเท่าใด") else first
        assert Fraction(_answer(q)) == expected, stem


def test_converse_verdict_follows_the_rule():
    for seed in SEEDS:
        q = generate("math.parallel_test_m2", Random(seed))
        stem = _text(q.stem)
        u, v = (int(n) for n in re.findall(r"(\d+) องศา", stem)[:2])
        interior = "มุมภายในที่อยู่บนข้างเดียวกัน" in stem
        parallel = u + v == 180 if interior else u == v
        assert _answer(q).startswith("ℓ ขนานกับ m" if parallel else "ℓ ไม่ขนานกับ m"), stem


def test_reason_answer_is_not_also_a_distractor():
    for seed in SEEDS:
        q = generate("math.parallel_reason_m2", Random(seed))
        texts = [_text(c.content) for c in q.choices]
        assert len(set(texts)) == len(texts)
