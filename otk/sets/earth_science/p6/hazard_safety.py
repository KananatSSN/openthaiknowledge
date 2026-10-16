"""การเฝ้าระวังและปฏิบัติตนจากภัยธรรมชาติ

ธรณีวิทยา · ป.6 · สสวท. พื้นฐาน
Indicators: ว 3.2 ป.6/7

Sets moved here from: science_wave_c15.
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
from otk.sets._support.science_wave_b17 import PRIMARY_SIX
from otk.sets._support.science_wave_c10 import SUBJECT
from otk.sets._support.science_wave_c15 import SAFETY_SCENARIOS

PROVENANCE = Provenance("original")


SAFETY_TOPIC = "การเฝ้าระวังและปฏิบัติตนจากภัยธรรมชาติ"


MONITOR = "เฝ้าระวัง"


ACT = "ปฏิบัติตนให้ปลอดภัย"


class Plan(NamedTuple):
    """A local hazard, how to watch for it, and what to do when it comes."""
    hazard: str
    situation: str
    monitor: str
    act: str


# Monitoring and acting are specific to each hazard, so another hazard's half is
# always wrong for a case: watching a river says nothing about a tsunami.
PLANS = (
    Plan("น้ำท่วม",
         "หมู่บ้านของนักเรียนอยู่ริมแม่น้ำ และถูกน้ำท่วมเกือบทุกปีในช่วงปลายฤดูฝน",
         "ติดตามระดับน้ำในแม่น้ำและประกาศเตือนน้ำท่วมของหน่วยงานในพื้นที่",
         "ขนย้ายสิ่งของขึ้นที่สูงและตัดกระแสไฟฟ้าก่อนน้ำเข้าบ้าน"),
    Plan("ดินถล่ม",
         "โรงเรียนของนักเรียนตั้งอยู่เชิงเขาที่ป่าถูกบุกรุก และเคยมีดินสไลด์เมื่อฝนตกหนักหลายวัน",
         "สังเกตน้ำในลำห้วยที่ขุ่นข้นผิดปกติและเสียงดังจากภูเขาขณะฝนตกหนัก",
         "อพยพออกจากพื้นที่เชิงเขาไปยังจุดปลอดภัยที่นัดหมายไว้ทันที"),
    Plan("แผ่นดินไหว",
         "จังหวัดของนักเรียนอยู่ใกล้รอยเลื่อนที่ยังมีพลัง และเคยรู้สึกถึงแผ่นดินไหวหลายครั้ง",
         "ติดตามข่าวแผ่นดินไหวและตรวจรอยร้าวของอาคารอย่างสม่ำเสมอ",
         "หมอบลง หาที่กำบังใต้โต๊ะที่แข็งแรง และจับขาโต๊ะไว้จนกว่าจะหยุดสั่น"),
    Plan("สึนามิ",
         "บ้านของนักเรียนอยู่ริมชายหาดฝั่งทะเลอันดามัน ซึ่งเคยเกิดคลื่นสึนามิมาแล้ว",
         "ฟังสัญญาณเตือนภัยสึนามิ และสังเกตน้ำทะเลที่ลดลงอย่างรวดเร็วหลังแผ่นดินไหว",
         "วิ่งขึ้นที่สูงหรืออาคารสูงที่แข็งแรงให้ห่างจากชายฝั่งทันที"),
)


# More ways to watch for each hazard and to act when it comes. Like PLANS, each
# line fits its own hazard only, so it is wrong for any other.
MORE_PLAN_LINES = {
    "น้ำท่วม": (
        ("สังเกตระดับน้ำที่หลักวัดระดับน้ำริมตลิ่งทุกวันในช่วงฤดูฝน",
         "ฟังพยากรณ์ปริมาณฝนและประกาศระดับน้ำในแม่น้ำจากหน่วยงานน้ำ"),
        ("ไม่ลงลุยน้ำที่ไหลเชี่ยว และอพยพไปยังที่สูงเมื่อได้รับประกาศ",
         "เตรียมน้ำดื่มและอาหารแห้งไว้บนชั้นบนของบ้านก่อนน้ำขึ้น"),
    ),
    "ดินถล่ม": (
        ("วัดปริมาณฝนสะสมด้วยกระบอกวัดฝนของหมู่บ้านในช่วงฝนตกหนัก",
         "สังเกตรอยแยกบนพื้นดินและต้นไม้ที่เอียงผิดปกติบนลาดเขา"),
        ("ออกห่างจากลำห้วยและเชิงเขาเมื่อฝนตกหนักติดต่อกันหลายวัน",
         "ไม่พักหรือหลบฝนใกล้ทางน้ำไหลและลาดเขาชันระหว่างฝนตกหนัก"),
    ),
    "แผ่นดินไหว": (
        ("ติดตามประกาศแผ่นดินไหวของกรมอุตุนิยมวิทยาผ่านแอปเตือนภัย",
         "ตรวจว่าตู้และชั้นวางของในบ้านยึดติดผนังไว้แน่นหนา"),
        ("อยู่ห่างจากหน้าต่างกระจกและสิ่งของที่อาจล้มทับระหว่างที่พื้นสั่น",
         "เมื่อหยุดสั่นแล้วจึงออกจากอาคารทางบันได ไม่ใช้ลิฟต์"),
    ),
    "สึนามิ": (
        ("ติดตามประกาศจากหอเตือนภัยสึนามิริมชายฝั่ง",
         "จดจำเส้นทางอพยพและป้ายบอกทางหนีสึนามิในชุมชน"),
        ("ไม่ลงไปเก็บปลาหรือหอยเมื่อน้ำทะเลลดลงผิดปกติ แต่รีบออกจากชายหาด",
         "อยู่บนที่สูงจนกว่าจะมีประกาศว่าปลอดภัย เพราะอาจมีคลื่นลูกต่อไป"),
    ),
}


def _monitor(rng: Random, plan) -> str:
    return rng.choice((plan.monitor, *MORE_PLAN_LINES[plan.hazard][0]))


def _act(rng: Random, plan) -> str:
    return rng.choice((plan.act, *MORE_PLAN_LINES[plan.hazard][1]))


def _plan(monitor: str, act: str) -> str:
    return f"{MONITOR}โดย{monitor} และ{ACT}โดย{act}"


@question_type(
    "geo.hazard_safety_foundation",
    display_name={"th": "สัญญาณเตือนและการปฏิบัติตนจากภัยแต่ละชนิด"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=SAFETY_TOPIC,
)
class HazardSafetyFoundation(QuestionType):
    """One half of a plan at a time: how to watch for a hazard, or what to do."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        plan = rng.choice(PLANS)
        others = [other for other in PLANS if other.hazard != plan.hazard]
        if rng.random() < 0.5:
            return _labelled(
                stem=f"ข้อใดเป็นการเฝ้าระวัง{plan.hazard}ที่เหมาะสม",
                correct=_monitor(rng, plan),
                wrongs=tuple(_monitor(rng, other) for other in others),
                hint="การเฝ้าระวังคือติดตามสัญญาณก่อนภัยนั้นจะมาถึง",
                topic=SAFETY_TOPIC,
            )
        return _labelled(
            stem=f"เมื่อเกิด{plan.hazard} ข้อใดเป็นการปฏิบัติตนให้ปลอดภัยที่สุด",
            correct=_act(rng, plan),
            wrongs=tuple(_act(rng, other) for other in others),
            hint="นึกว่าอันตรายของภัยนั้นมาจากทิศทางใด แล้วหลบให้พ้น",
            topic=SAFETY_TOPIC,
        )


