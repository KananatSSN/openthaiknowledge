"""การวัดมวลและปริมาตรของสารบริสุทธิ์และสารผสม

เคมี · ม.1 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.1/6

Sets moved here from: science_wave_d8.
"""

from __future__ import annotations

from decimal import Decimal
from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d1 import SUBJECT
from otk.sets._support.science_wave_d7 import SECONDARY_ONE

PROVENANCE = Provenance("original")


MEASURING_TOPIC = "การวัดมวลและปริมาตรของสารบริสุทธิ์และสารผสม"


class Liquid(NamedTuple):
    name: str
    density: float   # g/cm³, to two decimals


LIQUIDS = (
    Liquid("น้ำกลั่น", 1.00),
    Liquid("น้ำเกลือ", 1.10),
    Liquid("น้ำเชื่อม", 1.20),
    Liquid("เอทานอล", 0.80),
)


VOLUMES = (20, 25, 40, 50)


def _g(value: float) -> str:
    return f"{value:g}"


MEASURING_SCENARIOS = (
    ("นักเรียนวัดความหนาแน่นของน้ำกลั่นได้ 1.00 และของน้ำเกลือได้ 1.10 กรัมต่อลูกบาศก์เซนติเมตร ถ้าละลายเกลือเพิ่มลงในน้ำเกลือนั้น ความหนาแน่นน่าจะเป็นอย่างไร",
     "มากกว่า 1.10 กรัมต่อลูกบาศก์เซนติเมตร เพราะสารผสมมีความหนาแน่นเปลี่ยนไปตามสัดส่วนของสารที่ผสม",
     ("เท่ากับ 1.00 กรัมต่อลูกบาศก์เซนติเมตร เพราะยังเป็นน้ำ",
      "เท่ากับ 1.10 กรัมต่อลูกบาศก์เซนติเมตรเสมอ เพราะเป็นน้ำเกลือเหมือนเดิม",
      "น้อยกว่า 1.00 กรัมต่อลูกบาศก์เซนติเมตร เพราะเกลือทำให้น้ำเบาลง",
      "น้อยกว่า 1.10 กรัมต่อลูกบาศก์เซนติเมตร เพราะเกลือแทนที่น้ำ",
      "เท่ากับความหนาแน่นของเกลือพอดี เพราะมีเกลือมากขึ้น")),
    ("นักเรียนสองคนวัดปริมาตรน้ำเชื่อมชุดเดียวกัน คนหนึ่งอ่านได้ 48 อีกคนอ่านได้ 50 ลูกบาศก์เซนติเมตร เพราะมองระดับน้ำต่างกัน ควรทำอย่างไร",
     "อ่านใหม่โดยวางกระบอกตวงบนพื้นราบและมองระดับสายตาตรงส่วนโค้งล่าง แล้ววัดซ้ำหลายครั้ง",
     ("ใช้ค่าที่มากกว่าเพราะปลอดภัยกว่า",
      "เฉลี่ยสองค่าโดยไม่ต้องอ่านใหม่",
      "เปลี่ยนไปวัดด้วยไม้บรรทัด",
      "ใช้ค่าที่น้อยกว่าเพราะน้ำเชื่อมระเหยไปบางส่วน",
      "เทน้ำเชื่อมใส่บีกเกอร์แล้วประมาณค่าด้วยตา")),
    ("ทองคำบริสุทธิ์มีความหนาแน่น 19.3 กรัมต่อลูกบาศก์เซนติเมตร แหวนวงหนึ่งวัดมวลได้ 38.6 กรัม และปริมาตรได้ 2.5 ลูกบาศก์เซนติเมตร ข้อสรุปใดสมเหตุสมผลที่สุด",
     "แหวนไม่น่าจะเป็นทองคำบริสุทธิ์ เพราะความหนาแน่นที่คำนวณได้ประมาณ 15.4 กรัมต่อลูกบาศก์เซนติเมตร ต่ำกว่าของทองคำบริสุทธิ์",
     ("แหวนเป็นทองคำบริสุทธิ์ เพราะมีมวลมาก",
      "แหวนเป็นทองคำบริสุทธิ์ เพราะ 38.6 เป็นสองเท่าของ 19.3",
      "สรุปไม่ได้ เพราะความหนาแน่นใช้กับของเหลวเท่านั้น",
      "แหวนเป็นทองคำบริสุทธิ์ เพราะความหนาแน่นที่คำนวณได้ 96.5 กรัมต่อลูกบาศก์เซนติเมตร",
      "แหวนไม่ใช่ทองคำ เพราะทองคำต้องมีปริมาตรมากกว่า 10 ลูกบาศก์เซนติเมตร")),
)


