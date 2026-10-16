"""ผลกระทบของการตั้งครรภ์ก่อนวัยอันควร

ชีวะ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.2/17

Sets moved here from: science_wave_b13.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import LEVEL, SUBJECT, TOPIC, labelled, scenario_question
from otk.sets._support.science_wave_b13 import TEEN_PREGNANCY_SCENARIOS

PROVENANCE = Provenance("original")


class Impact(NamedTuple):
    """One side of life the early pregnancy affects, and how."""
    aspect: str
    effect: str


IMPACTS = (
    Impact("ต่อสุขภาพของแม่วัยรุ่น",
           "ร่างกายที่ยังเจริญเติบโตไม่เต็มที่ทำให้เสี่ยงต่อภาวะแทรกซ้อนขณะตั้งครรภ์"
           "และขณะคลอดมากกว่าผู้ที่โตเต็มวัย"),
    Impact("ต่อสุขภาพของทารก",
           "ทารกมีโอกาสคลอดก่อนกำหนดและมีน้ำหนักแรกเกิดน้อยกว่าเกณฑ์มากกว่าปกติ"),
    Impact("ต่อการเรียน",
           "การตั้งครรภ์ในวัยเรียนมักทำให้ต้องหยุดเรียนหรือออกจากระบบการศึกษากลางคัน"),
    Impact("ต่อโอกาสในอนาคต",
           "การศึกษาที่ไม่ต่อเนื่องทำให้ทางเลือกในการทำงานและรายได้ในระยะยาวลดลง"),
    Impact("ต่อสภาพจิตใจ",
           "การเปลี่ยนบทบาทอย่างกะทันหันพร้อมกับแรงกดดันรอบตัวทำให้เกิดความเครียด"
           "และความวิตกกังวลสูง"),
    Impact("ต่อครอบครัว",
           "ภาระการเลี้ยงดูมักตกอยู่กับครอบครัวซึ่งอาจยังไม่ได้เตรียมพร้อมมาก่อน"),
)


class Conduct(NamedTuple):
    """A situation, and the way of behaving that fits it."""
    situation: str
    action: str


# Every ``action`` appears once, so the situation question has one answer and its
# distractors are other real courses of action rather than obviously bad ones.
CONDUCTS = (
    Conduct("เพื่อนชวนนักเรียนไปค้างคืนที่บ้านซึ่งไม่มีผู้ใหญ่อยู่ด้วย "
            "และนักเรียนรู้สึกไม่สบายใจ ควรประพฤติตนอย่างไร",
            "ปฏิเสธอย่างหนักแน่นและอธิบายเหตุผลของตนเอง โดยไม่ต้องกลัวว่าจะเสียเพื่อน"),
    Conduct("ในงานเลี้ยง มีผู้ชวนนักเรียนดื่มเครื่องดื่มแอลกอฮอล์โดยบอกว่าดื่มนิดหน่อย"
            "ไม่เป็นไร ควรประพฤติตนอย่างไร",
            "ไม่ดื่ม เพราะแอลกอฮอล์ทำให้การตัดสินใจแย่ลงจนอาจนำไปสู่สถานการณ์"
            "ที่ควบคุมไม่ได้"),
    Conduct("นักเรียนไม่แน่ใจว่าข้อมูลเรื่องเพศที่อ่านจากสื่อออนไลน์ถูกต้องหรือไม่ "
            "ควรประพฤติตนอย่างไร",
            "ตรวจสอบกับแหล่งข้อมูลที่เชื่อถือได้ หรือปรึกษาครูหรือผู้ปกครอง "
            "แทนการเชื่อตามที่มีคนแชร์ต่อกันมา"),
    Conduct("แฟนของนักเรียนกดดันให้มีเพศสัมพันธ์โดยบอกว่าเป็นการพิสูจน์ความรัก "
            "ควรประพฤติตนอย่างไร",
            "ปฏิเสธและยืนยันสิทธิ์ในการตัดสินใจเรื่องร่างกายของตนเอง "
            "เพราะความรักไม่ควรมาพร้อมกับการบังคับ"),
    Conduct("นักเรียนมีความกังวลเกี่ยวกับความสัมพันธ์และไม่กล้าปรึกษาใคร "
            "ควรประพฤติตนอย่างไร",
            "หาผู้ใหญ่ที่ไว้ใจได้ เช่น ครูหรือผู้ปกครอง เพื่อขอคำแนะนำ "
            "แทนการเก็บไว้คนเดียวหรือถามจากคนที่ไม่มีข้อมูลที่ถูกต้อง"),
    Conduct("นักเรียนยังไม่เคยคิดถึงเป้าหมายของตนเองหลังจบการศึกษา "
            "ควรประพฤติตนอย่างไรเพื่อลดความเสี่ยงของการตั้งครรภ์ก่อนวัยอันควร",
            "วางแผนการเรียนและเป้าหมายชีวิตของตนเองไว้ล่วงหน้า "
            "เพื่อให้การตัดสินใจในแต่ละครั้งสอดคล้องกับเป้าหมายนั้น"),
)


@question_type(
    "body.teen_pregnancy_foundation",
    display_name={"th": "ผลกระทบของการตั้งครรภ์ก่อนวัยอันควร"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class TeenPregnancyFoundation(QuestionType):
    """Name the effect on one side of life, or the side of life affected."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(IMPACTS)
        others = [other for other in IMPACTS if other.aspect != item.aspect]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return labelled(
                stem=f"การตั้งครรภ์ก่อนวัยอันควรมีผลกระทบ “{item.aspect}” อย่างไร",
                correct=item.effect,
                wrongs=tuple(other.effect for other in others[:3]),
                hint="แยกก่อนว่าเป็นผลต่อร่างกาย ต่อการเรียนและอนาคต "
                     "หรือต่อจิตใจและครอบครัว",
            )
        return labelled(
            stem=f"ผลกระทบที่ว่า {item.effect} เป็นผลกระทบด้านใด",
            correct=item.aspect,
            wrongs=tuple(other.aspect for other in others[:3]),
            hint="อ่านผลกระทบให้จบ แล้วจึงระบุว่าเป็นเรื่องของใครและด้านใด",
        )


