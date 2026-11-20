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


from otk.core.provenance import Provenance  # noqa: E402
from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.concept_bank import Concept, ConceptBankType  # noqa: E402
from otk.kit.math_problems import ChoiceType, MathType, WordProblem  # noqa: E402
from otk.kit.math_problems import frac_tex  # noqa: E402
from otk.sets._support.math_m6 import M6 as LEVEL  # noqa: E402


def _nz6(rng: Random, lo: int, hi: int) -> int:
    return rng.choice((1, -1)) * rng.randint(lo, hi)


def _tk6(*values: str, answer: str) -> list[str]:
    """Distinct TeX distractors, the answer left out."""
    return [v for v in dict.fromkeys(values) if v != answer]


def _fk6(*values, answer: Fraction) -> list[str]:
    """Distinct fraction distractors as TeX, the answer left out."""
    return _tk6(*(frac_tex(Fraction(v)) for v in values), answer=frac_tex(answer))


def _pt6(x, y) -> str:
    return f"({frac_tex(Fraction(x))}, {frac_tex(Fraction(y))})"


def _nk6(*values: int, answer: int, lo: int | None = None) -> list[str]:
    """Distinct whole-number distractors, the answer (and values below lo) left out."""
    return _tk6(*(str(v) for v in values if lo is None or v >= lo), answer=str(answer))


def _num6(v) -> str:
    """A terminating decimal without trailing zeros: Fraction(25, 2) -> 12.5."""
    v = Fraction(v)
    sign = "-" if v < 0 else ""
    v = abs(v)
    whole, rem = divmod(v.numerator, v.denominator)
    if not rem:
        return f"{sign}{whole}"
    digits = ""
    for _ in range(6):
        rem *= 10
        d, rem = divmod(rem, v.denominator)
        digits += str(d)
        if not rem:
            break
    return f"{sign}{whole}.{digits.rstrip('0')}"


def _dk6(*values, answer) -> list[str]:
    """Distinct decimal distractors, the answer left out."""
    return _tk6(*(_num6(v) for v in values), answer=_num6(answer))

# ── More regression (2026-11): the intercept through the means, the x needed for a forecast, what r tells,
# what the slope means, and a residual ──


@question_type("math.regression_intercept_m6", display_name={"th": "หาค่าคงตัวของสมการถดถอยจากค่าเฉลี่ย"}, level=LEVEL,
               topic="การวิเคราะห์การถดถอย")
class RegressionInterceptM6(WordProblem):
    def expr(self, rng: Random):
        b = rng.randint(2, 9)
        xbar, ybar = rng.randint(3, 20), rng.randint(40, 120)
        right = ybar - b * xbar
        prompt = (f"เส้นถดถอย ŷ = a + {b}x ผ่านจุด (x̄, ȳ) เมื่อ x̄ = {xbar} และ ȳ = {ybar} ค่าของ a เท่ากับเท่าใด")
        # The product added; x and y swapped; the slope ignored.
        return MathDraw("", str(right), prompt=prompt, distractors=_nk6(ybar + b * xbar, xbar - b * ybar, ybar - xbar, right + b, answer=right))


@question_type("math.regression_x_needed_m6", display_name={"th": "หาค่า x ที่ทำให้ได้ค่าพยากรณ์ตามต้องการ"}, level=LEVEL,
               topic="การวิเคราะห์การถดถอย")
