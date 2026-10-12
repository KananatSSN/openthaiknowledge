"""กระจกเงาทรงกลม

ฟิสิกส์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 2 ม.5/9

Sets moved here from: physics, science_wave_a7.
"""

from __future__ import annotations

from math import gcd
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import question_type
from otk.kit.concept_bank import Concept, ConceptBankType
from otk.kit.numeric_scenario import Calc, PhysCalc, fmt, slips
from otk.sets._support.physics import SUBJECT, TOPIC
from otk.sets._support.science_wave_a7 import UPPER, WAVES

PROVENANCE = Provenance("original")


# (ความยาวโฟกัส f, ระยะวัตถุ s) เซนติเมตร โดย s' = fs/(s − f) เป็นจำนวนเต็ม.
# เก็บเฉพาะ f กับ s ระยะภาพจึงคำนวณจากทั้งสองค่าเสมอ ไม่มีทางคลาดเคลื่อนจากกัน.
MIRROR_SETUPS = (
    (6, 8), (6, 9), (6, 10), (6, 15), (6, 18), (6, 24),
    (8, 10), (8, 12), (8, 24), (8, 40),
    (10, 12), (10, 14), (10, 15), (10, 30), (10, 35), (10, 60),
    (12, 15), (12, 16), (12, 18), (12, 20), (12, 21), (12, 28), (12, 30),
    (15, 18), (15, 20), (15, 24), (15, 40), (15, 60),
    (20, 24), (20, 25), (20, 28), (20, 30), (20, 36), (20, 45), (20, 60),
)


def image_distance(focal: int, distance: int) -> int:
    """s' from 1/f = 1/s + 1/s'; whole for every row of :data:`MIRROR_SETUPS`."""
    return focal * distance // (distance - focal)


def _object_height(distance: int, image: int, rng: Random) -> int:
    """An object height whose image height is also whole."""
    return distance // gcd(distance, image) * rng.randint(1, 3)


