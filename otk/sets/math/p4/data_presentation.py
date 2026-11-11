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


# ── More two-way tables (2026-11): the grand total, two column totals compared, the row with the largest
# total, two cells in a row compared, one column over two rows, a true statement, and a missing cell ──

from otk.core.registry import QuestionType, question_type  # noqa: E402
from otk.kit.math_problems import ChoiceType, WordProblem  # noqa: E402
from otk.sets._support.math_p4 import LEVEL  # noqa: E402


def _g(n: int) -> str:
    """A whole number in TeX with grouped thousands: 4{,}572{,}318."""
    return f"{n:,}".replace(",", "{,}")


def _gk(*values: int, answer: int, lo: int = 0, hi: int | None = None) -> list[str]:
    """``story.keep`` for grouped numbers."""
    return [_g(int(v)) for v in _story.keep(*values, answer=answer, lo=lo, hi=hi)]


@question_type("math.two_way_grand_total_p4", display_name={"th": "ตารางสองทาง: ผลรวมทั้งหมด"},
               level=LEVEL, topic="การนำเสนอข้อมูล")
class TwoWayGrandTotalP4(WordProblem):
    def expr(self, rng: Random):
        tt, rows, cols, cells, unit = two_way_table(rng)
        right = sum(cells.values())
        first_col = sum(cells[r, cols[0]] for r in rows)
        return MathDraw("", str(right), prompt=f"{tt}{NL}รวมทั้งตารางมีกี่{unit}",
                        distractors=_story.keep(first_col, right - cells[rows[0], cols[0]], right + 10, right - 10,
                                                answer=right, lo=1))


@question_type("math.two_way_column_diff_p4", display_name={"th": "ตารางสองทาง: ผลรวมของสองหลักต่างกันเท่าใด"},
               level=LEVEL, topic="การนำเสนอข้อมูล")
class TwoWayColumnDiffP4(WordProblem):
    def expr(self, rng: Random):
        while True:
            tt, rows, cols, cells, unit = two_way_table(rng)
            totals = {c: sum(cells[r, c] for r in rows) for c in cols}
            if totals[cols[0]] != totals[cols[1]]:
                break
        big, small = sorted(cols, key=totals.get, reverse=True)
        right = totals[big] - totals[small]
        prompt = f"{tt}{NL}{big}รวมทุกแถวมากกว่า{small}รวมทุกแถวกี่{unit}"
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(totals[big], abs(cells[rows[0], big] - cells[rows[0], small]),
                                                totals[big] + totals[small], right + 10, answer=right, lo=1))


@question_type("math.two_way_row_most_p4", display_name={"th": "ตารางสองทาง: แถวใดรวมมากที่สุด"},
               level=LEVEL, topic="การนำเสนอข้อมูล")
class TwoWayRowMostP4(ChoiceType):
    def compose(self, rng: Random):
        while True:
            tt, rows, cols, cells, unit = two_way_table(rng)
            totals = {r: sum(cells[r, c] for c in cols) for r in rows}
            if len(set(totals.values())) == len(rows):
                break
        most = rng.random() < 0.5
        right = (max if most else min)(totals, key=totals.get)
        return (f"{tt}{NL}รายการใดรวมทุกหลักแล้ว{'มากที่สุด' if most else 'น้อยที่สุด'}", right,
                [r for r in rows if r != right] + ["มีเท่ากันทุกรายการ"])


@question_type("math.two_way_cell_diff_p4", display_name={"th": "ตารางสองทาง: เปรียบเทียบสองช่องในแถวเดียวกัน"},
               level=LEVEL, topic="การนำเสนอข้อมูล")
class TwoWayCellDiffP4(WordProblem):
    def expr(self, rng: Random):
        while True:
            tt, rows, cols, cells, unit = two_way_table(rng)
            r = rng.choice(rows)
            if cells[r, cols[0]] != cells[r, cols[1]]:
                break
        big, small = sorted(cols, key=lambda c: cells[r, c], reverse=True)
        right = cells[r, big] - cells[r, small]
        prompt = f"{tt}{NL}ใน{r} {big}มากกว่า{small}กี่{unit}"
        other = [x for x in rows if x != r][0]
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(cells[r, big] + cells[r, small], abs(cells[other, big] - cells[other, small]),
                                                cells[r, big], right + 1, answer=right, lo=1))


@question_type("math.two_way_two_rows_p4", display_name={"th": "ตารางสองทาง: หลักเดียวกันสองแถวรวมกัน"},
               level=LEVEL, topic="การนำเสนอข้อมูล")
class TwoWayTwoRowsP4(WordProblem):
    def expr(self, rng: Random):
        tt, rows, cols, cells, unit = two_way_table(rng)
        x, y = rng.sample(rows, 2)
        c = rng.choice(cols)
        other = [k for k in cols if k != c][0]
        right = cells[x, c] + cells[y, c]
        prompt = f"{tt}{NL}{c}ของ{x}และ{y}รวมกันกี่{unit}"
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(cells[x, other] + cells[y, other], cells[x, c] + cells[x, other],
                                                abs(cells[x, c] - cells[y, c]), right + 10, answer=right, lo=1))


@question_type("math.two_way_true_statement_p4", display_name={"th": "ตารางสองทาง: ข้อความใดถูกต้อง"},
               level=LEVEL, topic="การนำเสนอข้อมูล")
class TwoWayTrueStatementP4(ChoiceType):
    def compose(self, rng: Random):
        tt, rows, cols, cells, unit = two_way_table(rng)
        r = rng.choice(rows)
        c = rng.choice(cols)
        other = [k for k in cols if k != c][0]
        v = cells[r, c]
        total = v + cells[r, other]
        right = f"{r}มี{c} {v} {unit} และรวมทั้งหมด {total} {unit}"
        # The other column's cell; a wrong total; the other row's cell.
        nxt = [x for x in rows if x != r][0]
        wrongs = [f"{r}มี{c} {cells[r, other]} {unit} และรวมทั้งหมด {total} {unit}",
                  f"{r}มี{c} {v} {unit} และรวมทั้งหมด {total + 10} {unit}",
                  f"{r}มี{c} {cells[nxt, c]} {unit} และรวมทั้งหมด {total} {unit}"]
        return f"{tt}{NL}ข้อความใดถูกต้อง", right, [w for w in dict.fromkeys(wrongs) if w != right] + \
            [f"{r}มี{c} {v + 1} {unit} และรวมทั้งหมด {total + 1} {unit}"]


@question_type("math.two_way_missing_cell_p4", display_name={"th": "ตารางสองทาง: หาค่าที่หายไปจากผลรวม"},
               level=LEVEL, topic="การนำเสนอข้อมูล")
class TwoWayMissingCellP4(WordProblem):
    def expr(self, rng: Random):
        tt, rows, cols, cells, unit = two_way_table(rng)
        r = rng.choice(rows)
        c = rng.choice(cols)
        other = [k for k in cols if k != c][0]
        total = cells[r, c] + cells[r, other]
        line = f"{r} | " + " | ".join(str(cells[r, k]) for k in cols)
        hidden = f"{r} | " + " | ".join("?" if k == c else str(cells[r, k]) for k in cols)
        tt = tt.replace(line, hidden)
        right = cells[r, c]
        prompt = f"{tt}{NL}ถ้า{r}รวมทั้งหมด {total} {unit} ช่อง ? คือกี่{unit}"
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(total + cells[r, other], cells[r, other], total, right + 10,
                                                answer=right, lo=1))
