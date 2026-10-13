"""ระบบสุริยะและแรงโน้มถ่วง

ดาราศาสตร์ · ม.3 · สสวท. พื้นฐาน
Indicators: ว 3.1 ม.3/1, ว 3.1 ม.3/2, ว 3.1 ม.3/3

Sets moved here from: astronomy, science_wave_c5.
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
from otk.kit.concept_bank import Concept, ConceptBankType, widen
from otk.sets._support.astronomy import SUBJECT, TOPIC
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b25 import MIDDLE_THREE
from otk.sets._support.science_wave_c5 import EQUATION_CASES, GRAVITY_FACTS, ORBIT_SCENARIOS

PROVENANCE = Provenance("original")


class Planet(NamedTuple):
    order: int          # position from the sun, 1 = closest
    name: str           # Thai name with the English one alongside


# The eight ดาวเคราะห์ in order from the sun (Pluto is a ดาวเคราะห์แคระ, excluded).
PLANETS = [Planet(*t) for t in [
    (1, "ดาวพุธ (Mercury)"), (2, "ดาวศุกร์ (Venus)"), (3, "โลก (Earth)"),
    (4, "ดาวอังคาร (Mars)"), (5, "ดาวพฤหัสบดี (Jupiter)"), (6, "ดาวเสาร์ (Saturn)"),
    (7, "ดาวยูเรนัส (Uranus)"), (8, "ดาวเนปจูน (Neptune)"),
]]


ORBIT_TOPIC = "ระบบสุริยะและแรงโน้มถ่วง"


EQUATION = "จากสมการแรงโน้มถ่วง F = Gm₁m₂/r² "


@question_type("astro.phenomena",
               display_name={"th": "ปรากฏการณ์และแรงโน้มถ่วงในระบบสุริยะ"},
               level={"th": "ม.3"}, subject=SUBJECT, topic=TOPIC)
class AstronomicalPhenomena(ClassifyType):
    """โยงปรากฏการณ์เข้ากับต้นเหตุ การโคจร/การหมุนรอบตัวเอง/การโคจรของดวงจันทร์/แรงโน้มถ่วง."""

    CLASSIFY_STEM = "ปรากฏการณ์ต่อไปนี้เกิดจากสาเหตุใด: “{member}”"
    PICK_STEM = "ข้อใดคือปรากฏการณ์ที่เกิดจาก{category}"

    CATEGORIES = [
        Category("การโคจรของโลกรอบดวงอาทิตย์ โดยแกนเอียงมีผลต่อฤดูกาล",
                 ("การเกิดฤดูกาลต่างๆ",
                  "ช่วงกลางวันและกลางคืนยาวไม่เท่ากันในรอบปี",
                  "การเห็นกลุ่มดาวจักรราศีเปลี่ยนตำแหน่งไปในแต่ละเดือน")),
        Category("การหมุนรอบตัวเองของโลก",
                 ("การเกิดปรากฏการณ์กลางวันและกลางคืน",
                  "การเห็นดวงอาทิตย์และดวงดาวขึ้นและตกในแต่ละวัน",
                  "การเห็นตำแหน่งดวงอาทิตย์เปลี่ยนไปบนท้องฟ้าในระหว่างวัน")),
        Category("การโคจรของดวงจันทร์รอบโลก",
                 ("ปรากฏการณ์ข้างขึ้น–ข้างแรม",
                  "การเห็นส่วนสว่างของดวงจันทร์เปลี่ยนรูปร่างไปในแต่ละคืน",
                  "เวลาขึ้นและตกของดวงจันทร์เปลี่ยนไปจากวันหนึ่งสู่อีกวันหนึ่ง")),
        Category("อิทธิพลของแรงโน้มถ่วง (Gravity)",
                 ("การรักษาวงโคจรของดาวเคราะห์ไม่ให้หลุดออกจากระบบสุริยะ",
                  "แรงดึงดูดที่ทำให้มวลน้ำบนโลกโป่งพองจนเกิดน้ำขึ้น",
                  "แรงที่ดึงดูดให้ดวงจันทร์โคจรรอบโลก")),
    ]


@question_type("astro.planet_order",
               display_name={"th": "ลำดับของดาวเคราะห์ในระบบสุริยะ"},
               level={"th": "ม.3"}, subject=SUBJECT, topic=TOPIC)
class PlanetOrder(QuestionType):
    """ลำดับของดาวเคราะห์จากดวงอาทิตย์ ถามทั้งสองทาง: ลำดับ → ชื่อ และ ชื่อ → ลำดับ.

    ``ask`` pins one direction (``1`` = บอกลำดับ ถามชื่อ, ``2`` = บอกชื่อ ถามลำดับ);
    ``0`` draws one per item. Distractors are always *other* real planets / other
    real positions, drawn from the same list.
    """

    ASKS = ("name", "order")

    def build(self, rng: Random, ask: int = 0) -> GeneratedQuestion:
        which = (self.ASKS[ask - 1] if 1 <= ask <= len(self.ASKS)
                 else rng.choice(self.ASKS))
        p = rng.choice(PLANETS)
        if which == "name":                     # given the order, name the planet
            return GeneratedQuestion(
                stem=[text(f"ดาวเคราะห์ลำดับที่ {p.order} เมื่อนับจากดวงอาทิตย์ออกไป "
                           f"คือดาวใด")],
                correct=[text(p.name)],
                distractors=label_pool([q.name for q in PLANETS]),
                topic=self.topic,
            )
        return GeneratedQuestion(                # given the planet, tell its order
            stem=[text(f"“{p.name}” เป็นดาวเคราะห์ลำดับที่เท่าใดเมื่อนับจาก"
                       f"ดวงอาทิตย์ออกไป")],
            correct=[text(f"ลำดับที่ {p.order}")],
            distractors=label_pool([f"ลำดับที่ {q.order}" for q in PLANETS]),
            topic=self.topic,
        )


@question_type(
    "astro.gravity_orbit_foundation",
    display_name={"th": "แรงโน้มถ่วงกับการโคจร"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=ORBIT_TOPIC,
)
class GravityOrbitFoundation(QuestionType):
    """Know what the symbols mean and which way the force points."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, GRAVITY_FACTS,
            hint="อ่านสมการทีละตัวแปร แล้วนึกว่าแรงดึงเข้าหากันเสมอ",
        ), ORBIT_TOPIC)


