"""การนำเสนอข้อมูล

คณิตศาสตร์ · ป.5 · สสวท. พื้นฐาน
Indicators: ค 3.1 ป.5/1, ค 3.1 ป.5/2

Sets moved here from: math, math_diagrams, math_gaps_shape_data.
"""

from __future__ import annotations

from random import Random

from otk.core.content import math as content_math
from otk.core.content import text
from otk.core.distractors import fixed
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, WordProblem
from otk.sets._support.math_diagrams import LINE_GRAPHS, _img, _math_q, _nums
from otk.sets._support.math_gaps_shape_data import _TALLY, _choices, _table

PROVENANCE = Provenance("original")


LINE_ALT = "กราฟเส้นที่มีจุดข้อมูลหกจุด แกนนอนเป็นลำดับที่ 1 ถึง 6 บนเส้นตาราง"


@question_type("math.line_graph_picture_p5", display_name={"th": "อ่านกราฟเส้น (รูป)"},
               level={"th": "ป.5"}, topic="การนำเสนอข้อมูล")
class LineGraphPictureP5(QuestionType):
    _SERIES = (("ความสูงของต้นถั่ว", "สัปดาห์ที่", "เซนติเมตร"),
               ("จำนวนผู้เข้าชมห้องสมุด", "วันที่", "คน"),
               ("อุณหภูมิของน้ำในการทดลอง", "นาทีที่", "องศาเซลเซียส"),
               ("ยอดขายขนมของร้านค้า", "เดือนที่", "ชิ้น"))

    def build(self, rng: Random) -> GeneratedQuestion:
        g = rng.choice(LINE_GRAPHS)
        title, xname, unit = rng.choice(self._SERIES)
        head = text(f"กราฟเส้นแสดง{title} แกนนอนเป็น{xname} 1 ถึง 6 แกนตั้งมีหน่วยเป็น{unit}")
        img = _img(g.asset_id, LINE_ALT)
        v = g.values
        kind = rng.randrange(3)
        if kind == 0:
            i = rng.randrange(6)
            ans = v[i]
            wrongs = _nums(*(x for x in v if x != ans), ans + g.step, answer=ans)
            ask = f"{xname} {i + 1} มีค่าเท่าใด"
        elif kind == 1:
            i, j = sorted(rng.sample(range(6), 2))
            if v[i] == v[j]:
                return self.build(rng)
            ans = abs(v[j] - v[i])
            way = "เพิ่มขึ้น" if v[j] > v[i] else "ลดลง"
            ask = f"จาก{xname} {i + 1} ถึง{xname} {j + 1} {way}กี่{unit}"
            wrongs = _nums(v[i] + v[j], ans + g.step, max(v) - min(v), ans - g.step, 2 * ans,
                           answer=ans, lo=1)
        else:
            top = max(v)
            if v.count(top) > 1:
                return self.build(rng)
            ans = v.index(top) + 1
            ask = f"{xname}ใดมีค่ามากที่สุด"
            wrongs = _nums(top, v.index(min(v)) + 1, ans % 6 + 1, answer=ans, lo=1)
        return _math_q([head, img, text(ask)], str(ans), wrongs, self.topic)


@question_type("math.line_graph_change",
               display_name={"th": "อ่านกราฟเส้น (การเปลี่ยนแปลง)"}, level={"th": "ป.5"},
               topic="การนำเสนอข้อมูล")
class LineGraphChange(WordProblem):
    _SERIES = (("อุณหภูมิตอนเที่ยงของแต่ละวัน", ("จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์"),
                "องศาเซลเซียส", (24, 40)),
               ("ความสูงของต้นถั่ว", ("สัปดาห์ที่ 1", "สัปดาห์ที่ 2", "สัปดาห์ที่ 3",
                                     "สัปดาห์ที่ 4", "สัปดาห์ที่ 5"), "เซนติเมตร", (2, 60)),
               ("จำนวนผู้เข้าชมงาน", ("ปี 2564", "ปี 2565", "ปี 2566", "ปี 2567", "ปี 2568"),
                "คน", (100, 900)))

    def expr(self, rng: Random):
        title, points, unit, (lo, hi) = rng.choice(self._SERIES)
        values = rng.sample(range(lo, hi + 1), len(points))
        i, j = sorted(rng.sample(range(len(points)), 2))
        rows = "\n".join(f"{x}: {v}" for x, v in zip(points, values))
        change = abs(values[j] - values[i])
        way = "เพิ่มขึ้น" if values[j] > values[i] else "ลดลง"
        return MathDraw(
            "", str(change),
            prompt=(f"กราฟเส้นแสดง{title} อ่านค่าจากกราฟได้ดังนี้\n{rows}\n"
                    f"จาก{points[i]}ถึง{points[j]} {way}กี่{unit}"),
            distractors=_story.keep(values[i] + values[j], change + 1, max(values) - min(values),
                                    change - 1, answer=change, lo=1))


@question_type("math.bar_chart_make_p5", display_name={"th": "เขียนแผนภูมิแท่งจากข้อมูล"},
               level={"th": "ป.5"}, topic="การนำเสนอข้อมูล")
