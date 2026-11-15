"""การวัด

คณิตศาสตร์ · ป.1 · สสวท. พื้นฐาน
Indicators: ค 2.1 ป.1/*

Sets moved here from: math, math_measure_pictures, math_number, math_p1.
"""

from __future__ import annotations

from random import Random

from otk.core.content import image, text
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit import story as _story
from otk.kit.math_problems import ChoiceType, MathDraw, WordProblem, _no_carry_sum
from otk.sets._support.math_diagrams import _math_q
from otk.sets._support.math_measure_pictures import RULERS
from otk.sets._support.math_p1 import LEVEL
from otk.sets._support.math_pictures import _near

PROVENANCE = Provenance("original")


# (unit, its counter word, things short enough to measure with it)
_NONSTANDARD = (
    ("คลิปหนีบกระดาษ", "อัน", ("ดินสอ", "ไม้บรรทัด", "สมุด", "กล่องดินสอ")),
    ("ไม้ขีดไฟ", "ก้าน", ("ดินสอ", "ปากกา", "หนังสือนิทาน", "ช้อน")),
    ("ลูกบาศก์ไม้", "ลูก", ("ดินสอ", "กล่องนม", "สมุด", "ไม้บรรทัด")),
    ("คืบ", "คืบ", ("โต๊ะ", "ประตู", "กระดานดำ", "เตียง")),
    ("ก้าว", "ก้าว", ("ห้องเรียน", "สนามเด็กเล่น", "ทางเดิน", "ห้องสมุด")),
)


# Pairs that sit on the two pans of a balance, and what they are weighed in.
_WEIGH_PAIRS = (("แอปเปิล", "ส้ม"), ("มะม่วง", "ฝรั่ง"), ("หนังสือ", "กล่องดินสอ"),
                ("ลูกบอล", "ตุ๊กตา"), ("กล้วย", "มังคุด"), ("แก้วน้ำ", "ถ้วยกาแฟ"))


_WEIGH_UNITS = (("ลูกแก้ว", "ลูก"), ("ลูกบาศก์ไม้", "ลูก"), ("เหรียญ", "เหรียญ"),
                ("ยางลบ", "ก้อน"))


RULER_ALT = "ภาพดินสอวางบนไม้บรรทัดที่มีหน่วยเป็นเซนติเมตร"


# (measuring unit, its counter word). The things being measured are chosen from
# a separate list, so the unit is never also the object — "ดินสอยาว 5 ดินสอ".
_UNITS = [("คลิปหนีบกระดาษ", "คลิป"), ("ไม้ขีดไฟ", "ก้าน"),
          ("ลูกบาศก์ไม้", "ลูก"), ("ฝาขวดน้ำ", "ฝา")]


_MEASURED = ["ดินสอ", "ยางลบ", "สมุด", "กล่องนม", "ไม้บรรทัด"]


_MEASURED_math_p1 = ("ดินสอ", "ยางลบ", "ไม้บรรทัด", "ปากกา", "ช้อน", "หลอดดูด", "ใบไม้")


_WEIGHED = (("แตงโม", "ผล"), ("ฟักทอง", "ผล"), ("ถุงข้าวสาร", "ถุง"),
            ("ถุงน้ำตาล", "ถุง"), ("สับปะรด", "ผล"), ("กระเป๋านักเรียน", "ใบ"))


@question_type("math.count_units_nonstandard",
               display_name={"th": "นับหน่วยที่ไม่ใช่มาตรฐาน"}, level={"th": "ป.1"}, topic="การวัด")