@question_type(
    "body.teen_pregnancy_fluency",
    display_name={"th": "การประพฤติตนเมื่อเผชิญสถานการณ์เสี่ยง"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class TeenPregnancyFluency(QuestionType):
    """Pick the course of action a risky situation calls for.

    ``ม.2/17``'s evidence clause is ``โดยการประพฤติตนให้เหมาะสม`` — conduct, which
    no item can observe. Naming the right course of action is within the standard
    but is not that evidence, so this set is ``standard_scope``.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(CONDUCTS)
        others = [other.action for other in CONDUCTS if other.action != item.action]
        rng.shuffle(others)
        return labelled(
            stem=item.situation,
            correct=item.action,
            wrongs=tuple(others[:3]),
            hint="เลือกแนวทางที่รักษาสิทธิ์ในการตัดสินใจของตนเอง "
                 "และที่ทำให้ได้ข้อมูลหรือความช่วยเหลือที่ถูกต้อง",
        )


@question_type(
    "body.teen_pregnancy_application",
    display_name={"th": "วิเคราะห์ผลกระทบและการตัดสินใจในสถานการณ์เสี่ยง"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class TeenPregnancyApplication(QuestionType):
    """Explain an effect, or judge a piece of advice against what it leads to."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return scenario_question(
            rng, TEEN_PREGNANCY_SCENARIOS,
            hint="ตามผลที่จะเกิดขึ้นต่อไปให้ครบทั้งด้านร่างกาย การเรียน "
                 "และจิตใจ ก่อนตัดสินว่าแนวทางใดเหมาะสม",
        )


# Two more situations. Each action answers its own situation only, and no
# earlier action fits these situations.
CONDUCTS = (*CONDUCTS,
    Conduct("คนแปลกหน้าในโซเชียลมีเดียขอรูปส่วนตัวของนักเรียน และชวนออกไปพบกันตามลำพัง "
            "ควรประพฤติตนอย่างไร",
            "ไม่ส่งรูปและไม่ไปพบตามลำพัง แล้วบล็อกบัญชีนั้น "
            "พร้อมเล่าให้ผู้ปกครองหรือครูทราบ"),
    Conduct("มีคนส่งภาพลามกเข้ามาในกลุ่มแชตของห้อง และเพื่อนหลายคนกำลังส่งต่อกัน "
            "ควรประพฤติตนอย่างไร",
            "ไม่ส่งต่อและไม่ร่วมแสดงความเห็น ลบภาพนั้นออก "
            "แล้วแจ้งครูหรือผู้ปกครองให้ช่วยจัดการ"),
)
