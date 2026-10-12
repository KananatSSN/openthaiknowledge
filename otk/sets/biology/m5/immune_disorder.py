"""ความผิดปกติของระบบภูมิคุ้มกัน

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.5/17

Sets moved here from: science_wave_f63.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f63 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_DISORDER = "ความผิดปกติของระบบภูมิคุ้มกัน"


DISORDERS = (
    ("โรคเอดส์", "เชื้อ HIV ทำลายเซลล์ T ผู้ช่วย ภูมิคุ้มกันจึงบกพร่องและติดเชื้อฉวยโอกาสได้ง่าย", "ภูมิคุ้มกันบกพร่อง"),
    ("ภูมิแพ้", "ร่างกายตอบสนองต่อสารที่ปกติไม่เป็นอันตรายมากเกินไป เซลล์หลั่งฮีสตามีน", "ภูมิคุ้มกันไวเกิน"),
    ("โรคลูปัส (SLE)", "ร่างกายสร้างแอนติบอดีต่อต้านเนื้อเยื่อของตนเองหลายระบบ", "ภูมิต้านทานต่อเนื้อเยื่อตนเอง"),
    ("โรคข้ออักเสบรูมาทอยด์", "ระบบภูมิคุ้มกันทำลายเยื่อบุข้อของตนเอง", "ภูมิต้านทานต่อเนื้อเยื่อตนเอง"),
    ("เบาหวานชนิดที่ 1", "ระบบภูมิคุ้มกันทำลายเซลล์ที่สร้างอินซูลินในตับอ่อน", "ภูมิต้านทานต่อเนื้อเยื่อตนเอง"),
)


DISORDER_HINT = ("เอดส์เกิดจาก HIV ทำลายเซลล์ T ผู้ช่วย ภูมิแพ้คือการตอบสนองมากเกินต่อสารก่อภูมิแพ้ "
                 "ภูมิต้านทานต่อเนื้อเยื่อตนเองคือร่างกายทำลายเซลล์ของตนเอง")


@question_type(
    "biology.immune_disorder_foundation",
    display_name={"th": "สาเหตุของเอดส์ ภูมิแพ้ และภูมิต้านทานต่อเนื้อเยื่อตนเอง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_DISORDER,
)
class ImmuneDisorderFoundation(QuestionType):
    """What goes wrong in each disorder."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, cause, _ = rng.choice(DISORDERS)
        others = rng.sample([d for d in DISORDERS if d[0] != name], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"{name}เกิดจากอะไร", correct=cause, wrongs=tuple(d[1] for d in others), topic=TOPIC_DISORDER,
                             hint=DISORDER_HINT)
        return _labelled(stem=f"\"{cause}\" เป็นสาเหตุของโรคใด", correct=name, wrongs=tuple(d[0] for d in others), topic=TOPIC_DISORDER,
                         hint=DISORDER_HINT)


