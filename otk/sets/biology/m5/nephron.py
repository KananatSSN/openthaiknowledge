"""การทำงานของหน่วยไต

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.5/20

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


TOPIC_NEPHRON = "การทำงานของหน่วยไต"


STEPS = (
    ("โกลเมอรูลัสและโบว์แมนแคปซูล", "กรองน้ำและสารโมเลกุลเล็กออกจากเลือดด้วยแรงดันเลือด"),
    ("ท่อหน่วยไตส่วนต้น", "ดูดกลับกลูโคสและกรดอะมิโนเกือบทั้งหมด รวมทั้งน้ำและ Na⁺ ส่วนใหญ่"),
    ("ห่วงเฮนเล", "ดูดน้ำและเกลือกลับ ทำให้เนื้อเยื่อในเมดัลลามีความเข้มข้นสูง"),
    ("ท่อหน่วยไตส่วนท้าย", "หลั่ง H⁺ และ K⁺ ออกสู่ท่อ และดูดกลับ Na⁺ ภายใต้การควบคุมของฮอร์โมน"),
    ("ท่อรวม", "ดูดน้ำกลับมากหรือน้อยตามปริมาณฮอร์โมน ADH"),
)


SUBSTANCES = (
    ("กลูโคส", True, False), ("กรดอะมิโน", True, False), ("ยูเรีย", True, True), ("โซเดียมไอออน", True, True),
    ("โปรตีนในพลาสมา", False, False), ("เซลล์เม็ดเลือดแดง", False, False), ("น้ำ", True, True), ("เพลตเลต", False, False),
    ("ครีอะทินีน", True, True),
)


NEPHRON_HINT = ("โกลเมอรูลัสกรองสารโมเลกุลเล็ก โปรตีนและเซลล์เม็ดเลือดผ่านไม่ได้ ท่อส่วนต้นดูดกลับกลูโคสและกรดอะมิโนเกือบทั้งหมด "
                "ท่อส่วนท้ายหลั่ง H⁺ K⁺ ท่อรวมดูดน้ำกลับตาม ADH")


@question_type(
    "biology.nephron_foundation",
    display_name={"th": "หน้าที่ของส่วนต่าง ๆ ของหน่วยไต"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_NEPHRON,
)
class NephronFoundation(QuestionType):
    """Filtration, reabsorption and secretion, part by part."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        part, role = rng.choice(STEPS)
        others = rng.sample([s for s in STEPS if s[0] != part], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"{part}ทำหน้าที่อย่างไร", correct=role, wrongs=tuple(s[1] for s in others), topic=TOPIC_NEPHRON,
                             hint=NEPHRON_HINT)
        return _labelled(stem=f"ส่วนใดของหน่วยไต{role}", correct=part, wrongs=tuple(s[0] for s in others), topic=TOPIC_NEPHRON,
                         hint=NEPHRON_HINT)


