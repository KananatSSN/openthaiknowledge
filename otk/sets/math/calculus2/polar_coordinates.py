"""พิกัดเชิงขั้ว

คณิตศาสตร์ · แคลคูลัส 2 · อุดมศึกษา
Indicators: —

Sets moved here from: math, math_calculus.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType

PROVENANCE = Provenance("original")


@question_type("math.polar_to_cartesian",
               display_name={"th": "แปลงพิกัดเชิงขั้วเป็นพิกัดฉาก"},
               level={"th": "แคลคูลัส 2"}, topic="พิกัดเชิงขั้ว")
class PolarToCartesian(MathType):
    def expr(self, rng: Random):
        return MathDraw(
            r"(r, \theta)", r"(r\cos\theta,\ r\sin\theta)",
            prompt="พิกัดฉาก (x, y) คือข้อใด",
            distractors=[r"(r\sin\theta,\ r\cos\theta)",
                         r"(\cos\theta,\ \sin\theta)",
                         r"(r\cos\theta,\ -r\sin\theta)"])


@question_type("math.polar_area",
               display_name={"th": "พื้นที่ในพิกัดเชิงขั้ว"},
               level={"th": "แคลคูลัส 2"}, topic="พิกัดเชิงขั้ว")
class PolarArea(MathType):
    def expr(self, rng: Random):
        return MathDraw(
            r"r = f(\theta),\ \theta \in [\alpha, \beta]",
            r"\frac{1}{2}\int_{\alpha}^{\beta} [f(\theta)]^{2}\,d\theta",
            prompt="สูตรพื้นที่ที่ล้อมด้วย r = f(θ) คือข้อใด",
            distractors=[r"\int_{\alpha}^{\beta} [f(\theta)]^{2}\,d\theta",
                         r"\int_{\alpha}^{\beta} f(\theta)\,d\theta",
                         r"\pi\int_{\alpha}^{\beta} [f(\theta)]^{2}\,d\theta"])


@question_type("math.cartesian_to_polar", display_name={"th": "แปลงพิกัดฉากเป็นพิกัดเชิงขั้ว"},
               level={"th": "แคลคูลัส 2"}, topic="พิกัดเชิงขั้ว")
class CartesianToPolar(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random, radius_lo: int = 1, radius_hi: int = 8):
        r = rng.randint(radius_lo, radius_hi)
        deg = rng.choice([0, 90, 180, 270])
        point = {0: (r, 0), 90: (0, r), 180: (-r, 0), 270: (0, -r)}[deg]
        return MathDraw(
            f"({point[0]}, {point[1]})", rf"(r, \theta) = ({r}, {deg}^\circ)",
            prompt="จงเขียนจุดนี้ในพิกัดเชิงขั้ว",
            distractors=[rf"(r, \theta) = ({r}, {(deg + 90) % 360}^\circ)",
                         rf"(r, \theta) = ({r}, {(deg + 180) % 360}^\circ)",
                         rf"(r, \theta) = ({r * r}, {deg}^\circ)"])
