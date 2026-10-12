"""ภาพจากกระจกเงา

ฟิสิกส์ · ม.3 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.3/14

Sets moved here from: physics, science_wave_a4.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.classify import Category, ClassifyType
from otk.kit.numeric_scenario import Calc, PhysCalc
from otk.sets._support.physics import SUBJECT, TOPIC
from otk.sets._support.science_wave_a4 import (
    FOCAL_LENGTHS,
    PHYSICS,
    WAVES,
    _converging_distance,
    _converging_image,
    _distinct,
    _image_wrongs,
    _question,
)

PROVENANCE = Provenance("original")


# (รังสีตกกระทบ, แนวการสะท้อน) — รังสีหลักที่ใช้เขียนแผนภาพการเกิดภาพจากกระจกโค้ง
MIRROR_RAY_RULES = (
    ("รังสีที่ขนานกับแกนมุขสำคัญตกกระทบ<u>กระจกเว้า</u>",
     "สะท้อนผ่านจุดโฟกัส (F) ที่อยู่หน้ากระจก"),
    ("รังสีที่พุ่งผ่านจุดโฟกัส (F) ไปตกกระทบ<u>กระจกเว้า</u>",
     "สะท้อนออกไปขนานกับแกนมุขสำคัญ"),
    ("รังสีที่พุ่งผ่านจุดศูนย์กลางความโค้ง (C) ไปตกกระทบ<u>กระจกเว้า</u>",
     "สะท้อนย้อนกลับไปตามแนวเดิม"),
    ("รังสีที่ขนานกับแกนมุขสำคัญตกกระทบ<u>กระจกนูน</u>",
     "สะท้อนออกไปในแนวที่เสมือนว่าพุ่งออกมาจากจุดโฟกัสหลังกระจก"),
)


MIRROR_RAY_PATHS = tuple(path for _, path in MIRROR_RAY_RULES)


@question_type(
    "phys.mirror_image_foundation",
    display_name={"th": "ภาพจากกระจกเงา: รังสีหลักและชนิดของภาพ"},
    level={"th": "ม.3"}, subject=PHYSICS, topic=WAVES,
)
class MirrorImageFoundation(QuestionType):
    """Name one principal ray, or state one basic property of a mirror image."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.45:
            distance = rng.randint(5, 150)
            who = rng.choice(("นักเรียน", "ตุ๊กตา", "แจกัน", "เทียนไข", "นาฬิกา"))
            if rng.random() < 0.5:
                return _question(
                    stem=f"{who}อยู่หน้ากระจกเงาราบ ห่างจากกระจก {distance} เซนติเมตร ภาพอยู่ห่างจากกระจกเท่าใด",
                    correct=f"{distance} เซนติเมตร หลังกระจก",
                    wrongs=(f"{distance} เซนติเมตร หน้ากระจก", f"{2 * distance} เซนติเมตร หลังกระจก",
                            f"{3 * distance} เซนติเมตร หลังกระจก"),
                    hint="ภาพในกระจกเงาราบอยู่หลังกระจกเป็นระยะเท่ากับระยะวัตถุ",
                )
            return _question(
                stem=f"{who}อยู่หน้ากระจกเงาราบ ห่างจากกระจก {distance} เซนติเมตร {who}กับภาพของ{who}อยู่ห่างกันเท่าใด",
                correct=f"{2 * distance} เซนติเมตร",
                wrongs=(f"{distance} เซนติเมตร", f"{3 * distance} เซนติเมตร", f"{4 * distance} เซนติเมตร"),
                hint="ภาพอยู่หลังกระจกเท่ากับระยะวัตถุหน้ากระจก ระยะระหว่างวัตถุกับภาพจึงเป็นสองเท่า",
            )
        which = rng.randrange(8)
        if which < 4:
            ray, path = MIRROR_RAY_RULES[which]
            wrongs = _distinct(path, [other for other in MIRROR_RAY_PATHS if other != path])
            assert wrongs is not None
            return _question(
                stem=f"{ray} จะสะท้อนไปในแนวใด",
                correct=path,
                wrongs=wrongs,
                hint="เขียนรังสีหลักทีละเส้น แล้วดูว่าเส้นนั้นผ่านจุดโฟกัสหรือจุดศูนย์กลางความโค้งหรือไม่",
            )
        if which == 4:
            return _question(
                stem="ภาพจริงกับภาพเสมือนต่างกันอย่างไร",
                correct="ภาพจริงเกิดจากรังสีของแสงมาตัดกันจริง จึงรับภาพบนฉากได้ ส่วนภาพเสมือนรับบนฉากไม่ได้",
                wrongs=(
                    "ภาพจริงมีขนาดเท่าวัตถุเสมอ ส่วนภาพเสมือนมีขนาดเล็กกว่าวัตถุเสมอ",
                    "ภาพจริงเป็นภาพหัวตั้งเสมอ ส่วนภาพเสมือนเป็นภาพหัวกลับเสมอ",
                    "ภาพจริงเกิดจากกระจกเงาราบ ส่วนภาพเสมือนเกิดจากกระจกโค้งเท่านั้น",
                ),
                hint="เกณฑ์ตัดสินคือรังสีของแสงมาตัดกันจริงหรือไม่ ไม่ใช่ขนาดหรือทิศของภาพ",
            )
        if which == 5:
            return _question(
                stem="ภาพที่เกิดจากกระจกเงาราบมีลักษณะอย่างไร",
                correct="ภาพเสมือน หัวตั้ง ขนาดเท่าวัตถุ และอยู่หลังกระจกเป็นระยะเท่ากับระยะวัตถุ",
                wrongs=(
                    "ภาพจริง หัวกลับ ขนาดเท่าวัตถุ และอยู่หน้ากระจกเป็นระยะเท่ากับระยะวัตถุ",
                    "ภาพเสมือน หัวตั้ง ขนาดใหญ่กว่าวัตถุ และอยู่หลังกระจกไกลกว่าระยะวัตถุ",
                    "ภาพเสมือน หัวกลับ ขนาดเล็กกว่าวัตถุ และอยู่หลังกระจกใกล้กว่าระยะวัตถุ",
                ),
                hint="ลองยืนหน้ากระจกเงาราบแล้วสังเกตว่าภาพหัวตั้งหรือหัวกลับ และดูใหญ่ขึ้นหรือไม่",
            )
        if which == 6:
            return _question(
                stem="กระจกชนิดใดให้ภาพเสมือน หัวตั้ง ขนาดเล็กกว่าวัตถุ ไม่ว่าจะวางวัตถุไว้ที่ระยะใด",
                correct="กระจกนูน",
                wrongs=(
                    "กระจกเว้า",
                    "กระจกเงาราบ",
                    "กระจกเว้าเมื่อวางวัตถุไว้ที่จุดศูนย์กลางความโค้ง",
                ),
                hint="กระจกที่ผิวสะท้อนโค้งออกจะกระจายแสง จึงไม่มีรังสีมาตัดกันจริงเลย",
            )
        return _question(
            stem="แกนมุขสำคัญของกระจกโค้งหมายถึงเส้นใด",
            correct="เส้นตรงที่ลากผ่านจุดกึ่งกลางกระจกและจุดศูนย์กลางความโค้ง",
            wrongs=(
                "เส้นตรงที่ลากผ่านจุดโฟกัสและตั้งฉากกับผิวกระจกที่ขอบกระจก",
                "เส้นตรงที่ลากจากวัตถุไปยังจุดโฟกัสของกระจก",
                "เส้นโค้งที่ลากไปตามผิวสะท้อนของกระจก",
            ),
            hint="เป็นเส้นอ้างอิงที่ผ่านกึ่งกลางกระจก ใช้วัดระยะวัตถุและระยะภาพ",
        )


