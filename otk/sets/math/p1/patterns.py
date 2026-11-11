"""แบบรูป

คณิตศาสตร์ · ป.1 · สสวท. พื้นฐาน
Indicators: ค 1.2 ป.1/1

Sets moved here from: math_apply_stage, math_p1.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.math_apply_stage import _nums
from otk.sets._support.math_gaps_shape_data import _choices
from otk.sets._support.math_m4 import maths
from otk.sets._support.math_p1 import (
    LEVEL,
    NumberPatternType,
    PatternRuleType,
    RepeatingPatternType,
)

PROVENANCE = Provenance("original")


@question_type("math.repeating_pattern_p1",
               display_name={"th": "แบบรูปซ้ำของรูป (ชุดละ 2 รูป)"},
               level=LEVEL, topic="แบบรูป")
class RepeatingPatternP1(RepeatingPatternType):
    UNIT = 2


@question_type("math.number_pattern_p1",
               display_name={"th": "แบบรูปของจำนวน (เพิ่มขึ้น/ลดลงทีละ 1 และ 10)"},
               level=LEVEL, topic="แบบรูป")
class NumberPatternP1(NumberPatternType):
    STEPS = (1, 10)


@question_type("math.pattern_word_p1", display_name={"th": "แบบรูปในชีวิตประจำวัน"},
               level={"th": "ป.1"}, topic="แบบรูป")
class PatternWordP1(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            # A repeating pattern: the k-th item is the ((k − 1) mod length)-th of the unit.
            unit = rng.sample(("แดง", "ฟ้า", "เหลือง", "เขียว"), rng.choice((2, 3)))
            k = rng.randint(len(unit) * 2 + 1, 15)
            shown = " ".join(f"สี{c}" for c in (unit * 3)[:len(unit) * 2])
            right = f"สี{unit[(k - 1) % len(unit)]}"
            return _choices([text(f"ร้อยลูกปัดเรียงเป็นแบบรูปซ้ำ {shown} ... ลูกปัดลูกที่ {k} เป็นสีอะไร")],
                            right, [f"สี{c}" for c in ("แดง", "ฟ้า", "เหลือง", "เขียว")], self.topic)
        step = rng.choice((2, 5, 10))
        thing, counter, unit = {2: ("นก", "ตัว", "ขา"), 5: ("ปลาดาว", "ตัว", "แขน"), 10: ("กล่องดินสอ", "กล่อง", "แท่ง")}[step]
        k = rng.randint(4, 10 if step != 10 else 9)
        stem = (f"{thing} 1, 2, 3 {counter} มี{unit} {step}, {2 * step}, {3 * step} {unit} "
                f"ถ้ามี{thing} {k} {counter} จะมี{unit}ทั้งหมดกี่{unit}")
        return maths([text(stem)], str(k * step), _nums(k * step, k + step, (k - 1) * step, (k + 1) * step, lo=1),
                     self.topic)


@question_type("math.pattern_rule_p1",
               display_name={"th": "บอกความสัมพันธ์ของแบบรูป"},
               level=LEVEL, topic="แบบรูป")
class PatternRuleP1(PatternRuleType):
    STEPS = (1, 10)


# ── More patterns (2026-11): the next number, the shape at a far place, growing boxes, counting down by
# tens, colours in turn, and how many of one shape ──

from otk.kit import story as _story  # noqa: E402
from otk.kit.math_problems import ChoiceType, MathDraw, WordProblem  # noqa: E402
from otk.sets._support.math_p1 import LEVEL  # noqa: E402

_PAT_SHAPES = ("○", "△", "□", "☆", "◇", "♡")
_PAT_COLOURS = ("สีแดง", "สีเหลือง", "สีเขียว", "สีฟ้า", "สีชมพู", "สีม่วง")
_THAI_PLACE = {9: "เก้า", 10: "สิบ", 11: "สิบเอ็ด", 12: "สิบสอง", 13: "สิบสาม", 14: "สิบสี่", 15: "สิบห้า"}


@question_type("math.pattern_next_term_p1", display_name={"th": "จำนวนถัดไปในแบบรูป"},
               level=LEVEL, topic="แบบรูป")
class PatternNextTermP1(WordProblem):
    def expr(self, rng: Random):
        step = rng.choice((1, 10))
        if rng.random() < 0.5:
            step = -step
        start = rng.randint(40, 59) if step in (1, -1) else rng.randint(1, 9) + (50 if step < 0 else 0)
        terms = [start + step * i for i in range(5)]
        right = terms[-1] + step
        s = abs(step)
        prompt = f"{', '.join(str(t) for t in terms[:-1])}, {terms[-1]}, ... จำนวนถัดไปคือจำนวนใด"
        # The step taken the wrong way; the other step size; the last term again plus one.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(terms[-1] - step, terms[-1] + (11 - s if step > 0 else s - 11),
                                                right + step, terms[-1] + 1 if step != 1 else terms[-1] + 2,
                                                answer=right, lo=0, hi=100))


@question_type("math.pattern_nth_shape_p1", display_name={"th": "รูปในลำดับที่กำหนดของแบบรูปซ้ำ"},
               level=LEVEL, topic="แบบรูป")
class PatternNthShapeP1(ChoiceType):
    def compose(self, rng: Random):
        a, b = rng.sample(_PAT_SHAPES, 2)
        k = rng.randint(9, 15)
        right = a if k % 2 == 1 else b
        others = [s for s in _PAT_SHAPES if s not in (a, b)]
        stem = f"แบบรูป {a}  {b}  {a}  {b}  {a}  {b}  ... รูปที่{_THAI_PLACE[k]} ({k}) คือรูปใด"
        return stem, right, [b if right == a else a, *rng.sample(others, 2)]


@question_type("math.pattern_growing_p1", display_name={"th": "แบบรูปที่เพิ่มขึ้นในชีวิตประจำวัน"},
               level=LEVEL, topic="แบบรูป")
class PatternGrowingP1(WordProblem):
    def expr(self, rng: Random):
        step = rng.choice((1, 10))
        first = rng.randint(1, 9) if step == 1 else rng.randint(1, 4)
        n = rng.randint(4, 6)
        right = first + step * (n - 1)
        t = rng.choice(_story.THINGS)
        prompt = (f"กล่องใบที่ 1 มี{t.noun} {first} {t.cl} กล่องใบถัดไปมีเพิ่มขึ้นทีละ {step} {t.cl} "
                  f"กล่องใบที่ {n} มี{t.noun}กี่{t.cl}")
        # One step too many; one too few; the first box times the box number; two steps too many.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(right + step, right - step, first * n, right + 2 * step,
                                                answer=right, lo=1, hi=100))


@question_type("math.count_down_tens_p1", display_name={"th": "นับลดทีละ 10"},
               level=LEVEL, topic="แบบรูป")
class CountDownTensP1(WordProblem):
    def expr(self, rng: Random):
        start = rng.randint(6, 9) * 10 + rng.randint(0, 9)
        k = rng.randint(3, 5)
        right = start - 10 * (k - 1)
        prompt = f"นับลดทีละ 10 เริ่มจาก {start} จำนวนที่ {k} ที่นับได้คือจำนวนใด"
        # One count too many or too few; counted down by 1 instead.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(right - 10, right + 10, start - (k - 1), answer=right, lo=0))


@question_type("math.pattern_colours_p1", display_name={"th": "แบบรูปซ้ำของสี"},
               level=LEVEL, topic="แบบรูป")
class PatternColoursP1(ChoiceType):
    def compose(self, rng: Random):
        a, b = rng.sample(_PAT_COLOURS, 2)
        row = [a, b, a, b, a, b, a]
        gap = rng.randrange(2, 7)
        right = row[gap]
        shown = "  ".join("___" if i == gap else c for i, c in enumerate(row))
        others = [c for c in _PAT_COLOURS if c not in (a, b)]
        return f"ลูกปัดร้อยเรียงสีเป็นแบบรูป {shown} ลูกปัดในช่องว่างเป็นสีใด", right, \
            [b if right == a else a, *rng.sample(others, 2)]


@question_type("math.pattern_shape_count_p1", display_name={"th": "นับจำนวนรูปในแบบรูปซ้ำ"},
               level=LEVEL, topic="แบบรูป")
class PatternShapeCountP1(WordProblem):
    def expr(self, rng: Random):
        a, b = rng.sample(_PAT_SHAPES, 2)
        total = rng.randint(8, 16)
        first = rng.random() < 0.5
        right = (total + 1) // 2 if first else total // 2
        prompt = (f"วาดรูปเป็นแบบรูป {a}  {b}  {a}  {b}  ... จนครบ {total} รูป "
                  f"มีรูป {a if first else b} ทั้งหมดกี่รูป")
        # The other shape's count; all the shapes; half rounded the other way.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(total - right, total, right + 1, right - 1, answer=right, lo=1))
