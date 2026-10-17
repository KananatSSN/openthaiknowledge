"""f(cos(x + y)) = cos x f(cos y) + k f(sin x)f(sin y) with f(1) < 0 gives f(t) = −t/k."""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance("adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2549, วันแรก ข้อ 6",))


def frac_tex(v: Fraction) -> str:
    if v.denominator == 1:
        return str(v.numerator)
    sign = "-" if v < 0 else ""
    return rf"{sign}\frac{{{abs(v.numerator)}}}{{{v.denominator}}}"


def function_value(k: int, t: Fraction) -> Fraction:
    """x = y = 0 gives f(0) = 0; y = 0 gives f(cos x) = c·cos x with c = f(1);
    x = y = π/2 gives −c = kc², so c = −1/k and f(t) = −t/k on [−1, 1]
    (source: k = 2, f(2006/2549) = −1003/2549)."""
    return -t / k


@question_type(
    "math.cosine_addition_functional_olympiad",
    display_name={"th": "สมการเชิงฟังก์ชันจากสูตรผลบวกโคไซน์"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สมการเชิงฟังก์ชัน",
)
class CosineAdditionFunctional(WordProblem):
    def expr(self, rng: Random):
        k = rng.randint(2, 9)
        q = rng.randint(5, 3000)
        t = Fraction(rng.randint(1, q - 1), q) * rng.choice([1, -1])
        answer = function_value(k, t)
        wrong = [frac_tex(v) for v in dict.fromkeys([-answer, -t, -k * t if abs(k * t) < 50 else t, -t / (2 * k), t / k / 2]) if v != answer]
        kk = "" if k == 1 else str(k)
        return MathDraw(
            rf"f(\cos(x+y))=\cos x\,f(\cos y)+{kk}f(\sin x)f(\sin y),\quad f(1)<0",
            frac_tex(answer),
            prompt=f"f : ℝ → ℝ สอดคล้องสมการต่อไปนี้สำหรับทุก x, y ∈ ℝ จงหาค่าของ f({t})",
            hint="แทน x = y = 0 หา f(0) แทน y = 0 จะได้ f(cos x) = f(1)cos x แล้วแทน x = y = π/2 หา f(1)",
            distractors=wrong,
        )
