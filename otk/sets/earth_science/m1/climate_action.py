"""การปฏิบัติตนภายใต้การเปลี่ยนแปลงภูมิอากาศ

ธรณีวิทยา · ม.1 · สสวท. พื้นฐาน
Indicators: ว 3.2 ม.1/7

Sets moved here from: science_wave_c18.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b2 import LEVEL as MIDDLE_ONE
from otk.sets._support.science_wave_b9 import Care, Need, care_fluency, scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c10 import SUBJECT
from otk.sets._support.science_wave_c18 import CLIMATE_ACTION_SCENARIOS

PROVENANCE = Provenance("original")


CLIMATE_ACTION_TOPIC = "การปฏิบัติตนภายใต้การเปลี่ยนแปลงภูมิอากาศ"


CLIMATE_CARE = (
    Care("ดื่มน้ำให้เพียงพอ หลีกเลี่ยงแดดจัดช่วงบ่าย และดูแลผู้สูงอายุในบ้าน",
         "คลื่นความร้อนที่เกิดบ่อยขึ้นทำให้ร่างกายเสียน้ำและเสี่ยงต่อโรคลมแดด"),
    Care("รองเก็บน้ำฝนไว้ใช้และปลูกพืชที่ใช้น้ำน้อย",
         "ภัยแล้งที่ยาวนานขึ้นทำให้น้ำมีไม่พอใช้ตลอดปี"),
    Care("กำจัดแหล่งน้ำขังรอบบ้านที่เป็นแหล่งเพาะพันธุ์ยุง",
         "อากาศที่อุ่นและชื้นขึ้นทำให้ยุงแพร่พันธุ์ได้นานและกว้างขึ้น โรคไข้เลือดออกจึงระบาดมากขึ้น"),
    Care("ยกของใช้สำคัญไว้ที่สูงและติดตามประกาศเตือนน้ำท่วม",
         "ฝนที่ตกหนักขึ้นในช่วงสั้น ๆ ทำให้น้ำท่วมฉับพลันบ่อยขึ้น"),
    Care("ร่วมปลูกและดูแลป่าชายเลนในชุมชนชายฝั่ง",
         "ระดับน้ำทะเลที่สูงขึ้นทำให้คลื่นกัดเซาะชายฝั่งรุนแรงขึ้น"),
    Care("ปลูกไม้ยืนต้นให้ร่มเงาและเปิดให้อากาศถ่ายเทในอาคารแทนการปิดทึบ",
         "อุณหภูมิที่สูงขึ้นทำให้อาคารที่ร้อนอบอ้าวต้องใช้พลังงานทำความเย็นมากขึ้น"),
)


CLIMATE_NEEDS = (
    Need("ช่วงหลายปีหลัง หมู่บ้านของนักเรียนมีวันที่อุณหภูมิสูงเกิน 40 องศาเซลเซียสบ่อยขึ้น และคุณยายที่อยู่บ้านเพลียแดดบ่อย "
         "ควรเสนอแนวทางปฏิบัติตนใดที่ตรงกับปัญหาที่สุด",
         "ดื่มน้ำให้เพียงพอ หลีกเลี่ยงแดดจัดช่วงบ่าย และดูแลผู้สูงอายุในบ้าน"),
    Need("ฤดูแล้งในชุมชนยาวนานขึ้นทุกปี จนบ่อน้ำแห้งก่อนฝนมา "
         "ควรเสนอแนวทางปฏิบัติตนใดที่ตรงกับปัญหาที่สุด",
         "รองเก็บน้ำฝนไว้ใช้และปลูกพืชที่ใช้น้ำน้อย"),
    Need("ชุมชนมีผู้ป่วยไข้เลือดออกเพิ่มขึ้นและระบาดนานขึ้นกว่าในอดีต "
         "ควรเสนอแนวทางปฏิบัติตนใดที่ตรงกับปัญหาที่สุด",
         "กำจัดแหล่งน้ำขังรอบบ้านที่เป็นแหล่งเพาะพันธุ์ยุง"),
    Need("ฝนตกหนักในช่วงสั้น ๆ บ่อยขึ้น จนน้ำท่วมฉับพลันเข้าบ้านหลายครั้งในปีเดียว "
         "ควรเสนอแนวทางปฏิบัติตนใดที่ตรงกับปัญหาที่สุด",
         "ยกของใช้สำคัญไว้ที่สูงและติดตามประกาศเตือนน้ำท่วม"),
    Need("ชายหาดหน้าหมู่บ้านถูกคลื่นกัดเซาะจนแคบลงทุกปีเมื่อน้ำทะเลขึ้นสูงกว่าเดิม "
         "ควรเสนอแนวทางปฏิบัติตนใดที่ตรงกับปัญหาที่สุด",
         "ร่วมปลูกและดูแลป่าชายเลนในชุมชนชายฝั่ง"),
    Need("ห้องเรียนชั้นบนของโรงเรียนร้อนอบอ้าวขึ้นทุกปี จนต้องเปิดพัดลมทุกตัวทั้งวัน และรอบอาคารไม่มีต้นไม้เลย "
         "ควรเสนอแนวทางปฏิบัติตนใดที่ตรงกับปัญหาที่สุด",
         "ปลูกไม้ยืนต้นให้ร่มเงาและเปิดให้อากาศถ่ายเทในอาคารแทนการปิดทึบ"),
)


@question_type(
    "geo.climate_action_foundation",
    display_name={"th": "เหตุผลของแนวทางปรับตัวต่อการเปลี่ยนแปลงภูมิอากาศ"},
    level=MIDDLE_ONE, subject=SUBJECT, topic=CLIMATE_ACTION_TOPIC,
)
class ClimateActionFoundation(QuestionType):
    """Match a practice to the climate change it answers, in either direction."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(CLIMATE_CARE)
        others = [other for other in CLIMATE_CARE if other.practice != item.practice]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"แนวทาง “{item.practice}” ช่วยรับมือกับการเปลี่ยนแปลงภูมิอากาศเรื่องใด",
                correct=item.reason,
                wrongs=tuple(other.reason for other in others[:3]),
                hint="นึกว่าแนวทางนั้นป้องกันอันตรายใดโดยตรง",
                topic=CLIMATE_ACTION_TOPIC,
            )
        return _labelled(
            stem=f"แนวทางใดช่วยรับมือได้ เมื่อ{item.reason}",
            correct=item.practice,
            wrongs=tuple(other.practice for other in others[:3]),
            hint="นึกว่าแนวทางนั้นป้องกันอันตรายใดโดยตรง",
            topic=CLIMATE_ACTION_TOPIC,
        )