@question_type("phys.curved_mirror_image",
               display_name={"th": "ภาพที่เกิดจากกระจกเงาโค้ง"},
               level={"th": "ม.3"}, subject=SUBJECT, topic=TOPIC)
class CurvedMirrorImage(ClassifyType):
    """โยงตำแหน่งวัตถุหน้ากระจกเว้า/กระจกนูน เข้ากับลักษณะของภาพที่เกิดขึ้น."""

    CLASSIFY_STEM = "สถานการณ์ต่อไปนี้ทำให้เกิดภาพลักษณะใด: “{member}”"
    PICK_STEM = "ข้อใดคือสถานการณ์ที่ทำให้เกิด{category}"

    CATEGORIES = [
        Category("ภาพจริง หัวกลับ ขนาดเล็กกว่าวัตถุ",
                 ("วางวัตถุไว้ไกลกว่าจุดศูนย์กลางความโค้ง (C) ของกระจกเว้า",)),
        Category("ภาพจริง หัวกลับ ขนาดเท่าวัตถุ",
                 ("วางวัตถุไว้ที่จุดศูนย์กลางความโค้ง (C) ของกระจกเว้า",)),
        Category("ภาพจริง หัวกลับ ขนาดใหญ่กว่าวัตถุ",
                 ("วางวัตถุไว้ระหว่างจุดศูนย์กลางความโค้ง (C) กับจุดโฟกัส (F) ของกระจกเว้า",)),
        Category("ภาพเสมือน หัวตั้ง ขนาดใหญ่กว่าวัตถุ",
                 ("วางวัตถุไว้ระหว่างจุดโฟกัส (F) กับหน้ากระจกเว้า",)),
        Category("ภาพเสมือน หัวตั้ง ขนาดเล็กกว่าวัตถุ",
                 ("วางวัตถุไว้หน้ากระจกนูนที่ระยะใดๆ",
                  "การมองภาพในกระจกมองหลัง (กระจกนูน) ของรถยนต์")),
    ]


