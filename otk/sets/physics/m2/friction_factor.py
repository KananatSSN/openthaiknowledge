"""ปัจจัยที่มีผลต่อแรงเสียดทาน

ฟิสิกส์ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 2.2 ม.2/7

Sets moved here from: science_wave_d19.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c23 import Part
from otk.sets._support.science_wave_c24 import parts_item
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d18 import SECONDARY_TWO

PROVENANCE = Provenance("original")


FRICTION_FACTOR_TOPIC = "ปัจจัยที่มีผลต่อแรงเสียดทาน"


SURFACE_PAIRS = (("พื้นพรม", "พื้นกระเบื้อง"), ("กระดาษทราย", "แผ่นกระจก"), ("พื้นไม้หยาบ", "พื้นไม้ขัดมัน"))


def factor_parts(light: int, heavy: int, rough: str, smooth: str) -> tuple[Part, ...]:
    return (
        Part("น้ำหนักที่กดลงบนพื้น", f"เมื่อเพิ่มน้ำหนักกล่องจาก {light} เป็น {heavy} นิวตัน แรงเสียดทานเพิ่มขึ้น",
             f"เมื่อเพิ่มน้ำหนักกล่องจาก {light} เป็น {heavy} นิวตัน แรงเสียดทานลดลง"),
        Part("ชนิดของผิวสัมผัส", f"{rough}ซึ่งขรุขระกว่ามีแรงเสียดทานมากกว่า{smooth}",
             f"{smooth}ซึ่งเรียบกว่ามีแรงเสียดทานมากกว่า{rough}"),
        Part("พื้นที่ผิวสัมผัส", "วางกล่องด้านกว้างหรือด้านแคบ แรงเสียดทานเท่ากัน พื้นที่ผิวสัมผัสจึงไม่มีผล",
             "วางกล่องด้านกว้างมีแรงเสียดทานมากกว่าด้านแคบเสมอ พื้นที่ผิวสัมผัสจึงมีผล"),
    )


FACTOR_CHANGES = (
    ("วางกระสอบทรายบนกระบะรถกระบะเมื่อขับบนถนนลื่น", "น้ำหนักที่กดลงบนผิวสัมผัส"),
    ("ให้เพื่อนนั่งบนเลื่อนเพื่อไม่ให้เลื่อนไถลลงเนิน", "น้ำหนักที่กดลงบนผิวสัมผัส"),
    ("เอาหนังสือออกจากกล่องก่อนเข็นกล่องข้ามห้อง", "น้ำหนักที่กดลงบนผิวสัมผัส"),
    ("ทำพื้นรองเท้าให้มีลวดลายขรุขระ", "ชนิดหรือความขรุขระของผิวสัมผัส"),
    ("โรยทรายบนถนนที่มีน้ำแข็งเกาะ", "ชนิดหรือความขรุขระของผิวสัมผัส"),
    ("ขัดพื้นไม้ให้เรียบแล้วลงแว็กซ์", "ชนิดหรือความขรุขระของผิวสัมผัส"),
    ("พันด้ามไม้แบดมินตันด้วยผ้าพันด้ามที่หนึบ", "ชนิดหรือความขรุขระของผิวสัมผัส"),
    ("ทาผงชอล์กที่มือก่อนเล่นยิมนาสติก", "ชนิดหรือความขรุขระของผิวสัมผัส"),
)


FRICTION_FACTOR_SCENARIOS = (
    ("เหตุใดรถบรรทุกที่บรรทุกของหนักจึงต้องใช้ระยะเบรกนาน แม้แรงเสียดทานที่ล้อจะมากขึ้นด้วย",
     "น้ำหนักที่มากเพิ่มแรงเสียดทาน แต่มวลที่มากก็ทำให้เปลี่ยนการเคลื่อนที่ได้ยากกว่า",
     ("น้ำหนักที่มากทำให้แรงเสียดทานลดลง", "รถบรรทุกไม่มีแรงเสียดทาน", "ยางรถบรรทุกเรียบกว่ารถเก๋งเสมอ")),
    ("นักเรียนคนหนึ่งสรุปว่า \"ยางรถที่กว้างมีแรงเสียดทานมากกว่าเพราะพื้นที่สัมผัสมากกว่า\" จากผลการทดลองในห้องเรียน ข้อใดโต้แย้งได้ดีที่สุด",
     "ในการทดลองที่ควบคุมน้ำหนักและผิวให้เท่ากัน พื้นที่ผิวสัมผัสไม่ทำให้แรงเสียดทานเปลี่ยน",
     ("ข้อสรุปถูกต้องเสมอ", "ยางกว้างไม่มีแรงเสียดทาน", "แรงเสียดทานขึ้นกับสีของยาง")),
    ("นักปีนผาทาผงชอล์กที่มือก่อนปีน เพื่อประโยชน์ใด",
     "ทำให้มือแห้งและผิวสัมผัสกับหินมีแรงเสียดทานมากขึ้น จึงจับได้แน่น",
     ("ลดแรงเสียดทานให้มือเลื่อนได้ง่าย", "ทำให้หินลื่นขึ้น", "ทำให้มือเบาลง")),
    ("นักเรียนลากกล่องบนพื้นเดียวกันสองครั้ง ครั้งที่สองเพิ่มน้ำหนักในกล่อง และใช้แรงลากมากขึ้น ข้อสรุปใดถูกต้อง",
     "น้ำหนักที่กดลงมากขึ้นทำให้แรงเสียดทานมากขึ้น",
     ("พื้นเปลี่ยนเป็นขรุขระขึ้น", "พื้นที่ผิวสัมผัสมากขึ้นจึงลากยากขึ้น", "แรงเสียดทานไม่เกี่ยวกับน้ำหนัก")),
    ("เหตุใดยางรถยนต์ที่ดอกยางสึกจนเรียบจึงอันตรายเมื่อถนนเปียก",
     "ผิวยางเรียบทำให้แรงเสียดทานกับถนนน้อยลง รถจึงลื่นไถลและเบรกได้ไม่ดี",
     ("ยางเรียบทำให้รถหนักขึ้น", "ยางเรียบทำให้แรงเสียดทานมากเกินไปจนล้อหยุดหมุน", "ดอกยางไม่มีผลต่อแรงเสียดทาน")),
)


@question_type(
    "phys.friction_factor_foundation",
    display_name={"th": "ระบุตัวแปรในการทดลองเรื่องแรงเสียดทาน"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=FRICTION_FACTOR_TOPIC,
)
class FrictionFactorFoundation(QuestionType):
    """Which variable to hold constant, and which of two set-ups has more friction."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.75:
            case = rng.choice(("weight", "surface", "area"))
            thing = rng.choice(("กล่องไม้", "ก้อนอิฐ", "หนังสือ", "กล่องพลาสติก"))
            if case == "weight":
                light, heavy = sorted(rng.sample(range(5, 41, 5), 2))
                first, second = rng.sample((light, heavy), 2)
                stem = f"ลาก{thing}หนัก {first} นิวตันกับ{thing}หนัก {second} นิวตันบนพื้นเดียวกัน แบบใดมีแรงเสียดทานมากกว่า"
                answer = f"{thing}หนัก {heavy} นิวตัน เพราะกดลงบนพื้นมากกว่า"
                wrongs = (f"{thing}หนัก {light} นิวตัน เพราะเบากว่าจึงฝืดกว่า", "เท่ากัน เพราะใช้พื้นเดียวกัน",
                          f"{thing}หนัก {light} นิวตัน เพราะกดลงบนพื้นมากกว่า")
            elif case == "surface":
                rough, smooth = rng.choice(SURFACE_PAIRS + (("พื้นคอนกรีต", "พื้นน้ำแข็ง"), ("ถนนลูกรัง", "ถนนลาดยางเรียบ")))
                first, second = rng.sample((rough, smooth), 2)
                stem = f"ลาก{thing}ชิ้นเดียวกันบน{first}และบน{second} แบบใดมีแรงเสียดทานมากกว่า"
                answer = f"บน{rough} เพราะผิวขรุขระกว่า"
                wrongs = (f"บน{smooth} เพราะผิวเรียบกว่า", "เท่ากัน เพราะเป็นวัตถุชิ้นเดียวกัน", f"บน{smooth} เพราะผิวขรุขระกว่า")
            else:
                stem = (f"ลาก{thing}ชิ้นเดียวกันบนพื้นเดียวกัน โดยวางด้านกว้างลงครั้งหนึ่งและวางด้านแคบลงอีกครั้ง "
                        "แบบใดมีแรงเสียดทานมากกว่า")
                answer = "เท่ากัน เพราะพื้นที่ผิวสัมผัสไม่มีผลต่อแรงเสียดทาน"
                wrongs = ("วางด้านกว้าง เพราะพื้นที่สัมผัสมากกว่า", "วางด้านแคบ เพราะกดลงแรงกว่า", "วางด้านกว้าง เพราะหนักกว่า")
            return _labelled(stem=stem, correct=answer, wrongs=wrongs,
                             hint="แรงเสียดทานขึ้นกับน้ำหนักที่กดลงและความขรุขระของผิว ไม่ขึ้นกับพื้นที่ผิวสัมผัส",
                             topic=FRICTION_FACTOR_TOPIC)
        factor, keep = rng.choice((
            ("ชนิดของผิวสัมผัส", "น้ำหนักของกล่องและพื้นที่ผิวสัมผัส"),
            ("น้ำหนักของกล่อง", "ชนิดของผิวสัมผัสและพื้นที่ผิวสัมผัส"),
            ("พื้นที่ผิวสัมผัส", "น้ำหนักของกล่องและชนิดของผิวสัมผัส"),
        ))
        return _labelled(
            stem=f"นักเรียนออกแบบการทดลองว่า{factor}มีผลต่อแรงเสียดทานหรือไม่ ควรควบคุมสิ่งใดให้เท่ากัน",
            correct=keep,
            wrongs=tuple(k for f, k in (
                ("ชนิดของผิวสัมผัส", "น้ำหนักของกล่องและพื้นที่ผิวสัมผัส"),
                ("น้ำหนักของกล่อง", "ชนิดของผิวสัมผัสและพื้นที่ผิวสัมผัส"),
                ("พื้นที่ผิวสัมผัส", "น้ำหนักของกล่องและชนิดของผิวสัมผัส"),
            ) if f != factor) + ("ไม่ต้องควบคุมสิ่งใด",),
            hint="เปลี่ยนเฉพาะสิ่งที่ต้องการศึกษา ส่วนปัจจัยอื่นต้องเท่ากัน",
            topic=FRICTION_FACTOR_TOPIC,
        )


