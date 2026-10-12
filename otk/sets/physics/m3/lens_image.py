"""ภาพจากเลนส์

ฟิสิกส์ · ม.3 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.3/16, ว 2.3 ม.3/18

Sets moved here from: physics, science_wave_a4.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.classify import Category, ClassifyType
from otk.sets._support.physics import SUBJECT, TOPIC
from otk.sets._support.science_wave_a4 import (
    FOCAL_LENGTHS,
    IMAGE_REAL_LARGER,
    IMAGE_REAL_SMALLER,
    IMAGE_VIRTUAL_LARGER,
    IMAGE_VIRTUAL_SMALLER,
    PHYSICS,
    WAVES,
    _converging_distance,
    _converging_image,
    _distinct,
    _image_wrongs,
    _question,
)

PROVENANCE = Provenance("original")


# (รังสีตกกระทบ, แนวการหักเห) — รังสีหลักที่ใช้เขียนแผนภาพการเกิดภาพจากเลนส์บาง
LENS_RAY_RULES = (
    ("รังสีที่ขนานกับแกนมุขสำคัญผ่าน<u>เลนส์นูน</u>",
     "หักเหไปรวมกันที่จุดโฟกัสอีกด้านหนึ่งของเลนส์"),
    ("รังสีที่ขนานกับแกนมุขสำคัญผ่าน<u>เลนส์เว้า</u>",
     "หักเหกระจายออกในแนวที่เสมือนว่าพุ่งมาจากจุดโฟกัสด้านเดียวกับแสงตกกระทบ"),
    ("รังสีที่พุ่งผ่านจุดกึ่งกลางของ<u>เลนส์บาง</u>",
     "ทะลุผ่านไปเป็นแนวตรงโดยไม่เบี่ยงเบน"),
    ("รังสีที่พุ่งผ่านจุดโฟกัสด้านหน้าของ<u>เลนส์นูน</u>",
     "หักเหออกไปขนานกับแกนมุขสำคัญ"),
)


LENS_RAY_PATHS = tuple(path for _, path in LENS_RAY_RULES)


@question_type(
    "phys.lens_image_foundation",
    display_name={"th": "ภาพจากเลนส์: รังสีหลักและชนิดของเลนส์"},
    level={"th": "ม.3"}, subject=PHYSICS, topic=WAVES,
)
class LensImageFoundation(QuestionType):
    """Name one principal ray, or state one basic property of a thin lens."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.45:
            focal = rng.choice(FOCAL_LENGTHS + (4, 25, 30))
            if rng.random() < 0.5:
                return _question(
                    stem=(f"ฉายลำแสงขนานกับแกนมุขสำคัญผ่านเลนส์นูนที่มีความยาวโฟกัส {focal} เซนติเมตร "
                          "ลำแสงจะรวมกันที่ใด"),
                    correct=f"ที่จุดโฟกัส ห่างจากเลนส์ {focal} เซนติเมตร อีกด้านหนึ่งของเลนส์",
                    wrongs=(f"ห่างจากเลนส์ {2 * focal} เซนติเมตร อีกด้านหนึ่งของเลนส์",
                            f"ที่จุดโฟกัส ห่างจากเลนส์ {focal} เซนติเมตร ด้านเดียวกับแสงตกกระทบ",
                            "ไม่รวมกัน เพราะเลนส์นูนกระจายแสง"),
                    hint="เลนส์นูนรวมลำแสงขนานไปที่จุดโฟกัสด้านตรงข้ามกับแสงตกกระทบ",
                )
            return _question(
                stem=f"เลนส์นูนมีความยาวโฟกัส {focal} เซนติเมตร จุด 2F อยู่ห่างจากจุดกึ่งกลางเลนส์เท่าใด",
                correct=f"{2 * focal} เซนติเมตร",
                wrongs=(f"{focal} เซนติเมตร", f"{focal + 2} เซนติเมตร", f"{4 * focal} เซนติเมตร"),
                hint="2F อยู่ห่างจากเลนส์เป็นสองเท่าของความยาวโฟกัส",
            )
        which = rng.randrange(8)
        if which < 4:
            ray, path = LENS_RAY_RULES[which]
            wrongs = _distinct(path, [other for other in LENS_RAY_PATHS if other != path])
            assert wrongs is not None
            return _question(
                stem=f"{ray} จะหักเหไปในแนวใด",
                correct=path,
                wrongs=wrongs,
                hint="เลนส์นูนรวมแสงเข้าหาจุดโฟกัส ส่วนเลนส์เว้ากระจายแสงออกจากจุดโฟกัส",
            )
        if which == 4:
            return _question(
                stem="เลนส์นูนมีลักษณะรูปร่างอย่างไร",
                correct="ตรงกลางหนากว่าขอบ",
                wrongs=(
                    "ตรงกลางบางกว่าขอบ",
                    "หนาเท่ากันตลอดทั้งแผ่น",
                    "ผิวโค้งเฉพาะด้านที่แสงตกกระทบเท่านั้น",
                ),
                hint="เนื้อแก้วที่หนากว่าจะหักเหแสงมากกว่า จึงบีบให้ลำแสงเข้ามารวมกัน",
            )
        if which == 5:
            return _question(
                stem="ความยาวโฟกัสของเลนส์บางหมายถึงระยะใด",
                correct="ระยะจากจุดกึ่งกลางเลนส์ถึงจุดโฟกัส",
                wrongs=(
                    "ระยะจากจุดกึ่งกลางเลนส์ถึงวัตถุ",
                    "ระยะจากวัตถุถึงภาพที่เกิดขึ้น",
                    "ระยะจากขอบเลนส์ถึงแกนมุขสำคัญ",
                ),
                hint="วัดจากกลางเลนส์ไปยังจุดที่ลำแสงขนานมารวมกัน",
            )
        if which == 6:
            return _question(
                stem="ภาพที่เกิดจากเลนส์เว้ามีลักษณะอย่างไร ไม่ว่าจะวางวัตถุไว้ที่ระยะใด",
                correct=IMAGE_VIRTUAL_SMALLER,
                wrongs=(
                    IMAGE_VIRTUAL_LARGER,
                    IMAGE_REAL_SMALLER,
                    IMAGE_REAL_LARGER,
                ),
                hint="เลนส์เว้ากระจายแสงออก จึงไม่มีรังสีมาตัดกันจริงให้รับบนฉากได้",
            )
        return _question(
            stem="จุดโฟกัสของเลนส์นูนหาได้อย่างไร",
            correct="ฉายลำแสงขนานผ่านเลนส์ แล้วหาตำแหน่งที่ลำแสงมารวมกันเป็นจุดสว่างที่สุด",
            wrongs=(
                "วัดจากขอบเลนส์ด้านหนึ่งไปยังขอบอีกด้านหนึ่ง แล้วหารด้วยสอง",
                "วางวัตถุไว้ชิดเลนส์ แล้ววัดระยะจากวัตถุถึงเลนส์",
                "วัดความหนาของเนื้อเลนส์ตรงกึ่งกลาง",
            ),
            hint="จุดโฟกัสคือจุดที่ลำแสงขนานกับแกนมุขสำคัญมารวมกันหลังผ่านเลนส์",
        )


