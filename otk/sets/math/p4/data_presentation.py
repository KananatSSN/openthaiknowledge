"""การนำเสนอข้อมูล

คณิตศาสตร์ · ป.4 · สสวท. พื้นฐาน
Indicators: ค 3.1 ป.4/1

Sets moved here from: math_p5.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_p2 import _maths, _texts
from otk.sets._support.math_p5 import LEVEL

PROVENANCE = Provenance("original")


NL = chr(10)       # a new stem line


_TW_TOPIC = "การนำเสนอข้อมูล"


_TWO_WAY = (
    ("จำนวนนักเรียนที่เลือกกิจกรรม", ("ชั้น ป.5/1", "ชั้น ป.5/2", "ชั้น ป.5/3"),
     ("ชาย", "หญิง"), "คน"),
    ("จำนวนหนังสือที่ห้องสมุดได้รับบริจาค", ("เดือนมกราคม", "เดือนกุมภาพันธ์", "เดือนมีนาคม"),
     ("นิทาน", "สารคดี"), "เล่ม"),
    ("จำนวนผลไม้ที่ร้านค้าขายได้", ("วันเสาร์", "วันอาทิตย์", "วันจันทร์"),
     ("มะม่วง", "ส้ม"), "ผล"),
)


def two_way_table(rng: Random):
    """``(text, rows, cols, cell dict, unit)`` — a ตารางสองทาง with totals left
    for the learner."""
    title, rows, cols, unit = rng.choice(_TWO_WAY)
    cells = {(r, c): rng.randint(8, 95) for r in rows for c in cols}
    lines = [f"ตารางแสดง{title}", "รายการ | " + " | ".join(cols)]
    lines += [f"{r} | " + " | ".join(str(cells[r, c]) for c in cols) for r in rows]
    return "\n".join(lines), rows, cols, cells, unit


@question_type("math.two_way_table_read_p5",
               display_name={"th": "อ่านตารางสองทาง"},
               level=LEVEL, topic=_TW_TOPIC)
class TwoWayTableReadP5(WordProblem):
    def expr(self, rng: Random):
        tt, rows, cols, cells, unit = two_way_table(rng)
        r, c = rng.choice(rows), rng.choice(cols)
        v = cells[r, c]
        other_c = [x for x in cols if x != c][0]
        wrongs = [cells[r, other_c]] + [cells[x, c] for x in rows if x != r]
        return MathDraw("", str(v), prompt=f"{tt}{NL}{r} {c} มีกี่{unit}",
                        distractors=_story.keep(*wrongs, answer=v))


@question_type("math.two_way_table_total_p5",
               display_name={"th": "ตารางสองทาง: ผลรวมตามแถวและตามหลัก"},
               level=LEVEL, topic=_TW_TOPIC)
class TwoWayTableTotalP5(WordProblem):
    def expr(self, rng: Random):
        tt, rows, cols, cells, unit = two_way_table(rng)
        if rng.random() < 0.5:
            r = rng.choice(rows)
            v = sum(cells[r, c] for c in cols)
            wrongs = [sum(cells[x, cols[0]] for x in rows), cells[r, cols[0]], v + 10]
            ask = f"{r} รวมทั้งหมดกี่{unit}"
        else:
            c = rng.choice(cols)
            v = sum(cells[r, c] for r in rows)
            wrongs = [sum(cells[rows[0], x] for x in cols), cells[rows[0], c], v + 10]
            ask = f"{c} รวมทุกแถวกี่{unit}"
        return MathDraw("", str(v), prompt=f"{tt}{NL}{ask}",
                        distractors=_story.keep(*wrongs, v - 10, answer=v, lo=1))


@question_type("math.two_way_table_compare_p5",
               display_name={"th": "ตารางสองทาง: เปรียบเทียบและหามากที่สุด"},
               level=LEVEL, topic=_TW_TOPIC)
class TwoWayTableCompareP5(QuestionType):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def build(self, rng: Random) -> GeneratedQuestion:
        tt, rows, cols, cells, unit = two_way_table(rng)
        if rng.random() < 0.5:
            totals = {r: sum(cells[r, c] for c in cols) for r in rows}
            if len(set(totals.values())) < len(totals):
                return self.build(rng)
            pick = max(totals, key=totals.get)
            # The row with the single largest cell, if it differs.
            lure = max(rows, key=lambda r: max(cells[r, c] for c in cols))
            wrongs = [lure] + [r for r in rows if r not in (pick, lure)] + ["เท่ากันทุกแถว"]
            return _texts([text(tt), text("แถวใดมีผลรวมมากที่สุด")], pick,
                          [w for w in dict.fromkeys(wrongs) if w != pick], self.topic)
        r = rng.choice(rows)
        a, b = cells[r, cols[0]], cells[r, cols[1]]
        v = abs(a - b)
        more, less = (cols[0], cols[1]) if a >= b else (cols[1], cols[0])
        if v == 0:
            return self.build(rng)
        return _maths([text(tt), text(f"{r} {more}มากกว่า{less}กี่{unit}")], str(v),
                      _story.keep(a + b, v + 10, v - 1, max(a, b), answer=v, lo=1), self.topic)