@question_type("phys.plane_mirror_image",
               display_name={"th": "ภาพที่เกิดจากกระจกเงาราบ"},
               level={"th": "ม.3"}, subject=SUBJECT, topic=TOPIC)
class PlaneMirrorImage(PhysCalc):
    """ภาพในกระจกเงาราบ: เสมือน หัวตั้ง ขนาดเท่าวัตถุ ระยะภาพ = ระยะวัตถุ."""

    def draw(self, rng: Random) -> Calc:
        r = rng.random()
        if r < 0.34:
            d = rng.randint(5, 60)
            return Calc(
                f"วางวัตถุห่างจากกระจกเงาราบ {d} เซนติเมตร "
                f"ภาพที่เกิดขึ้นอยู่หลังกระจกกี่เซนติเมตร",
                str(d), wrongs=(str(2 * d), str(d + 10), "0"),
                hint=r"\text{ระยะภาพ} = \text{ระยะวัตถุ}")
        if r < 0.67:
            d = rng.randint(5, 60)
            return Calc(
                f"วัตถุอยู่ห่างกระจกเงาราบ {d} เซนติเมตร "
                f"ระยะจากวัตถุถึงภาพเป็นกี่เซนติเมตร",
                str(2 * d), wrongs=(str(d), str(4 * d), str(d + 20)),
                hint=r"\text{ระยะวัตถุถึงภาพ} = 2 \times \text{ระยะวัตถุ}")
        h = rng.randint(2, 40)
        return Calc(
            f"วัตถุสูง {h} เซนติเมตร วางหน้ากระจกเงาราบ ภาพที่เกิดขึ้นสูงกี่เซนติเมตร",
            str(h), wrongs=(str(2 * h), str(h + 5), "0"),
            hint=r"\text{ขนาดภาพ} = \text{ขนาดวัตถุ}")