@question_type(
    "geo.hazard_safety_fluency",
    display_name={"th": "เสนอแนวทางเฝ้าระวังและปฏิบัติตนจากภัยในท้องถิ่น"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=SAFETY_TOPIC,
)
class HazardSafetyFluency(QuestionType):
    """Propose both halves of a plan for a local hazard; a wrong choice gets one wrong."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        plan = rng.choice(PLANS)
        others = [other for other in PLANS if other.hazard != plan.hazard]
        rng.shuffle(others)
        return _labelled(
            stem=f"{plan.situation} ควรเสนอแนวทางใดในการเฝ้าระวังและปฏิบัติตนให้ปลอดภัยจากภัยที่อาจเกิดในท้องถิ่นนี้",
            correct=_plan(_monitor(rng, plan), _act(rng, plan)),
            wrongs=(_plan(_monitor(rng, others[0]), plan.act),
                    _plan(plan.monitor, _act(rng, others[1])),
                    _plan(_monitor(rng, others[2]), _act(rng, others[2])),
                    # Both halves wrong, crossed between two other hazards.
                    _plan(_monitor(rng, others[1]), _act(rng, others[0])),
                    _plan(_monitor(rng, others[0]), _act(rng, others[2]))),
            hint="หาภัยที่ท้องถิ่นนี้เสี่ยงก่อน แล้วตรวจทั้งส่วนเฝ้าระวังและส่วนปฏิบัติตนว่าตรงกับภัยนั้น",
            topic=SAFETY_TOPIC,
        )


@question_type(
    "geo.hazard_safety_application",
    display_name={"th": "วางแผนรับมือภัยธรรมชาติในโรงเรียนและชุมชน"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=SAFETY_TOPIC,
)
class HazardSafetyApplication(QuestionType):
    """Plan a drill, refuse a dangerous choice, and see why plans differ by place."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, SAFETY_SCENARIOS,
            hint="นึกว่าอันตรายที่แท้จริงของภัยนั้นคืออะไร แล้วเลือกทางที่หลีกเลี่ยงอันตรายนั้นได้",
        ), SAFETY_TOPIC)
