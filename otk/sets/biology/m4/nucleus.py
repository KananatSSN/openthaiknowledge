"""โครงสร้างและหน้าที่ของนิวเคลียส

ชีวะ · ม.4 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 1 ม.4/13

Sets moved here from: science_wave_f47.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f47 import CHROMOSOMES, SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_NUCLEUS = "โครงสร้างและหน้าที่ของนิวเคลียส"


NUCLEUS_PARTS = (
    ("เยื่อหุ้มนิวเคลียส", "เยื่อสองชั้นที่มีรูเปิดให้สารผ่านเข้าออกระหว่างนิวเคลียสกับไซโทพลาซึม"),
    ("รูที่เยื่อหุ้มนิวเคลียส", "เป็นทางให้ RNA ออกจากนิวเคลียสและให้โปรตีนเข้าสู่นิวเคลียส"),
    ("นิวคลีโอลัส", "เป็นบริเวณสร้าง RNA ของไรโบโซม (rRNA) และประกอบหน่วยย่อยไรโบโซม"),
    ("โครมาทิน", "DNA พันรอบโปรตีนฮิสโตน ซึ่งขดแน่นเป็นโครโมโซมเมื่อแบ่งเซลล์"),
)


NUCLEUS_TRUE = ("เยื่อหุ้มนิวเคลียสมีสองชั้นและมีรูให้สารผ่าน", "นิวคลีโอลัสเป็นแหล่งสร้าง rRNA",
                "โครมาทินประกอบด้วย DNA และโปรตีนฮิสโตน", "mRNA ออกจากนิวเคลียสทางรูที่เยื่อหุ้มนิวเคลียส",
                "เมื่อเซลล์เริ่มแบ่ง โครมาทินขดตัวแน่นเป็นโครโมโซม")


NUCLEUS_FALSE = ("เยื่อหุ้มนิวเคลียสมีชั้นเดียวและไม่มีรู", "นิวคลีโอลัสมีเยื่อหุ้มสองชั้นล้อมรอบ",
                 "โครมาทินประกอบด้วยลิพิดและคาร์โบไฮเดรต", "นิวเคลียสเป็นแหล่งสร้าง ATP หลักของเซลล์",
                 "เซลล์ทุกชนิดในร่างกายคนมีนิวเคลียสเดียวเสมอ", "โปรตีนทั้งหมดถูกสร้างภายในนิวเคลียส")


NUCLEUS_FACTS = (
    ("เซลล์ใดไม่มีนิวเคลียส", "เซลล์เม็ดเลือดแดงของคนที่เจริญเต็มที่", ("เซลล์ตับ", "เซลล์ประสาท", "เซลล์กล้ามเนื้อ")),
    ("เซลล์ใดมีหลายนิวเคลียส", "เซลล์กล้ามเนื้อลาย", ("เซลล์เม็ดเลือดแดงของคน", "เซลล์เยื่อบุข้างแก้ม", "เซลล์คุม")),
    ("ถ้าตัดนิวเคลียสออกจากอะมีบา จะเกิดอะไรขึ้น", "อะมีบาไม่เจริญเติบโต ไม่แบ่งตัว และตายในที่สุด",
     ("อะมีบาแบ่งตัวได้เร็วขึ้น", "อะมีบาสร้างนิวเคลียสใหม่ได้ทันที", "อะมีบาไม่มีการเปลี่ยนแปลง")),
    ("การทดลองของแฮมเมอร์ลิงกับสาหร่ายอะซิตาบูลาเรียแสดงว่าอะไร", "นิวเคลียสควบคุมลักษณะของเซลล์",
     ("ไซโทพลาซึมควบคุมลักษณะของเซลล์", "ผนังเซลล์ควบคุมรูปร่างหมวก", "คลอโรพลาสต์ควบคุมการแบ่งเซลล์")),
    ('รูที่เยื่อหุ้มนิวเคลียสมีหน้าที่อะไร', 'เป็นทางให้ mRNA และโปรตีนผ่านเข้าออกนิวเคลียส',
     ('เป็นทางให้โครโมโซมทั้งแท่งออกไปแบ่งตัวในไซโทพลาซึม', 'เป็นที่สังเคราะห์โปรตีนทั้งหมดที่เซลล์ใช้อยู่ทุกชนิด', 'เป็นทางให้ไมโทคอนเดรียเข้าไปในนิวเคลียส')),
    ('นิวคลีโอลัสมีหน้าที่สำคัญอย่างไร', 'เป็นแหล่งสร้าง rRNA และประกอบหน่วยย่อยของไรโบโซม',
     ('เป็นที่เก็บพลังงานในรูป ATP ของเซลล์ทั้งหมดไว้ใช้ยามจำเป็น', 'เป็นที่สังเคราะห์ด้วยแสงภายในนิวเคลียสแทนคลอโรพลาสต์', 'เป็นที่ย่อยสลายโปรตีนที่เซลล์ไม่ต้องการแล้วด้วยเอนไซม์')),
    ('เซลล์แบคทีเรียต่างจากเซลล์พืชและสัตว์ในเรื่องนิวเคลียสอย่างไร', 'ไม่มีเยื่อหุ้มนิวเคลียส สารพันธุกรรมอยู่ในไซโทพลาซึม',
     ('มีนิวเคลียสหลายอันอยู่ในเซลล์เดียวเสมอ ทุกอันมีเยื่อหุ้มสองชั้น', 'ไม่มีสารพันธุกรรมใด ๆ อยู่ภายในเซลล์เลย จึงรับคำสั่งจากเซลล์อื่น', 'มีนิวเคลียสที่มีเยื่อหุ้มหนาสามชั้นซ้อนกันและไม่มีรูให้สารผ่าน')),
    ('ในเซลล์ที่ไม่ได้แบ่งตัว สารพันธุกรรมในนิวเคลียสอยู่ในรูปใด', 'โครมาทินที่เป็นเส้นใยยาวกระจายอยู่ ยังไม่ขดเป็นแท่ง',
     ('โครโมโซมแท่งสั้นหนาที่เห็นได้ชัดตลอดเวลาแม้เซลล์ไม่ได้แบ่งตัว', 'ก้อนโปรตีนที่ไม่มีดีเอ็นเออยู่ภายในเลย และไม่เปลี่ยนรูปไปตลอดชีวิตเซลล์', 'สาย mRNA ที่ขดอยู่รอบนิวคลีโอลัสโดยไม่มีดีเอ็นเอปนอยู่')),
)


@question_type(
    "biology.nucleus_foundation",
    display_name={"th": "โครงสร้างของนิวเคลียส"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_NUCLEUS,
)
class NucleusFoundation(QuestionType):
    """Envelope with pores, nucleolus, and chromatin."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            return _labelled(stem="ข้อใดกล่าวถึงนิวเคลียสได้ถูกต้อง", correct=rng.choice(NUCLEUS_TRUE),
                             wrongs=tuple(NUCLEUS_FALSE), topic=TOPIC_NUCLEUS,
                             hint="เยื่อหุ้มสองชั้นมีรู นิวคลีโอลัสสร้าง rRNA โครมาทินคือ DNA กับฮิสโตน")
        part, role = rng.choice(NUCLEUS_PARTS)
        others = [p for p in NUCLEUS_PARTS if p[0] != part]
        if rng.random() < 0.5:
            return _labelled(stem=f"{part}มีลักษณะหรือหน้าที่อย่างไร", correct=role, wrongs=tuple(p[1] for p in others),
                             topic=TOPIC_NUCLEUS, hint="เยื่อหุ้มสองชั้นมีรู นิวคลีโอลัสสร้าง rRNA โครมาทินคือ DNA กับฮิสโตน")
        return _labelled(stem=f"ส่วนใดของนิวเคลียส{role}", correct=part, wrongs=tuple(p[0] for p in others),
                         topic=TOPIC_NUCLEUS, hint="เยื่อหุ้มสองชั้นมีรู นิวคลีโอลัสสร้าง rRNA โครมาทินคือ DNA กับฮิสโตน")


