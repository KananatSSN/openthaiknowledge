"""แบบรูป

คณิตศาสตร์ · ป.3 · สสวท. พื้นฐาน
Indicators: ค 1.2 ป.3/1

Sets moved here from: math_p3, math_pictures_p2.
"""

from __future__ import annotations

from random import Random

from otk.core.content import image, text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_diagrams import _math_q
from otk.sets._support.math_p1 import NumberPatternType, PatternRuleType
from otk.sets._support.math_p3 import LEVEL
from otk.sets._support.math_pictures import _near
from otk.sets._support.math_pictures_p2 import GROWING, P3

PROVENANCE = Provenance("original")


_P3_STEPS = (3, 4, 6, 7, 8, 9, 25, 50)


@question_type("math.number_pattern_p3",
               display_name={"th": "แบบรูปของจำนวนที่เพิ่มขึ้นหรือลดลงทีละเท่า ๆ กัน"},
               level=LEVEL, topic="แบบรูป")
class NumberPatternP3(NumberPatternType):
    STEPS = _P3_STEPS
    HI = 1000


@question_type("math.pattern_rule_p3",
               display_name={"th": "บอกความสัมพันธ์ของแบบรูป (ทีละเท่า ๆ กัน)"},
               level=LEVEL, topic="แบบรูป")
class PatternRuleP3(PatternRuleType):
    STEPS = _P3_STEPS
    HI = 1000


@question_type("math.growing_pattern_picture_p3", display_name={"th": "แบบรูปที่เพิ่มขึ้นจากภาพ"},
               level=P3, topic="แบบรูป")
