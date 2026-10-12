"""สมบัติ โครงสร้าง และการจำลอง DNA

ชีวะ · ม.4 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 2 ม.4/6

Sets moved here from: science_wave_f49.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f49 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_DNA = "สมบัติ โครงสร้าง และการจำลอง DNA"


EXPERIMENTS = (
    ("กริฟฟิท", "แบคทีเรียสายพันธุ์ S ที่ตายแล้วทำให้สายพันธุ์ R ที่มีชีวิตเปลี่ยนเป็นสายพันธุ์ S ได้"),
    ("เอเวอรีและคณะ", "เมื่อย่อย DNA ด้วยเอนไซม์ DNase แบคทีเรียสายพันธุ์ R ไม่เปลี่ยนเป็นสายพันธุ์ S จึงสรุปว่า DNA เป็นสารพันธุกรรม"),
    ("เฮอร์ชีย์และเชส", "ติดฉลากไวรัสด้วย ³²P และ ³⁵S พบว่า DNA ของไวรัสเข้าไปในแบคทีเรีย แต่โปรตีนไม่เข้าไป"),
    ("วัตสันและคริก", "เสนอแบบจำลอง DNA เป็นพอลินิวคลีโอไทด์สองสายบิดเป็นเกลียวคู่"),
    ("เมเซลสันและสตาห์ล", "ใช้ ¹⁵N และ ¹⁴N แสดงว่า DNA จำลองตัวแบบกึ่งอนุรักษ์"),
    ("ชาร์กาฟฟ์", "พบว่าใน DNA ปริมาณเบส A เท่ากับ T และ C เท่ากับ G"),
    ("แฟรงคลินและวิลคินส์", "ถ่ายภาพการเลี้ยวเบนของรังสีเอกซ์ที่แสดงว่า DNA เป็นเกลียว"),
    ("มีเชอร์", "สกัดสารที่เรียกว่านิวคลีอินได้จากนิวเคลียสของเซลล์เม็ดเลือดขาว"),
)


MATERIAL_FACTS = (
    ("สารพันธุกรรมต้องมีสมบัติข้อใด", "เพิ่มจำนวนตัวเองได้ ควบคุมลักษณะได้ และเปลี่ยนแปลงได้",
     ("สลายตัวได้ง่ายเมื่อเซลล์แบ่ง", "สร้างพลังงานให้เซลล์", "มีปริมาณเปลี่ยนไปตามอาหารที่กิน")),
    ("DNA หนึ่งนิวคลีโอไทด์ประกอบด้วยอะไร", "น้ำตาลดีออกซีไรโบส หมู่ฟอสเฟต และเบสไนโตรเจน",
     ("น้ำตาลไรโบส หมู่ฟอสเฟต และเบสไนโตรเจน", "กรดอะมิโน หมู่ฟอสเฟต และเบสไนโตรเจน", "น้ำตาลเพนโทส กลีเซอรอล และกรดไขมัน")),
    ("ในเซลล์ยูแคริโอต DNA ส่วนใหญ่อยู่ที่ใด", "นิวเคลียส", ("ไรโบโซม", "กอลจิคอมเพล็กซ์", "เยื่อหุ้มเซลล์")),
)


EXP_HINT = "กริฟฟิทพบทรานสฟอร์เมชัน เอเวอรีพบว่าเป็น DNA เฮอร์ชีย์และเชสยืนยันด้วยไวรัส เมเซลสันและสตาห์ลพบการจำลองแบบกึ่งอนุรักษ์"


ENZYMES = (
    ("เฮลิเคส", "คลายเกลียวและแยกพอลินิวคลีโอไทด์สองสายออกจากกัน"),
    ("ไพรเมส", "สร้างไพรเมอร์สั้น ๆ ให้เป็นจุดเริ่มต้นการต่อสายใหม่"),
    ("DNA พอลิเมอเรส", "ต่อนิวคลีโอไทด์ที่เข้าคู่กับสายแม่แบบให้สายใหม่ยาวขึ้น"),
    ("DNA ไลเกส", "เชื่อมชิ้นส่วนโอคาซากิให้เป็นสายเดียวกัน"),
)


REPLICATION_FACTS = (
    ("การจำลอง DNA แบบกึ่งอนุรักษ์หมายถึงข้อใด", "DNA ใหม่แต่ละโมเลกุลมีสายเดิม 1 สายและสายใหม่ 1 สาย",
     ("DNA ใหม่โมเลกุลหนึ่งเป็นสายเดิมทั้งหมด อีกโมเลกุลเป็นสายใหม่ทั้งหมด", "ทุกสายมีส่วนเก่าและส่วนใหม่ปนกันเป็นช่วง ๆ",
      "DNA เดิมถูกสลายแล้วสร้างใหม่ทั้งหมด", "DNA ใหม่ทั้งสองโมเลกุลเป็นสายใหม่ทั้งหมด")),
    ("DNA พอลิเมอเรสต่อสายใหม่ในทิศทางใด", "จากปลาย 5′ ไปยังปลาย 3′",
     ("จากปลาย 3′ ไปยังปลาย 5′", "ได้ทั้งสองทิศทางเท่ากัน", "สลับทิศทุก 10 คู่เบส")),
    ("ไพรเมอร์ที่ใช้เริ่มต้นการจำลอง DNA ในเซลล์เป็นสารใด", "RNA สายสั้น",
     ("โปรตีนสายสั้น", "DNA สายคู่ยาว", "ลิพิด", "น้ำตาลดีออกซีไรโบส")),
    ("การจำลอง DNA เกิดขึ้นในระยะใดของวัฏจักรเซลล์", "ระยะ S ของอินเตอร์เฟส",
     ("ระยะ G₁ ของอินเตอร์เฟส", "ระยะเมทาเฟส", "ระยะแอนาเฟส", "ระยะเทโลเฟส")),
    ("จุดเริ่มต้นการจำลอง DNA บนโครโมโซมของยูแคริโอตมีลักษณะอย่างไร", "มีหลายจุดบนโมเลกุล DNA เดียว",
     ("มีเพียงจุดเดียวที่ปลายโครโมโซม", "มีจุดเดียวที่เซนโทรเมียร์", "ไม่มีจุดเริ่มต้นที่แน่นอน")),
    ("สายที่สร้างเป็นช่วงสั้น ๆ (ชิ้นส่วนโอคาซากิ) เรียกว่าอะไร", "แลกกิงสแตรนด์", ("ลีดดิงสแตรนด์", "สายแม่แบบ", "ไพรเมอร์", "ออริจิน")),
    ("สายที่สร้างต่อเนื่องเป็นสายยาวสายเดียวเรียกว่าอะไร", "ลีดดิงสแตรนด์", ("แลกกิงสแตรนด์", "ชิ้นส่วนโอคาซากิ", "ไพรเมอร์", "สายแม่แบบ")),
    ("DNA สองสายในเกลียวคู่วางตัวอย่างไร", "ขนานสวนทางกัน ปลาย 5′ ของสายหนึ่งอยู่ด้านเดียวกับปลาย 3′ ของอีกสาย",
     ("ขนานไปทางเดียวกัน", "ตั้งฉากกัน", "ไม่มีทิศทางที่แน่นอน", "ปลาย 5′ ของทั้งสองสายอยู่ด้านเดียวกัน")),
    ("พันธะใดยึดเบสคู่สมระหว่าง DNA สองสาย", "พันธะไฮโดรเจน", ("พันธะฟอสโฟไดเอสเทอร์", "พันธะเพปไทด์", "พันธะไกลโคซิดิก", "พันธะไอออนิก")),
    ("พันธะใดเชื่อมนิวคลีโอไทด์ที่อยู่ติดกันในสายเดียวกัน", "พันธะฟอสโฟไดเอสเทอร์", ("พันธะไฮโดรเจน", "พันธะเพปไทด์", "พันธะไอออนิก", "พันธะไดซัลไฟด์")),
)


REP_HINT = "เฮลิเคสแยกสาย ไพรเมสสร้างไพรเมอร์ DNA พอลิเมอเรสต่อสาย 5′→3′ ไลเกสเชื่อมชิ้นส่วนโอคาซากิ ผลคือ DNA ใหม่มีสายเดิม 1 สาย"


@question_type(
    "biology.dna_replication_foundation",
    display_name={"th": "สมบัติของสารพันธุกรรมและการทดลองที่ค้นพบ DNA"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_DNA,
)
class DnaReplicationFoundation(QuestionType):
    """Who showed what, and what genetic material must be able to do."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.25:
            stem, right, wrongs = rng.choice(MATERIAL_FACTS)
            return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_DNA, hint=EXP_HINT)
        who, what = rng.choice(EXPERIMENTS)
        others = [e for e in EXPERIMENTS if e[0] != who]
        picked = rng.sample(others, 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"ผลงานของ{who}ที่เกี่ยวกับสารพันธุกรรมคือข้อใด", correct=what,
                             wrongs=tuple(e[1] for e in picked), topic=TOPIC_DNA, hint=EXP_HINT)
        return _labelled(stem=f"\"{what}\" เป็นผลงานของใคร", correct=who, wrongs=tuple(e[0] for e in picked), topic=TOPIC_DNA,
                         hint=EXP_HINT)


