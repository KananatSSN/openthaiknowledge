"""แบบรูป

คณิตศาสตร์ · ป.6 · สสวท. พื้นฐาน
Indicators: ค 1.2 ป.6/1

Sets moved here from: math_p6.
"""

from __future__ import annotations

from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_p2 import _maths
from otk.sets._support.math_p6 import LEVEL

PROVENANCE = Provenance("original")


_PATTERN_TOPIC = "แบบรูป"


@question_type("math.pattern_nth_term_p6",
               display_name={"th": "แบบรูป: หาพจน์ที่ n"},
               level=LEVEL, topic=_PATTERN_TOPIC)
class PatternNthTermP6(WordProblem):
    def expr(self, rng: Random):
        first, step = rng.randint(1, 20), rng.choice((2, 3, 4, 5, 6, 7, 8, 9, 11, 12))
        n = rng.randint(10, 40)
        terms = [first + step * i for i in range(4)]
        ans = first + step * (n - 1)
        p = rng.choice(_story.NAMES)
        prompt = rng.choice((
            f"จากแบบรูป พจน์ที่ {n} คือจำนวนใด",
            f"{p}ออมเงินวันที่ {n} กี่บาท ถ้าออมเงินแต่ละวันเป็นแบบรูปดังนี้ (บาท)",
            f"หอประชุมจัดเก้าอี้แต่ละแถวเป็นแบบรูปดังนี้ แถวที่ {n} มีเก้าอี้กี่ตัว",
        ))
        return MathDraw(r",\ ".join(map(str, terms)) + r",\ \ldots", str(ans),
                        prompt=prompt,
                        # n steps instead of n − 1, and n × step alone.
                        distractors=_story.keep(first + step * n, step * n, ans - first,
                                                first * n, answer=ans, lo=1))


@question_type("math.pattern_rule_expression_p6",
               display_name={"th": "แบบรูป: เขียนความสัมพันธ์ของพจน์ที่ n"},
               level=LEVEL, topic=_PATTERN_TOPIC)
