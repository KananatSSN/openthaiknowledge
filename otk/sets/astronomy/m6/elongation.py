"""มุมห่างและตำแหน่งปรากฏของดาวเคราะห์

ดาราศาสตร์ · ม.6 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/17

Sets moved here from: science_wave_f86.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f86 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_ELONG = "มุมห่างและตำแหน่งปรากฏของดาวเคราะห์"


CONFIGS = (
    ("ดาวเคราะห์วงนอกอยู่ในตำแหน่งตรงข้ามกับดวงอาทิตย์ (opposition)", "มุมห่าง 180° ขึ้นเมื่อดวงอาทิตย์ตก เห็นได้ตลอดคืน และสว่างที่สุด"),
    ("ดาวเคราะห์วงนอกอยู่ในตำแหน่งร่วมทิศกับดวงอาทิตย์ (conjunction)", "มุมห่าง 0° อยู่หลังดวงอาทิตย์ มองไม่เห็น"),
    ("ดาวเคราะห์วงนอกอยู่ในตำแหน่งตั้งฉากตะวันออก (eastern quadrature)", "มุมห่าง 90° อยู่กลางฟ้าเมื่อดวงอาทิตย์ตก เห็นในครึ่งแรกของคืน"),
    ("ดาวศุกร์อยู่ในตำแหน่งมุมห่างมากที่สุดทางตะวันออก", "เห็นเป็นดาวประจำเมืองทางทิศตะวันตกหลังดวงอาทิตย์ตก"),
    ("ดาวศุกร์อยู่ในตำแหน่งมุมห่างมากที่สุดทางตะวันตก", "เห็นเป็นดาวรุ่งทางทิศตะวันออกก่อนดวงอาทิตย์ขึ้น"),
    ("ดาวศุกร์อยู่ในตำแหน่งร่วมทิศวงใน (inferior conjunction)", "อยู่ระหว่างโลกกับดวงอาทิตย์ มองไม่เห็น ยกเว้นเมื่อผ่านหน้าดวงอาทิตย์"),
)


ELONG_FACTS = (
    ("มุมห่าง (elongation) ของดาวเคราะห์คืออะไร", "มุมระหว่างดวงอาทิตย์กับดาวเคราะห์ เมื่อมองจากโลก",
     ("มุมระหว่างโลกกับดวงอาทิตย์ เมื่อมองจากดาวเคราะห์", "มุมเงยของดาวเคราะห์เหนือขอบฟ้า", "มุมที่แกนหมุนของดาวเคราะห์เอียงจากแนวตั้งฉาก", "มุมทิศของดาวเคราะห์ เมื่อวัดจากทิศเหนือ")),
    ("เหตุใดจึงไม่เคยเห็นดาวพุธและดาวศุกร์กลางฟ้าตอนเที่ยงคืน", "เป็นดาวเคราะห์วงใน มุมห่างจากดวงอาทิตย์มีค่าจำกัด (ดาวพุธประมาณ 28° ดาวศุกร์ประมาณ 47°)",
     ("เป็นดาวเคราะห์วงใน จึงอยู่ตรงข้ามกับดวงอาทิตย์ได้ในคืนวันเพ็ญ", "ทั้งสองดวงอยู่นอกวงโคจรของโลก", "เป็นดาวเคราะห์วงนอก มุมห่างจากดวงอาทิตย์มีค่าได้ถึง 180° ทุกดวง", "ทั้งสองดวงอยู่ไกลกว่าดาวพฤหัสบดี")),
    ("ดาวเคราะห์ใดมีมุมห่างจากดวงอาทิตย์ได้ถึง 180°", "ดาวเคราะห์วงนอก เช่น ดาวอังคาร ดาวพฤหัสบดี",
     ("ดาวพุธที่อยู่ใกล้ดวงอาทิตย์ที่สุด", "ดาวศุกร์ซึ่งสว่างที่สุดบนท้องฟ้า", "ดาวพุธและดาวศุกร์", "ไม่มีดาวเคราะห์ดวงใดเลย เพราะมุมห่างสูงสุดคือ 90°")),
    ("เหตุใดดาวอังคารจึงสว่างมากที่สุดในช่วงตำแหน่งตรงข้ามดวงอาทิตย์", "อยู่ใกล้โลกที่สุดและหันด้านสว่างเต็มดวงเข้าหาโลก",
     ("อยู่ไกลโลกที่สุดและหันด้านมืดเข้าหาโลก", "ดาวอังคารร้อนที่สุดในช่วงนั้น", "ดาวอังคารเข้าใกล้ดวงอาทิตย์ที่สุดจนร้อนและเรืองแสงเอง", "ดาวอังคารอยู่หลังดวงอาทิตย์")),
    ("ดาวเคราะห์วงนอกที่อยู่ตำแหน่งตรงข้ามดวงอาทิตย์จะผ่านเมริเดียนเวลาประมาณเท่าใด", "ประมาณเที่ยงคืน",
     ("ประมาณเที่ยงวัน", "ประมาณหกโมงเช้า", "ประมาณหกโมงเย็น", "ไม่ผ่านเมริเดียนเลย")),
    ("เหตุใดเมื่อดูดาวศุกร์ผ่านกล้องโทรทรรศน์จึงเห็นเป็นเสี้ยวคล้ายดวงจันทร์", "ดาวศุกร์เป็นดาวเคราะห์วงใน ด้านที่รับแสงหันเข้าหาโลกไม่เท่ากันตามตำแหน่งในวงโคจร",
     ("เงาของโลกบังดาวศุกร์เป็นบางส่วน ตามตำแหน่งของดาวศุกร์ในวงโคจร", "ดาวศุกร์ผลิตแสงเองไม่สม่ำเสมอ", "ดาวศุกร์เป็นดาวเคราะห์วงนอก จึงหันด้านสว่างเข้าหาโลกเต็มดวงตลอดเวลา", "ดาวศุกร์หมุนรอบตัวเองเร็วมาก")),
    ("ดาวเคราะห์ใดไม่สามารถอยู่ในตำแหน่งร่วมทิศวงใน (inferior conjunction) ได้", "ดาวเคราะห์วงนอก เช่น ดาวเสาร์",
     ("ดาวพุธที่อยู่ใกล้ดวงอาทิตย์ที่สุด", "ดาวศุกร์ซึ่งสว่างที่สุดบนท้องฟ้า", "ดาวพุธและดาวศุกร์", "ดาวเคราะห์ทุกดวงอยู่ได้")),
)


ELONG_HINT = ("มุมห่างคือมุมระหว่างดวงอาทิตย์กับดาวเคราะห์เมื่อมองจากโลก ดาวเคราะห์วงในมีมุมห่างสูงสุดจำกัด "
              "มุมห่างตะวันออก = เห็นหัวค่ำทางทิศตะวันตก มุมห่างตะวันตก = เห็นก่อนรุ่งทางทิศตะวันออก "
              "ดาวเคราะห์วงนอกที่ตำแหน่งตรงข้ามดวงอาทิตย์ (180°) อยู่ใกล้โลกที่สุด เห็นทั้งคืน ผ่านเมริเดียนตอนเที่ยงคืน")


SYNODIC = ((2, 2), (3, Fraction(3, 2)), (5, Fraction(5, 4)), (6, Fraction(6, 5)), (11, Fraction(11, 10)), (Fraction(3, 2), 3),
           (Fraction(5, 4), 5), (Fraction(1, 2), 1), (Fraction(4, 5), 4), (Fraction(3, 5), Fraction(3, 2)),
           (Fraction(3, 4), 3), (Fraction(1, 5), Fraction(1, 4)))


@question_type(
    "astro.elongation_foundation",
    display_name={"th": "มุมห่างและตำแหน่งของดาวเคราะห์ในวงโคจร"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_ELONG,
)
class ElongationFoundation(QuestionType):
    """What elongation is; inner planets' limit; opposition."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(ELONG_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_ELONG, hint=ELONG_HINT)