class BarChartMakeP5(QuestionType):
    def build(self, rng: Random, **params) -> GeneratedQuestion:
        title, rows, unit = rng.choice(_TALLY)
        scale = rng.choice((5, 10, 20, 50))
        counts = [scale * rng.randint(2, 12) for _ in rows]
        i = rng.randrange(len(rows))
        table = _table(title, rows, counts, unit)
        if rng.random() < 0.5:
            right = counts[i] // scale
            stem = [text(f"{table}\nถ้าเขียนแผนภูมิแท่ง โดยให้ความยาว 1 ช่องแทน {scale} {unit} "
                         f"แท่งของ{rows[i]} ต้องยาวกี่ช่อง")]
            wrongs = _story.keep(counts[i], right * 2, right + 1, answer=right, lo=1)
            return GeneratedQuestion(stem=stem, correct=[content_math(str(right))],
                                     distractors=fixed(*[[content_math(w)] for w in wrongs]),
                                     topic=self.topic)
        # Choosing a scale: the only one of the offered scales that makes the
        # longest bar 10 to 20 squares. Data with two such scales is redrawn.
        top = max(counts)
        scales = (1, 2, 5, 10, 20, 50, 100, 200)
        ok = [s for s in scales if 10 <= -(-top // s) <= 20]
        if len(ok) != 1:
            return self.build(rng, **params)
        right_scale = ok[0]
        wrong_scales = [s for s in scales if s != right_scale]
        rng.shuffle(wrong_scales)
        stem = [text(f"{table}\nกระดาษกราฟมีช่องตามแนวยาว 20 ช่อง ถ้าต้องการให้แท่งที่ยาวที่สุด"
                     f"ยาวอย่างน้อย 10 ช่องแต่ไม่เกิน 20 ช่อง ควรให้ 1 ช่องแทนกี่{unit}")]
        return _choices(stem, f"{right_scale} {unit}", [f"{s} {unit}" for s in wrong_scales], self.topic)


@question_type("math.line_graph_problem_p5", display_name={"th": "ใช้ข้อมูลจากกราฟเส้นแก้โจทย์ปัญหา"},
               level={"th": "ป.5"}, topic="การนำเสนอข้อมูล")
class LineGraphProblemP5(QuestionType):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    _SERIES = (
        ("ความสูงของต้นถั่ว (เซนติเมตร) ในแต่ละสัปดาห์", ("สัปดาห์ที่ 1", "สัปดาห์ที่ 2", "สัปดาห์ที่ 3",
                                                          "สัปดาห์ที่ 4", "สัปดาห์ที่ 5"), "เซนติเมตร", True),
        ("จำนวนผู้เข้าชมห้องสมุด (คน) ในแต่ละวัน", ("จันทร์", "อังคาร", "พุธ", "พฤหัสบดี", "ศุกร์"), "คน", False),
        ("ยอดขายไอศกรีม (ถ้วย) ในแต่ละเดือน", ("มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม"), "ถ้วย", False),
    )

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        title, xs, unit, rising = rng.choice(self._SERIES)
        while True:
            if rising:
                ys = [rng.randint(2, 6)]
                for _ in xs[1:]:
                    ys.append(ys[-1] + rng.randint(1, 8))
            else:
                ys = [rng.randint(20, 90) for _ in xs]
            steps = [b - a for a, b in zip(ys, ys[1:])]
            if len(set(steps)) == len(steps) and max(steps) > 0:
                break
        data = f"กราฟเส้นแสดง{title} อ่านค่าจากกราฟได้ดังนี้\n" + "\n".join(
            f"{x}: {y}" for x, y in zip(xs, ys))
        # A total only means something for counts; a height is not summed.
        kind = rng.randrange(3) if not rising else rng.choice((0, 2))
        if kind == 0:
            k = max(range(len(steps)), key=lambda i: steps[i])
            right = f"จาก{xs[k]}ถึง{xs[k + 1]}"
            wrongs = [f"จาก{xs[i]}ถึง{xs[i + 1]}" for i in range(len(steps)) if i != k]
            # The largest value, taken for the largest rise, is the usual slip.
            return _choices([text(f"{data}\nช่วงใดเพิ่มขึ้นมากที่สุด")], right, wrongs, self.topic)
        if kind == 1:
            total = sum(ys)
            wrongs = _story.keep(max(ys) * len(ys), total - ys[0], total + ys[-1], answer=total, lo=1)
            stem = [text(f"{data}\nรวมทั้ง {len(xs)} ช่วง มีทั้งหมดกี่{unit}")]
            return GeneratedQuestion(stem=stem, correct=[content_math(str(total))],
                                     distractors=fixed(*[[content_math(w)] for w in wrongs]),
                                     topic=self.topic)
        spread = max(ys) - min(ys)
        wrongs = _story.keep(max(ys), max(ys) + min(ys), abs(ys[-1] - ys[0]),
                             spread + 1, spread - 1, answer=spread, lo=1)[:3]
        stem = [text(f"{data}\nค่าที่มากที่สุดมากกว่าค่าที่น้อยที่สุดอยู่กี่{unit}")]
        return GeneratedQuestion(stem=stem, correct=[content_math(str(spread))],
                                 distractors=fixed(*[[content_math(w)] for w in wrongs]),
                                 topic=self.topic)
