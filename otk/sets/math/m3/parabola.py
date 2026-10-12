"""กราฟของฟังก์ชันกำลังสอง

คณิตศาสตร์ · ม.3 · สสวท. พื้นฐาน
Indicators: ค 1.2 ม.3/2

Sets moved here from: math, math_algebra, math_diagrams.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import MathDraw, MathType, coef_term, poly_tex
from otk.sets._support.math_algebra import _nonzero
from otk.sets._support.math_diagrams import PARABOLAS, _img, _math_q

PROVENANCE = Provenance("original")


PARABOLA_ALT = "กราฟพาราโบลาบนระนาบพิกัดฉากที่มีเส้นตาราง แกน X และแกน Y กำกับทุก 1 หน่วย"


@question_type("math.parabola_graph_m3", display_name={"th": "อ่านจุดยอด แกนสมมาตร และค่าสูงสุด/ต่ำสุดจากกราฟพาราโบลา"},
               level={"th": "ม.3"}, topic="กราฟของฟังก์ชันกำลังสอง")
class ParabolaGraphM3(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        p = rng.choice(PARABOLAS)
        img = _img(p.asset_id, PARABOLA_ALT)
        kind = rng.randrange(3)
        if kind == 0:
            return _math_q([text("จุดยอดของพาราโบลาในกราฟคือจุดใด"), img], f"({p.h}, {p.k})",
                           [f"({p.k}, {p.h})", f"({-p.h}, {p.k})", f"({p.h}, {-p.k})" if p.k else f"({p.h}, 1)",
                            f"({p.h + 1}, {p.k})", f"({p.h}, {p.k + 1})"], self.topic)
        if kind == 1:
            return _math_q([text("แกนสมมาตรของพาราโบลาในกราฟคือเส้นตรงใด"), img], f"x = {p.h}",
                           [f"y = {p.k}", f"x = {-p.h}" if p.h else "x = 1", f"x = {p.k}" if p.k != p.h
                            else f"x = {p.h + 2}", f"y = {p.h}", f"x = {p.h + 1}"], self.topic)
        word = "ค่าต่ำสุด" if p.a > 0 else "ค่าสูงสุด"
        return _math_q([text(f"ฟังก์ชันในกราฟมี{word}เท่าใด"), img], str(p.k),
                       [str(p.h), str(-p.k) if p.k else "1", str(p.k + 1), str(p.k - 1)], self.topic)


@question_type("math.parabola_vertex",
               display_name={"th": "จุดยอดของพาราโบลา"}, level={"th": "ม.3"},
               topic="กราฟของฟังก์ชันกำลังสอง")
class ParabolaVertex(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random):
        a = rng.choice([1, -1, 2])
        h, k = rng.randint(-5, 5), rng.randint(-5, 5)
        lead = "" if a == 1 else ("-" if a == -1 else str(a))
        tex = rf"y = {lead}(x {'-' if h >= 0 else '+'} {abs(h)})^{{2}}" \
              rf"{coef_term(k, '')}"
        return MathDraw(tex, rf"({h}, {k})", prompt="พาราโบลานี้มีจุดยอดที่ใด",
                        distractors=[rf"({-h}, {k})", rf"({h}, {-k})",
                                     rf"({k}, {h})"])


@question_type("math.parabola_axis_intercept",
               display_name={"th": "แกนสมมาตรและจุดตัดแกน y ของพาราโบลา"},
               level={"th": "ม.3"}, topic="กราฟของฟังก์ชันกำลังสอง")
class ParabolaAxisIntercept(MathType):
    break_convergence = True  # one-part slips cluster round the answer
    def expr(self, rng: Random, lead_hi: int = 3, h_hi: int = 8):
        a = _nonzero(rng, -lead_hi, lead_hi)
        h = _nonzero(rng, -h_hi, h_hi)
        k = rng.randint(-12, 12)
        # a(x − h)² + k expanded
        b, c = -2 * a * h, a * h * h + k
        shown = poly_tex((a, "x^2"), (b, "x"), (c, ""))
        if rng.random() < 0.5:
            return MathDraw(f"y = {shown}", f"x = {h}",
                            prompt="จงหาสมการแกนสมมาตรของพาราโบลา",
                            distractors=[f"x = {-h}", f"y = {h}", f"x = {c}"])
        return MathDraw(f"y = {shown}", f"(0, {c})",
                        prompt="พาราโบลานี้ตัดแกน y ที่จุดใด",
                        distractors=[f"(0, {k})", f"({c}, 0)", f"(0, {-c})"])