@question_type("astro.gravity",
               display_name={"th": "แรงโน้มถ่วงระหว่างดวงอาทิตย์กับดาวบริวาร"},
               level={"th": "ม.3"}, subject=SUBJECT, topic=TOPIC)
class Gravity(ConceptBankType):
    """แรงโน้มถ่วงของดวงอาทิตย์ที่ยึดดาวเคราะห์ไว้ในวงโคจร และปัจจัยที่กำหนดขนาดของแรง."""

    ITEMS = widen([
        Concept(
            "แรงใดที่ทำให้ดาวเคราะห์โคจรรอบดวงอาทิตย์ได้โดยไม่หลุดออกไปในอวกาศ",
            "แรงโน้มถ่วงของดวงอาทิตย์ที่ดึงดูดดาวเคราะห์เข้าหาศูนย์กลาง",
            ("แรงแม่เหล็กของดวงอาทิตย์ที่ผลักดาวเคราะห์ออกไปจากศูนย์กลาง",
             "แรงจากลมสุริยะที่พัดดาวเคราะห์ให้เคลื่อนที่ไปตามวงโคจร",
             "แรงเสียดทานระหว่างดาวเคราะห์กับอวกาศ")),
        Concept(
            "ขนาดของแรงโน้มถ่วงระหว่างดวงอาทิตย์กับดาวเคราะห์ขึ้นอยู่กับสิ่งใด",
            "ผลคูณมวลของทั้งสองวัตถุและกำลังสองของระยะห่าง ตาม F = Gm₁m₂/r²",
            ("ผลบวกมวลของทั้งสองวัตถุและระยะห่างระหว่างกัน ตาม F = G(m₁+m₂)r",
             "ความเร็วในการหมุนรอบตัวเองของดาวเคราะห์",
             "จำนวนดวงจันทร์บริวารของดาวเคราะห์")),
        Concept(
            "ถ้ามวลคงเดิมแต่ระยะห่างระหว่างดาวเคราะห์กับดวงอาทิตย์เพิ่มเป็น 2 เท่า แรงโน้มถ่วงจะเป็นกี่เท่าของเดิม",
            "เหลือ 1/4 ของแรงเดิม",
            ("เหลือ 1/2 ของแรงเดิม", "เพิ่มเป็น 2 เท่าของแรงเดิม", "เพิ่มเป็น 4 เท่าของแรงเดิม")),
        Concept(
            "ถ้าดาวเคราะห์สองดวงมีมวลเท่ากัน ดวงที่อยู่ใกล้ดวงอาทิตย์มากกว่าจะได้รับแรงโน้มถ่วงอย่างไร",
            "ได้รับแรงโน้มถ่วงมากกว่าดวงที่อยู่ไกล",
            ("ได้รับแรงโน้มถ่วงน้อยกว่าดวงที่อยู่ไกล",
             "ได้รับแรงโน้มถ่วงเท่ากันทั้งสองดวง",
             "ไม่ได้รับแรงโน้มถ่วงจากดวงอาทิตย์เลย")),
        Concept(
            "แรงโน้มถ่วงของดวงอาทิตย์ทำหน้าที่เป็นแรงชนิดใดที่ทำให้ทิศความเร็วของดาวเคราะห์เปลี่ยนไปตามวงโคจร",
            "แรงสู่ศูนย์กลาง (Centripetal force)",
            ("แรงหนีศูนย์กลางที่ผลักดาวออกไป",
             "แรงพยุงที่ทำให้ดาวลอยนิ่ง",
             "แรงผลักจากการแผ่รังสีความร้อน")),
    ], (
        ("แรงลอยตัวจากชั้นบรรยากาศของดวงอาทิตย์",
         "แรงดึงของดาวเคราะห์ดวงอื่นที่อยู่ข้างเคียงเท่านั้น"),
        ("มวลของวัตถุที่เล็กกว่าเพียงอย่างเดียว ไม่ขึ้นกับระยะห่างระหว่างกัน",
         "ความสว่างที่ปรากฏของดาวเคราะห์เมื่อมองจากโลก"),
        ("เหลือ 1/8 ของแรงเดิม",
         "เท่าเดิมเพราะมวลไม่เปลี่ยน"),
        ("ได้รับแรงโน้มถ่วงมากกว่าเพียงในฤดูร้อนเท่านั้น",
         "ขึ้นอยู่กับสีของดาวเคราะห์แต่ละดวง"),
        ("แรงเสียดทานของอวกาศที่ช่วยเลี้ยวดาว",
         "แรงแม่เหล็กโลกที่ดึงดาวเคราะห์ไว้"),
    ))


