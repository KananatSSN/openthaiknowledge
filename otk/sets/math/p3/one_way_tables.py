"""ตารางทางเดียว

คณิตศาสตร์ · ป.3 · สสวท. พื้นฐาน
Indicators: ค 3.1 ป.3/*

Sets moved here from: math, math_gaps_indicators, math_gaps_shape_data, math_p3.
"""

from __future__ import annotations

from collections import Counter
from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.distractors import fixed
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_gaps_shape_data import _TALLY, _choices, _table
from otk.sets._support.math_p2 import _texts
from otk.sets._support.math_p3 import LEVEL

PROVENANCE = Provenance("original")


_SURVEYS = (
    ("ผลไม้ที่ชอบ", ("ส้ม", "มะม่วง", "กล้วย", "แตงโม")),
    ("สีที่ชอบ", ("แดง", "ฟ้า", "เขียว", "เหลือง")),
    ("กีฬาที่ชอบ", ("ฟุตบอล", "ว่ายน้ำ", "แบดมินตัน", "วิ่ง")),
    ("สัตว์เลี้ยงที่มีที่บ้าน", ("แมว", "สุนัข", "ปลา", "นก")),
)


NL = chr(10)       # a new stem line


@question_type("math.table_most_p3",
               display_name={"th": "อ่านตารางทางเดียว: มากที่สุดและน้อยที่สุด"},
               level=LEVEL, topic="ตารางทางเดียว")
