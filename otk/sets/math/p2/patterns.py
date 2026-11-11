"""แบบรูป

คณิตศาสตร์ · ป.2 · สสวท. พื้นฐาน
Indicators: —

Sets moved here from: math_apply_stage, math_p2.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.sets._support.math_apply_stage import _nums
from otk.sets._support.math_m4 import maths
from otk.sets._support.math_p1 import NumberPatternType, PatternRuleType, RepeatingPatternType
from otk.sets._support.math_p2 import LEVEL

PROVENANCE = Provenance("original")


@question_type("math.repeating_pattern_p2",
               display_name={"th": "แบบรูปซ้ำของรูป (ชุดละ 3 รูป)"},
               level=LEVEL, topic="แบบรูป")
class RepeatingPatternP2(RepeatingPatternType):
    UNIT = 3


@question_type("math.number_pattern_p2",
               display_name={"th": "แบบรูปของจำนวน (ทีละ 2, 5, 10, 100)"},
               level=LEVEL, topic="แบบรูป")
class NumberPatternP2(NumberPatternType):
    STEPS = (2, 5, 10, 100)
    HI = 1000


@question_type("math.pattern_word_p2", display_name={"th": "แบบรูปของจำนวนที่เพิ่มขึ้นหรือลดลงในสถานการณ์"},
               level={"th": "ป.2"}, topic="แบบรูป")
class PatternWordP2(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        step = rng.choice((2, 5, 10, 100))
        k = rng.randint(5, 9)
        who = rng.choice(_story.NAMES)
        # Every number stays within 1,000.
        if rng.random() < 0.5:
            start = step * rng.randint(1, 2) if step == 100 else rng.randint(1, 9) * (step if step != 2 else 1)
            terms = [start + step * i for i in range(3)]
            ans = start + step * (k - 1)
            frames = [f"{who}ออมเงินวันที่ 1, 2, 3 มีเงินสะสม {terms[0]}, {terms[1]}, {terms[2]} บาท "
                      f"ถ้าเพิ่มขึ้นแบบนี้ทุกวัน วันที่ {k} มีเงินสะสมกี่บาท"]
            if step != 100:
                frames.append(f"{who}อ่านหนังสือถึงหน้า {terms[0]}, {terms[1]}, {terms[2]} ในวันที่ 1, 2, 3 "
                              f"ถ้าอ่านเพิ่มเท่ากันทุกวัน วันที่ {k} อ่านถึงหน้าใด")
            stem = rng.choice(frames)
        else:
            if step == 100:
                k = min(k, 7)
            start = step * rng.randint(k + 2, min(k + 9, 1000 // step))
            ans = start - step * k
            stem = (f"ถังมีน้ำ {start} ลิตร ใช้น้ำไปวันละเท่ากัน วันที่ 1, 2, 3 เหลือน้ำ "
                    f"{start - step}, {start - 2 * step}, {start - 3 * step} ลิตร วันที่ {k} เหลือน้ำกี่ลิตร")
        # One step too many or too few, and the step taken as one.
        return maths([text(stem)], str(ans), _nums(ans, ans + step, ans - step, ans + 1, lo=0), self.topic)


@question_type("math.pattern_rule_p2",
               display_name={"th": "บอกความสัมพันธ์ของแบบรูป (ทีละ 2, 5, 10, 100)"},
               level=LEVEL, topic="แบบรูป")
class PatternRuleP2(PatternRuleType):
    STEPS = (2, 5, 10, 100)
    HI = 1000


# ── More patterns (2026-11): the next number, two numbers missing, a far term, a three-shape repeat at a far
# place, growing dots, and counting back ──
from otk.core.registry import question_type  # noqa: E402
from otk.kit.math_problems import ChoiceType, MathDraw, WordProblem  # noqa: E402
from otk.sets._support.math_p2 import LEVEL  # noqa: E402

_P2_STEPS = (2, 5, 10, 100)
_P2_SHAPES = ("○", "△", "□", "☆", "◇", "♡")


@question_type("math.pattern_next_p2", display_name={"th": "จำนวนถัดไปในแบบรูป (ทีละ 2, 5, 10, 100)"},
               level=LEVEL, topic="แบบรูป")
class PatternNextP2(WordProblem):
    def expr(self, rng: Random):
        step = rng.choice(_P2_STEPS)
        down = rng.random() < 0.5
        low = rng.randint(0, 1000 - 5 * step)
        seq = [low + step * i for i in range(6)]
        if down:
            seq.reverse()
        terms, right = seq[:5], seq[5]
        d = right - terms[-1]
        others = [s for s in _P2_STEPS if s != step]
        # Stepping the wrong way; another step size the same way; one step too far.
        return MathDraw("", str(right), prompt=f"{', '.join(map(str, terms))}, ... จำนวนถัดไปคือจำนวนใด",
                        distractors=_story.keep(terms[-1] - d, *[terms[-1] + (-s if down else s) for s in others],
                                                right + d, answer=right, lo=0, hi=1000))


@question_type("math.pattern_two_missing_p2", display_name={"th": "หาจำนวนที่หายไปสองจำนวนในแบบรูป"},
               level=LEVEL, topic="แบบรูป")
class PatternTwoMissingP2(ChoiceType):
    def compose(self, rng: Random):
        step = rng.choice(_P2_STEPS)
        start = rng.randint(1, (1000 - 5 * step) // step) * step
        terms = [start + step * i for i in range(6)]
        i = rng.randrange(1, 4)
        shown = ", ".join("□" if j in (i, i + 2) else str(t) for j, t in enumerate(terms))
        a, b = terms[i], terms[i + 2]
        right = f"{a} และ {b}"
        # Each gap filled by one step only; the gaps swapped; both filled with the neighbour.
        wrongs = [f"{a + 1} และ {b + 1}", f"{b} และ {a}", f"{a} และ {b + step}"]
        return f"จำนวนใดเติมใน □ ตามลำดับ: {shown}", right, wrongs


@question_type("math.pattern_nth_term_p2", display_name={"th": "จำนวนในลำดับที่กำหนดของแบบรูป"},
               level=LEVEL, topic="แบบรูป")
class PatternNthTermP2(WordProblem):
    def expr(self, rng: Random):
        step = rng.choice((2, 5, 10))
        start = rng.randint(1, 30)
        n = rng.randint(6, 12)
        right = start + step * (n - 1)
        prompt = f"นับเพิ่มทีละ {step} เริ่มจาก {start} จำนวนที่ {n} ที่นับได้คือจำนวนใด"
        # One step too many; the step times n; one step short.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(right + step, step * n, right - step, start + n,
                                                answer=right, lo=1))


@question_type("math.pattern_three_nth_p2", display_name={"th": "รูปในลำดับที่กำหนดของแบบรูปซ้ำ (ชุดละ 3 รูป)"},
               level=LEVEL, topic="แบบรูป")
class PatternThreeNthP2(ChoiceType):
    def compose(self, rng: Random):
        unit = rng.sample(_P2_SHAPES, 3)
        k = rng.randint(10, 24)
        right = unit[(k - 1) % 3]
        others = [s for s in _P2_SHAPES if s not in unit]
        shown = "  ".join(unit * 2)
        return (f"แบบรูป {shown}  ... รูปที่ {k} คือรูปใด", right,
                [s for s in unit if s != right] + [rng.choice(others)])


@question_type("math.pattern_growing_dots_p2", display_name={"th": "แบบรูปที่เพิ่มขึ้นทีละเท่ากัน"},
               level=LEVEL, topic="แบบรูป")
class PatternGrowingDotsP2(WordProblem):
    def expr(self, rng: Random):
        first = rng.randint(1, 9)
        step = rng.choice((2, 3, 4, 5))
        n = rng.randint(5, 9)
        right = first + step * (n - 1)
        prompt = (f"รูปที่ 1 มีจุด {first} จุด รูปถัดไปแต่ละรูปมีจุดเพิ่มขึ้นรูปละ {step} จุด "
                  f"รูปที่ {n} มีจุดกี่จุด")
        # Counting one step too many; the step times the figure number; one step too few.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(right + step, step * n, right - step, first * n, answer=right, lo=1))


@question_type("math.pattern_count_back_p2", display_name={"th": "นับลดทีละ 2, 5, 10 หรือ 100"},
               level=LEVEL, topic="แบบรูป")
class PatternCountBackP2(WordProblem):
    def expr(self, rng: Random):
        step = rng.choice(_P2_STEPS)
        k = rng.randint(4, 7)
        start = rng.randint(k - 1, 10) * 100 if step == 100 else rng.randint(step * (k - 1), 900)
        right = start - step * (k - 1)
        prompt = f"นับลดทีละ {step} เริ่มจาก {start} จำนวนที่ {k} ที่นับได้คือจำนวนใด"
        # One count too many or too few; counted down by one instead.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(right - step, right + step, start - (k - 1), start - step * k,
                                                answer=right, lo=0))
