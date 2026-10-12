"""การสื่อสารระหว่างสัตว์

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.6/19

Sets moved here from: science_wave_f70.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f70 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_COMM = "การสื่อสารระหว่างสัตว์"


SIGNALS = {
    "เสียง": ("นกร้องประกาศอาณาเขต", "กบตัวผู้ส่งเสียงร้องเรียกตัวเมียในฤดูผสมพันธุ์", "จิ้งหรีดสีปีกให้เกิดเสียง"),
    "ท่าทางหรือการมองเห็น": ("หิ่งห้อยกะพริบแสงเป็นจังหวะเพื่อหาคู่", "นกยูงตัวผู้รำแพนหางอวดตัวเมีย", "สุนัขแยกเขี้ยวขู่"),
    "สารเคมี": ("มดปล่อยฟีโรโมนเป็นทางนำสมาชิกไปยังอาหาร", "ผีเสื้อกลางคืนตัวเมียปล่อยสารดึงดูดตัวผู้จากที่ไกล", "สุนัขปัสสาวะทำเครื่องหมายอาณาเขต"),
    "การสัมผัส": ("ลิงไซ้ขนให้กันเพื่อกระชับความสัมพันธ์", "ผึ้งงานใช้หนวดสัมผัสกันในรังที่มืด"),
}


COMM_HINT = ("สัตว์สื่อสารด้วยเสียง ท่าทางหรือแสง สารเคมี (ฟีโรโมน) และการสัมผัส ผึ้งเต้นรำแบบวงกลมเมื่ออาหารอยู่ใกล้ "
             "และแบบส่ายท้องเมื่ออาหารอยู่ไกล มุมของการส่ายท้องจากแนวดิ่งเท่ากับมุมของอาหารจากทิศดวงอาทิตย์")


@question_type(
    "biology.animal_communication_foundation",
    display_name={"th": "รูปแบบการสื่อสารระหว่างสัตว์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_COMM,
)
class AnimalCommunicationFoundation(QuestionType):
    """Sound, sight, chemicals or touch."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.choice(sorted(SIGNALS))
        example = rng.choice(SIGNALS[kind])
        others = [k for k in SIGNALS if k != kind]
        if rng.random() < 0.55:
            return _labelled(stem=f"\"{example}\" เป็นการสื่อสารด้วยสิ่งใด", correct=kind, wrongs=tuple(others), topic=TOPIC_COMM, hint=COMM_HINT)
        pool = [e for k in others for e in SIGNALS[k]]
        return _labelled(stem=f"ข้อใดเป็นการสื่อสารด้วย{kind}", correct=example, wrongs=tuple(pool), topic=TOPIC_COMM, hint=COMM_HINT)


