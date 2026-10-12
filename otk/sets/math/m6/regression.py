"""การวิเคราะห์การถดถอย

คณิตศาสตร์ · ม.6 · สสวท. พื้นฐาน
Indicators: ค 3.1 ม.6/1

Sets moved here from: math, math_data, math_diagrams_hi, math_m6.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.math_problems import ChoiceType, MathDraw, MathType, WordProblem
from otk.sets._support.math_diagrams import _img, _text_q
from otk.sets._support.math_diagrams_hi import SCATTERS
from otk.sets._support.math_m4 import maths as _math_q
from otk.sets._support.math_m4 import maths as _maths
from otk.sets._support.math_m6 import M6, _dec
from otk.sets._support.math_p2 import _texts

PROVENANCE = Provenance("original")


SCATTER_ALT = "แผนภาพการกระจายของข้อมูลสองตัวแปร x และ y"


_TREND_TEXT = {"strong_pos": "ความสัมพันธ์เชิงเส้นทางบวกที่ค่อนข้างสูง",
               "weak_pos": "ความสัมพันธ์เชิงเส้นทางบวกที่ค่อนข้างต่ำ",
               "strong_neg": "ความสัมพันธ์เชิงเส้นทางลบที่ค่อนข้างสูง",
               "weak_neg": "ความสัมพันธ์เชิงเส้นทางลบที่ค่อนข้างต่ำ",
               "none": "ไม่มีความสัมพันธ์เชิงเส้น"}


_TREND_R = {"strong_pos": "0.95", "weak_pos": "0.4", "strong_neg": "-0.95", "weak_neg": "-0.4", "none": "0"}


@question_type("math.regression_correlation",
               display_name={"th": "ทิศทางของสหสัมพันธ์"},
               level={"th": "ม.6"}, topic="การวิเคราะห์การถดถอย")
class RegressionCorrelation(ChoiceType):
    def compose(self, rng: Random):
        positive = rng.random() < 0.5
        pairs = [("ชั่วโมงที่อ่านหนังสือ", "คะแนนสอบ"),
                 ("จำนวนปุ๋ยที่ใส่", "ผลผลิตต่อไร่"),
                 ("ขนาดของบ้าน", "ราคาบ้าน")] if positive else [
                 ("จำนวนชั่วโมงที่เล่นเกม", "คะแนนสอบ"),
                 ("อายุของรถยนต์", "ราคาขายต่อ"),
                 ("ระยะทางจากใจกลางเมือง", "ราคาที่ดิน")]
        a, b = rng.choice(pairs)
        stem = f"ความสัมพันธ์ระหว่าง “{a}” กับ “{b}” น่าจะเป็นแบบใด"
        answer = "สหสัมพันธ์เชิงบวก" if positive else "สหสัมพันธ์เชิงลบ"
        other = "สหสัมพันธ์เชิงลบ" if positive else "สหสัมพันธ์เชิงบวก"
        return stem, answer, [other, "ไม่มีสหสัมพันธ์",
                              "สหสัมพันธ์เท่ากับ 1 พอดี"]


@question_type("math.scatter_plot_picture_m6",
               display_name={"th": "ลักษณะความสัมพันธ์จากแผนภาพการกระจาย"},
               level={"th": "ม.6"}, topic="การวิเคราะห์การถดถอย")
class ScatterPlotPictureM6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        s = rng.choice(SCATTERS)
        img = _img(s.asset_id, SCATTER_ALT)
        if rng.random() < 0.5:
            others = [t for k, t in _TREND_TEXT.items() if k != s.trend]
            rng.shuffle(others)
            return _text_q([text("ข้อมูลในแผนภาพการกระจายนี้มีความสัมพันธ์แบบใด"), img],
                           _TREND_TEXT[s.trend], others, self.topic)
        others = [r for k, r in _TREND_R.items() if k != s.trend]
        rng.shuffle(others)
        return _math_q([text("ค่าสัมประสิทธิ์สหสัมพันธ์ r ของข้อมูลนี้ใกล้เคียงกับค่าใดมากที่สุด"), img],
                       _TREND_R[s.trend], others, self.topic)


@question_type("math.linear_regression",
               display_name={"th": "การทำนายด้วยสมการถดถอย"}, level={"th": "ม.6"},
               topic="การวิเคราะห์การถดถอย")
class LinearRegression(WordProblem):
    def expr(self, rng: Random):
        a = rng.randint(-10, 10)
        b = rng.choice([n for n in range(-5, 6) if n])
        x = rng.randint(1, 10)
        bx = "x" if abs(b) == 1 else f"{abs(b)}x"
        line = (f"ŷ = {a} {'+' if b > 0 else '-'} {bx}" if a else f"ŷ = {'' if b > 0 else '-'}{bx}")
        prompt = rng.choice((
            f"สมการถดถอย {line} ทำนายค่า y เมื่อ x = {x} เท่ากับเท่าใด?",
            f"ร้านค้าพบว่ากำไร (พันบาท) ŷ สัมพันธ์กับจำนวนวันที่ลงโฆษณา x ตามสมการ {line} "
            f"ถ้าลงโฆษณา {x} วัน พยากรณ์ว่าจะได้กำไรกี่พันบาท",
            f"อุณหภูมิ (องศาเซลเซียส) ŷ ของสารละลายสัมพันธ์กับเวลา x นาที ตามสมการ {line} "
            f"พยากรณ์อุณหภูมิเมื่อเวลาผ่านไป {x} นาที",
        ))
        return MathDraw("", str(a + b * x), prompt=prompt,
                        distractors=[str(a * x + b), str(a + b + x), str(b * x)])


@question_type("math.regression_predict_m6", display_name={"th": "พยากรณ์ค่าจากสมการถดถอยเชิงเส้น"},
               level=M6, topic="การวิเคราะห์การถดถอย")
class RegressionPredictM6(QuestionType):
    _CASES = (("จำนวนชั่วโมงที่อ่านหนังสือ", "คะแนนสอบ", "คะแนน"),
              ("อุณหภูมิ (องศาเซลเซียส)", "ยอดขายน้ำแข็ง", "ถุง"),
              ("งบโฆษณา (พันบาท)", "ยอดขาย", "พันบาท"))

    def build(self, rng: Random) -> GeneratedQuestion:
        xname, yname, unit = rng.choice(self._CASES)
        a = rng.randint(5, 60)
        b = Fraction(rng.choice((5, 8, 12, 15, 25, 35)), 10)
        x = rng.randint(2, 20)
        y = a + b * x
        eq = rf"\hat{{y}} = {a} + {_dec(b)}x"
        if rng.random() < 0.6:
            return _maths([text(f"ให้ x แทน{xname} และ y แทน{yname} จากสมการถดถอย"), content_math(eq),
                           text(f"ถ้า x = {x} จะพยากรณ์ y ได้เท่าใด")], _dec(y),
                          # The slope term alone, adding x, and (a + b)·x.
                          [_dec(b * x), _dec(a + b + x), _dec((a + b) * x), _dec(y + b)],
                          self.topic)
        return _texts([text(f"ให้ x แทน{xname} และ y แทน{yname} จากสมการถดถอย"), content_math(eq),
                       text("ความชัน b หมายความว่าอย่างไร")],
                      f"เมื่อ x เพิ่มขึ้น 1 หน่วย y เพิ่มขึ้นประมาณ {_dec(b)} {unit}",
                      [f"เมื่อ x = 0 จะได้ y = {_dec(b)} {unit}", f"เมื่อ y เพิ่มขึ้น 1 {unit} x เพิ่มขึ้น {_dec(b)} หน่วย",
                       f"เมื่อ x เพิ่มขึ้น 1 หน่วย y เพิ่มขึ้นประมาณ {a} {unit}"], self.topic)


@question_type("math.regression_slope", display_name={"th": "ความชันของเส้นถดถอย"},
               level={"th": "ม.6"}, topic="การวิเคราะห์การถดถอย")
class RegressionSlope(MathType):
    """Points placed exactly on a line, so the least-squares fit is that line."""

    def expr(self, rng: Random, slope_hi: int = 8, intercept_hi: int = 15):
        m = rng.choice([n for n in range(-slope_hi, slope_hi + 1) if n])
        b = rng.randint(-intercept_hi, intercept_hi)
        xs = sorted(rng.sample(range(1, 12), 4))
        rows = r",\quad ".join(f"({x}, {m * x + b})" for x in xs)
        prompt = rng.choice((
            "ข้อมูลเหล่านี้อยู่บนเส้นตรงพอดี จงหาความชันของเส้นถดถอย",
            "ข้อมูล (จำนวนชั่วโมงทำงาน, ค่าจ้างสุทธิเป็นร้อยบาท) ต่อไปนี้อยู่บนเส้นตรงพอดี "
            "จงหาความชันของเส้นถดถอย",
            "ข้อมูล (อายุต้นไม้เป็นปี, ความสูงเป็นเดซิเมตร) ต่อไปนี้อยู่บนเส้นตรงพอดี "
            "จงหาความชันของเส้นถดถอย",
        ))
        return MathDraw(
            rows, str(m), prompt=prompt,
            distractors=[str(-m), str(b), str(m + 1)])