class RegressionXNeededM6(WordProblem):
    def expr(self, rng: Random):
        a, b = rng.randint(5, 50), rng.randint(2, 9)
        x = rng.randint(2, 30)
        y = a + b * x
        prompt = f"สมการถดถอยคือ ŷ = {a} + {b}x ถ้าต้องการให้ค่าพยากรณ์ ŷ เท่ากับ {y} ต้องให้ x เท่ากับเท่าใด"
        # The y put in for x; not taking off a first; divided only.
        return MathDraw("", str(x), prompt=prompt, distractors=_nk6(a + b * y if y < 30 else y - a, y // b, x + 1, y - a, answer=x, lo=1))


@question_type("math.correlation_meaning_m6", display_name={"th": "ความหมายของสัมประสิทธิ์สหสัมพันธ์"}, level=LEVEL,
               topic="การวิเคราะห์การถดถอย")
class CorrelationMeaningM6(ConceptBankType):
    ITEMS = [
        Concept("ถ้า r = 0.95 หมายความว่าอย่างไร", "สัมพันธ์เชิงเส้นในทิศทางเดียวกันอย่างมาก",
                ("สัมพันธ์เชิงเส้นในทิศทางตรงข้ามอย่างมาก", "ไม่มีความสัมพันธ์เชิงเส้น", "ตัวแปรหนึ่งเป็นสาเหตุของอีกตัวแปร")),
        Concept("ถ้า r = −0.9 หมายความว่าอย่างไร", "สัมพันธ์เชิงเส้นในทิศทางตรงข้ามอย่างมาก",
                ("สัมพันธ์เชิงเส้นในทิศทางเดียวกันอย่างมาก", "ไม่มีความสัมพันธ์เชิงเส้น", "ความสัมพันธ์อ่อนมาก")),
        Concept("ถ้า r ใกล้เคียง 0 หมายความว่าอย่างไร", "แทบไม่มีความสัมพันธ์เชิงเส้น",
                ("สัมพันธ์เชิงเส้นอย่างสมบูรณ์", "สัมพันธ์ในทิศทางเดียวกันอย่างมาก", "สัมพันธ์ในทิศทางตรงข้ามอย่างมาก")),
        Concept("ค่าสัมประสิทธิ์สหสัมพันธ์ r มีค่าได้ในช่วงใด", "ตั้งแต่ −1 ถึง 1", ("ตั้งแต่ 0 ถึง 1", "ตั้งแต่ 0 ถึง 100", "จำนวนจริงใด ๆ")),
    ]


@question_type("math.slope_meaning_m6", display_name={"th": "ความหมายของความชันของเส้นถดถอย"}, level=LEVEL,
               topic="การวิเคราะห์การถดถอย")
class SlopeMeaningM6(ChoiceType):
    def compose(self, rng: Random):
        a, b = rng.randint(10, 60), rng.choice((2, 3, 4, 5, -2, -3))
        stem = f"สมการถดถอยของคะแนนสอบ (y) กับจำนวนชั่วโมงที่อ่านหนังสือ (x) คือ ŷ = {a} + ({b})x ข้อความใดถูกต้อง"
        way = "เพิ่มขึ้น" if b > 0 else "ลดลง"
        other = "ลดลง" if b > 0 else "เพิ่มขึ้น"
        right = f"อ่านเพิ่ม 1 ชั่วโมง คะแนนคาดว่าจะ{way} {abs(b)} คะแนน"
        wrongs = [f"อ่านเพิ่ม 1 ชั่วโมง คะแนนคาดว่าจะ{other} {abs(b)} คะแนน", f"อ่านเพิ่ม 1 ชั่วโมง คะแนนคาดว่าจะ{way} {a} คะแนน",
                  f"อ่านเพิ่ม {abs(b)} ชั่วโมง คะแนนคาดว่าจะ{way} 1 คะแนน"]
        return stem, right, wrongs


@question_type("math.residual_m6", display_name={"th": "ค่าคลาดเคลื่อนจากการพยากรณ์"}, level=LEVEL, topic="การวิเคราะห์การถดถอย")
class ResidualM6(WordProblem):
    def expr(self, rng: Random):
        a, b = rng.randint(10, 40), rng.randint(2, 6)
        x = rng.randint(2, 15)
        e = _nz6(rng, 1, 9)
        y = a + b * x + e
        prompt = f"จากสมการถดถอย ŷ = {a} + {b}x เมื่อ x = {x} ค่าจริงของ y คือ {y} ค่าคลาดเคลื่อน (y − ŷ) เท่ากับเท่าใด"
        # The sign flipped; the forecast itself; the actual value.
        return MathDraw("", str(e), prompt=prompt, distractors=_nk6(-e, a + b * x, y - a, e + 1, answer=e))
