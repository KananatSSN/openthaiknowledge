"""โครงสร้างและหน้าที่ของไต

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.5/19

Sets moved here from: science_wave_f64.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f64 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_KIDNEY = "โครงสร้างและหน้าที่ของไต"


KIDNEY_PARTS = (
    ("คอร์เทกซ์ของไต", "เนื้อไตชั้นนอก เป็นที่อยู่ของโกลเมอรูลัสและโบว์แมนแคปซูล"),
    ("เมดัลลาของไต", "เนื้อไตชั้นใน มีห่วงเฮนเลและท่อรวมเรียงเป็นกลุ่มรูปกรวย"),
    ("กรวยไต", "โพรงรวบรวมปัสสาวะก่อนส่งเข้าท่อไต"),
    ("ท่อไต", "ลำเลียงปัสสาวะจากไตไปยังกระเพาะปัสสาวะ"),
    ("กระเพาะปัสสาวะ", "เก็บปัสสาวะไว้ชั่วคราว"),
    ("ท่อปัสสาวะ", "ลำเลียงปัสสาวะออกนอกร่างกาย"),
    ("หน่วยไต (เนฟรอน)", "หน่วยที่ทำหน้าที่กรองเลือดและสร้างปัสสาวะ ไตแต่ละข้างมีประมาณหนึ่งล้านหน่วย"),
)


URINE_PATH = ("ท่อรวม", "กรวยไต", "ท่อไต", "กระเพาะปัสสาวะ", "ท่อปัสสาวะ")


KIDNEY_HINT = ("ไตมีคอร์เทกซ์ เมดัลลา และกรวยไต ปัสสาวะจากหน่วยไต → ท่อรวม → กรวยไต → ท่อไต → กระเพาะปัสสาวะ → ท่อปัสสาวะ "
               "ไตได้รับเลือดประมาณหนึ่งในห้าของเลือดที่หัวใจสูบฉีด")


@question_type(
    "biology.kidney_structure_foundation",
    display_name={"th": "ส่วนประกอบของไตและทางเดินปัสสาวะ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_KIDNEY,
)
class KidneyStructureFoundation(QuestionType):
    """Each part and its job, both ways."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        part, role = rng.choice(KIDNEY_PARTS)
        others = rng.sample([k for k in KIDNEY_PARTS if k[0] != part], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"{part}มีลักษณะหรือหน้าที่อย่างไร", correct=role, wrongs=tuple(k[1] for k in others), topic=TOPIC_KIDNEY,
                             hint=KIDNEY_HINT)
        return _labelled(stem=f"ส่วนใด{role}", correct=part, wrongs=tuple(k[0] for k in others), topic=TOPIC_KIDNEY, hint=KIDNEY_HINT)


@question_type(
    "biology.kidney_structure_fluency",
    display_name={"th": "เส้นทางของปัสสาวะออกจากร่างกาย"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_KIDNEY,
)
class KidneyStructureFluency(QuestionType):
    """Collecting duct to urethra, in order."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            i = rng.randrange(len(URINE_PATH) - 1)
            pool = [p for p in URINE_PATH if p not in (URINE_PATH[i], URINE_PATH[i + 1])] + ["เวนไต", "อาร์เทอรีไต"]
            return _labelled(stem=f"ปัสสาวะที่ผ่าน{URINE_PATH[i]}แล้วจะไปยังส่วนใดต่อไป", correct=URINE_PATH[i + 1],
                             wrongs=tuple(pool), topic=TOPIC_KIDNEY, hint=KIDNEY_HINT)
        start = rng.randrange(len(URINE_PATH) - 3)
        chunk = list(URINE_PATH[start:start + 4])
        wrongs: dict[str, None] = {}   # insertion-ordered: a set's order changes per process
        while len(wrongs) < 3:
            c = chunk[:]
            rng.shuffle(c)
            if c != chunk:
                wrongs[" → ".join(c)] = None
        return _labelled(stem="ข้อใดเรียงลำดับเส้นทางของปัสสาวะได้ถูกต้อง", correct=" → ".join(chunk), wrongs=tuple(wrongs),
                         topic=TOPIC_KIDNEY, hint=KIDNEY_HINT)


@question_type(
    "biology.kidney_structure_application",
    display_name={"th": "คำนวณเลือดที่ผ่านไตและจำนวนหน่วยไต"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_KIDNEY,
)
class KidneyStructureApplication(QuestionType):
    """A fifth or so of cardiac output goes through the kidneys."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            output = Fraction(rng.randrange(40, 71, 5), 10)
            share = rng.choice((20, 22, 24, 25))
            per_min = output * share / 100
            if (per_min * 100).denominator != 1:
                share = 20
                per_min = output * share / 100
            if rng.random() < 0.5:
                return numeric(stem=f"หัวใจสูบฉีดเลือด {show(output)} ลิตรต่อนาที ไตได้รับเลือดร้อยละ {share} ของปริมาณนี้ ไตได้รับเลือดกี่ลิตรต่อนาที",
                               answer=per_min, wrongs=[output * (100 - share) / 100, output, share], unit="ลิตรต่อนาที", topic=TOPIC_KIDNEY,
                               hint="เลือดที่ผ่านไต = ปริมาณเลือดที่หัวใจสูบฉีด × ร้อยละ ÷ 100")
            return numeric(stem=f"ไตได้รับเลือด {show(per_min)} ลิตรต่อนาที ในหนึ่งชั่วโมงเลือดผ่านไตกี่ลิตร", answer=per_min * 60,
                           wrongs=[per_min * 24, per_min * 3600, per_min * 60 * 24], unit="ลิตร", topic=TOPIC_KIDNEY,
                           hint="1 ชั่วโมง = 60 นาที")
        per_kidney = Fraction(rng.randrange(8, 16), 10)
        lost = rng.choice((0, 25, 50))
        total = per_kidney * 2 * (100 - lost) / 100
        return numeric(stem=f"ไตแต่ละข้างมีหน่วยไตประมาณ {show(per_kidney)} ล้านหน่วย"
                            + (f" ถ้าหน่วยไตทั้งหมดเสื่อมไปร้อยละ {lost}" if lost else "") + " จะมีหน่วยไตที่ทำงานได้รวมกี่ล้านหน่วย",
                       answer=total, wrongs=[per_kidney, per_kidney * 2 if lost else per_kidney * 4, total * 2], unit="ล้านหน่วย",
                       topic=TOPIC_KIDNEY, hint="คนมีไต 2 ข้าง หน่วยไตรวม = จำนวนต่อข้าง × 2 × (100 − ร้อยละที่เสื่อม) ÷ 100")
