"""ประโยชน์ของการนำวัสดุที่ใช้แล้วกลับมาใช้ใหม่

เคมี · ป.2 · สสวท. พื้นฐาน
Indicators: ว 2.1 ป.2/4

Sets moved here from: science_wave_d2.
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
from otk.sets._support.science_wave_d1 import SECOND, SUBJECT

PROVENANCE = Provenance("original")


REUSE_TOPIC = "ประโยชน์ของการนำวัสดุที่ใช้แล้วกลับมาใช้ใหม่"


BENEFITS = (
    "ช่วยลดปริมาณขยะ",
    "ช่วยประหยัดเงินที่ต้องซื้อของใหม่",
    "ช่วยลดการใช้ทรัพยากรธรรมชาติในการผลิตของใหม่",
    "ช่วยลดพลังงานที่ใช้ในการผลิตของใหม่",
    "ช่วยให้ของที่ยังใช้ได้ไม่ถูกทิ้งไปโดยเปล่าประโยชน์",
)


NOT_BENEFITS = (
    "ทำให้มีขยะเพิ่มขึ้น",
    "ทำให้ต้องซื้อของใหม่บ่อยขึ้น",
    "ทำให้ต้องตัดต้นไม้มาผลิตของมากขึ้น",
    "ทำให้วัสดุที่ใช้แล้วกลายเป็นวัสดุชนิดใหม่เสมอ",
    "ทำให้ต้องใช้พลังงานผลิตของใหม่มากขึ้น",
    "ทำให้ถังขยะเต็มเร็วขึ้น",
)


class Choice(NamedTuple):
    situation: str
    reuse: str
    wrongs: tuple[str, ...]


CHOICES = (
    Choice("นักเรียนมีกระดาษรายงานที่ใช้ไปเพียงหน้าเดียวหลายแผ่น",
           "ใช้หน้าที่ยังว่างเป็นกระดาษทดเลข",
           ("ทิ้งลงถังขยะทันที", "เผาทิ้งหลังบ้าน", "ซื้อสมุดทดเลขเล่มใหม่แล้วทิ้งกระดาษเหล่านั้น",
            "ขยำเป็นก้อนแล้วโยนเล่นจนทิ้ง", "ฉีกเป็นชิ้นเล็กแล้วทิ้งลงถังขยะ")),
    Choice("หลังงานวันเกิด มีแก้วพลาสติกแบบหนาที่ล้างแล้วเหลืออยู่หลายใบ",
           "ล้างให้สะอาดแล้วใช้เป็นถ้วยเพาะต้นกล้า",
           ("ทิ้งรวมกับเศษอาหาร", "ฝังดินในสวน", "เผาเพื่อลดปริมาณขยะ",
            "ทิ้งลงแม่น้ำหลังบ้าน", "ซื้อแก้วใหม่มาใช้ทุกครั้งแล้วทิ้งแก้วเก่า")),
    Choice("บ้านของนักเรียนมีขวดโหลแก้วที่ใส่แยมหมดแล้ว",
           "ล้างให้สะอาดแล้วใช้ใส่กระดุมหรือของชิ้นเล็ก",
           ("ทุบขวดโหลให้แตกเป็นชิ้นเล็กแล้วทิ้งลงถังขยะ", "ทิ้งลงถังขยะเปียก", "ซื้อกล่องใหม่มาใส่ของแล้วทิ้งขวดโหล",
            "ทิ้งรวมกับถุงขยะเศษอาหาร", "ขว้างทิ้งในที่รกร้างหลังบ้านเพื่อไม่ให้รกบ้าน")),
    Choice("โรงเรียนมีเสื้อพละเก่าที่ขาดเล็กน้อยจำนวนมาก",
           "ตัดเป็นผ้าเช็ดโต๊ะหรือผ้าถูพื้นในห้องเรียน",
           ("ทิ้งรวมกับขยะทั่วไป", "เผาทิ้งในสนาม", "ซื้อผ้าถูพื้นใหม่แล้วทิ้งเสื้อเก่าทั้งหมด",
            "ฝังดินในสนามโรงเรียน", "เก็บไว้ในห้องเก็บของโดยไม่ได้ใช้จนผ้าผุขาดไปเอง")),
    Choice("บ้านของนักเรียนมีกล่องรองเท้ากระดาษที่ยังแข็งแรงหลายใบ",
           "ใช้เป็นกล่องเก็บของเล่นหรือเครื่องเขียน",
           ("ทิ้งลงถังขยะทันที", "เผาทิ้งหลังบ้าน", "ซื้อกล่องพลาสติกใหม่แล้วทิ้งกล่องรองเท้า",
            "ฉีกเป็นชิ้นเล็กแล้วทิ้ง", "ทิ้งลงคลองข้างบ้าน")),
    Choice("บ้านของนักเรียนมีขวดน้ำพลาสติกหนาที่ดื่มหมดแล้ว",
           "ล้างให้สะอาดแล้วตัดเป็นกระถางปลูกต้นไม้",
           ("ทิ้งลงถังขยะทันที", "เผาทิ้งหลังบ้าน", "ทิ้งลงคลองข้างบ้าน",
            "ซื้อกระถางใหม่มาปลูกต้นไม้แล้วทิ้งขวดไป", "บีบให้แบนแล้วทิ้งรวมกับเศษอาหารในถังเดียวกัน")),
)


REUSE_SCENARIOS = (
    ("ห้องเรียนหนึ่งเริ่มนำกระดาษหน้าเดียวกลับมาใช้ทดเลข หลังผ่านไปหนึ่งเดือน ข้อใดน่าจะเกิดขึ้น",
     "ขยะกระดาษในห้องลดลง และห้องเรียนซื้อกระดาษใหม่น้อยลง",
     ("ขยะกระดาษในห้องเพิ่มขึ้นเป็นสองเท่า",
      "ห้องเรียนต้องซื้อกระดาษใหม่มากขึ้น",
      "กระดาษหน้าเดียวกลายเป็นพลาสติก",
      "ครูต้องทิ้งกระดาษเพิ่มขึ้นทุกวัน",
      "กระดาษหน้าเดียวหายไปจากห้องทั้งหมด")),
    ("นักเรียนสองคนมีขวดพลาสติกคนละ 10 ขวด คนแรกทิ้งทั้งหมด คนที่สองนำ 6 ขวดไปทำกระถางต้นไม้และทิ้ง 4 ขวด คนที่สองทิ้งขยะขวดพลาสติกน้อยกว่าคนแรกกี่ขวด",
     "6 ขวด",
     ("4 ขวด", "10 ขวด", "16 ขวด", "20 ขวด", "2 ขวด")),
    ("ข้อใดแสดงว่านักเรียนเห็นคุณค่าของการนำวัสดุที่ใช้แล้วกลับมาใช้ใหม่",
     "เก็บกล่องกระดาษที่ยังแข็งแรงไว้ใช้ใส่ของแทนการซื้อกล่องใหม่",
     ("ทิ้งกล่องกระดาษทุกใบทันทีที่แกะของออก",
      "ซื้อกล่องใหม่ทุกครั้งแม้มีกล่องเก่าที่ยังใช้ได้",
      "เผากล่องกระดาษเก่าเพื่อให้บ้านสะอาด",
      "ทิ้งกล่องกระดาษลงแม่น้ำ",
      "ใช้กล่องกระดาษครั้งเดียวแล้วเผา")),
)


# (used thing, unit, what the second learner made of some of them)
KEPT = (("ขวดพลาสติก", "ขวด", "กระถางต้นไม้"), ("กล่องนม", "กล่อง", "ที่ใส่ดินสอ"),
        ("กระป๋อง", "ใบ", "กระถางต้นไม้"), ("ถุงพลาสติก", "ใบ", "ถุงใส่ขยะ"))


def kept_out(rng: Random) -> GeneratedQuestion:
    """How many fewer used things end up in the bin when some are reused."""
    thing, unit, made = rng.choice(KEPT)
    total = rng.randint(8, 20)
    reused = rng.choice([k for k in range(2, total - 1) if 2 * k != total])
    pool = (total - reused, total, total + reused, 2 * total - reused, reused + 1)
    return _labelled(
        stem=(f"นักเรียนสองคนมี{thing}คนละ {total} {unit} คนแรกทิ้งทั้งหมด คนที่สองนำ {reused} {unit}ไปทำ{made} "
              f"และทิ้ง {total - reused} {unit} คนที่สองทิ้งขยะ{thing}น้อยกว่าคนแรกกี่{unit}"),
        correct=f"{reused} {unit}",
        wrongs=tuple(dict.fromkeys(f"{w} {unit}" for w in pool if w != reused)),
        hint="ขยะที่ลดลงเท่ากับจำนวนที่นำกลับมาใช้ใหม่",
        topic=REUSE_TOPIC,
    )


@question_type(
    "chem.reuse_benefit_foundation",
    display_name={"th": "บอกประโยชน์ของการนำวัสดุที่ใช้แล้วกลับมาใช้ใหม่"},
    level=SECOND, subject=SUBJECT, topic=REUSE_TOPIC,
)
class ReuseBenefitFoundation(QuestionType):
    """One benefit of reusing materials, among things that are not benefits."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _labelled(
            stem="ข้อใดเป็นประโยชน์ของการนำวัสดุที่ใช้แล้วกลับมาใช้ใหม่",
            correct=rng.choice(BENEFITS),
            wrongs=tuple(NOT_BENEFITS),
            hint="นึกว่าถ้าไม่ทิ้งของแต่นำกลับมาใช้อีก ขยะและการซื้อของใหม่จะเปลี่ยนไปอย่างไร",
            topic=REUSE_TOPIC,
        )