class GrowingPatternPictureP3(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        g = rng.choice(GROWING)
        piece = "รูปสี่เหลี่ยม" if g.style == "tile" else "จุด"
        img = image(g.asset_id, alt=f"ภาพแบบรูปสามรูปแรก ประกอบด้วย{piece}")
        if rng.random() < 0.3:
            step = g.rows
            return _math_q([text(f"จากแบบรูป แต่ละรูปมี{piece}เพิ่มขึ้นจากรูปก่อนกี่{'รูป' if g.style == 'tile' else 'จุด'}"),
                            img], str(step), _near(step, g.count(1), g.count(3), step + 2, lo=1),
                           self.topic)
        n = rng.choice((4, 5, 6, 8, 10))
        right = g.count(n)
        # One more per figure instead of one more column; n pieces per row;
        # an off-by-one figure.
        wrongs = [g.count(3) + (n - 3), g.rows * n, g.count(n + 1), g.count(n - 1)]
        return _math_q([text(f"ถ้าแบบรูปนี้เพิ่มขึ้นแบบเดิมไปเรื่อย ๆ รูปที่ {n} มี{piece}ทั้งหมดเท่าใด"), img],
                       str(right), _near(right, *wrongs, lo=1), self.topic)


@question_type("math.growing_pattern_p3",
               display_name={"th": "แบบรูปที่เพิ่มขึ้น: รูปที่เท่าใดมีกี่ชิ้น"},
               level=LEVEL, topic="แบบรูป")
class GrowingPatternP3(WordProblem):
    _THINGS = (("จุด", "จุด"), ("ไม้ขีดไฟ", "ก้าน"), ("ลูกปัด", "เม็ด"), ("บล็อกไม้", "ก้อน"))

    def expr(self, rng: Random):
        thing, cl = rng.choice(self._THINGS)
        first, step = rng.randint(2, 9), rng.randint(2, 6)
        k = rng.randint(5, 12)
        shown = ", ".join(f"รูปที่ {i + 1} มี {first + step * i} {cl}" for i in range(3))
        ans = first + step * (k - 1)
        return MathDraw("", str(ans),
                        prompt=f"แบบรูปของ{thing}: {shown} ถ้าเพิ่มขึ้นแบบนี้ไปเรื่อย ๆ "
                               f"รูปที่ {k} มี{thing}กี่{cl}",
                        # Stepping k times instead of k − 1, and k × step alone.
                        distractors=_story.keep(first + step * k, step * k, ans - step,
                                                first * k, answer=ans, lo=1))


# ── More patterns (2026-11): the next term, a far term, two missing, a four-shape repeat at a far place,
# money spent day by day, and which number belongs to a pattern ──
from otk.core.registry import question_type  # noqa: E402
from otk.kit.math_problems import ChoiceType, WordProblem  # noqa: E402
from otk.sets._support.math_p3 import LEVEL  # noqa: E402

_P3_STEPS = (3, 4, 6, 7, 8, 9, 25, 50, 100, 1000)
_P3_SHAPES = ("○", "△", "□", "☆", "◇", "♡", "▲", "■")


from otk.core.content import text as _text_block  # noqa: E402
from otk.core.registry import QuestionType as _QT  # noqa: E402
from otk.sets._support.math_p2 import _maths as _fixed_maths  # noqa: E402


@question_type("math.pattern_next_p3", display_name={"th": "จำนวนถัดไปในแบบรูป (ทีละเท่า ๆ กัน)"},
               level=LEVEL, topic="แบบรูป")
class PatternNextP3(WordProblem):
    def expr(self, rng: Random):
        step = rng.choice(_P3_STEPS)
        down = rng.random() < 0.5
        low = rng.randint(1, 20) * (step if step >= 25 else 1) + (0 if step >= 25 else rng.randint(0, 50))
        seq = [low + step * i for i in range(6)]
        if down:
            seq.reverse()
        terms, right = seq[:5], seq[5]
        d = right - terms[-1]
        # The wrong way; one step too far; a step one larger.
        return MathDraw("", str(right), prompt=f"{', '.join(map(str, terms))}, ... จำนวนถัดไปคือจำนวนใด",
                        distractors=_story.keep(terms[-1] - d, right + d, terms[-1] + d + (1 if d > 0 else -1),
                                                right + (10 if d > 0 else -10), answer=right, lo=0))


@question_type("math.pattern_far_term_p3", display_name={"th": "จำนวนในลำดับที่กำหนดของแบบรูป (ทีละเท่า ๆ กัน)"},
               level=LEVEL, topic="แบบรูป")
class PatternFarTermP3(WordProblem):
    def expr(self, rng: Random):
        step = rng.choice((3, 4, 6, 7, 8, 9, 25))
        start = rng.randint(1, 50)
        n = rng.randint(8, 20)
        right = start + step * (n - 1)
        terms = ", ".join(str(start + step * i) for i in range(4))
        prompt = f"แบบรูป {terms}, ... จำนวนที่ {n} คือจำนวนใด"
        # n steps instead of n − 1; the step times n; one step short.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(right + step, step * n, right - step, start + n, answer=right, lo=1))


@question_type("math.pattern_two_missing_p3", display_name={"th": "หาจำนวนที่หายไปสองจำนวนในแบบรูป (ทีละเท่า ๆ กัน)"},
               level=LEVEL, topic="แบบรูป")
class PatternTwoMissingP3(ChoiceType):
    def compose(self, rng: Random):
        step = rng.choice((3, 4, 6, 7, 8, 9, 25, 50))
        start = rng.randint(1, 100)
        terms = [start + step * i for i in range(6)]
        i = rng.randrange(1, 4)
        shown = ", ".join("□" if j in (i, i + 2) else str(t) for j, t in enumerate(terms))
        a, b = terms[i], terms[i + 2]
        return (f"จำนวนใดเติมใน □ ตามลำดับ: {shown}", f"{a} และ {b}",
                [f"{a + 1} และ {b + 1}", f"{b} และ {a}", f"{a} และ {b + step}"])


@question_type("math.pattern_four_shapes_p3", display_name={"th": "รูปในลำดับที่กำหนดของแบบรูปซ้ำ (ชุดละ 4 รูป)"},
               level=LEVEL, topic="แบบรูป")
class PatternFourShapesP3(ChoiceType):
    def compose(self, rng: Random):
        unit = rng.sample(_P3_SHAPES, 4)
        k = rng.randint(13, 40)
        right = unit[(k - 1) % 4]
        others = [s for s in _P3_SHAPES if s not in unit]
        return (f"แบบรูป {'  '.join(unit * 2)}  ... รูปที่ {k} คือรูปใด", right,
                [s for s in unit if s != right][:2] + [rng.choice(others)])


@question_type("math.pattern_spending_p3", display_name={"th": "แบบรูปที่ลดลงในชีวิตประจำวัน"},
               level=LEVEL, topic="แบบรูป")
class PatternSpendingP3(WordProblem):
    def expr(self, rng: Random):
        per = rng.choice((15, 20, 25, 30, 40, 50))
        days = rng.randint(4, 9)
        have = per * days + rng.randint(1, 10) * 10
        right = have - per * days
        p = rng.choice(_story.NAMES)
        prompt = f"{p}มีเงิน {have} บาท ใช้วันละ {per} บาท เมื่อผ่านไป {days} วัน {p}เหลือเงินกี่บาท"
        # One day more or fewer; only one day spent.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(right - per, right + per, have - per, per * days, answer=right, lo=0))


@question_type("math.pattern_member_p3", display_name={"th": "จำนวนใดอยู่ในแบบรูป"},
               level=LEVEL, topic="แบบรูป")
class PatternMemberP3(_QT):
    """Fixed choices: a number from another draw could also belong to the pattern."""

    def build(self, rng: Random):
        step = rng.choice((3, 4, 6, 7, 8, 9))
        start = rng.randint(1, 9)
        k = rng.randint(8, 20)
        right = start + step * k
        terms = ", ".join(str(start + step * i) for i in range(4))
        # Numbers one or two off the pattern, never on it (step ≥ 3).
        wrongs = _story.keep(right + 1, right - 1, right + step + 1, right - 2, answer=right, lo=1)
        return _fixed_maths([_text_block(f"แบบรูป {terms}, ... จำนวนใดอยู่ในแบบรูปนี้")], str(right), wrongs, self.topic)