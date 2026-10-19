"""Root sets closed under a + b + k·ab: shift to a set closed under products."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2556, ข้อ 4",)
)

# finite sets of distinct reals closed under multiplication (squares included)
PRODUCT_CLOSED = ((0,), (1,), (0, 1), (-1, 1), (-1, 0, 1))


def root_sets(k: int) -> list[tuple[Fraction, ...]]:
    """(1 + ka)(1 + kb) = 1 + k(a + b + kab), so u = 1 + ka turns the rule
    into closure under products; a finite such set lies in {−1, 0, 1}."""
    return [tuple(sorted(Fraction(u - 1, k) for u in s)) for s in PRODUCT_CLOSED]


def _num(v: Fraction) -> str:
    sign = "-" if v < 0 else ""
    v = abs(v)
    return sign + (str(v.numerator) if v.denominator == 1 else rf"\frac{{{v.numerator}}}{{{v.denominator}}}")


def factor_tex(roots) -> str:
    parts = []
    for root in roots:
        if root == 0:
            parts.append("x")
        else:
            sign = "+" if root < 0 else "-"
            parts.append(rf"\left(x{sign}{_num(abs(root))}\right)")
    return "".join(parts)


@question_type(
    "math.shifted_product_closed_roots_olympiad",
    display_name={"th": "พหุนามที่เซตรากปิดภายใต้ a + b + kab"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="รากของพหุนาม",
)
class ShiftedProductClosedRoots(WordProblem):
    def expr(self, rng: Random):
        k = rng.randint(1, 6)
        sets = root_sets(k)
        rule = "a + b + ab" if k == 1 else f"a + b + {k}ab"
        prompt = (
            "พหุนามโมนิก p(x) สัมประสิทธิ์จริงไม่เป็นค่าคงตัว มีรากเป็นจำนวนจริงไม่ซ้ำกันทั้งหมด "
            f"และถ้า a, b เป็นราก (a = b ได้) แล้ว {rule} เป็นรากด้วย "
        )
        if rng.randrange(2):
            cubic = sets[-1]
            answer = factor_tex(cubic)
            unit = Fraction(1, k)
            candidates = [
                factor_tex((-unit, 0, unit)),  # stop at {−1, 0, 1} itself
                factor_tex((0, unit, 2 * unit)),  # shift the wrong way
                factor_tex((-3 * unit, -2 * unit, -unit)),
                factor_tex((-2 * Fraction(k), -Fraction(k), 0)),  # multiply by k instead of dividing
            ]
            return MathDraw(
                "",
                answer,
                prompt=prompt + "พหุนามดีกรีสามที่มีสมบัติดังกล่าวคือข้อใด",
                hint="ให้ u = 1 + ka แล้วกฎกลายเป็นการคูณ เซตจำกัดที่ปิดภายใต้การคูณอยู่ใน {−1, 0, 1}",
                distractors=[t for t in dict.fromkeys(candidates) if t != answer],
                variant="cubic",
            )
        total = sum(sum(s) for s in sets)
        candidates = [-total, total - Fraction(1, k), total * k, sum(sets[-1]), total / 2, total + Fraction(1, k)]
        return MathDraw(
            "",
            _num(total),
            prompt=prompt + "จงหาผลบวกของรากทั้งหมดของพหุนามทุกตัวที่มีสมบัตินี้ (นับแยกตามพหุนาม)",
            hint="ให้ u = 1 + ka แล้วกฎกลายเป็นการคูณ เซตจำกัดที่ปิดภายใต้การคูณอยู่ใน {−1, 0, 1}",
            distractors=[_num(v) for v in dict.fromkeys(candidates) if v != total],
            variant="sum",
        )
