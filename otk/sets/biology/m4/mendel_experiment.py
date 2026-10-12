"""การทดลองของเมนเดล

ชีวะ · ม.4 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 2 ม.4/1

Sets moved here from: science_wave_f48.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f48 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_MENDEL = "การทดลองของเมนเดล"


TRAITS = (
    ("รูปร่างเมล็ด", "กลม", "ขรุขระ"), ("สีเมล็ด", "เหลือง", "เขียว"), ("สีดอก", "ม่วง", "ขาว"),
    ("รูปร่างฝัก", "อวบ", "แฟบเป็นข้อ"), ("สีฝัก", "เขียว", "เหลือง"), ("ตำแหน่งดอก", "ที่ซอกใบ", "ที่ปลายยอด"),
    ("ความสูงของลำต้น", "สูง", "เตี้ย"),
)


WHY_PEA = (
    ("เมนเดลเลือกถั่วลันเตาเพราะเหตุใด", "ปลูกง่าย อายุสั้น ได้ลูกมาก มีลักษณะที่แตกต่างชัดเจน และผสมตัวเองได้",
     ("เป็นพืชที่มีโครโมโซมมากที่สุด", "ผสมข้ามพันธุ์เองตามธรรมชาติเสมอ", "ไม่ต้องใช้ดินในการปลูก")),
    ("ลักษณะที่ปรากฏในรุ่น F₁ ทั้งหมดเรียกว่าอะไร", "ลักษณะเด่น", ("ลักษณะด้อย", "ลักษณะแปรผันต่อเนื่อง",
                                                              "ลักษณะที่เกิดจากสิ่งแวดล้อม")),
    ("ลักษณะด้อยที่หายไปใน F₁ กลับมาปรากฏในรุ่นใด", "รุ่น F₂", ("รุ่น F₁", "ไม่ปรากฏอีกเลย", "รุ่นพ่อแม่เท่านั้น")),
    ("เมนเดลสรุปว่าลักษณะถูกควบคุมด้วยอะไร", "หน่วยพันธุกรรมที่มาเป็นคู่ และแยกจากกันเมื่อสร้างเซลล์สืบพันธุ์",
     ("เลือดที่ผสมกันระหว่างพ่อแม่", "อาหารที่ต้นถั่วได้รับ", "สิ่งแวดล้อมเพียงอย่างเดียว")),
)


@question_type(
    "biology.mendel_experiment_foundation",
    display_name={"th": "ลักษณะเด่นและลักษณะด้อยในการทดลองของเมนเดล"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MENDEL,
)
class MendelExperimentFoundation(QuestionType):
    """Crossing pure lines: F₁ shows only the dominant trait."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        trait, dominant, recessive = rng.choice(TRAITS)
        if rng.random() < 0.35:
            want_dominant = rng.random() < 0.5
            pick = f"{trait}{dominant if want_dominant else recessive}"
            others = [f"{t}{r if want_dominant else d}" for t, d, r in TRAITS if t != trait]
            return _labelled(stem=f"ในการทดลองของเมนเดล ลักษณะใดของถั่วลันเตาเป็นลักษณะ{'เด่น' if want_dominant else 'ด้อย'}",
                             correct=pick, wrongs=tuple(others), topic=TOPIC_MENDEL,
                             hint="เมล็ดกลม เมล็ดเหลือง ดอกม่วง ฝักอวบ ฝักเขียว ดอกที่ซอกใบ และต้นสูง เป็นลักษณะเด่น")
        if rng.random() < 0.6:
            options = (f"{trait}{dominant}ทั้งหมด", f"{trait}{recessive}ทั้งหมด", f"{trait}{dominant}และ{recessive}อย่างละครึ่ง",
                       f"{trait}เป็นลักษณะกึ่งกลางระหว่าง{dominant}กับ{recessive}")
            return _labelled(stem=f"เมนเดลผสมถั่วลันเตาพันธุ์แท้{trait}{dominant}กับ{trait}{recessive} รุ่น F₁ มีลักษณะอย่างไร",
                             correct=options[0], wrongs=options[1:], topic=TOPIC_MENDEL,
                             hint="พ่อแม่พันธุ์แท้ต่างลักษณะ ลูกรุ่น F₁ ทุกต้นแสดงลักษณะเด่น")
        stem, right, wrongs = rng.choice(WHY_PEA)
        return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_MENDEL,
                         hint="เมนเดลผสมพันธุ์แท้ต่างลักษณะ ได้ F₁ ลักษณะเด่น แล้วให้ F₁ ผสมตัวเองได้ F₂")