class CountUnitsNonstandard(WordProblem):
    def expr(self, rng: Random):
        unit, cl, things = rng.choice(_NONSTANDARD)
        x, y = rng.sample(things, 2)
        k = rng.randint(2, 12)
        d = rng.randint(1, 6)
        # คืบ and ก้าว are their own counters: "ยาว 12 คืบ", not "ยาวเท่ากับคืบ 12 คืบ".
        by = "" if unit == cl else f"เท่ากับ{unit}"
        if rng.random() < 0.6:
            return MathDraw(
                "", rf"{d}",
                prompt=(f"{x}ยาว{by} {k} {cl} {y}ยาว{by} {k + d} {cl} "
                        f"{y}ยาวกว่า{x}กี่{cl}"),
                distractors=_story.keep(2 * k + d, d + 1, k, answer=d, lo=1))
        return MathDraw(
            "", rf"{2 * k + d}",
            prompt=(f"{x}ยาว{by} {k} {cl} {y}ยาว{by} {k + d} {cl} "
                    f"ถ้านำมาวางต่อกัน จะยาว{by}กี่{cl}"),
            distractors=_story.keep(d, 2 * k + d + 1, k + d, answer=2 * k + d))


@question_type("math.compare_nonstandard_length",
               display_name={"th": "เปรียบเทียบความยาว (หน่วยไม่มาตรฐาน)"},
               level={"th": "ป.1"}, topic="การวัด")
class CompareNonstandardLength(WordProblem):
    def expr(self, rng: Random, lo: int = 3, hi: int = 15):
        unit, counter = rng.choice(_UNITS)
        first, second = rng.sample(_MEASURED, 2)
        a, b = rng.sample(range(lo, hi), 2)
        return MathDraw(
            "", str(abs(a - b)),
            prompt=(f"{first}ยาว {a} {unit} {second}ยาว {b} {unit} "
                    f"ของสองสิ่งนี้ยาวต่างกันกี่{counter}"),
            distractors=[str(a + b), str(max(a, b)), str(min(a, b))])


@question_type("math.compare_nonstandard_weight",
               display_name={"th": "เปรียบเทียบน้ำหนัก (หน่วยไม่มาตรฐาน)"}, level={"th": "ป.1"}, topic="การวัด")
class CompareNonstandardWeight(ChoiceType):
    def compose(self, rng: Random):
        x, y = rng.choice(_WEIGH_PAIRS)
        unit, cl = rng.choice(_WEIGH_UNITS)
        a, b = rng.sample(range(2, 16), 2)
        if rng.random() < 0.15:
            b = a
        heavy = rng.random() < 0.5
        if a == b:
            answer = "หนักเท่ากัน"
        else:
            answer = x if (a > b) == heavy else y
        by = "" if unit == cl else unit
        stem = (f"{x}หนักเท่ากับ{by} {a} {cl} {y}หนักเท่ากับ{by} {b} {cl} "
                f"สิ่งใด{'หนักกว่า' if heavy else 'เบากว่า'}")
        return stem, answer, [x, y, "หนักเท่ากัน"]


@question_type("math.ruler_picture_p1", display_name={"th": "วัดความยาวด้วยไม้บรรทัดจากภาพ"},
               level={"th": "ป.1"}, topic="การวัด")
class RulerPictureP1(QuestionType):
    invent_numbers = True  # computed answer: near values on the short side cannot be right
    def build(self, rng: Random) -> GeneratedQuestion:
        r = rng.choice(RULERS)
        end = r.start + r.length
        # Reading the number at the tip when the pencil does not start at 0.
        return _math_q([text("ดินสอยาวกี่เซนติเมตร"), image(r.asset_id, alt=RULER_ALT)],
                       str(r.length), _near(r.length, end, end + 1, r.length + 2, lo=1)
                       if r.start else _near(r.length, r.length + 1, r.length - 1, lo=1),
                       self.topic)


@question_type("math.length_cm_m_p1",
               display_name={"th": "วัดและเปรียบเทียบความยาว (เซนติเมตร เมตร)"},
               level=LEVEL, topic="การวัด")
