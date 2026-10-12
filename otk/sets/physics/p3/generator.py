"""การทำงานของเครื่องกำเนิดไฟฟ้าและแหล่งพลังงาน

ฟิสิกส์ · ป.3 · สสวท. พื้นฐาน
Indicators: ว 2.3 ป.3/2

Sets moved here from: science_wave_d23.
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
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d23 import THIRD

PROVENANCE = Provenance("original")


GENERATOR_TOPIC = "การทำงานของเครื่องกำเนิดไฟฟ้าและแหล่งพลังงาน"


GENERATOR_FACTS = (
    ("เครื่องกำเนิดไฟฟ้าทำงานอย่างไร", "เปลี่ยนพลังงานกลเป็นพลังงานไฟฟ้า โดยอาศัยการหมุนของขดลวดหรือแม่เหล็ก",
     ("เปลี่ยนพลังงานไฟฟ้าเป็นพลังงานกลโดยตรง ไม่มีการเปลี่ยนรูปพลังงานอื่น", "เก็บพลังงานไฟฟ้าไว้ใช้ในภายหลังโดยไม่มีการเปลี่ยนรูปพลังงาน",
      "เปลี่ยนพลังงานเคมีเป็นพลังงานไฟฟ้าโดยไม่ต้องมีการเคลื่อนที่ใด ๆ", "เปลี่ยนพลังงานเสียงเป็นพลังงานไฟฟ้า", "ผลิตไฟฟ้าได้เองโดยไม่ต้องมีสิ่งใดมาหมุน")),
    ("ส่วนประกอบสำคัญของเครื่องกำเนิดไฟฟ้าคืออะไร", "ขดลวดและแม่เหล็ก", ("หลอดไฟและสวิตช์", "ถ่านไฟฉายและสายไฟ", "ลำโพงและไมโครโฟน", "แผงโซลาร์เซลล์และแบตเตอรี่", "ใบพัดและเสา")),
    ("ข้อใดเป็นเครื่องกำเนิดไฟฟ้าขนาดเล็กที่พบในชีวิตประจำวัน", "ไดนาโมที่ติดกับล้อจักรยาน", ("ถ่านไฟฉาย", "หลอดไฟ", "ปลั๊กพ่วง", "สวิตช์ไฟ", "พัดลมตั้งโต๊ะ")),
    ("ถ้าหมุนเครื่องกำเนิดไฟฟ้าเร็วขึ้น จะเกิดผลอย่างไร", "ผลิตไฟฟ้าได้มากขึ้น", ("ผลิตไฟฟ้าได้น้อยลง", "หยุดผลิตไฟฟ้า", "เปลี่ยนเป็นผลิตแสงแทน", "ไม่มีผลใด ๆ", "ผลิตน้ำแทนไฟฟ้า")),
)


GENERATOR_HINT = "เครื่องกำเนิดไฟฟ้าเปลี่ยนพลังงานกลเป็นพลังงานไฟฟ้า ต้องมีสิ่งมาหมุนขดลวดหรือแม่เหล็ก เช่น น้ำ ลม หรือไอน้ำ"


class PowerSource(NamedTuple):
    record: str
    source: str


POWER_SOURCES = (
    PowerSource("โรงไฟฟ้าที่ปล่อยน้ำจากเขื่อนให้ไหลแรงหมุนกังหันของเครื่องกำเนิดไฟฟ้า", "พลังงานน้ำ"),
    PowerSource("โรงไฟฟ้าที่เผาถ่านหินต้มน้ำเป็นไอน้ำแรงดันสูงไปหมุนกังหันของเครื่องกำเนิดไฟฟ้า", "พลังงานเชื้อเพลิงฟอสซิล (ถ่านหิน)"),
    PowerSource("กังหันลมขนาดใหญ่ที่ใบพัดหมุนเมื่อมีลมพัดแรง แล้วหมุนเครื่องกำเนิดไฟฟ้าที่ต่ออยู่", "พลังงานลม"),
    PowerSource("โรงไฟฟ้าที่ใช้ไอน้ำร้อนจากใต้พิภพหมุนกังหันของเครื่องกำเนิดไฟฟ้า", "พลังงานความร้อนใต้พิภพ"),
    PowerSource("โรงไฟฟ้าที่เผาแกลบและชานอ้อยต้มน้ำเป็นไอน้ำไปหมุนกังหัน", "พลังงานชีวมวล"),
    PowerSource("โรงไฟฟ้าที่เผาแก๊สธรรมชาติจากอ่าวไทยต้มน้ำเป็นไอน้ำไปหมุนกังหัน", "พลังงานเชื้อเพลิงฟอสซิล (แก๊สธรรมชาติ)"),
    PowerSource("แผงโซลาร์เซลล์บนหลังคาที่ผลิตไฟฟ้าเมื่อได้รับแสงแดด", "พลังงานแสงอาทิตย์"),
    PowerSource("โรงไฟฟ้าที่นำแก๊สจากมูลสัตว์ในฟาร์มหมูมาเผาเพื่อหมุนเครื่องยนต์ต่อเครื่องกำเนิดไฟฟ้า", "พลังงานก๊าซชีวภาพ"),
)


RENEWABLE = ("พลังงานแสงอาทิตย์", "พลังงานลม", "พลังงานน้ำ", "พลังงานชีวมวล", "พลังงานความร้อนใต้พิภพ", "พลังงานก๊าซชีวภาพ")


NONRENEWABLE = ("ถ่านหิน", "น้ำมันดิบ", "แก๊สธรรมชาติ", "ลิกไนต์")


GENERATOR_SCENARIOS = (
    ("บ้านที่ติดตั้งกังหันลมขนาดเล็กผลิตไฟฟ้าใช้เองมีข้อดีอย่างไรเมื่อเทียบกับการซื้อไฟฟ้าจากโรงไฟฟ้าถ่านหินเพียงอย่างเดียว",
     "ลดการปล่อยมลพิษจากการเผาเชื้อเพลิง และใช้แหล่งพลังงานที่ไม่มีวันหมด",
     ("กังหันลมผลิตไฟฟ้าได้มากกว่าและไม่มีข้อจำกัดใด ๆ", "กังหันลมไม่ต้องอาศัยการหมุนของเครื่องกำเนิดไฟฟ้าเลย", "โรงไฟฟ้าถ่านหินไม่มีการเปลี่ยนรูปพลังงานเช่นเดียวกับกังหันลม")),
    ("เหตุใดโรงไฟฟ้าพลังน้ำจึงผลิตไฟฟ้าได้มากขึ้นเมื่อปล่อยน้ำจากเขื่อนที่มีความสูงมากขึ้น",
     "น้ำที่ตกจากที่สูงกว่ามีพลังงานศักย์มากกว่า จึงหมุนกังหันได้แรงขึ้นและผลิตไฟฟ้าได้มากขึ้น",
     ("ความสูงของเขื่อนไม่มีผลต่อปริมาณไฟฟ้าที่ผลิตได้", "น้ำที่ตกจากที่สูงกว่าจะเย็นกว่าจึงผลิตไฟฟ้าได้มากกว่า", "เขื่อนที่สูงกว่ามีเครื่องกำเนิดไฟฟ้าขนาดเล็กกว่าเสมอ")),
    ("ทำไมพื้นที่ห่างไกลที่ไม่มีสายส่งไฟฟ้าจึงมักเลือกใช้แผงโซลาร์เซลล์แทนโรงไฟฟ้าถ่านหินขนาดใหญ่",
     "แผงโซลาร์เซลล์ติดตั้งใช้งานเฉพาะจุดได้โดยไม่ต้องพึ่งสายส่งไฟฟ้าระยะไกล",
     ("แผงโซลาร์เซลล์ผลิตไฟฟ้าได้มากกว่าโรงไฟฟ้าถ่านหินเสมอ", "โรงไฟฟ้าถ่านหินสร้างในพื้นที่ห่างไกลไม่ได้เลย", "แผงโซลาร์เซลล์ใช้เชื้อเพลิงฟอสซิลเช่นเดียวกับโรงไฟฟ้าถ่านหิน")),
)


@question_type(
    "phys.generator_work_foundation",
    display_name={"th": "บรรยายการทำงานของเครื่องกำเนิดไฟฟ้า"},
    level=THIRD, subject=SUBJECT, topic=GENERATOR_TOPIC,
)
class GeneratorWorkFoundation(QuestionType):
    """How a generator works, its parts, and a small one at home."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(GENERATOR_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), hint=GENERATOR_HINT, topic=GENERATOR_TOPIC)


