"""การเปลี่ยนพลังงานทดแทนเป็นพลังงานไฟฟ้า ประสิทธิภาพ และความคุ้มค่า

ฟิสิกส์ · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.5/2

Sets moved here from: science_wave_e13.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e13 import SUBJECT, UPPER_FIVE, _labelled, _numeric, show

PROVENANCE = Provenance("original")


TOPIC_RENEWABLE = "การเปลี่ยนพลังงานทดแทนเป็นพลังงานไฟฟ้า ประสิทธิภาพ และความคุ้มค่า"


class Plant(NamedTuple):
    name: str
    source: str          # the energy the plant starts from
    chain: str           # the whole conversion
    suits: str           # a place it suits


PLANTS: tuple[Plant, ...] = (
    Plant("เซลล์สุริยะ", "พลังงานแสง", "พลังงานแสง → พลังงานไฟฟ้า",
          "หลังคาบ้านที่ได้รับแสงแดดตลอดวัน"),
    Plant("โรงไฟฟ้าพลังงานลม", "พลังงานจลน์ของลม", "พลังงานจลน์ของลม → พลังงานจลน์ของกังหัน → พลังงานไฟฟ้า",
          "ชายฝั่งทะเลหรือสันเขาที่มีลมพัดแรงสม่ำเสมอ"),
    Plant("โรงไฟฟ้าพลังน้ำจากเขื่อน", "พลังงานศักย์โน้มถ่วงของน้ำ",
          "พลังงานศักย์โน้มถ่วงของน้ำ → พลังงานจลน์ของน้ำและกังหัน → พลังงานไฟฟ้า",
          "หุบเขาที่มีแม่น้ำและกักเก็บน้ำไว้ในที่สูงได้"),
    Plant("โรงไฟฟ้าพลังงานความร้อนใต้พิภพ", "พลังงานความร้อนใต้พิภพ",
          "พลังงานความร้อนใต้พิภพ → พลังงานจลน์ของไอน้ำและกังหัน → พลังงานไฟฟ้า",
          "บริเวณที่มีบ่อน้ำพุร้อน"),
    Plant("โรงไฟฟ้าชีวมวล", "พลังงานเคมีในชีวมวล",
          "พลังงานเคมีในชีวมวล → พลังงานความร้อน → พลังงานจลน์ของกังหัน → พลังงานไฟฟ้า",
          "ชุมชนเกษตรที่มีแกลบหรือชานอ้อยเหลือทิ้งจำนวนมาก"),
    Plant("โรงไฟฟ้าพลังงานน้ำขึ้นน้ำลง", "พลังงานจลน์และพลังงานศักย์ของน้ำทะเลขึ้นลง",
          "พลังงานของน้ำทะเลที่ขึ้นลง → พลังงานจลน์ของกังหัน → พลังงานไฟฟ้า",
          "ปากอ่าวที่ระดับน้ำขึ้นลงต่างกันมาก"),
)


# (device, input power in W, useful output in W) for efficiency, and pairs of
# lamps with the same brightness for cost.
LAMPS = (("หลอดไส้", 60), ("หลอดฟลูออเรสเซนต์", 18), ("หลอด LED", 9))


@question_type(
    "phys.renewable_energy_foundation",
    display_name={"th": "การเปลี่ยนพลังงานทดแทนเป็นพลังงานไฟฟ้า"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_RENEWABLE,
)
class RenewableEnergyFoundation(QuestionType):
    """The first outcome: which energy each renewable plant turns into electricity, and how."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        plant = rng.choice(PLANTS)
        hint = "ไล่ตั้งแต่พลังงานที่ธรรมชาติให้มา ผ่านการหมุนกังหัน (ถ้ามี) จนเป็นพลังงานไฟฟ้า"
        if rng.random() < 0.5:
            return _labelled(
                stem=f"{plant.name}เปลี่ยนพลังงานรูปใดเป็นพลังงานไฟฟ้าเป็นหลัก",
                correct=plant.source,
                wrongs=tuple([p.source for p in PLANTS if p != plant]),
                topic=TOPIC_RENEWABLE, hint=hint)
        return _labelled(
            stem=f"ข้อใดแสดงการเปลี่ยนพลังงานใน{plant.name}ได้ถูกต้อง",
            correct=plant.chain,
            wrongs=tuple([p.chain for p in PLANTS if p != plant]),
            topic=TOPIC_RENEWABLE, hint=hint)