class LengthCmMP1(WordProblem):
    def expr(self, rng: Random):
        thing = rng.choice(_MEASURED_math_p1)
        kind = rng.randrange(4)
        if kind == 0:
            # A ruler read from a mark other than 0: the answer is the gap, and
            # the end mark is the mistake.
            start = rng.randint(1, 8)
            length = rng.randint(3, 15)
            end = start + length
            return MathDraw("", str(length),
                            prompt=(f"วาง{thing}บนไม้บรรทัด ปลายด้านหนึ่งอยู่ที่ขีด {start} "
                                    f"อีกด้านหนึ่งอยู่ที่ขีด {end} {thing}ยาวกี่เซนติเมตร"),
                            distractors=_story.keep(end, start + end, length + 1,
                                                    answer=length))
        if kind == 1:
            a, b = sorted(rng.sample(range(5, 40), 2), reverse=True)
            other = rng.choice([m for m in _MEASURED_math_p1 if m != thing])
            return MathDraw("", str(a - b),
                            prompt=(f"{thing}ยาว {a} เซนติเมตร {other}ยาว {b} เซนติเมตร "
                                    f"{thing}ยาวกว่า{other}กี่เซนติเมตร"),
                            distractors=_story.keep(a + b, a - b + 1, a, answer=a - b))
        if kind == 2:
            a, b = rng.randint(10, 45), rng.randint(10, 45)
            c1, c2 = rng.sample(_story.COLOURS, 2)
            return MathDraw("", str(a + b),
                            prompt=(f"ต่อเชือก{c1}ยาว {a} เซนติเมตร กับเชือก{c2}ยาว {b} "
                                    f"เซนติเมตร เป็นเส้นเดียวกัน จะยาวกี่เซนติเมตร"),
                            distractors=_story.keep(abs(a - b), _no_carry_sum(a, b),
                                                    a + b + 10, answer=a + b))
        tall = (("ต้นมะพร้าว", "ต้น"), ("เสาธง", "ต้น"), ("ตึก", "หลัง"),
                ("ต้นมะม่วง", "ต้น"), ("บ้าน", "หลัง"))
        (x, _), (y, _) = rng.sample(tall, 2)
        a, b = sorted(rng.sample(range(3, 30), 2), reverse=True)
        return MathDraw("", str(a - b),
                        prompt=f"{x}สูง {a} เมตร {y}สูง {b} เมตร {x}สูงกว่า{y}กี่เมตร",
                        distractors=_story.keep(a + b, a - b + 1, b, answer=a - b))


@question_type("math.weight_kg_khit_p1",
               display_name={"th": "ชั่งและเปรียบเทียบน้ำหนัก (กิโลกรัม ขีด)"},
               level=LEVEL, topic="การวัด")
class WeightKgKhitP1(WordProblem):
    def expr(self, rng: Random):
        (x, _), (y, _) = rng.sample(_WEIGHED, 2)
        unit = rng.choice(("กิโลกรัม", "ขีด"))
        a, b = sorted(rng.sample(range(2, 20), 2), reverse=True)
        kind = rng.randrange(3)
        if kind == 0:
            return MathDraw("", str(a + b),
                            prompt=f"{x}หนัก {a} {unit} {y}หนัก {b} {unit} รวมกันหนักกี่{unit}",
                            distractors=_story.keep(a - b, a + b + 1, a + b - 1, answer=a + b))
        if kind == 1:
            return MathDraw("", str(a - b),
                            prompt=f"{x}หนัก {a} {unit} {y}หนัก {b} {unit} "
                                   f"{x}หนักกว่า{y}กี่{unit}",
                            distractors=_story.keep(a + b, a - b + 1, a - b - 1, answer=a - b))
        # Weighing a basket: the reading minus the basket.
        return MathDraw("", str(a - b),
                        prompt=(f"ชั่ง{x}ใส่ตะกร้าได้ {a} {unit} ตะกร้าเปล่าหนัก {b} {unit} "
                                f"{x}หนักกี่{unit}"),
                        distractors=_story.keep(a + b, a, a - b + 1, answer=a - b))


# ── More measuring (2026-11): how much longer, two lengths joined, kilograms compared, and choosing the
# unit ──

from otk.kit.concept_bank import Concept, ConceptBankType  # noqa: E402

