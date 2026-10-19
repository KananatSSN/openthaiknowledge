"""f(m + f(n)) = f(m) + a·f(n) + b·f(n + 1) on ℕ: solvable only when b = 0."""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, WordProblem

PROVENANCE = Provenance(
    "adapted", sources=("สอวน. คณิตศาสตร์โอลิมปิกระดับชาติ 2554, ข้อ 10",)
)

CANDIDATES = {
    "linear": lambda a, c: (lambda n: a * n + c),
    "scaled": lambda a, c: (lambda n: (a + 1) * n),
    "power": lambda a, c: (lambda n: (a + 1) ** n),
    "shift": lambda a, c: (lambda n: n + a + c + 1),
    "double": lambda a, c: (lambda n: 2 * a * n + c),
}


def satisfies(f, a: int, b: int) -> bool:
    return all(f(m + f(n)) == f(m) + a * f(n) + b * f(n + 1) for m in range(1, 7) for n in range(1, 7))


def has_solution(a: int, b: int) -> bool:
    """Comparing f(m + f(n)f(k)) two ways makes (a f(n) + b f(n+1))/f(n) a
    constant λ, so f is geometric with ratio μ and f(m + T) = f(m) + λT is
    linear along progressions; that forces μ = 1, a constant f = c, and then
    c = c + (a + b)c is impossible once b ≥ 1. With b = 0, f(n) = an + c works
    (a constant when a = 0)."""
    return b == 0


@question_type(
    "math.shift_additive_functional_existence_olympiad",
    display_name={"th": "การมีอยู่ของฟังก์ชัน f(m + f(n)) = f(m) + af(n) + bf(n + 1)"},
    level={"th": "โอลิมปิก (สอวน.)"},
    topic="สมการเชิงฟังก์ชัน",
)
class ShiftAdditiveFunctionalExistence(WordProblem):
    def expr(self, rng: Random):
        top_a = rng.randint(2, 12)
        top_b = rng.randint(2, 12)
        answer = sum(1 for a in range(top_a + 1) for b in range(top_b + 1) if has_solution(a, b))
        wrong = [v for v in dict.fromkeys([
            (top_a + 1) * (top_b + 1),  # every pair
            top_a,  # forget a = 0 (a constant f works there)
            top_b + 1,  # count the b-column instead
            (top_a + 1) * top_b,  # the pairs with b ≥ 1
            top_a + top_b + 1,
        ]) if v != answer]
        return MathDraw(
            rf"f\big(m+f(n)\big)=f(m)+a\,f(n)+b\,f(n+1),\quad 0\le a\le {top_a},\ 0\le b\le {top_b}",
            str(answer),
            prompt="มีคู่จำนวนเต็ม (a, b) ในช่วงต่อไปนี้กี่คู่ที่มีฟังก์ชัน f : ℕ → ℕ สอดคล้องสมการทุก m, n ∈ ℕ",
            hint="เทียบ f(m + f(n)f(k)) สองแบบ แล้วพิจารณาการเติบโตของ f ตามลำดับเลขคณิตกับลำดับเรขาคณิต",
            distractors=[str(v) for v in wrong],
        )
