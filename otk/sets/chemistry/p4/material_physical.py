"""สมบัติทางกายภาพของวัสดุ

เคมี · ป.4 · สสวท. พื้นฐาน
Indicators: ว 2.1 ป.4/1

Sets moved here from: science_wave_d4.
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
from otk.sets._support.science_wave_d4 import FOURTH

PROVENANCE = Provenance("original")


PROPERTIES_TOPIC = "สมบัติทางกายภาพของวัสดุ"


class Material(NamedTuple):
    name: str
    hardness: int      # 3 metal, 2 wood or hard plastic, 1 rubber
    elastic: bool
    conducts: bool     # heat and electricity alike, at this level


MATERIALS = (
    Material("แท่งเหล็ก", 3, False, True),
    Material("แท่งทองแดง", 3, False, True),
    Material("แท่งอะลูมิเนียม", 3, False, True),
    Material("แท่งไม้", 2, False, False),
    Material("แท่งพลาสติกแข็ง", 2, False, False),
    Material("แท่งยาง", 1, True, False),
)


def comparison(a: Material, b: Material) -> tuple[Part, ...]:
    """Every property compared for a pair that differs in hardness."""
    hard, soft = (a, b) if a.hardness > b.hardness else (b, a)
    parts = [Part("ความแข็ง", f"{hard.name}แข็งกว่า{soft.name}", f"{soft.name}แข็งกว่า{hard.name}")]
    if a.elastic != b.elastic:
        el, other = (a, b) if a.elastic else (b, a)
        parts.append(Part("สภาพยืดหยุ่น", f"{el.name}มีสภาพยืดหยุ่นมากกว่า{other.name}",
                          f"{other.name}มีสภาพยืดหยุ่นมากกว่า{el.name}"))
    else:
        parts.append(Part("สภาพยืดหยุ่น", "ไม่มีสภาพยืดหยุ่นทั้งคู่", f"{a.name}มีสภาพยืดหยุ่นมากกว่า{b.name}"))
    for label, verb in (("การนำความร้อน", "นำความร้อน"), ("การนำไฟฟ้า", "นำไฟฟ้า")):
        if a.conducts != b.conducts:
            yes, no = (a, b) if a.conducts else (b, a)
            parts.append(Part(label, f"{yes.name}{verb}ได้ดีกว่า{no.name}", f"{no.name}{verb}ได้ดีกว่า{yes.name}"))
        elif a.conducts:
            parts.append(Part(label, f"{verb}ได้ดีทั้งคู่", f"{b.name}{verb}ไม่ได้"))
        else:
            parts.append(Part(label, f"{verb}ได้ไม่ดีทั้งคู่", f"{a.name}{verb}ได้ดีกว่า{b.name}"))
    return tuple(parts)


def record(a: Material, b: Material, rng: Random) -> str:
    """What the four tests showed, as a ป.4 notebook would put it."""
    hard, soft = (a, b) if a.hardness > b.hardness else (b, a)
    lines = [f"นำมาขูดกัน {soft.name}เกิดรอยขูด แต่{hard.name}ไม่เกิดรอย"]
    bend = {True: "กลับสู่รูปเดิม", False: "ไม่กลับสู่รูปเดิม"}
    lines.append(f"ดัดแล้วปล่อย {a.name}{bend[a.elastic]} และ{b.name}{bend[b.elastic]}")
    fast = rng.randint(1, 2)
    heat = {True: f"ปลายอีกด้านร้อนภายใน {fast} นาที", False: "ปลายอีกด้านยังไม่ร้อนหลัง 10 นาที"}
    lines.append(f"จุ่มปลายหนึ่งในน้ำร้อน {a.name}{heat[a.conducts]} ส่วน{b.name}{heat[b.conducts]}")
    lamp = {True: "หลอดไฟสว่าง", False: "หลอดไฟไม่สว่าง"}
    lines.append(f"ต่อเข้าในวงจรไฟฟ้า เมื่อใช้{a.name}{lamp[a.conducts]} เมื่อใช้{b.name}{lamp[b.conducts]}")
    return " / ".join(lines)


def pairs() -> list[tuple[Material, Material]]:
    return [(a, b) for a in MATERIALS for b in MATERIALS if a.hardness > b.hardness]


class Design(NamedTuple):
    part: str
    need: str
    material: str
    wrongs: tuple[str, ...]


DESIGNS = (
    Design("ด้ามจับของหม้อต้มน้ำ", "นำความร้อนได้ไม่ดี", "ไม้",
           ("อะลูมิเนียม เพราะนำความร้อนได้ดี", "ทองแดง เพราะนำไฟฟ้าได้ดี", "เหล็ก เพราะแข็ง",
            "ยาง เพราะมีสภาพยืดหยุ่น", "ทองแดง เพราะนำความร้อนได้ดี")),
    Design("ก้นหม้อต้มน้ำ", "นำความร้อนได้ดี", "อะลูมิเนียม",
           ("ไม้ เพราะนำความร้อนได้ไม่ดี", "ยาง เพราะมีสภาพยืดหยุ่น", "พลาสติก เพราะไม่นำไฟฟ้า",
            "พลาสติก เพราะนำความร้อนได้ไม่ดี", "ยาง เพราะไม่นำไฟฟ้า")),
    Design("แกนกลางของสายไฟ", "นำไฟฟ้าได้ดี", "ทองแดง",
           ("พลาสติก เพราะไม่นำไฟฟ้า", "ไม้ เพราะนำความร้อนได้ไม่ดี", "ยาง เพราะมีสภาพยืดหยุ่น",
            "ยาง เพราะไม่นำไฟฟ้า", "ไม้ เพราะแข็ง")),
    Design("ส่วนหุ้มภายนอกของสายไฟ", "ไม่นำไฟฟ้า", "พลาสติก",
           ("ทองแดง เพราะนำไฟฟ้าได้ดี", "อะลูมิเนียม เพราะนำความร้อนได้ดี", "เหล็ก เพราะแข็ง",
            "เหล็ก เพราะนำไฟฟ้าได้ดี", "ทองแดง เพราะแข็ง")),
    Design("ขอบกันกระแทกรอบโทรศัพท์", "มีสภาพยืดหยุ่น", "ยาง",
           ("เหล็ก เพราะแข็ง", "ทองแดง เพราะนำไฟฟ้าได้ดี", "อะลูมิเนียม เพราะนำความร้อนได้ดี",
            "ไม้ เพราะแข็ง", "พลาสติกแข็ง เพราะไม่นำไฟฟ้า")),
    Design("หัวค้อนสำหรับตอกตะปู", "แข็ง", "เหล็ก",
           ("ยาง เพราะมีสภาพยืดหยุ่น", "พลาสติก เพราะไม่นำไฟฟ้า", "ไม้ เพราะนำความร้อนได้ไม่ดี",
            "อะลูมิเนียม เพราะนำความร้อนได้ดี", "ทองแดง เพราะนำไฟฟ้าได้ดี")),
    Design("สายรัดของที่ยืดแล้วหดกลับ", "มีสภาพยืดหยุ่นและหดกลับได้", "ยาง",
           ("เหล็ก เพราะแข็ง", "ทองแดง เพราะนำไฟฟ้าได้ดี", "ไม้ เพราะนำความร้อนได้ไม่ดี",
            "อะลูมิเนียม เพราะนำความร้อนได้ดี", "พลาสติกแข็ง เพราะไม่นำไฟฟ้า")),
    Design("ขาโต๊ะที่ต้องรับน้ำหนักมาก", "แข็งและไม่งอ", "เหล็ก",
           ("ยาง เพราะมีสภาพยืดหยุ่น", "พลาสติกนิ่ม เพราะไม่นำไฟฟ้า", "ทองแดง เพราะนำไฟฟ้าได้ดี",
            "อะลูมิเนียมฟอยล์ เพราะนำความร้อนได้ดี", "ฟองน้ำ เพราะนุ่ม")),
)


PROPERTIES_SCENARIOS = (
    ("นักเรียนออกแบบกระทะที่ทอดอาหารได้เร็วและจับได้ไม่ร้อนมือ ควรใช้วัสดุอย่างไร",
     "ตัวกระทะใช้โลหะที่นำความร้อนได้ดี ส่วนด้ามจับใช้ไม้หรือพลาสติกที่นำความร้อนได้ไม่ดี",
     ("ทั้งตัวกระทะและด้ามจับใช้โลหะ เพราะแข็งแรงที่สุด",
      "ตัวกระทะใช้ไม้ ส่วนด้ามจับใช้โลหะ",
      "ทั้งตัวกระทะและด้ามจับใช้ยาง เพราะมีสภาพยืดหยุ่น",
      "ตัวกระทะใช้พลาสติกที่นำความร้อนได้ดี ส่วนด้ามจับใช้ทองแดงที่นำความร้อนได้ไม่ดี",
      "ทั้งตัวกระทะและด้ามจับใช้ไม้ เพราะไม่นำความร้อน")),
    ("ช่างไฟฟ้าสวมถุงมือยางขณะซ่อมสายไฟ เพราะเหตุใด",
     "ยางไม่นำไฟฟ้า จึงช่วยป้องกันไม่ให้กระแสไฟฟ้าผ่านเข้าสู่ร่างกาย",
     ("ยางนำไฟฟ้าได้ดี จึงช่วยให้ซ่อมเร็วขึ้น",
      "ยางแข็งกว่าโลหะ จึงตัดสายไฟได้",
      "ยางนำความร้อนได้ดี จึงช่วยให้มืออุ่น",
      "ยางนำไฟฟ้าได้ดี กระแสไฟฟ้าจึงไหลผ่านถุงมือลงดินได้เร็ว ไม่ผ่านร่างกาย",
      "ยางมีสภาพยืดหยุ่นจึงทำให้สายไฟยาวขึ้นและซ่อมได้ง่าย")),
    ("นักเรียนต้องการทำที่รองแก้วที่วางแก้วน้ำร้อนแล้วโต๊ะไม่ร้อน และไม่ทำให้แก้วแตกเมื่อวางแรง ควรเลือกวัสดุใด",
     "แผ่นยาง เพราะนำความร้อนได้ไม่ดีและมีสภาพยืดหยุ่น",
     ("แผ่นทองแดง เพราะนำความร้อนได้ดี",
      "แผ่นอะลูมิเนียม เพราะแข็งและนำไฟฟ้าได้",
      "แผ่นเหล็ก เพราะแข็งที่สุด",
      "แผ่นกระจก เพราะแข็งและใส",
      "แผ่นอะลูมิเนียมฟอยล์ เพราะบางและเบา")),
    ("ของเล่นเด็กเล็กมักทำขอบด้วยยางหรือพลาสติกนิ่มแทนโลหะแข็ง เพราะเหตุใด",
     "ยางและพลาสติกนิ่มมีสภาพยืดหยุ่น เมื่อเด็กชนหรือทำตกจึงไม่เป็นอันตรายมาก",
     ("ยางแข็งกว่าโลหะ จึงแข็งแรงกว่าและไม่แตกหักเมื่อเด็กทำตก",
      "ยางนำไฟฟ้าได้ดี จึงปลอดภัยเมื่อเด็กเอาของเล่นไปเล่นใกล้ปลั๊กไฟ",
      "ยางนำความร้อนได้ดี จึงอุ่นมือ",
      "โลหะมีสภาพยืดหยุ่นมากกว่ายาง แต่ยางมีราคาถูกกว่าจึงเลือกใช้ยาง",
      "ยางไม่มีมวลจึงเบากว่าโลหะ")),
    ("หม้อหุงข้าวไฟฟ้าใช้โลหะทำหม้อด้านใน แต่ใช้พลาสติกทำตัวเครื่องด้านนอก เพราะเหตุใด",
     "โลหะนำความร้อนได้ดีจึงทำให้ข้าวสุก ส่วนพลาสติกนำความร้อนและไฟฟ้าได้ไม่ดี จึงจับตัวเครื่องได้ปลอดภัย",
     ("พลาสติกนำความร้อนได้ดีกว่าโลหะจึงใช้ทำด้านนอก ส่วนโลหะนำไฟฟ้าไม่ได้จึงใช้ทำหม้อด้านใน",
      "โลหะไม่นำไฟฟ้า จึงใช้ทำหม้อด้านใน",
      "ทั้งสองวัสดุนำความร้อนได้ดีเท่ากัน แต่พลาสติกราคาถูกกว่าจึงใช้ทำด้านนอกของหม้อหุงข้าว",
      "พลาสติกแข็งกว่าโลหะ จึงใช้ทำด้านนอก",
      "โลหะมีสภาพยืดหยุ่นจึงใส่ข้าวได้มาก")),
)


@question_type(
    "chem.material_physical_foundation",
    display_name={"th": "ระบุการนำสมบัติทางกายภาพของวัสดุไปใช้ในการออกแบบชิ้นงาน"},
    level=FOURTH, subject=SUBJECT, topic=PROPERTIES_TOPIC,
)
class MaterialPhysicalFoundation(QuestionType):
    """A part of a design; the material whose property that part needs."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        design = rng.choice(DESIGNS)
        return _labelled(
            stem=f"นักเรียนออกแบบ{design.part} ควรเลือกใช้วัสดุใด เพราะเหตุใด",
            correct=f"{design.material} เพราะ{design.need}",
            wrongs=design.wrongs,
            hint="ถามก่อนว่าชิ้นส่วนนี้ต้องทำหน้าที่อะไร แล้วเลือกวัสดุที่มีสมบัติตรงกับหน้าที่นั้น",
            topic=PROPERTIES_TOPIC,
        )


