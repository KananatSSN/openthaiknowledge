"""Classify integer-valued functions obeying a product inequality."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2563, ข้อ 7",)
)


def possible_sample_sums(zeros: int, nonzeros: int) -> tuple[int, ...]:
    """Sums for f=0, f=1, and f=1 at zero only."""
    if zeros < 0 or nonzeros < 0 or zeros + nonzeros == 0:
        raise ValueError("the sample must contain at least one point")
    return tuple(sorted({0, zeros, zeros + nonzeros}))


def _set(values: tuple[int, ...]) -> str:
    return "{" + ", ".join(map(str, values)) + "}"


@question_type(
    "math.integer_valued_product_inequality_olympiad",
    display_name={"th": "จำแนกฟังก์ชันจำนวนเต็มจากอสมการผลคูณ"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สมการเชิงฟังก์ชัน",
)
class IntegerValuedProductInequality(WordProblem):
    def expr(self, rng: Random):
        zeros = rng.randint(2, 8)
        nonzeros = rng.randint(2, 8)
        answer = possible_sample_sums(zeros, nonzeros)
        return MathDraw(
            rf"z={zeros},\quad m={nonzeros}",
            _set(answer),
            prompt=(
                "ให้ f:ℝ→ℤ สอดคล้องกับ f(x)²+f(y)²≤2f(xy) สำหรับทุก x,y∈ℝ "
                "นำค่า f มาบวกที่จุด 0 จำนวน z ครั้งและที่จุดที่ไม่ใช่ 0 จำนวน m ครั้ง "
                "จงหาเซตของผลบวกที่เป็นไปได้ทั้งหมด"
            ),
            hint=(
                "แทน y=0 ก่อน จะได้ f(0)∈{0,1} แล้วแทน y=1 "
                "เพื่อจำกัดค่าของ f(x) และพิจารณาว่ามี x≠0 ที่ f(x)=1 ได้หรือไม่"
            ),
            distractors=[
                _set((0, zeros + nonzeros)),  # overlook the zero indicator
                _set((0, zeros, nonzeros, zeros + nonzeros)),  # invent nonzero indicator
                _set((zeros, zeros + nonzeros)),  # omit zero function
                _set((0, nonzeros, zeros + nonzeros)),  # swap zeros and nonzeros
                _set((0, 1, zeros + nonzeros)),  # count a repeated zero once
                _set((0, zeros, zeros + nonzeros + 1)),  # add a spurious sample
            ],
        )
