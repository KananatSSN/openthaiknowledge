"""สมบัติของธาตุแทรนซิชัน

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.4/6

Sets moved here from: science_wave_f19.
"""

from __future__ import annotations

from random import Random

from otk.core.distractors import near_length_sample
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f19 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_TRANSITION = "สมบัติของธาตุแทรนซิชัน"


TRANSITION_FACTS = (
    ("ข้อใดเป็นสมบัติเด่นของธาตุแทรนซิชัน", "สารประกอบส่วนใหญ่มีสี และมีเลขออกซิเดชันได้หลายค่า",
     ("มีเลขออกซิเดชันได้ค่าเดียวเสมอ และสารประกอบไม่มีสี", "สารประกอบไม่มีสีทั้งหมด และมีเลขออกซิเดชันเดียว", "เป็นอโลหะทั้งหมดที่มีจุดหลอมเหลวต่ำ")),
    ("เปรียบเทียบธาตุแทรนซิชันกับโลหะหมู่ 1 ข้อใดถูกต้อง", "ธาตุแทรนซิชันมีจุดหลอมเหลวและความหนาแน่นสูงกว่า",
     ("ธาตุแทรนซิชันว่องไวต่อน้ำมากกว่าจนต้องเก็บในน้ำมัน", "ธาตุแทรนซิชันอ่อนนิ่มตัดด้วยมีดได้", "ธาตุแทรนซิชันมีจุดหลอมเหลวต่ำกว่าและเบากว่า")),
    ("ธาตุแทรนซิชันหลายชนิดใช้เป็นตัวเร่งปฏิกิริยาในอุตสาหกรรม เช่น ข้อใด", "เหล็กในการผลิตแอมโมเนีย",
     ("โซเดียมในการผลิตแก้ว", "คลอรีนในการฆ่าเชื้อ", "ฮีเลียมในบอลลูน")),
    ("ธาตุแทรนซิชันอยู่ในส่วนใดของตารางธาตุ", "หมู่ 3 ถึงหมู่ 12 (กลุ่ม B)", ("หมู่ 1 และ 2", "หมู่ 13 ถึง 18", "แถวแลนทาไนด์เท่านั้น")),
    ("ธาตุแทรนซิชันเกิดไอออนเชิงซ้อนได้ง่าย เพราะเหตุใด", "มีออร์บิทัล d ว่างที่รับคู่อิเล็กตรอนจากลิแกนด์ได้",
     ("มีเวเลนซ์อิเล็กตรอนตัวเดียวเหมือนโลหะหมู่ 1", "เป็นแก๊สที่อุณหภูมิห้องเกือบทุกธาตุ", "ไม่มีอิเล็กตรอนในระดับพลังงานย่อย d จึงรับคู่อิเล็กตรอนได้")),
)


ION_COLOURS = (
    ("Cu²⁺", "สีฟ้า"), ("Fe³⁺", "สีเหลืองแกมน้ำตาล"), ("Fe²⁺", "สีเขียวอ่อน"), ("Cr₂O₇²⁻", "สีส้ม"),
    ("MnO₄⁻", "สีม่วง"), ("Ni²⁺", "สีเขียว"), ("Co²⁺", "สีชมพู"), ("CrO₄²⁻", "สีเหลือง"),
)


# (formula, metal, its oxidation number)
OXIDATION = (
    ("KMnO₄", "Mn", 7), ("MnO₂", "Mn", 4), ("MnCl₂", "Mn", 2), ("K₂Cr₂O₇", "Cr", 6), ("Cr₂O₃", "Cr", 3),
    ("FeCl₃", "Fe", 3), ("FeSO₄", "Fe", 2), ("Fe₂O₃", "Fe", 3), ("CuO", "Cu", 2), ("Cu₂O", "Cu", 1),
    ("V₂O₅", "V", 5), ("TiO₂", "Ti", 4), ("K₂CrO₄", "Cr", 6), ("ZnCl₂", "Zn", 2), ("Co(NO₃)₂", "Co", 2),
)


