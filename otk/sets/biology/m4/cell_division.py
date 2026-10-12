"""การแบ่งนิวเคลียสแบบไมโทซิสและไมโอซิส

ชีวะ · ม.4 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 1 ม.4/16

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


TOPIC_DIVISION = "การแบ่งนิวเคลียสแบบไมโทซิสและไมโอซิส"


MITOSIS = (
    ("โพรเฟส", "โครมาทินขดตัวเป็นโครโมโซมเห็นชัด เยื่อหุ้มนิวเคลียสสลาย"),
    ("เมทาเฟส", "โครโมโซมเรียงตัวกลางเซลล์ เห็นชัดที่สุด"),
    ("แอนาเฟส", "โครมาทิดพี่น้องแยกไปยังขั้วเซลล์"),
    ("เทโลเฟส", "โครโมโซมถึงขั้วเซลล์ เยื่อหุ้มนิวเคลียสกลับมา"),
)


MEIOSIS = (
    ("โพรเฟส I", "โครโมโซมคู่เหมือนเข้าคู่กัน (ไซแนปซิส) และอาจเกิดครอสซิงโอเวอร์"),
    ("เมทาเฟส I", "คู่โครโมโซมคู่เหมือนเรียงตัวกลางเซลล์เป็นคู่"),
    ("แอนาเฟส I", "โครโมโซมคู่เหมือนแยกจากกันไปคนละขั้ว"),
    ("แอนาเฟส II", "โครมาทิดพี่น้องแยกจากกันไปคนละขั้ว"),
)


COMPARE = (
    ("จำนวนเซลล์ที่ได้จากการแบ่งหนึ่งครั้ง", "2 เซลล์", "4 เซลล์"),
    ("จำนวนโครโมโซมของเซลล์ที่ได้เทียบกับเซลล์เริ่มต้น", "เท่าเดิม (2n)", "ลดลงครึ่งหนึ่ง (n)"),
    ("การเกิดครอสซิงโอเวอร์", "ไม่เกิด", "เกิดในโพรเฟส I"),
    ("ความเหมือนกันทางพันธุกรรมของเซลล์ที่ได้", "เหมือนเซลล์เดิม", "ต่างกันและต่างจากเซลล์เดิม"),
    ("ตำแหน่งที่พบในพืช", "ปลายรากและปลายยอด", "อับเรณูและออวุล"),
)


@question_type(
    "biology.cell_division_foundation",
    display_name={"th": "ระยะต่าง ๆ ของการแบ่งนิวเคลียส"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_DIVISION,
)
class CellDivisionFoundation(QuestionType):
    """Prophase, metaphase, anaphase, telophase: what each looks like on the slide."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        phase, event = rng.choice(MITOSIS)
        others = [m for m in MITOSIS if m[0] != phase]
        if rng.random() < 0.4:
            stage, event = rng.choice(MEIOSIS)
            pool = [e for s2, e in MEIOSIS + MITOSIS if e != event]
            return _labelled(stem=f"ในการแบ่งแบบไมโอซิส ระยะ{stage}มีเหตุการณ์ใด", correct=event, wrongs=tuple(pool),
                             topic=TOPIC_DIVISION, hint="ไมโอซิส I แยกคู่ฮอมอโลกัส (มีไซแนปซิสและครอสซิงโอเวอร์) ไมโอซิส II แยกโครมาทิด")
        if rng.random() < 0.5:
            return _labelled(stem=f"เมื่อส่องเซลล์ปลายรากหอมที่กำลังแบ่งแบบไมโทซิส พบว่า \"{event}\" เซลล์นั้นอยู่ในระยะใด",
                             correct=phase, wrongs=tuple(m[0] for m in others), topic=TOPIC_DIVISION,
                             hint="โพรเฟสโครโมโซมขดตัว เมทาเฟสเรียงกลาง แอนาเฟสแยกไปขั้ว เทโลเฟสถึงขั้วและสร้างนิวเคลียสใหม่")
        return _labelled(stem=f"ระยะ{phase}ของไมโทซิสมีเหตุการณ์ใด", correct=event, wrongs=tuple(m[1] for m in others),
                         topic=TOPIC_DIVISION, hint="โพรเฟสโครโมโซมขดตัว เมทาเฟสเรียงกลาง แอนาเฟสแยกไปขั้ว เทโลเฟสถึงขั้ว")


@question_type(
    "biology.cell_division_fluency",
    display_name={"th": "เปรียบเทียบไมโทซิสกับไมโอซิส"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_DIVISION,
)
class CellDivisionFluency(QuestionType):
    """Two identical cells, or four varied cells with half the chromosomes."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        feature, mitosis, meiosis = rng.choice(COMPARE)
        which = rng.choice(("ไมโทซิส", "ไมโอซิส"))
        right = mitosis if which == "ไมโทซิส" else meiosis
        other = meiosis if which == "ไมโทซิส" else mitosis
        pool = [x for f in COMPARE if f[0] != feature for x in f[1:]]
        return _labelled(stem=f"{feature}ในการแบ่งแบบ{which}เป็นอย่างไร", correct=right, wrongs=(other, *rng.sample(pool, 2)),
                         topic=TOPIC_DIVISION, hint="ไมโทซิสได้ 2 เซลล์เหมือนเดิม ไมโอซิสได้ 4 เซลล์ที่มีโครโมโซมครึ่งหนึ่งและต่างกัน")


@question_type(
    "biology.cell_division_application",
    display_name={"th": "จำนวนโครโมโซมและโครมาทิดในแต่ละระยะ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_DIVISION,
)
class CellDivisionApplication(QuestionType):
    """Count chromosomes and chromatids through each division."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        organism, diploid = rng.choice(CHROMOSOMES)
        cases = (
            ("เมทาเฟสของไมโทซิส", "โครมาทิด", diploid * 2), ("แอนาเฟสของไมโทซิส (ทั้งเซลล์)", "โครโมโซม", diploid * 2),
            ("เซลล์ลูกหลังไมโทซิส", "โครโมโซม", diploid), ("เมทาเฟส I ของไมโอซิส", "โครโมโซม", diploid),
            ("เซลล์หลังไมโอซิส I", "โครโมโซม", diploid // 2), ("เซลล์หลังไมโอซิส II", "โครโมโซม", diploid // 2),
            ("โพรเฟส I ของไมโอซิส", "ไบวาเลนต์ (คู่โครโมโซมที่เข้าคู่กัน)", diploid // 2),
        )
        stage, thing, count = rng.choice(cases)
        return numeric(stem=f"เซลล์ร่างกายของ{organism}มีโครโมโซม {diploid} แท่ง (2n) ใน{stage} มี{thing}กี่หน่วย",
                       answer=count, wrongs=[c for c in (diploid, diploid * 2, diploid // 2, diploid * 4) if c != count][:3],
                       unit="", topic=TOPIC_DIVISION,
                       hint="ก่อนแบ่งจำลองดีเอ็นเอ (โครโมโซมละ 2 โครมาทิด) ไมโอซิส I แยกคู่ฮอมอโลกัส ไมโอซิส II แยกโครมาทิด")