@question_type(
    "chem.reuse_benefit_fluency",
    display_name={"th": "เลือกวิธีนำวัสดุที่ใช้แล้วกลับมาใช้ใหม่ในชีวิตประจำวัน"},
    level=SECOND, subject=SUBJECT, topic=REUSE_TOPIC,
)
class ReuseBenefitFluency(QuestionType):
    """A situation with used materials; the action that reuses them."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        choice = rng.choice(CHOICES)
        return _labelled(
            stem=f"{choice.situation} ข้อใดเป็นการนำวัสดุที่ใช้แล้วกลับมาใช้ใหม่",
            correct=choice.reuse,
            wrongs=choice.wrongs,
            hint="การนำกลับมาใช้ใหม่คือการใช้ของชิ้นเดิมอีกครั้ง ไม่ใช่ทิ้งหรือซื้อใหม่",
            topic=REUSE_TOPIC,
        )


@question_type(
    "chem.reuse_benefit_application",
    display_name={"th": "วิเคราะห์ผลของการนำวัสดุที่ใช้แล้วกลับมาใช้ใหม่"},
    level=SECOND, subject=SUBJECT, topic=REUSE_TOPIC,
)
class ReuseBenefitApplication(QuestionType):
    """A class reusing paper, counting bottles kept out of the bin, and valuing reuse."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            return kept_out(rng)
        return _retopic(scenario_question(
            rng, REUSE_SCENARIOS,
            hint="เปรียบเทียบขยะและการซื้อของใหม่ ระหว่างทิ้งกับนำกลับมาใช้ใหม่",
        ), REUSE_TOPIC)
