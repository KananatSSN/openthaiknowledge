"""การหายใจระดับเซลล์

ชีวะ · ม.4 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 1 ม.4/17

Sets moved here from: science_wave_f48.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f48 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_RESP = "การหายใจระดับเซลล์"


STAGES = (
    ("ไกลโคลิซิส", "ไซโทซอล", "กลูโคสถูกสลายเป็นกรดไพรูวิก 2 โมเลกุล ได้ ATP สุทธิ 2 โมเลกุล และ NADH", False),
    ("การสร้างแอซีทิลโคเอนไซม์เอ", "เมทริกซ์ของไมโทคอนเดรีย", "กรดไพรูวิกเปลี่ยนเป็นแอซีทิลโคเอนไซม์เอ และปล่อย CO₂", True),
    ("วัฏจักรเครบส์", "เมทริกซ์ของไมโทคอนเดรีย", "ปล่อย CO₂ และได้ NADH FADH₂ และ ATP", True),
    ("การถ่ายทอดอิเล็กตรอน", "เยื่อชั้นในของไมโทคอนเดรีย", "ได้ ATP มากที่สุด โดยมี O₂ เป็นตัวรับอิเล็กตรอนตัวสุดท้ายได้น้ำ", True),
)


FERMENT = (
    ("การหมักแอลกอฮอล์", "ยีสต์ที่หมักน้ำผลไม้หรือแป้งขนมปัง", "เอทานอลและ CO₂"),
    ("การหมักกรดแล็กติก", "เซลล์กล้ามเนื้อที่ขาดออกซิเจนและแบคทีเรียกรดแล็กติก", "กรดแล็กติก"),
)


RESP_FACTS = (
    ("การหายใจแบบใช้ออกซิเจนต่างจากการหมักอย่างไร", "ใช้ O₂ เป็นตัวรับอิเล็กตรอนสุดท้าย และได้ ATP มากกว่ามาก",
     ("ได้ ATP น้อยกว่าการหมัก เพราะไม่ใช้ O₂ เป็นตัวรับอิเล็กตรอน", "ไม่มีไกลโคลิซิส จึงเริ่มจากวัฏจักรเครบส์ทันที",
      "เกิดในไซโทซอลทั้งหมดโดยไม่ใช้ไมโทคอนเดรีย", "ใช้ CO₂ เป็นตัวรับอิเล็กตรอนสุดท้าย และได้ ATP น้อยกว่า")),
    ("ขั้นตอนใดเกิดได้ทั้งในภาวะที่มีและไม่มีออกซิเจน", "ไกลโคลิซิสในไซโทซอล",
     ("วัฏจักรเครบส์ในไมโทคอนเดรีย", "การถ่ายทอดอิเล็กตรอน", "การสร้างแอซีทิลโคเอนไซม์เอ", "การสังเคราะห์ด้วยแสง")),
    ("เมื่อวิ่งเร็วจนขาดออกซิเจน กล้ามเนื้อล้าเพราะสะสมสารใด", "กรดแล็กติก", ("เอทานอล", "กลูโคส", "ไกลโคเจน", "แก๊ส CO₂")),
    ("การทำขนมปังให้ฟูอาศัยผลิตภัณฑ์ใดของยีสต์", "แก๊ส CO₂ จากการหมัก", ("กรดแล็กติกจากการหมัก", "แก๊ส O₂ จากการหายใจ", "น้ำตาลกลูโคสที่เหลือ", "เอทานอลจากการหมัก")),
    ("การหมักทำให้เซลล์ยังได้ ATP ต่อไปได้เพราะเหตุใด", "เปลี่ยน NADH กลับเป็น NAD⁺ ให้ไกลโคลิซิสดำเนินต่อไปได้",
     ("สร้าง ATP จากการถ่ายทอดอิเล็กตรอน โดยไม่ต้องใช้ O₂", "ใช้ O₂ จากอากาศเปลี่ยน NADH เป็นน้ำแทนไกลโคลิซิส",
      "เปลี่ยนกรดแล็กติกเป็นกลูโคส ให้ไกลโคลิซิสใช้ซ้ำได้", "เปลี่ยน NAD⁺ เป็น NADH ให้เซลล์เก็บพลังงานไว้ใช้")),
)


@question_type(
    "biology.respiration_foundation",
    display_name={"th": "ขั้นตอนและตำแหน่งของการหายใจระดับเซลล์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_RESP,
)
class RespirationFoundation(QuestionType):
    """Glycolysis in the cytosol; the rest inside the mitochondrion."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stage, place, event, _ = rng.choice(STAGES)
        others = [s for s in STAGES if s[0] != stage]
        if rng.random() < 0.3:
            asks = (("ปล่อย CO₂", {"การสร้างแอซีทิลโคเอนไซม์เอ", "วัฏจักรเครบส์"}), ("ใช้ O₂ โดยตรง", {"การถ่ายทอดอิเล็กตรอน"}),
                    ("เกิดนอกไมโทคอนเดรีย", {"ไกลโคลิซิส"}), ("ได้ ATP มากที่สุด", {"การถ่ายทอดอิเล็กตรอน"}),
                    ("ได้กรดไพรูวิก", {"ไกลโคลิซิส"}))
            ask, answers = rng.choice(asks)
            right = rng.choice(sorted(answers))
            return _labelled(stem=f"ขั้นตอนใดของการหายใจระดับเซลล์{ask}", correct=right,
                             wrongs=tuple(s[0] for s in STAGES if s[0] not in answers)[:3] if len(STAGES) - len(answers) >= 3
                             else tuple(s[0] for s in STAGES if s[0] not in answers) + ("การหมักแอลกอฮอล์",),
                             topic=TOPIC_RESP, hint="ไกลโคลิซิสในไซโทซอลได้ไพรูวิก เครบส์ปล่อย CO₂ การถ่ายทอดอิเล็กตรอนใช้ O₂ และได้ ATP มากที่สุด")
        kind = rng.randrange(3)
        hint = "ไกลโคลิซิสในไซโทซอล วัฏจักรเครบส์ในเมทริกซ์ การถ่ายทอดอิเล็กตรอนที่เยื่อชั้นในของไมโทคอนเดรีย"
        if kind == 0:
            places = sorted(({s[1] for s in STAGES} | {"เยื่อชั้นนอกของไมโทคอนเดรีย", "คลอโรพลาสต์"}) - {place})
            return _labelled(stem=f"{stage}เกิดขึ้นที่ใด", correct=place, wrongs=tuple(places), topic=TOPIC_RESP,
                             hint=hint)
        if kind == 1:
            return _labelled(stem=f"ข้อใดเกิดขึ้นในขั้น{stage}", correct=event, wrongs=tuple(s[2] for s in others),
                             topic=TOPIC_RESP, hint=hint)
        return _labelled(stem=f"\"{event}\" เป็นขั้นตอนใดของการหายใจระดับเซลล์", correct=stage,
                         wrongs=tuple(s[0] for s in others), topic=TOPIC_RESP, hint=hint)


