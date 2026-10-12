"""โครงสร้างและลักษณะของสิ่งมีชีวิตที่เกิดจากการปรับตัว

ชีวะ · ป.5 · สสวท. พื้นฐาน
Indicators: ว 1.1 ป.5/1

Sets moved here from: science_wave_b31.
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
from otk.sets._support.science_wave_b24 import PRIMARY_FIVE
from otk.sets._support.science_wave_b31 import ADAPTATION_SCENARIOS, ECOLOGY_TOPIC

PROVENANCE = Provenance("original")


class Adaptation(NamedTuple):
    """A structure, the organism that has it, where it lives, and what it does."""
    organism: str
    habitat: str
    structure: str
    benefit: str


ADAPTATIONS = (
    Adaptation("ผักตบชวา", "แหล่งน้ำจืด",
               "ก้านใบพองออกและมีช่องอากาศอยู่ภายใน",
               "ลอยอยู่บนผิวน้ำได้"),
    Adaptation("บัว", "แหล่งน้ำจืด",
               "ใบกว้างแบนและมีปากใบอยู่ด้านบนของใบ",
               "ลอยรับแสงและแลกเปลี่ยนแก๊สกับอากาศได้แม้ใบแตะผิวน้ำ"),
    Adaptation("โกงกาง", "ป่าชายเลน",
               "มีรากค้ำจุนแตกออกจากโคนต้นลงสู่ดินเลน",
               "ยึดลำต้นไว้ในดินเลนที่อ่อนนุ่มได้แม้น้ำขึ้นลงทุกวัน"),
    Adaptation("ปลาตีน", "ป่าชายเลน",
               "มีครีบอกแข็งแรงใช้คืบคลาน และเก็บน้ำไว้ในช่องเหงือกได้",
               "เคลื่อนที่และหายใจบนหาดเลนได้ขณะน้ำลง"),
    Adaptation("หมีขั้วโลก", "ขั้วโลกที่หนาวจัด",
               "มีขนหนาและมีชั้นไขมันใต้ผิวหนังหนา",
               "รักษาความอบอุ่นของร่างกายไว้ได้"),
    Adaptation("สุนัขจิ้งจอกอาร์กติก", "ขั้วโลกที่หนาวจัด",
               "ขนเปลี่ยนเป็นสีขาวในฤดูที่หิมะปกคลุม",
               "พรางตัวกลืนกับหิมะ ทำให้ศัตรูและเหยื่อมองเห็นได้ยาก"),
    Adaptation("กระบองเพชร", "ทะเลทรายที่ร้อนและแห้งแล้ง",
               "ใบเปลี่ยนเป็นหนามและลำต้นอวบน้ำ",
               "ลดการสูญเสียน้ำและเก็บน้ำไว้ใช้ได้นาน"),
    Adaptation("อูฐ", "ทะเลทรายที่ร้อนและแห้งแล้ง",
               "มีขนตายาวสองชั้นและปิดรูจมูกได้",
               "ป้องกันทรายไม่ให้เข้าตาและจมูกเมื่อเกิดพายุทราย"),
)


HABITATS = tuple(dict.fromkeys(item.habitat for item in ADAPTATIONS))


@question_type(
    "ecology.adaptation_foundation",
    display_name={"th": "โครงสร้างของสิ่งมีชีวิตกับการดำรงชีวิต"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=ECOLOGY_TOPIC,
)
class AdaptationFoundation(QuestionType):
    """Describe what a structure does for the organism that has it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(ADAPTATIONS)
        # Two structures from the same habitat can share a benefit — a lotus
        # leaf floats too — so wrong benefits come from other habitats only.
        others = [other.benefit for other in ADAPTATIONS
                  if other.habitat != item.habitat]
        rng.shuffle(others)
        return _labelled(
            stem=f"{item.organism}{item.structure} "
                 f"ลักษณะนี้ช่วยให้{item.organism}ดำรงชีวิตได้อย่างไร",
            correct=item.benefit, wrongs=tuple(others[:3]),
            hint="นึกถึงว่าสิ่งมีชีวิตชนิดนั้นอาศัยอยู่ที่ใด "
                 "และที่นั่นมีปัญหาอะไรที่ต้องเอาชนะ",
            topic=ECOLOGY_TOPIC,
        )


@question_type(
    "ecology.adaptation_fluency",
    display_name={"th": "บรรยายลักษณะที่เหมาะกับแหล่งที่อยู่"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=ECOLOGY_TOPIC,
)
class AdaptationFluency(QuestionType):
    """Match a structure to the habitat it suits, in either direction.

    Wrong structures come only from *other* habitats. Two structures from the
    same habitat both help there, and offering one against the other would give
    the item two right answers.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(ADAPTATIONS)
        if rng.random() < 0.5:
            others = [other for other in ADAPTATIONS if other.habitat != item.habitat]
            rng.shuffle(others)
            return _labelled(
                stem=f"ลักษณะใดช่วยให้สิ่งมีชีวิตดำรงชีวิตใน“{item.habitat}”ได้",
                correct=f"{item.structure} ซึ่งช่วยให้{item.benefit}",
                wrongs=tuple(f"{other.structure} ซึ่งช่วยให้{other.benefit}"
                             for other in others[:3]),
                hint="นึกถึงปัญหาหลักของแหล่งที่อยู่นั้นก่อน เช่น ขาดน้ำ หนาวจัด "
                     "หรือดินอ่อนนุ่ม แล้วหาลักษณะที่แก้ปัญหานั้น",
                topic=ECOLOGY_TOPIC,
            )
        places = [habitat for habitat in HABITATS if habitat != item.habitat]
        rng.shuffle(places)
        return _labelled(
            stem=f"สิ่งมีชีวิตที่{item.structure} "
                 f"น่าจะอาศัยอยู่ในแหล่งที่อยู่ใดมากที่สุด",
            correct=item.habitat, wrongs=tuple(places[:3]),
            hint="ถามว่าลักษณะนี้ช่วยแก้ปัญหาอะไร แล้วหาแหล่งที่อยู่ที่มีปัญหานั้น",
            topic=ECOLOGY_TOPIC,
        )


@question_type(
    "ecology.adaptation_application",
    display_name={"th": "วิเคราะห์การปรับตัวของสิ่งมีชีวิต"},
    level=PRIMARY_FIVE, subject=SUBJECT, topic=ECOLOGY_TOPIC,
)
class AdaptationApplication(QuestionType):
    """Explain a case by the fit between structure and habitat."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, ADAPTATION_SCENARIOS,
            hint="หาว่าลักษณะนั้นแก้ปัญหาอะไรในแหล่งที่อยู่เดิม "
                 "แล้วถามว่าสถานการณ์ใหม่ยังมีปัญหานั้นอยู่หรือไม่",
        ), ECOLOGY_TOPIC)