@question_type(
    "geo.climate_action_fluency",
    display_name={"th": "เสนอแนวทางปฏิบัติตนภายใต้การเปลี่ยนแปลงภูมิอากาศ"},
    level=MIDDLE_ONE, subject=SUBJECT, topic=CLIMATE_ACTION_TOPIC,
)
class ClimateActionFluency(QuestionType):
    """Put forward the practice that fits a case — the indicator's own clause."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(care_fluency(
            rng, needs=CLIMATE_NEEDS, cares=CLIMATE_CARE,
            hint="หาว่าภูมิอากาศที่เปลี่ยนไปทำให้เกิดปัญหาใดในเรื่อง แล้วเลือกแนวทางที่รับมือกับปัญหานั้นโดยตรง",
        ), CLIMATE_ACTION_TOPIC)


@question_type(
    "geo.climate_action_application",
    display_name={"th": "วางแผนปรับตัวและลดผลกระทบจากการเปลี่ยนแปลงภูมิอากาศ"},
    level=MIDDLE_ONE, subject=SUBJECT, topic=CLIMATE_ACTION_TOPIC,
)
class ClimateActionApplication(QuestionType):
    """Find an action that both mitigates and adapts, and adapt a farm to erratic rain."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, CLIMATE_ACTION_SCENARIOS,
            hint="แยกให้ออกว่าแนวทางใดลดสาเหตุ แนวทางใดช่วยรับมือ และแนวทางใดทำได้ทั้งสองอย่าง",
        ), CLIMATE_ACTION_TOPIC)