@question_type(
    "phys.generator_source_fluency",
    display_name={"th": "ระบุแหล่งพลังงานในการผลิตไฟฟ้าจากข้อมูลที่รวบรวมได้"},
    level=THIRD, subject=SUBJECT, topic=GENERATOR_TOPIC,
)
class GeneratorSourceFluency(QuestionType):
    """A power plant's record; the energy source that spins its generator."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        index = rng.randrange(len(POWER_SOURCES))
        record = POWER_SOURCES[index]
        others = [s for i, (_, s) in enumerate(POWER_SOURCES) if i != index]
        return _labelled(
            stem=f"{record.record} จากข้อมูลนี้ แหล่งพลังงานที่ใช้ในการผลิตไฟฟ้าคือสิ่งใด",
            correct=record.source,
            wrongs=tuple(others),
            hint="แหล่งพลังงานคือสิ่งที่ทำให้กังหันหรือส่วนหมุนของเครื่องกำเนิดไฟฟ้าเคลื่อนที่ตั้งแต่ต้น",
            topic=GENERATOR_TOPIC,
        )


@question_type(
    "phys.generator_source_application",
    display_name={"th": "เปรียบเทียบแหล่งพลังงานในการผลิตไฟฟ้า"},
    level=THIRD, subject=SUBJECT, topic=GENERATOR_TOPIC,
)
class GeneratorSourceApplication(QuestionType):
    """Authored comparisons, and renewable against used-up sources."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            return _retopic(scenario_question(rng, GENERATOR_SCENARIOS,
                                              hint="เปรียบเทียบว่าแหล่งพลังงานแต่ละชนิดหมดไปได้หรือไม่ และเหมาะกับพื้นที่แบบใด"), GENERATOR_TOPIC)
        renewable = rng.random() < 0.5
        right = rng.choice(RENEWABLE if renewable else NONRENEWABLE)
        wrongs = rng.sample(NONRENEWABLE if renewable else RENEWABLE, 3)
        return _labelled(stem=f"แหล่งพลังงานใดใช้ผลิตไฟฟ้าแล้ว{'ไม่หมดไป (พลังงานหมุนเวียน)' if renewable else 'หมดไปได้ (ใช้แล้วหมดไป)'}",
                         correct=right, wrongs=tuple(wrongs),
                         hint="พลังงานหมุนเวียนเกิดขึ้นใหม่ได้ตามธรรมชาติ เช่น แสงแดด ลม น้ำ ส่วนเชื้อเพลิงฟอสซิลใช้แล้วหมดไป", topic=GENERATOR_TOPIC)
