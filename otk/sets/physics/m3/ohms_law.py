"""กฎของโอห์ม

ฟิสิกส์ · ม.3 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.3/1, ว 2.3 ม.3/3

Sets moved here from: electricity, science_pilots.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.content import text
from otk.core.distractors import label_pool
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.classify import Category, ClassifyType
from otk.kit.concept_bank import Concept, ConceptBankType
from otk.kit.numeric_scenario import Calc, PhysCalc, fmt, slips
from otk.sets._support.electricity import LEVEL, SUBJECT, TOPIC

PROVENANCE = Provenance("original")


PHYSICS = "ฟิสิกส์"


ELECTRICITY = "ไฟฟ้า"


class OhmsMeasurement(NamedTuple):
    voltage: int
    current: int


OHM_EQUATION_TASKS = (
    ("ทราบความต่างศักย์และความต้านทาน ต้องการหากระแสไฟฟ้า", "I = V / R",
     ("I = V × R", "I = R / V", "I = V − R")),
    ("ทราบกระแสไฟฟ้าและความต้านทาน ต้องการหาความต่างศักย์", "V = I × R",
     ("V = I / R", "V = R / I", "V = I + R")),
    ("ทราบความต่างศักย์และกระแสไฟฟ้า ต้องการหาความต้านทาน", "R = V / I",
     ("R = V × I", "R = I / V", "R = V + I")),
)


OHM_UNITS = ("โอห์ม (Ω)", "โวลต์ (V)", "แอมแปร์ (A)")


OHM_UNIT_QUANTITIES = ("ความต้านทาน", "ความต่างศักย์", "กระแสไฟฟ้า")


OHM_QUANTITY_NAMES = ("ความต้านทาน", "ความต่างศักย์", "กระแสไฟฟ้า", "กำลังไฟฟ้า")


OHM_INSTRUMENTS = (
    ("กระแสไฟฟ้าที่ผ่านตัวต้านทาน", "แอมมิเตอร์ ต่อแบบอนุกรมกับตัวต้านทาน"),
    ("ความต่างศักย์คร่อมตัวต้านทาน", "โวลต์มิเตอร์ ต่อแบบขนานกับตัวต้านทาน"),
)


OHM_SYMBOLS = (
    ("V", "ความต่างศักย์", "โวลต์"),
    ("I", "กระแสไฟฟ้า", "แอมแปร์"),
    ("R", "ความต้านทาน", "โอห์ม"),
)


OHM_INSTRUMENT_WRONGS = (
    "แอมมิเตอร์ ต่อแบบขนานกับตัวต้านทาน",
    "โวลต์มิเตอร์ ต่อแบบอนุกรมกับตัวต้านทาน",
    "เทอร์มอมิเตอร์ ต่อแบบอนุกรมกับตัวต้านทาน",
)


# (V, I เดิม, I ใหม่) เลือกให้ผลต่างความต้านทานไม่ตรงกับความต้านทานค่าใดค่าหนึ่ง
OHM_DIMMER_CASES = (
    (60, 6, 4), (60, 10, 6), (60, 12, 5), (60, 5, 3),
    (60, 4, 3), (60, 6, 5), (60, 12, 10), (60, 10, 4), (60, 3, 2),
)


OHM_DEVICES = ("หลอดไฟในห้องเรียน", "พัดลมตั้งโต๊ะ", "เตารีดขนาดเล็ก", "หัวแร้งบัดกรี")


def _elec_question(
    *, stem: str, correct: str, wrongs: tuple[str, str, str], hint: str,
) -> GeneratedQuestion:
    return GeneratedQuestion(
        stem=[text(stem)],
        correct=[text(correct)],
        distractors=label_pool([correct, *wrongs]),
        topic=ELECTRICITY,
        hint=[text(hint)],
    )


def _ohm_table(rows: tuple[OhmsMeasurement, ...]) -> str:
    """One measurement per line, short enough to stay on one line at 375 px."""
    body = "\n".join(
        f"ครั้งที่ {index}: {row.voltage} V, {row.current} A"
        for index, row in enumerate(rows, start=1)
    )
    return "(ความต่างศักย์, กระแสไฟฟ้า)\n" + body


@question_type("elec.quantities",
               display_name={"th": "ปริมาณไฟฟ้า: ความต่างศักย์ กระแส และความต้านทาน"},
               level=LEVEL, subject=SUBJECT, topic=TOPIC)
class Quantities(ClassifyType):
    """โยงคำนิยาม หน่วย และเครื่องวัด เข้ากับปริมาณ V, I หรือ R ที่ถูกต้อง."""

    CLASSIFY_STEM = "“{member}” เป็นลักษณะของปริมาณไฟฟ้าใด"
    PICK_STEM = "ข้อใดเป็นลักษณะของ{category}"

    CATEGORIES = [
        Category("ความต่างศักย์ไฟฟ้า (V)",
                 ("มีหน่วยเป็นโวลต์ (V)",
                  "วัดได้ด้วยโวลต์มิเตอร์ที่ต่อคร่อมอุปกรณ์",
                  "พลังงานที่ใช้ในการเคลื่อนประจุไฟฟ้าหนึ่งหน่วยระหว่างจุดสองจุด",
                  "เป็นสิ่งที่ผลักดันให้ประจุไฟฟ้าเคลื่อนที่ไปตามวงจร")),
        Category("กระแสไฟฟ้า (I)",
                 ("มีหน่วยเป็นแอมแปร์ (A)",
                  "วัดได้ด้วยแอมมิเตอร์ที่ต่ออนุกรมเข้าไปในวงจร",
                  "ปริมาณประจุไฟฟ้าที่ผ่านตัวนำในหนึ่งหน่วยเวลา",
                  "เมื่อความต่างศักย์เท่ากัน ยิ่งมีค่ามาก เครื่องใช้ไฟฟ้ายิ่งใช้กำลังไฟฟ้ามาก")),
        Category("ความต้านทานไฟฟ้า (R)",
                 ("มีหน่วยเป็นโอห์ม (Ω)",
                  "สมบัติของตัวนำที่ต้านการไหลของกระแสไฟฟ้า",
                  "หาได้จากสภาพต้านทาน ความยาว และพื้นที่หน้าตัดของลวดตัวนำ",
                  "มีค่ามากขึ้นเมื่อนำลวดชนิดเดิมที่ยาวกว่ามาใช้แทน")),
    ]


@question_type("elec.units_symbols",
               display_name={"th": "หน่วยและสัญลักษณ์ทางไฟฟ้า"},
               level=LEVEL, subject=SUBJECT, topic=TOPIC)
class UnitsSymbols(ConceptBankType):
    """หน่วยของ ρ, L, A, P, W, Q และความหมายของตัวแปรในสูตร R = ρL/A."""

    ITEMS = [
        Concept("สภาพต้านทาน (ρ) ของวัสดุมีหน่วยเป็นอะไร",
                "โอห์ม·เมตร (Ω·m)",
                ("โอห์ม (Ω)", "โอห์มต่อเมตร (Ω/m)", "โอห์ม·ตารางเมตร (Ω·m²)")),
        Concept("พื้นที่หน้าตัด (A) ของลวดตัวนำมีหน่วยเป็นอะไร",
                "ตารางเมตร (m²)",
                ("เมตร (m)", "ลูกบาศก์เมตร (m³)", "โอห์ม·เมตร (Ω·m)")),
        Concept("กำลังไฟฟ้า (P) มีหน่วยเป็นอะไร",
                "วัตต์ (W)",
                ("จูล (J)", "โวลต์ (V)", "คูลอมบ์ (C)")),
        Concept("พลังงานไฟฟ้า (W) มีหน่วยเป็นอะไร",
                "จูล (J)",
                ("วัตต์ (W)", "คูลอมบ์ (C)", "โอห์ม (Ω)")),
        Concept("ประจุไฟฟ้า (Q) มีหน่วยเป็นอะไร",
                "คูลอมบ์ (C)",
                ("จูล (J)", "แอมแปร์ (A)", "โวลต์ (V)")),
        Concept("สัญลักษณ์ Ω ใช้แทนหน่วยของปริมาณใด",
                "ความต้านทานไฟฟ้า",
                ("ความต่างศักย์ไฟฟ้า", "กระแสไฟฟ้า", "กำลังไฟฟ้า")),
        Concept("ในสูตร R = ρL/A ตัว L หมายถึงอะไร",
                "ความยาวของลวดตัวนำ",
                ("พื้นที่หน้าตัดของลวดตัวนำ", "สภาพต้านทานของวัสดุ",
                 "ความต่างศักย์ที่ปลายลวดตัวนำ")),
        Concept("ในสูตร R = ρL/A ตัว ρ หมายถึงอะไร",
                "สภาพต้านทานของวัสดุที่ใช้ทำลวดตัวนำ",
                ("ความต้านทานรวมของวงจร", "ความหนาแน่นของลวดตัวนำ",
                 "ความยาวของลวดตัวนำ")),
        Concept("หนึ่งวัตต์·วินาที มีค่าเท่ากับข้อใด",
                "1 จูล",
                ("1 คูลอมบ์", "1 โวลต์", "60 จูล")),
        Concept("กระแสไฟฟ้า (I) มีหน่วยเป็นอะไร",
                "แอมแปร์ (A)",
                (
                 "โวลต์ (V)",
                 "โอห์ม (Ω)",
                 "คูลอมบ์ (C)",
                 "วัตต์ (W)",
                 "จูล (J)")),
        Concept("ความต่างศักย์ไฟฟ้า (V) มีหน่วยเป็นอะไร",
                "โวลต์ (V)",
                (
                 "แอมแปร์ (A)",
                 "โอห์ม (Ω)",
                 "วัตต์ (W)",
                 "จูล (J)",
                 "คูลอมบ์ (C)")),
        Concept("หน่วยกิโลวัตต์·ชั่วโมง (kWh) ใช้วัดปริมาณใด",
                "พลังงานไฟฟ้า",
                (
                 "กำลังไฟฟ้า",
                 "กระแสไฟฟ้า",
                 "ความต่างศักย์ไฟฟ้า",
                 "ความต้านทานไฟฟ้า",
                 "ประจุไฟฟ้า")),
        Concept("หนึ่งแอมแปร์มีค่าเท่ากับข้อใด",
                "1 คูลอมบ์ต่อวินาที",
                (
                 "1 จูลต่อวินาที",
                 "1 จูลต่อคูลอมบ์",
                 "1 คูลอมบ์·วินาที",
                 "1 วัตต์·วินาที",
                 "1 โอห์ม·เมตร")),
        Concept("หนึ่งโอห์มมีค่าเท่ากับข้อใด",
                "1 โวลต์ต่อแอมแปร์",
                (
                 "1 แอมแปร์ต่อโวลต์",
                 "1 วัตต์ต่อแอมแปร์",
                 "1 จูลต่อวินาที",
                 "1 คูลอมบ์ต่อวินาที",
                 "1 โวลต์·แอมแปร์")),
    ]


@question_type(
    "elec.ohms_law_foundation",
    display_name={"th": "กฎของโอห์ม: ระบุปริมาณและความสัมพันธ์"},
    level={"th": "ม.3"}, subject=PHYSICS, topic=ELECTRICITY,
)
class OhmsLawFoundation(QuestionType):
    """Name the quantity, unit, meter, or equation form for one relationship."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            k = rng.choice((2, 3, 4, 5))
            case = rng.choice(("v_up", "r_up", "i_up", "r_down"))
            words = {2: "สองเท่า", 3: "สามเท่า", 4: "สี่เท่า", 5: "ห้าเท่า"}
            part = {2: "ครึ่งหนึ่ง", 3: "หนึ่งในสาม", 4: "หนึ่งในสี่", 5: "หนึ่งในห้า"}
            if case == "v_up":
                stem = f"ตัวต้านทานมีความต้านทานคงที่ ถ้าเพิ่มความต่างศักย์คร่อมตัวต้านทานเป็น{words[k]} กระแสไฟฟ้าจะเป็นอย่างไร"
                correct, others = f"เพิ่มเป็น{words[k]}", (f"ลดลงเหลือ{part[k]}", "เท่าเดิม", f"เพิ่มเป็น{words[k]}ยกกำลังสอง")
            elif case == "r_up":
                stem = f"ความต่างศักย์คงที่ ถ้าเปลี่ยนตัวต้านทานให้มีความต้านทานเป็น{words[k]}ของเดิม กระแสไฟฟ้าจะเป็นอย่างไร"
                correct, others = f"ลดลงเหลือ{part[k]}", (f"เพิ่มเป็น{words[k]}", "เท่าเดิม", "ลดลงเป็นศูนย์")
            elif case == "r_down":
                stem = f"ความต่างศักย์คงที่ ถ้าเปลี่ยนตัวต้านทานให้มีความต้านทานลดลงเหลือ{part[k]}ของเดิม กระแสไฟฟ้าจะเป็นอย่างไร"
                correct, others = f"เพิ่มเป็น{words[k]}", (f"ลดลงเหลือ{part[k]}", "เท่าเดิม", "เพิ่มขึ้นเพียงเล็กน้อยโดยไม่ขึ้นกับความต้านทาน")
            else:
                stem = f"ตัวต้านทานมีความต้านทานคงที่ ถ้าต้องการให้กระแสไฟฟ้าเพิ่มเป็น{words[k]} ต้องทำอย่างไรกับความต่างศักย์"
                correct, others = f"เพิ่มความต่างศักย์เป็น{words[k]}", (f"ลดความต่างศักย์เหลือ{part[k]}", "คงความต่างศักย์ไว้เท่าเดิม",
                                                                      f"เพิ่มความต้านทานเป็น{words[k]}")
            return _elec_question(
                stem=stem, correct=correct, wrongs=others,
                hint="ใช้ V = IR: ถ้า R คงที่ I แปรผันตรงกับ V ถ้า V คงที่ I แปรผกผันกับ R",
            )
        which = rng.randrange(5)
        if which == 0:
            task, correct, wrongs = rng.choice(OHM_EQUATION_TASKS)
            return _elec_question(
                stem=f"{task} ควรใช้สมการรูปใดจากกฎของโอห์ม",
                correct=correct,
                wrongs=wrongs,
                hint="เริ่มจาก V = IR แล้วย้ายข้างเพียงขั้นตอนเดียวให้ปริมาณที่ต้องการอยู่ตัวเดียว",
            )
        if which == 1:
            index = rng.randrange(len(OHM_UNITS))
            quantity = OHM_UNIT_QUANTITIES[index]
            wrongs = tuple(name for name in OHM_QUANTITY_NAMES if name != quantity)
            return _elec_question(
                stem=f"ปริมาณใดในวงจรไฟฟ้ามีหน่วยเป็น{OHM_UNITS[index]}",
                correct=quantity,
                wrongs=wrongs,
                hint="จับคู่หน่วยกับปริมาณทีละคู่: โวลต์คู่กับความต่างศักย์ แอมแปร์คู่กับกระแสไฟฟ้า และโอห์มคู่กับความต้านทาน",
            )
        if which == 2:
            target, correct = rng.choice(OHM_INSTRUMENTS)
            wrongs = tuple(item for item in OHM_INSTRUMENT_WRONGS if item != correct)[:3]
            return _elec_question(
                stem=f"ต้องการวัด{target} ควรใช้เครื่องมือใดและต่ออย่างไร",
                correct=correct,
                wrongs=wrongs,
                hint="แอมมิเตอร์วัดกระแสจึงต้องให้กระแสไหลผ่าน ส่วนโวลต์มิเตอร์วัดความต่างศักย์คร่อมอุปกรณ์",
            )
        if which == 3:
            symbol, quantity, unit = rng.choice(OHM_SYMBOLS)
            wrongs = tuple(name for name in OHM_QUANTITY_NAMES if name != quantity)
            return _elec_question(
                stem=f"ในสมการ V = IR สัญลักษณ์ {symbol} แทนปริมาณใด",
                correct=quantity,
                wrongs=wrongs,
                hint=f"เทียบสัญลักษณ์กับหน่วยของปริมาณนั้น เช่น {symbol} วัดเป็น{unit}",
            )
        if rng.randrange(2) == 0:
            return _elec_question(
                stem=("ใช้ตัวต้านทานตัวเดิมที่มีความต้านทานคงที่ "
                      "ถ้าเพิ่มความต่างศักย์คร่อมตัวต้านทาน กระแสไฟฟ้าจะเปลี่ยนอย่างไร"),
                correct="เพิ่มขึ้น",
                wrongs=("ลดลง", "คงเดิม", "เพิ่มขึ้นแล้วลดลงกลับค่าเดิม"),
                hint="ในสมการ I = V/R ให้ R คงที่ แล้วดูว่า V ที่มากขึ้นทำให้ผลหารเปลี่ยนไปทางใด",
            )
        return _elec_question(
            stem=("ต่ออุปกรณ์กับแหล่งกำเนิดไฟฟ้าที่ความต่างศักย์คงที่ "
                  "ถ้าเปลี่ยนไปใช้ตัวต้านทานที่มีความต้านทานมากขึ้น กระแสไฟฟ้าจะเปลี่ยนอย่างไร"),
            correct="ลดลง",
            wrongs=("เพิ่มขึ้น", "คงเดิม", "ลดลงแล้วเพิ่มขึ้นกลับค่าเดิม"),
            hint="ในสมการ I = V/R ให้ V คงที่ แล้วดูว่า R ที่มากขึ้นทำให้ผลหารเปลี่ยนไปทางใด",
        )