class TableMostP3(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        tb = _story.one_way_table(rng)
        most = rng.random() < 0.5
        pick = (max if most else min)(tb.data, key=tb.data.get)
        # The opposite end first: reading "น้อยที่สุด" as "มากที่สุด".
        other = (min if most else max)(tb.data, key=tb.data.get)
        wrongs = [other] + [r for r in tb.data if r not in (pick, other)]
        return _texts([text(tb.text),
                       text(tb.table.most.format(most="มากที่สุด" if most else "น้อยที่สุด"))],
                      pick, wrongs, self.topic)


@question_type("math.tally_to_table_p3", display_name={"th": "เขียนตารางทางเดียวจากข้อมูล"},
               level={"th": "ป.3"}, topic="ตารางทางเดียว")
class TallyToTableP3(QuestionType):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        about, kinds = rng.choice(_SURVEYS)
        kinds = list(kinds[:rng.choice((3, 4))])
        while True:
            answers = [rng.choice(kinds) for _ in range(rng.randint(12, 18))]
            counts = Counter(answers)
            if len(counts) == len(kinds) and len(set(counts.values())) > 1:
                break
        listed = " ".join(answers)
        stem_start = f"ถามนักเรียน {len(answers)} คนเรื่อง{about} ได้คำตอบดังนี้: {listed}"
        if rng.random() < 0.5:
            k = rng.choice(kinds)
            right = counts[k]
            wrongs = [str(v) for v in dict.fromkeys((right + 1, right - 1, len(answers) - right, right + 2))
                      if v > 0 and v != right]
            return _choices([text(f"{stem_start} ถ้าเขียนเป็นตารางทางเดียว ช่องจำนวนนักเรียนที่ตอบ{k}ต้องเป็นเท่าใด")],
                            str(right), wrongs, self.topic)

        def table(c):
            return "   ".join(f"{k} {c[k]}" for k in kinds)

        right = table(counts)
        # Two rows swapped, one row miscounted, and every row one off.
        a, b = rng.choice([(x, y) for x in kinds for y in kinds if x < y and counts[x] != counts[y]])
        swapped = dict(counts)
        swapped[a], swapped[b] = counts[b], counts[a]
        off = dict(counts)
        off[rng.choice(kinds)] += 1
        wrongs = [table(swapped), table(off), table({k: counts[k] + (1 if i % 2 else -1)
                                                     for i, k in enumerate(kinds)})]
        return _choices([text(f"{stem_start} ตารางทางเดียวในข้อใดถูกต้อง")], right, wrongs, self.topic)


@question_type("math.pictograph_make_p3", display_name={"th": "เขียนแผนภูมิรูปภาพจากตาราง"},
               level={"th": "ป.3"}, topic="ตารางทางเดียว")
class PictographMakeP3(QuestionType):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        title, rows, unit = rng.choice(_TALLY)
        key = rng.choice((2, 5, 10))
        counts = rng.sample([key * v for v in range(2, 10)], len(rows))
        i = rng.randrange(len(rows))
        table = _table(title, rows, counts, unit)
        if rng.random() < 0.5:
            right = counts[i] // key
            stem = [text(f"{table}\nถ้าเขียนแผนภูมิรูปภาพ โดยให้ ● 1 รูป แทน {key} {unit} "
                         f"แถวของ{rows[i]} ต้องมี ● กี่รูป")]
            # One symbol per unit, then off-by-one slips.
            wrongs = _story.keep(counts[i], right * 2, right + 1, right - 1, answer=right, lo=1)[:3]
            return GeneratedQuestion(stem=stem, correct=[content_math(str(right))],
                                     distractors=fixed(*[[content_math(w)] for w in wrongs]),
                                     topic=self.topic)
        j = (i + 1) % len(rows)
        row = lambda v: " ".join(["●"] * (v // key))
        right = f"{rows[i]}: {row(counts[i])}   {rows[j]}: {row(counts[j])}"
        # One symbol per unit, the two rows swapped, one symbol short.
        wrongs = [f"{rows[i]}: {row(counts[j])}   {rows[j]}: {row(counts[i])}",
                  f"{rows[i]}: {row(counts[i] - key)}   {rows[j]}: {row(counts[j])}",
                  f"{rows[i]}: {row(counts[i])}   {rows[j]}: {row(counts[j] + key)}"]
        stem = [text(f"{table}\nถ้าให้ ● 1 รูป แทน {key} {unit} "
                     f"แผนภูมิรูปภาพของ{rows[i]}และ{rows[j]}ข้อใดถูกต้อง")]
        return _choices(stem, right, wrongs, self.topic)


@question_type("math.table_read_p3",
               display_name={"th": "อ่านตารางทางเดียว: ค่า ผลต่าง และผลรวม"},
               level=LEVEL, topic="ตารางทางเดียว")
class TableReadP3(WordProblem):
    def expr(self, rng: Random):
        tb = _story.one_way_table(rng)
        x, y = rng.sample(list(tb.data), 2)
        if tb.data[x] < tb.data[y]:
            x, y = y, x
        a, b, unit = tb.data[x], tb.data[y], tb.table.unit
        lx, ly = (tb.table.label.format(r=r) for r in (x, y))
        count = tb.table.count
        kind = rng.randrange(3)
        if kind == 0:
            return MathDraw("", str(a), prompt=f"{tb.text}{NL}{lx}มี{count}กี่{unit}",
                            distractors=_story.keep(*[v for v in tb.data.values() if v != a],
                                                    answer=a))
        if kind == 1:
            return MathDraw("", str(a - b),
                            prompt=f"{tb.text}{NL}{lx}มี{count}มากกว่า{ly}กี่{unit}",
                            distractors=_story.keep(a + b, a - b + 10, a - b - 10, answer=a - b,
                                                    lo=1))
        return MathDraw("", str(a + b),
                        prompt=f"{tb.text}{NL}{lx}และ{ly}มี{count}รวมกันกี่{unit}",
                        distractors=_story.keep(a - b, a + b + 10, a + b - 10, answer=a + b))


@question_type("math.table_sum",
               display_name={"th": "หาผลรวมจากตารางทางเดียว"}, level={"th": "ป.3"},
               topic="ตารางทางเดียว")
class TableSum(WordProblem):
    def expr(self, rng: Random):
        tb = _story.one_way_table(rng, lo=5, hi=120, rows=rng.choice((3, 4)))
        total = sum(tb.data.values())
        values = list(tb.data.values())
        return MathDraw(
            "", str(total),
            prompt=f"{tb.text}\nรวมทั้งหมดกี่{tb.table.unit}",
            # Leaving out the last row, then a ten gained or lost in carrying.
            distractors=_story.keep(total - values[-1], total + 10, total - 10,
                                    max(values), answer=total, lo=1))


# ── More one-way tables (2026-11): most minus least, the order of the rows, rows above a number, two rows
# against a third, and a true statement ──
from otk.core.registry import question_type  # noqa: E402
from otk.kit.math_problems import ChoiceType, WordProblem  # noqa: E402
from otk.sets._support.math_p3 import LEVEL  # noqa: E402


def _row(tb, r: str) -> str:
    return tb.table.label.format(r=r)


@question_type("math.table_range_p3", display_name={"th": "ตารางทางเดียว: มากที่สุดมากกว่าน้อยที่สุดเท่าใด"},
               level=LEVEL, topic="ตารางทางเดียว")
class TableRangeP3(WordProblem):
    def expr(self, rng: Random):
        tb = _story.one_way_table(rng)
        a, b = max(tb.data.values()), min(tb.data.values())
        right = a - b
        unit = tb.table.unit
        return MathDraw("", str(right), prompt=f"{tb.text}\nรายการที่มากที่สุดมากกว่ารายการที่น้อยที่สุดกี่{unit}",
                        distractors=_story.keep(a + b, a, b, right + 10, answer=right, lo=1))


@question_type("math.table_order_p3", display_name={"th": "ตารางทางเดียว: เรียงลำดับ"},
               level=LEVEL, topic="ตารางทางเดียว")
class TableOrderP3(ChoiceType):
    def compose(self, rng: Random):
        tb = _story.one_way_table(rng)
        up = rng.random() < 0.5
        ordered = sorted(tb.data, key=tb.data.get, reverse=not up)
        place = rng.choice((1, 2))
        right = ordered[place]
        stem = (f"{tb.text}\nเมื่อเรียงจาก{'น้อยไปมาก' if up else 'มากไปน้อย'} "
                f"รายการใดอยู่ลำดับที่{'สอง' if place == 1 else 'สาม'}")
        return stem, right, [r for r in ordered if r != right]


@question_type("math.table_count_above_p3", display_name={"th": "ตารางทางเดียว: นับรายการที่มากกว่าจำนวนที่กำหนด"},
               level=LEVEL, topic="ตารางทางเดียว")
class TableCountAboveP3(WordProblem):
    def expr(self, rng: Random):
        tb = _story.one_way_table(rng)
        values = sorted(tb.data.values())
        k = rng.randint(values[0], values[-1] - 1)
        right = sum(v > k for v in values)
        return MathDraw("", str(right), prompt=f"{tb.text}\nมีกี่รายการที่มากกว่า {k} {tb.table.unit}",
                        distractors=_story.keep(sum(v >= k for v in values), len(values) - right, len(values),
                                                right - 1, right + 1, answer=right, lo=0, hi=len(values)))


@question_type("math.table_two_rows_p3", display_name={"th": "ตารางทางเดียว: สองรายการรวมกันเทียบกับอีกรายการ"},
               level=LEVEL, topic="ตารางทางเดียว")
class TableTwoRowsP3(WordProblem):
    def expr(self, rng: Random):
        tb = _story.one_way_table(rng)
        ordered = sorted(tb.data, key=tb.data.get)
        z = ordered[0]
        x, y = rng.sample(ordered[1:], 2)
        a, b, c = tb.data[x], tb.data[y], tb.data[z]
        right = a + b - c
        prompt = (f"{tb.text}\n{_row(tb, x)}และ{_row(tb, y)}รวมกัน มากกว่า{_row(tb, z)}กี่{tb.table.unit}")
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(a + b, a - c, b - c, a + b + c, answer=right, lo=1))


@question_type("math.table_true_statement_p3", display_name={"th": "ตารางทางเดียว: ข้อความใดถูกต้อง"},
               level=LEVEL, topic="ตารางทางเดียว")
class TableTrueStatementP3(ChoiceType):
    def compose(self, rng: Random):
        tb = _story.one_way_table(rng)
        x, y = rng.sample(list(tb.data), 2)
        if tb.data[x] < tb.data[y]:
            x, y = y, x
        a, b, unit = tb.data[x], tb.data[y], tb.table.unit
        lx, ly = _row(tb, x), _row(tb, y)
        right = f"{lx}มากกว่า{ly} {a - b} {unit}"
        wrongs = [f"{ly}มากกว่า{lx} {a - b} {unit}", f"{lx}มากกว่า{ly} {a + b} {unit}",
                  f"{lx}มากกว่า{ly} {a - b + 10} {unit}"]
        return f"{tb.text}\nข้อความใดถูกต้อง", right, wrongs