@question_type(
    "chem.transition_metal_foundation",
    display_name={"th": "สมบัติของธาตุแทรนซิชันเทียบกับโลหะเรพรีเซนเททีฟ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_TRANSITION,
)
class TransitionMetalFoundation(QuestionType):
    """Coloured compounds, many oxidation states, high melting points, catalysts."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, correct, wrongs = rng.choice(TRANSITION_FACTS)
        if rng.random() < 0.6:
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_TRANSITION,
                             hint="ธาตุแทรนซิชัน: จุดหลอมเหลวสูง สารประกอบมีสี มีหลายเลขออกซิเดชัน และเป็นตัวเร่งปฏิกิริยา")
        transition = rng.choice((("เหล็ก", "Fe"), ("ทองแดง", "Cu"), ("โครเมียม", "Cr"), ("นิกเกิล", "Ni"),
                                 ("แมงกานีส", "Mn"), ("สังกะสี", "Zn"), ("โคบอลต์", "Co")))
        others = near_length_sample(rng, (("โซเดียม", "Na"), ("แมกนีเซียม", "Mg"), ("โพแทสเซียม", "K"), ("แคลเซียม", "Ca"),
                                          ("อะลูมิเนียม", "Al"), ("ลิเทียม", "Li"), ("แบเรียม", "Ba")),
                                    f"{transition[0]} ({transition[1]})", key=lambda e: f"{e[0]} ({e[1]})")
        listed = [transition, *others]
        rng.shuffle(listed)
        return _labelled(stem=f"ธาตุใดต่อไปนี้เป็นธาตุแทรนซิชัน: {' '.join(f'{n} ({s})' for n, s in listed)}",
                         correct=f"{transition[0]} ({transition[1]})", wrongs=tuple(f"{n} ({s})" for n, s in others),
                         topic=TOPIC_TRANSITION, hint="ธาตุแทรนซิชันอยู่หมู่ 3-12 เช่น Fe Cu Cr Ni Mn ส่วน Na K Mg Ca Al เป็นโลหะเรพรีเซนเททีฟ")


@question_type(
    "chem.transition_metal_fluency",
    display_name={"th": "สีของไอออนของธาตุแทรนซิชัน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_TRANSITION,
)
class TransitionMetalFluency(QuestionType):
    """Match an ion to the colour of its solution, either way round."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        chosen = rng.sample(ION_COLOURS, 4)
        ion, colour = chosen[0]
        hint = "Cu²⁺ ฟ้า Fe³⁺ เหลืองน้ำตาล Fe²⁺ เขียวอ่อน Cr₂O₇²⁻ ส้ม CrO₄²⁻ เหลือง MnO₄⁻ ม่วง Ni²⁺ เขียว Co²⁺ ชมพู"
        if rng.random() < 0.5:
            return _labelled(stem=f"สารละลายที่มีไอออน {ion} มีสีใด", correct=colour,
                             wrongs=tuple(c for _, c in chosen[1:]), topic=TOPIC_TRANSITION, hint=hint)
        return _labelled(stem=f"สารละลาย{colour}น่าจะมีไอออนใด", correct=ion,
                         wrongs=tuple(i for i, _ in chosen[1:]), topic=TOPIC_TRANSITION, hint=hint)


@question_type(
    "chem.transition_metal_application",
    display_name={"th": "เลขออกซิเดชันของธาตุแทรนซิชันในสารประกอบ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_TRANSITION,
)
class TransitionMetalApplication(QuestionType):
    """One metal, several oxidation numbers: work each out from the formula."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            formula, metal, number = rng.choice(OXIDATION)
        else:
            metal, number = rng.choice((("Fe", 2), ("Fe", 3), ("Cu", 1), ("Cu", 2), ("Mn", 2), ("Mn", 4), ("Cr", 2), ("Cr", 3),
                                        ("Co", 2), ("Co", 3), ("Ni", 2), ("V", 3), ("V", 5), ("Ti", 4), ("Zn", 2)))
            sub = lambda n: "" if n == 1 else str(n).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))
            formula = rng.choice((f"{metal}{sub(2 if number % 2 else 1)}O{sub(number if number % 2 else number // 2)}",
                                  f"{metal}Cl{sub(number)}", f"{metal}(NO₃){sub(number)}" if number > 1 else f"{metal}NO₃"))
        return numeric(
            stem=f"เลขออกซิเดชันของ {metal} ใน {formula} เท่าใด (O = −2, K = +1, Cl = −1, SO₄ = −2, NO₃ = −1)",
            answer=number, wrongs=[number + 1, number - 1 if number > 1 else number + 2, 8 - number if 8 - number != number else 2],
            unit="", topic=TOPIC_TRANSITION,
            hint="ผลรวมเลขออกซิเดชันในสารประกอบเป็นศูนย์ หาเลขของโลหะจากธาตุหรือกลุ่มอื่นที่รู้ค่า")
