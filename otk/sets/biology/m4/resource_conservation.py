"""ปัญหาและการอนุรักษ์ทรัพยากรธรรมชาติและสิ่งแวดล้อม

ชีวะ · ม.4 · สสวท. พื้นฐาน
Indicators: ว 1.1 ม.4/4

Sets moved here from: science_wave_b33.
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
from otk.sets._support.science_wave_b19 import UPPER_FOUR
from otk.sets._support.science_wave_b31 import ECOLOGY_TOPIC
from otk.sets._support.science_wave_b33 import CONSERVATION_SCENARIOS

PROVENANCE = Provenance("original")


RESOURCE = "ทรัพยากรธรรมชาติ"


ENVIRONMENT = "สิ่งแวดล้อม"


class Problem(NamedTuple):
    """A problem, what it damages, a case of it, its impact and its remedy."""
    problem: str
    target: str
    situation: str
    impact: str
    solution: str


PROBLEMS = (
    Problem("การตัดไม้ทำลายป่าต้นน้ำ", RESOURCE,
            "ป่าบนภูเขาเหนือหมู่บ้านถูกตัดโค่นเป็นบริเวณกว้าง "
            "และหมู่บ้านเกิดน้ำป่าไหลหลากทุกฤดูฝน",
            "ดินพังทลายและน้ำหลากง่ายขึ้น เพราะไม่มีรากไม้ยึดดินและชะลอน้ำ "
            "และสัตว์ป่าเสียที่อยู่",
            "ปลูกป่าทดแทนและกำหนดเขตป่าต้นน้ำที่ห้ามตัดไม้"),
    Problem("การทำประมงเกินขนาดด้วยอวนตาถี่", RESOURCE,
            "ชาวประมงใช้อวนตาถี่จับสัตว์น้ำได้ทั้งตัวเล็กและตัวใหญ่ "
            "และจับได้น้อยลงทุกปี",
            "สัตว์น้ำถูกจับก่อนโตพอจะสืบพันธุ์ ประชากรจึงฟื้นตัวไม่ทัน",
            "กำหนดขนาดตาอวนขั้นต่ำและปิดอ่าวในฤดูวางไข่"),
    Problem("การสูบน้ำบาดาลมากเกินไป", RESOURCE,
            "เมืองใหญ่สูบน้ำบาดาลขึ้นมาใช้ปริมาณมากต่อเนื่องหลายปี "
            "และพบว่าพื้นดินบางบริเวณทรุดลง",
            "ระดับน้ำใต้ดินลดลงจนแผ่นดินทรุด และน้ำเค็มอาจรุกเข้าชั้นน้ำใต้ดิน",
            "ควบคุมปริมาณการสูบน้ำบาดาลและหันไปใช้น้ำประปาจากแหล่งน้ำผิวดิน"),
    Problem("การปลูกพืชชนิดเดียวซ้ำในที่เดิมเป็นเวลานาน", RESOURCE,
            "แปลงที่ปลูกข้าวโพดชนิดเดียวติดต่อกันหลายปีให้ผลผลิตลดลงทุกปี "
            "แม้ดูแลเหมือนเดิม",
            "ธาตุอาหารบางชนิดในดินถูกดึงไปใช้ซ้ำจนหมด ดินจึงเสื่อมโทรม",
            "ปลูกพืชหมุนเวียนสลับกับพืชตระกูลถั่ว"),
    Problem("ขยะพลาสติกที่หลุดลงสู่ทะเล", ENVIRONMENT,
            "ชายหาดท่องเที่ยวมีขวดและถุงพลาสติกถูกคลื่นซัดขึ้นมาทุกวัน "
            "และพบเต่าทะเลตายโดยมีพลาสติกอยู่ในท้อง",
            "สัตว์ทะเลกินหรือติดพลาสติกจนตาย และไมโครพลาสติกเข้าสู่โซ่อาหาร",
            "ลดการใช้พลาสติกแบบใช้ครั้งเดียวทิ้งและคัดแยกขยะไม่ให้หลุดลงทะเล"),
    Problem("ฝุ่นละอองขนาดเล็กจากไอเสียรถยนต์", ENVIRONMENT,
            "เมืองที่มีรถติดหนาแน่นมีค่าฝุ่น PM2.5 เกินมาตรฐานเกือบทุกเช้าในฤดูหนาว",
            "ฝุ่นขนาดเล็กเข้าไปถึงถุงลมปอด ทำให้เกิดโรคระบบทางเดินหายใจ",
            "ใช้ระบบขนส่งสาธารณะมากขึ้นและตรวจสภาพเครื่องยนต์ไม่ให้ปล่อยควันดำ"),
    Problem("การปล่อยน้ำเสียที่มีโลหะหนักจากโรงงาน", ENVIRONMENT,
            "โรงงานริมแม่น้ำปล่อยน้ำทิ้งที่มีสารปรอทลงแม่น้ำ "
            "และพบสารปรอทสะสมในเนื้อปลาที่ชาวบ้านจับได้",
            "โลหะหนักสะสมในสัตว์น้ำและเพิ่มความเข้มข้นตามโซ่อาหารจนถึงมนุษย์",
            "บังคับให้โรงงานบำบัดน้ำเสียให้ได้มาตรฐานก่อนปล่อยออก"),
    Problem("ปุ๋ยเคมีจากแปลงเกษตรไหลลงแหล่งน้ำ", ENVIRONMENT,
            "หลังฝนตกหนักในพื้นที่เกษตร บึงท้ายแปลงมีสาหร่ายขึ้นเขียวเต็มผิวน้ำ "
            "และต่อมาพบปลาตายลอยจำนวนมาก",
            "สาหร่ายเพิ่มจำนวนอย่างรวดเร็ว เมื่อตายและถูกย่อยสลายจะใช้ออกซิเจนในน้ำ"
            "จนสัตว์น้ำขาดออกซิเจน",
            "ใส่ปุ๋ยเท่าที่พืชต้องการและปลูกแนวพืชกันชนริมแหล่งน้ำเพื่อดักปุ๋ยที่ไหลมา"),
)


def _across(item: Problem) -> list[Problem]:
    """Rows about the *other* target.

    Two problems of the same target can share a remedy or an impact — a planted
    forest also slows the loss of farm soil — so wrong choices come from the
    other half of the table, where no overlap can give an item two answers.
    """
    return [other for other in PROBLEMS if other.target != item.target]


@question_type(
    "ecology.resource_conservation_foundation",
    display_name={"th": "ปัญหาและผลกระทบต่อทรัพยากรธรรมชาติและสิ่งแวดล้อม"},
    level=UPPER_FOUR, subject=SUBJECT, topic=ECOLOGY_TOPIC,
)
class ResourceConservationFoundation(QuestionType):
    """Discuss a problem by the impact it has, in either direction."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(PROBLEMS)
        others = _across(item)
        rng.shuffle(others)
        hint = "ตามผลของปัญหาไปทีละขั้น ว่าสิ่งใดถูกทำลายและส่งผลต่อใครต่อ"
        if rng.random() < 0.5:
            return _labelled(
                stem=f"“{item.problem}” ส่งผลกระทบอย่างไร",
                correct=item.impact,
                wrongs=tuple(other.impact for other in others[:3]),
                hint=hint, topic=ECOLOGY_TOPIC,
            )
        return _labelled(
            stem=f"ปัญหาใดทำให้เกิดผลกระทบว่า {item.impact}",
            correct=item.problem,
            wrongs=tuple(other.problem for other in others[:3]),
            hint=hint, topic=ECOLOGY_TOPIC,
        )


