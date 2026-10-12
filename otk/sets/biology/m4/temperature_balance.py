"""ดุลยภาพของอุณหภูมิภายในร่างกาย

ชีวะ · ม.4 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.4/4

Sets moved here from: science_wave_b20.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import SUBJECT, scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b19 import BALANCE_TOPIC, UPPER_FOUR, Fact, _fact_question
from otk.sets._support.science_wave_b20 import TEMPERATURE_SCENARIOS

PROVENANCE = Provenance("original")


TEMPERATURE_FACTS = (
    Fact("เหตุใดร่างกายจึงต้องรักษาอุณหภูมิภายในไว้ที่ประมาณ 37 องศาเซลเซียส",
         "เอนไซม์ที่เร่งปฏิกิริยาในเซลล์ทำงานได้ดีที่สุดในช่วงอุณหภูมินี้ "
         "ถ้าอุณหภูมิเปลี่ยนไปมากปฏิกิริยาในเซลล์จะช้าลงหรือหยุดไป"),
    Fact("อวัยวะใดทำหน้าที่เป็นศูนย์ควบคุมอุณหภูมิของร่างกาย",
         "ไฮโพทาลามัสในสมอง ซึ่งรับรู้อุณหภูมิของเลือดที่ไหลผ่าน "
         "แล้วสั่งการไปยังหลอดเลือด ผิวหนัง และกล้ามเนื้อโครงร่าง"),
    Fact("หลอดเลือดที่ผิวหนังตอบสนองอย่างไรเมื่ออุณหภูมิร่างกายสูงขึ้น",
         "ขยายตัวให้เลือดไหลมาที่ผิวหนังมากขึ้น "
         "ความร้อนจากเลือดจึงถ่ายเทออกสู่สิ่งแวดล้อมได้มากขึ้น"),
    Fact("หลอดเลือดที่ผิวหนังตอบสนองอย่างไรเมื่ออุณหภูมิร่างกายลดลง",
         "หดตัวให้เลือดไหลมาที่ผิวหนังน้อยลง "
         "ความร้อนจึงถูกเก็บไว้ที่แกนกลางร่างกายแทนที่จะถ่ายเทออกไป"),
    Fact("ต่อมเหงื่อในผิวหนังช่วยลดอุณหภูมิของร่างกายได้อย่างไร",
         "หลั่งเหงื่อออกมาที่ผิว เมื่อเหงื่อระเหยจะดึงความร้อนจากผิวหนังไปด้วย "
         "อุณหภูมิของร่างกายจึงลดลง"),
    Fact("กล้ามเนื้อโครงร่างช่วยเพิ่มอุณหภูมิของร่างกายได้อย่างไร",
         "หดตัวและคลายตัวสลับกันอย่างรวดเร็วเป็นอาการสั่น "
         "ซึ่งเพิ่มการสลายสารอาหารและปล่อยความร้อนออกมา"),
    Fact("กล้ามเนื้อที่โคนขนในผิวหนังมีบทบาทใดเมื่ออากาศเย็น",
         "หดตัวจนขนตั้งชันเป็นขนลุก ทำให้เกิดชั้นอากาศนิ่งเหนือผิวหนัง "
         "ซึ่งช่วยลดการถ่ายเทความร้อนออกจากร่างกาย"),
)


class Exposure(NamedTuple):
    """A thermal challenge, and the three effectors' answer to it together."""
    situation: str
    response: str