@question_type(
    "phys.renewable_energy_fluency",
    display_name={"th": "ประสิทธิภาพและความคุ้มค่าของเทคโนโลยีด้านพลังงาน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_RENEWABLE,
)
class RenewableEnergyFluency(QuestionType):
    """The second outcome, judged by numbers: efficiency, payback, and running cost."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        if shape == 0:
            given = rng.choice((100, 200, 250, 400, 500, 1000))
            # Only percentages that leave a whole number of joules.
            pct = rng.choice([p for p in (15, 20, 25, 30, 40, 60, 75, 80, 90) if given * p % 100 == 0])
            useful = given * pct // 100
            device = rng.choice(("แผงเซลล์สุริยะ", "มอเตอร์ไฟฟ้า", "กังหันลม", "เครื่องกำเนิดไฟฟ้า"))
            return _numeric(
                stem=(f"{device}ได้รับพลังงาน {given} จูลต่อวินาที และให้พลังงานที่ใช้ประโยชน์ได้ "
                      f"{useful} จูลต่อวินาที มีประสิทธิภาพร้อยละเท่าใด"),
                answer=pct, wrongs=[100 - pct, Fraction(given, useful) * 10, useful],
                unit="เปอร์เซ็นต์", topic=TOPIC_RENEWABLE,
                hint="ประสิทธิภาพ = (พลังงานที่ใช้ประโยชน์ได้ ÷ พลังงานที่ได้รับ) × 100")
        if shape == 1:
            saving = rng.choice((1_000, 1_500, 2_000, 2_500, 3_000, 4_000, 5_000))
            years = rng.randint(3, 12)
            cost = saving * years
            return _numeric(
                stem=(f"ติดตั้งแผงเซลล์สุริยะบนหลังคาบ้านราคา {cost:,} บาท ช่วยลดค่าไฟฟ้าได้ปีละ "
                      f"{saving:,} บาท ต้องใช้เวลากี่ปีจึงจะคืนทุน"),
                answer=years, wrongs=[years * 2, years + 1, years - 1], unit="ปี",
                topic=TOPIC_RENEWABLE,
                hint="ระยะเวลาคืนทุน = เงินลงทุน ÷ เงินที่ประหยัดได้ต่อปี")
        (a, pa), (b, pb) = rng.sample(LAMPS, 2)
        hours = rng.choice((1_000, 2_000, 5_000, 10_000))
        rate = rng.choice((4, 5))
        cost_a = Fraction(pa * hours, 1000) * rate
        cost_b = Fraction(pb * hours, 1000) * rate
        cheaper = a if cost_a < cost_b else b
        return _labelled(
            stem=(f"{a}กำลังไฟฟ้า {pa} วัตต์ และ{b}กำลังไฟฟ้า {pb} วัตต์ ให้ความสว่างเท่ากัน "
                  f"ถ้าเปิดใช้ {hours:,} ชั่วโมง และค่าไฟฟ้าหน่วยละ {rate} บาท ข้อใดถูกต้อง"),
            correct=f"{cheaper}คุ้มค่ากว่า ประหยัดค่าไฟฟ้าได้ {show(abs(cost_a - cost_b))} บาท",
            wrongs=(f"{a if cheaper == b else b}คุ้มค่ากว่า ประหยัดค่าไฟฟ้าได้ {show(abs(cost_a - cost_b))} บาท",
                    # Forgetting to turn watt-hours into kilowatt-hours.
                    f"{cheaper}คุ้มค่ากว่า ประหยัดค่าไฟฟ้าได้ {show(abs(pa - pb) * hours * rate)} บาท",
                    "ค่าไฟฟ้าเท่ากัน เพราะให้ความสว่างเท่ากัน"),
            topic=TOPIC_RENEWABLE,
            hint="พลังงานไฟฟ้า (หน่วย) = กำลังไฟฟ้า (กิโลวัตต์) × เวลา (ชั่วโมง) แล้วคูณด้วยค่าไฟฟ้าต่อหน่วย")


@question_type(
    "phys.renewable_energy_application",
    display_name={"th": "เลือกพลังงานทดแทนและเทคโนโลยีให้เหมาะกับสถานการณ์"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_RENEWABLE,
)
class RenewableEnergyApplication(QuestionType):
    """Match a source to a place, and weigh a limitation against a fix."""

    LIMITS = (
        ("เซลล์สุริยะผลิตไฟฟ้าไม่ได้ในเวลากลางคืน", "ติดตั้งแบตเตอรี่เก็บพลังงานไฟฟ้าที่ผลิตได้ในเวลากลางวัน"),
        ("กังหันลมผลิตไฟฟ้าได้ไม่สม่ำเสมอเมื่อลมพัดไม่แรง", "ใช้ร่วมกับแหล่งพลังงานอื่นหรือระบบกักเก็บพลังงาน"),
        ("เขื่อนผลิตไฟฟ้าได้น้อยลงในหน้าแล้ง", "บริหารการปล่อยน้ำและใช้ร่วมกับแหล่งพลังงานอื่น"),
        ("โรงไฟฟ้าชีวมวลต้องใช้เชื้อเพลิงต่อเนื่อง", "ตั้งโรงไฟฟ้าใกล้แหล่งวัสดุเหลือทิ้งทางการเกษตร"),
    )

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            plant = rng.choice(PLANTS)
            return _labelled(
                stem=f"พื้นที่ใดเหมาะกับการสร้าง{plant.name}มากที่สุด",
                correct=plant.suits,
                wrongs=tuple([p.suits for p in PLANTS if p != plant]),
                topic=TOPIC_RENEWABLE,
                hint="แหล่งพลังงานทดแทนต้องมีอยู่มากและสม่ำเสมอในพื้นที่นั้น")
        problem, fix = rng.choice(self.LIMITS)
        return _labelled(
            stem=f"\"{problem}\" วิธีใดช่วยแก้ปัญหานี้ได้เหมาะสมที่สุด",
            correct=fix,
            wrongs=tuple([f for p, f in self.LIMITS if f != fix]
                                    + ["เลิกใช้พลังงานทดแทนทั้งหมด"]),
            topic=TOPIC_RENEWABLE,
            hint="พลังงานทดแทนหลายชนิดผลิตได้ไม่ต่อเนื่อง ทางแก้คือกักเก็บพลังงานหรือใช้หลายแหล่งร่วมกัน")