@question_type(
    "astro.gravity_orbit_fluency",
    display_name={"th": "ใช้สมการแรงโน้มถ่วงอธิบายการโคจร"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=ORBIT_TOPIC,
)
class GravityOrbitFluency(QuestionType):
    """Work the orbit from the equation the indicator names — its ``exact`` set."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.75:
            change, effect, wrongs = rng.choice(EQUATION_CASES)
            return _labelled(
                stem=EQUATION + f"ถ้า{change} แรงโน้มถ่วงระหว่างทั้งสองจะเปลี่ยนไปอย่างไร",
                correct=effect, wrongs=tuple(wrongs),
                hint="มวลอยู่ในตัวเศษ ส่วนระยะห่างอยู่ในตัวส่วนและถูกยกกำลังสอง",
                topic=ORBIT_TOPIC,
            )
        return _labelled(
            stem=EQUATION + "ข้อใดอธิบายได้ถูกต้องว่าเหตุใดดาวเคราะห์วงในจึงโคจร"
                            "ครบรอบเร็วกว่าดาวเคราะห์วงนอก",
            correct="ดาวเคราะห์วงในมี r น้อยกว่า จึงถูกแรงโน้มถ่วงดึงแรงกว่า "
                    "และต้องเคลื่อนที่เร็วกว่าจึงจะคงอยู่ในวงโคจรได้",
            wrongs=tuple((
                "ดาวเคราะห์วงในมี r มากกว่า จึงถูกแรงโน้มถ่วงดึงแรงกว่า",
                "ดาวเคราะห์วงในมีมวลมากกว่าดาวเคราะห์วงนอกทุกดวง",
                "ดาวเคราะห์วงในอยู่ใกล้ดวงอาทิตย์จึงร้อนกว่าและขยายตัวจนเคลื่อนที่เร็วขึ้น",
                "ดาวเคราะห์วงในมี r น้อยกว่า จึงถูกแรงโน้มถ่วงดึงน้อยกว่าและเคลื่อนที่ช้ากว่า",
                "ดาวเคราะห์ทุกดวงเคลื่อนที่เร็วเท่ากัน ดาวเคราะห์วงในเพียงมีวงโคจรสั้นกว่า",
            )),
            hint="ดูว่า r ที่น้อยลงทำให้ F ในสมการเปลี่ยนไปอย่างไร",
            topic=ORBIT_TOPIC,
        )


@question_type(
    "astro.gravity_orbit_application",
    display_name={"th": "วิเคราะห์วงโคจรด้วยแรงโน้มถ่วง"},
    level=MIDDLE_THREE, subject=SUBJECT, topic=ORBIT_TOPIC,
)
class GravityOrbitApplication(QuestionType):
    """Take the law to a spacecraft, a comet, and a calculation that looks wrong."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, ORBIT_SCENARIOS,
            hint="ถามว่ามวลและระยะห่างเปลี่ยนไปอย่างไร แล้วดูผลต่อ F",
        ), ORBIT_TOPIC)