@question_type(
    "phys.friction_factor_fluency",
    display_name={"th": "อธิบายปัจจัยที่มีผลต่อขนาดของแรงเสียดทานจากผลการทดลอง"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=FRICTION_FACTOR_TOPIC,
)
class FrictionFactorFluency(QuestionType):
    """Three one-factor experiments; weight, surface and area explained together."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        light = rng.choice((5, 10, 15))
        heavy = light + rng.choice((5, 10, 15))
        rough, smooth = rng.choice(SURFACE_PAIRS)
        f_light = rng.randint(2, 4)
        f_heavy = f_light + rng.randint(2, 5)
        f_rough, f_smooth = rng.randint(6, 10), rng.randint(2, 5)
        same = rng.randint(3, 7)
        record = (f"การทดลองที่ 1 (พื้นเดียวกัน): กล่องหนัก {light} นิวตัน ลากได้ด้วยแรง {f_light} นิวตัน "
                  f"กล่องหนัก {heavy} นิวตัน ลากได้ด้วยแรง {f_heavy} นิวตัน / "
                  f"การทดลองที่ 2 (กล่องเดียวกัน): บน{rough}ใช้แรง {f_rough} นิวตัน บน{smooth}ใช้แรง {f_smooth} นิวตัน / "
                  f"การทดลองที่ 3 (กล่องและพื้นเดียวกัน): วางด้านกว้างและด้านแคบใช้แรง {same} นิวตันเท่ากัน")
        return parts_item(
            rng, factor_parts(light, heavy, rough, smooth),
            stem=(f"นักเรียนลากกล่องด้วยความเร็วคงที่ โดยเปลี่ยนเพียงปัจจัยเดียวในแต่ละการทดลอง ได้ผลดังนี้ — {record} "
                  "จากผลการทดลอง ข้อใดอธิบายปัจจัยที่มีผลต่อขนาดของแรงเสียดทานได้ถูกต้องทั้งหมด"),
            hint="ลากด้วยความเร็วคงที่ แรงลากเท่ากับแรงเสียดทาน อ่านทีละการทดลอง ข้อที่ผิดจะผิดอย่างน้อยหนึ่งปัจจัย",
            topic=FRICTION_FACTOR_TOPIC,
        )


@question_type(
    "phys.friction_factor_application",
    display_name={"th": "ใช้ปัจจัยของแรงเสียดทานอธิบายและโต้แย้ง"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=FRICTION_FACTOR_TOPIC,
)
class FrictionFactorApplication(QuestionType):
    """Authored cases, and which factor an everyday change works through."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.35:
            thing = rng.choice(("กล่อง", "รองเท้า", "ก้อนไม้", "ลังพลาสติก"))
            if rng.random() < 0.5:
                w1, w2 = sorted(rng.sample(range(10, 61, 10), 2))
                f1 = rng.randint(2, 6)
                f2 = f1 + rng.randint(2, 8)
                stem = (f"นักเรียนลาก{thing}บนพื้นเดียวกันด้วยความเร็วคงที่ เมื่อหนัก {w1} นิวตันใช้แรง {f1} นิวตัน "
                        f"เมื่อเพิ่มของจนหนัก {w2} นิวตันใช้แรง {f2} นิวตัน ข้อสรุปใดถูกต้อง")
                answer = "น้ำหนักที่กดลงมากขึ้นทำให้แรงเสียดทานมากขึ้น"
                wrongs = ("น้ำหนักที่กดลงมากขึ้นทำให้แรงเสียดทานน้อยลง", "พื้นที่ผิวสัมผัสมากขึ้นจึงลากยากขึ้น",
                          "แรงเสียดทานไม่ขึ้นกับน้ำหนัก ความต่างเกิดจากการวัดคลาดเคลื่อน")
            else:
                rough, smooth = rng.choice(SURFACE_PAIRS)
                f_smooth = rng.randint(2, 6)
                f_rough = f_smooth + rng.randint(2, 8)
                first, second = rng.sample(((rough, f_rough), (smooth, f_smooth)), 2)
                stem = (f"นักเรียนลาก{thing}ชิ้นเดียวกันด้วยความเร็วคงที่ บน{first[0]}ใช้แรง {first[1]} นิวตัน "
                        f"บน{second[0]}ใช้แรง {second[1]} นิวตัน ข้อสรุปใดถูกต้อง")
                answer = f"ผิวที่ขรุขระกว่าอย่าง{rough}ทำให้แรงเสียดทานมากกว่า"
                wrongs = (f"ผิวที่เรียบกว่าอย่าง{smooth}ทำให้แรงเสียดทานมากกว่า", "ชนิดของผิวสัมผัสไม่มีผลต่อแรงเสียดทาน",
                          f"{thing}หนักขึ้นเมื่ออยู่บน{rough}")
            return _labelled(stem=stem, correct=answer, wrongs=wrongs,
                             hint="ลากด้วยความเร็วคงที่ แรงลากเท่ากับแรงเสียดทาน เทียบว่าเปลี่ยนปัจจัยใดแล้วแรงเปลี่ยนอย่างไร",
                             topic=FRICTION_FACTOR_TOPIC)
        if roll < 0.7:
            change, factor = rng.choice(FACTOR_CHANGES)
            factors = ("น้ำหนักที่กดลงบนผิวสัมผัส", "ชนิดหรือความขรุขระของผิวสัมผัส", "พื้นที่ผิวสัมผัส", "สีของวัตถุ")
            return _labelled(
                stem=f"\"{change}\" เปลี่ยนแรงเสียดทานโดยอาศัยปัจจัยใด",
                correct=factor, wrongs=tuple(f for f in factors if f != factor),
                hint="แรงเสียดทานขึ้นกับน้ำหนักที่กดลงและชนิดของผิวสัมผัส",
                topic=FRICTION_FACTOR_TOPIC,
            )
        return _retopic(scenario_question(
            rng, FRICTION_FACTOR_SCENARIOS,
            hint="แรงเสียดทานขึ้นกับน้ำหนักที่กดลงและชนิดของผิวสัมผัส ไม่ขึ้นกับพื้นที่ผิวสัมผัส",
        ), FRICTION_FACTOR_TOPIC)
