"""อัตราสัมพัทธ์

คณิตศาสตร์ · แคลคูลัส 1 · อุดมศึกษา
Indicators: —

Sets moved here from: math, math_calculus.
"""

from __future__ import annotations

import math as _math
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType, WordProblem

PROVENANCE = Provenance("original")


@question_type("math.related_rates",
               display_name={"th": "อัตราสัมพัทธ์ (ทรงกลม)"},
               level={"th": "แคลคูลัส 1"}, topic="อัตราสัมพัทธ์")
class RelatedRates(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random):
        return MathDraw(
            r"V = \frac{4}{3}\pi r^{3}", r"4\pi r^{2}\frac{dr}{dt}",
            prompt="ทรงกลมขยายตัว dV/dt เท่ากับข้อใด",
            distractors=[r"4\pi r^{2}", r"\frac{4}{3}\pi r^{2}\frac{dr}{dt}",
                         r"4\pi r\frac{dr}{dt}",
                         r"\frac{4}{3}\pi r^{2}", r"4\pi r"])


@question_type("math.related_rates_square",
               display_name={"th": "อัตราสัมพัทธ์: สี่เหลี่ยมจัตุรัสขยายตัว"},
               level={"th": "แคลคูลัส 1"}, topic="อัตราสัมพัทธ์")
class RelatedRatesSquare(WordProblem):
    """A = s² so dA/dt = 2s·ds/dt — exact for whole numbers."""

    def expr(self, rng: Random, side_lo: int = 3, side_hi: int = 20,
             rate_lo: int = 1, rate_hi: int = 6):
        s = rng.randint(side_lo, side_hi)
        rate = rng.randint(rate_lo, rate_hi)
        return MathDraw(
            "", str(2 * s * rate),
            prompt=(f"ด้านของรูปสี่เหลี่ยมจัตุรัสยาวเพิ่มขึ้นในอัตรา {rate} "
                    f"เซนติเมตรต่อวินาที ขณะที่ด้านยาว {s} เซนติเมตร "
                    "พื้นที่เพิ่มขึ้นในอัตรากี่ตารางเซนติเมตรต่อวินาที"),
            hint=r"\frac{dA}{dt} = 2s\frac{ds}{dt}",
            distractors=[str(s * rate), str(s * s), str(4 * rate)])


@question_type("math.related_rates_ladder",
               display_name={"th": "อัตราสัมพัทธ์: บันไดพิงกำแพง"},
               level={"th": "แคลคูลัส 1"}, topic="อัตราสัมพัทธ์")
class RelatedRatesLadder(WordProblem):
    """x·dx/dt + y·dy/dt = 0. The triple keeps x, y and the answer whole."""

    def expr(self, rng: Random, k_lo: int = 1, k_hi: int = 3, rate_hi: int = 6):
        a, b, c = rng.choice([(3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15)])
        k = rng.randint(k_lo, k_hi)
        x, y, length = a * k, b * k, c * k
        # Choose dx/dt so that dy/dt = −x·(dx/dt)/y is a whole number.
        step = y // _math.gcd(x, y)
        dx = step * rng.randint(1, max(1, rate_hi // step))
        dy = x * dx // y
        return MathDraw(
            "", str(dy),
            prompt=(f"บันไดยาว {length} เมตรพิงกำแพง ปลายล่างถูกดึงออกจากกำแพง "
                    f"ด้วยอัตรา {dx} เมตรต่อวินาที ขณะที่ปลายล่างห่างกำแพง "
                    f"{x} เมตร ปลายบนเลื่อนลงด้วยอัตรากี่เมตรต่อวินาที"),
            hint=r"x\frac{dx}{dt} + y\frac{dy}{dt} = 0",
            distractors=[str(dx), str(dy + 1), str(x * dx)])
