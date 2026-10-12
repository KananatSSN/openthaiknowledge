"""สมบัติของธาตุโลหะ อโลหะ และกึ่งโลหะ

เคมี · ม.1 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.1/1

Sets moved here from: science_wave_d7.
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
from otk.sets._support.science_wave_c23 import Part
from otk.sets._support.science_wave_c24 import parts_item
from otk.sets._support.science_wave_d1 import SUBJECT
from otk.sets._support.science_wave_d7 import METAL, METALLOID, NONMETAL, SECONDARY_ONE

PROVENANCE = Provenance("original")


CLASSES_TOPIC = "สมบัติของธาตุโลหะ อโลหะ และกึ่งโลหะ"


KINDS = (METAL, NONMETAL, METALLOID)


class Element(NamedTuple):
    name: str
    kind: str
    look: str


ELEMENTS = (
    Element("ทองแดง", METAL, "ของแข็งสีแดงส้ม ผิวมันวาว"),
    Element("เหล็ก", METAL, "ของแข็งสีเทาเงิน ผิวมันวาว"),
    Element("อะลูมิเนียม", METAL, "ของแข็งสีเงิน ผิวมันวาว"),
    Element("สังกะสี", METAL, "ของแข็งสีเทาอมฟ้า ผิวมันวาว"),
    Element("กำมะถัน", NONMETAL, "ของแข็งสีเหลือง ผิวไม่มันวาว"),
    Element("ฟอสฟอรัสแดง", NONMETAL, "ผงของแข็งสีแดงคล้ำ ผิวไม่มันวาว"),
    Element("ซิลิคอน", METALLOID, "ของแข็งสีเทาเข้ม ผิวมันวาวเล็กน้อย"),
    Element("โบรอน", METALLOID, "ของแข็งสีดำ ผิวมันวาวเล็กน้อย"),
    Element("เจอร์เมเนียม", METALLOID, "ของแข็งสีเทาเงิน ผิวมันวาว"),
)


# What each class shows in the two tests every ม.1 laboratory runs.
TESTS = {
    METAL: ("หลอดไฟสว่างมาก", "ตีแล้วแผ่ออกเป็นแผ่นบาง ไม่แตก"),
    NONMETAL: ("หลอดไฟไม่สว่าง", "ตีแล้วแตกเป็นผง"),
    METALLOID: ("หลอดไฟสว่างเล็กน้อย", "ตีแล้วแตกเป็นชิ้น"),
}


def tested(element: Element) -> str:
    lamp, hammer = TESTS[element.kind]
    return f"{element.name}: {element.look} ต่อในวงจรแล้ว{lamp} {hammer}"


def _grouping(groups: dict[str, list[str]]) -> str:
    return " / ".join(f"{kind}: {', '.join(groups[kind]) or 'ไม่มี'}" for kind in KINDS)


CLASS_PARTS = (
    Part(METAL, "นำไฟฟ้าได้ดี และตีแผ่เป็นแผ่นบางได้โดยไม่แตก",
         "ไม่นำไฟฟ้า และตีแล้วแตกเป็นผง"),
    Part(NONMETAL, "ไม่นำไฟฟ้า และเปราะ ตีแล้วแตก",
         "นำไฟฟ้าได้ดี และตีแผ่เป็นแผ่นบางได้"),
    Part(METALLOID, "นำไฟฟ้าได้เล็กน้อย และเปราะ ตีแล้วแตก",
         "นำไฟฟ้าได้ดีเท่าโลหะ และตีแผ่เป็นแผ่นบางได้"),
)


CLASSES_SCENARIOS = (
    ("เหตุใดชิปคอมพิวเตอร์จึงนิยมทำจากซิลิคอนแทนทองแดง",
     "ซิลิคอนเป็นกึ่งโลหะที่นำไฟฟ้าได้เล็กน้อย จึงควบคุมการไหลของกระแสไฟฟ้าในชิปได้",
     ("ซิลิคอนนำไฟฟ้าได้ดีกว่าทองแดงมาก",
      "ซิลิคอนเป็นอโลหะที่ไม่นำไฟฟ้าเลย",
      "ซิลิคอนตีแผ่เป็นแผ่นบางได้ดีกว่าทองแดง",
      "ซิลิคอนเป็นโลหะที่ตีแผ่ได้ดีที่สุด",
      "ซิลิคอนเป็นของเหลวจึงไหลไปทั่วชิปได้")),
    ("นักเรียนพบธาตุชนิดหนึ่งผิวมันวาว แต่ตีแล้วแตกเป็นชิ้น และนำไฟฟ้าได้เล็กน้อย ควรจัดธาตุนี้ไว้กลุ่มใด เพราะเหตุใด",
     "กึ่งโลหะ เพราะแม้ผิวจะมันวาวเหมือนโลหะ แต่เปราะและนำไฟฟ้าได้เพียงเล็กน้อย",
     ("โลหะ เพราะผิวมันวาว",
      "อโลหะ เพราะนำไฟฟ้าได้",
      "จัดกลุ่มไม่ได้ เพราะมีสมบัติไม่ครบ",
      "โลหะ เพราะนำไฟฟ้าได้",
      "อโลหะ เพราะตีแล้วแตก")),
    ("ข้อมูลจากแหล่งสารสนเทศระบุว่าปรอทเป็นโลหะ แต่ปรอทเป็นของเหลวที่อุณหภูมิห้อง นักเรียนควรสรุปอย่างไร",
     "ปรอทยังเป็นโลหะเพราะผิวมันวาวและนำไฟฟ้าได้ดี สถานะของเหลวเป็นข้อยกเว้นของโลหะ",
     ("ปรอทเป็นอโลหะ เพราะโลหะทุกชนิดต้องเป็นของแข็ง",
      "ปรอทเป็นกึ่งโลหะ เพราะเป็นของเหลว",
      "ข้อมูลผิด เพราะของเหลวนำไฟฟ้าไม่ได้",
      "ปรอทเป็นอโลหะ เพราะเป็นของเหลว",
      "ปรอทไม่ใช่ธาตุ เพราะธาตุต้องเป็นของแข็ง")),
    ("เหตุใดสายไฟฟ้าในบ้านจึงใช้ทองแดงเป็นลวดตัวนำ",
     "ทองแดงเป็นโลหะที่นำไฟฟ้าได้ดี และดึงเป็นเส้นลวดได้โดยไม่แตก",
     ("ทองแดงเป็นกึ่งโลหะที่นำไฟฟ้าได้เล็กน้อย",
      "ทองแดงเป็นอโลหะที่ไม่นำไฟฟ้า จึงปลอดภัย",
      "ทองแดงเปราะจึงตัดเป็นท่อนได้ง่าย",
      "ทองแดงไม่มีผิวมันวาวจึงไม่สะท้อนแสง",
      "ทองแดงนำไฟฟ้าได้น้อยที่สุดในบรรดาโลหะ")),
    ("กำมะถันผงสีเหลืองตีแล้วแตกเป็นผงและไม่นำไฟฟ้า ใช้ทำยาฆ่าเชื้อราและผสมในยาง ควรจัดกำมะถันเป็นกลุ่มใด เพราะเหตุใด",
     "อโลหะ เพราะไม่มันวาว เปราะ และไม่นำไฟฟ้า",
     ("โลหะ เพราะนำไปใช้งานได้หลายอย่าง",
      "กึ่งโลหะ เพราะเป็นผง",
      "โลหะ เพราะมีสีเหลืองเหมือนทองคำ",
      "กึ่งโลหะ เพราะนำไฟฟ้าได้เล็กน้อย",
      "จัดกลุ่มไม่ได้ เพราะไม่ใช่ของเหลว")),
)


@question_type(
    "chem.element_class_group_foundation",
    display_name={"th": "จัดกลุ่มธาตุเป็นโลหะ อโลหะ และกึ่งโลหะจากผลการทดสอบ"},
    level=SECONDARY_ONE, subject=SUBJECT, topic=CLASSES_TOPIC,
)
class ElementClassGroupFoundation(QuestionType):
    """Five elements' test results; place every one in its class."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        chosen = [rng.choice([e for e in ELEMENTS if e.kind == kind]) for kind in KINDS]
        rest = [e for e in ELEMENTS if e not in chosen]
        chosen += rng.sample(rest, 2)
        rng.shuffle(chosen)
        groups = {kind: [e.name for e in chosen if e.kind == kind] for kind in KINDS}
        wrongs = []
        # Each wrong grouping moves exactly one element into another class.
        for element in rng.sample(chosen, 3):
            target = rng.choice([k for k in KINDS if k != element.kind])
            moved = {kind: [n for n in names if n != element.name] for kind, names in groups.items()}
            moved[target].append(element.name)
            wrongs.append(_grouping(moved))
        # Spares move two elements at once, so the answer is not the grouping
        # every wrong differs from by a single move.
        for pair in (rng.sample(chosen, 2) for _ in range(2)):
            moved = {kind: [n for n in names if n not in {e.name for e in pair}] for kind, names in groups.items()}
            for element in pair:
                moved[rng.choice([k for k in KINDS if k != element.kind])].append(element.name)
            wrongs.append(_grouping(moved))
        wrongs = list(dict.fromkeys(wrongs))
        return _labelled(
            stem=(f"นักเรียนทดสอบธาตุ 5 ชนิด ได้ผลดังนี้ — {' / '.join(tested(e) for e in chosen)} "
                  "จากผลการทดสอบ ข้อใดจัดกลุ่มธาตุได้ถูกต้อง"),
            correct=_grouping(groups),
            wrongs=tuple(wrongs),
            hint="โลหะนำไฟฟ้าได้ดีและตีแผ่ได้ อโลหะไม่นำไฟฟ้าและเปราะ กึ่งโลหะนำไฟฟ้าได้เล็กน้อยและเปราะ",
            topic=CLASSES_TOPIC,
        )