@question_type("phys.lens_image",
               display_name={"th": "เลนส์และภาพที่เกิดจากเลนส์นูนและเลนส์เว้า"},
               level={"th": "ม.3"}, subject=SUBJECT, topic=TOPIC)
class LensImage(ClassifyType):
    """โยงตำแหน่งวัตถุหน้าเลนส์นูน/เลนส์เว้า เข้ากับลักษณะของภาพที่เกิดขึ้น."""

    CLASSIFY_STEM = "สถานการณ์ต่อไปนี้ทำให้เกิดภาพลักษณะใด: “{member}”"
    PICK_STEM = "ข้อใดคือสถานการณ์ที่ทำให้เกิด{category}"

    CATEGORIES = [
        Category("ภาพจริง หัวกลับ ขนาดเล็กกว่าวัตถุ",
                 ("วางวัตถุไว้ไกลกว่าระยะสองเท่าของโฟกัส (2F) หน้าเลนส์นูน",)),
        Category("ภาพจริง หัวกลับ ขนาดเท่าวัตถุ",
                 ("วางวัตถุไว้ที่ระยะสองเท่าของโฟกัส (2F) หน้าเลนส์นูน",)),
        Category("ภาพจริง หัวกลับ ขนาดใหญ่กว่าวัตถุ",
                 ("วางวัตถุไว้ระหว่างระยะ 2F กับจุดโฟกัส (F) ของเลนส์นูน",)),
        Category("ภาพเสมือน หัวตั้ง ขนาดใหญ่กว่าวัตถุ",
                 ("วางวัตถุไว้ระหว่างจุดโฟกัส (F) กับเลนส์นูน (เช่น การใช้แว่นขยาย)",)),
        Category("ภาพเสมือน หัวตั้ง ขนาดเล็กกว่าวัตถุ",
                 ("วางวัตถุไว้หน้าเลนส์เว้าที่ระยะใดๆ",)),
    ]