# (metal, density of the pure metal in g/cm³)
PURE_METALS = (("ทองคำ", "19.3"), ("เงิน", "10.5"), ("ทองแดง", "8.9"), ("อะลูมิเนียม", "2.7"))


def purity_check(rng: Random) -> GeneratedQuestion:
    """A measured mass and volume; is the object the pure metal it is sold as?"""
    metal, pure = rng.choice(PURE_METALS)
    pure = Decimal(pure)
    volume = Decimal(rng.choice(("2", "2.5", "4", "5", "8", "10")))
    density = pure if rng.random() < 0.5 else pure - Decimal(rng.choice(("0.5", "1.1", "1.5", "0.3")))
    mass = density * volume
    d = f"{density.normalize():f}"
    unit = "กรัมต่อลูกบาศก์เซนติเมตร"
    same = f"น่าจะเป็น{metal}บริสุทธิ์ เพราะความหนาแน่นที่คำนวณได้ {d} {unit} เท่ากับของ{metal}บริสุทธิ์"
    lower = f"ไม่น่าจะเป็น{metal}บริสุทธิ์ เพราะความหนาแน่นที่คำนวณได้ {d} {unit} ต่ำกว่าของ{metal}บริสุทธิ์"
    swapped = f"{(volume / mass).quantize(Decimal('0.01'))}"
    options = (f"เป็น{metal}บริสุทธิ์ เพราะมีมวลมากถึง {mass.normalize():f} กรัม",
               "สรุปไม่ได้ เพราะความหนาแน่นใช้กับของเหลวเท่านั้น",
               f"ไม่น่าจะเป็น{metal}บริสุทธิ์ เพราะความหนาแน่นที่คำนวณได้ {swapped} {unit}",
               f"น่าจะเป็น{metal}บริสุทธิ์ เพราะมวลหารด้วยปริมาตรได้เท่ากับปริมาตร")
    correct = same if density == pure else lower
    return _labelled(
        stem=(f"{metal}บริสุทธิ์มีความหนาแน่น {pure} {unit} ชิ้นงานที่ขายว่าเป็น{metal}ชิ้นหนึ่ง "
              f"วัดมวลได้ {mass.normalize():f} กรัม และปริมาตรได้ {volume} ลูกบาศก์เซนติเมตร ข้อสรุปใดสมเหตุสมผลที่สุด"),
        correct=correct,
        wrongs=(lower if correct == same else same, *options),
        hint="ความหนาแน่น = มวล ÷ ปริมาตร แล้วเทียบกับความหนาแน่นของสารบริสุทธิ์",
        topic=MEASURING_TOPIC,
    )


