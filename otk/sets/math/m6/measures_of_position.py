"""การวัดตำแหน่งข้อมูล

คณิตศาสตร์ · ม.6 · สสวท. พื้นฐาน
Indicators: ค 3.1 ม.6/1

Sets moved here from: math, math_data, math_diagrams_hi, math_m6.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem
from otk.sets._support.math_diagrams import _img
from otk.sets._support.math_diagrams_hi import BOX_ALT, BOX_PLOTS
from otk.sets._support.math_m4 import maths as _math_q
from otk.sets._support.math_m4 import maths as _maths
from otk.sets._support.math_m6 import M6
from otk.sets._support.math_p2 import _texts

PROVENANCE = Provenance("original")


@question_type("math.quartile",
               display_name={"th": "การหาควอไทล์"}, level={"th": "ม.6"},
               topic="การวัดตำแหน่งข้อมูล")
class Quartile(WordProblem):
    def expr(self, rng: Random):
        data = sorted(rng.sample(range(1, 50), 7))
        q1, q2, q3 = data[1], data[3], data[5]
        label, ans = rng.choice([("Q_1", q1), ("Q_2", q2), ("Q_3", q3)])
        listed = ", ".join(map(str, data))
        prompt = rng.choice((
            f"จากข้อมูล {listed} จงหา {label}",
            f"คะแนนสอบย่อยของนักเรียน 7 คนเรียงจากน้อยไปมากคือ {listed} จงหา {label}",
            f"ปริมาณน้ำฝน (มิลลิเมตร) ใน 7 วันเรียงจากน้อยไปมากคือ {listed} จงหา {label}",
        ))
        return MathDraw("", str(ans), prompt=prompt,
                        distractors=[str(x) for x in (q1, q2, q3) if x != ans]
                        + [str(data[0])])


@question_type("math.box_plot_picture_m6", display_name={"th": "อ่านแผนภาพกล่อง"},
               level={"th": "ม.6"}, topic="การวัดตำแหน่งข้อมูล")
class BoxPlotPictureM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        b = rng.choice(BOX_PLOTS)
        img = _img(b.asset_id, BOX_ALT)
        kind = rng.randrange(5)
        if kind == 0:
            return _math_q([text("มัธยฐานของข้อมูลเท่ากับเท่าใด"), img], str(b.med),
                           [str(b.q1), str(b.q3), str((b.lo + b.hi) // 2)], self.topic)
        if kind == 1:
            return _math_q([text("พิสัยระหว่างควอร์ไทล์ (Q3 - Q1) เท่ากับเท่าใด"), img], str(b.q3 - b.q1),
                           [str(b.hi - b.lo), str(b.q3 - b.med), str(b.med - b.q1)], self.topic)
        if kind == 2:
            return _math_q([text("พิสัยของข้อมูลเท่ากับเท่าใด"), img], str(b.hi - b.lo),
                           [str(b.q3 - b.q1), str(b.hi), str(b.hi - b.med)], self.topic)
        if kind == 3:
            return _math_q([text("ควอร์ไทล์ที่ 3 เท่ากับเท่าใด"), img], str(b.q3),
                           [str(b.q1), str(b.med), str(b.hi)], self.topic)
        return _math_q([text(f"ข้อมูลที่มีค่ามากกว่า {b.q3} คิดเป็นประมาณร้อยละเท่าใดของข้อมูลทั้งหมด"), img],
                       "25", ["50", "75", "100"], self.topic)


@question_type("math.percentile_position", display_name={"th": "ตำแหน่งเปอร์เซ็นไทล์"},
               level={"th": "ม.6"}, topic="การวัดตำแหน่งข้อมูล")
class PercentilePosition(MathType):
    """Position (n+1)·r/100 — chosen so it lands on a data point exactly."""

    def expr(self, rng: Random):
        n = rng.choice([9, 19, 24, 49, 99])
        r = rng.choice([10, 20, 25, 50, 75, 80, 90])
        pos = Fraction((n + 1) * r, 100)
        if pos.denominator != 1:
            n, r = 19, 50
            pos = Fraction((n + 1) * r, 100)
        prompt = rng.choice((
            "ข้อมูลมี n จำนวน เรียงจากน้อยไปมาก ตำแหน่งของเปอร์เซ็นไทล์นี้คือตำแหน่งที่เท่าใด",
            "นักเรียน n คนเรียงคะแนนสอบจากน้อยไปมาก เปอร์เซ็นไทล์นี้อยู่ที่ตำแหน่งที่เท่าใด",
            "บันทึกเวลาวิ่งของนักกีฬา n คนแล้วเรียงจากน้อยไปมาก เปอร์เซ็นไทล์นี้อยู่ที่ตำแหน่งที่เท่าใด",
        ))
        return MathDraw(
            rf"n = {n}, \quad P_{{{r}}}", str(pos.numerator), prompt=prompt,
            hint=r"\frac{(n+1)r}{100}",
            distractors=[str(n * r // 100), str(pos.numerator + 1),
                         str(pos.numerator - 1)])


@question_type("math.percentile_rank_m6", display_name={"th": "ตำแหน่งเปอร์เซ็นไทล์ของข้อมูล"},
               level=M6, topic="การวัดตำแหน่งข้อมูล")
class PercentileRankM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        n = rng.choice((20, 25, 40, 50, 80, 100, 200))
        below = rng.randint(1, n - 1)
        pct = Fraction(below * 100, n)
        if pct.denominator != 1:
            return self.build(rng)
        p = int(pct)
        if rng.random() < 0.5:
            who = rng.choice(_story.NAMES)
            stem = rng.choice((
                f"นักเรียน {n} คนสอบวิชาหนึ่ง มีนักเรียน {below} คนได้คะแนนน้อยกว่า{who} "
                f"คะแนนของเขาอยู่ที่เปอร์เซ็นไทล์ที่เท่าใดโดยประมาณ",
                f"วัดส่วนสูงของนักเรียน {n} คน มีนักเรียน {below} คนเตี้ยกว่า{who} "
                f"ส่วนสูงของ{who}อยู่ที่เปอร์เซ็นไทล์ที่เท่าใดโดยประมาณ",
                f"โรงพยาบาลชั่งน้ำหนักทารกแรกเกิด {n} คน มี {below} คนหนักน้อยกว่าทารกคนหนึ่ง "
                f"น้ำหนักของทารกคนนี้อยู่ที่เปอร์เซ็นไทล์ที่เท่าใดโดยประมาณ",
            ))
            return _maths([text(stem)],
                          str(p), [str(100 - p) if 100 - p != p else str(p + 5), str(below),
                                   str(p + 10) if p <= 90 else str(p - 10)], self.topic)
        return _texts([text(f"คะแนนสอบของนักเรียนคนหนึ่งอยู่ที่เปอร์เซ็นไทล์ที่ {p} หมายความว่าอย่างไร")],
                      f"ผู้สอบประมาณร้อยละ {p} ได้คะแนนไม่เกินคะแนนของเขา",
                      [f"เขาตอบข้อสอบถูกประมาณร้อยละ {p} ของข้อสอบทั้งหมด", f"เขาได้คะแนนประมาณร้อยละ {p} ของคะแนนเต็ม",
                       f"มีผู้สอบประมาณร้อยละ {p} ได้คะแนนสูงกว่าเขา"], self.topic)