@question_type(
    "ecology.resource_conservation_fluency",
    display_name={"th": "นำเสนอแนวทางอนุรักษ์และแก้ไขปัญหา"},
    level=UPPER_FOUR, subject=SUBJECT, topic=ECOLOGY_TOPIC,
)
class ResourceConservationFluency(QuestionType):
    """Put forward the remedy that fits a described case — ``นำเสนอแนวทาง``."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(PROBLEMS)
        others = _across(item)
        rng.shuffle(others)
        return _labelled(
            stem=f"{item.situation} แนวทางใดแก้ไขปัญหานี้ได้ตรงต้นเหตุที่สุด",
            correct=item.solution,
            wrongs=tuple(other.solution for other in others[:3]),
            hint="ระบุต้นเหตุของปัญหาในสถานการณ์ก่อน แล้วเลือกแนวทางที่ลดต้นเหตุนั้นโดยตรง",
            topic=ECOLOGY_TOPIC,
        )


@question_type(
    "ecology.resource_conservation_application",
    display_name={"th": "วิเคราะห์แนวทางอนุรักษ์ทรัพยากรและสิ่งแวดล้อม"},
    level=UPPER_FOUR, subject=SUBJECT, topic=ECOLOGY_TOPIC,
)
class ResourceConservationApplication(QuestionType):
    """Weigh a proposed remedy: its cost, its reach, and how long it takes."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, CONSERVATION_SCENARIOS,
            hint="ถามว่าแนวทางนั้นแก้ที่ต้นเหตุหรือแค่ลดอาการ "
                 "และผลจะยั่งยืนหรือกระทบผู้ใดบ้าง",
        ), ECOLOGY_TOPIC)