@question_type(
    "biology.nephron_fluency",
    display_name={"th": "สารที่พบในของเหลวที่กรองได้และในปัสสาวะ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_NEPHRON,
)
class NephronFluency(QuestionType):
    """What passes the filter, and what stays in normal urine."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, filtered, in_urine = rng.choice(SUBSTANCES)
        options = ("พบทั้งในของเหลวที่กรองได้และในปัสสาวะ", "พบในของเหลวที่กรองได้ แต่ปกติไม่พบในปัสสาวะ",
                   "ไม่ผ่านการกรองจึงไม่พบทั้งสองแห่ง", "พบในปัสสาวะเท่านั้น แต่ไม่ผ่านการกรอง")
        right = options[0] if in_urine else (options[1] if filtered else options[2])
        if rng.random() < 0.35:
            want = rng.choice(((True, True), (True, False), (False, False)))
            label = {(True, True): "พบทั้งในของเหลวที่กรองได้และในปัสสาวะของคนปกติ",
                     (True, False): "ผ่านการกรองได้ แต่ปกติถูกดูดกลับจนไม่พบในปัสสาวะ",
                     (False, False): "ไม่ผ่านการกรองที่โกลเมอรูลัส"}[want]
            match = [n for n, f, u in SUBSTANCES if (f, u) == want]
            rest = [n for n, f, u in SUBSTANCES if (f, u) != want]
            return _labelled(stem=f"สารใด{label}", correct=rng.choice(match), wrongs=tuple(rest), topic=TOPIC_NEPHRON,
                             hint=NEPHRON_HINT)
        if rng.random() < 0.6:
            return _labelled(stem=f"ในคนปกติ {name}พบในของเหลวที่กรองได้ที่โบว์แมนแคปซูลและในปัสสาวะหรือไม่", correct=right,
                             wrongs=tuple(o for o in options if o != right), topic=TOPIC_NEPHRON, hint=NEPHRON_HINT)
        abnormal = (("กลูโคส", "ระดับน้ำตาลในเลือดสูงเกินกว่าท่อหน่วยไตจะดูดกลับได้หมด เช่น โรคเบาหวาน"),
                    ("โปรตีน", "โกลเมอรูลัสเสียหายจนโปรตีนรั่วผ่านการกรอง"),
                    ("เซลล์เม็ดเลือดแดง", "มีการบาดเจ็บหรืออักเสบในไตหรือทางเดินปัสสาวะ"))
        thing, why = rng.choice(abnormal)
        return _labelled(stem=f"ตรวจพบ{thing}ในปัสสาวะปริมาณมาก น่าจะเกิดจากสาเหตุใด", correct=why,
                         wrongs=tuple(w for t, w in abnormal if t != thing) + ("ดื่มน้ำมากเกินไปเพียงอย่างเดียว",), topic=TOPIC_NEPHRON,
                         hint=NEPHRON_HINT)


@question_type(
    "biology.nephron_application",
    display_name={"th": "คำนวณการกรองและการดูดกลับของหน่วยไต"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_NEPHRON,
)
class NephronApplication(QuestionType):
    """Filtrate per day, the share taken back, and how far urea is concentrated."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.35:
            rate = rng.choice((100, 110, 120, 125))
            per_day = Fraction(rate * 60 * 24, 1000)
            return numeric(stem=f"ไตกรองของเหลวได้ {rate} mL ต่อนาที ในหนึ่งวันกรองได้กี่ลิตร", answer=per_day,
                           wrongs=[Fraction(rate * 60, 1000), rate * 24, per_day * 1000], unit="ลิตร", topic=TOPIC_NEPHRON,
                           hint="ลิตรต่อวัน = mL ต่อนาที × 60 × 24 ÷ 1,000")
        if roll < 0.7:
            filtrate = rng.choice((150, 160, 180, 200))
            reabsorbed = rng.choice((98, 99, Fraction(995, 10)))
            urine = Fraction(filtrate) * (100 - reabsorbed) / 100
            if (urine * 100).denominator != 1:
                reabsorbed = 99
                urine = Fraction(filtrate) * (100 - reabsorbed) / 100
            if rng.random() < 0.5:
                return numeric(stem=f"ไตกรองของเหลวได้ {filtrate} ลิตรต่อวัน และดูดกลับร้อยละ {show(reabsorbed)} ปัสสาวะที่ขับออกมีกี่ลิตรต่อวัน",
                               answer=urine, wrongs=[filtrate * reabsorbed / 100, filtrate - reabsorbed, urine * 10], unit="ลิตร",
                               topic=TOPIC_NEPHRON, hint="ปัสสาวะ = ของเหลวที่กรองได้ × (100 − ร้อยละที่ดูดกลับ) ÷ 100")
            return numeric(stem=f"ไตกรองของเหลวได้ {filtrate} ลิตรต่อวัน ขับปัสสาวะ {show(urine)} ลิตรต่อวัน ดูดกลับร้อยละเท่าใด",
                           answer=reabsorbed, wrongs=[100 - reabsorbed, urine, 100 - urine], unit="%", topic=TOPIC_NEPHRON,
                           hint="ร้อยละที่ดูดกลับ = (ของเหลวที่กรอง − ปัสสาวะ) × 100 ÷ ของเหลวที่กรอง")
        plasma = Fraction(rng.choice((2, 3, 4, 5)), 10)
        times = rng.choice((20, 40, 50, 60, 65, 70))
        urine = plasma * times
        return numeric(stem=f"พลาสมามียูเรีย {show(plasma)} g ต่อลิตร ปัสสาวะมียูเรีย {show(urine)} g ต่อลิตร ยูเรียในปัสสาวะเข้มข้นเป็นกี่เท่าของในพลาสมา",
                       answer=times, wrongs=[urine - plasma, times * 2, times + 1], unit="เท่า", topic=TOPIC_NEPHRON,
                       hint="ความเข้มข้นในปัสสาวะ ÷ ความเข้มข้นในพลาสมา เพิ่มขึ้นเพราะน้ำถูกดูดกลับ")
