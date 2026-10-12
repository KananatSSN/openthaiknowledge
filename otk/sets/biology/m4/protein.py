"""โปรตีน

ชีวะ · ม.4 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 1 ม.4/5

Sets moved here from: science_wave_f44.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f44 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_PROTEIN = "โปรตีน"


FUNCTIONS = (
    ("เอนไซม์อะไมเลส", "เร่งปฏิกิริยาย่อยแป้ง"), ("ฮีโมโกลบิน", "ลำเลียงออกซิเจนในเลือด"),
    ("คอลลาเจน", "เป็นโครงสร้างให้ความแข็งแรงแก่ผิวหนังและเอ็น"), ("เคราติน", "เป็นโครงสร้างของผมและเล็บ"),
    ("อินซูลิน", "เป็นฮอร์โมนควบคุมระดับน้ำตาลในเลือด"), ("แอนติบอดี", "ป้องกันร่างกายจากสิ่งแปลกปลอม"),
    ("แอกทินและไมโอซิน", "ทำให้กล้ามเนื้อหดตัว"), ("เคซีน", "เป็นโปรตีนสะสมในนม"),
)


STRUCTURES = (
    ("โครงสร้างปฐมภูมิ", "ลำดับของกรดอะมิโนในสายพอลิเพปไทด์"),
    ("โครงสร้างทุติยภูมิ", "การม้วนเป็นเกลียวแอลฟาหรือพับเป็นแผ่นบีตาด้วยพันธะไฮโดรเจน"),
    ("โครงสร้างตติยภูมิ", "การพับตัวของสายพอลิเพปไทด์ทั้งสายเป็นรูปร่างสามมิติ"),
    ("โครงสร้างจตุรภูมิ", "สายพอลิเพปไทด์หลายสายรวมกัน เช่น ฮีโมโกลบิน"),
)


@question_type(
    "biology.protein_foundation",
    display_name={"th": "หน้าที่ของโปรตีน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_PROTEIN,
)
class ProteinFoundation(QuestionType):
    """Enzymes, transport, structure, hormones, defence, movement."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        protein, role = rng.choice(FUNCTIONS)
        others = [f for f in FUNCTIONS if f[0] != protein]
        if rng.random() < 0.5:
            return _labelled(stem=f"{protein}มีหน้าที่ใด", correct=role, wrongs=tuple(f[1] for f in rng.sample(others, 3)),
                             topic=TOPIC_PROTEIN, hint="โปรตีนทำหน้าที่เป็นเอนไซม์ ตัวลำเลียง โครงสร้าง ฮอร์โมน แอนติบอดี และการเคลื่อนไหว")
        return _labelled(stem=f"โปรตีนใดทำหน้าที่{role}", correct=protein, wrongs=tuple(f[0] for f in rng.sample(others, 3)),
                         topic=TOPIC_PROTEIN, hint="โปรตีนทำหน้าที่เป็นเอนไซม์ ตัวลำเลียง โครงสร้าง ฮอร์โมน แอนติบอดี และการเคลื่อนไหว")