@question_type(
    "phys.spherical_mirror_foundation",
    display_name={"th": "ส่วนประกอบของกระจกเงาทรงกลมและกฎการสะท้อน"},
    level=UPPER, subject=SUBJECT, topic=WAVES,
)
class SphericalMirrorFoundation(ConceptBankType):
    """The names and the reflection law the ม.5/9 ray diagram is drawn from.

    `phys.curved_mirror` converts between R and f and says nothing about what
    either one is. Everything a learner needs before drawing a single ray —
    which point is which, which mirror converges, what the law of reflection
    says — is stated here.
    """

    ITEMS = [
        Concept(
            "จุดโฟกัสของกระจกเงาเว้าคือจุดใด",
            "จุดที่รังสีขนานกับแกนมุขสำคัญไปตัดกันหลังการสะท้อน",
            ("จุดกึ่งกลางของผิวสะท้อนของกระจก",
             "จุดศูนย์กลางของทรงกลมที่กระจกเป็นส่วนหนึ่งของมัน",
             "จุดที่วัตถุต้องวางเพื่อให้เกิดภาพเสมือนเสมอ"),
        ),
        Concept(
            "จุดศูนย์กลางความโค้งของกระจกเงาทรงกลมคือจุดใด",
            "จุดศูนย์กลางของทรงกลมที่ผิวกระจกเป็นส่วนหนึ่งของมัน",
            ("จุดที่รังสีขนานไปรวมกันหลังการสะท้อน",
             "จุดกึ่งกลางของผิวสะท้อนบนแกนมุขสำคัญ",
             "จุดที่อยู่กึ่งกลางระหว่างวัตถุกับภาพเสมอ"),
        ),
        Concept(
            "ความยาวโฟกัสของกระจกเงาทรงกลมสัมพันธ์กับรัศมีความโค้งอย่างไร",
            "ความยาวโฟกัสเป็นครึ่งหนึ่งของรัศมีความโค้ง",
            ("ความยาวโฟกัสเป็นสองเท่าของรัศมีความโค้ง",
             "ความยาวโฟกัสเท่ากับรัศมีความโค้ง",
             "ความยาวโฟกัสเป็นหนึ่งในสี่ของรัศมีความโค้ง"),
        ),
        Concept(
            "กฎการสะท้อนของแสงกล่าวไว้ว่าอย่างไร",
            "มุมตกกระทบเท่ากับมุมสะท้อน โดยวัดจากเส้นแนวฉากที่จุดตกกระทบ",
            ("มุมตกกระทบเท่ากับมุมสะท้อน โดยวัดจากผิวสะท้อนที่จุดตกกระทบ",
             "มุมตกกระทบมากกว่ามุมสะท้อนเสมอ เพราะพลังงานบางส่วนสูญเสียไป",
             "มุมตกกระทบเท่ากับมุมสะท้อนเฉพาะเมื่อผิวสะท้อนเป็นระนาบเท่านั้น"),
        ),
        Concept(
            "กระจกเงานูนให้ภาพของวัตถุที่อยู่หน้ากระจกเป็นภาพแบบใดเสมอ",
            "ภาพเสมือน หัวตั้ง และมีขนาดเล็กกว่าวัตถุ",
            ("ภาพจริง หัวกลับ และมีขนาดเล็กกว่าวัตถุ",
             "ภาพเสมือน หัวตั้ง และมีขนาดใหญ่กว่าวัตถุ",
             "ภาพจริง หัวตั้ง และมีขนาดเท่ากับวัตถุ"),
        ),
        Concept(
            "เหตุใดจุดโฟกัสของกระจกเงานูนจึงเรียกว่าจุดโฟกัสเสมือน",
            "เพราะรังสีสะท้อนกระจายออก ต้องต่อแนวรังสีย้อนกลับไปจึงจะพบจุดตัดหลังกระจก",
            ("เพราะรังสีสะท้อนไปรวมกันจริงที่หน้ากระจก แต่มองไม่เห็นด้วยตาเปล่า",
             "เพราะกระจกนูนไม่มีจุดโฟกัส จึงสมมติจุดหนึ่งขึ้นมาใช้ในการคำนวณ",
             "เพราะตำแหน่งของจุดโฟกัสเปลี่ยนไปตามระยะของวัตถุที่วางไว้"),
        ),
        Concept(
            "รังสีที่พุ่งเข้าหาจุดศูนย์กลางความโค้งของกระจกเงาเว้า จะสะท้อนอย่างไร",
            "สะท้อนกลับไปตามแนวเดิม เพราะตกกระทบผิวกระจกในแนวตั้งฉาก",
            ("สะท้อนออกไปขนานกับแกนมุขสำคัญ",
             "สะท้อนผ่านจุดโฟกัสของกระจก",
             "สะท้อนไปยังจุดกึ่งกลางของผิวกระจกเสมอ"),
        ),
        Concept("กระจกเงาเว้ามีรัศมีความโค้ง 40 เซนติเมตร ความยาวโฟกัสเป็นเท่าใด",
                "20 เซนติเมตร",
                (
                 "40 เซนติเมตร",
                 "80 เซนติเมตร",
                 "10 เซนติเมตร",
                 "60 เซนติเมตร",
                 "4 เซนติเมตร")),
        Concept("รังสีที่ผ่านจุดโฟกัสแล้วตกกระทบกระจกเงาเว้า จะสะท้อนอย่างไร",
                "สะท้อนออกไปขนานกับแกนมุขสำคัญ",
                (
                 "สะท้อนผ่านจุดโฟกัสอีกครั้ง",
                 "สะท้อนกลับไปตามแนวเดิม",
                 "สะท้อนผ่านจุดศูนย์กลางความโค้ง",
                 "ทะลุผ่านกระจกออกไป",
                 "สะท้อนตั้งฉากกับแกนมุขสำคัญ")),
        Concept("ไฟหน้ารถยนต์วางหลอดไฟไว้ที่จุดโฟกัสของกระจกเงาเว้า เพื่อประโยชน์ใด",
                "ให้แสงสะท้อนออกไปเป็นลำขนานส่องได้ไกล",
                (
                 "ให้แสงรวมเป็นจุดเล็ก ๆ จุดเดียวหน้ารถ",
                 "ให้เห็นภาพหลอดไฟขยายใหญ่",
                 "ให้แสงกระจายออกทุกทิศเท่ากัน",
                 "ลดความร้อนของหลอดไฟ",
                 "ให้แสงสะท้อนกลับเข้าหลอดไฟ")),
        Concept("วางวัตถุไว้ที่จุดศูนย์กลางความโค้งของกระจกเงาเว้า ภาพที่ได้เป็นอย่างไร",
                "ภาพจริง หัวกลับ ขนาดเท่าวัตถุ อยู่ที่จุดศูนย์กลางความโค้ง",
                (
                 "ภาพเสมือน หัวตั้ง ขนาดใหญ่กว่าวัตถุ",
                 "ภาพจริง หัวกลับ ขนาดเล็กกว่าวัตถุ อยู่ที่จุดโฟกัส",
                 "ไม่เกิดภาพ",
                 "ภาพเสมือน หัวตั้ง ขนาดเท่าวัตถุ",
                 "ภาพจริง หัวตั้ง ขนาดใหญ่กว่าวัตถุ")),
    ]


