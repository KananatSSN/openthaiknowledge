"""Largest k with Π(k + a/b) ≤ c·(Σ a/b)(Σ b/a) for all positive a, b, c."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2557, ข้อ 5",)
)


def _root(value: int, index: int) -> tuple[int, int]:
    """value^(1/index) as outside·inside^(1/index) with inside power-free."""
    outside, inside = 1, value
    factor = 2
    while factor**index <= inside:
        while inside % factor**index == 0:
            inside //= factor**index
            outside *= factor
        factor += 1
    return outside, inside


def root_tex(value: int, index: int, minus: int = 0) -> str:
    outside, inside = _root(value, index)
    if inside == 1:
        return str(outside - minus)
    sign = "" if index == 2 else f"[{index}]"
    body = ("" if outside == 1 else str(outside)) + rf"\sqrt{sign}{{{inside}}}"
    return body + (f"-{minus}" if minus else "")


def largest_k(scale: int) -> float:
    """With S = Σ a/b and T = Σ b/a (both ≥ 3, Π a/b = 1), the left side is
    k³ + k²S + kT + 1, and c·ST − k²S − kT = c(S − k/c)(T − k²/c) − k³/c.
    Both factors are smallest at S = T = 3, so k works iff (k + 1)³ ≤ 9c."""
    return (9 * scale) ** (1 / 3) - 1


@question_type(
    "math.cyclic_ratio_product_bound_olympiad",
    display_name={"th": "ค่า k มากสุดในอสมการผลคูณของอัตราส่วนวนรอบ"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="อสมการ",
)
class CyclicRatioProductBound(WordProblem):
    def expr(self, rng: Random):
        scale = rng.randint(1, 30)
        nine = 9 * scale
        answer = root_tex(nine, 3, minus=1)
        candidates = [
            root_tex(nine, 3),  # forget the 1 in (k + 1)³
            root_tex(3 * scale, 3, minus=1),  # equality value 3 instead of 9
            root_tex(27 * scale, 3, minus=1),
            root_tex(nine, 2, minus=1),  # square root instead of cube root
            root_tex(nine + 1, 3, minus=1),
        ]
        wrong = [t for t in dict.fromkeys(candidates) if t != answer]
        factor = "" if scale == 1 else str(scale)
        return MathDraw(
            (
                r"\left(k+\frac{a}{b}\right)\left(k+\frac{b}{c}\right)\left(k+\frac{c}{a}\right)"
                rf"\le {factor}\left(\frac{{a}}{{b}}+\frac{{b}}{{c}}+\frac{{c}}{{a}}\right)"
                r"\left(\frac{b}{a}+\frac{c}{b}+\frac{a}{c}\right)"
            ),
            answer,
            prompt="จงหาจำนวนจริง k ที่มากที่สุดซึ่งทำให้อสมการต่อไปนี้เป็นจริงสำหรับทุกจำนวนจริงบวก a, b, c",
            hint="ให้ x = a/b, y = b/c, z = c/a จะได้ xyz = 1 และ xy + yz + zx = b/a + c/b + a/c แล้วกระจายด้านซ้าย",
            distractors=wrong,
        )