@question_type(
    "phys.mirror_image_application",
    display_name={"th": "ภาพจากกระจกเงา: ทำนายภาพและเลือกกระจกให้เหมาะกับงาน"},
    level={"th": "ม.3"}, subject=PHYSICS, topic=WAVES,
)
class MirrorImageApplication(QuestionType):
    """Predict the image from an object position, or pick a mirror for a job."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        which = rng.randrange(4)
        if which == 0:
            focal = rng.choice(FOCAL_LENGTHS)
            distance = _converging_distance(rng, focal)
            correct = _converging_image(distance, focal)
            return _question(
                stem=(f"วางวัตถุไว้หน้ากระจกเว้าที่มีความยาวโฟกัส {focal} เซนติเมตร "
                      f"โดยวัตถุอยู่ห่างจากกระจก {distance} เซนติเมตร "
                      "ภาพที่เกิดขึ้นมีลักษณะอย่างไร"),
                correct=correct,
                wrongs=_image_wrongs(correct, rng),
                hint=(f"เทียบระยะวัตถุกับจุดโฟกัส ({focal} ซม.) และจุดศูนย์กลางความโค้ง "
                      f"({2 * focal} ซม.) ก่อนเขียนแผนภาพรังสี"),
            )
        if which == 1:
            return _question(
                stem="ร้านค้าต้องการติดกระจกหนึ่งบานเพื่อให้พนักงานมองเห็นบริเวณกว้างที่สุด ควรเลือกกระจกชนิดใด เพราะเหตุใด",
                correct="กระจกนูน เพราะให้ภาพเสมือนขนาดเล็กกว่าวัตถุ จึงเห็นบริเวณได้กว้างขึ้น",
                wrongs=(
                    "กระจกเว้า เพราะให้ภาพเสมือนขนาดใหญ่กว่าวัตถุ จึงเห็นบริเวณได้กว้างขึ้น",
                    "กระจกเงาราบ เพราะให้ภาพขนาดเท่าวัตถุ จึงเห็นบริเวณได้กว้างที่สุด",
                    "กระจกเว้า เพราะรวมแสงให้ภาพสว่างขึ้น จึงเห็นบริเวณได้กว้างขึ้น",
                ),
                hint="ภาพยิ่งเล็กลง พื้นที่ที่ปรากฏบนกระจกบานเดิมยิ่งกว้างขึ้น",
            )
        if which == 2:
            return _question(
                stem="ทันตแพทย์ต้องการกระจกที่ส่องดูฟันแล้วเห็นภาพขยายใหญ่ ควรใช้กระจกชนิดใดและวางอย่างไร",
                correct="กระจกเว้า โดยวางให้ฟันอยู่ใกล้กระจกกว่าจุดโฟกัส",
                wrongs=(
                    "กระจกเว้า โดยวางให้ฟันอยู่ไกลกว่าจุดศูนย์กลางความโค้ง",
                    "กระจกนูน โดยวางให้ฟันอยู่ใกล้ผิวกระจกมาก ๆ",
                    "กระจกเงาราบ โดยวางให้ฟันอยู่ใกล้ผิวกระจกมาก ๆ",
                ),
                hint="ภาพเสมือนขนาดใหญ่กว่าวัตถุจากกระจกเว้าเกิดเมื่อวัตถุอยู่ในระยะโฟกัสเข้ามา",
            )
        near, far = sorted(rng.sample([6, 8, 12, 18, 24, 30], 2))
        return _question(
            stem=("วางเทียนไขหน้ากระจกเว้าบานหนึ่งแล้วบันทึกผลได้ดังนี้\n"
                  f"ครั้งที่ 1: ระยะวัตถุ {far} ซม. รับภาพบนฉากได้ เป็นภาพหัวกลับ\n"
                  f"ครั้งที่ 2: ระยะวัตถุ {near} ซม. รับภาพบนฉากไม่ได้ มองผ่านกระจกเห็นภาพหัวตั้งขนาดใหญ่\n"
                  "ข้อสรุปใดตรงกับหลักฐานมากที่สุด"),
            correct=f"ความยาวโฟกัสของกระจกอยู่ระหว่าง {near} ถึง {far} เซนติเมตร",
            wrongs=(
                f"ความยาวโฟกัสของกระจกน้อยกว่า {near} เซนติเมตร",
                f"ความยาวโฟกัสของกระจกมากกว่า {far} เซนติเมตร",
                "กระจกบานนี้เป็นกระจกนูน เพราะให้ภาพหัวตั้งขนาดใหญ่ได้",
            ),
            hint="ภาพจริงเกิดเมื่อวัตถุอยู่ไกลกว่าจุดโฟกัส ส่วนภาพเสมือนขนาดใหญ่เกิดเมื่อวัตถุอยู่ใกล้กว่าจุดโฟกัส",
        )
