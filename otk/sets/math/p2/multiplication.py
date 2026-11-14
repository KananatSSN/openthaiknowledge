"""การคูณ

คณิตศาสตร์ · ป.2 · สสวท. พื้นฐาน
Indicators: ค 1.1 ป.2/5

Sets moved here from: math, math_p2, math_pictures_p2.
"""

from __future__ import annotations

from random import Random

from otk.core.content import text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import MathDraw, MathType, WordProblem
from otk.sets._support.math_diagrams import _math_q
from otk.sets._support.math_p2 import _LEGS, LEVEL
from otk.sets._support.math_pictures import BY_KEY, _img, _near
from otk.sets._support.math_pictures_p2 import ARRAYS, GROUPS, P2

PROVENANCE = Provenance("original")


_WHEELS = (("รถจักรยาน", 2), ("รถสามล้อ", 3), ("รถยนต์", 4))


def _groups_story(rng: Random, groups: int, each: int) -> str:
    """``groups`` equal groups of ``each``: boxes, rows, legs, prices."""
    p = rng.choice(_story.NAMES)
    t = rng.choice(_story.THINGS)
    goods = rng.choice(("สมุด", "ดินสอ", "ขนม", "ยางลบ", "ปากกา", "ไอศกรีม"))
    animal, legs = rng.choice(_LEGS)
    vehicle, wheels = rng.choice(_WHEELS)
    stories = [
        f"มีกล่อง {groups} ใบ แต่ละใบใส่{t.noun}ไว้ {each} {t.cl} มี{t.noun}ทั้งหมดกี่{t.cl}",
        f"ครูจัดเก้าอี้ {groups} แถว แถวละ {each} ตัว มีเก้าอี้ทั้งหมดกี่ตัว",
        f"{p}ซื้อ{goods} {groups} ชิ้น ราคาชิ้นละ {each} บาท {p}ต้องจ่ายเงินกี่บาท",
        f"{p}ออมเงินวันละ {each} บาท เป็นเวลา {groups} วัน {p}ออมเงินได้กี่บาท",
        f"ชาวสวนปลูกต้นกล้วย {groups} แถว แถวละ {each} ต้น ปลูกต้นกล้วยทั้งหมดกี่ต้น",
    ]
    if each in (2, 4, 6, 8) and groups <= 30:
        a2 = next((a for a, n in _LEGS if n == each), animal)
        stories.append(f"{a2} {groups} ตัว มีขารวมกันกี่ขา")
    if each in (2, 3, 4):
        v2 = next(v for v, n in _WHEELS if n == each)
        stories.append(f"{v2} {groups} คัน มีล้อรวมกันกี่ล้อ")
    return rng.choice(stories)


@question_type("math.repeated_addition",
               display_name={"th": "การบวกซ้ำเป็นการคูณ"}, level={"th": "ป.2"},
               topic="การคูณ")
class RepeatedAddition(MathType):
    def expr(self, rng: Random, a_lo: int = 2, a_hi: int = 9):
        a = rng.randint(a_lo, a_hi)
        b = rng.randint(2, 6)
        return MathDraw(" + ".join([str(a)] * b), rf"{a * b}",
                        prompt="การบวกซ้ำนี้เท่ากับข้อใด",
                        distractors=[str(a * (b + 1)), str(a + b), str(a * (b - 1))])


@question_type("math.multiplication_picture_p2", display_name={"th": "การคูณจากภาพ"},
               level=P2, topic="การคูณ")