EXPOSURES = (
    Exposure("วิ่งออกกำลังกายกลางแดดจนอุณหภูมิร่างกายสูงขึ้น",
             "หลอดเลือดที่ผิวหนังขยายตัวและต่อมเหงื่อหลั่งเหงื่อมากขึ้นเพื่อระบาย"
             "ความร้อน ส่วนกล้ามเนื้อโครงร่างไม่สั่นเพราะไม่ต้องสร้างความร้อนเพิ่ม"),
    Exposure("ยืนอยู่กลางอากาศหนาวโดยสวมเสื้อผ้าบาง",
             "หลอดเลือดที่ผิวหนังหดตัวและต่อมเหงื่อหลั่งเหงื่อน้อยลงเพื่อลดการเสีย"
             "ความร้อน พร้อมกับกล้ามเนื้อโครงร่างสั่นเพื่อสร้างความร้อนขึ้นมาชดเชย"),
    Exposure("แช่มือทั้งสองข้างในน้ำเย็นจัดเป็นเวลานาน",
             "หลอดเลือดที่ผิวหนังบริเวณมือหดตัวจนมือซีดและเย็นลง "
             "เพื่อลดการเสียความร้อนจากแกนกลางร่างกายไปกับเลือดที่ไหลผ่านมือ"),
    Exposure("มีไข้จากการติดเชื้อจนรู้สึกหนาวสั่นทั้งที่วัดอุณหภูมิได้สูง",
             "ไฮโพทาลามัสตั้งอุณหภูมิเป้าหมายไว้สูงขึ้น ร่างกายจึงหดหลอดเลือด"
             "ที่ผิวหนังและสั่นกล้ามเนื้อเพื่อดันอุณหภูมิขึ้นไปให้ถึงเป้าหมายใหม่"),
    Exposure("อยู่ในห้องอบไอน้ำที่ทั้งร้อนและมีความชื้นสูงมาก",
             "หลอดเลือดที่ผิวหนังขยายตัวและมีเหงื่อออกมาก แต่ความชื้นในอากาศที่สูง"
             "ทำให้เหงื่อระเหยได้น้อย การระบายความร้อนจึงทำได้ไม่ดีเท่าที่ควร"),
    Exposure("ยืนตากลมทันทีหลังอาบน้ำเสร็จโดยยังไม่ได้เช็ดตัว",
             "น้ำที่ผิวหนังระเหยไปพร้อมกับพาความร้อนออกไปอย่างรวดเร็ว "
             "ร่างกายจึงหดหลอดเลือดที่ผิวหนังและอาจเกิดขนลุกเพื่อลดการเสียความร้อน"),
)


@question_type(
    "body.temperature_balance_foundation",
    display_name={"th": "การควบคุมดุลยภาพของอุณหภูมิภายในร่างกาย"},
    level=UPPER_FOUR, subject=SUBJECT, topic=BALANCE_TOPIC,
)
class TemperatureBalanceFoundation(QuestionType):
    """What blood vessels, skin and skeletal muscle each contribute."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _fact_question(
            rng, TEMPERATURE_FACTS, topic=BALANCE_TOPIC,
            hint="ถามก่อนว่าร่างกายกำลังต้องระบายความร้อนออกหรือเก็บความร้อนไว้ "
                 "แล้วจึงดูว่าอวัยวะนั้นช่วยไปในทางใด",
        )


@question_type(
    "body.temperature_balance_fluency",
    display_name={"th": "การตอบสนองต่ออุณหภูมิที่เปลี่ยนแปลง"},
    level=UPPER_FOUR, subject=SUBJECT, topic=BALANCE_TOPIC,
)
class TemperatureBalanceFluency(QuestionType):
    """Give the three effectors' combined answer to a thermal challenge."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(EXPOSURES)
        others = [other.response for other in EXPOSURES
                  if other.response != item.response]
        rng.shuffle(others)
        return _labelled(
            stem=f"เมื่อ{item.situation} ร่างกายจะรักษาดุลยภาพของอุณหภูมิ"
                 f"ไว้ได้อย่างไร",
            correct=item.response, wrongs=tuple(others[:3]),
            hint="ตอบให้ครบทั้งสามส่วน คือหลอดเลือดที่ผิวหนัง ต่อมเหงื่อ "
                 "และกล้ามเนื้อโครงร่าง",
            topic=BALANCE_TOPIC,
        )


@question_type(
    "body.temperature_balance_application",
    display_name={"th": "วิเคราะห์การรักษาดุลยภาพของอุณหภูมิ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=BALANCE_TOPIC,
)
class TemperatureBalanceApplication(QuestionType):
    """Judge a case where temperature regulation is helped, hindered or misread."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, TEMPERATURE_SCENARIOS,
            hint="แยกให้ออกว่ากลไกใดถูกใช้ กลไกใดถูกขัดขวาง "
                 "และผลสุทธิคือได้ความร้อนหรือเสียความร้อน",
        ), BALANCE_TOPIC)
