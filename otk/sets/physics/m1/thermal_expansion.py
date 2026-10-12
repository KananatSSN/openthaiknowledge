"""แบบจำลองการขยายตัวหรือหดตัวของสสารเนื่องจากความร้อน

ฟิสิกส์ · ม.1 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.1/3

Sets moved here from: science_wave_d28.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import numeric, show
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d28 import FIRST_SECONDARY

PROVENANCE = Provenance("original")


THERMAL_EXPANSION_TOPIC = "แบบจำลองการขยายตัวหรือหดตัวของสสารเนื่องจากความร้อน"


EXPAND_EVENTS = ("ลูกโป่งที่ครอบปากขวดพองขึ้นเมื่อแช่ขวดในน้ำร้อน", "ระดับน้ำสีในหลอดแก้วที่เสียบจุกขวดสูงขึ้นเมื่ออุ่นขวด",
                 "ลูกโลหะลอดห่วงไม่ได้หลังเผาไฟ", "สายไฟฟ้าหย่อนลงมากขึ้นในวันที่อากาศร้อน", "ปรอทในเทอร์มอมิเตอร์สูงขึ้นเมื่อจุ่มน้ำร้อน")


CONTRACT_EVENTS = ("ลูกโป่งที่ครอบปากขวดแฟบลงเมื่อแช่ขวดในน้ำเย็นจัด", "ระดับแอลกอฮอล์ในเทอร์มอมิเตอร์ลดลงเมื่อวางในน้ำแข็ง",
                   "สายไฟฟ้าตึงขึ้นในเช้าที่อากาศหนาว", "ช่องว่างระหว่างรางรถไฟกว้างขึ้นในคืนที่อากาศเย็น", "ขวดพลาสติกเปล่าที่ปิดฝาบุบเมื่อนำเข้าตู้เย็น")


EXPAND_FACTS = (
    ("เมื่อสสารได้รับความร้อน โดยทั่วไปจะเกิดการเปลี่ยนแปลงอย่างไร", "ขยายตัว เนื่องจากอนุภาคเคลื่อนที่เร็วขึ้นและอยู่ห่างกันมากขึ้น",
     ("หดตัว เนื่องจากอนุภาคเคลื่อนที่ช้าลงและอยู่ใกล้กันมากขึ้น", "ไม่มีการเปลี่ยนแปลงขนาดใด ๆ ไม่ว่าจะได้รับความร้อนมากเท่าใด",
      "เปลี่ยนเป็นสารชนิดใหม่ทันทีที่ได้รับความร้อน", "อนุภาคมีขนาดใหญ่ขึ้นทุกอนุภาค", "มวลของสสารเพิ่มขึ้น")),
    ("เมื่อสสารขยายตัวเนื่องจากความร้อน สิ่งใดไม่เปลี่ยนแปลง", "มวลและจำนวนอนุภาคของสสาร",
     ("ปริมาตรและความหนาแน่น", "ระยะห่างระหว่างอนุภาค", "ความหนาแน่นของสสาร", "อัตราเร็วของอนุภาค", "ขนาดโดยรวมของวัตถุ")),
    ("ถ้าให้ความร้อนเท่ากัน สสารสถานะใดขยายตัวมากที่สุด", "แก๊ส", ("ของแข็ง", "ของเหลว", "ทุกสถานะขยายตัวเท่ากัน", "ไม่มีสถานะใดขยายตัว", "ของแข็งที่เป็นโลหะ")),
)


EXPAND_HINT = "ความร้อนทำให้อนุภาคเคลื่อนที่เร็วขึ้นและอยู่ห่างกันมากขึ้น สสารจึงขยายตัว เมื่อเย็นลงอนุภาคเข้าใกล้กันสสารจึงหดตัว มวลไม่เปลี่ยน"


METALS = (("อะลูมิเนียม", 23), ("ทองเหลือง", 19), ("ทองแดง", 17), ("เหล็ก", 12))


BALL_RING_STEM = ("ลูกโลหะลอดผ่านห่วงโลหะได้พอดีที่อุณหภูมิห้อง เมื่อนำลูกโลหะไปเผาไฟจนร้อนจัดแล้วนำมาลอดห่วงทันที "
                  "พบว่าลูกโลหะลอดผ่านห่วงไม่ได้อีก จากแบบจำลองนี้ ข้อใดอธิบายได้ถูกต้อง")


THERMAL_EXPANSION_SCENARIOS = (
    ("รางรถไฟเหล็กมักเว้นช่องว่างเล็ก ๆ ระหว่างท่อนราง เหตุใดจึงต้องเว้นช่องว่างนี้",
     "เพื่อรองรับการขยายตัวของรางเหล็กเมื่ออุณหภูมิสูงขึ้นในวันที่อากาศร้อน ไม่ให้รางโก่งงอ",
     ("เพื่อรองรับการหดตัวของรางเหล็กเมื่ออากาศร้อน ไม่ให้รางขาดออกจากกันในวันที่แดดจัด", "เพื่อให้รถไฟวิ่งผ่านช่องว่างได้เร็วขึ้น และลดเสียงดังขณะล้อกระทบรอยต่อของราง", "เพื่อระบายน้ำฝนออกจากรางเหล็ก ไม่ให้รางเป็นสนิมจนโก่งงอเมื่ออุณหภูมิสูงขึ้นมาก")),
    ("แถบโลหะสองชนิดประกบกัน (bimetallic strip) ในเทอร์โมสตัทจะโค้งงอเมื่ออุณหภูมิเปลี่ยนแปลง เพราะเหตุใด",
     "โลหะสองชนิดขยายตัวหรือหดตัวได้ไม่เท่ากันเมื่ออุณหภูมิเปลี่ยน แถบโลหะจึงโค้งงอไปทางโลหะที่ขยายตัวน้อยกว่า",
     ("โลหะสองชนิดขยายตัวเท่ากันเมื่ออุณหภูมิเปลี่ยน แต่แถบโลหะโค้งงอเพราะโลหะชนิดหนึ่งอ่อนตัวลงเมื่อร้อน", "โลหะสองชนิดขยายตัวหรือหดตัวได้ไม่เท่ากันเมื่ออุณหภูมิเปลี่ยน แถบโลหะจึงโค้งงอไปทางโลหะที่ขยายตัวมากกว่า", "โลหะสองชนิดขยายตัวเท่ากัน แต่มีน้ำหนักต่างกัน แถบโลหะจึงโค้งงอไปทางโลหะที่หนักกว่า")),
    ("ฝาโลหะของขวดแก้วที่แน่นมากจนเปิดไม่ออก มักแก้ไขได้โดยแช่ฝาในน้ำอุ่น เหตุใดวิธีนี้จึงได้ผล",
     "ความร้อนจากน้ำอุ่นทำให้ฝาโลหะขยายตัวมากกว่าขวดแก้ว ฝาจึงหลวมและหมุนเปิดได้ง่ายขึ้น",
     ("ความร้อนจากน้ำอุ่นทำให้ขวดแก้วหดตัวมากกว่าฝาโลหะ ฝาจึงหลวมและหมุนเปิดได้ง่าย", "ความร้อนทำให้ฝาโลหะหดตัวแน่นขึ้น แต่น้ำอุ่นหล่อลื่นเกลียวฝาจึงหมุนเปิดได้ง่าย", "ความร้อนจากน้ำอุ่นทำให้ฝาโลหะและขวดแก้วขยายตัวเท่ากัน เกลียวจึงลื่นและหมุนเปิดได้")),
)


@question_type(
    "phys.thermal_expansion_foundation",
    display_name={"th": "บอกผลของความร้อนต่อการขยายตัวของสสาร"},
    level=FIRST_SECONDARY, subject=SUBJECT, topic=THERMAL_EXPANSION_TOPIC,
)
class ThermalExpansionFoundation(QuestionType):
    """Heating expands and cooling contracts; which everyday events show which."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.5:
            expand = roll < 0.25
            return _labelled(stem=f"เหตุการณ์ใดแสดงการ{'ขยายตัว' if expand else 'หดตัว'}ของสสาร", correct=rng.choice(EXPAND_EVENTS if expand else CONTRACT_EVENTS),
                             wrongs=tuple(CONTRACT_EVENTS if expand else EXPAND_EVENTS), hint=EXPAND_HINT, topic=THERMAL_EXPANSION_TOPIC)
        stem, right, wrongs = rng.choice(EXPAND_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), hint=EXPAND_HINT, topic=THERMAL_EXPANSION_TOPIC)