class MultiplicationPictureP2(QuestionType):
    def build(self, rng: Random) -> GeneratedQuestion:
        if rng.random() < 0.5:
            a = rng.choice(ARRAYS)
            kind, n, each, img = BY_KEY[a.kind], a.rows, a.cols, _img(a.asset_id, [a.kind])
            setup = f"{kind.thai}เรียงเป็นแถว แถวละเท่า ๆ กัน"
        else:
            g = rng.choice(GROUPS)
            kind, n, each, img = BY_KEY[g.kind], g.groups, g.size, _img(g.asset_id, [g.kind])
            setup = f"{kind.thai}อยู่ในจาน จานละเท่า ๆ กัน"
        total = n * each
        if rng.random() < 0.5:
            # Adding the two numbers instead of multiplying; one group short.
            return _math_q([text(f"{setup} มี{kind.thai}ทั้งหมดกี่{kind.unit}"), img],
                           str(total), _near(total, n + each, total - each, total + each, lo=1),
                           self.topic)
        correct = f"{n} \\times {each} = {total}"
        wrongs = [f"{n} + {each} = {n + each}", f"{n} \\times {each} = {total + each}",
                  f"{n} \\times {each + 1} = {n * (each + 1)}"]
        return _math_q([text(f"{setup} ประโยคสัญลักษณ์ใดตรงกับภาพ"), img],
                       correct, wrongs, self.topic)


@question_type("math.multiply_1x2_p2",
               display_name={"th": "การคูณจำนวนหนึ่งหลักกับจำนวนสองหลัก"},
               level=LEVEL, topic="การคูณ")
class Multiply1x2P2(MathType):
    def expr(self, rng: Random, lo: int = 11, hi: int = 99):
        a = rng.randint(max(11, int(lo)), min(99, int(hi)))
        b = rng.randint(2, 9)
        tens, ones = divmod(a, 10)
        ans = a * b
        # Forgetting the carry from the ones, and multiplying only the tens.
        no_carry = tens * b * 10 + (ones * b) % 10
        return MathDraw(rf"{a} \times {b}" if rng.random() < 0.7 else rf"{b} \times {a}",
                        str(ans), prompt="จงหาผลคูณ",
                        distractors=_story.keep(no_carry, tens * b * 10 + ones, ans + 10,
                                                a + b, answer=ans))


@question_type("math.multiplication_properties_p2",
               display_name={"th": "สมบัติการคูณและตัวไม่ทราบค่าในประโยคการคูณ"},
               level=LEVEL, topic="การคูณ")
class MultiplicationPropertiesP2(MathType):
    def expr(self, rng: Random):
        a, b = rng.randint(2, 9), rng.randint(2, 12)
        sq = r"\square"
        kind = rng.randrange(5)
        if kind == 0:     # สลับที่
            return MathDraw(rf"{a} \times {b} = {b} \times {sq}", str(a),
                            prompt="จงหาจำนวนที่แทนใน □",
                            distractors=_story.keep(b, a * b, a + b, answer=a))
        if kind == 1:
            return MathDraw(rf"{sq} \times {a} = {a * b}", str(b),
                            prompt="จงหาจำนวนที่แทนใน □",
                            distractors=_story.keep(a * b - a, a * b + a, a, b + 1, answer=b))
        if kind == 2:
            return MathDraw(rf"{a} \times {sq} = {a * b}", str(b),
                            prompt="จงหาจำนวนที่แทนใน □",
                            distractors=_story.keep(a * b - a, a, b - 1, b + 1, answer=b))
        if kind == 3:     # คูณด้วยศูนย์
            n = rng.randint(10, 99)
            return MathDraw(rf"{n} \times 0", "0", prompt="จงหาผลคูณ",
                            distractors=_story.keep(n, 1, 10, answer=0))
        n = rng.randint(10, 99)
        return MathDraw(rf"{n} \times 1", str(n), prompt="จงหาผลคูณ",
                        distractors=_story.keep(n + 1, 1, 0, 10 * n, answer=n))


@question_type("math.multiplication_word_problem_p2",
               display_name={"th": "โจทย์ปัญหาการคูณ"},
               level=LEVEL, topic="การคูณ")
class MultiplicationWordProblemP2(WordProblem):
    def expr(self, rng: Random, hi: int = 30):
        groups = rng.randint(2, max(3, min(int(hi), 99)))
        each = rng.randint(2, 9)
        if groups > 9 and each > 9:
            each = rng.randint(2, 9)
        ans = groups * each
        return MathDraw("", str(ans), prompt=_groups_story(rng, groups, each),
                        distractors=_story.keep(groups + each, ans + each, ans - each,
                                                ans + 10, answer=ans, lo=1))