@question_type("elec.ohms_law",
               display_name={"th": "กฎของโอห์ม (V = IR)"},
               level=LEVEL, subject=SUBJECT, topic=TOPIC)
class OhmsLaw(PhysCalc):
    """V = IR — ถามครบทั้งสามทาง (หา V, หา I, หา R).

    โจทย์สร้างจาก I กับ R ก่อนแล้วจึงคำนวณ V ทุกคำตอบจึงลงตัวเสมอ ตัวลวงหลักคือ
    การสับสนของการดำเนินการ — บวกแทนคูณเมื่อหา V และคูณแทนหารเมื่อหา I หรือ R.
    """

    _R = [2, 3, 4, 5, 6, 8, 10, 12]          # ความต้านทาน (โอห์ม)
    _I = [1, 2, 3, 4, 5, 6]                  # กระแสไฟฟ้า (แอมแปร์)

    def draw(self, rng: Random) -> Calc:
        r, i = rng.choice(self._R), rng.choice(self._I)
        v = i * r
        which = rng.random()
        if which < 0.34:                     # ให้ I กับ R → หา V
            return Calc(
                f"ตัวต้านทานขนาด {r} โอห์ม มีกระแสไฟฟ้าผ่าน {i} แอมแปร์ "
                f"จงหาความต่างศักย์คร่อมตัวต้านทานนี้ (โวลต์)",
                fmt(v), wrongs=slips(fmt(v), i + r, r - i, v * 2),
                hint=r"V = IR")
        if which < 0.67:                     # ให้ V กับ R → หา I
            return Calc(
                f"ต่อตัวต้านทานขนาด {r} โอห์ม เข้ากับความต่างศักย์ {v} โวลต์ "
                f"จงหากระแสไฟฟ้าที่ผ่านตัวต้านทาน (แอมแปร์)",
                fmt(i), wrongs=slips(fmt(i), v * r, v - r, r / v),
                hint=r"I = \frac{V}{R}")
        return Calc(                         # ให้ V กับ I → หา R
            f"เมื่อต่อตัวต้านทานตัวหนึ่งเข้ากับความต่างศักย์ {v} โวลต์ "
            f"มีกระแสไฟฟ้าผ่าน {i} แอมแปร์ จงหาความต้านทานของตัวต้านทานนี้ (โอห์ม)",
            fmt(r), wrongs=slips(fmt(r), v * i, v - i, i / v),
            hint=r"R = \frac{V}{I}")