@question_type(
    "biology.dna_replication_fluency",
    display_name={"th": "โครงสร้าง DNA และขั้นตอนการจำลอง DNA"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_DNA,
)
class DnaReplicationFluency(QuestionType):
    """The enzymes of the replication fork, and the facts of the double helix."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            name, role = rng.choice(ENZYMES)
            others = [e for e in ENZYMES if e[0] != name]
            if rng.random() < 0.5:
                roles = [e[1] for e in others] + ["ถอดรหัสจาก DNA เป็น mRNA", "ตัด DNA ตรงลำดับเบสที่จำเพาะ"]
                return _labelled(stem=f"ในการจำลอง DNA เอนไซม์ {name} ทำหน้าที่ใด", correct=role, wrongs=tuple(roles),
                                 topic=TOPIC_DNA, hint=REP_HINT)
            names = [e[0] for e in others] + ["เอนไซม์ตัดจำเพาะ", "โปรตีเอส"]
            return _labelled(stem=f"ในการจำลอง DNA เอนไซม์ใดทำหน้าที่{role}", correct=name,
                             wrongs=tuple(names), topic=TOPIC_DNA, hint=REP_HINT)
        stem, right, wrongs = rng.choice(REPLICATION_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_DNA, hint=REP_HINT)


@question_type(
    "biology.dna_replication_application",
    display_name={"th": "คำนวณจากการทดลองของเมเซลสันและสตาห์ลและขนาดเกลียว DNA"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_DNA,
)
class DnaReplicationApplication(QuestionType):
    """Semiconservative counts, and 10 base pairs per 3.4 nm turn."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.55:
            start = rng.choice((1, 2, 3, 4, 5, 8, 10, 20))
            rounds = rng.randint(1, 5)
            total = start * 2 ** rounds
            intro = (f"นำแบคทีเรียที่มี DNA ซึ่งมีแต่ ¹⁵N จำนวน {start} โมเลกุลไปเลี้ยงในอาหารที่มีแต่ ¹⁴N "
                     f"ให้ DNA จำลองตัว {rounds} รอบ")
            hint = "DNA จำลองตัวแบบกึ่งอนุรักษ์ สาย ¹⁵N เดิม 2 สายต่อโมเลกุลไม่หายไป จึงมีโมเลกุลลูกผสม ¹⁵N/¹⁴N เท่ากับ 2 เท่าของจำนวนเริ่มต้นเสมอ"
            asks = [("มี DNA ทั้งหมดกี่โมเลกุล", total, [start * 2 * rounds, total * 2, total // 2 or 3], "โมเลกุล"),
                    ("มี DNA ลูกผสม ¹⁵N/¹⁴N กี่โมเลกุล", 2 * start, [start, total, total - 2 * start or 4 * start], "โมเลกุล"),
                    ("โมเลกุลลูกผสม ¹⁵N/¹⁴N คิดเป็นร้อยละเท่าใดของ DNA ทั้งหมด", Fraction(200, 2 ** rounds),
                     [Fraction(100, 2 ** rounds), 100 - Fraction(200, 2 ** rounds) or 50, 50], "%")]
            if rounds >= 2:
                asks.append(("มี DNA ที่มีแต่ ¹⁴N กี่โมเลกุล", total - 2 * start, [total, total - start, 2 * start], "โมเลกุล"))
            ask, answer, wrongs, unit = rng.choice(asks)
            return numeric(stem=f"{intro} {ask}", answer=answer, wrongs=wrongs, unit=unit, topic=TOPIC_DNA, hint=hint)
        hint = "เกลียว DNA หนึ่งรอบมี 10 คู่เบส ยาว 3.4 nm แต่ละคู่เบสห่างกัน 0.34 nm"
        pairs = rng.randrange(60, 5001, 10)
        kind = rng.randrange(4)
        if kind == 0:
            return numeric(stem=f"DNA สายคู่ยาว {pairs} คู่เบส มีความยาวกี่ nm", answer=pairs * Fraction(34, 100),
                           wrongs=[pairs * Fraction(34, 10), pairs * Fraction(34, 100) * 2, pairs / 10], unit="nm", topic=TOPIC_DNA,
                           hint=hint)
        if kind == 1:
            return numeric(stem=f"DNA สายคู่ยาว {pairs} คู่เบส บิดเกลียวกี่รอบ", answer=Fraction(pairs, 10),
                           wrongs=[pairs * Fraction(34, 100), Fraction(pairs, 5), Fraction(pairs, 20)], unit="รอบ", topic=TOPIC_DNA,
                           hint=hint)
        if kind == 2:
            length = pairs * Fraction(34, 100)
            return numeric(stem=f"DNA สายคู่ยาว {show(length)} nm มีกี่คู่เบส", answer=pairs,
                           wrongs=[pairs * 2, Fraction(pairs, 10), pairs * 10], unit="คู่เบส", topic=TOPIC_DNA, hint=hint)
        return numeric(stem=f"DNA สายคู่ที่บิดเกลียว {pairs // 10} รอบ มีนิวคลีโอไทด์ทั้งหมดกี่นิวคลีโอไทด์", answer=pairs // 10 * 20,
                       wrongs=[pairs // 10 * 10, pairs // 10 * 40, pairs // 10 * 2], unit="นิวคลีโอไทด์", topic=TOPIC_DNA,
                       hint=hint + " แต่ละคู่เบสมี 2 นิวคลีโอไทด์")
