"""กาแล็กซีทางช้างเผือก

ดาราศาสตร์ · ม.6 · สสวท. พื้นฐาน
Indicators: ว 3.1 ม.6/3

Sets moved here from: science_wave_c6, science_wave_f82.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import (
    _labelled as _labelled_science_wave_f82,
)
from otk.kit.answer_choices import (
    numeric,
    show,
)
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c1 import SUBJECT
from otk.sets._support.science_wave_c6 import (
    GALAXY_FACTS as GALAXY_FACTS_science_wave_c6,
)
from otk.sets._support.science_wave_c6 import (
    GALAXY_SCENARIOS,
    UPPER_SIX,
)

PROVENANCE = Provenance("original")


GALAXY_TOPIC = "กาแล็กซีทางช้างเผือก"


class Part(NamedTuple):
    """One structural part of the galaxy, and what it holds."""
    name: str
    where: str
    holds: str


GALAXY_PARTS = (
    Part("นิวเคลียสและดุมกลาง",
         "ใจกลางของกาแล็กซี",
         "ดาวฤกษ์เก่าหนาแน่นมาก และหลุมดำมวลยิ่งยวดอยู่ตรงกลาง"),
    Part("จานและแขนกังหัน",
         "แผ่นแบนที่ล้อมรอบใจกลาง",
         "แก๊ส ฝุ่น และดาวฤกษ์อายุน้อยที่กำลังก่อตัวขึ้นใหม่"),
    Part("เฮโล",
         "ทรงกลมที่ห่อหุ้มจานและใจกลางไว้",
         "กระจุกดาวทรงกลมที่มีดาวฤกษ์อายุมาก และสสารมืด"),
)


TOPIC_GALAXY = "กาแล็กซีทางช้างเผือก"


GALAXY_PARTS_science_wave_f82 = (
    ("นิวเคลียส (ใจกลาง) และส่วนป่อง", "มีดาวฤกษ์หนาแน่น ส่วนใหญ่เป็นดาวอายุมาก และมีหลุมดำมวลยวดยิ่งอยู่ที่ใจกลาง"),
    ("จาน", "แบนบาง มีแขนกังหันที่มีแก๊ส ฝุ่น และดาวฤกษ์เกิดใหม่จำนวนมาก"),
    ("ฮาโล", "ล้อมรอบกาแล็กซีเป็นทรงกลม มีกระจุกดาวทรงกลมที่มีดาวอายุมาก"),
)


GALAXY_FACTS = (
    ("กาแล็กซีทางช้างเผือกเป็นกาแล็กซีรูปร่างแบบใด", "กาแล็กซีกังหันมีคาน",
     ("กาแล็กซีรี", "กาแล็กซีไร้รูปแบบ", "กาแล็กซีทรงกลมสมบูรณ์", "กาแล็กซีวงแหวน")),
    ("ระบบสุริยะอยู่ตำแหน่งใดในกาแล็กซีทางช้างเผือก", "อยู่ในจาน บนแขนย่อยนายพราน ห่างจากใจกลางประมาณ 26,000 ปีแสง",
     ("อยู่ที่ใจกลางกาแล็กซี", "อยู่ในฮาโลเหนือจาน ห่างจากใจกลางประมาณ 100,000 ปีแสง", "อยู่ที่ขอบนอกสุดของจาน ห่างจากใจกลางประมาณ 50,000 ปีแสง", "อยู่ที่ใจกลางกาแล็กซี ใกล้หลุมดำมวลยวดยิ่งที่ใจกลาง")),
    ("เหตุใดคนบนโลกจึงเห็นทางช้างเผือกเป็นแถบฝ้าขาวพาดผ่านท้องฟ้า", "เรามองจากภายในจานของกาแล็กซี จึงเห็นดาวจำนวนมากซ้อนกันตามแนวจาน",
     ("เป็นเมฆในบรรยากาศชั้นสูง", "เป็นแสงสะท้อนจากดวงจันทร์", "เรามองกาแล็กซีจากด้านบนของจาน จึงเห็นแขนกังหันเรียงเป็นแนวยาว", "เป็นแสงสะท้อนจากฝุ่นในระบบสุริยะที่เรียงตัวเป็นแถบยาวข้ามฟ้า")),
    ("แถบมืดที่เห็นพาดกลางทางช้างเผือกเกิดจากอะไร", "ฝุ่นและแก๊สในจานกาแล็กซีบังแสงดาวที่อยู่ด้านหลัง",
     ("บริเวณว่างที่ไม่มีดาวฤกษ์อยู่เลยในแนวนั้น", "เงาของโลกที่ทอดไปบนแถบทางช้างเผือก", "หลุมดำขนาดใหญ่หลายแห่ง", "หลุมดำขนาดใหญ่หลายแห่งที่ดูดกลืนแสงดาวบริเวณนั้น")),
    ("ในประเทศไทย ช่วงเวลาใดเห็นใจกลางทางช้างเผือกได้ชัดเจนที่สุด", "ช่วงกลางปีราวเดือนมิถุนายนถึงสิงหาคม บริเวณกลุ่มดาวคนยิงธนู ในคืนเดือนมืด",
     ("ทุกคืนตลอดปีในทิศเหนือ", "ทุกคืนตลอดปีในทิศเหนือ เพราะทางช้างเผือกอยู่รอบขั้วฟ้าเหนือ", "เฉพาะคืนวันเพ็ญ เพราะแสงจันทร์ช่วยให้เห็นแถบทางช้างเผือกชัดขึ้น", "ช่วงเดือนธันวาคมถึงมกราคม บริเวณกลุ่มดาวนายพรานตอนหัวค่ำในคืนเดือนหงาย")),
    ("กาแล็กซีทางช้างเผือกมีขนาดเส้นผ่านศูนย์กลางประมาณเท่าใด", "ประมาณ 100,000 ปีแสง",
     ("ประมาณ 100 ปีแสง", "ประมาณ 1 ปีแสง", "ประมาณ 100 ล้านปีแสง", "ประมาณ 13,800 ล้านปีแสง")),
    ("ดวงอาทิตย์ใช้เวลาโคจรรอบใจกลางทางช้างเผือกรอบละประมาณเท่าใด", "ประมาณ 230 ล้านปี",
     ("ประมาณ 1 ปี", "ประมาณ 365 ปี", "ประมาณ 13,800 ล้านปี", "ประมาณ 1,000 ปี")),
    ("ทางช้างเผือกอยู่ในกลุ่มกาแล็กซีใด และกาแล็กซีขนาดใหญ่ที่อยู่ใกล้ที่สุดคือกาแล็กซีใด", "กลุ่มท้องถิ่น (Local Group) ใกล้กับกาแล็กซีแอนดรอเมดา",
     ("กลุ่มกาแล็กซีหญิงสาว ใกล้กับกาแล็กซีหมวกปีก", "กลุ่มท้องถิ่น (Local Group) ใกล้กับกาแล็กซีหมวกปีก", "กระจุกกาแล็กซีหญิงสาว ใกล้กับกาแล็กซีแอนดรอเมดา", "กลุ่มดาวนายพราน ใกล้กับเนบิวลานายพรานในกาแล็กซี")),
)


GALAXY_HINT = ("ทางช้างเผือกเป็นกาแล็กซีกังหันมีคาน กว้างประมาณ 100,000 ปีแสง มีนิวเคลียสและส่วนป่อง จาน และฮาโล "
               "ระบบสุริยะอยู่ในจานห่างจากใจกลางประมาณ 26,000 ปีแสง เราจึงเห็นทางช้างเผือกเป็นแถบพาดท้องฟ้า")


@question_type(
    "astro.milky_way_foundation",
    display_name={"th": "โครงสร้างและองค์ประกอบของทางช้างเผือก"},
    level=UPPER_SIX, subject=SUBJECT, topic=GALAXY_TOPIC,
)
class MilkyWayFoundation(QuestionType):
    """Describe the galaxy's parts — the indicator's first free verb."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            return _retopic(scenario_question(
                rng, GALAXY_FACTS_science_wave_c6,
                hint="นึกภาพกาแล็กซีกังหันเมื่อมองจากด้านบนและจากด้านข้าง",
            ), GALAXY_TOPIC)
        item = rng.choice(GALAXY_PARTS)
        others = [other for other in GALAXY_PARTS if other.name != item.name]
        if rng.random() < 0.5:
            return _labelled(
                stem=f"“{item.name}” ของกาแล็กซีทางช้างเผือกมีอะไรอยู่",
                correct=item.holds,
                wrongs=tuple(other.holds for other in others)
                       + ("ดาวเคราะห์ของระบบสุริยะทั้งแปดดวงเท่านั้น",),
                hint="นึกว่าส่วนนั้นเป็นที่อยู่ของดาวฤกษ์อายุมากหรืออายุน้อย",
                topic=GALAXY_TOPIC,
            )
        return _labelled(
            stem=f"ส่วนใดของกาแล็กซีทางช้างเผือกอยู่ที่{item.where}",
            correct=item.name,
            wrongs=tuple(other.name for other in others)
                   + ("กระจุกดาวเปิดที่อยู่นอกกาแล็กซี",),
            hint="นึกภาพจานแบนที่มีดุมนูนอยู่ตรงกลางและทรงกลมห่อหุ้มอยู่รอบนอก",
            topic=GALAXY_TOPIC,
        )