_LONG_THINGS = (("ดินสอ", "แท่ง"), ("ไม้บรรทัด", "อัน"), ("ยางลบ", "ก้อน"), ("ริบบิ้น", "เส้น"),
                ("เชือก", "เส้น"), ("หลอดดูดน้ำ", "หลอด"))
_HEAVY_THINGS = ("แตงโม", "ฟักทอง", "ถุงข้าวสาร", "ถุงส้ม", "กล่องหนังสือ", "สุนัข")


@question_type("math.length_difference_p1", display_name={"th": "ยาวกว่ากันกี่เซนติเมตร"},
               level=LEVEL, topic="การวัด")
class LengthDifferenceP1(WordProblem):
    def expr(self, rng: Random):
        (x, _), (y, _) = rng.sample(_LONG_THINGS, 2)
        a = rng.randint(8, 30)
        b = rng.randint(2, a - 2)
        right = a - b
        prompt = f"{x}ยาว {a} เซนติเมตร {y}ยาว {b} เซนติเมตร {x}ยาวกว่า{y}กี่เซนติเมตร"
        # Added instead; one of the lengths; one off.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(a + b, a, b, right + 1, answer=right, lo=1))


@question_type("math.join_lengths_p1", display_name={"th": "ต่อความยาวสองชิ้น"},
               level=LEVEL, topic="การวัด")
class JoinLengthsP1(WordProblem):
    def expr(self, rng: Random):
        unit = rng.choice(("เซนติเมตร", "เมตร"))
        a, b = rng.randint(3, 40), rng.randint(3, 40)
        right = a + b
        thing = rng.choice(("ริบบิ้น", "เชือก", "สายไฟ"))
        prompt = f"นำ{thing}ยาว {a} {unit} มาต่อกับ{thing}ยาว {b} {unit} จะได้{thing}ยาวกี่{unit}"
        # Subtracted; tens added without the ones carried; one off.
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(abs(a - b), _no_carry_sum(a, b), right + 1, right - 1,
                                                answer=right, lo=1))


@question_type("math.weight_compare_kg_p1", display_name={"th": "เปรียบเทียบน้ำหนักเป็นกิโลกรัม"},
               level=LEVEL, topic="การวัด")
class WeightCompareKgP1(WordProblem):
    def expr(self, rng: Random):
        x, y = rng.sample(_HEAVY_THINGS, 2)
        a = rng.randint(5, 20)
        b = rng.randint(1, a - 1)
        heavier = rng.random() < 0.5
        if heavier:
            right = a - b
            prompt = f"{x}หนัก {a} กิโลกรัม {y}หนัก {b} กิโลกรัม {x}หนักกว่า{y}กี่กิโลกรัม"
            wrong = a + b
        else:
            right = a + b
            prompt = f"{x}หนัก {a} กิโลกรัม {y}หนัก {b} กิโลกรัม รวมกันหนักกี่กิโลกรัม"
            wrong = a - b
        return MathDraw("", str(right), prompt=prompt,
                        distractors=_story.keep(wrong, a, right + 1, right - 1, answer=right, lo=1))


@question_type("math.choose_unit_p1", display_name={"th": "เลือกหน่วยวัดให้เหมาะสม"},
               level=LEVEL, topic="การวัด")
class ChooseUnitP1(ConceptBankType):
    ITEMS = [
        Concept("วัดความยาวของดินสอควรใช้หน่วยใด", "เซนติเมตร", ("เมตร", "กิโลกรัม", "ขีด")),
        Concept("วัดความยาวของห้องเรียนควรใช้หน่วยใด", "เมตร", ("เซนติเมตร", "กิโลกรัม", "ขีด")),
        Concept("ชั่งน้ำหนักของถุงข้าวสารควรใช้หน่วยใด", "กิโลกรัม", ("เมตร", "เซนติเมตร", "ลิตร")),
        Concept("ชั่งน้ำหนักของขนมหนึ่งถุงเล็ก ๆ ควรใช้หน่วยใด", "ขีด", ("เมตร", "เซนติเมตร", "กิโลกรัม")),
        Concept("วัดความสูงของต้นไม้ใหญ่ควรใช้หน่วยใด", "เมตร", ("เซนติเมตร", "ขีด", "กิโลกรัม")),
        Concept("วัดความยาวของยางลบควรใช้หน่วยใด", "เซนติเมตร", ("เมตร", "กิโลกรัม", "ขีด")),
        Concept("ชั่งน้ำหนักของตัวเราควรใช้หน่วยใด", "กิโลกรัม", ("ขีด", "เมตร", "เซนติเมตร")),
        Concept("วัดความยาวของสนามฟุตบอลควรใช้หน่วยใด", "เมตร", ("เซนติเมตร", "ขีด", "กิโลกรัม")),
    ]


