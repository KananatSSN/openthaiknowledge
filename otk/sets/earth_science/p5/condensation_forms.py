"""เมฆ หมอก น้ำค้าง และน้ำค้างแข็ง

ธรณีวิทยา · ป.5 · สสวท. พื้นฐาน
Indicators: ว 3.2 ป.5/4

Sets moved here from: science_wave_c13.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b24 import PRIMARY_FIVE
from otk.sets._support.science_wave_c10 import LETTERS, SUBJECT
from otk.sets._support.science_wave_c13 import CONDENSATION_SCENARIOS, _swapped, _swaps

PROVENANCE = Provenance("original")


CONDENSATION_TOPIC = "เมฆ หมอก น้ำค้าง และน้ำค้างแข็ง"


class Form(NamedTuple):
    """One thing water vapour becomes, how, and the classroom model that shows it."""
    name: str
    how: str
    model: str


# No two rows share a description or a model, so a swap always changes the text.
FORMS = (
    Form("เมฆ",
         "ไอน้ำในอากาศที่ลอยสูงขึ้นและเย็นลงควบแน่นบนละอองฝุ่น เป็นละอองน้ำเล็ก ๆ ลอยอยู่สูงจากพื้น",
         "ใส่ควันธูปลงในขวดที่มีน้ำอุ่นเล็กน้อย บีบขวดแล้วปล่อยทันที เกิดละอองขาวฟุ้งทั่วขวด"),
    Form("หมอก",
         "ไอน้ำในอากาศใกล้พื้นควบแน่นเมื่ออากาศเย็นลง เป็นละอองน้ำเล็ก ๆ ลอยอยู่ใกล้พื้นดิน",
         "เทน้ำอุ่นลงในขวดแล้ววางก้อนน้ำแข็งบนปากขวด เกิดละอองขาวลอยอยู่เหนือผิวน้ำในขวด"),
    Form("น้ำค้าง",
         "ไอน้ำในอากาศควบแน่นเมื่อสัมผัสผิววัตถุที่เย็น เป็นหยดน้ำเกาะอยู่บนผิววัตถุ",
         "ใส่น้ำแข็งลงในแก้ว ไม่นานมีหยดน้ำเกาะรอบนอกแก้ว"),
    Form("น้ำค้างแข็ง",
         "ไอน้ำในอากาศสัมผัสผิววัตถุที่เย็นจัดต่ำกว่าจุดเยือกแข็ง เปลี่ยนเป็นเกล็ดน้ำแข็งเกาะอยู่บนผิววัตถุ",
         "ใส่น้ำแข็งผสมเกลือลงในกระป๋องโลหะ ไม่นานมีเกล็ดสีขาวเกาะรอบนอกกระป๋อง"),
)


# Things one sees, one form each.
FORM_EXAMPLES = {
    "เมฆ": ("กลุ่มละอองน้ำสีขาวลอยอยู่สูงบนท้องฟ้า",
            "ก้อนสีเทาเข้มบนท้องฟ้าที่ก่อตัวขึ้นก่อนฝนตก"),
    "หมอก": ("ละอองขาวลอยต่ำเหนือนาข้าวตอนเช้ามืดจนมองไม่เห็นทางข้างหน้า",
             "ละอองขาวปกคลุมผิวน้ำในบึงตอนเช้าที่อากาศเย็น"),
    "น้ำค้าง": ("หยดน้ำใสเกาะบนใบหญ้าตอนเช้า",
                "หยดน้ำเกาะบนเบาะรถที่จอดไว้กลางแจ้งทั้งคืน"),
    "น้ำค้างแข็ง": ("เกล็ดน้ำแข็งสีขาวเกาะบนยอดหญ้าบนยอดดอยในเช้าที่หนาวจัด",
                    "เกล็ดน้ำแข็งบาง ๆ เกาะบนหลังคารถบนภูเขาสูงในเช้าฤดูหนาว"),
}


def _compare_forms(order: list[Form], hows: list[str]) -> str:
    return " / ".join(f"{form.name}: {how}" for form, how in zip(order, hows))


def _match_models(order: list[Form], models: list[str]) -> str:
    return " / ".join(f"แบบจำลอง {letter} → {form.name}"
                      for letter, form in zip(models, order))


@question_type(
    "geo.condensation_forms_foundation",
    display_name={"th": "เมฆ หมอก น้ำค้าง และน้ำค้างแข็ง"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=CONDENSATION_TOPIC,
)
class CondensationFormsFoundation(QuestionType):
    """Know each of the four one at a time, before comparing them."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        form = rng.choice(FORMS)
        others = [other for other in FORMS if other.name != form.name]
        ask = rng.randrange(4)
        if ask == 2:
            return _labelled(
                stem=f"“{rng.choice(FORM_EXAMPLES[form.name])}” คือสิ่งใด",
                correct=form.name,
                wrongs=tuple(other.name for other in others),
                hint="ถามว่าเกิดสูงในอากาศ ใกล้พื้น หรือบนผิววัตถุ และเป็นน้ำหรือน้ำแข็ง",
                topic=CONDENSATION_TOPIC,
            )
        if ask == 3:
            return _labelled(
                stem=f"ข้อใดเป็นตัวอย่างของ “{form.name}”",
                correct=rng.choice(FORM_EXAMPLES[form.name]),
                wrongs=tuple(rng.choice(FORM_EXAMPLES[other.name]) for other in others),
                hint="ถามว่าเกิดสูงในอากาศ ใกล้พื้น หรือบนผิววัตถุ และเป็นน้ำหรือน้ำแข็ง",
                topic=CONDENSATION_TOPIC,
            )
        if ask == 0:
            return _labelled(
                stem=f"“{form.name}” เกิดขึ้นได้อย่างไร",
                correct=form.how,
                wrongs=tuple(other.how for other in others),
                hint="ถามว่าเกิดสูงในอากาศ ใกล้พื้น หรือบนผิววัตถุ และเป็นน้ำหรือน้ำแข็ง",
                topic=CONDENSATION_TOPIC,
            )
        return _labelled(
            stem=f"สิ่งที่เกิดจาก{form.how} เรียกว่าอะไร",
            correct=form.name,
            wrongs=tuple(other.name for other in others),
            hint="ถามว่าเกิดสูงในอากาศ ใกล้พื้น หรือบนผิววัตถุ และเป็นน้ำหรือน้ำแข็ง",
            topic=CONDENSATION_TOPIC,
        )


