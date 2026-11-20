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


from otk.core.provenance import Provenance  # noqa: E402
from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.math_problems import MathType, WordProblem  # noqa: E402
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

# ── More measures of position (2026-11): a percentile's value, a decile's position, a quartile's position,
# how many below a percentile, a quartile from data, and a percentile rank from a ranking ──


@question_type("math.percentile_value_m6", display_name={"th": "ค่าของเปอร์เซ็นไทล์จากข้อมูล"}, level=LEVEL,
               topic="การวัดตำแหน่งข้อมูล")
class PercentileValueM6(WordProblem):
    def expr(self, rng: Random):
        n, k = rng.choice(((19, 25), (19, 50), (19, 75), (9, 50), (39, 25), (39, 75), (9, 20), (9, 80)))
        data = sorted(rng.sample(range(10, 100), n))
        pos = k * (n + 1) // 100
        right = data[pos - 1]
        prompt = f"ข้อมูลเรียงจากน้อยไปมากคือ {', '.join(map(str, data))} เปอร์เซ็นไทล์ที่ {k} เท่ากับเท่าใด"
        # The neighbouring values; the position itself.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_nk6(data[pos], data[pos - 2] if pos > 1 else data[pos + 1], pos, k, answer=right, lo=1))


@question_type("math.decile_position_m6", display_name={"th": "ตำแหน่งของเดไซล์"}, level=LEVEL, topic="การวัดตำแหน่งข้อมูล")
class DecilePositionM6(MathType):
    def expr(self, rng: Random):
        n, k = rng.randint(9, 99), rng.randint(1, 9)
        right = Fraction(k * (n + 1), 10)
        return MathDraw(rf"n = {n}, \quad D_{{{k}}}", _num6(right), prompt="ข้อมูลเรียงจากน้อยไปมาก ตำแหน่งของเดไซล์นี้คือตำแหน่งที่เท่าใด",
                        distractors=_dk6(Fraction(k * n, 10), Fraction(k * (n + 1), 100), Fraction(k * (n + 1), 4), right + 1,
                                         answer=right))


@question_type("math.quartile_position_m6", display_name={"th": "ตำแหน่งของควอร์ไทล์"}, level=LEVEL, topic="การวัดตำแหน่งข้อมูล")
class QuartilePositionM6(MathType):
    def expr(self, rng: Random):
        n, k = rng.randint(7, 99), rng.randint(1, 3)
        right = Fraction(k * (n + 1), 4)
        return MathDraw(rf"n = {n}, \quad Q_{{{k}}}", _num6(right), prompt="ข้อมูลเรียงจากน้อยไปมาก ตำแหน่งของควอร์ไทล์นี้คือตำแหน่งที่เท่าใด",
                        distractors=_dk6(Fraction(k * n, 4), Fraction(k * (n + 1), 10), Fraction(n + 1, 4), right + 1, answer=right))


@question_type("math.count_below_percentile_m6", display_name={"th": "จำนวนคนที่มีคะแนนต่ำกว่าเปอร์เซ็นไทล์"}, level=LEVEL,
               topic="การวัดตำแหน่งข้อมูล")
class CountBelowPercentileM6(WordProblem):
    def expr(self, rng: Random):
        n = rng.choice((200, 300, 400, 500, 1000))
        p = rng.choice((10, 20, 25, 40, 60, 75, 80, 90))
        right = n * p // 100
        prompt = f"นักเรียน {n} คนเข้าสอบ คะแนนของเก่งอยู่ที่เปอร์เซ็นไทล์ที่ {p} มีนักเรียนประมาณกี่คนที่ได้คะแนนน้อยกว่าเก่ง"
        # Those above; the percentile itself; half.
        return MathDraw("", str(right), prompt=prompt, distractors=_nk6(n - right, p, n // 2, right + 10, answer=right, lo=1))


@question_type("math.quartile_from_list_m6", display_name={"th": "ควอร์ไทล์ที่ 1 หรือ 3 จากข้อมูล"}, level=LEVEL,
               topic="การวัดตำแหน่งข้อมูล")
class QuartileFromListM6(WordProblem):
    def expr(self, rng: Random):
        n = rng.choice((7, 11, 15))
        data = sorted(rng.sample(range(10, 100), n))
        k = rng.choice((1, 3))
        right = data[k * (n + 1) // 4 - 1]
        prompt = f"ข้อมูลเรียงจากน้อยไปมากคือ {', '.join(map(str, data))} ควอร์ไทล์ที่ {k} เท่ากับเท่าใด"
        other = data[(4 - k) * (n + 1) // 4 - 1]
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_nk6(other, data[n // 2], data[k * (n + 1) // 4], k * (n + 1) // 4, answer=right, lo=1))


@question_type("math.percentile_rank_from_order_m6", display_name={"th": "เปอร์เซ็นไทล์จากอันดับที่"}, level=LEVEL,
               topic="การวัดตำแหน่งข้อมูล")
class PercentileRankFromOrderM6(WordProblem):
    def expr(self, rng: Random):
        n = rng.choice((50, 100, 200, 400))
        below = rng.randint(1, 19) * n // 20
        right = below * 100 // n
        prompt = f"ในการสอบที่มีผู้เข้าสอบ {n} คน มีผู้ได้คะแนนน้อยกว่าฝ้าย {below} คน คะแนนของฝ้ายอยู่ที่เปอร์เซ็นไทล์ที่เท่าใด"
        # Those above instead; the count itself; one more.
        return MathDraw("", str(right), prompt=prompt, distractors=_nk6(100 - right, below, right + 1, right + 5, answer=right, lo=1))