@question_type("math.length_comparison_statement_p1", display_name={"th": "เลือกข้อความเปรียบเทียบความยาวที่ถูกต้อง"},
               level=LEVEL, topic="การวัด")
class LengthComparisonStatementP1(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=(
        "openthaiknowledge-bank/mathematics/level/primary-1/4017-1-2567-2-3.pdf, ตอนที่ 1 ข้อ 19",))

    def compose(self, rng: Random):
        a, b = rng.sample(range(5, 50), 2)
        longer, shorter = ("ริบบิ้นสีแดง", "ริบบิ้นสีฟ้า") if a > b else ("ริบบิ้นสีฟ้า", "ริบบิ้นสีแดง")
        gap = abs(a - b)
        return (f"ริบบิ้นสีแดงยาว {a} เซนติเมตร ริบบิ้นสีฟ้ายาว {b} เซนติเมตร ข้อใดถูกต้อง",
                f"{longer}ยาวกว่า{shorter} {gap} เซนติเมตร",
                # Reverse the subjects; sum instead of difference; mis-subtract one.
                [f"{shorter}ยาวกว่า{longer} {gap} เซนติเมตร",
                 f"{longer}ยาวกว่า{shorter} {a + b} เซนติเมตร",
                 f"{longer}ยาวกว่า{shorter} {gap + 1} เซนติเมตร"])


@question_type("math.measuring_tool_p1", display_name={"th": "เลือกเครื่องมือวัดความยาวให้เหมาะกับงาน"},
               level=LEVEL, topic="การวัด")
class MeasuringToolP1(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=(
        "openthaiknowledge-bank/mathematics/level/primary-1/4018-1-2567-2-2.pdf, ข้อ 5–6",))

    def compose(self, rng: Random):
        tools = ("ไม้บรรทัดแข็งยาว 30 เซนติเมตร", "ไม้เมตรแข็งยาว 100 เซนติเมตร",
                 "สายวัดผ้าอ่อนยาว 150 เซนติเมตร", "เครื่องชั่งน้ำหนัก")
        kind = rng.randrange(3)
        if kind == 2:
            obj = rng.choice(("รอบเอว", "รอบศีรษะ", "รอบแขน"))
            length = rng.randint(25, 80)
            stem = (f"ต้องการวัด{obj}ประมาณ {length} เซนติเมตร โดยให้เครื่องมือโค้งแนบตามรอบได้ "
                    "ควรใช้เครื่องมือใด")
        else:
            length = rng.randint(8, 28) if kind == 0 else rng.randint(40, 95)
            obj = rng.choice(("แถบกระดาษ", "แผ่นไม้", "ริบบิ้นที่วางเหยียดตรง"))
            stem = (f"ต้องการวัดความยาว{obj}ประมาณ {length} เซนติเมตร "
                    "โดยใช้เครื่องมือแข็งที่สั้นที่สุดที่ทาบครั้งเดียวได้ ควรใช้เครื่องมือใด")
        # Wrong tools fail the needed length, flexibility, or measured quantity.
        return stem, tools[kind], [tool for i, tool in enumerate(tools) if i != kind]


@question_type("math.weight_difference_pairs_p1", display_name={"th": "เปรียบเทียบผลต่างน้ำหนักต่างหน่วย"},
               level=LEVEL, topic="การวัด")