@question_type(
    "astro.galaxy_structure_foundation",
    display_name={"th": "โครงสร้างและองค์ประกอบของกาแล็กซีทางช้างเผือก"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_GALAXY,
)
class GalaxyStructureFoundation(QuestionType):
    """Nucleus and bulge, disc, halo."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            found = {"นิวเคลียส (ใจกลาง) และส่วนป่อง": ("หลุมดำมวลยวดยิ่ง", "ดาวฤกษ์อายุมากอยู่กันหนาแน่นที่สุด"),
                     "จาน": ("เนบิวลาและดาวฤกษ์เกิดใหม่", "ระบบสุริยะ", "กระจุกดาวเปิด", "แก๊สและฝุ่นหนาแน่นเป็นแนวแขนกังหัน"),
                     "ฮาโล": ("กระจุกดาวทรงกลม", "สสารมืดส่วนใหญ่ของกาแล็กซี")}
            part = rng.choice(tuple(found))
            item = rng.choice(found[part])
            if rng.random() < 0.5:
                return _labelled_science_wave_f82(stem=f"\"{item}\" พบมากในส่วนใดของกาแล็กซีทางช้างเผือก", correct=part,
                                 wrongs=(*(p for p in found if p != part), "นอกกาแล็กซีทั้งหมด"), topic=TOPIC_GALAXY, hint=GALAXY_HINT)
            pool = [i for p, items in found.items() if p != part for i in items]
            return _labelled_science_wave_f82(stem=f"ข้อใดพบมากในส่วน{part}ของกาแล็กซีทางช้างเผือก", correct=item, wrongs=tuple(pool),
                             topic=TOPIC_GALAXY, hint=GALAXY_HINT)
        part, what = rng.choice(GALAXY_PARTS_science_wave_f82)
        extra = ("เป็นดาวเคราะห์ที่โคจรรอบดวงอาทิตย์", "เป็นกลุ่มแก๊สที่ไม่มีดาวฤกษ์เลย")
        if rng.random() < 0.5:
            wrongs = [w for p, w in GALAXY_PARTS_science_wave_f82 if p != part] + [rng.choice(extra)]
            return _labelled_science_wave_f82(stem=f"ส่วน{part}ของกาแล็กซีทางช้างเผือกมีลักษณะอย่างไร", correct=what, wrongs=tuple(wrongs),
                             topic=TOPIC_GALAXY, hint=GALAXY_HINT)
        wrongs = [p for p, _ in GALAXY_PARTS_science_wave_f82 if p != part] + ["ดาวเคราะห์แคระ"]
        return _labelled_science_wave_f82(stem=f"ส่วนใดของกาแล็กซีทางช้างเผือก{what}", correct=part, wrongs=tuple(wrongs), topic=TOPIC_GALAXY, hint=GALAXY_HINT)


@question_type(
    "astro.milky_way_fluency",
    display_name={"th": "ตำแหน่งของระบบสุริยะกับภาพทางช้างเผือกที่เห็น"},
    level=UPPER_SIX, subject=SUBJECT, topic=GALAXY_TOPIC,
)
class MilkyWayFluency(QuestionType):
    """Link where we sit to what we see — the indicator's second and third verbs.

    ``ระบุตำแหน่งของระบบสุริยะ`` and ``อธิบายเชื่อมโยงกับการสังเกตเห็นทางช้างเผือก``
    are two free verbs, and the second exists only to be joined to the first, so
    one set carries both.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        draw = rng.random()
        if draw < 0.35:
            return _labelled(
                stem="เหตุใดคนบนโลกจึงมองเห็นทางช้างเผือกเป็นแถบฝ้าสว่างพาดผ่านท้องฟ้า",
                correct="เพราะระบบสุริยะอยู่ในจานของกาแล็กซี เมื่อมองตามระนาบของจานจึงเห็นดาวฤกษ์มากมายซ้อนกันเป็นแถบ",
                wrongs=tuple((
                    "เพราะระบบสุริยะอยู่นอกกาแล็กซี จึงเห็นกาแล็กซีทั้งแผ่นจากด้านนอกเป็นแถบยาว",
                    "เพราะมีเมฆบาง ๆ ในชั้นบรรยากาศของโลกเรียงตัวเป็นแถบ",
                    "เพราะดาวฤกษ์ที่สว่างที่สุดในกาแล็กซีเรียงตัวกันเป็นเส้นตรงพอดีในทิศที่เรามองเห็น",
                    "เพราะระบบสุริยะอยู่ที่ใจกลางกาแล็กซี จึงเห็นดาวล้อมรอบเป็นวง",
                    "เพราะแสงจากดวงอาทิตย์สะท้อนฝุ่นในระบบสุริยะเป็นแถบ",
                )),
                hint="ถามว่าเรามองกาแล็กซีจากข้างในหรือจากข้างนอก",
                topic=GALAXY_TOPIC,
            )
        if draw < 0.6:
            return _labelled(
                stem="ถ้าระบบสุริยะอยู่ในเฮโลแทนที่จะอยู่ในจานของกาแล็กซี "
                     "คนบนโลกจะเห็นทางช้างเผือกต่างไปอย่างไร",
                correct="จะเห็นจานของกาแล็กซีเป็นแผ่นอยู่ห่างออกไป แทนที่จะเป็นแถบพาดรอบท้องฟ้า",
                wrongs=tuple((
                    "จะเห็นเหมือนเดิมทุกประการ เพราะตำแหน่งไม่มีผลต่อภาพที่เห็น",
                    "จะมองไม่เห็นดาวฤกษ์ดวงใดเลย เพราะเฮโลไม่มีดาวอยู่",
                    "จะเห็นแถบฝ้าสว่างกว้างขึ้นจนเต็มท้องฟ้าทุกทิศ",
                    "จะเห็นแถบทางช้างเผือกแคบลงเป็นเส้นบาง ๆ แต่ยังพาดรอบท้องฟ้าเหมือนเดิม",
                    "จะเห็นใจกลางกาแล็กซีอยู่เหนือศีรษะตลอดเวลาโดยไม่เห็นจาน",
                )),
                hint="นึกว่าอยู่ในแผ่นจานกับอยู่นอกแผ่นจาน จะมองเห็นต่างกันอย่างไร",
                topic=GALAXY_TOPIC,
            )
        if draw < 0.8:
            return _labelled(
                stem="เมื่อมองไปทางกลุ่มดาวคนยิงธนู แถบทางช้างเผือกดูสว่างและหนากว่าทิศอื่น "
                     "ข้อใดอธิบายได้เหมาะสมที่สุด",
                correct="ทิศนั้นคือทิศที่มองไปยังใจกลางกาแล็กซี ซึ่งมีดาวฤกษ์หนาแน่นที่สุด",
                wrongs=tuple((
                    "ทิศนั้นคือทิศที่มองออกไปนอกกาแล็กซี ซึ่งไม่มีอะไรมาบังสายตา",
                    "ทิศนั้นอยู่ใกล้โลกมากที่สุด ดาวจึงดูสว่างกว่า",
                    "ทิศนั้นเป็นทิศที่ระบบสุริยะกำลังเคลื่อนที่ไป",
                    "ทิศนั้นคือทิศของเฮโลที่มีกระจุกดาวทรงกลมสว่างที่สุด",
                    "ทิศนั้นมีฝุ่นน้อยที่สุดในกาแล็กซี จึงเห็นดาวได้ทุกดวง",
                )),
                hint="ระบบสุริยะอยู่ห่างจากใจกลาง ดังนั้นใจกลางจึงอยู่ทางทิศใดทิศหนึ่ง",
                topic=GALAXY_TOPIC,
            )
        return _labelled(
            stem="ข้อใดกล่าวถึงตำแหน่งของระบบสุริยะในกาแล็กซีทางช้างเผือกได้ถูกต้อง",
            correct="อยู่ในจาน บนแขนกังหันแขนหนึ่ง ห่างจากใจกลางราว 26,000 ปีแสง และโคจรรอบใจกลาง",
            wrongs=tuple((
                "อยู่ที่ใจกลางของกาแล็กซีพอดี และกาแล็กซีทั้งหมดโคจรรอบระบบสุริยะเป็นวงกลม",
                "อยู่ในเฮโลชั้นนอก ห่างจากจานของกาแล็กซีมาก",
                "อยู่ที่ขอบนอกสุดของจาน เลยแขนกังหันแขนสุดท้ายออกไป",
                "อยู่ในดุมกลาง ห่างจากหลุมดำใจกลางไม่กี่ปีแสง",
                "อยู่นอกกาแล็กซีทางช้างเผือก ในกาแล็กซีเพื่อนบ้าน",
            )),
            hint="นึกว่าเราอยู่ในจาน แต่ไม่ได้อยู่ตรงกลาง",
            topic=GALAXY_TOPIC,
        )


@question_type(
    "astro.galaxy_structure_fluency",
    display_name={"th": "ตำแหน่งระบบสุริยะและการสังเกตทางช้างเผือกจากโลก"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_GALAXY,
)
class GalaxyStructureFluency(QuestionType):
    """Shape, where we are, why a band, dark lanes, when to look."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(GALAXY_FACTS)
        return _labelled_science_wave_f82(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_GALAXY, hint=GALAXY_HINT)


@question_type(
    "astro.milky_way_application",
    display_name={"th": "วิเคราะห์การสังเกตทางช้างเผือก"},
    level=UPPER_SIX, subject=SUBJECT, topic=GALAXY_TOPIC,
)
class MilkyWayApplication(QuestionType):
    """Reason about light pollution, dust, and a model that puts us in the middle."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, GALAXY_SCENARIOS,
            hint="นึกว่าเราอยู่ในจานของกาแล็กซี และมีฝุ่นในจานบังสายตาอยู่",
        ), GALAXY_TOPIC)


