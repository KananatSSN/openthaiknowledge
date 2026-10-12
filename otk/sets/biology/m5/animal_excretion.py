"""การกำจัดของเสียของสัตว์

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.5/18

Sets moved here from: science_wave_f64.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f64 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_EXCRETE = "การกำจัดของเสียของสัตว์"


EXCRETORS = (
    ("ฟองน้ำ", "เซลล์ทุกเซลล์แพร่ของเสียออกสู่น้ำที่ไหลผ่านโดยตรง"),
    ("ไฮดรา", "เซลล์แพร่ของเสียออกสู่น้ำผ่านผิวลำตัวโดยตรง"),
    ("พลานาเรีย", "เฟลมเซลล์ (โพรโทเนฟริเดีย) ที่มีซิเลียพัดของเหลวออกทางรูขับถ่าย"),
    ("ไส้เดือนดิน", "เนฟริเดียปล้องละ 1 คู่"),
    ("แมลง", "ท่อมัลพิเกียนที่ส่งของเสียเข้าสู่ลำไส้"),
    ("สัตว์มีกระดูกสันหลัง", "ไต"),
)


WASTES = {
    "แอมโมเนีย": ("ปลากระดูกแข็ง", "ลูกอ๊อด", "สัตว์ไม่มีกระดูกสันหลังในน้ำ"),
    "ยูเรีย": ("คน", "สัตว์เลี้ยงลูกด้วยน้ำนม", "กบตัวเต็มวัย", "ฉลาม"),
    "กรดยูริก": ("นก", "สัตว์เลื้อยคลาน", "แมลง"),
}


WASTE_FACTS = {
    "แอมโมเนีย": "เป็นพิษมากและละลายน้ำได้ดี ต้องใช้น้ำปริมาณมากในการขับออก",
    "ยูเรีย": "เป็นพิษน้อยกว่าแอมโมเนีย สร้างที่ตับ และขับออกพร้อมน้ำปริมาณปานกลาง",
    "กรดยูริก": "แทบไม่ละลายน้ำ ขับออกเป็นของกึ่งแข็ง ช่วยประหยัดน้ำได้มาก",
}


EXCRETE_HINT = ("ฟองน้ำและไฮดราแพร่ของเสียออกทางผิว พลานาเรียใช้เฟลมเซลล์ ไส้เดือนใช้เนฟริเดีย แมลงใช้ท่อมัลพิเกียน "
                "สัตว์ในน้ำขับแอมโมเนีย สัตว์เลี้ยงลูกด้วยน้ำนมขับยูเรีย นก สัตว์เลื้อยคลาน และแมลงขับกรดยูริก")


EXCRETE_CASES = (
    ("เหตุใดนกจึงขับของเสียในรูปกรดยูริก", "ประหยัดน้ำและทำให้ตัวเบาเหมาะกับการบิน และเก็บในไข่ที่มีเปลือกได้โดยไม่เป็นพิษ",
     ("นกดื่มน้ำมากจึงต้องขับน้ำออกในรูปกรดยูริกที่ละลายน้ำได้ดีที่สุด", "นกไม่มีไต จึงต้องขับของเสียไนโตรเจนออกทางลำไส้", "กรดยูริกเป็นพิษมากกว่าแอมโมเนีย นกจึงต้องขับออกทันทีพร้อมน้ำปริมาณมากเสมอ", "นกขับของเสียทางปอด")),
    ("เหตุใดปลากระดูกแข็งจึงขับแอมโมเนียได้โดยไม่เป็นอันตราย", "อยู่ในน้ำ แอมโมเนียจึงเจือจางและแพร่ออกทางเหงือกได้รวดเร็ว",
     ("ปลาเปลี่ยนแอมโมเนียเป็นกรดยูริกทันทีก่อนขับออกทางไต", "แอมโมเนียไม่เป็นพิษต่อปลา", "ปลาเก็บแอมโมเนียไว้ในกระเพาะว่ายน้ำแล้วขับออกทีละน้อย", "ปลาไม่สร้างของเสียไนโตรเจน")),
    ("ลูกอ๊อดขับแอมโมเนีย แต่กบตัวเต็มวัยขับยูเรีย เพราะเหตุใด", "กบตัวเต็มวัยอาศัยบนบกได้ จึงต้องประหยัดน้ำมากกว่า",
     ("กบตัวเต็มวัยดื่มน้ำมากกว่าลูกอ๊อดที่อยู่ในน้ำ", "ลูกอ๊อดไม่มีตับ", "ยูเรียเป็นพิษมากกว่าแอมโมเนีย", "กบตัวเต็มวัยไม่มีไต จึงต้องเก็บของเสียไว้")),
    ("สัตว์ชนิดหนึ่งอาศัยในทะเลทรายที่ขาดแคลนน้ำ ควรขับของเสียไนโตรเจนในรูปใดจึงเหมาะสมที่สุด", "กรดยูริก เพราะใช้น้ำในการขับออกน้อยที่สุด",
     ("แอมโมเนีย เพราะสร้างง่ายที่สุด", "ยูเรีย เพราะไม่ต้องใช้น้ำเลยในการขับ", "แอมโมเนีย เพราะไม่เป็นพิษต่อเซลล์", "ไม่ต้องขับของเสียไนโตรเจน เพราะเก็บไว้ในไข่")),
    ("เหตุใดสัตว์เลี้ยงลูกด้วยน้ำนมจึงเปลี่ยนแอมโมเนียเป็นยูเรียที่ตับก่อนขับออก", "ยูเรียเป็นพิษน้อยกว่า จึงเก็บในร่างกายได้ระยะหนึ่งและใช้น้ำขับน้อย",
     ("ยูเรียเป็นพิษมากกว่าแอมโมเนีย", "ยูเรียไม่ละลายน้ำ จึงเก็บไว้ในร่างกายได้นานโดยไม่ต้องใช้น้ำขับ", "ตับไม่สามารถกำจัดแอมโมเนียได้เลย จึงต้องเปลี่ยนเป็นยูเรียที่เป็นพิษมากกว่า", "ยูเรียใช้เป็นอาหารของเซลล์")),
    ("เนฟริเดียของไส้เดือนดินมีลักษณะอย่างไร", "เป็นท่อขดที่มีปลายเปิดรับของเหลวจากช่องลำตัวและเปิดออกนอกลำตัว ปล้องละ 1 คู่",
     ("เป็นเซลล์ที่มีซิเลียเหมือนเปลวไฟ กระจายอยู่ทั่วลำตัวแบนโดยไม่มีท่อเปิดออก", "เป็นท่อที่ส่งของเสียเข้าลำไส้", "เป็นไตขนาดเล็กหนึ่งคู่ทั้งตัว ที่กรองของเสียจากเลือดแล้วส่งออกทางทวารหนัก", "เป็นเหงือกที่ขับแอมโมเนีย")),
    ("เหตุใดของเสียจากท่อมัลพิเกียนของแมลงจึงถูกส่งเข้าลำไส้", "เพื่อให้ลำไส้ดูดน้ำกลับก่อนขับกรดยูริกออกพร้อมกากอาหาร",
     ("เพื่อย่อยของเสียเป็นอาหาร", "เพราะแมลงไม่มีทวารหนัก จึงต้องขับของเสียทางท่อมัลพิเกียน", "เพื่อเปลี่ยนเป็นแอมโมเนียก่อนขับออกทางผิวหนัง", "เพื่อส่งไปยังระบบท่อลมแล้วขับออกเป็นแก๊ส")),
)


@question_type(
    "biology.animal_excretion_foundation",
    display_name={"th": "โครงสร้างกำจัดของเสียของสัตว์ต่าง ๆ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_EXCRETE,
)
class AnimalExcretionFoundation(QuestionType):
    """Flame cells, nephridia, Malpighian tubules and kidneys."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        animal, organ = rng.choice(EXCRETORS)
        others = rng.sample([e for e in EXCRETORS if e[0] != animal], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"{animal}กำจัดของเสียด้วยโครงสร้างหรือวิธีใด", correct=organ, wrongs=tuple(e[1] for e in others),
                             topic=TOPIC_EXCRETE, hint=EXCRETE_HINT)
        return _labelled(stem=f"สัตว์ใดกำจัดของเสียด้วย{organ}", correct=animal, wrongs=tuple(e[0] for e in others), topic=TOPIC_EXCRETE,
                         hint=EXCRETE_HINT)