@question_type(
    "geo.condensation_forms_fluency",
    display_name={"th": "เปรียบเทียบการเกิดเมฆ หมอก น้ำค้าง และน้ำค้างแข็งจากแบบจำลอง"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=CONDENSATION_TOPIC,
)
class CondensationFormsFluency(QuestionType):
    """Compare all four from the models; each wrong choice swaps two of them."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        order = list(FORMS)
        if rng.random() < 0.5:
            models = list(FORMS)
            rng.shuffle(models)
            record = " / ".join(f"แบบจำลอง {letter}: {form.model}"
                                for letter, form in zip(LETTERS, models))
            letter_of = {form.name: LETTERS[i] for i, form in enumerate(models)}
            right = [letter_of[form.name] for form in order]
            return _labelled(
                stem=f"นักเรียนทำแบบจำลอง 4 แบบ — {record} "
                     "ข้อใดจับคู่แบบจำลองกับการเกิดเมฆ หมอก น้ำค้าง และน้ำค้างแข็งได้ถูกต้องทั้งหมด",
                correct=_match_models(order, right),
                wrongs=tuple(_match_models(order, _swapped(right, i, j))
                             for i, j in _swaps(rng, 3, 4)),
                hint="ดูว่าในแต่ละแบบจำลอง ละอองหรือหยดน้ำเกิดที่ใด และเป็นน้ำหรือน้ำแข็ง",
                topic=CONDENSATION_TOPIC,
            )
        rng.shuffle(order)
        hows = [form.how for form in order]
        models = " / ".join(form.model for form in FORMS)
        return _labelled(
            stem=f"จากแบบจำลอง — {models} — "
                 "ข้อใดเปรียบเทียบการเกิดเมฆ หมอก น้ำค้าง และน้ำค้างแข็งได้ถูกต้องทั้งหมด",
            correct=_compare_forms(order, hows),
            wrongs=tuple(_compare_forms(order, _swapped(hows, i, j))
                         for i, j in _swaps(rng, 3, 4)),
            hint="ตรวจทีละอย่าง: เกิดที่ใด และเป็นหยดน้ำ ละอองน้ำ หรือเกล็ดน้ำแข็ง",
            topic=CONDENSATION_TOPIC,
        )


@question_type(
    "geo.condensation_forms_application",
    display_name={"th": "อธิบายน้ำค้าง หมอก และน้ำค้างแข็งในชีวิตจริง"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=CONDENSATION_TOPIC,
)
class CondensationFormsApplication(QuestionType):
    """Dew on a windscreen, frost on a mountain, fog that lifts by mid-morning."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, CONDENSATION_SCENARIOS,
            hint="ถามว่าอากาศหรือผิววัตถุเย็นลงเท่าใด และเกิดที่ใด",
        ), CONDENSATION_TOPIC)
