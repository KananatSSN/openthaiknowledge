"""การสืบพันธุ์ของสัตว์

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.6/12

Sets moved here from: science_wave_f68.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f68 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_REPRO = "การสืบพันธุ์ของสัตว์"


# Each kind is shown by a described event, not an animal's name: many animals use several kinds.
ASEXUAL = (
    ("การแตกหน่อ", ("ไฮดรามีหน่อเจริญออกจากลำตัว แล้วหลุดออกไปเป็นตัวใหม่", "ฟองน้ำมีกลุ่มเซลล์งอกออกเป็นหน่อ แล้วเจริญเป็นตัวใหม่")),
    ("การงอกใหม่", ("พลานาเรียถูกตัดเป็นสองท่อน แต่ละท่อนเจริญเป็นตัวใหม่ที่สมบูรณ์", "แขนดาวทะเลที่ขาดพร้อมส่วนกลางลำตัวเจริญเป็นตัวใหม่")),
    ("พาร์ทีโนเจเนซิส", ("ไข่ของผึ้งที่ไม่ได้รับการผสมเจริญเป็นผึ้งตัวผู้", "เพลี้ยอ่อนเพศเมียออกลูกได้โดยไม่ต้องผสมกับเพศผู้")),
)


SEXUAL = (
    ("การปฏิสนธิภายนอก", ("ปลาเพศเมียวางไข่ในน้ำ แล้วปลาเพศผู้ปล่อยอสุจิมาผสม", "กบเพศผู้เกาะหลังกบเพศเมีย ปล่อยอสุจิผสมกับไข่ในน้ำ")),
    ("การปฏิสนธิภายใน", ("ไก่ผสมพันธุ์ อสุจิผสมกับไข่ภายในท่อนำไข่ก่อนสร้างเปลือก", "สุนัขผสมพันธุ์ ไข่ได้รับการผสมภายในร่างกายของแม่")),
    ("กะเทยที่ผสมข้ามตัว", ("ไส้เดือนดินสองตัวแลกเปลี่ยนอสุจิกัน แม้แต่ละตัวมีอวัยวะทั้งสองเพศ", "ปลิงน้ำจืดมีอวัยวะทั้งสองเพศ แต่ผสมพันธุ์กับตัวอื่น")),
)


REPRO_HINT = ("การสืบพันธุ์แบบไม่อาศัยเพศ: แตกหน่อ งอกใหม่ แบ่งตัว พาร์ทีโนเจเนซิส ลูกเหมือนพ่อแม่ทุกประการ "
              "แบบอาศัยเพศมีการรวมเซลล์สืบพันธุ์ ลูกมีความแปรผัน สัตว์น้ำมักปฏิสนธิภายนอก สัตว์บกปฏิสนธิภายใน")


REPRO_FACTS = (
    ("การสืบพันธุ์แบบไม่อาศัยเพศมีข้อดีอย่างไร", "เพิ่มจำนวนได้เร็วโดยไม่ต้องหาคู่ และลูกมีลักษณะเหมือนพ่อแม่",
     ("ลูกมีความแปรผันทางพันธุกรรมสูง และต้องหาคู่ก่อนสืบพันธุ์ทุกครั้ง", "ต้องใช้ทั้งเพศผู้และเพศเมีย จึงเพิ่มจำนวนได้ช้ากว่า", "ทำให้เกิดสปีชีส์ใหม่ทุกรุ่น", "ต้องมีการปฏิสนธิภายใน")),
    ("การสืบพันธุ์แบบอาศัยเพศมีข้อดีอย่างไร", "ลูกมีความแปรผันทางพันธุกรรม จึงมีโอกาสอยู่รอดเมื่อสิ่งแวดล้อมเปลี่ยน",
     ("ลูกเหมือนพ่อแม่ทุกประการ", "ไม่ต้องสร้างเซลล์สืบพันธุ์", "เพิ่มจำนวนได้เร็วที่สุดโดยไม่ต้องหาคู่ผสมพันธุ์", "ไม่ต้องใช้พลังงาน")),
    ("สัตว์ที่ปฏิสนธิภายนอกมักปล่อยไข่ครั้งละจำนวนมากเพราะเหตุใด", "ไข่และตัวอ่อนจำนวนมากถูกกินหรือไม่ได้รับการผสม",
     ("ไข่ทุกฟองได้รับการผสมเสมอ", "ตัวอ่อนทุกตัวรอดชีวิต", "ไข่มีเปลือกแข็งป้องกันอย่างดี", "พ่อแม่เลี้ยงดูลูกทุกตัว")),
    ("การดูแลลูกของสัตว์ที่ปฏิสนธิภายในมักเป็นอย่างไรเมื่อเทียบกับสัตว์ที่ปฏิสนธิภายนอก", "มีลูกน้อยกว่าแต่ลูกมีโอกาสรอดสูงกว่า",
     ("มีลูกมากกว่าและไม่ดูแลลูกเลย", "ลูกไม่มีโอกาสรอด", "ไม่มีความแตกต่าง", "ลูกเหมือนพ่อแม่ทุกประการ")),
    ("ไข่ของสัตว์เลื้อยคลานและนกมีเปลือกและถุงน้ำคร่ำมีประโยชน์อย่างไร", "ป้องกันเอ็มบริโอจากการสูญเสียน้ำ ทำให้วางไข่บนบกได้",
     ("ทำให้ไข่ลอยน้ำได้", "ทำให้ไม่ต้องมีการปฏิสนธิ ไข่จึงเจริญเป็นตัวได้เองบนบก", "ทำให้ไข่ฟักเร็วขึ้นเป็นสองเท่าเมื่อวางไข่ในน้ำ", "ทำให้เอ็มบริโอสังเคราะห์ด้วยแสงได้")),
    ("ลูกที่เกิดจากการแตกหน่อของไฮดรามีลักษณะทางพันธุกรรมอย่างไร", "เหมือนตัวแม่ทุกประการ",
     ("แตกต่างจากตัวแม่มาก", "ได้ลักษณะครึ่งหนึ่งจากตัวผู้", "เป็นหมันทุกตัว", "มีโครโมโซมเป็นสองเท่าของตัวแม่")),
    ("ไส้เดือนดินเป็นกะเทย แต่เหตุใดจึงยังต้องผสมพันธุ์กับตัวอื่น", "อวัยวะเพศผู้และเพศเมียเจริญไม่พร้อมกัน จึงผสมข้ามตัว",
     ("ไส้เดือนดินไม่มีอวัยวะเพศเมีย", "ไข่ไม่ต้องได้รับการผสม", "ไส้เดือนดินสืบพันธุ์ด้วยการแตกหน่อจึงไม่ต้องผสมพันธุ์", "สเปิร์มของตัวเองมีพิษต่อไข่ของตัวเอง จึงผสมข้ามตัว")),
)


@question_type(
    "biology.animal_reproduction_foundation",
    display_name={"th": "รูปแบบการสืบพันธุ์แบบไม่อาศัยเพศและแบบอาศัยเพศ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_REPRO,
)
class AnimalReproductionFoundation(QuestionType):
    """Name the way each animal reproduces."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        pool = ASEXUAL + SEXUAL
        kind, scenes = rng.choice(pool)
        scene = rng.choice(scenes)
        others = [p for p in pool if p[0] != kind]
        if rng.random() < 0.5:
            return _labelled(stem=f"\"{scene}\" เป็นการสืบพันธุ์แบบใด", correct=kind, wrongs=tuple(o[0] for o in rng.sample(others, 3)),
                             topic=TOPIC_REPRO, hint=REPRO_HINT)
        return _labelled(stem=f"ข้อใดเป็นตัวอย่างของ{kind}", correct=scene,
                         wrongs=tuple(rng.choice(o[1]) for o in rng.sample(others, 3)), topic=TOPIC_REPRO, hint=REPRO_HINT)


