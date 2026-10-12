"""การประยุกต์ปริพันธ์

คณิตศาสตร์ · แคลคูลัส 2 · อุดมศึกษา
Indicators: —

Sets moved here from: math.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.math_problems import MathDraw, MathType

PROVENANCE = Provenance("original")


@question_type("math.volume_of_revolution",
               display_name={"th": "ปริมาตรทรงตันจากการหมุน"},
               level={"th": "แคลคูลัส 2"}, topic="การประยุกต์ปริพันธ์")
class VolumeOfRevolution(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random):
        if rng.random() < 0.5:
            return MathDraw(
                r"y = f(x),\ x \in [a, b]", r"\pi\int_{a}^{b} [f(x)]^{2}\,dx",
                prompt="หมุนรอบแกน x (วิธีจาน) ปริมาตรเท่ากับข้อใด",
                distractors=[r"\pi\int_{a}^{b} f(x)\,dx",
                             r"2\pi\int_{a}^{b} f(x)\,dx",
                             r"\int_{a}^{b} [f(x)]^{2}\,dx"])
        return MathDraw(
            r"y = f(x),\ x \in [a, b]", r"2\pi\int_{a}^{b} x\,f(x)\,dx",
            prompt="หมุนรอบแกน y (วิธีเปลือกทรงกระบอก) ปริมาตรเท่ากับข้อใด",
            distractors=[r"\pi\int_{a}^{b} x\,f(x)\,dx",
                         r"2\pi\int_{a}^{b} f(x)\,dx",
                         r"\pi\int_{a}^{b} [f(x)]^{2}\,dx"])


@question_type("math.arc_length",
               display_name={"th": "ความยาวส่วนโค้ง"}, level={"th": "แคลคูลัส 2"},
               topic="การประยุกต์ปริพันธ์")
class ArcLength(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random):
        return MathDraw(
            r"y = f(x),\ x \in [a, b]", r"\int_{a}^{b} \sqrt{1 + [f'(x)]^{2}}\,dx",
            prompt="สูตรความยาวส่วนโค้งคือข้อใด",
            # One-slip copies of the answer alone make it the choice they all
            # resemble; the disc-volume formula and a two-slip root are mixed in.
            distractors=[r"\int_{a}^{b} \sqrt{1 + [f(x)]^{2}}\,dx",
                         r"\int_{a}^{b} \sqrt{1 + f(x)}\,dx",
                         r"\pi\int_{a}^{b} [f(x)]^{2}\,dx",
                         r"\int_{a}^{b} \sqrt{1 + f'(x)}\,dx",
                         r"\int_{a}^{b} [f'(x)]^{2}\,dx"])


@question_type("math.surface_area_revolution",
               display_name={"th": "พื้นที่ผิวจากการหมุน"},
               level={"th": "แคลคูลัส 2"}, topic="การประยุกต์ปริพันธ์")
class SurfaceAreaRevolution(MathType):
    def expr(self, rng: Random):
        return MathDraw(
            r"y = f(x),\ x \in [a, b]",
            r"2\pi\int_{a}^{b} f(x)\sqrt{1 + [f'(x)]^{2}}\,dx",
            prompt="สูตรพื้นที่ผิวจากการหมุนรอบแกน x คือข้อใด",
            # The disc-volume formula it is most often confused with, a shell
            # without the arc length, and one as long as the answer but with f
            # and f' misplaced (not all one-slip copies of the answer).
            distractors=[r"\pi\int_{a}^{b} [f'(x)]^{2}\sqrt{1 + f(x)}\,dx",
                         r"\pi\int_{a}^{b} [f(x)]^{2}\,dx",
                         r"2\pi\int_{a}^{b} f(x)\,dx"])
