"""การเปลี่ยนแปลงของวัสดุเมื่อร้อนขึ้นหรือเย็นลง

เคมี · ป.3 · สสวท. พื้นฐาน
Indicators: ว 2.1 ป.3/2

Sets moved here from: science_wave_d3.
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
from otk.sets._support.science_wave_d1 import SUBJECT
from otk.sets._support.science_wave_d3 import THIRD

PROVENANCE = Provenance("original")


HEATING_TOPIC = "การเปลี่ยนแปลงของวัสดุเมื่อร้อนขึ้นหรือเย็นลง"


HOTTER, COLDER = "ทำให้ร้อนขึ้น", "ทำให้เย็นลง"


class Change(NamedTuple):
    """A material, what was done to it, and how it looked before and after."""
    material: str
    action: str
    how: str
    before: str
    after: str


CHANGES = (
    Change("เนยก้อน", HOTTER, "วางในกระทะที่ตั้งไฟอ่อน", "ก้อนแข็ง", "ของเหลว"),
    Change("ช็อกโกแลตแท่ง", HOTTER, "ใส่ถ้วยแล้ววางในน้ำอุ่น", "แท่งแข็ง", "ของเหลวข้นที่ไหลได้"),
    Change("เนื้อเทียนรอบไส้เทียน", HOTTER, "จุดไฟที่ไส้เทียน", "ของแข็ง", "ของเหลว"),
    Change("น้ำ", COLDER, "ใส่ถาดแล้ววางในช่องแช่แข็ง", "ของเหลว", "ก้อนน้ำแข็ง"),
    Change("ช็อกโกแลตที่หลอมเหลว", COLDER, "เทลงแม่พิมพ์แล้ววางในตู้เย็น", "ของเหลวที่ไหลได้", "ของแข็งตามรูปแม่พิมพ์"),
    Change("น้ำหวานผสมน้ำผลไม้", COLDER, "ใส่แม่พิมพ์ไอศกรีมแล้วแช่แข็ง", "ของเหลว", "แท่งแข็ง"),
    Change("ไข่ขาว", HOTTER, "ทอดในกระทะ", "ของเหลวใส", "ของแข็งสีขาวขุ่น"),
    Change("น้ำแข็งก้อน", HOTTER, "ใส่ถ้วยแล้ววางในน้ำอุ่น", "ก้อนแข็ง", "น้ำที่ไหลได้"),
    Change("เทียนไขที่หลอมเหลว", COLDER, "เทลงแม่พิมพ์แล้วตั้งทิ้งไว้ให้เย็น", "ของเหลว", "ของแข็งตามรูปแม่พิมพ์"),
    Change("ผงวุ้นที่ต้มละลายกับน้ำ", COLDER, "เทลงถ้วยแล้วแช่ตู้เย็น", "ของเหลว", "วุ้นที่คงรูป"),
)


def _changed(material: str, action: str, before: str, after: str) -> str:
    return f"เมื่อ{action} {material}เปลี่ยนจาก{before}กลายเป็น{after}"


HEATING_SCENARIOS = (
    ("นักเรียนลืมช็อกโกแลตแท่งไว้ในรถที่จอดกลางแดด เมื่อกลับมาพบว่าช็อกโกแลตเหลว ถ้านำไปแช่ตู้เย็น จะเกิดอะไรขึ้น",
     "ช็อกโกแลตกลับมาแข็งอีกครั้ง เพราะเมื่อทำให้เย็นลง ช็อกโกแลตเหลวเปลี่ยนเป็นของแข็ง",
     ("ช็อกโกแลตยังเหลวอยู่ตลอดไป เพราะละลายแล้วแข็งไม่ได้อีก",
      "ช็อกโกแลตกลายเป็นไอหายไป",
      "ช็อกโกแลตเหลวมากขึ้นเพราะตู้เย็นให้ความร้อน",
      "ช็อกโกแลตกลายเป็นน้ำเปล่า",
      "ช็อกโกแลตแข็งตัวได้เฉพาะเมื่อวางกลางแดดอีกครั้ง")),
    ("แม่ทอดไข่ ไข่ขาวที่เคยใสกลายเป็นสีขาวขุ่นและแข็งตัว เมื่อทิ้งไข่ทอดไว้ให้เย็น ไข่ขาวจะเป็นอย่างไร",
     "ยังคงขาวขุ่นและแข็งอยู่ ไม่กลับมาใสเหมือนเดิม",
     ("กลับมาใสและเหลวเหมือนก่อนทอด",
      "กลายเป็นน้ำแข็ง",
      "หลอมเหลวไหลออกจากจาน",
      "กลายเป็นไข่ทั้งฟองเหมือนเดิม",
      "ไข่ขาวระเหยหายไปทั้งหมด")),
    ("ร้านขายไอศกรีมต้องเก็บไอศกรีมไว้ในตู้แช่แข็งตลอดเวลา เพราะเหตุใด",
     "ถ้าไอศกรีมร้อนขึ้นจะละลายเป็นของเหลว ตู้แช่แข็งทำให้ไอศกรีมเย็นจึงคงเป็นของแข็ง",
     ("ตู้แช่แข็งทำให้ไอศกรีมหวานขึ้น",
      "ไอศกรีมจะแข็งขึ้นเมื่อวางไว้ข้างนอกตู้",
      "ความเย็นทำให้ไอศกรีมเปลี่ยนเป็นวัสดุชนิดใหม่",
      "ตู้แช่แข็งทำให้ไอศกรีมร้อนขึ้น",
      "ไอศกรีมไม่ละลายไม่ว่าจะวางไว้ที่ใด")),
    ("นักเรียนวางน้ำแข็งก้อนหนึ่งไว้ในจานกลางแดด และอีกก้อนหนึ่งไว้ในกระติกน้ำแข็ง ก้อนใดละลายเร็วกว่า เพราะเหตุใด",
     "ก้อนที่อยู่กลางแดด เพราะได้รับความร้อนมากกว่า จึงเปลี่ยนเป็นน้ำเร็วกว่า",
     ("ก้อนในกระติก เพราะกระติกทำให้ร้อนขึ้น",
      "ละลายพร้อมกัน เพราะเป็นน้ำแข็งเหมือนกัน",
      "ก้อนกลางแดด เพราะแสงแดดทำให้เย็นลง",
      "ไม่ละลายทั้งสองก้อน",
      "ก้อนในกระติก เพราะกระติกมีลมพัด")),
    ("เหตุใดเทียนไขที่จุดแล้วจึงมีเนื้อเทียนไหลลงมาแข็งตัวอยู่ที่ฐานเชิงเทียน",
     "เนื้อเทียนใกล้เปลวไฟร้อนขึ้นจนเป็นของเหลวไหลลงมา แล้วเย็นลงจนกลับเป็นของแข็ง",
     ("เนื้อเทียนเย็นลงจนเป็นของเหลว",
      "เทียนไขกลายเป็นน้ำแล้วแข็งตัวเป็นน้ำแข็ง",
      "เนื้อเทียนร้อนขึ้นจนแข็งตัว",
      "ฐานเชิงเทียนสร้างเนื้อเทียนขึ้นมาเอง",
      "เนื้อเทียนไหลลงมาเพราะลมพัดโดยไม่ได้ร้อนขึ้น")),
)


@question_type(
    "chem.heating_change_foundation",
    display_name={"th": "บอกผลเมื่อทำให้วัสดุร้อนขึ้นหรือเย็นลง"},
    level=THIRD, subject=SUBJECT, topic=HEATING_TOPIC,
)
class HeatingChangeFoundation(QuestionType):
    """One material heated or cooled; whether and how it changes."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        change = rng.choice(CHANGES)
        opposite = COLDER if change.action == HOTTER else HOTTER
        return _labelled(
            stem=f"ถ้า{change.action} {change.material}ซึ่งเป็น{change.before} จะเกิดการเปลี่ยนแปลงอย่างไร",
            correct=f"กลายเป็น{change.after}",
            wrongs=(f"ยังเป็น{change.before}เหมือนเดิม ไม่เปลี่ยนแปลง",
                    "หายไปทั้งหมดทันที",
                    f"เปลี่ยนแปลงได้เฉพาะเมื่อ{opposite}เท่านั้น",
                    "มีขนาดใหญ่ขึ้นเป็นสองเท่าโดยไม่เปลี่ยนลักษณะ",
                    "เปลี่ยนเป็นสีดำทันที"),
            hint="นึกถึงสิ่งที่เคยเห็นเมื่ออาหารหรือวัสดุนี้ถูกความร้อนหรือความเย็น",
            topic=HEATING_TOPIC,
        )


