"""สนามแม่เหล็กเนื่องจากกระแสไฟฟ้า

ฟิสิกส์ · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.2 ม.5/7

Sets moved here from: science_wave_e12.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e12 import (
    DIRECTION,
    SUBJECT,
    UPPER_FIVE,
    Vec,
    _direction_choices,
    _labelled,
    cross,
)

PROVENANCE = Provenance("original")


TOPIC_FIELD = "สนามแม่เหล็กเนื่องจากกระแสไฟฟ้า"


IN_PLANE = [v for v in DIRECTION if v[2] == 0]


FIELD_FACTS = (
    ("สนามแม่เหล็กรอบลวดตรงที่มีกระแสไฟฟ้าผ่านมีลักษณะอย่างไร",
     "เป็นวงกลมรอบเส้นลวด โดยมีเส้นลวดเป็นแกนกลาง",
     ("เป็นเส้นตรงขนานกับเส้นลวด", "เป็นเส้นตรงพุ่งออกจากเส้นลวดทุกทิศ",
      "ไม่มีสนามแม่เหล็ก เพราะลวดไม่ใช่แม่เหล็ก")),
    ("ถ้าเพิ่มกระแสไฟฟ้าที่ผ่านลวดตรง สนามแม่เหล็กรอบลวดจะเป็นอย่างไร",
     "มีขนาดมากขึ้น",
     ("มีขนาดน้อยลง", "มีขนาดเท่าเดิมแต่กลับทิศ", "หายไป")),
    ("ที่ตำแหน่งห่างจากลวดตรงที่มีกระแสไฟฟ้ามากขึ้น สนามแม่เหล็กจะเป็นอย่างไร",
     "มีขนาดน้อยลง",
     ("มีขนาดมากขึ้น", "มีขนาดเท่าเดิมทุกตำแหน่ง", "กลับทิศทุกครั้งที่ห่างออกไป")),
    ("ขดลวดโซเลนอยด์ที่มีกระแสไฟฟ้าผ่าน มีสนามแม่เหล็กคล้ายกับสิ่งใด",
     "แท่งแม่เหล็ก โดยปลายหนึ่งเป็นขั้วเหนือและอีกปลายเป็นขั้วใต้",
     ("เส้นลวดตรงหนึ่งเส้น", "ลูกโลกที่ไม่มีขั้วแม่เหล็ก", "วงกลมรอบขดลวดที่ไม่มีขั้ว")),
    ("ถ้ากลับทิศของกระแสไฟฟ้าในขดลวดโซเลนอยด์ ขั้วแม่เหล็กของขดลวดจะเป็นอย่างไร",
     "สลับกัน ปลายที่เคยเป็นขั้วเหนือกลายเป็นขั้วใต้",
     ("เหมือนเดิม", "กลายเป็นขั้วเหนือทั้งสองปลาย", "หายไปทั้งสองปลาย")),
)


ELECTROMAGNET_WAYS = (
    "เพิ่มจำนวนรอบของขดลวด",
    "เพิ่มกระแสไฟฟ้าที่ผ่านขดลวด",
    "ใส่แกนเหล็กอ่อนไว้ในขดลวด",
)


NOT_ELECTROMAGNET_WAYS = (
    "เปลี่ยนสีของฉนวนหุ้มลวด",
    "ใช้แกนพลาสติกแทนแกนเหล็กอ่อน",
    "ลดจำนวนรอบของขดลวด",
    "ลดกระแสไฟฟ้าที่ผ่านขดลวด",
    "ใช้ลวดที่ยาวขึ้นแต่พันจำนวนรอบเท่าเดิม",
)


ELECTROMAGNET_USES = (
    "เครนยกเศษเหล็กในโรงงาน", "กริ่งไฟฟ้า", "รีเลย์ในวงจรควบคุม", "ลำโพง",
    "รถไฟฟ้าแม่เหล็กลอยตัว", "เครื่องสร้างภาพด้วยสนามแม่เหล็ก (MRI)",
)


NOT_ELECTROMAGNET_USES = (
    "เทอร์มอมิเตอร์ปรอท", "แว่นขยาย", "กระจกเงาราบ", "เตาถ่าน", "หลอดไฟไส้ร้อนแบบใช้ถ่านไฟฉาย",
)


def wire_field(current: Vec, to_point: Vec) -> Vec:
    """Right-hand grip rule: B at a point is along current × (wire → point)."""
    return cross(current, to_point)


@question_type(
    "phys.current_field_foundation",
    display_name={"th": "ลักษณะของสนามแม่เหล็กรอบลวดและขดลวดที่มีกระแสไฟฟ้า"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_FIELD,
)
class CurrentFieldFoundation(QuestionType):
    """The shape of the field and what makes it stronger."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = "กระแสไฟฟ้าทำให้เกิดสนามแม่เหล็ก ยิ่งกระแสมาก สนามยิ่งมาก และยิ่งห่างจากลวด สนามยิ่งน้อย"
        if rng.random() < 0.6:
            stem, correct, wrongs = rng.choice(FIELD_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_FIELD, hint=hint)
        return _labelled(
            stem="วิธีใดทำให้แม่เหล็กไฟฟ้าที่ทำจากขดลวดมีสนามแม่เหล็กมากขึ้น",
            correct=rng.choice(ELECTROMAGNET_WAYS),
            wrongs=tuple(NOT_ELECTROMAGNET_WAYS),
            topic=TOPIC_FIELD, hint=hint,
        )