class WeightDifferencePairsP1(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=(
        "openthaiknowledge-bank/mathematics/level/primary-1/4018-1-2567-2-2.pdf, ข้อ 11",))

    def compose(self, rng: Random):
        # All four pairs have a distinct gap in ขีด. Bound the search space
        # directly rather than retrying a draw until one maximum exists.
        gaps = rng.sample(range(1, 10), 4)
        pairs = []
        for gap in gaps:
            kg = rng.randint(1, 4)
            khit = 10 * kg + rng.choice((-gap, gap))
            pairs.append((kg, khit))
        labels = [f"{kg} กิโลกรัม กับ {khit} ขีด" for kg, khit in pairs]
        right = max(range(4), key=lambda i: abs(10 * pairs[i][0] - pairs[i][1]))
        # The other actual pairs are distractors: compare the displayed
        # numerals without normalizing units, or rank weights instead of gaps.
        return ("กำหนดให้ 1 กิโลกรัม เท่ากับ 10 ขีด คู่ใดมีน้ำหนักต่างกันมากที่สุด",
                labels[right], [label for i, label in enumerate(labels) if i != right])


@question_type("math.scale_kg_khit_p1", display_name={"th": "อ่านขีดแบ่งบนเครื่องชั่ง"},
               level=LEVEL, topic="การวัด")
class ScaleKgKhitP1(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=(
        "openthaiknowledge-bank/mathematics/level/primary-1/4018-1-2567-2-2.pdf, ข้อ 7, 12",))

    def compose(self, rng: Random):
        kg, ticks = rng.randint(1, 5), rng.randint(1, 9)
        readings = [(kg, ticks), (kg, 10 - ticks), (kg + 1, ticks), (kg, ticks - 1), (kg, ticks + 1)]
        def label(k, t):
            k, t = k + t // 10, t % 10
            return f"{k} กิโลกรัม {t} ขีด"
        answer = label(kg, ticks)
        # Counting backwards, reading the next kilogram, or being off by one
        # tick. Remove the complement collision at the midpoint (5 ขีด).
        wrong = list(dict.fromkeys(label(k, t) for k, t in readings if label(k, t) != answer))
        return (f"เครื่องชั่งแบ่งช่วงระหว่างเลขกิโลกรัมติดกันเป็น 10 ช่วงเท่ากัน ช่วงละ 1 ขีด "
                f"เข็มอยู่เลยขีด {kg} กิโลกรัม ไปทาง {kg + 1} กิโลกรัม {ticks} ช่วงเล็ก "
                "อ่านน้ำหนักได้เท่าไร", answer, wrong)


@question_type("math.closest_weight_pair_p1", display_name={"th": "เลือกคู่น้ำหนักที่ใกล้เคียงกันที่สุด"},
               level=LEVEL, topic="การวัด")
class ClosestWeightPairP1(ChoiceType):
    PROVENANCE = Provenance("adapted", sources=(
        "openthaiknowledge-bank/mathematics/level/primary-1/4006-1-2565-2-2.pdf, ข้อ 11",))

    def compose(self, rng: Random):
        gaps = rng.sample(range(1, 10), 4)
        pairs = []
        for gap in gaps:
            kg = rng.randint(1, 4)
            khit = kg * 10 + rng.choice((-gap, gap))
            pairs.append((kg, khit))
        right = min(range(4), key=lambda i: abs(10 * pairs[i][0] - pairs[i][1]))
        labels = [f"{kg} กิโลกรัม กับ {khit} ขีด" for kg, khit in pairs]
        # Other real pairs represent ranking the raw numerals or choosing the
        # largest gap instead of the smallest after normalizing units.
        return ("กำหนดให้ 1 กิโลกรัม เท่ากับ 10 ขีด คู่ใดมีน้ำหนักใกล้เคียงกันมากที่สุด",
                labels[right], [label for i, label in enumerate(labels) if i != right])
