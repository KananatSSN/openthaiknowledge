"""องค์ประกอบและระดับของระบบนิเวศ

ชีวะ · ม.3 · สสวท. พื้นฐาน
Indicators: ว 1.1 ม.3/1, ว 1.1 ม.3/2

Sets moved here from: biology, science_wave_b.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.content import text
from otk.core.distractors import label_pool
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.classify import Category, ClassifyType
from otk.kit.concept_bank import contextual_scenario_question
from otk.sets._support.biology import SUBJECT, TOPIC_ECOLOGY
from otk.sets._support.science_wave_b import INTERACTION_SURVEYS, LEVEL, TOPIC

PROVENANCE = Provenance("original")


class Level(NamedTuple):
    """One level of ecological organization, in ascending (smaller → larger) order."""
    th: str
    en: str
    examples: tuple[str, ...]
    definition: str


def _level_name(lv: Level) -> str:
    return f"{lv.th} ({lv.en})"


@question_type("ecology.levels",
               display_name={"th": "ระดับการจัดระบบทางนิเวศวิทยา"},
               level={"th": "ป.6"}, subject=SUBJECT, topic=TOPIC_ECOLOGY)
class EcoLevels(QuestionType):
    """ระดับการจัดระบบทางนิเวศวิทยา สิ่งมีชีวิต → ชีวมณฑล.

    ``ask`` pins one style (``1`` = จากตัวอย่าง, ``2`` = จากความหมาย,
    ``3`` = ระดับที่ใหญ่ถัดขึ้นไป); ``0`` draws one per item.
    """

    # Ascending: each level nests inside the next.
    LEVELS = [
        Level("สิ่งมีชีวิต", "Organism",
              ("กระต่ายหนึ่งตัว", "ต้นมะม่วงหนึ่งต้น", "ปลาหนึ่งตัวในบ่อ"),
              "สิ่งมีชีวิตหนึ่งหน่วยหรือหนึ่งตัว"),
        Level("ประชากร", "Population",
              ("ฝูงช้าง 20 ตัวในป่าแห่งหนึ่ง", "ต้นสักทั้งหมดในป่าแห่งหนึ่ง",
               "ปลานิลทั้งหมดในบ่อเดียวกัน"),
              "สิ่งมีชีวิตชนิดเดียวกันที่อาศัยอยู่ในบริเวณเดียวกันและช่วงเวลาเดียวกัน"),
        Level("กลุ่มสิ่งมีชีวิต", "Community",
              ("สิ่งมีชีวิตทุกชนิดที่อาศัยอยู่ในสระน้ำแห่งหนึ่ง",
               "พืชและสัตว์ทุกชนิดที่อาศัยอยู่ร่วมกันในป่า"),
              "ประชากรของสิ่งมีชีวิตหลายชนิดที่อาศัยอยู่ร่วมกันในบริเวณเดียวกัน"),
        Level("ระบบนิเวศ", "Ecosystem",
              ("สระน้ำพร้อมทั้งสิ่งมีชีวิตและสิ่งแวดล้อมทางกายภาพ",
               "ป่าไม้ทั้งสิ่งมีชีวิตและสิ่งแวดล้อมที่ไม่มีชีวิต"),
              "กลุ่มสิ่งมีชีวิตกับสิ่งแวดล้อมทางกายภาพที่สัมพันธ์กัน "
              "มีการถ่ายทอดพลังงานและหมุนเวียนสาร"),
        Level("ชีวมณฑล", "Biosphere",
              ("ทุกบริเวณบนโลกที่มีสิ่งมีชีวิตอาศัยอยู่",
               "ผลรวมของระบบนิเวศทั้งหมดบนโลก"),
              "ผลรวมของระบบนิเวศทั้งหมดบนโลก เป็นระดับที่ใหญ่ที่สุด"),
    ]
    ASKS = ("example", "definition", "order")

    def build(self, rng: Random, ask: int = 0) -> GeneratedQuestion:
        levels = self.LEVELS
        names = [_level_name(lv) for lv in levels]
        asked = (self.ASKS[ask - 1] if 1 <= ask <= len(self.ASKS)
                 else rng.choice(self.ASKS))

        if asked == "example":
            lv = rng.choice(levels)
            ex = rng.choice(lv.examples)
            return GeneratedQuestion(
                stem=[text(f"“{ex}” จัดอยู่ในระดับการจัดระบบทางนิเวศวิทยาระดับใด")],
                correct=[text(_level_name(lv))],
                distractors=label_pool(names),
                topic=self.topic,
            )
        if asked == "definition":
            lv = rng.choice(levels)
            return GeneratedQuestion(
                stem=[text(f"ข้อใดคือความหมายของ “{lv.th}” "
                           f"ในการจัดระบบทางนิเวศวิทยา")],
                correct=[text(lv.definition)],
                distractors=label_pool([x.definition for x in levels]),
                topic=self.topic,
            )
        # order: name the level one step larger (ranks 0..n-2 have a larger neighbour)
        i = rng.randrange(len(levels) - 1)
        return GeneratedQuestion(
            stem=[text(f"ระดับที่ใหญ่ถัดขึ้นไปจาก “{_level_name(levels[i])}” "
                       f"หนึ่งระดับคือข้อใด")],
            correct=[text(_level_name(levels[i + 1]))],
            distractors=label_pool(names),
            topic=self.topic,
        )


@question_type(
    "ecology.ecosystem_components_fluency",
    display_name={"th": "องค์ประกอบของระบบนิเวศจากการสำรวจ"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class EcosystemComponentsFluency(ClassifyType):
    """Sort what a survey turns up into the four roles an ecosystem has.

    `ecology.levels` names the nested levels from สิ่งมีชีวิต up to ชีวมณฑล. It
    never asks what a single ecosystem is *made of*, which is where ม.3/1 starts:
    a decomposer and a consumer are both สิ่งมีชีวิต at that level, and telling
    them apart is the step the interaction question then depends on.
    """

    CLASSIFY_STEM = "จากการสำรวจระบบนิเวศแห่งหนึ่ง พบ “{member}” สิ่งนี้เป็นองค์ประกอบชนิดใด"
    PICK_STEM = "ข้อใดที่พบจากการสำรวจจัดเป็น{category}"

    CATEGORIES = [
        Category("องค์ประกอบทางกายภาพ (ไม่มีชีวิต)",
                 ("แสงจากดวงอาทิตย์ที่ส่องถึงผิวน้ำ",
                  "อุณหภูมิของน้ำในสระ",
                  "แร่ธาตุที่ละลายอยู่ในดิน",
                  "ปริมาณแก๊สออกซิเจนที่ละลายในน้ำ",
                  "ความเป็นกรด-เบสของดิน",
                  "ปริมาณน้ำฝนในรอบปี")),
        Category("ผู้ผลิต",
                 ("สาหร่ายสีเขียวที่ลอยอยู่ในน้ำ",
                  "ต้นจอกและแหนที่ปกคลุมผิวน้ำ",
                  "หญ้าที่ขึ้นรอบขอบสระ",
                  "ต้นไม้ใหญ่ที่ให้ร่มเงาแก่สระ",
                  "แพลงก์ตอนพืชในน้ำ")),
        Category("ผู้บริโภค",
                 ("ลูกอ๊อดที่ว่ายอยู่ในน้ำ",
                  "ปลานิลที่กินแพลงก์ตอนพืช",
                  "นกยางที่ลงมาจับปลา",
                  "หอยขมที่เกาะอยู่ตามพื้นสระ",
                  "แมลงปอที่บินอยู่เหนือผิวน้ำ")),
        Category("ผู้ย่อยสลายสารอินทรีย์",
                 ("แบคทีเรียที่ย่อยซากใบไม้ที่ทับถมอยู่ก้นสระ",
                  "เห็ดราที่ขึ้นบนขอนไม้ผุ",
                  "ราที่ย่อยสลายซากสัตว์ที่ตายแล้ว",
                  "จุลินทรีย์ในดินที่เปลี่ยนซากพืชให้เป็นแร่ธาตุ")),
    ]


@question_type(
    "ecology.ecosystem_interaction_application",
    display_name={"th": "อธิบายปฏิสัมพันธ์ขององค์ประกอบของระบบนิเวศจากผลการสำรวจ"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class EcosystemInteractionApplication(QuestionType):
    """Read a survey result and say which component acted on which.

    This is ``ม.3/1`` stated as it is written: an interaction explained *from a
    survey*. Each wrong choice reverses the direction of the effect, swaps cause
    for consequence, or denies that a physical factor is part of the ecosystem —
    the three ways the reasoning actually fails.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return contextual_scenario_question(
            rng, INTERACTION_SURVEYS,
            hint="ไล่ลำดับว่าอะไรเปลี่ยนก่อนและอะไรเปลี่ยนตาม แล้วดูว่าองค์ประกอบ"
                 "ที่เปลี่ยนก่อนนั้นเป็นองค์ประกอบทางกายภาพหรือสิ่งมีชีวิต",
            topic=TOPIC,
        )