@question_type(
    "phys.lens_image_application",
    display_name={"th": "ภาพจากเลนส์: ทำนายภาพและเลือกตำแหน่งวางวัตถุ"},
    level={"th": "ม.3"}, subject=PHYSICS, topic=WAVES,
)
class LensImageApplication(QuestionType):
    """Predict the image from an object position, or place an object for a job."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        which = rng.randrange(4)
        if which == 0:
            focal = rng.choice(FOCAL_LENGTHS)
            distance = _converging_distance(rng, focal)
            correct = _converging_image(distance, focal)
            return _question(
                stem=(f"วางวัตถุไว้หน้าเลนส์นูนที่มีความยาวโฟกัส {focal} เซนติเมตร "
                      f"โดยวัตถุอยู่ห่างจากเลนส์ {distance} เซนติเมตร "
                      "ภาพที่เกิดขึ้นมีลักษณะอย่างไร"),
                correct=correct,
                wrongs=_image_wrongs(correct, rng),
                hint=(f"เทียบระยะวัตถุกับความยาวโฟกัส ({focal} ซม.) และระยะสองเท่าของโฟกัส "
                      f"({2 * focal} ซม.) ก่อนเขียนแผนภาพรังสี"),
            )
        if which == 1:
            focal = rng.choice(FOCAL_LENGTHS)
            return _question(
                stem=(f"ต้องการใช้เลนส์นูนที่มีความยาวโฟกัส {focal} เซนติเมตร เป็นแว่นขยาย "
                      "ควรวางวัตถุไว้ที่ระยะใด"),
                correct=f"ห่างจากเลนส์น้อยกว่า {focal} เซนติเมตร",
                wrongs=(
                    f"ห่างจากเลนส์เท่ากับ {focal} เซนติเมตรพอดี",
                    f"ห่างจากเลนส์ระหว่าง {focal} ถึง {2 * focal} เซนติเมตร",
                    f"ห่างจากเลนส์มากกว่า {2 * focal} เซนติเมตร",
                ),
                hint="แว่นขยายให้ภาพเสมือนหัวตั้งขนาดใหญ่ ซึ่งเกิดเมื่อวัตถุอยู่ในระยะโฟกัสเข้ามา",
            )
        if which == 2:
            focal = rng.choice(FOCAL_LENGTHS)
            return _question(
                stem=(f"เครื่องฉายภาพนิ่งใช้เลนส์นูนความยาวโฟกัส {focal} เซนติเมตร "
                      "ต้องการภาพบนฉากที่ใหญ่กว่าฟิล์มต้นฉบับ ควรวางฟิล์มไว้ที่ระยะใด"),
                correct=f"ระหว่าง {focal} ถึง {2 * focal} เซนติเมตรจากเลนส์",
                wrongs=(
                    f"ไกลกว่า {2 * focal} เซนติเมตรจากเลนส์",
                    f"ที่ระยะ {focal} เซนติเมตรจากเลนส์พอดี",
                    f"ใกล้เลนส์กว่า {focal} เซนติเมตร",
                ),
                hint="ภาพบนฉากต้องเป็นภาพจริง และจะใหญ่กว่าวัตถุเมื่อวัตถุอยู่ระหว่าง F กับ 2F",
            )
        focal = rng.choice(FOCAL_LENGTHS)
        return _question(
            stem=(f"เลื่อนเทียนไขเข้าหาเลนส์นูนความยาวโฟกัส {focal} เซนติเมตร ทีละน้อย "
                  f"เมื่อเทียนอยู่ห่างเลนส์น้อยกว่า {focal} เซนติเมตร พบว่ารับภาพบนฉากไม่ได้อีกต่อไป "
                  "ข้อใดอธิบายผลนี้ได้ถูกต้อง"),
            correct="รังสีที่ผ่านเลนส์ไม่มาตัดกันจริง จึงเกิดเป็นภาพเสมือนที่รับบนฉากไม่ได้",
            wrongs=(
                "แสงถูกเลนส์ดูดกลืนไปหมด จึงไม่มีแสงออกมาสร้างภาพ",
                "ภาพยังเป็นภาพจริงอยู่ แต่เล็กเกินกว่าจะมองเห็นบนฉาก",
                "เลนส์เปลี่ยนสภาพเป็นเลนส์เว้าเมื่อวัตถุเข้ามาใกล้",
            ),
            hint="ภาพจะรับบนฉากได้ก็ต่อเมื่อรังสีของแสงมาตัดกันจริงหลังผ่านเลนส์",
        )