@question_type(
    "biology.protein_fluency",
    display_name={"th": "กรดอะมิโนและพันธะเพปไทด์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_PROTEIN,
)
class ProteinFluency(QuestionType):
    """n amino acids make n − 1 peptide bonds and release n − 1 waters."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            n = rng.randint(3, 600)
            thing = rng.choice(("พันธะเพปไทด์", "โมเลกุลน้ำที่ถูกปล่อยออกมา"))
            return numeric(stem=f"สายพอลิเพปไทด์หนึ่งสายประกอบด้วยกรดอะมิโน {n} โมเลกุล มี{thing}กี่{'พันธะ' if thing.startswith('พันธะ') else 'โมเลกุล'}",
                           answer=n - 1, wrongs=[n, n + 1, n * 2], unit="", topic=TOPIC_PROTEIN,
                           hint="กรดอะมิโนต่อกันทีละคู่ด้วยพันธะเพปไทด์และเสียน้ำ 1 โมเลกุล สาย n หน่วยจึงมี n − 1 พันธะ")
        if kind == 1:
            n = rng.randint(2, 4)
            return numeric(stem=f"สายเพปไทด์ที่มีกรดอะมิโน {n} หน่วย จากกรดอะมิโน 20 ชนิด (ใช้ซ้ำได้) เรียงลำดับต่างกันได้กี่แบบ",
                           answer=20 ** n, wrongs=[20 * n, 20 ** (n - 1), 20 ** n * 2], unit="แบบ",
                           topic=TOPIC_PROTEIN, hint="แต่ละตำแหน่งเลือกได้ 20 แบบ จึงเป็น 20 ยกกำลังจำนวนตำแหน่ง")
        parts = (("หมู่อะมิโน (−NH₂)", "เป็นเบส"), ("หมู่คาร์บอกซิล (−COOH)", "เป็นกรด"),
                 ("หมู่ R", "ต่างกันในกรดอะมิโนแต่ละชนิด"), ("อะตอมคาร์บอนกลาง", "ยึดทุกหมู่เข้าด้วยกัน"))
        part, role = rng.choice(parts)
        others = [p[1] for p in parts if p[0] != part]
        return _labelled(stem=f"ในโครงสร้างของกรดอะมิโน {part} มีลักษณะอย่างไร", correct=role, wrongs=tuple(others),
                         topic=TOPIC_PROTEIN, hint="กรดอะมิโนมีหมู่อะมิโน หมู่คาร์บอกซิล และหมู่ R ที่ทำให้แต่ละชนิดต่างกัน")


@question_type(
    "biology.protein_application",
    display_name={"th": "ระดับโครงสร้างของโปรตีนและการเสียสภาพ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_PROTEIN,
)
class ProteinApplication(QuestionType):
    """Shape follows sequence; heat and extreme pH break the shape, not the sequence."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            level, meaning = rng.choice(STRUCTURES)
            others = [s for s in STRUCTURES if s[0] != level]
            if rng.random() < 0.5:
                return _labelled(stem=f"\"{meaning}\" คือโครงสร้างระดับใดของโปรตีน", correct=level,
                                 wrongs=tuple(s[0] for s in others), topic=TOPIC_PROTEIN,
                                 hint="ปฐมภูมิ = ลำดับ ทุติยภูมิ = เกลียว/แผ่น ตติยภูมิ = สามมิติทั้งสาย จตุรภูมิ = หลายสาย")
            return _labelled(stem=f"{level}ของโปรตีนหมายถึงอะไร", correct=meaning, wrongs=tuple(s[1] for s in others),
                             topic=TOPIC_PROTEIN, hint="ปฐมภูมิ = ลำดับ ทุติยภูมิ = เกลียว/แผ่น ตติยภูมิ = สามมิติทั้งสาย จตุรภูมิ = หลายสาย")
        cases = (
            ("ต้มไข่ขาวจนแข็งเป็นสีขาว", "โปรตีนเสียสภาพเพราะความร้อนทำลายโครงสร้างสามมิติ แต่ลำดับกรดอะมิโนยังเหมือนเดิม"),
            ("บีบมะนาวลงในนมแล้วนมจับตัวเป็นก้อน", "โปรตีนในนมเสียสภาพเพราะ pH เปลี่ยน"),
            ("ไข้สูงมากเป็นเวลานานเป็นอันตราย", "เอนไซม์ในร่างกายเสียสภาพ จึงเร่งปฏิกิริยาไม่ได้"),
            ("การดัดผมด้วยความร้อนและน้ำยา", "พันธะที่ยึดโครงสร้างของเคราตินถูกทำลายและสร้างใหม่ในรูปร่างใหม่"),
            ("ใช้แอลกอฮอล์เช็ดแผลเพื่อฆ่าเชื้อ", "แอลกอฮอล์ทำให้โปรตีนของจุลินทรีย์เสียสภาพ"),
            ("ผู้ป่วยโลหิตจางชนิดเซลล์รูปเคียวมีฮีโมโกลบินผิดปกติ", "กรดอะมิโนเปลี่ยนไปหนึ่งตำแหน่ง ทำให้โครงสร้างและการทำงานของโปรตีนเปลี่ยน"),
        )
        case, right = rng.choice(cases)
        others = [c[1] for c in cases if c[1] != right]
        false = ("โปรตีนถูกย่อยจนเหลือกรดอะมิโนเดี่ยว ๆ ทันที", "โปรตีนเปลี่ยนเป็นคาร์โบไฮเดรต",
                 "พันธะเพปไทด์ทุกพันธะถูกสลายจนหมด")
        return _labelled(stem=f"\"{case}\" อธิบายได้อย่างไร", correct=right,
                         wrongs=(*rng.sample(others, 2), rng.choice(false)), topic=TOPIC_PROTEIN,
                         hint="การเสียสภาพทำลายรูปร่างสามมิติ ไม่ได้ตัดพันธะเพปไทด์")