@question_type(
    "chem.material_physical_fluency",
    display_name={"th": "เปรียบเทียบความแข็ง สภาพยืดหยุ่น การนำความร้อน และการนำไฟฟ้าจากผลการทดลอง"},
    level=FOURTH, subject=SUBJECT, topic=PROPERTIES_TOPIC,
)
class MaterialPhysicalFluency(QuestionType):
    """Four tests on two materials; compare them on all four properties."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        a, b = rng.choice(pairs())
        if rng.random() < 0.5:
            a, b = b, a
        return parts_item(
            rng, comparison(a, b),
            stem=(f"นักเรียนทดสอบ{a.name}และ{b.name}ขนาดเท่ากัน ได้ผลดังนี้ — {record(a, b, rng)} "
                  "จากหลักฐานนี้ ข้อใดเปรียบเทียบสมบัติของวัสดุทั้งสองได้ถูกต้องทั้งหมด"),
            hint="อ่านผลการทดสอบทีละข้อ ข้อที่ผิดจะเปรียบเทียบผิดอย่างน้อยหนึ่งสมบัติ",
            topic=PROPERTIES_TOPIC,
        )


@question_type(
    "chem.material_physical_application",
    display_name={"th": "ใช้สมบัติทางกายภาพของวัสดุแก้ปัญหาในชีวิตประจำวัน"},
    level=FOURTH, subject=SUBJECT, topic=PROPERTIES_TOPIC,
)
class MaterialPhysicalApplication(QuestionType):
    """A frying pan, an electrician's gloves, and a coaster for a hot cup."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, PROPERTIES_SCENARIOS,
            hint="แยกหน้าที่ของแต่ละส่วนก่อน แล้วจับคู่กับสมบัติของวัสดุ",
        ), PROPERTIES_TOPIC)
