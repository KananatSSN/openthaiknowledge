"""ความสัมพันธ์ระหว่างยีน แอลลีล โปรตีน และลักษณะ

ชีวะ · ม.4 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 2 ม.4/8

Sets moved here from: science_wave_f50.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f50 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_TRAIT = "ความสัมพันธ์ระหว่างยีน แอลลีล โปรตีน และลักษณะ"


TERMS = (
    ("ยีน", "ช่วงของ DNA ที่กำหนดการสร้างโปรตีนหรือ RNA"),
    ("แอลลีล", "รูปแบบต่าง ๆ ของยีนที่อยู่ตำแหน่งเดียวกันบนโครโมโซมคู่เหมือน"),
    ("โลคัส", "ตำแหน่งของยีนบนโครโมโซม"),
    ("จีโนไทป์", "แอลลีลที่สิ่งมีชีวิตมีสำหรับยีนหนึ่ง เช่น Aa"),
    ("ฟีโนไทป์", "ลักษณะที่แสดงออกให้เห็นหรือตรวจวัดได้"),
    ("โฮโมไซกัส", "มีแอลลีลของยีนหนึ่งเหมือนกันทั้งสองแอลลีล"),
    ("เฮเทอโรไซกัส", "มีแอลลีลของยีนหนึ่งต่างกันสองแบบ"),
    ("โครโมโซมคู่เหมือน", "โครโมโซมคู่ที่รูปร่างเหมือนกันและมียีนควบคุมลักษณะเดียวกันที่ตำแหน่งตรงกัน"),
)


TRAIT_HINT = "ยีนเป็นช่วงของ DNA ยีนหนึ่งมีได้หลายแอลลีล แต่ละแอลลีลกำหนดโปรตีนที่ต่างกันเล็กน้อย โปรตีนทำให้เกิดลักษณะ"


EXAMPLES = (
    ("เมล็ดถั่วลันเตาขรุขระ", "แอลลีลด้อยสร้างเอนไซม์เปลี่ยนน้ำตาลเป็นแป้งที่ทำงานไม่ได้ เมล็ดสะสมน้ำตาลและน้ำมาก แล้วเหี่ยวย่นเมื่อแห้ง"),
    ("ผิวเผือก", "แอลลีลด้อยสร้างเอนไซม์ไทโรซิเนสที่ทำงานไม่ได้ จึงสร้างสารสีเมลานินไม่ได้"),
    ("โลหิตจางชนิดเซลล์รูปเคียว", "แอลลีลที่ผิดปกติทำให้กรดอะมิโนในสายโกลบินเปลี่ยนจากกรดกลูทามิกเป็นวาลีน"),
    ("ต้นถั่วลันเตาเตี้ย", "แอลลีลด้อยสร้างเอนไซม์ในการสร้างฮอร์โมนจิบเบอเรลลินที่ทำงานได้น้อย"),
    ("ฟีนิลคีโตนูเรีย", "แอลลีลด้อยทำให้เอนไซม์เปลี่ยนฟีนิลแอลานีนทำงานไม่ได้ ฟีนิลแอลานีนจึงสะสมเป็นพิษต่อสมอง"),
    ("ดอกถั่วลันเตาสีขาว", "แอลลีลด้อยไม่สร้างโปรตีนที่ควบคุมการสร้างสารสีแอนโทไซยานินในกลีบดอก"),
    ("ธาลัสซีเมีย", "ยีนที่ผิดปกติทำให้สร้างสายโกลบินของฮีโมโกลบินได้น้อยหรือไม่ได้เลย"),
)


PRODUCTS = (
    ("สีดอก", "เอนไซม์สร้างสารสี", "ดอกมีสี", "ดอกสีขาว", "ดอกสีอ่อน"),
    ("สีผิว", "เอนไซม์ไทโรซิเนส", "ผิวปกติ", "ผิวเผือก", "ผิวสีอ่อนลง"),
    ("รูปร่างเมล็ด", "เอนไซม์เปลี่ยนน้ำตาลเป็นแป้ง", "เมล็ดกลม", "เมล็ดขรุขระ", "เมล็ดกลมแต่ย่นเล็กน้อย"),
    ("ความสูงของลำต้น", "เอนไซม์สร้างจิบเบอเรลลิน", "ต้นสูง", "ต้นเตี้ย", "ต้นสูงปานกลาง"),
)


@question_type(
    "biology.gene_to_trait_foundation",
    display_name={"th": "ความหมายของยีน แอลลีล จีโนไทป์ และฟีโนไทป์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_TRAIT,
)
class GeneToTraitFoundation(QuestionType):
    """The words of genetics, both ways, and the chain from DNA to trait."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.15:
            return _labelled(stem="ข้อใดแสดงความสัมพันธ์จากสารพันธุกรรมไปสู่ลักษณะได้ถูกต้อง",
                             correct="ยีน (DNA) → mRNA → โปรตีน → ลักษณะทางพันธุกรรม",
                             wrongs=tuple(("โปรตีน → ยีน (DNA) → mRNA → ลักษณะทางพันธุกรรม",
                                                      "ยีน (DNA) → โปรตีน → mRNA → ลักษณะทางพันธุกรรม",
                                                      "ลักษณะทางพันธุกรรม → โปรตีน → mRNA → ยีน (DNA)",
                                                      "mRNA → ยีน (DNA) → ลักษณะทางพันธุกรรม → โปรตีน")),
                             topic=TOPIC_TRAIT, hint=TRAIT_HINT)
        term, meaning = rng.choice(TERMS)
        others = rng.sample([t for t in TERMS if t[0] != term], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"{term}หมายถึงข้อใด", correct=meaning, wrongs=tuple(t[1] for t in others), topic=TOPIC_TRAIT,
                             hint=TRAIT_HINT)
        return _labelled(stem=f"\"{meaning}\" คือความหมายของคำใด", correct=term, wrongs=tuple(t[0] for t in others),
                         topic=TOPIC_TRAIT, hint=TRAIT_HINT)