@question_type(
    "astro.galaxy_structure_application",
    display_name={"th": "คำนวณจำนวนรอบการโคจรและย่อส่วนแบบจำลองทางช้างเผือก"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_GALAXY,
)
class GalaxyStructureApplication(QuestionType):
    """Laps of the galaxy since the Sun formed; a scale model."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            while True:
                period = rng.choice((200, 220, 225, 230, 240, 250))
                age = rng.choice((4600, 4500, 4000, 3000, 2300, 1000, 500))
                laps = Fraction(age, period)
                if (laps * 100).denominator == 1:
                    break
            if rng.random() < 0.5:
                return numeric(stem=f"ดวงอาทิตย์ใช้เวลาโคจรรอบใจกลางทางช้างเผือกรอบละประมาณ {period} ล้านปี ในเวลา {show(age)} ล้านปี จะโคจรได้กี่รอบ",
                               answer=laps, wrongs=[Fraction(period, age) * 100 if (Fraction(period, age) * 10000).denominator == 1 else laps * 2, laps + 5, age - period],
                               unit="รอบ", topic=TOPIC_GALAXY, hint="จำนวนรอบ = เวลาทั้งหมด ÷ เวลาต่อรอบ")
            return numeric(stem=f"ดวงอาทิตย์โคจรรอบใจกลางทางช้างเผือกได้ {show(laps)} รอบในเวลา {show(age)} ล้านปี ใช้เวลารอบละกี่ล้านปี",
                           answer=period, wrongs=[period * 2, age, period + 50], unit="ล้านปี", topic=TOPIC_GALAXY, hint="เวลาต่อรอบ = เวลาทั้งหมด ÷ จำนวนรอบ")
        size = rng.choice((1, 2, 4, 5, 10, 20, 50))
        what, ly = rng.choice((("ระบบสุริยะ", 26000), ("ความหนาของจาน", 1000), ("รัศมีของกาแล็กซี", 50000), ("ระบบสุริยะ", 27000)))
        return numeric(stem=f"ถ้าย่อทางช้างเผือกซึ่งกว้าง 100,000 ปีแสงให้เหลือแบบจำลองกว้าง {size} m ระยะ{'จากใจกลางถึง' if what == 'ระบบสุริยะ' else ''}{what} "
                            f"{show(ly)} ปีแสงจะยาวกี่เมตรในแบบจำลอง",
                       answer=Fraction(size * ly, 100000), wrongs=[Fraction(size * ly, 10000), Fraction(ly, 1000), size],
                       unit="m", topic=TOPIC_GALAXY, hint="ความยาวในแบบจำลอง = ความยาวจริง × ขนาดแบบจำลอง ÷ 100,000 ปีแสง")