@question_type(
    "astro.elongation_fluency",
    display_name={"th": "ตำแหน่งปรากฏของดาวเคราะห์จากตำแหน่งในวงโคจร"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_ELONG,
)
class ElongationFluency(QuestionType):
    """Configuration to what an observer sees, and back; where a planet is at a given elongation."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.6:
            config, seen = rng.choice(CONFIGS)
            picked = rng.sample([c for c in CONFIGS if c[0] != config], 3)
            if roll < 0.3:
                return _labelled(stem=f"เมื่อ{config} ผู้สังเกตบนโลกจะเห็นอย่างไร", correct=seen, wrongs=tuple(p[1] for p in picked),
                                 topic=TOPIC_ELONG, hint=ELONG_HINT)
            return _labelled(stem=f"ผู้สังเกตเห็นดาวเคราะห์ในลักษณะ \"{seen}\" ดาวเคราะห์อยู่ในตำแหน่งใด", correct=config,
                             wrongs=tuple(p[0] for p in picked), topic=TOPIC_ELONG, hint=ELONG_HINT)
        angle = rng.choice([a for a in range(10, 171, 10) if a != 90])
        east = rng.random() < 0.5
        right = ("เห็นทางท้องฟ้าด้านตะวันตกหลังดวงอาทิตย์ตก" if east else "เห็นทางท้องฟ้าด้านตะวันออกก่อนดวงอาทิตย์ขึ้น") if angle < 90 else \
                ("เห็นตั้งแต่หัวค่ำ อยู่ค่อนไปทางท้องฟ้าด้านตะวันออก" if east else "เห็นตั้งแต่ก่อนเที่ยงคืนจนถึงรุ่งเช้า อยู่ค่อนไปทางท้องฟ้าด้านตะวันตกเมื่อใกล้รุ่ง")
        options = ("เห็นทางท้องฟ้าด้านตะวันตกหลังดวงอาทิตย์ตก", "เห็นทางท้องฟ้าด้านตะวันออกก่อนดวงอาทิตย์ขึ้น",
                   "เห็นตั้งแต่หัวค่ำ อยู่ค่อนไปทางท้องฟ้าด้านตะวันออก", "เห็นตั้งแต่ก่อนเที่ยงคืนจนถึงรุ่งเช้า อยู่ค่อนไปทางท้องฟ้าด้านตะวันตกเมื่อใกล้รุ่ง")
        return _labelled(stem=f"ดาวเคราะห์วงนอกดวงหนึ่งมีมุมห่าง {angle}° ทาง{'ตะวันออก' if east else 'ตะวันตก'}ของดวงอาทิตย์ ผู้สังเกตจะเห็นได้อย่างไร",
                         correct=right, wrongs=tuple(o for o in options if o != right), topic=TOPIC_ELONG, hint=ELONG_HINT)


@question_type(
    "astro.elongation_application",
    display_name={"th": "คำนวณคาบซินอดิกและระยะห่างจากโลก"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_ELONG,
)
class ElongationApplication(QuestionType):
    """1/S = |1/P − 1|; distance at opposition a − 1 and at conjunction a + 1."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.55:
            period, synodic = rng.choice(SYNODIC)
            kind = "วงนอก" if period > 1 else "วงใน"
            return numeric(stem=f"ดาวเคราะห์{kind}ดวงหนึ่งมีคาบการโคจร {show(period)} ปี (1/S = |1/P − 1| เมื่อ S และ P เป็นปี) "
                                f"จะกลับมาอยู่ตำแหน่งเดิมเทียบกับดวงอาทิตย์และโลก (คาบซินอดิก) ทุกกี่ปี", answer=synodic,
                           wrongs=[Fraction(period) + 1, abs(Fraction(period) - 1) if Fraction(period) != 2 else 3, Fraction(synodic) * 2],
                           unit="ปี", topic=TOPIC_ELONG, hint="1/S = |1/P − 1|")
        a = Fraction(rng.choice((15, 52, 95, 192, 301, 25, 40, 30)), 10)
        opposition = rng.random() < 0.5
        return numeric(stem=f"ดาวเคราะห์วงนอกดวงหนึ่งอยู่ห่างดวงอาทิตย์ {show(a)} AU ขณะอยู่ตำแหน่ง{'ตรงข้ามดวงอาทิตย์' if opposition else 'ร่วมทิศกับดวงอาทิตย์'} "
                            f"จะอยู่ห่างจากโลกกี่ AU (โลกห่างดวงอาทิตย์ 1 AU และถือว่าวงโคจรเป็นวงกลมระนาบเดียวกัน)",
                       answer=a - 1 if opposition else a + 1, wrongs=[a + 1 if opposition else a - 1, a, a * 2], unit="AU", topic=TOPIC_ELONG,
                       hint="ตรงข้ามดวงอาทิตย์: a − 1 ร่วมทิศ: a + 1")