@question_type(
    "phys.current_field_fluency",
    display_name={"th": "หาทิศของสนามแม่เหล็กเนื่องจากกระแสไฟฟ้าด้วยกฎมือขวา"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_FIELD,
)
class CurrentFieldFluency(QuestionType):
    """The indicator: where the field of a current points, by the right-hand rule."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.random()
        if shape < 0.3:
            # Reverse: the field at P is known, find the current. For
            # perpendicular unit vectors, r × (I × r) = I.
            to_point = rng.choice(IN_PLANE)
            current = rng.choice([v for v in DIRECTION if cross(v, to_point) != (0, 0, 0)])
            field = wire_field(current, to_point)
            assert cross(to_point, field) == current
            side = {(1, 0, 0): "ทางขวาของ", (-1, 0, 0): "ทางซ้ายของ",
                    (0, 1, 0): "ด้านบนของ", (0, -1, 0): "ด้านล่างของ"}[to_point]
            return _labelled(
                stem=(f"จุด P อยู่{side}ลวดตรงยาวที่มีกระแสไฟฟ้า สนามแม่เหล็กที่จุด P มีทิศ"
                      f"{DIRECTION[field]} กระแสไฟฟ้าในลวดไหลไปทางใด"),
                correct=DIRECTION[current],
                wrongs=tuple(_direction_choices(current, field, to_point)),
                topic=TOPIC_FIELD,
                hint="กำมือขวาให้นิ้วทั้งสี่วนตามทิศสนามที่จุด P นิ้วหัวแม่มือจะชี้ทิศของกระแส")
        if shape < 0.75:
            # P always lies in the page, so its place is easy to say.
            current = rng.choice(list(DIRECTION))
            to_point = rng.choice([v for v in IN_PLANE if cross(current, v) != (0, 0, 0)])
            field = wire_field(current, to_point)
            side = {(1, 0, 0): "ทางขวาของ", (-1, 0, 0): "ทางซ้ายของ",
                    (0, 1, 0): "ด้านบนของ", (0, -1, 0): "ด้านล่างของ"}[to_point]
            return _labelled(
                stem=(f"ลวดตรงยาวมีกระแสไฟฟ้าไหล{DIRECTION[current]} จุด P อยู่{side}เส้นลวด "
                      "สนามแม่เหล็กที่จุด P มีทิศใด"),
                correct=DIRECTION[field],
                wrongs=tuple(_direction_choices(field, current, to_point)),
                topic=TOPIC_FIELD,
                hint="กำมือขวารอบลวดให้นิ้วหัวแม่มือชี้ตามทิศกระแส นิ้วทั้งสี่ที่วนรอบลวดชี้ทิศของสนามแม่เหล็ก",
            )
        clockwise = rng.random() < 0.5
        end = rng.choice(("ปลาย A", "ปลาย B"))
        pole = "ขั้วใต้" if clockwise else "ขั้วเหนือ"
        return _labelled(
            stem=(f"มองขดลวดโซเลนอยด์จาก{end} เห็นกระแสไฟฟ้าไหลวน"
                  f"{'ตามเข็มนาฬิกา' if clockwise else 'ทวนเข็มนาฬิกา'} {end}เป็นขั้วแม่เหล็กใด"),
            correct=f"{end}เป็น{pole}",
            wrongs=(f"{end}เป็น{'ขั้วเหนือ' if clockwise else 'ขั้วใต้'}",
                    f"{end}ไม่เป็นขั้วแม่เหล็ก เพราะขั้วอยู่ตรงกลางขดลวด",
                    f"{end}เป็นขั้วเหนือและขั้วใต้สลับกันตลอดเวลา"),
            topic=TOPIC_FIELD,
            hint="กำมือขวาให้นิ้วทั้งสี่วนตามทิศกระแสในขดลวด นิ้วหัวแม่มือชี้ไปทางขั้วเหนือ "
                 "(มองแล้วกระแสวนทวนเข็มคือขั้วเหนือ วนตามเข็มคือขั้วใต้)",
        )


@question_type(
    "phys.current_field_application",
    display_name={"th": "ใช้สนามแม่เหล็กจากกระแสไฟฟ้าอธิบายเข็มทิศและแม่เหล็กไฟฟ้า"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_FIELD,
)
class CurrentFieldApplication(QuestionType):
    """Ørsted's compass, electromagnets at work, and a field reversed."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        if shape == 0:
            return _labelled(
                stem="ข้อใดใช้หลักการของแม่เหล็กไฟฟ้า (สนามแม่เหล็กที่เกิดจากกระแสไฟฟ้า)",
                correct=rng.choice(ELECTROMAGNET_USES),
                wrongs=tuple(NOT_ELECTROMAGNET_USES),
                topic=TOPIC_FIELD,
                hint="มองหาอุปกรณ์ที่มีขดลวดซึ่งกลายเป็นแม่เหล็กเมื่อมีกระแสไฟฟ้าผ่าน")
        if shape == 1:
            return _labelled(
                stem=("วางเข็มทิศไว้ใต้ลวดตรงที่วางตามแนวเหนือ–ใต้ เมื่อเปิดสวิตช์ให้กระแสไฟฟ้าผ่านลวด "
                      "เข็มทิศเบนไปจากแนวเดิม ถ้ากลับขั้วแบตเตอรี่แล้วเปิดสวิตช์อีกครั้ง จะสังเกตเห็นอะไร"),
                correct="เข็มทิศเบนไปในทิศตรงข้ามกับครั้งแรก เพราะสนามแม่เหล็กรอบลวดกลับทิศ",
                wrongs=("เข็มทิศเบนไปทางเดิม เพราะสนามแม่เหล็กไม่ขึ้นกับทิศของกระแส",
                        "เข็มทิศไม่เบนเลย เพราะกระแสสองทิศหักล้างกัน",
                        "เข็มทิศหมุนรอบตัวเองไม่หยุด"),
                topic=TOPIC_FIELD,
                hint="ทิศของสนามแม่เหล็กรอบลวดขึ้นกับทิศของกระแส")
        n1, n2 = sorted(rng.sample((50, 100, 150, 200, 300), 2))
        i = rng.choice((1, 2, 3))
        return _labelled(
            stem=(f"แม่เหล็กไฟฟ้า ก พันลวด {n1} รอบ แม่เหล็กไฟฟ้า ข พันลวด {n2} รอบ บนแกนเหล็กอ่อนแบบเดียวกัน "
                  f"และมีกระแสไฟฟ้า {i} แอมแปร์เท่ากัน ข้อใดถูกต้อง"),
            correct="แม่เหล็กไฟฟ้า ข ดูดคลิปหนีบกระดาษได้มากกว่า เพราะมีจำนวนรอบมากกว่า",
            wrongs=("แม่เหล็กไฟฟ้า ก ดูดคลิปหนีบกระดาษได้มากกว่า เพราะลวดสั้นกว่า",
                    "ดูดคลิปหนีบกระดาษได้เท่ากัน เพราะกระแสไฟฟ้าเท่ากัน",
                    "ดูดคลิปหนีบกระดาษได้เท่ากัน เพราะใช้แกนเหล็กอ่อนแบบเดียวกัน"),
            topic=TOPIC_FIELD,
            hint="เมื่อกระแสและแกนเท่ากัน จำนวนรอบที่มากขึ้นทำให้สนามแม่เหล็กมากขึ้น")