@question_type(
    "biology.gene_to_trait_fluency",
    display_name={"th": "ตัวอย่างความสัมพันธ์ระหว่างแอลลีล โปรตีน และลักษณะ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_TRAIT,
)
class GeneToTraitFluency(QuestionType):
    """Real traits traced back to the protein their allele makes."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        trait, cause = rng.choice(EXAMPLES)
        others = rng.sample([e for e in EXAMPLES if e[0] != trait], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"ลักษณะ{trait}เกิดขึ้นได้อย่างไรในระดับโปรตีน", correct=cause, wrongs=tuple(e[1] for e in others),
                             topic=TOPIC_TRAIT, hint=TRAIT_HINT)
        return _labelled(stem=f"\"{cause}\" ทำให้เกิดลักษณะใด", correct=trait, wrongs=tuple(e[0] for e in others),
                         topic=TOPIC_TRAIT, hint=TRAIT_HINT)


@question_type(
    "biology.gene_to_trait_application",
    display_name={"th": "อธิบายลักษณะเด่นและด้อยด้วยปริมาณโปรตีน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_TRAIT,
)
class GeneToTraitApplication(QuestionType):
    """One working allele may make enough protein (dominance), or only half enough (incomplete)."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        trait, protein, normal, absent, half = rng.choice(PRODUCTS)
        enough = rng.random() < 0.6
        genotype = rng.choice(("AA", "Aa", "aa", "Aa"))
        setting = (f"ยีนควบคุม{trait} แอลลีล A สร้าง{protein}ที่ทำงานได้ แอลลีล a สร้าง{protein}ที่ทำงานไม่ได้ "
                   + ("และ" if enough else "แต่") + f"{protein}จากแอลลีล A เพียงหนึ่งแอลลีล"
                   + ("เพียงพอให้แสดงลักษณะปกติ" if enough else "ได้ปริมาณเพียงครึ่งหนึ่งและไม่พอให้แสดงลักษณะเต็มที่"))
        if rng.random() < 0.3:
            right = "ลักษณะเด่นสมบูรณ์ ต้น AA และ Aa มีฟีโนไทป์เหมือนกัน" if enough else "ลักษณะเด่นไม่สมบูรณ์ ต้น Aa มีลักษณะกึ่งกลาง"
            wrong = "ลักษณะเด่นไม่สมบูรณ์ ต้น Aa มีลักษณะกึ่งกลาง" if enough else "ลักษณะเด่นสมบูรณ์ ต้น AA และ Aa มีฟีโนไทป์เหมือนกัน"
            return _labelled(stem=f"{setting} ลักษณะนี้ถ่ายทอดแบบใด", correct=right,
                             wrongs=(wrong, "การข่มร่วมกัน ต้น Aa แสดงทั้งสองลักษณะแยกกันชัดเจน", "a ข่ม A เพราะ a สร้างโปรตีนไม่ได้"),
                             topic=TOPIC_TRAIT, hint="ถ้าโปรตีนจากแอลลีลเดียวพอ Aa จะเหมือน AA (เด่นสมบูรณ์) ถ้าไม่พอ Aa จะอยู่กึ่งกลาง")
        if genotype == "AA":
            right = f"{normal} เพราะมี{protein}ที่ทำงานได้เต็มที่"
        elif genotype == "aa":
            right = f"{absent} เพราะไม่มี{protein}ที่ทำงานได้"
        elif enough:
            right = f"{normal} เพราะ{protein}จากแอลลีล A หนึ่งแอลลีลเพียงพอ"
        else:
            right = f"{half} เพราะมี{protein}ที่ทำงานได้เพียงครึ่งหนึ่ง"
        options = [f"{normal} เพราะมี{protein}ที่ทำงานได้เต็มที่", f"{absent} เพราะไม่มี{protein}ที่ทำงานได้",
                   f"{normal} เพราะ{protein}จากแอลลีล A หนึ่งแอลลีลเพียงพอ", f"{half} เพราะมี{protein}ที่ทำงานได้เพียงครึ่งหนึ่ง",
                   f"{absent} เพราะแอลลีล a ข่มแอลลีล A"]
        wrongs = rng.sample([o for o in options if o != right], 3)
        return _labelled(stem=f"{setting} ต้นจีโนไทป์ {genotype} มีฟีโนไทป์อย่างไร", correct=right, wrongs=tuple(wrongs),
                         topic=TOPIC_TRAIT, hint="นับว่ามีแอลลีล A ที่สร้างโปรตีนทำงานได้กี่แอลลีล แล้วดูว่าปริมาณนั้นพอหรือไม่")