class PatternRuleExpressionP6(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        step = rng.randint(2, 9)
        c = rng.randint(-5, 9)
        while c == 0 or step + c <= 0:
            c = rng.randint(-5, 9)
        terms = [step * n + c for n in range(1, 5)]
        form = lambda k, m: f"{k}n {'+' if m > 0 else '-'} {abs(m)}" if m else f"{k}n"
        first = terms[0]
        wrongs = [f"n + {step}", form(step, c + step), form(c if c > 1 else step + 1, step),
                  f"{first}n"]
        right = form(step, c)
        return _maths([text("จากแบบรูป"), content_math(r",\ ".join(map(str, terms)) + r",\ \ldots"),
                       text("พจน์ที่ n คือข้อใด")], right,
                      [w for w in dict.fromkeys(wrongs) if w != right], self.topic)


@question_type("math.matchstick_pattern_p6",
               display_name={"th": "แบบรูปของรูปเรขาคณิต: ไม้ขีดไฟและรูปสี่เหลี่ยม"},
               level=LEVEL, topic=_PATTERN_TOPIC)
class MatchstickPatternP6(WordProblem):
    _SHAPES = (("รูปสี่เหลี่ยมจัตุรัส", 4, 3), ("รูปสามเหลี่ยม", 3, 2),
               ("รูปหกเหลี่ยม", 6, 5), ("รูปห้าเหลี่ยม", 5, 4))

    def expr(self, rng: Random):
        n = rng.randint(6, 30)
        kind = rng.randrange(3)
        if kind == 0:
            shape, first, step = rng.choice(self._SHAPES)
            ans = first + step * (n - 1)
            prompt = (f"นำไม้ขีดไฟมาต่อเป็น{shape}เรียงติดกันเป็นแถว โดยรูปที่อยู่ติดกันใช้ไม้ขีด"
                      f"ร่วมกัน 1 ก้าน แถวที่มี{shape} 1, 2, 3 รูป ใช้ไม้ขีด "
                      f"{first}, {first + step}, {first + 2 * step} ก้าน ถ้าเรียง {n} รูป "
                      f"ต้องใช้ไม้ขีดไฟกี่ก้าน")
        elif kind == 1:
            # Tables pushed end to end: the joined sides lose their seats.
            table, first, step = rng.choice((("รูปสี่เหลี่ยมจัตุรัส", 4, 2), ("รูปหกเหลี่ยม", 6, 4),
                                              ("รูปสามเหลี่ยม", 3, 1)))
            ans = first + step * (n - 1)
            prompt = (f"นำโต๊ะ{table}มาต่อกันเป็นแถวยาว ด้านละ 1 ที่นั่ง โต๊ะ 1, 2, 3 ตัว นั่งได้ "
                      f"{first}, {first + step}, {first + 2 * step} คน ถ้าต่อโต๊ะ {n} ตัว จะนั่งได้กี่คน")
        else:
            # A path of dark tiles edged with white ones.
            first, step = 8, 2
            ans = first + step * (n - 1)
            prompt = (f"ปูทางเดินด้วยกระเบื้องสีดำเรียงเป็นแถว แล้วล้อมรอบด้วยกระเบื้องสีขาว "
                      f"กระเบื้องสีดำ 1, 2, 3 แผ่น ใช้กระเบื้องสีขาว {first}, {first + step}, "
                      f"{first + 2 * step} แผ่น ถ้ากระเบื้องสีดำมี {n} แผ่น ต้องใช้กระเบื้องสีขาวกี่แผ่น")
        return MathDraw("", str(ans), prompt=prompt,
                        # Counting every shape's sticks separately.
                        distractors=_story.keep(first * n, step * n, ans + step, ans - 1,
                                                answer=ans, lo=1))

from fractions import Fraction  # noqa: E402

from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.math_problems import ChoiceType, WordProblem  # noqa: E402
from otk.sets._support.math_p4 import as_mixed  # noqa: E402
from otk.sets._support.math_p6 import LEVEL  # noqa: E402


def _g6(n: int) -> str:
    """A whole number in TeX with grouped thousands: 4{,}572{,}318."""
    return f"{n:,}".replace(",", "{,}")


def _gk6(*values: int, answer: int, lo: int = 0, hi: int | None = None) -> list[str]:
    """``story.keep`` for grouped numbers."""
    return [_g6(int(v)) for v in _story.keep(*values, answer=answer, lo=lo, hi=hi)]


def _d6(value: int, places: int) -> str:
    """An integer count of 10**-places as a decimal, trailing zeros dropped: (2350, 3) -> 2.35."""
    sign = "-" if value < 0 else ""
    whole, frac = divmod(abs(value), 10 ** places)
    digits = str(frac).rjust(places, "0").rstrip("0") if places else ""
    return f"{sign}{whole}.{digits}" if digits else f"{sign}{whole}"


def _dk6(*values: int, answer: int, places: int, lo: int = 0) -> list[str]:
    """``story.keep`` for decimals held as integer counts of 10**-places."""
    return [_d6(int(v), places) for v in _story.keep(*values, answer=answer, lo=lo)]


def _fk6(*values: Fraction, answer: Fraction) -> list[str]:
    """Distinct fraction distractors as TeX, the answer and non-positive values left out."""
    out: list[str] = []
    for v in values:
        if v > 0 and v != answer and as_mixed(v) not in out:
            out.append(as_mixed(v))
    return out


# ── More patterns (2026-11): the next term, a missing middle term, multiplying patterns, which term has a
# value, square numbers, growing differences, and a repeating colour ──


def _seq6(values) -> str:
    return ", ".join(str(v) for v in values)


@question_type("math.pattern_next_term_p6", display_name={"th": "จำนวนถัดไปในแบบรูป"},
               level=LEVEL, topic="แบบรูป")
class PatternNextTermP6(WordProblem):
    def expr(self, rng: Random):
        step = rng.choice((-9, -8, -7, -6, -5, -4, -3, 3, 4, 5, 6, 7, 8, 9, 11, 12, 15))
        start = rng.randint(60, 120) if step < 0 else rng.randint(1, 40)
        values = [start + step * i for i in range(5)]
        right = values[-1] + step
        # The step the wrong way; two steps; the last term repeated.
        return MathDraw("", str(right), prompt=f"{_seq6(values)}, ... จำนวนถัดไปคือจำนวนใด",
                        distractors=_story.keep(values[-1] - step, values[-1] + 2 * step, values[-1], right + 1,
                                                answer=right, lo=0))


@question_type("math.pattern_missing_middle_p6", display_name={"th": "จำนวนที่หายไปในแบบรูป"},
               level=LEVEL, topic="แบบรูป")
class PatternMissingMiddleP6(WordProblem):
    def expr(self, rng: Random):
        step = rng.randint(3, 15)
        start = rng.randint(1, 50)
        values = [start + step * i for i in range(6)]
        gap = rng.randint(1, 4)
        right = values[gap]
        shown = ["□" if i == gap else str(v) for i, v in enumerate(values)]
        # The term before or after; the step itself.
        return MathDraw("", str(right), prompt=f"{', '.join(shown)} จำนวนใน □ คือจำนวนใด",
                        distractors=_story.keep(values[gap - 1], values[gap + 1], right + 1, step,
                                                answer=right, lo=0))


@question_type("math.pattern_multiply_p6", display_name={"th": "แบบรูปที่เพิ่มขึ้นเป็นเท่า"},
               level=LEVEL, topic="แบบรูป")
class PatternMultiplyP6(WordProblem):
    def expr(self, rng: Random):
        r = rng.choice((2, 3, 4, 5))
        start = rng.randint(1, 5)
        values = [start * r ** i for i in range(4)]
        right = values[-1] * r
        # The last difference added again; the ratio added; doubled.
        return MathDraw("", _g6(right), prompt=f"{_seq6(values)}, ... จำนวนถัดไปคือจำนวนใด",
                        distractors=_gk6(values[-1] + (values[-1] - values[-2]), values[-1] + r, values[-1] * 2,
                                         right + start, answer=right, lo=1))


@question_type("math.pattern_which_term_p6", display_name={"th": "จำนวนนี้เป็นพจน์ที่เท่าใด"},
               level=LEVEL, topic="แบบรูป")
class PatternWhichTermP6(WordProblem):
    def expr(self, rng: Random):
        step = rng.randint(2, 9)
        start = rng.randint(1, 20)
        right = rng.randint(8, 40)
        value = start + step * (right - 1)
        values = [start + step * i for i in range(4)]
        # Divided by the step without the first term; one off either way.
        return MathDraw("", str(right), prompt=f"{_seq6(values)}, ... จำนวน {value} เป็นพจน์ที่เท่าใด",
                        distractors=_story.keep(value // step, right - 1, right + 1, (value - start) // step,
                                                answer=right, lo=1))


@question_type("math.square_numbers_p6", display_name={"th": "แบบรูปจำนวนกำลังสอง"},
               level=LEVEL, topic="แบบรูป")
class SquareNumbersP6(WordProblem):
    def expr(self, rng: Random):
        k = rng.randint(6, 20)
        right = k * k
        # The next odd step mistaken; twice k; one term off.
        return MathDraw("", str(right), prompt=f"1, 4, 9, 16, 25, ... พจน์ที่ {k} คือจำนวนใด",
                        distractors=_story.keep(2 * k, (k - 1) ** 2, (k + 1) ** 2, k * k + k, answer=right, lo=1))


@question_type("math.growing_difference_p6", display_name={"th": "แบบรูปที่ผลต่างเพิ่มขึ้นทีละหนึ่ง"},
               level=LEVEL, topic="แบบรูป")
class GrowingDifferenceP6(WordProblem):
    def expr(self, rng: Random):
        start = rng.randint(1, 20)
        d0 = rng.randint(1, 5)
        values = [start]
        for i in range(5):
            values.append(values[-1] + d0 + i)
        right = values[-1] + d0 + 5
        # The last difference reused; the first difference; two more.
        return MathDraw("", str(right), prompt=f"{_seq6(values)}, ... จำนวนถัดไปคือจำนวนใด",
                        distractors=_story.keep(values[-1] + d0 + 4, values[-1] + d0, right + 1, right + 2,
                                                answer=right, lo=1))


@question_type("math.repeating_colour_p6", display_name={"th": "แบบรูปซ้ำ ลำดับที่เท่าใดเป็นสีใด"},
               level=LEVEL, topic="แบบรูป")
class RepeatingColourP6(ChoiceType):
    _COLOURS = ("แดง", "เขียว", "ฟ้า", "เหลือง", "ม่วง")

    def compose(self, rng: Random):
        k = rng.randint(3, 5)
        cycle = rng.sample(self._COLOURS, k)
        n = rng.randint(20, 99)
        right = cycle[(n - 1) % k]
        shown = ", ".join(cycle * 2)
        stem = f"ลูกปัดเรียงสีเป็นแบบรูปซ้ำ {shown}, ... ลูกปัดลูกที่ {n} เป็นสีใด"
        wrongs = [c for c in cycle if c != right] + [c for c in self._COLOURS if c not in cycle]
        return stem, right, wrongs[:3]