@question_type(
    "chem.element_class_group_fluency",
    display_name={"th": "อธิบายสมบัติทางกายภาพของธาตุโลหะ อโลหะ และกึ่งโลหะจากหลักฐาน"},
    level=SECONDARY_ONE, subject=SUBJECT, topic=CLASSES_TOPIC,
)
class ElementClassGroupFluency(QuestionType):
    """One element per class tested; explain every class's properties together."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        chosen = [rng.choice([e for e in ELEMENTS if e.kind == kind]) for kind in KINDS]
        rng.shuffle(chosen)
        record = " / ".join(f"{tested(e)} ({e.kind})" for e in chosen)
        return parts_item(
            rng, CLASS_PARTS,
            stem=(f"ผลการทดสอบธาตุที่ทราบกลุ่มแล้วเป็นดังนี้ — {record} "
                  "จากหลักฐานนี้ ข้อใดอธิบายสมบัติทางกายภาพของธาตุแต่ละกลุ่มได้ถูกต้องทั้งหมด"),
            hint="อ่านผลของธาตุแต่ละกลุ่มทีละข้อ ข้อที่ผิดจะอธิบายผิดอย่างน้อยหนึ่งกลุ่ม",
            topic=CLASSES_TOPIC,
        )


@question_type(
    "chem.element_class_group_application",
    display_name={"th": "ใช้สมบัติของโลหะ อโลหะ และกึ่งโลหะอธิบายการใช้งาน"},
    level=SECONDARY_ONE, subject=SUBJECT, topic=CLASSES_TOPIC,
)
class ElementClassGroupApplication(QuestionType):
    """Silicon chips, a shiny but brittle element, and liquid mercury."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, CLASSES_SCENARIOS,
            hint="ใช้สมบัติหลายด้านร่วมกัน ทั้งความมันวาว การนำไฟฟ้า และความเปราะ",
        ), CLASSES_TOPIC)