@question_type(
    "biology.immune_disorder_fluency",
    display_name={"th": "จำแนกประเภทความผิดปกติของระบบภูมิคุ้มกัน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_DISORDER,
)
class ImmuneDisorderFluency(QuestionType):
    """Deficiency, over-reaction, or attack on self; and how HIV spreads."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            name, _, kind = rng.choice(DISORDERS)
            kinds = ("ภูมิคุ้มกันบกพร่อง", "ภูมิคุ้มกันไวเกิน", "ภูมิต้านทานต่อเนื้อเยื่อตนเอง", "ภูมิคุ้มกันรับมา")
            return _labelled(stem=f"{name}จัดเป็นความผิดปกติของระบบภูมิคุ้มกันแบบใด", correct=kind,
                             wrongs=tuple(k for k in kinds if k != kind), topic=TOPIC_DISORDER, hint=DISORDER_HINT)
        spreads = ("การรับเลือดที่มีเชื้อ HIV", "การใช้เข็มฉีดยาร่วมกับผู้ติดเชื้อ", "การมีเพศสัมพันธ์โดยไม่ป้องกันกับผู้ติดเชื้อ",
                   "จากแม่ที่ติดเชื้อสู่ลูกระหว่างคลอด")
        safe = ("การจับมือหรือกอดทักทายกับผู้ติดเชื้อ", "การใช้ห้องน้ำและโถส้วมร่วมกับผู้ติดเชื้อ",
                "การถูกยุงที่เพิ่งกัดผู้ติดเชื้อมากัดต่อ", "การรับประทานอาหารร่วมโต๊ะกับผู้ติดเชื้อ",
                "การว่ายน้ำในสระเดียวกันกับผู้ติดเชื้อ")
        if rng.random() < 0.5:
            return _labelled(stem="ข้อใดเป็นทางติดต่อของเชื้อ HIV", correct=rng.choice(spreads), wrongs=tuple(safe),
                             topic=TOPIC_DISORDER, hint="HIV ติดต่อทางเลือด เพศสัมพันธ์ และจากแม่สู่ลูก ไม่ติดต่อจากการสัมผัสทั่วไปหรือยุง")
        return _labelled(stem="ข้อใดไม่ใช่ทางติดต่อของเชื้อ HIV", correct=rng.choice(safe), wrongs=tuple(spreads),
                         topic=TOPIC_DISORDER, hint="HIV ติดต่อทางเลือด เพศสัมพันธ์ และจากแม่สู่ลูก ไม่ติดต่อจากการสัมผัสทั่วไปหรือยุง")


@question_type(
    "biology.immune_disorder_application",
    display_name={"th": "วิเคราะห์ผลตรวจและการรักษาความผิดปกติของระบบภูมิคุ้มกัน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_DISORDER,
)
class ImmuneDisorderApplication(QuestionType):
    """CD4 counts, and why each treatment works."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            before = rng.randrange(400, 1001, 50)
            drop = rng.choice((10, 20, 25, 40, 50, 60, 75))
            after = Fraction(before * (100 - drop), 100)
            if rng.random() < 0.5:
                return numeric(stem=f"ผู้ติดเชื้อ HIV มีเซลล์ T ผู้ช่วย (CD4) {before} เซลล์ต่อ mm³ ต่อมาลดลงร้อยละ {drop} เหลือกี่เซลล์ต่อ mm³",
                               answer=after, wrongs=[Fraction(before * drop, 100), before - drop, before], unit="เซลล์ต่อ mm³",
                               topic=TOPIC_DISORDER, hint="ที่เหลือ = ค่าเดิม × (100 − ร้อยละที่ลด) ÷ 100")
            return numeric(stem=f"เซลล์ T ผู้ช่วย (CD4) ลดจาก {before} เหลือ {show(after)} เซลล์ต่อ mm³ ลดลงร้อยละเท่าใด", answer=drop,
                           wrongs=[100 - drop, before - after, Fraction(after * 100, before)], unit="%", topic=TOPIC_DISORDER,
                           hint="ร้อยละที่ลด = (ค่าเดิม − ค่าใหม่) × 100 ÷ ค่าเดิม")
        cases = (("ยาแอนติฮีสตามีนช่วยบรรเทาอาการภูมิแพ้ได้อย่างไร", "ยับยั้งการออกฤทธิ์ของฮีสตามีนที่ทำให้เกิดอาการแพ้",
                  ("ฆ่าเชื้อแบคทีเรียที่เป็นสาเหตุของอาการแพ้", "เพิ่มจำนวนเซลล์ T ผู้ช่วยให้ต่อต้านสารก่อภูมิแพ้",
                   "สร้างแอนติบอดีต่อสารก่อภูมิแพ้ให้ร่างกายโดยตรง")),
                 ("ผู้ป่วยโรคภูมิต้านทานต่อเนื้อเยื่อตนเองมักได้รับยากดภูมิคุ้มกันเพราะเหตุใด", "ลดการทำลายเนื้อเยื่อของตนเองโดยระบบภูมิคุ้มกัน",
                  ("เพิ่มการสร้างแอนติบอดีให้ต่อต้านเนื้อเยื่อได้ดีขึ้น", "ฆ่าเชื้อโรคที่เป็นสาเหตุของการทำลายเนื้อเยื่อ",
                   "กระตุ้นให้เกิดภูมิแพ้แทนการทำลายเนื้อเยื่อตนเอง")),
                 ("เหตุใดผู้ป่วยเอดส์จึงป่วยด้วยโรคติดเชื้อฉวยโอกาสได้ง่าย", "เซลล์ T ผู้ช่วยลดลง จึงกระตุ้นลิมโฟไซต์อื่นได้น้อย",
                  ("มีแอนติบอดีมากเกินไปจนทำลายเซลล์ของตนเอง", "ร่างกายทำลายเนื้อเยื่อของตนเองจนติดเชื้อง่าย",
                   "มีฮีสตามีนมากเกินไป จึงอักเสบและติดเชื้อง่าย")))
        stem, right, wrongs = rng.choice(cases)
        return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_DISORDER, hint=DISORDER_HINT)
