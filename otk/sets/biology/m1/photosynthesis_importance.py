"""ความสำคัญของการสังเคราะห์ด้วยแสง

ชีวะ · ม.1 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.1/7

Sets moved here from: science_wave_b3.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.concept_bank import (
    Concept,
    ConceptBankType,
    contextual_scenario_question,
    widen,
)
from otk.sets._support.science_wave_b3 import (
    IMPORTANCE_SCENARIOS,
    LEVEL,
    SUBJECT,
    TOPIC,
    _labelled,
)

PROVENANCE = Provenance("original")


# (การเปลี่ยนแปลง, ผลที่เกิดขึ้น). Each row is one change with one consequence,
# and the wrong choices for a row are the consequences of the other rows — real
# effects attached to the wrong cause.
IMPORTANCE_CHANGES = (
    ("ตัดไม้ทำลายป่าเป็นบริเวณกว้าง",
     "แก๊สคาร์บอนไดออกไซด์ในบรรยากาศมีแนวโน้มสูงขึ้น เพราะมีต้นไม้นำไปใช้น้อยลง"),
    ("ปลูกต้นไม้เพิ่มในเมืองเป็นจำนวนมาก",
     "แก๊สออกซิเจนในบริเวณนั้นมีแนวโน้มสูงขึ้น และอากาศร่มเย็นลง"),
    ("น้ำในบ่อขุ่นจนแสงส่องถึงสาหร่ายใต้น้ำได้น้อยลง",
     "สาหร่ายสังเคราะห์ด้วยแสงได้น้อยลง ปริมาณออกซิเจนละลายน้ำจึงลดลง"),
    ("ปิดไฟและปิดม่านห้องที่มีต้นไม้ในกระถางไว้ตลอดทั้งสัปดาห์",
     "ต้นไม้สร้างอาหารไม่ได้ ต้องใช้อาหารที่สะสมไว้จนใบเหลืองและอ่อนแอลง"),
    ("เกิดฝุ่นหนาเกาะบนผิวใบของต้นไม้ริมถนนเป็นเวลานาน",
     "ใบรับแสงได้น้อยลง อัตราการสังเคราะห์ด้วยแสงจึงลดลงและต้นไม้โตช้าลง"),
)


@question_type(
    "plant.photosynthesis_importance_foundation",
    display_name={"th": "ความสำคัญของการสังเคราะห์ด้วยแสงต่อสิ่งมีชีวิต"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class PhotosynthesisImportanceFoundation(ConceptBankType):
    """What the process gives the rest of the living world."""

    ITEMS = widen([
        Concept(
            "การสังเคราะห์ด้วยแสงของพืชสำคัญต่อสัตว์อย่างไร",
            "เป็นแหล่งอาหารและพลังงานเริ่มต้นของสัตว์ทุกชนิด เพราะสัตว์สร้างอาหารเองไม่ได้",
            ("ช่วยให้สัตว์ย่อยอาหารที่กินเข้าไปได้เร็วขึ้น เพราะพืชสร้างเอนไซม์ย่อยอาหารให้สัตว์",
             "ช่วยกำจัดของเสียที่สัตว์ขับถ่ายออกมาให้หมดไป เพราะพืชดูดของเสียทั้งหมดไปใช้",
             "ทำให้สัตว์ไม่ต้องหายใจเอาแก๊สออกซิเจนเข้าไปอีก"),
        ),
        Concept(
            "แก๊สออกซิเจนในบรรยากาศส่วนใหญ่มาจากที่ใด",
            "จากการสังเคราะห์ด้วยแสงของพืชและสาหร่าย",
            ("จากการหายใจของสัตว์ทุกชนิดรวมกัน",
             "จากการระเหยของน้ำในมหาสมุทร",
             "จากการย่อยสลายซากสิ่งมีชีวิตของผู้ย่อยสลาย"),
        ),
        Concept(
            "การสังเคราะห์ด้วยแสงช่วยลดปัญหาใดของสิ่งแวดล้อม",
            "ช่วยลดปริมาณแก๊สคาร์บอนไดออกไซด์ในบรรยากาศ ซึ่งเป็นแก๊สเรือนกระจก",
            ("ช่วยลดปริมาณแก๊สออกซิเจนที่มากเกินไปในบรรยากาศ",
             "ช่วยลดปริมาณน้ำฝนที่ตกหนักเกินไปในฤดูฝน",
             "ช่วยลดปริมาณแสงแดดที่ส่องมายังผิวโลก"),
        ),
        Concept(
            "ข้อใดเปรียบเทียบการสังเคราะห์ด้วยแสงกับการหายใจของพืชได้ถูกต้อง",
            "การสังเคราะห์ด้วยแสงใช้แก๊สคาร์บอนไดออกไซด์และสร้างแก๊สออกซิเจน "
            "ส่วนการหายใจใช้แก๊สออกซิเจนและปล่อยแก๊สคาร์บอนไดออกไซด์",
            ("พืชสังเคราะห์ด้วยแสงในเวลากลางวันและไม่หายใจเลยในเวลากลางคืน",
             "ทั้งสองกระบวนการใช้แก๊สคาร์บอนไดออกไซด์และสร้างแก๊สออกซิเจนเหมือนกัน",
             "การหายใจของพืชเกิดเฉพาะที่รากเท่านั้น ส่วนการสังเคราะห์ด้วยแสงเกิดที่ใบ"),
        ),
        Concept(
            "พลังงานที่มนุษย์ได้รับจากการกินข้าวมีต้นทางมาจากที่ใด",
            "จากพลังงานแสงของดวงอาทิตย์ที่ต้นข้าวเปลี่ยนเป็นพลังงานเคมีในเมล็ด",
            ("จากธาตุอาหารในดินที่ต้นข้าวดูดขึ้นมาสะสมไว้",
             "จากพลังงานความร้อนในดินที่ถ่ายทอดเข้าสู่รากข้าวแล้วสะสมไว้ในเมล็ด",
             "จากพลังงานที่มนุษย์สร้างขึ้นเองในกระบวนการย่อยอาหาร"),
        ),
        Concept(
            "เหตุใดการปลูกป่าจึงช่วยบรรเทาภาวะโลกร้อนได้",
            "เพราะต้นไม้นำคาร์บอนไดออกไซด์ไปสังเคราะห์ด้วยแสงและเก็บคาร์บอนไว้ในเนื้อไม้",
            ("เพราะต้นไม้ปล่อยแก๊สคาร์บอนไดออกไซด์ออกมาแทนที่แก๊สเรือนกระจกชนิดอื่น",
             "เพราะเงาของต้นไม้บังแสงอาทิตย์ไม่ให้ส่องถึงผิวโลกทั้งหมด",
             "เพราะต้นไม้ดูดความร้อนจากอากาศเก็บไว้ในลำต้นอย่างถาวร"),
        ),
        Concept(
            "ถ้าพืชและสาหร่ายบนโลกหายไปทั้งหมด ผลที่ตามมาจะเป็นอย่างไร",
            "ผู้บริโภคทุกลำดับขาดทั้งอาหารและแหล่งเติมแก๊สออกซิเจน ระบบนิเวศทั้งหมดจึงล่มสลาย",
            ("สัตว์จะปรับตัวมาสร้างอาหารเองได้แทนพืชภายในไม่กี่ชั่วอายุ",
             "ผู้ย่อยสลายจะทำหน้าที่ผลิตอาหารแทนพืชได้ทั้งหมด ระบบนิเวศจึงยังคงอยู่ได้ตามปกติ",
             "ปริมาณแก๊สออกซิเจนจะคงเดิม เพราะออกซิเจนในระบบนิเวศไม่ได้มาจากพืชเพียงอย่างเดียว"),
        ),
    ], (
        ("ช่วยให้สัตว์สร้างอาหารได้เองโดยไม่ต้องกินพืช",
         "ช่วยให้สัตว์มีขนและผิวหนังสีเขียว"),
        ("จากภูเขาไฟที่ปะทุ",
         "จากการเผาไหม้เชื้อเพลิงของมนุษย์"),
        ("ช่วยเพิ่มปริมาณแก๊สคาร์บอนไดออกไซด์ในบรรยากาศ",
         "ช่วยลดปริมาณน้ำใต้ดินที่มากเกินไป"),
        ("การหายใจของพืชสร้างแป้งและปล่อยแก๊สออกซิเจน",
         "การสังเคราะห์ด้วยแสงเกิดเฉพาะกลางคืน ส่วนการหายใจเกิดเฉพาะกลางวัน"),
        ("จากน้ำที่ต้นข้าวดูดขึ้นมาเท่านั้น",
         "จากแก๊สออกซิเจนที่ต้นข้าวปล่อยออกมา"),
        ("เพราะต้นไม้ปล่อยความเย็นออกมาทำให้โลกเย็นลงทันที",
         "เพราะต้นไม้ดูดแก๊สออกซิเจนออกจากบรรยากาศ"),
        ("ผู้บริโภคจะเพิ่มจำนวนขึ้นเพราะไม่ต้องแย่งพื้นที่กับพืช",
         "โลกจะมีแก๊สออกซิเจนมากขึ้นเพราะไม่มีพืชมาใช้"),
    ))


@question_type(
    "plant.photosynthesis_importance_fluency",
    display_name={"th": "ผลของการเปลี่ยนแปลงที่มีต่อการสังเคราะห์ด้วยแสง"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class PhotosynthesisImportanceFluency(QuestionType):
    """Match a change to what it does to the process, or the other way round.

    Every wrong choice is a real consequence of a *different* change in the same
    table, so the item cannot be answered by recognising which option sounds
    like it belongs to photosynthesis at all.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        change, effect = rng.choice(IMPORTANCE_CHANGES)
        others = [other for other in IMPORTANCE_CHANGES if other[0] != change]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"“{change}” จะส่งผลอย่างไร",
                correct=effect,
                wrongs=tuple(other[1] for other in others[:3]),
                hint="ถามก่อนว่าการเปลี่ยนแปลงนั้นทำให้พืชได้รับแสง น้ำ หรือแก๊ส"
                     "คาร์บอนไดออกไซด์เปลี่ยนไปอย่างไร",
            )
        return _labelled(
            stem=f"ผลที่ว่า “{effect}” เกิดจากการเปลี่ยนแปลงใด",
            correct=change,
            wrongs=tuple(other[0] for other in others[:3]),
            hint="ไล่ย้อนจากผลกลับไปหาปัจจัยของการสังเคราะห์ด้วยแสงที่ถูกกระทบ",
        )


@question_type(
    "plant.photosynthesis_importance_application",
    display_name={"th": "ประเมินผลของการสังเคราะห์ด้วยแสงต่อสิ่งมีชีวิตและสิ่งแวดล้อม"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class PhotosynthesisImportanceApplication(QuestionType):
    """Weigh a real decision or a common belief against what the process does.

    ``ม.1/7`` is about importance, which only shows when something is taken away
    or added. Each item states a change — a room full of plants at night, a pond
    at dawn, a park turned into a car park — and asks what actually follows.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return contextual_scenario_question(
            rng, IMPORTANCE_SCENARIOS,
            hint="แยกให้ชัดว่าช่วงเวลานั้นมีแสงหรือไม่ และพืชกำลังสังเคราะห์ด้วยแสง "
                 "หายใจ หรือทำทั้งสองอย่างพร้อมกัน",
            topic=TOPIC,
        )
