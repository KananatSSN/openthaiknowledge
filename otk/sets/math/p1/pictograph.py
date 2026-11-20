"""แผนภูมิรูปภาพ

คณิตศาสตร์ · ป.1 · สสวท. พื้นฐาน
Indicators: ค 3.1 ป.1/1

Sets moved here from: math_measure_pictures, math_p1.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_measure_pictures import PICTOGRAPHS_P1, _picto_question
from otk.sets._support.math_p1 import LEVEL, _texts

PROVENANCE = Provenance("original")


@question_type("math.pictograph_picture_p1", display_name={"th": "อ่านแผนภูมิรูปภาพจากภาพ"},
               level={"th": "ป.1"}, topic="แผนภูมิรูปภาพ")
class PictographPictureP1(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        return _picto_question(rng.choice(PICTOGRAPHS_P1), rng, self.topic)


@question_type("math.pictograph_read_p1",
               display_name={"th": "อ่านแผนภูมิรูปภาพ"},
               level=LEVEL, topic="แผนภูมิรูปภาพ")
class PictographReadP1(WordProblem):
    def expr(self, rng: Random):
        pg = _story.pictograph(rng)
        row = rng.choice(list(pg.data))
        n = pg.data[row]
        return MathDraw("", str(n),
                        prompt=f"{pg.text}\n{pg.label(row)}มีกี่{pg.chart.unit}",
                        distractors=_story.keep(*[v for c, v in pg.data.items() if c != row],
                                                n + 1, n - 1, answer=n, lo=1))


@question_type("math.pictograph_compare_p1",
               display_name={"th": "แผนภูมิรูปภาพ: มากกว่า น้อยกว่า และรวมกัน"},
               level=LEVEL, topic="แผนภูมิรูปภาพ")
class PictographCompareP1(WordProblem):
    def expr(self, rng: Random):
        pg = _story.pictograph(rng)
        x, y = rng.sample(list(pg.data), 2)
        if pg.data[x] < pg.data[y]:
            x, y = y, x
        a, b, unit = pg.data[x], pg.data[y], pg.chart.unit
        kind = rng.randrange(4)
        if kind == 0:
            return MathDraw("", str(a - b),
                            prompt=f"{pg.text}\n{pg.label(x)}มากกว่า{pg.label(y)}กี่{unit}",
                            distractors=_story.keep(a + b, a, b, a - b + 1, answer=a - b, lo=1))
        if kind == 1:
            return MathDraw("", str(a - b),
                            prompt=f"{pg.text}\n{pg.label(y)}น้อยกว่า{pg.label(x)}กี่{unit}",
                            distractors=_story.keep(a + b, b, a, a - b + 1, answer=a - b, lo=1))
        if kind == 2:
            return MathDraw("", str(a + b),
                            prompt=f"{pg.text}\n{pg.label(x)}และ{pg.label(y)}รวมกันมีกี่{unit}",
                            distractors=_story.keep(a - b, a + b + 1, a + b - 1, answer=a + b))
        total = sum(pg.data.values())
        return MathDraw("", str(total),
                        prompt=f"{pg.text}\nจากแผนภูมิ รวมทั้งหมดมีกี่{unit}",
                        distractors=_story.keep(total - b, total + 1, total - 1,
                                                answer=total))


@question_type("math.pictograph_most_p1",
               display_name={"th": "แผนภูมิรูปภาพ: มากที่สุดและน้อยที่สุด"},
               level=LEVEL, topic="แผนภูมิรูปภาพ")
class PictographMostP1(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        pg = _story.pictograph(rng)
        most = rng.random() < 0.5
        pick = (max if most else min)(pg.data, key=pg.data.get)
        q = _texts(pick, [c for c in pg.data if c != pick], self.topic)
        q.stem = [text(pg.text),
                  text(pg.chart.most.format(most="มากที่สุด" if most else "น้อยที่สุด"))]
        return q


# ── More pictographs (2026-11): most minus least, a row after more are added, the order of the rows, how
# many rows are above a number, a true statement, and two rows together against a third ──

from otk.kit.math_problems import ChoiceType  # noqa: E402


@question_type("math.pictograph_range_p1", display_name={"th": "แผนภูมิรูปภาพ: มากที่สุดมากกว่าน้อยที่สุดกี่"},
               level=LEVEL, topic="แผนภูมิรูปภาพ")
class PictographRangeP1(WordProblem):
    def expr(self, rng: Random):
        pg = _story.pictograph(rng)
        hi_row = max(pg.data, key=pg.data.get)
        lo_row = min(pg.data, key=pg.data.get)
        a, b = pg.data[hi_row], pg.data[lo_row]
        right = a - b
        prompt = (f"{pg.text}\nรายการที่มีมากที่สุดมากกว่ารายการที่มีน้อยที่สุดกี่{pg.chart.unit}")
        # Added instead; the most alone; one off.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(a + b, a, b, right + 1, answer=right, lo=1))


@question_type("math.pictograph_add_more_p1", display_name={"th": "แผนภูมิรูปภาพ: ถ้าเพิ่มอีกจะมีเท่าใด"},
               level=LEVEL, topic="แผนภูมิรูปภาพ")
class PictographAddMoreP1(WordProblem):
    def expr(self, rng: Random):
        pg = _story.pictograph(rng)
        row = rng.choice(list(pg.data))
        n = pg.data[row]
        k = rng.randint(2, 9)
        right = n + k
        prompt = f"{pg.text}\nถ้า{pg.label(row)}เพิ่มขึ้นอีก {k} {pg.chart.unit} จะมีทั้งหมดกี่{pg.chart.unit}"
        # The chart's number alone; the number added only; one off.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(n, k, right + 1, right - 1, abs(n - k), answer=right, lo=1))


@question_type("math.pictograph_order_p1", display_name={"th": "แผนภูมิรูปภาพ: เรียงลำดับจากมากไปน้อย"},
               level=LEVEL, topic="แผนภูมิรูปภาพ")
class PictographOrderP1(ChoiceType):
    def compose(self, rng: Random):
        pg = _story.pictograph(rng)
        up = rng.random() < 0.5
        ordered = sorted(pg.data, key=pg.data.get, reverse=not up)
        place = rng.choice((1, 2))
        right = ordered[place]
        stem = (f"{pg.text}\nเมื่อเรียงจาก{'น้อยไปมาก' if up else 'มากไปน้อย'} "
                f"รายการใดอยู่ลำดับที่{'สอง' if place == 1 else 'สาม'}")
        return stem, right, [r for r in ordered if r != right]


@question_type("math.pictograph_count_above_p1", display_name={"th": "แผนภูมิรูปภาพ: นับรายการที่มากกว่าจำนวนที่กำหนด"},
               level=LEVEL, topic="แผนภูมิรูปภาพ")
class PictographCountAboveP1(WordProblem):
    def expr(self, rng: Random):
        pg = _story.pictograph(rng)
        values = sorted(pg.data.values())
        k = rng.randint(values[0], values[-1] - 1)
        right = sum(v > k for v in values)
        prompt = f"{pg.text}\nมีกี่รายการที่มีมากกว่า {k} {pg.chart.unit}"
        # Counting "at least" instead; the rows below; all of them.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(sum(v >= k for v in values), len(values) - right, len(values),
                                                right - 1, right + 1, answer=right, lo=0, hi=len(values)))


@question_type("math.pictograph_true_statement_p1", display_name={"th": "แผนภูมิรูปภาพ: ข้อความใดถูกต้อง"},
               level=LEVEL, topic="แผนภูมิรูปภาพ")
class PictographTrueStatementP1(ChoiceType):
    def compose(self, rng: Random):
        pg = _story.pictograph(rng)
        x, y = rng.sample(list(pg.data), 2)
        if pg.data[x] < pg.data[y]:
            x, y = y, x
        a, b, unit = pg.data[x], pg.data[y], pg.chart.unit
        lx, ly = pg.label(x), pg.label(y)
        right = f"{lx}มากกว่า{ly} {a - b} {unit}"
        wrongs = [f"{ly}มากกว่า{lx} {a - b} {unit}", f"{lx}มากกว่า{ly} {a + b} {unit}",
                  f"{lx}มากกว่า{ly} {a - b + 1} {unit}"]
        return f"{pg.text}\nข้อความใดถูกต้อง", right, wrongs


@question_type("math.pictograph_two_rows_p1", display_name={"th": "แผนภูมิรูปภาพ: สองรายการรวมกันเทียบกับอีกรายการ"},
               level=LEVEL, topic="แผนภูมิรูปภาพ")
class PictographTwoRowsP1(WordProblem):
    def expr(self, rng: Random):
        pg = _story.pictograph(rng)
        ordered = sorted(pg.data, key=pg.data.get)
        z = ordered[0]
        x, y = rng.sample(ordered[1:], 2)
        a, b, c = pg.data[x], pg.data[y], pg.data[z]
        right = a + b - c
        prompt = (f"{pg.text}\n{pg.label(x)}และ{pg.label(y)}รวมกัน มากกว่า{pg.label(z)}กี่{pg.chart.unit}")
        # Only one row compared; the sum alone; one off.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(a - c, b - c, a + b, a + b + c, right + 1, answer=right, lo=1))
