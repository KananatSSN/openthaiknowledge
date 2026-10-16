"""Incentres of right triangles on a unit square's sides lie on its circumcircle."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2555, ข้อ 4",)
)


def incenter_area_parts(angles: tuple[int, int, int, int]) -> tuple[int, int]:
    """∠AO₁B = 135° puts O₁ on the square's circumcircle (R² = 1/2), at arc
    α₁ from B and 90° − α₁ from A, where α₁ = ∠EAB. The arcs between
    consecutive incentres are 90° + αᵢ − αᵢ₊₁, so the area is
    ¼·Σ cos(αᵢ − αᵢ₊₁) ≤ 1. With angles 30° or 60°, returns (zeros, thirties):
    area = (2·zeros + √3·thirties)/8."""
    zeros = thirties = 0
    for a, b in zip(angles, angles[1:] + angles[:1]):
        if a == b:
            zeros += 1
        elif abs(a - b) == 30:
            thirties += 1
        else:
            raise ValueError("angles must be 30° or 60°")
    return zeros, thirties


def area_tex(zeros: int, thirties: int) -> str:
    """zeros/4 + thirties·√3/8 as one reduced fraction."""
    from fractions import Fraction
    from math import gcd

    rational, root = Fraction(zeros, 4), Fraction(thirties, 8)
    den = rational.denominator * root.denominator // gcd(rational.denominator, root.denominator)
    a, b = int(rational * den), int(root * den)
    g = gcd(gcd(a, b), den)
    a, b, den = a // g, b // g, den // g
    surd = "" if b == 0 else (r"\sqrt{3}" if b == 1 else rf"{b}\sqrt{{3}}")
    top = "+".join(part for part in (str(a) if a else "", surd) if part) or "0"
    return top if den == 1 else rf"\frac{{{top}}}{{{den}}}"


@question_type(
    "math.square_incenter_quadrilateral_olympiad",
    display_name={"th": "พื้นที่รูปสี่เหลี่ยมจากจุดศูนย์กลางวงกลมแนบในบนด้านสี่เหลี่ยมจัตุรัส"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="เรขาคณิต: สี่เหลี่ยมจัตุรัส",
)
class SquareIncenterQuadrilateral(WordProblem):
    def expr(self, rng: Random):
        angles = tuple(rng.choice((30, 60)) for _ in range(4))
        zeros, thirties = incenter_area_parts(angles)
        answer = area_tex(zeros, thirties)
        candidates = [area_tex(4, 0), area_tex(2, 2), area_tex(0, 4), area_tex(2, 0),
                      area_tex(zeros, 0), area_tex(0, 2)]
        wrong = [t for t in dict.fromkeys(candidates) if t != answer]
        a1, a2, a3, a4 = angles
        return MathDraw(
            rf"\angle EAB={a1}^\circ,\ \angle FBC={a2}^\circ,\ \angle GCD={a3}^\circ,\ \angle HDA={a4}^\circ",
            answer,
            prompt=(
                "ABCD เป็นรูปสี่เหลี่ยมจัตุรัสยาวด้านละ 1 หน่วย สร้างรูปสามเหลี่ยมมุมฉาก ABE, BCF, CDG, DAH "
                "ภายนอกรูปจัตุรัส โดยมุมฉากอยู่ที่ E, F, G, H ให้ O₁, O₂, O₃, O₄ เป็นจุดศูนย์กลางวงกลมแนบใน "
                "จงหาพื้นที่ของรูปสี่เหลี่ยม O₁O₂O₃O₄"
            ),
            hint="∠AO₁B = 90° + 90°/2 = 135° จึง O₁ อยู่บนวงกลมล้อมรอบรูปจัตุรัส หาตำแหน่งบนวงกลมด้วยมุมในส่วนโค้ง",
            distractors=wrong,
        )