# ── More multiplying (2026-11): the times tables, by ten and a hundred, the largest product, rows and
# columns, and multiplying by 0 and 1 ──
from otk.core.registry import question_type  # noqa: E402
from otk.kit.math_problems import ChoiceType, MathType, WordProblem  # noqa: E402
from otk.sets._support.math_p2 import LEVEL  # noqa: E402


@question_type("math.times_table_p2", display_name={"th": "สูตรคูณแม่ 2 ถึงแม่ 9"},
               level=LEVEL, topic="การคูณ")
class TimesTableP2(MathType):
    def expr(self, rng: Random):
        a, b = rng.randint(2, 9), rng.randint(2, 9)
        right = a * b
        # The next row of the table; the row before; added instead.
        return MathDraw(rf"{a} \times {b}", str(right), prompt="จงหาผลคูณ",
                        distractors=_story.keep(a * (b + 1), a * (b - 1), a + b, (a + 1) * b, answer=right, lo=1))


@question_type("math.multiply_by_ten_p2", display_name={"th": "คูณด้วย 10 และ 100"},
               level=LEVEL, topic="การคูณ")
class MultiplyByTenP2(MathType):
    def expr(self, rng: Random):
        if rng.random() < 0.5:
            a, k = rng.randint(2, 99), 10
        else:
            a, k = rng.randint(2, 9), 100
        right = a * k
        # One zero too many or too few; the ten added.
        return MathDraw(rf"{a} \times {k}", str(right), prompt="จงหาผลคูณ",
                        distractors=_story.keep(right * 10, a * k // 10, a + k, right + k, answer=right, lo=1))


@question_type("math.largest_product_p2", display_name={"th": "ผลคูณใดมากที่สุดหรือน้อยที่สุด"},
               level=LEVEL, topic="การคูณ")
class LargestProductP2(ChoiceType):
    def compose(self, rng: Random):
        while True:
            exprs = {}
            for _ in range(4):
                a, b = rng.randint(2, 9), rng.randint(2, 9)
                exprs[f"{a} × {b}"] = a * b
            if len(exprs) == 4 and len(set(exprs.values())) == 4:
                break
        most = rng.random() < 0.5
        right = (max if most else min)(exprs, key=exprs.get)
        return f"ข้อใดมีผลคูณ{'มากที่สุด' if most else 'น้อยที่สุด'}", right, [e for e in exprs if e != right]


@question_type("math.array_rows_p2", display_name={"th": "โจทย์ปัญหาการคูณ: จัดเป็นแถว"},
               level=LEVEL, topic="การคูณ")
class ArrayRowsP2(WordProblem):
    def expr(self, rng: Random):
        rows, cols = rng.randint(2, 9), rng.randint(3, 9)
        what, unit, verb = rng.choice((("ต้นมะม่วง", "ต้น", "ปลูก"), ("เก้าอี้", "ตัว", "จัด"),
                                       ("นักเรียน", "คน", "ให้ยืนเข้าแถว"), ("กระถางดอกไม้", "กระถาง", "วาง")))
        right = rows * cols
        prompt = f"{verb}{what} {rows} แถว แถวละ {cols} {unit} มี{what}ทั้งหมดกี่{unit}"
        # Added instead; one row more or fewer.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(rows + cols, (rows + 1) * cols, (rows - 1) * cols, right + 1,
                                                answer=right, lo=1))


@question_type("math.multiply_zero_one_p2", display_name={"th": "การคูณด้วย 0 และ 1"},
               level=LEVEL, topic="การคูณ")
class MultiplyZeroOneP2(MathType):
    def expr(self, rng: Random):
        a = rng.randint(2, 99)
        k = rng.choice((0, 1))
        tex = rf"{a} \times {k}" if rng.random() < 0.5 else rf"{k} \times {a}"
        right = a * k
        # The other rule; the number plus one; one.
        return MathDraw(tex, str(right), prompt="จงหาผลคูณ",
                        distractors=_story.keep(a if k == 0 else 0, a + 1, 1, 10 * a, answer=right, lo=0))