@question_type(
    "biology.animal_communication_fluency",
    display_name={"th": "การเต้นรำของผึ้งและฟีโรโมน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_COMM,
)
class AnimalCommunicationFluency(QuestionType):
    """Round against waggle dances, and what pheromones do."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        facts = (
            ("ผึ้งงานเต้นรำแบบวงกลมเพื่อบอกอะไร", "มีแหล่งอาหารอยู่ใกล้รัง", ("มีแหล่งอาหารอยู่ไกลมาก", "มีศัตรูอยู่ใกล้รัง", "นางพญาตายแล้ว", "ถึงเวลาแยกรัง")),
            ("ผึ้งงานเต้นรำแบบส่ายท้องเพื่อบอกอะไร", "ทิศทางและระยะทางของแหล่งอาหารที่อยู่ไกล",
             ("มีแหล่งอาหารอยู่ติดรังภายในระยะไม่กี่เมตร", "ชนิดและสีของดอกไม้ที่เป็นแหล่งอาหารเท่านั้น", "จำนวนผึ้งในรัง", "อุณหภูมิของรัง")),
            ("ในการเต้นรำแบบส่ายท้อง ระยะเวลาการส่ายท้องที่นานขึ้นบอกอะไร", "แหล่งอาหารอยู่ไกลขึ้น",
             ("แหล่งอาหารอยู่ใกล้ขึ้น", "อาหารมีรสหวานน้อยลง", "มีศัตรูมากขึ้น", "ดวงอาทิตย์ตกแล้ว")),
            ("ฟีโรโมนคืออะไร", "สารเคมีที่สัตว์ปล่อยออกมาเพื่อสื่อสารกับสัตว์ชนิดเดียวกัน",
             ("ฮอร์โมนที่ออกฤทธิ์เฉพาะภายในร่างกายตนเอง", "เสียงความถี่สูงที่สัตว์ชนิดเดียวกันได้ยินแต่มนุษย์ไม่ได้ยิน", "แสงที่หิ่งห้อยปล่อยออกมา", "เอนไซม์ย่อยอาหาร")),
            ("หิ่งห้อยแต่ละชนิดกะพริบแสงด้วยจังหวะต่างกันเพื่ออะไร", "ให้จำคู่ที่เป็นชนิดเดียวกันได้",
             ("ล่อเหยื่อทุกชนิด", "ให้แสงสว่างในการหาอาหารยามกลางคืน", "ขับไล่ผู้ล่าเท่านั้น", "ควบคุมอุณหภูมิร่างกาย")),
            ("การใช้กับดักฟีโรโมนเพศในสวนผลไม้มีประโยชน์อย่างไร", "ล่อแมลงศัตรูพืชเพศผู้มาติดกับดัก ลดการผสมพันธุ์โดยไม่ต้องใช้สารฆ่าแมลงมาก",
             ("ทำให้ผลไม้หวานขึ้น เพราะฟีโรโมนซึมเข้าผลไม้และเปลี่ยนเป็นน้ำตาล", "ล่อแมลงทุกชนิดในสวนทั้งเพศผู้และเพศเมียให้มาติดกับดัก จึงไม่ต้องใช้สารฆ่าแมลงเลย", "เพิ่มจำนวนผึ้ง", "ช่วยผสมเกสร")),
            ("การสื่อสารด้วยสารเคมีมีข้อดีอย่างไร", "อยู่ได้นานและใช้ได้ในที่มืดหรือระยะไกล",
             ("ส่งข้อมูลได้เร็วที่สุดเสมอเมื่อเทียบกับเสียง", "ใช้ได้เฉพาะในที่สว่าง", "สัตว์ทุกชนิดรับรู้ได้เหมือนกัน", "ไม่ต้องมีหน่วยรับความรู้สึก")),
        )
        stem, right, wrongs = rng.choice(facts)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_COMM, hint=COMM_HINT)


@question_type(
    "biology.animal_communication_application",
    display_name={"th": "แปลความหมายการเต้นรำแบบส่ายท้องของผึ้ง"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_COMM,
)
class AnimalCommunicationApplication(QuestionType):
    """Angle from vertical is angle from the sun; waggle time grows with distance."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.55:
            angle = rng.choice((0, 30, 45, 60, 90, 120, 180))
            side = rng.choice(("ขวา", "ซ้าย"))
            if angle in (0, 180):
                run = "ขึ้นตรงตามแนวดิ่ง" if angle == 0 else "ลงตรงตามแนวดิ่ง"
                right = "ไปทางเดียวกับดวงอาทิตย์" if angle == 0 else "ไปทางตรงข้ามกับดวงอาทิตย์"
            else:
                run = f"เอียงไปทาง{side}ของแนวดิ่งขึ้น {angle} องศา"
                right = f"เบนไปทาง{side}ของทิศดวงอาทิตย์ {angle} องศา"
            options = {"ไปทางเดียวกับดวงอาทิตย์", "ไปทางตรงข้ามกับดวงอาทิตย์"} | {
                f"เบนไปทาง{s}ของทิศดวงอาทิตย์ {a} องศา" for s in ("ขวา", "ซ้าย") for a in (30, 45, 60, 90, 120)}
            pool = sorted(options - {right})
            near = [o for o in pool if (str(angle) in o) or ("ดวงอาทิตย์" in o and angle in (0, 180))]
            wrongs = list(dict.fromkeys(near + rng.sample(pool, 3)))[:3]
            return _labelled(stem=f"ผึ้งงานเต้นรำแบบส่ายท้องบนรวงผึ้งในแนวตั้ง โดยช่วงส่ายท้อง{run} แหล่งอาหารอยู่ทางใด", correct=right,
                             wrongs=tuple(wrongs), topic=TOPIC_COMM, hint=COMM_HINT)
        per = rng.choice((Fraction(1, 2), Fraction(3, 4), 1))
        seconds = rng.choice((1, 2, 3, 4, 5, 6))
        distance = per * seconds
        return numeric(stem=f"ถ้าการส่ายท้อง 1 วินาทีแทนระยะทางประมาณ {show(per * 1000)} เมตร ผึ้งส่ายท้องนาน {seconds} วินาที แหล่งอาหารอยู่ห่างประมาณกี่กิโลเมตร",
                       answer=distance, wrongs=[distance * 1000, per, distance * 2], unit="km", topic=TOPIC_COMM,
                       hint="ระยะทาง = เวลาที่ส่ายท้อง × ระยะทางต่อวินาที แล้วแปลงเมตรเป็นกิโลเมตร")
