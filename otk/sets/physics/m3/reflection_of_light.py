"""การสะท้อนของแสง

ฟิสิกส์ · ม.3 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.3/13, ว 2.3 ม.3/15, ว 2.3 ม.3/17

Sets moved here from: physics, science_wave_a2.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.classify import Category, ClassifyType
from otk.kit.numeric_scenario import Calc, PhysCalc
from otk.sets._support.physics import SUBJECT, TOPIC
from otk.sets._support.science_wave_a2 import PHYSICS, WAVES, _question

PROVENANCE = Provenance("original")


@question_type("phys.light",
               display_name={"th": "การสะท้อนและการหักเหของแสง (จำแนกปรากฏการณ์)"},
               level={"th": "ม.3"}, subject=SUBJECT, topic=TOPIC)
class LightProperties(ClassifyType):
    """แยกปรากฏการณ์ที่เกิดจากการสะท้อน (มุมตกกระทบ = มุมสะท้อน) จากการหักเห (แสงเปลี่ยนทิศเมื่อผ่านตัวกลาง)."""

    CLASSIFY_STEM = "เหตุการณ์ต่อไปนี้เกิดจากสมบัติใดของแสง: “{member}”"
    PICK_STEM = "ข้อใดเป็นเหตุการณ์ที่เกิดจากสมบัติ{category}"

    CATEGORIES = [
        Category("การสะท้อนของแสง (Reflection)",
                 ("การทำงานของกระจกเงาราบ",
                  "การทำงานของกระจกนูนและกระจกเว้า",
                  "กฎที่ว่ามุมตกกระทบเท่ากับมุมสะท้อนเสมอ",
                  "การมองเห็นภาพทิวทัศน์บนผิวน้ำที่นิ่งสนิท")),
        Category("การหักเหของแสง (Refraction)",
                 ("การมองเห็นเหรียญที่อยู่ก้นถ้วยน้ำดูเหมือนอยู่ตื้นขึ้น",
                  "แนวลำแสงเปลี่ยนทิศเมื่อเดินทางผ่านปริซึม",
                  "การมองเห็นหลอดดูดน้ำดูเหมือนหักงอในแก้วน้ำ",
                  "การมองเห็นปลาในน้ำดูตื้นกว่าความเป็นจริง",
                  "การทำงานของเลนส์นูนและเลนส์เว้า")),
    ]


@question_type("phys.reflection_law",
               display_name={"th": "กฎการสะท้อนของแสง"},
               level={"th": "ม.3"}, subject=SUBJECT, topic=TOPIC)
class ReflectionLaw(PhysCalc):
    """มุมตกกระทบ = มุมสะท้อน (วัดจากเส้นแนวฉาก) และมุมระหว่างรังสีทั้งสอง = 2 เท่า."""

    def draw(self, rng: Random) -> Calc:
        th = rng.randint(10, 80)
        if rng.random() < 0.5:
            return Calc(
                f"แสงตกกระทบกระจกเงาราบ ทำมุม {th}° กับเส้นแนวฉาก (เส้นปกติ) "
                f"จงหามุมสะท้อนที่วัดจากเส้นแนวฉาก (องศา)",
                str(th), wrongs=(str(2 * th), str(90 - th), str(180 - 2 * th)),
                hint=r"\text{มุมสะท้อน} = \text{มุมตกกระทบ}")
        return Calc(
            f"แสงตกกระทบกระจกเงาราบด้วยมุมตกกระทบ {th}° "
            f"จงหามุมระหว่างรังสีตกกระทบกับรังสีสะท้อน (องศา)",
            str(2 * th), wrongs=(str(th), str(90 - th), str(90 + th)),
            hint=r"\text{มุมระหว่างรังสี} = 2 \times \text{มุมตกกระทบ}")


@question_type(
    "phys.reflection_application",
    display_name={"th": "การสะท้อนของแสง: ออกแบบและตีความการทดลอง"},
    level={"th": "ม.3"}, subject=PHYSICS, topic=WAVES,
)
class ReflectionApplication(QuestionType):
    """Design a reflection experiment, or read its measurements."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        which = rng.randrange(3)
        if which == 0:
            return _question(
                stem=("ต้องการทดลองเพื่ออธิบายกฎการสะท้อนของแสง "
                      "แผนการทดลองใดเหมาะสมที่สุด"),
                correct=("ฉายแสงลงบนกระจกเงาราบด้วยมุมตกกระทบหลายค่า "
                         "แล้ววัดมุมสะท้อนของแต่ละค่าเทียบกับเส้นปกติ"),
                wrongs=(
                    "ฉายแสงลงบนกระจกเงาราบด้วยมุมตกกระทบค่าเดียว แล้ววัดมุมสะท้อนเพียงครั้งเดียว",
                    "เปลี่ยนทั้งมุมตกกระทบและชนิดของกระจกไปพร้อมกันในการวัดแต่ละครั้ง",
                    "วัดความสว่างของแสงที่สะท้อนออกมาโดยไม่ต้องวัดมุมใด ๆ",
                ),
                hint="กฎนี้เป็นความสัมพันธ์ระหว่างมุมสองมุม จึงต้องวัดทั้งสองมุมที่ค่าต่าง ๆ หลายค่า",
                topic=WAVES,
            )
        if which == 1:
            angles = sorted(rng.sample([10, 20, 25, 30, 40, 50, 60, 70], 3))
            rows = "\n".join(
                f"ครั้งที่ {index}: มุมตกกระทบ {angle}°, มุมสะท้อน {angle}°"
                for index, angle in enumerate(angles, start=1)
            )
            return _question(
                stem=("วัดมุมตกกระทบและมุมสะท้อนบนกระจกเงาราบได้ดังนี้\n"
                      f"{rows}\n"
                      "ข้อสรุปใดตรงกับหลักฐานมากที่สุด"),
                correct="มุมสะท้อนเท่ากับมุมตกกระทบเสมอ เมื่อวัดเทียบกับเส้นปกติ",
                wrongs=(
                    "มุมสะท้อนมากกว่ามุมตกกระทบเสมอ",
                    "มุมสะท้อนเท่ากับมุมตกกระทบเฉพาะเมื่อมุมตกกระทบน้อยกว่า 45°",
                    "มุมสะท้อนไม่ขึ้นกับมุมตกกระทบ แต่ขึ้นกับความสว่างของแสง",
                ),
                hint="เทียบมุมสองค่าในแต่ละแถว แล้วดูว่าความสัมพันธ์เดิมเป็นจริงทุกแถวหรือไม่",
                topic=WAVES,
            )
        # 30°, 45° and 60° are left out: at each one two of the offered angles coincide.
        angle = rng.choice((10, 15, 20, 25, 35, 40, 50, 55, 65, 70, 75, 80))
        return _question(
            stem=(f"ฉายแสงลงบนกระจกเงาราบ โดยลำแสงทำมุม {angle}° กับ<u>ผิวกระจก</u> "
                  "มุมสะท้อนที่วัดเทียบกับเส้นปกติมีค่าเท่าใด"),
            correct=f"{90 - angle}°",
            wrongs=(
                f"{angle}°",
                f"{90 + angle}°",
                f"{180 - 2 * angle}°",
            ),
            hint="มุมตกกระทบและมุมสะท้อนวัดจากเส้นปกติซึ่งตั้งฉากกับผิวกระจก ไม่ได้วัดจากผิวกระจก",
            topic=WAVES,
        )