@question_type(
    "elec.ohms_law_fluency",
    display_name={"th": "กฎของโอห์ม: อ่านผลการวัดและคำนวณ"},
    level={"th": "ม.3"}, subject=PHYSICS, topic=ELECTRICITY,
)
class OhmsLawFluency(QuestionType):
    """Read one measurement table or graph and apply V = IR once."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        which = rng.randrange(4)
        if which == 0:
            resistance = rng.choice((3, 4, 5, 6, 8, 10, 12))
            first = rng.choice((2, 3))
            rows = tuple(
                OhmsMeasurement(resistance * current, current)
                for current in (first, first + 1, first + 2)
            )
            voltage = rows[0].voltage
            return _elec_question(
                stem=("ต่อตัวต้านทานตัวหนึ่งกับแหล่งกำเนิดที่ปรับค่าได้ "
                      f"และบันทึกผลการวัดได้ดังนี้\n{_ohm_table(rows)}\n"
                      "ตัวต้านทานนี้มีความต้านทานเท่าใด"),
                correct=f"{resistance} โอห์ม",
                wrongs=(
                    f"{voltage * first} โอห์ม",
                    f"{voltage + first} โอห์ม",
                    f"{voltage - first} โอห์ม",
                ),
                hint="ความต้านทานหาได้จาก R = V/I และควรได้ค่าเท่ากันทุกครั้งที่วัด",
            )
        if which == 1:
            resistance = rng.choice((3, 4, 5, 6, 8, 10, 12))
            current = rng.choice((1, 3, 4, 5))
            factor = rng.choice((2, 3))
            voltage = resistance * current
            return _elec_question(
                stem=(f"ตัวต้านทานตัวหนึ่งมีกระแสไฟฟ้าผ่าน {current} A "
                      f"เมื่อความต่างศักย์คร่อมตัวต้านทานเป็น {voltage} V "
                      f"ถ้าเพิ่มความต่างศักย์เป็น {voltage * factor} V "
                      "โดยใช้ตัวต้านทานตัวเดิม กระแสไฟฟ้าจะเป็นเท่าใด"),
                correct=f"{current * factor} A",
                wrongs=(
                    f"{current} A",
                    f"{current + factor} A",
                    f"{current * factor * factor} A",
                ),
                hint="ความต้านทานไม่เปลี่ยน จึงใช้ I = V/R กับความต่างศักย์ค่าใหม่",
            )
        if which == 2:
            resistance = rng.choice((4, 5, 6, 10))
            rows = tuple(
                OhmsMeasurement(resistance * current, current)
                for current in (1, 2, 3)
            )
            return _elec_question(
                stem=("ใช้ตัวต้านทานตัวเดิมและวัดค่าได้ดังนี้\n"
                      f"{_ohm_table(rows)}\n"
                      "ข้อสรุปใดตรงกับหลักฐานในตารางมากที่สุด"),
                correct="เมื่อความต้านทานคงที่ กระแสไฟฟ้าแปรผันตรงกับความต่างศักย์",
                wrongs=(
                    "เมื่อความต้านทานคงที่ กระแสไฟฟ้าแปรผกผันกับความต่างศักย์",
                    "ความต่างศักย์ที่เพิ่มขึ้นทำให้ความต้านทานของตัวต้านทานเพิ่มขึ้นด้วย",
                    "กระแสไฟฟ้าไม่ขึ้นกับความต่างศักย์ เพราะเป็นตัวต้านทานตัวเดิม",
                ),
                hint="เทียบอัตราส่วน V/I ของทุกแถว แล้วดูว่า I เปลี่ยนตาม V ในทิศทางใด",
            )
        slope = rng.choice((3, 4, 5, 6, 8, 10, 12))
        return _elec_question(
            stem=("เขียนกราฟความต่างศักย์ V (แกนตั้ง) กับกระแสไฟฟ้า I (แกนนอน) "
                  f"ของตัวต้านทานตัวหนึ่ง ได้เส้นตรงผ่านจุดกำเนิดที่มีความชัน {slope} "
                  "ความชันของกราฟนี้บอกปริมาณใดและมีค่าเท่าใด"),
            correct=f"ความต้านทาน {slope} โอห์ม",
            wrongs=(
                f"กระแสไฟฟ้า {slope} แอมแปร์",
                f"ความต่างศักย์ {slope} โวลต์",
                f"กำลังไฟฟ้า {slope} วัตต์",
            ),
            hint="ความชันคือ V หารด้วย I ให้เทียบกับสมการ V = IR ว่าตรงกับปริมาณใด",
        )


@question_type(
    "elec.ohms_law_application",
    display_name={"th": "กฎของโอห์ม: วิเคราะห์ข้อมูลและออกแบบการทดลอง"},
    level={"th": "ม.3"}, subject=PHYSICS, topic=ELECTRICITY,
)
class OhmsLawApplication(QuestionType):
    """Compare devices, screen measurements, control variables, and plan a change."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        which = rng.randrange(4)
        if which == 0:
            voltage = rng.choice((12, 24, 36, 60))
            options = [i for i in (1, 2, 3, 4, 5, 6, 10, 12) if voltage % i == 0]
            larger, smaller = sorted(rng.sample(options, 2), reverse=True)
            low, high = voltage // larger, voltage // smaller
            return _elec_question(
                stem=(f"ต่อตัวต้านทาน ก และ ข เข้ากับแหล่งกำเนิดเดียวกันที่ {voltage} V "
                      f"วัดกระแสได้ {larger} A ผ่าน ก และ {smaller} A ผ่าน ข "
                      "ข้อสรุปใดใช้หลักฐานได้ถูกต้อง"),
                correct=(f"ก มีความต้านทาน {low} โอห์ม และ ข มีความต้านทาน {high} โอห์ม "
                         "ดังนั้น ข ต้านทานมากกว่า"),
                wrongs=(
                    (f"ก มีความต้านทาน {high} โอห์ม และ ข มีความต้านทาน {low} โอห์ม "
                     "ดังนั้น ก ต้านทานมากกว่า"),
                    "ก ต้านทานมากกว่า เพราะมีกระแสไฟฟ้าผ่านมากกว่า",
                    "ทั้งสองตัวมีความต้านทานเท่ากัน เพราะใช้ความต่างศักย์เท่ากัน",
                ),
                hint="คำนวณ R = V/I ของแต่ละตัวก่อนเปรียบเทียบ อย่าตัดสินจากกระแสเพียงอย่างเดียว",
            )
        if which == 1:
            resistance = rng.choice((4, 5, 6, 10, 12))
            bad_index = rng.randrange(4)
            offset = rng.choice((-3, -2, 2, 3))
            rows = []
            for index, current in enumerate((1, 2, 3, 4)):
                voltage = resistance * current
                if index == bad_index:
                    voltage += offset * current
                rows.append(OhmsMeasurement(voltage, current))
            labels = tuple(
                f"ครั้งที่ {index}: {row.voltage} V กับ {row.current} A"
                for index, row in enumerate(rows, start=1)
            )
            return _elec_question(
                stem=("นักเรียนวัดค่าของตัวต้านทานตัวเดิมสี่ครั้งและได้ข้อมูลดังนี้\n"
                      f"{_ohm_table(tuple(rows))}\n"
                      "การวัดครั้งใดน่าจะคลาดเคลื่อน เพราะไม่สอดคล้องกับครั้งอื่น"),
                correct=labels[bad_index],
                wrongs=tuple(
                    label for index, label in enumerate(labels) if index != bad_index
                ),
                hint="คำนวณ V/I ของทุกครั้ง ครั้งที่ให้ค่าต่างจากครั้งอื่นคือครั้งที่น่าสงสัย",
            )
        if which == 2:
            return _elec_question(
                stem=("ต้องการทดสอบว่ากระแสไฟฟ้าสัมพันธ์กับความต่างศักย์อย่างไร "
                      "แผนการทดลองใดให้หลักฐานเชิงประจักษ์ที่เชื่อถือได้มากที่สุด"),
                correct=("ใช้ตัวต้านทานตัวเดิมและควบคุมอุณหภูมิ ปรับเฉพาะความต่างศักย์ "
                         "แล้ววัดกระแสหลายค่า"),
                wrongs=(
                    "เปลี่ยนทั้งตัวต้านทานและความต่างศักย์ในการวัดแต่ละครั้ง เพื่อให้ได้ข้อมูลหลากหลาย",
                    "วัดเพียงครั้งเดียวที่ความต่างศักย์ค่าหนึ่ง แล้วสรุปความสัมพันธ์จากค่านั้น",
                    "ปรับเฉพาะความต้านทานโดยให้ความต่างศักย์คงที่ แล้วสรุปผลของความต่างศักย์",
                ),
                hint="ระบุตัวแปรต้นหนึ่งตัวและตัวแปรตามหนึ่งตัว แล้วตรวจว่าปัจจัยอื่นถูกควบคุมและวัดซ้ำหลายค่าหรือไม่",
            )
        voltage, before, after = rng.choice(OHM_DIMMER_CASES)
        device = rng.choice(OHM_DEVICES)
        old, new = voltage // before, voltage // after
        return _elec_question(
            stem=(f"{device}ต่อกับแหล่งกำเนิด {voltage} V และมีกระแสไฟฟ้าผ่าน {before} A "
                  f"ต้องการลดกระแสให้เหลือ {after} A ที่ความต่างศักย์เดิม "
                  "ต้องเพิ่มความต้านทานรวมของวงจรอีกกี่โอห์ม"),
            correct=f"{new - old} โอห์ม",
            wrongs=(
                f"{new} โอห์ม",
                f"{old} โอห์ม",
                f"{new + old} โอห์ม",
            ),
            hint="หาความต้านทานเดิมและความต้านทานที่ต้องการจาก R = V/I ก่อน แล้วจึงหาผลต่าง",
        )