@question_type(
    "biology.animal_reproduction_fluency",
    display_name={"th": "ข้อดีข้อจำกัดของการสืบพันธุ์แต่ละแบบ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_REPRO,
)
class AnimalReproductionFluency(QuestionType):
    """Why each way pays."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(REPRO_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_REPRO, hint=REPRO_HINT)


@question_type(
    "biology.animal_reproduction_application",
    display_name={"th": "จำนวนโครโมโซมในผึ้งและการเพิ่มจำนวนแบบไม่อาศัยเพศ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_REPRO,
)
class AnimalReproductionApplication(QuestionType):
    """Drones from unfertilised eggs are n; budding doubles a clone each round."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            diploid = 32
            who = rng.choice((("ผึ้งตัวผู้ ซึ่งเจริญจากไข่ที่ไม่ได้รับการผสม", 16), ("ผึ้งงาน ซึ่งเจริญจากไข่ที่ได้รับการผสม", 32),
                              ("ผึ้งนางพญา", 32), ("สเปิร์มของผึ้งตัวผู้", 16)))
            return numeric(stem=f"ผึ้งนางพญามีโครโมโซม 2n = {diploid} {who[0]}มีโครโมโซมกี่แท่ง", answer=who[1],
                           wrongs=[diploid if who[1] == 16 else 16, 8, 64], unit="แท่ง", topic=TOPIC_REPRO,
                           hint="ผึ้งตัวผู้เกิดจากไข่ที่ไม่ได้ผสม (พาร์ทีโนเจเนซิส) จึงมีโครโมโซม n ผึ้งเพศเมียมี 2n "
                                "ผึ้งตัวผู้สร้างสเปิร์มด้วยไมโทซิสจึงมี n เท่ากับตัวมันเอง")
        start = rng.randint(1, 10)
        rounds = rng.randint(2, 6)
        return numeric(stem=f"ไฮดรา {start} ตัว แตกหน่อจนแต่ละตัวได้ตัวใหม่ 1 ตัวในทุกสัปดาห์ และไม่มีตัวใดตาย ผ่านไป {rounds} สัปดาห์จะมีไฮดรากี่ตัว",
                       answer=start * 2 ** rounds, wrongs=[start * 2 * rounds, start + rounds, start * 2 ** (rounds - 1)], unit="ตัว",
                       topic=TOPIC_REPRO, hint="ทุกสัปดาห์จำนวนเพิ่มเป็น 2 เท่า จำนวน = เริ่มต้น × 2 ยกกำลังจำนวนสัปดาห์")
