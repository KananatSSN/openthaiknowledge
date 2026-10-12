"""พื้นที่รูปสี่เหลี่ยม

คณิตศาสตร์ · ป.5 · สสวท. พื้นฐาน
Indicators: ค 2.1 ป.5/*

Sets moved here from: math, math_diagrams, math_geometry, math_p5.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.mistakes import named
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_diagrams import QUAD_FIGURES, _img, _math_q, _nums, figure_alt
from otk.sets._support.math_p5 import LEVEL

PROVENANCE = Provenance("original")


@question_type("math.parallelogram_area",
               display_name={"th": "พื้นที่สี่เหลี่ยมด้านขนาน"}, level={"th": "ป.5"},
               topic="พื้นที่รูปสี่เหลี่ยม")
class ParallelogramArea(WordProblem):
    def expr(self, rng: Random):
        base, h = rng.randint(3, 20), rng.randint(2, 15)
        prompt = rng.choice((
            f"สี่เหลี่ยมด้านขนานฐาน {base} สูง {h} หน่วย มีพื้นที่เท่าใด?",
            f"แปลงผักรูปสี่เหลี่ยมด้านขนานมีฐานยาว {base} เมตร สูง {h} เมตร "
            f"แปลงผักมีพื้นที่กี่ตารางเมตร",
            f"กระเบื้องแผ่นหนึ่งเป็นรูปสี่เหลี่ยมด้านขนาน ฐานยาว {base} เซนติเมตร สูง {h} เซนติเมตร "
            f"กระเบื้องมีพื้นที่กี่ตารางเซนติเมตร",
        ))
        return MathDraw("", str(base * h), prompt=prompt,
                        distractors=[str(base + h), str(2 * (base + h)),
                                     str(base * h // 2)])


@question_type("math.parallelogram_perimeter_p5",
               display_name={"th": "ความยาวรอบรูปสี่เหลี่ยมด้านขนานและขนมเปียกปูน"},
               level=LEVEL, topic="พื้นที่รูปสี่เหลี่ยม")
class ParallelogramPerimeterP5(WordProblem):
    def expr(self, rng: Random):
        if rng.random() < 0.5:
            a, b = rng.sample(range(4, 40), 2)
            ans = 2 * (a + b)
            prompt = rng.choice((
                f"รูปสี่เหลี่ยมด้านขนานมีด้านยาว {a} ซม. และ {b} ซม. ยาวรอบรูปกี่เซนติเมตร",
                f"สวนรูปสี่เหลี่ยมด้านขนานมีด้านยาว {a} เมตร และ {b} เมตร "
                f"ต้องใช้รั้วล้อมรอบสวนยาวกี่เมตร",
                f"กรอบรูปทรงสี่เหลี่ยมด้านขนานมีด้านยาว {a} ซม. และ {b} ซม. "
                f"ต้องใช้ริบบิ้นติดรอบกรอบยาวกี่เซนติเมตร",
            ))
            return MathDraw("", str(ans), prompt=prompt,
                            distractors=_story.keep(a + b, a * b, 2 * a + b, answer=ans))
        s = rng.randint(4, 30)
        prompt = rng.choice((
            f"รูปสี่เหลี่ยมขนมเปียกปูนยาวรอบรูป {4 * s} ซม. ด้านยาวด้านละกี่เซนติเมตร",
            f"ดัดลวดยาว {4 * s} ซม. เป็นรูปสี่เหลี่ยมขนมเปียกปูนได้พอดี แต่ละด้านยาวกี่เซนติเมตร",
        ))
        return MathDraw("", str(s), prompt=prompt,
                        distractors=_story.keep(2 * s, 4 * s, s + 4, answer=s, lo=1))


@question_type("math.quadrilateral_area_figure_p5",
               display_name={"th": "หาพื้นที่รูปสี่เหลี่ยมด้านขนานและคางหมูจากรูป"},
               level={"th": "ป.5"}, topic="พื้นที่รูปสี่เหลี่ยม")
class QuadrilateralAreaFigureP5(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        f = rng.choice(QUAD_FIGURES)
        if f.kind == "para":
            b, h, s = f.dims
            ans = b * h
            # The slanted side used as the height.
            wrongs = _nums(b * s, (b + s) * 2, b * h // 2 if b * h % 2 == 0 else b + h, answer=ans, lo=1)
            ask = "รูปสี่เหลี่ยมด้านขนานนี้มีพื้นที่กี่ตารางเซนติเมตร"
        else:
            a, b, h = f.dims
            ans = (a + b) * h // 2
            if (a + b) * h % 2:
                ans = None
            wrongs = _nums((a + b) * h, a * b, b * h, answer=ans or 0, lo=1)
            ask = "รูปสี่เหลี่ยมคางหมูนี้มีพื้นที่กี่ตารางเซนติเมตร"
            if ans is None:
                return self.build(rng)
        return _math_q([text(ask), _img(f.asset_id, figure_alt(f))], str(ans), wrongs, self.topic)


@question_type("math.trapezoid_area", display_name={"th": "พื้นที่รูปสี่เหลี่ยมคางหมู"},
               level={"th": "ป.5"}, topic="พื้นที่รูปสี่เหลี่ยม")
class TrapezoidArea(WordProblem):
    def expr(self, rng: Random, side_lo: int = 4, side_hi: int = 20):
        a, b = rng.randint(side_lo, side_hi), rng.randint(side_lo, side_hi)
        h = rng.randrange(2, 16, 2)               # even, so the half is whole
        area = (a + b) * h // 2
        prompt = rng.choice((
            f"รูปสี่เหลี่ยมคางหมูมีด้านคู่ขนานยาว {a} และ {b} เซนติเมตร "
            f"สูง {h} เซนติเมตร มีพื้นที่กี่ตารางเซนติเมตร",
            f"สนามหญ้ารูปสี่เหลี่ยมคางหมูมีด้านคู่ขนานยาว {a} และ {b} เมตร "
            f"ด้านคู่ขนานห่างกัน {h} เมตร สนามหญ้ามีพื้นที่กี่ตารางเมตร",
            f"ผนังด้านข้างของโรงรถเป็นรูปสี่เหลี่ยมคางหมู มีด้านคู่ขนานยาว {a} และ {b} ฟุต "
            f"สูง {h} ฟุต ต้องทาสีผนังนี้กี่ตารางฟุต",
        ))
        return MathDraw(
            "", str(area), prompt=prompt,
            hint=r"\frac{1}{2}(a + b)h",
            distractors=[str((a + b) * h), str(a * b), str(a * h)])


@question_type("math.rhombus_kite_area_p5",
               display_name={"th": "พื้นที่รูปสี่เหลี่ยมขนมเปียกปูนและรูปว่าว (เส้นทแยงมุม)"},
               level=LEVEL, topic="พื้นที่รูปสี่เหลี่ยม")
class RhombusKiteAreaP5(WordProblem):
    def expr(self, rng: Random):
        d1, d2 = 2 * rng.randint(2, 15), rng.randint(3, 30)
        shape = rng.choice(("สี่เหลี่ยมขนมเปียกปูน", "รูปว่าว"))
        ans = d1 * d2 // 2
        if rng.random() < 0.6:
            return MathDraw("", str(ans),
                            prompt=(f"รูป{shape.removeprefix('รูป')}มีเส้นทแยงมุมยาว {d1} ซม. และ {d2} ซม. "
                                    f"มีพื้นที่กี่ตารางเซนติเมตร"),
                            # Forgetting the half.
                            distractors=_story.keep(named("area.forgot_half", d1 * d2),
                                                    named("operation.reversed", d1 + d2),
                                                    2 * (d1 + d2), answer=ans))
        return MathDraw("", str(d2),
                        prompt=(f"รูป{shape.removeprefix('รูป')}มีพื้นที่ {ans} ตารางเซนติเมตร "
                                f"เส้นทแยงมุมเส้นหนึ่งยาว {d1} ซม. เส้นทแยงมุมอีกเส้นยาวกี่เซนติเมตร"),
                        distractors=_story.keep(ans // d1 if ans % d1 == 0 else d2 + 2, ans - d1,
                                                2 * ans, answer=d2, lo=1))