@question_type(
    "biology.nucleus_fluency",
    display_name={"th": "จำนวนโครโมโซมในเซลล์ร่างกายและเซลล์สืบพันธุ์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_NUCLEUS,
)
class NucleusFluency(QuestionType):
    """Body cells carry 2n; gametes carry n."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        organism, diploid = rng.choice(CHROMOSOMES)
        kind = rng.randrange(3)
        if kind == 0:
            return numeric(stem=f"เซลล์ร่างกายของ{organism}มีโครโมโซม {diploid} แท่ง (2n) เซลล์สืบพันธุ์มีโครโมโซมกี่แท่ง",
                           answer=diploid // 2, wrongs=[diploid, diploid * 2, diploid // 2 + 1], unit="แท่ง", topic=TOPIC_NUCLEUS,
                           hint="เซลล์สืบพันธุ์มีโครโมโซมครึ่งหนึ่งของเซลล์ร่างกาย (n)")
        if kind == 1:
            return numeric(stem=f"เซลล์สืบพันธุ์ของ{organism}มีโครโมโซม {diploid // 2} แท่ง เซลล์ร่างกายมีโครโมโซมกี่คู่",
                           answer=diploid // 2, wrongs=[diploid, diploid // 4 if diploid % 4 == 0 else diploid // 2 + 1, diploid * 2],
                           unit="คู่", topic=TOPIC_NUCLEUS, hint="เซลล์ร่างกายมี 2n แท่ง คือ n คู่")
        return numeric(stem=f"เซลล์ร่างกายของ{organism}มีโครโมโซม {diploid} แท่ง ก่อนแบ่งเซลล์เมื่อจำลองดีเอ็นเอแล้วมีโครมาทิดทั้งหมดกี่โครมาทิด",
                       answer=diploid * 2, wrongs=[diploid, diploid // 2, diploid * 4], unit="โครมาทิด", topic=TOPIC_NUCLEUS,
                       hint="หลังจำลองดีเอ็นเอ โครโมโซมหนึ่งแท่งมีสองโครมาทิด")


@question_type(
    "biology.nucleus_application",
    display_name={"th": "บทบาทของนิวเคลียสจากหลักฐานการทดลอง"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_NUCLEUS,
)
class NucleusApplication(QuestionType):
    """Cells without a nucleus cannot divide; the nucleus sets the cell's traits."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(NUCLEUS_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_NUCLEUS,
                         hint="นิวเคลียสเก็บสารพันธุกรรมและควบคุมการทำงานและการแบ่งของเซลล์")