@question_type(
    "biology.mendel_experiment_fluency",
    display_name={"th": "อัตราส่วนลักษณะในรุ่น F₂"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MENDEL,
)
class MendelExperimentFluency(QuestionType):
    """F₁ selfed gives dominant : recessive = 3 : 1 in F₂."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        trait, dominant, recessive = rng.choice(TRAITS)
        total = rng.randrange(40, 2001, 4)
        which = rng.random() < 0.5
        answer = total * 3 // 4 if which else total // 4
        return numeric(stem=f"นำถั่วลันเตา F₁ ที่ได้จากการผสม{trait}{dominant}พันธุ์แท้กับ{recessive}พันธุ์แท้มาผสมกันเอง ได้ F₂ {total} ต้น "
                            f"คาดว่าจะมีต้นที่{trait}{dominant if which else recessive}กี่ต้น",
                       answer=answer, wrongs=[total - answer, total // 2, total], unit="ต้น", topic=TOPIC_MENDEL,
                       hint="F₂ มีลักษณะเด่น : ลักษณะด้อย = 3 : 1")


@question_type(
    "biology.mendel_experiment_application",
    display_name={"th": "สรุปผลการทดลองของเมนเดลจากข้อมูล"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MENDEL,
)
class MendelExperimentApplication(QuestionType):
    """Read a count, find the ratio, and decide which trait is dominant."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        trait, dominant, recessive = rng.choice(TRAITS)
        unit = rng.randrange(20, 401)
        many, few = unit * 3 + rng.randint(-3, 3), unit + rng.randint(-2, 2)
        if rng.random() < 0.5:
            return _labelled(stem=f"ผลการผสม F₁ ด้วยกันเองได้ F₂ {trait}{dominant} {many} ต้น และ{recessive} {few} ต้น ข้อใดสรุปได้ถูกต้อง",
                             correct=f"{dominant}เป็นลักษณะเด่น อัตราส่วนประมาณ 3 : 1",
                             wrongs=(f"{recessive}เป็นลักษณะเด่น อัตราส่วนประมาณ 3 : 1", f"{dominant}เป็นลักษณะเด่น อัตราส่วนประมาณ 1 : 1",
                                     "ทั้งสองลักษณะเด่นเท่ากัน อัตราส่วนประมาณ 1 : 2 : 1"),
                             topic=TOPIC_MENDEL, hint="ลักษณะที่พบมากกว่าประมาณ 3 เท่าใน F₂ คือลักษณะเด่น")
        return _labelled(stem=f"ผสมต้นถั่ว{trait}{dominant}ที่ไม่ทราบพันธุ์กับต้น{recessive} ได้ลูก{dominant} {unit + rng.randint(-2, 2)} ต้น "
                              f"และ{recessive} {unit + rng.randint(-2, 2)} ต้น ต้น{dominant}ที่นำมาผสมมีจีโนไทป์แบบใด",
                         correct="พันธุ์ทาง (เฮเทอโรไซกัส)", wrongs=("พันธุ์แท้ลักษณะเด่น (โฮโมไซกัสเด่น)",
                                                             "พันธุ์แท้ลักษณะด้อย (โฮโมไซกัสด้อย)", "บอกไม่ได้จากข้อมูลนี้"),
                         topic=TOPIC_MENDEL, hint="ผสมทดสอบกับลักษณะด้อยแล้วได้ 1 : 1 แสดงว่าต้นลักษณะเด่นเป็นพันธุ์ทาง")