@question_type(
    "chem.heating_change_fluency",
    display_name={"th": "อธิบายการเปลี่ยนแปลงของวัสดุเมื่อร้อนขึ้นหรือเย็นลงจากหลักฐาน"},
    level=THIRD, subject=SUBJECT, topic=HEATING_TOPIC,
)
class HeatingChangeFluency(QuestionType):
    """An activity's record; explain the change, with its cause, from before to after."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        change = rng.choice(CHANGES)
        opposite = COLDER if change.action == HOTTER else HOTTER
        return _labelled(
            stem=(f"นักเรียนนำ{change.material}ซึ่งเป็น{change.before} ไป{change.how} "
                  f"สักครู่ต่อมาสังเกตเห็นว่า{change.material}กลายเป็น{change.after} "
                  "จากหลักฐานนี้ ข้อใดอธิบายการเปลี่ยนแปลงได้ถูกต้อง"),
            correct=_changed(change.material, change.action, change.before, change.after),
            wrongs=(_changed(change.material, opposite, change.before, change.after),
                    _changed(change.material, change.action, change.after, change.before),
                    f"เมื่อ{change.action} {change.material}ไม่เปลี่ยนแปลง ยังคงเป็น{change.before}",
                    f"เมื่อ{change.action} {change.material}หายไปทั้งหมด ไม่เหลืออะไร",
                    f"เมื่อ{change.action} {change.material}เปลี่ยนจาก{change.before}กลายเป็นแก๊สที่มองไม่เห็น"),
            hint="ดูว่าวิธีที่ทำเป็นการให้ความร้อนหรือทำให้เย็น แล้วเทียบสิ่งที่เห็นก่อนและหลัง",
            topic=HEATING_TOPIC,
        )


@question_type(
    "chem.heating_change_application",
    display_name={"th": "ใช้ความรู้เรื่องการเปลี่ยนแปลงของวัสดุเมื่อร้อนหรือเย็นในชีวิตประจำวัน"},
    level=THIRD, subject=SUBJECT, topic=HEATING_TOPIC,
)
class HeatingChangeApplication(QuestionType):
    """Melted chocolate cooled again, a fried egg, and keeping ice cream frozen."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, HEATING_SCENARIOS,
            hint="แยกว่าวัสดุถูกทำให้ร้อนขึ้นหรือเย็นลง และการเปลี่ยนแปลงนั้นกลับคืนได้หรือไม่",
        ), HEATING_TOPIC)