@question_type(
    "biology.respiration_fluency",
    display_name={"th": "เปรียบเทียบการหายใจแบบใช้ออกซิเจนและการหมัก"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_RESP,
)
class RespirationFluency(QuestionType):
    """Without oxygen, only glycolysis runs and pyruvate becomes lactate or ethanol."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.45:
            kind, who, products = rng.choice(FERMENT)
            other = [f for f in FERMENT if f[0] != kind][0]
            pool = ["CO₂ และน้ำ", "กลูโคสและ O₂", "กรดไพรูวิกและ O₂"]
            if rng.random() < 0.5:
                return _labelled(stem=f"{kind}ใน{who}ได้ผลิตภัณฑ์ใด", correct=products,
                                 wrongs=(other[2], *rng.sample(pool, 2)), topic=TOPIC_RESP,
                                 hint="ยีสต์หมักได้เอทานอลและ CO₂ กล้ามเนื้อหมักได้กรดแล็กติก")
            return _labelled(stem=f"การหมักที่ได้{products}เกิดในสิ่งมีชีวิตใด", correct=who,
                             wrongs=(other[1], "เซลล์ใบพืชที่ได้รับแสงเต็มที่", "เซลล์ประสาทที่มีออกซิเจนเพียงพอ"),
                             topic=TOPIC_RESP, hint="ยีสต์หมักได้เอทานอลและ CO₂ กล้ามเนื้อหมักได้กรดแล็กติก")
        stem, right, wrongs = rng.choice(RESP_FACTS)
        # The row's own wrong readings only: another row's answer is off topic here.
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_RESP,
                         hint="การหายใจแบบใช้ O₂ ได้ ATP มาก การหมักได้ ATP จากไกลโคลิซิสเพียง 2 โมเลกุลต่อกลูโคส")


@question_type(
    "biology.respiration_application",
    display_name={"th": "ปริมาณสารในการหายใจระดับเซลล์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_RESP,
)
class RespirationApplication(QuestionType):
    """C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O; fermentation gives 2 ATP, 2 ethanol and 2 CO₂ per glucose."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        glucose = rng.choice((Fraction(1, 2), 1, Fraction(3, 2), 2, 3, 4, 5, 10))
        cases = (
            ("สลายกลูโคสแบบใช้ออกซิเจนอย่างสมบูรณ์", "ต้องใช้ O₂", 6), ("สลายกลูโคสแบบใช้ออกซิเจนอย่างสมบูรณ์", "ได้ CO₂", 6),
            ("สลายกลูโคสแบบใช้ออกซิเจนอย่างสมบูรณ์", "ได้น้ำ", 6), ("ยีสต์หมักกลูโคส", "ได้เอทานอล", 2),
            ("ยีสต์หมักกลูโคส", "ได้ CO₂", 2), ("ยีสต์หมักกลูโคส", "ได้ ATP สุทธิ", 2),
            ("กล้ามเนื้อหมักกลูโคสเป็นกรดแล็กติก", "ได้กรดแล็กติก", 2), ("ไกลโคลิซิสสลายกลูโคส", "ได้กรดไพรูวิก", 2),
        )
        process, what, per = rng.choice(cases)
        return numeric(stem=f"{process} {show(glucose)} โมล {what}กี่โมล", answer=glucose * per,
                       wrongs=[glucose * (8 - per) if per != 4 else glucose * 3, glucose, glucose * per * 2], unit="โมล",
                       topic=TOPIC_RESP,
                       hint="แบบใช้ O₂: C₆H₁₂O₆ + 6O₂ → 6CO₂ + 6H₂O หมักแอลกอฮอล์: กลูโคส → 2 เอทานอล + 2 CO₂ ได้ 2 ATP")