@question_type(
    "phys.thermal_expansion_fluency",
    display_name={"th": "สร้างแบบจำลองที่อธิบายการขยายตัวของสสารเนื่องจากความร้อน"},
    level=FIRST_SECONDARY, subject=SUBJECT, topic=THERMAL_EXPANSION_TOPIC,
)
class ThermalExpansionFluency(QuestionType):
    """The ball and ring, or one observed event explained with the particle model."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.25:
            return _labelled(
                stem=BALL_RING_STEM,
                correct="ความร้อนทำให้อนุภาคของโลหะในลูกโลหะเคลื่อนที่เร็วขึ้นและอยู่ห่างกันมากขึ้น ลูกโลหะจึงขยายตัวจนใหญ่กว่าห่วง",
                wrongs=("ความร้อนทำให้อนุภาคของโลหะเคลื่อนที่ช้าลงและอยู่ใกล้กันมากขึ้น ลูกโลหะจึงขยายตัว",
                        "ลูกโลหะมีมวลเพิ่มขึ้นจากเขม่าและความร้อนที่สะสมระหว่างเผาไฟ จึงหนักจนลอดผ่านห่วงไม่ได้",
                        "ความร้อนจากลูกโลหะทำให้อนุภาคของห่วงโลหะเคลื่อนที่ช้าลงและอยู่ใกล้กันมากขึ้น ห่วงจึงหดตัวลง"),
                hint=EXPAND_HINT, topic=THERMAL_EXPANSION_TOPIC,
            )
        if rng.random() < 0.45:
            rod = rng.choice(("แท่งทองแดง", "แท่งอะลูมิเนียม", "แท่งเหล็ก", "ท่อทองเหลือง"))
            length = rng.choice((50, 80, 100, 120, 150, 200))
            temps = sorted(rng.sample(range(20, 101, 10), 3))
            grow = rng.choice((Fraction(1, 10), Fraction(2, 10), Fraction(3, 10), Fraction(5, 10)))
            rows = " / ".join(f"{t} °C: {show(length + grow * (t - temps[0]) / 10)} cm" for t in temps)
            return _labelled(stem=f"นักเรียนวัดความยาวของ{rod}ที่อุณหภูมิต่าง ๆ ได้ดังนี้ {rows} ข้อสรุปใดอธิบายด้วยแบบจำลองอนุภาคได้ถูกต้อง",
                             correct=f"{rod}ยาวขึ้นเมื่ออุณหภูมิสูงขึ้น เพราะอนุภาคเคลื่อนที่เร็วขึ้นและอยู่ห่างกันมากขึ้น",
                             wrongs=(f"ความร้อนทำให้{rod}สูญเสียอนุภาคบางส่วนไปในอากาศ ค่าที่อ่านได้จึงเปลี่ยนไปเรื่อย ๆ",
                                     f"{rod}ยาวขึ้นเมื่ออุณหภูมิสูงขึ้น เพราะความร้อนทำให้มีอนุภาคเพิ่มขึ้นในแท่งโลหะ",
                                     "ความยาวไม่เกี่ยวข้องกับอุณหภูมิ ค่าที่ต่างกันเป็นเพียงความคลาดเคลื่อนของการวัด"),
                             hint=EXPAND_HINT, topic=THERMAL_EXPANSION_TOPIC)
        expand = rng.random() < 0.5
        event = rng.choice(EXPAND_EVENTS if expand else CONTRACT_EVENTS)
        right = ("อนุภาคได้รับความร้อน เคลื่อนที่เร็วขึ้นและอยู่ห่างกันมากขึ้น สสารจึงขยายตัว" if expand
                 else "อนุภาคเสียความร้อน เคลื่อนที่ช้าลงและอยู่ใกล้กันมากขึ้น สสารจึงหดตัว")
        return _labelled(stem=f"สังเกตพบว่า{event} ข้อใดอธิบายด้วยแบบจำลองอนุภาคได้ถูกต้อง", correct=right,
                         wrongs=("อนุภาคได้รับความร้อน เคลื่อนที่เร็วขึ้นและอยู่ห่างกันมากขึ้น สสารจึงขยายตัว" if not expand
                                 else "อนุภาคเสียความร้อน เคลื่อนที่ช้าลงและอยู่ใกล้กันมากขึ้น สสารจึงหดตัว",
                                 "อนุภาคแต่ละตัวมีขนาดใหญ่ขึ้นหรือเล็กลงเอง", "จำนวนอนุภาคเพิ่มขึ้นหรือลดลงตามอุณหภูมิ"),
                         hint=EXPAND_HINT, topic=THERMAL_EXPANSION_TOPIC)


@question_type(
    "phys.thermal_expansion_application",
    display_name={"th": "ใช้ความรู้เรื่องการขยายตัวของสสารอธิบายอุปกรณ์จริง"},
    level=FIRST_SECONDARY, subject=SUBJECT, topic=THERMAL_EXPANSION_TOPIC,
)
class ThermalExpansionApplication(QuestionType):
    """Authored cases, and which way a two-metal strip bends when heated or cooled."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            return _retopic(scenario_question(
                rng, THERMAL_EXPANSION_SCENARIOS,
                hint="วัสดุต่างชนิดขยายตัวได้ต่างกัน และทุกชนิดขยายตัวเมื่อได้รับความร้อนมากขึ้น",
            ), THERMAL_EXPANSION_TOPIC)
        if rng.random() < 0.4:
            while True:
                (metal, rate) = rng.choice(METALS)
                length = rng.choice((5, 10, 12, 20, 25, 30, 50))
                rise = rng.choice((10, 15, 20, 25, 30, 40))
                grow = Fraction(rate * length * rise, 1000)
                if (grow * 100).denominator == 1:
                    break
            return numeric(stem=f"รางหรือท่อ{metal}ยาว {length} m ขยายตัว {rate} ส่วนในล้านส่วนต่อ 1 °C ถ้าอุณหภูมิสูงขึ้น {rise} °C "
                                f"จะยาวขึ้นกี่มิลลิเมตร (ส่วนที่ยาวขึ้น = ความยาว × อัตราการขยายตัว × อุณหภูมิที่เพิ่ม)",
                           answer=grow, wrongs=[grow * 10, Fraction(rate * length, 1000), grow + rise], unit="มิลลิเมตร",
                           topic=THERMAL_EXPANSION_TOPIC, hint="1 m = 1,000 mm ดังนั้นส่วนที่ยาวขึ้น (mm) = อัตรา (ส่วนในล้านส่วน) × ความยาว (m) × ΔT ÷ 1,000")
        (a, ea), (b, eb) = rng.sample(METALS, 2)
        heated = rng.random() < 0.5
        less, more = (a, b) if ea < eb else (b, a)
        toward = less if heated else more
        table = f"{a} ขยายตัว {ea} ส่วนในล้านส่วนต่อ 1 °C และ{b} ขยายตัว {eb} ส่วนในล้านส่วนต่อ 1 °C"
        return _labelled(stem=f"แถบโลหะคู่ทำจาก{a}ประกบกับ{b} ({table}) เมื่อ{'ให้ความร้อน' if heated else 'ทำให้เย็นลง'} แถบโลหะจะโค้งงอไปทางด้านใด",
                         correct=f"โค้งไปทางด้าน{toward}", wrongs=(f"โค้งไปทางด้าน{more if toward == less else less}", "ไม่โค้งงอเลย", "ยืดตรงและยาวขึ้นเท่ากันทั้งสองด้าน"),
                         hint="โลหะที่ขยายตัวมากจะยาวกว่า แถบจึงโค้งไปทางโลหะที่ยาวน้อยกว่า เมื่อเย็นลงโลหะที่หดตัวมากจะสั้นกว่า แถบจึงโค้งไปทางนั้น",
                         topic=THERMAL_EXPANSION_TOPIC)