@question_type(
    "chem.substance_measuring_foundation",
    display_name={"th": "ใช้เครื่องมือวัดมวลและปริมาตรของสารอย่างถูกวิธี"},
    level=SECONDARY_ONE, subject=SUBJECT, topic=MEASURING_TOPIC,
)
class SubstanceMeasuringFoundation(QuestionType):
    """The right way to take a mass or volume reading."""

    PRACTICES = (
        ("ชั่งมวลของน้ำเกลือในบีกเกอร์ด้วยเครื่องชั่งดิจิทัล",
         "วางบีกเกอร์เปล่าแล้วกดตั้งค่าศูนย์ก่อน จึงเทน้ำเกลือลงไปและอ่านค่า",
         ("เทน้ำเกลือลงบนจานเครื่องชั่งโดยตรง",
          "อ่านค่ามวลของบีกเกอร์พร้อมน้ำเกลือแล้วถือว่าเป็นมวลของน้ำเกลือ",
          "ยกเครื่องชั่งขึ้นขณะอ่านค่าเพื่อให้เห็นตัวเลขชัด",
          "กดตั้งค่าศูนย์หลังจากเทน้ำเกลือลงไปแล้ว",
          "วางเครื่องชั่งบนพื้นเอียงใกล้พัดลมที่เปิดอยู่")),
        ("อ่านปริมาตรของเอทานอลในกระบอกตวง",
         "วางกระบอกตวงบนพื้นราบ มองระดับสายตาตรงกับส่วนโค้งล่างของผิวของเหลว",
         ("ถือกระบอกตวงเอียงแล้วอ่านที่ขอบบนของของเหลวที่ติดผนัง",
          "มองจากด้านบนลงไปในกระบอกตวง",
          "อ่านค่าจากขีดบนสุดของกระบอกตวงเสมอ",
          "ย่อตัวมองจากระดับต่ำกว่าผิวของเหลว แล้วอ่านที่ส่วนโค้งบนของผิว",
          "อ่านค่าที่ขอบของเหลวที่เกาะผนังด้านบน")),
        ("วัดปริมาตรของก้อนโลหะผสมที่มีรูปร่างไม่แน่นอน",
         "ใส่น้ำในกระบอกตวง อ่านปริมาตร แล้วหย่อนก้อนโลหะลงไปให้จมมิดและอ่านปริมาตรใหม่ ผลต่างคือปริมาตรของก้อนโลหะ",
         ("ชั่งมวลของก้อนโลหะ แล้วใช้ค่ามวลเป็นปริมาตร",
          "วัดความยาวด้านเดียวด้วยไม้บรรทัด",
          "ใส่ก้อนโลหะในกระบอกตวงเปล่าแล้วอ่านค่า",
          "หย่อนก้อนโลหะให้จมเพียงครึ่งก้อนแล้วอ่านค่า",
          "อ่านปริมาตรน้ำหลังใส่ก้อนโลหะเพียงครั้งเดียวแล้วถือเป็นปริมาตรของก้อนโลหะ")),
        ("ตวงน้ำ 35 ลูกบาศก์เซนติเมตรด้วยกระบอกตวง",
         "เทน้ำใกล้ขีด 35 แล้วใช้หลอดหยดเติมจนส่วนโค้งล่างตรงขีด โดยมองระดับสายตา",
         ("เทน้ำจนล้นกระบอกตวงแล้วค่อยเทออกครึ่งหนึ่ง",
          "ใช้บีกเกอร์ที่มีขีดประมาณค่าแทนเพราะแม่นยำกว่ากระบอกตวง",
          "เทน้ำจนขอบบนของผิวน้ำตรงขีด 35 โดยมองจากด้านบน",
          "ถือกระบอกตวงเอียงขณะเติมน้ำเพื่อให้เห็นขีดชัด",
          "เทน้ำให้เกินขีดเล็กน้อย แล้วถือว่าใกล้เคียงพอโดยไม่ต้องใช้หลอดหยด")),
        ("ชั่งผงเกลือ 5 กรัมด้วยเครื่องชั่งดิจิทัล",
         "วางกระดาษชั่งบนเครื่องชั่ง กดตั้งค่าศูนย์ แล้วตักเกลือใส่จนอ่านค่าได้ 5 กรัม",
         ("เทเกลือลงบนจานเครื่องชั่งโดยตรงแล้วอ่านค่าเมื่อได้ 5 กรัม",
          "วางกระดาษชั่งแต่ไม่ตั้งค่าศูนย์ แล้วอ่านค่ารวมของกระดาษและเกลือเป็นมวลเกลือ",
          "ใช้มือกดจานเครื่องชั่งให้ตัวเลขนิ่งก่อนอ่าน",
          "ประมาณด้วยช้อนชาหนึ่งช้อนโดยไม่ต้องชั่ง",
          "ชั่งเกลือขณะเปิดพัดลมเป่าเครื่องชั่ง")),
    )

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        task, right, wrongs = rng.choice(self.PRACTICES)
        return _labelled(
            stem=f"นักเรียนต้องการ{task} ข้อใดเป็นวิธีที่ถูกต้อง",
            correct=right,
            wrongs=wrongs,
            hint="ค่าที่อ่านต้องเป็นของสารเพียงอย่างเดียว และอ่านในท่าที่ไม่ทำให้ค่าคลาดเคลื่อน",
            topic=MEASURING_TOPIC,
        )


