"""บทบาทของผู้ผลิต ผู้บริโภค และผู้ย่อยสลาย

ชีวะ · ม.3 · สสวท. พื้นฐาน
Indicators: ว 1.1 ม.3/4

Sets moved here from: science_wave_b.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.classify import Category, ClassifyType
from otk.kit.concept_bank import (
    Concept,
    ConceptBankType,
    contextual_scenario_question,
    widen,
)
from otk.sets._support.science_wave_b import DECOMPOSER_SCENARIOS, LEVEL, SUBJECT, TOPIC

PROVENANCE = Provenance("original")


@question_type(
    "ecology.decomposer_role_foundation",
    display_name={"th": "หน้าที่ของผู้ผลิต ผู้บริโภค และผู้ย่อยสลาย"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class DecomposerRoleFoundation(ConceptBankType):
    """What each of the three roles does, and what the ecosystem loses without it.

    `ecology.ecosystem_components_fluency` sorts organisms into these roles from a
    survey. This set asks what the role *is for*, which is what ม.3/4 needs before
    the relationship between the three can be explained.
    """

    ITEMS = widen([
        Concept(
            "ผู้ผลิตมีบทบาทใดในระบบนิเวศ",
            "เปลี่ยนพลังงานแสงเป็นพลังงานเคมีในสารอาหาร ให้สิ่งมีชีวิตอื่นใช้",
            ("ย่อยสลายซากสิ่งมีชีวิตให้กลายเป็นธาตุอาหารคืนกลับสู่ดินและน้ำ",
             "กินสิ่งมีชีวิตอื่นเพื่อให้ได้พลังงานไปใช้สร้างอาหารใหม่ให้ตนเอง",
             "ควบคุมจำนวนของผู้บริโภคไม่ให้มากเกินไป"),
        ),
        Concept(
            "ผู้ย่อยสลายสารอินทรีย์มีบทบาทใดในระบบนิเวศ",
            "ย่อยสารอินทรีย์ในซากสิ่งมีชีวิตและของเสีย แล้วคืนธาตุอาหารสู่ดินและน้ำ",
            ("สร้างอาหารขึ้นเองจากแสงและแก๊สคาร์บอนไดออกไซด์",
             "กินซากสิ่งมีชีวิตทั้งชิ้นแล้วเก็บพลังงานไว้ในร่างกายโดยไม่คืนสิ่งใด",
             "เปลี่ยนธาตุอาหารในดินให้กลายเป็นพลังงานแสง"),
        ),
        Concept(
            "ถ้าระบบนิเวศหนึ่งไม่มีผู้ย่อยสลายเลย จะเกิดผลอย่างไร",
            "ซากสิ่งมีชีวิตทับถมโดยไม่ย่อยสลาย ธาตุอาหารถูกกักอยู่ในซาก "
            "ผู้ผลิตจึงขาดธาตุอาหาร",
            ("ธาตุอาหารในดินเพิ่มขึ้น เพราะไม่มีสิ่งใดมาใช้ธาตุอาหารนั้น",
             "ผู้บริโภคจะเพิ่มจำนวนขึ้น เพราะมีซากสิ่งมีชีวิตให้กินมากขึ้น",
             "ระบบนิเวศไม่เปลี่ยนแปลง เพราะซากสิ่งมีชีวิตสลายไปเองได้โดยไม่ต้องมีสิ่งมีชีวิตใด"),
        ),
        Concept(
            "ถ้าระบบนิเวศหนึ่งไม่มีผู้ผลิตเลย จะเกิดผลอย่างไร",
            "ไม่มีพลังงานเข้าสู่ระบบนิเวศ ผู้บริโภคทุกลำดับจึงอยู่ไม่ได้",
            ("ผู้บริโภคจะเปลี่ยนไปสร้างอาหารเองด้วยแสงแทนผู้ผลิต",
             "ผู้ย่อยสลายจะทำหน้าที่ผลิตอาหารให้ผู้บริโภคแทน",
             "ระบบนิเวศยังคงอยู่ได้ เพราะธาตุอาหารในดินยังหมุนเวียนอยู่"),
        ),
        Concept(
            "ข้อใดเปรียบเทียบการถ่ายทอดพลังงานกับการหมุนเวียนสารในระบบนิเวศได้ถูกต้อง",
            "พลังงานถ่ายทอดไปทางเดียวและสูญเสียไปเป็นความร้อน "
            "ส่วนสารหมุนเวียนกลับมาใช้ใหม่ได้",
            ("ทั้งพลังงานและสารต่างก็หมุนเวียนกลับมาใช้ใหม่ได้เหมือนกัน",
             "พลังงานหมุนเวียนกลับมาใช้ใหม่ได้ ส่วนสารถ่ายทอดไปทางเดียวแล้วหมดไป",
             "ทั้งพลังงานและสารต่างก็ถ่ายทอดไปทางเดียวแล้วหมดไปจากระบบนิเวศ"),
        ),
        Concept(
            "เห็ดที่ขึ้นบนขอนไม้ผุจัดเป็นสิ่งมีชีวิตกลุ่มใด และได้พลังงานจากที่ใด",
            "ผู้ย่อยสลาย ได้พลังงานจากสารอินทรีย์ในซากพืชที่มันย่อย",
            ("ผู้ผลิต ได้พลังงานจากแสงเช่นเดียวกับพืชสีเขียว",
             "ผู้บริโภคลำดับที่ 1 ได้พลังงานจากการกินต้นไม้ที่ยังมีชีวิต",
             "ผู้ผลิต ได้พลังงานจากธาตุอาหารในเนื้อไม้โดยตรง"),
        ),
        Concept(
            "เหตุใดผู้ย่อยสลายจึงจำเป็นต่อผู้ผลิต ทั้งที่ผู้ผลิตสร้างอาหารเองได้",
            "เพราะผู้ผลิตต้องใช้ธาตุอาหารในดินและน้ำ ซึ่งผู้ย่อยสลายคืนกลับมาให้",
            ("เพราะผู้ย่อยสลายสร้างพลังงานแสงให้ผู้ผลิตใช้สังเคราะห์ด้วยแสง",
             "เพราะผู้ย่อยสลายช่วยกำจัดผู้บริโภคที่จะมากินผู้ผลิตในระบบนิเวศ",
             "เพราะผู้ผลิตต้องกินผู้ย่อยสลายเป็นอาหารเสริมในบางฤดู"),
        ),
    ], (
        ("กินผู้บริโภคลำดับสูงเพื่อควบคุมจำนวน",
         "เก็บพลังงานความร้อนไว้ให้ผู้บริโภคใช้ในฤดูหนาว"),
        ("ให้พลังงานแสงแก่ผู้ผลิตโดยตรง",
         "ล่าผู้บริโภคลำดับที่ 1 เป็นอาหาร"),
        ("ผู้ผลิตจะสร้างธาตุอาหารขึ้นเองได้แทน",
         "ซากจะกลายเป็นผู้ผลิตชนิดใหม่แทน"),
        ("ผู้ย่อยสลายจะเพิ่มจำนวนขึ้นมาก เพราะมีพลังงานแสงเหลือใช้",
         "ผู้บริโภคลำดับที่ 1 จะมีอาหารมากขึ้น เพราะไม่มีผู้ผลิตมาแย่ง"),
        ("พลังงานหมุนเวียนกลับมาใช้ใหม่ได้ผ่านผู้ย่อยสลาย ส่วนสารสูญเสียไปเป็นความร้อน",
         "สารถ่ายทอดไปทางเดียวจากผู้ผลิตถึงผู้บริโภคลำดับสูงสุด"),
        ("ผู้บริโภคลำดับที่ 2 ได้พลังงานจากการกินแมลงในขอนไม้",
         "ผู้ย่อยสลาย ได้พลังงานจากแสงที่ส่องผ่านขอนไม้"),
        ("เพราะผู้ย่อยสลายเปลี่ยนแก๊สออกซิเจนให้เป็นอาหารของผู้ผลิต",
         "เพราะผู้ผลิตสร้างอาหารไม่ได้ถ้าไม่มีผู้ย่อยสลายส่งแสงให้"),
    ))


@question_type(
    "ecology.matter_cycle_fluency",
    display_name={"th": "บทบาทในการหมุนเวียนสารและถ่ายทอดพลังงาน"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class MatterCycleFluency(ClassifyType):
    """Match a described function to the role that performs it.

    Sorted by what the organism *does* to matter and energy, not by what it is.
    That is the difference between this and the ม.3/1 component set, and it is
    what makes the ม.3/4 relationship statable.
    """

    CLASSIFY_STEM = "หน้าที่ต่อไปนี้เป็นของสิ่งมีชีวิตกลุ่มใด: “{member}”"
    PICK_STEM = "ข้อใดเป็นหน้าที่ของ{category}"

    # Four categories, not three. ``ClassifyType`` offers one choice per category
    # in its classify direction, so a three-way table would yield three-choice
    # questions where every other set offers four. Splitting ผู้บริโภค by trophic
    # level is not padding: the two levels have genuinely different functions, and
    # ม.3/3 has just made the distinction available.
    CATEGORIES = [
        Category("ผู้ผลิต",
                 ("เปลี่ยนพลังงานแสงให้เป็นพลังงานเคมีในสารอาหาร",
                  "นำแก๊สคาร์บอนไดออกไซด์และน้ำมาสร้างเป็นสารอาหาร",
                  "ดูดธาตุอาหารจากดินไปสร้างเป็นส่วนประกอบของร่างกาย",
                  "เป็นทางเข้าของพลังงานสู่ระบบนิเวศ")),
        Category("ผู้บริโภคลำดับที่ 1",
                 ("รับพลังงานเคมีจากผู้ผลิตโดยตรง",
                  "กินพืชหรือผู้ผลิตอื่นเป็นอาหารหลัก",
                  "เป็นลำดับขั้นแรกที่รับพลังงานต่อจากผู้ผลิต",
                  "ส่งพลังงานที่ได้จากผู้ผลิตต่อไปให้ผู้ล่า")),
        Category("ผู้บริโภคลำดับที่สูงขึ้น",
                 ("รับพลังงานจากการกินผู้บริโภคด้วยกัน",
                  "ควบคุมจำนวนประชากรของผู้บริโภคลำดับที่ต่ำกว่า",
                  "อยู่ในลำดับขั้นที่ได้รับพลังงานน้อยที่สุดของพีระมิดพลังงาน",
                  "เป็นผู้ล่าที่อยู่ปลายสุดของสายใยอาหาร")),
        Category("ผู้ย่อยสลายสารอินทรีย์",
                 ("ย่อยสารอินทรีย์ในซากสิ่งมีชีวิตให้เป็นสารอนินทรีย์",
                  "คืนธาตุอาหารกลับสู่ดินและน้ำให้ผู้ผลิตนำไปใช้ได้อีก",
                  "ทำให้ซากสิ่งมีชีวิตไม่ทับถมสะสมอยู่ในระบบนิเวศ",
                  "ปิดวงจรการหมุนเวียนสารในระบบนิเวศ")),
    ]


@question_type(
    "ecology.decomposer_application",
    display_name={"th": "วิเคราะห์บทบาทของผู้ย่อยสลายจากสถานการณ์จริง"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class DecomposerApplication(QuestionType):
    """Explain a real result by what the three roles do to matter and energy.

    Every item is a comparison the learner could actually set up — two compost
    bins, two pots, a sealed jar — so the relationship ม.3/4 asks about has to be
    used rather than restated.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return contextual_scenario_question(
            rng, DECOMPOSER_SCENARIOS,
            hint="แยกให้ชัดว่าอะไรคือพลังงานและอะไรคือสาร "
                 "แล้วถามว่าใครเป็นผู้เปลี่ยนสารอินทรีย์กลับเป็นธาตุอาหาร",
            topic=TOPIC,
        )
