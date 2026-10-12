"""การแยกตัวประกอบของพหุนามดีกรีสอง

คณิตศาสตร์ · ม.2 · สสวท. พื้นฐาน
Indicators: ค 1.2 ม.2/2

Sets moved here from: math_gaps_secondary.
"""

from __future__ import annotations

import math
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem, binomial_tex
from otk.sets._support.math_gaps_secondary import _distinct, _lin, _num, _nz, _quad

PROVENANCE = Provenance("original")


def _plain(tex: str) -> str:
    """A small polynomial as sentence text: x^{2} + 5x + 6 → x² + 5x + 6."""
    return tex.replace("^{2}", "²").replace("^{3}", "³").replace("-", "−")


_M2_TOPIC = "การแยกตัวประกอบของพหุนามดีกรีสอง"


@question_type("math.factor_common_m2", display_name={"th": "แยกตัวประกอบโดยดึงตัวประกอบร่วม"},
               level={"th": "ม.2"}, topic=_M2_TOPIC)
class FactorCommonM2(WordProblem):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random):
        while True:
            k, a, b = rng.randint(2, 9), rng.randint(1, 6), _nz(rng, -9, 9)
            if math.gcd(a, abs(b)) == 1 and a != abs(b):
                break
        expanded = _quad(k * a, k * b, 0)
        right = f"{k}x({_lin(a, b)})"
        # Stopping after the number or after the x, and a sign slip.
        return MathDraw(expanded, right, prompt="จงแยกตัวประกอบให้สมบูรณ์",
                        distractors=_distinct(right, f"{k}({_quad(a, b, 0)})", f"x({_lin(k * a, k * b)})",
                                              f"{k}x({_lin(a, -b)})", f"{k}({_lin(a, b)})"))


@question_type("math.factor_trinomial_m2", display_name={"th": "แยกตัวประกอบพหุนามดีกรีสอง x² + bx + c"},
               level={"th": "ม.2"}, topic=_M2_TOPIC)
class FactorTrinomialM2(WordProblem):
    def expr(self, rng: Random):
        while True:
            p, q = _nz(rng, -9, 9), _nz(rng, -9, 9)
            if p != q and p + q:
                break
        expanded = _quad(1, p + q, p * q)
        right = f"{binomial_tex(p)}{binomial_tex(q)}"
        # Both signs flipped, one sign flipped (the product's sign right,
        # the sum's wrong), and a pair that multiplies to c but misses b.
        pair = next(((m, p * q // m) for m in range(1, 10)
                     if p * q % m == 0 and m + p * q // m != p + q and m != p * q // m), None)
        wrongs = [f"{binomial_tex(-p)}{binomial_tex(-q)}", f"{binomial_tex(p)}{binomial_tex(-q)}",
                  f"{binomial_tex(-p)}{binomial_tex(q)}"]
        if pair:
            wrongs.insert(1, f"{binomial_tex(pair[0])}{binomial_tex(pair[1])}")
        return MathDraw(expanded, right, prompt="จงแยกตัวประกอบ",
                        distractors=[w for w in dict.fromkeys(wrongs) if w != right])


@question_type("math.factor_apply_m2", display_name={"th": "นำการแยกตัวประกอบไปใช้แก้ปัญหา"},
               level={"th": "ม.2"}, topic=_M2_TOPIC)
class FactorApplyM2(WordProblem):
    def expr(self, rng: Random):
        kind = rng.randrange(3)
        if kind == 0:
            p, q = rng.sample(range(2, 10), 2)
            area = _plain(_quad(1, p + q, p * q))
            right = _lin(1, q)
            return MathDraw("", right, prompt=(
                f"รูปสี่เหลี่ยมผืนผ้ารูปหนึ่งมีพื้นที่ {area} ตารางหน่วย ถ้าด้านหนึ่งยาว x + {p} หน่วย "
                f"อีกด้านหนึ่งยาวกี่หน่วย"),
                distractors=_distinct(right, _lin(1, p * q), _lin(1, p + q), _lin(1, q - p)))
        if kind == 1:
            k = rng.randint(3, 9)
            area = _plain(_quad(1, 2 * k, k * k))
            right = _lin(1, k)
            return MathDraw("", right, prompt=(
                f"รูปสี่เหลี่ยมจัตุรัสรูปหนึ่งมีพื้นที่ {area} ตารางหน่วย ด้านยาวด้านละกี่หน่วย"),
                distractors=_distinct(right, _lin(1, 2 * k), _lin(1, k * k), _lin(2, k)))
        # a² − b² = (a − b)(a + b) makes a hard product easy.
        n, d = rng.choice((20, 30, 40, 50, 60, 70, 80, 90, 100)), rng.randint(1, 3)
        value = (n - d) * (n + d)
        return MathDraw(rf"{n - d} \times {n + d}", _num(value),
                        prompt="ใช้ผลต่างกำลังสองหาค่า",
                        distractors=[_num(int(v)) for v in
                                     _story.keep(n * n + d * d, n * n - d, (n - d) * n, answer=value)])