@question_type(
    "chem.substance_measuring_fluency",
    display_name={"th": "หามวล ปริมาตร และความหนาแน่นจากค่าที่วัดได้"},
    level=SECONDARY_ONE, subject=SUBJECT, topic=MEASURING_TOPIC,
)
class SubstanceMeasuringFluency(QuestionType):
    """An empty cylinder's mass, then filled; the liquid's density."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        liquid = rng.choice(LIQUIDS)
        volume = rng.choice(VOLUMES)
        empty = rng.choice(range(60, 101, 5))
        mass = round(liquid.density * volume, 2)
        full = round(empty + mass, 2)
        density = liquid.density
        # Common slips: forgetting to subtract the cylinder, dividing the wrong way, or
        # reporting the mass itself. The first three that differ from the answer are offered.
        slips = (round(full / volume, 2), round(empty / volume, 2), round(volume / mass, 2), mass,
                 round(mass / (2 * volume), 2))
        wrongs = [w for w in dict.fromkeys(slips) if w != density][:3]
        return _labelled(
            stem=(f"นักเรียนชั่งกระบอกตวงเปล่าได้ {empty} กรัม เท{liquid.name}ลงไป {volume} ลูกบาศก์เซนติเมตร "
                  f"แล้วชั่งกระบอกตวงพร้อม{liquid.name}ได้ {_g(full)} กรัม {liquid.name}มีความหนาแน่นเท่าใด"),
            correct=f"{_g(density)} กรัมต่อลูกบาศก์เซนติเมตร",
            wrongs=tuple(f"{_g(w)} กรัมต่อลูกบาศก์เซนติเมตร" for w in wrongs),
            hint="มวลของของเหลว = มวลรวม − มวลกระบอกตวงเปล่า แล้วหารด้วยปริมาตร",
            topic=MEASURING_TOPIC,
        )


@question_type(
    "chem.substance_measuring_application",
    display_name={"th": "ใช้ผลการวัดมวลและปริมาตรตรวจสอบสารบริสุทธิ์และสารผสม"},
    level=SECONDARY_ONE, subject=SUBJECT, topic=MEASURING_TOPIC,
)
class SubstanceMeasuringApplication(QuestionType):
    """Saltier brine, two readers disagreeing, and a ring that is not pure gold."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            return purity_check(rng)
        return _retopic(scenario_question(
            rng, MEASURING_SCENARIOS,
            hint="คำนวณความหนาแน่นจากมวลและปริมาตร แล้วเทียบกับค่าของสารบริสุทธิ์",
        ), MEASURING_TOPIC)


SubstanceMeasuringFoundation.PRACTICES = (*SubstanceMeasuringFoundation.PRACTICES,
    ('ตวงน้ำ 5 ลูกบาศก์เซนติเมตรให้แม่นยำ',
     'ใช้กระบอกตวงขนาดเล็กหรือปิเปตที่มีขีดละเอียด แทนบีกเกอร์ขนาดใหญ่',
     ('ใช้บีกเกอร์ขนาด 500 ลูกบาศก์เซนติเมตรเพราะใส่น้ำได้มากกว่า', 'กะปริมาณด้วยสายตาโดยไม่ต้องใช้เครื่องมือ',
      'ใช้ถ้วยกาแฟที่บ้านแทนเพราะมีขนาดพอดี', 'เทน้ำจนล้นกระบอกตวงขนาดใหญ่แล้วกะว่าน่าจะใกล้เคียง',
      'ใช้ช้อนตักน้ำห้าช้อนโดยไม่ต้องวัดปริมาตร')),
    ('ชั่งมวลของสารที่เพิ่งนำออกจากเตาอบร้อน ๆ',
     'รอให้สารเย็นลงถึงอุณหภูมิห้องก่อนจึงชั่ง เพราะของร้อนทำให้ค่าที่อ่านได้คลาดเคลื่อน',
     ('ชั่งทันทีขณะยังร้อนเพราะได้ค่าที่แม่นยำที่สุด', 'เป่าลมใส่สารบนเครื่องชั่งระหว่างอ่านค่าเพื่อให้เย็นเร็ว',
      'วางสารร้อนลงบนจานเครื่องชั่งโดยตรงโดยไม่ใช้ภาชนะ', 'ชั่งพร้อมถุงมือกันร้อนแล้วถือว่าเป็นมวลของสาร',
      'ยกเครื่องชั่งไปวางใกล้เตาอบเพื่อให้ชั่งได้ทันที')),
)