# More items, each asking something the others do not.
Gravity.ITEMS = [*Gravity.ITEMS,
    Concept("ถ้าระยะห่างระหว่างวัตถุทั้งสองลดลงเหลือครึ่งหนึ่ง โดยมวลเท่าเดิม แรงโน้มถ่วงจะเป็นกี่เท่าของเดิม",
            "4 เท่าของแรงเดิม",
            ("2 เท่าของแรงเดิม", "เหลือครึ่งหนึ่งของแรงเดิม", "เหลือ 1/4 ของแรงเดิม", "เท่าเดิม", "8 เท่าของแรงเดิม")),
    Concept("น้ำหนักของนักบินอวกาศบนดวงจันทร์น้อยกว่าบนโลก แต่มวลเป็นอย่างไร",
            "มวลเท่าเดิม เพราะมวลคือปริมาณเนื้อสารซึ่งไม่เปลี่ยนตามสถานที่",
            ("มวลลดลงเท่ากับน้ำหนัก", "มวลเพิ่มขึ้นหกเท่า", "มวลเป็นศูนย์บนดวงจันทร์",
             "มวลเปลี่ยนตามความสูงของภูเขาบนดวงจันทร์", "มวลและน้ำหนักเป็นค่าเดียวกันเสมอ")),
    Concept("ดาวพฤหัสบดีมีดวงจันทร์บริวารจำนวนมาก ข้อใดเกี่ยวข้องมากที่สุด",
            "ดาวพฤหัสบดีมีมวลมาก แรงโน้มถ่วงจึงดึงวัตถุจำนวนมากให้โคจรรอบได้",
            ("ดาวพฤหัสบดีอยู่ใกล้ดวงอาทิตย์ที่สุด", "ดาวพฤหัสบดีไม่มีแรงโน้มถ่วง",
             "ดาวพฤหัสบดีหมุนรอบตัวเองช้าที่สุด", "ดาวพฤหัสบดีเป็นดาวเคราะห์หิน", "ดาวพฤหัสบดีสร้างดวงจันทร์ขึ้นเองทุกปี")),
    Concept("ดาวหางที่โคจรเข้าใกล้ดวงอาทิตย์จะเคลื่อนที่เร็วขึ้น เพราะเหตุใด",
            "แรงโน้มถ่วงของดวงอาทิตย์ที่ระยะใกล้มีค่ามาก ดึงให้ดาวหางเร่งความเร็วขึ้น",
            ("ดวงอาทิตย์ผลักดาวหางออกไปเมื่อเข้าใกล้", "ดาวหางมีเครื่องยนต์ที่ทำงานเมื่อร้อน",
             "ดาวหางเบาลงจนแรงโน้มถ่วงไม่มีผล", "ความเร็วของดาวหางคงที่ตลอดวงโคจร", "ลมสุริยะดึงดาวหางให้ช้าลง")),
]