@question_type(
    "biology.animal_excretion_fluency",
    display_name={"th": "ของเสียไนโตรเจนชนิดต่าง ๆ และสัตว์ที่ขับออก"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_EXCRETE,
)
class AnimalExcretionFluency(QuestionType):
    """Ammonia in water, urea in mammals, uric acid where water is scarce."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        waste = rng.choice(sorted(WASTES))
        others = [w for w in WASTES if w != waste]
        roll = rng.random()
        if roll < 0.35:
            animal = rng.choice(WASTES[waste])
            return _labelled(stem=f"{animal}ขับของเสียไนโตรเจนส่วนใหญ่ในรูปใด", correct=waste, wrongs=(*others, "กรดอะมิโน"),
                             topic=TOPIC_EXCRETE, hint=EXCRETE_HINT)
        if roll < 0.65:
            pool = [a for w in others for a in WASTES[w]]
            return _labelled(stem=f"สัตว์ใดขับของเสียไนโตรเจนส่วนใหญ่ในรูป{waste}", correct=rng.choice(WASTES[waste]),
                             wrongs=tuple(pool), topic=TOPIC_EXCRETE, hint=EXCRETE_HINT)
        if rng.random() < 0.5:
            return _labelled(stem=f"ข้อใดเป็นลักษณะของ{waste}", correct=WASTE_FACTS[waste],
                             wrongs=(*(WASTE_FACTS[w] for w in others), "ไม่มีไนโตรเจนเป็นองค์ประกอบ"), topic=TOPIC_EXCRETE, hint=EXCRETE_HINT)
        return _labelled(stem=f"ของเสียไนโตรเจนที่ \"{WASTE_FACTS[waste]}\" คือสารใด", correct=waste, wrongs=(*others, "คาร์บอนไดออกไซด์"),
                         topic=TOPIC_EXCRETE, hint=EXCRETE_HINT)


@question_type(
    "biology.animal_excretion_application",
    display_name={"th": "อธิบายการปรับตัวในการกำจัดของเสียตามแหล่งที่อยู่"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_EXCRETE,
)
class AnimalExcretionApplication(QuestionType):
    """Why the waste suits the water supply."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(EXCRETE_CASES)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_EXCRETE, hint=EXCRETE_HINT)