@question_type("phys.curved_mirror",
               display_name={"th": "กระจกเงาโค้ง (รัศมีความโค้งและโฟกัส)"},
               level={"th": "ม.3"}, subject=SUBJECT, topic=TOPIC)
class CurvedMirror(PhysCalc):
    """กระจกเงาโค้ง: ความยาวโฟกัสเป็นครึ่งหนึ่งของรัศมีความโค้ง (f = R/2)."""

    def draw(self, rng: Random) -> Calc:
        f = rng.randint(4, 30)
        radius = 2 * f
        if rng.random() < 0.5:
            return Calc(
                f"กระจกเงาโค้งมีรัศมีความโค้ง {radius} เซนติเมตร "
                f"จงหาความยาวโฟกัส (เซนติเมตร)",
                str(f), wrongs=(str(radius), str(4 * f), str(f + 5)),
                hint=r"f = \frac{R}{2}")
        return Calc(
            f"กระจกเงาโค้งมีความยาวโฟกัส {f} เซนติเมตร "
            f"จงหารัศมีความโค้ง (เซนติเมตร)",
            str(radius), wrongs=(str(f), str(4 * f), str(radius + 10)),
            hint=r"R = 2f")


@question_type(
    "phys.spherical_mirror_application",
    display_name={"th": "ตำแหน่งและขนาดของภาพจากกระจกเงาทรงกลม"},
    level=UPPER, subject=SUBJECT, topic=WAVES,
)
class SphericalMirrorApplication(PhysCalc):
    """Compute where the image lands and how big it is — ``ม.5/9`` in full.

    The ม.3 sets say which *kind* of image forms in each region; ``ม.5/9`` asks
    for the numbers, which needs the mirror equation and the magnification, and
    the third direction below needs both applied backwards.
    """

    def draw(self, rng: Random) -> Calc:
        focal, distance = rng.choice(MIRROR_SETUPS)
        image = image_distance(focal, distance)
        which = rng.random()
        if which < 0.4:
            return Calc(
                f"วางวัตถุห่างจากกระจกเงาเว้าที่มีความยาวโฟกัส {focal} เซนติเมตร "
                f"เป็นระยะ {distance} เซนติเมตร ภาพเกิดขึ้นห่างจากกระจกเท่าใด "
                "(เซนติเมตร)",
                fmt(image),
                # ลบระยะแทนการใช้สมการกระจก, ใช้รัศมีความโค้ง, หรือคิดว่าภาพอยู่ที่โฟกัส
                wrongs=slips(fmt(image), distance - focal, 2 * focal, focal),
                hint=r"\frac{1}{f} = \frac{1}{s} + \frac{1}{s'}")
        if which < 0.75:
            height = _object_height(distance, image, rng)
            tall = height * image // distance
            return Calc(
                f"วางวัตถุสูง {height} เซนติเมตร ห่างจากกระจกเงาเว้าที่มีความยาวโฟกัส "
                f"{focal} เซนติเมตร เป็นระยะ {distance} เซนติเมตร "
                "ภาพที่เกิดขึ้นสูงเท่าใด (เซนติเมตร)",
                fmt(tall),
                # ใช้สัดส่วนกลับด้าน, ตอบขนาดวัตถุเดิม, หรือใช้ระยะภาพเป็นความสูง
                wrongs=slips(fmt(tall), height * distance / image, height, image),
                hint=r"\frac{h'}{h} = \frac{s'}{s}")
        return Calc(
            f"วัตถุอยู่ห่างจากกระจกเงาเว้า {distance} เซนติเมตร และเกิดภาพจริง "
            f"ห่างจากกระจก {image} เซนติเมตร กระจกนี้มีความยาวโฟกัสเท่าใด "
            "(เซนติเมตร)",
            fmt(focal),
            # เฉลี่ยสองระยะ, ผลต่างของสองระยะ, หรือครึ่งหนึ่งของระยะวัตถุ
            wrongs=slips(fmt(focal), (distance + image) / 2, abs(distance - image),
                         distance / 2),
            hint=r"\frac{1}{f} = \frac{1}{s} + \frac{1}{s'}")
