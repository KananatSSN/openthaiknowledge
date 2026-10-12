"""ปฏิกิริยาผันกลับได้และภาวะสมดุล

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.5/7

Sets moved here from: science_wave_f33.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, show
from otk.sets._support.science_wave_f33 import SUBJECT, UPPER_FIVE, approach_table

PROVENANCE = Provenance("original")


TOPIC_REVERSIBLE = "ปฏิกิริยาผันกลับได้และภาวะสมดุล"


EQUILIBRIUM_FACTS = (
    ("ข้อใดกล่าวถึงระบบที่อยู่ในภาวะสมดุลได้ถูกต้อง",
     "อัตราการเกิดปฏิกิริยาไปข้างหน้าเท่ากับอัตราย้อนกลับ และความเข้มข้นของสารคงที่",
     ("ปฏิกิริยาหยุดเกิดแล้วทั้งสองทิศทาง", "ความเข้มข้นของสารตั้งต้นเท่ากับความเข้มข้นของผลิตภัณฑ์เสมอ",
      "เกิดเฉพาะปฏิกิริยาย้อนกลับ")),
    ("ภาวะสมดุลเคมีเรียกว่าสมดุลไดนามิกเพราะเหตุใด",
     "ปฏิกิริยาไปข้างหน้าและย้อนกลับยังเกิดด้วยอัตราเท่ากัน",
     ("ความเข้มข้นของสารเปลี่ยนตลอดเวลาแม้ระบบจะถึงสมดุลแล้ว", "ปฏิกิริยาหยุดนิ่งทั้งหมด ไม่มีการเปลี่ยนแปลงใด ๆ อีก", "มีการเติมสารเข้าระบบตลอดเวลาเพื่อรักษาสมดุล")),
    ("ระบบที่จะเข้าสู่ภาวะสมดุลได้ต้องเป็นระบบแบบใด", "ระบบปิดที่ไม่มีสารเข้าหรือออก",
     ("ระบบเปิดที่แก๊สหนีออกได้", "ระบบที่ต้องให้ความร้อนตลอดเวลา", "ระบบที่มีสารตั้งต้นเพียงชนิดเดียว")),
    ("เติม I₂ ที่มีไอโซโทปกัมมันตรังสีลงในระบบ I₂(s) ⇌ I₂(g) ที่สมดุล ต่อมาพบกัมมันตภาพรังสีทั้งในของแข็งและแก๊ส แสดงว่าอะไร",
     "ที่ภาวะสมดุลยังมีการระเหิดและการควบแน่นเกิดขึ้นตลอดเวลา",
     ("ระบบยังไม่ถึงภาวะสมดุล ไอของ I₂ จึงยังเกิดเพิ่มขึ้นเรื่อย ๆ", "I₂ ทำปฏิกิริยากับภาชนะจนเกิดสารใหม่ที่เป็นไอ", "ที่ภาวะสมดุลไม่มีการเปลี่ยนแปลงระดับโมเลกุล")),
)


# (system, what is seen going one way, what is seen coming back)
REVERSIBLE_CASES = (
    ("CuSO₄·5H₂O(s) ⇌ CuSO₄(s) + 5H₂O(g)", "เผาผลึกสีฟ้าได้ผงสีขาว", "หยดน้ำลงบนผงสีขาวได้สีฟ้ากลับมา"),
    ("N₂O₄(g) ⇌ 2NO₂(g)", "ให้ความร้อน แก๊สมีสีน้ำตาลเข้มขึ้น", "แช่หลอดในน้ำเย็น สีน้ำตาลจางลง"),
    ("NH₄Cl(s) ⇌ NH₃(g) + HCl(g)", "เผา NH₄Cl ในหลอด ของแข็งหายไป", "มีของแข็งสีขาวเกิดที่ปากหลอดซึ่งเย็นกว่า"),
    ("[Co(H₂O)₆]²⁺(aq) + 4Cl⁻(aq) ⇌ [CoCl₄]²⁻(aq) + 6H₂O(l)", "เติม HCl เข้มข้น สีชมพูเปลี่ยนเป็นสีน้ำเงิน",
     "เติมน้ำ กลับเป็นสีชมพู"),
    ("Fe³⁺(aq) + SCN⁻(aq) ⇌ FeSCN²⁺(aq)", "เติม Fe³⁺ สีแดงเข้มขึ้น", "เติมสารที่ดึง Fe³⁺ ออก สีแดงจางลง"),
)


IRREVERSIBLE = ("เผากระดาษจนเป็นเถ้าและแก๊ส แล้วปล่อยให้เย็นก็ได้กระดาษคืนไม่ได้", "ทอดไข่จนสุก แล้วปล่อยให้เย็นลง ไข่ก็ยังคงสุกอยู่ไม่กลับเป็นไข่ดิบ", "เผาแมกนีเซียมในอากาศได้ผงสีขาวที่เปลี่ยนกลับเป็นโลหะไม่ได้",
                "ใส่ Mg ลงในกรด HCl ในภาชนะเปิด แก๊สที่เกิดขึ้นลอยออกไปจากภาชนะ", "ต้มน้ำตาลจนไหม้เป็นสีดำ แล้วปล่อยให้เย็นก็ยังเป็นสีดำ")


def equilibrium_time(times, a, b):
    last = (a[-1], b[-1])
    return next(t for t, x, y in zip(times, a, b) if (x, y) == last)


@question_type(
    "chem.reversible_equilibrium_foundation",
    display_name={"th": "ลักษณะของภาวะสมดุลเคมี"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_REVERSIBLE,
)
class ReversibleEquilibriumFoundation(QuestionType):
    """Both directions keep going at equal rates, in a closed system."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = "ภาวะสมดุล: ระบบปิด อัตราไปข้างหน้า = อัตราย้อนกลับ ความเข้มข้นคงที่ (แต่ไม่จำเป็นต้องเท่ากัน)"
        if rng.random() < 0.5:
            stem, right, wrongs = rng.choice(EQUILIBRIUM_FACTS)
            return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_REVERSIBLE, hint=hint)
        system, forward, back = rng.choice(REVERSIBLE_CASES)
        return _labelled(stem="การเปลี่ยนแปลงใดแสดงว่าปฏิกิริยาผันกลับได้", correct=f"{forward} แล้ว{back}",
                         wrongs=tuple(IRREVERSIBLE), topic=TOPIC_REVERSIBLE,
                         hint="ปฏิกิริยาผันกลับได้เปลี่ยนไปแล้วเปลี่ยนกลับเป็นสารเดิมได้เมื่อเปลี่ยนภาวะ")


@question_type(
    "chem.reversible_equilibrium_fluency",
    display_name={"th": "อธิบายการเปลี่ยนแปลงในปฏิกิริยาผันกลับได้"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_REVERSIBLE,
)
class ReversibleEquilibriumFluency(QuestionType):
    """Match what is seen to the direction of the reversible reaction."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        system, forward, back = rng.choice(REVERSIBLE_CASES)
        if rng.random() < 0.5:
            want_forward = rng.random() < 0.5
            right = forward if want_forward else back
            others = [x for case in REVERSIBLE_CASES if case[0] != system for x in case[1:]]
            return _labelled(stem=f"ระบบ {system} ถ้าทำให้ปฏิกิริยาเกิด{'ไปข้างหน้า' if want_forward else 'ย้อนกลับ'}มากขึ้น "
                                  "จะสังเกตเห็นอะไร",
                             correct=right, wrongs=(back if want_forward else forward, *rng.sample(others, 2)),
                             topic=TOPIC_REVERSIBLE,
                             hint="ไปข้างหน้าได้สารทางขวามากขึ้น ย้อนกลับได้สารทางซ้ายมากขึ้น ดูว่าสารใดมีสีหรือสถานะอย่างไร")
        seen, direction = rng.choice(((forward, "ไปข้างหน้า (ซ้ายไปขวา)"), (back, "ย้อนกลับ (ขวาไปซ้าย)")))
        other = "ย้อนกลับ (ขวาไปซ้าย)" if direction.startswith("ไป") else "ไปข้างหน้า (ซ้ายไปขวา)"
        return _labelled(stem=f"ระบบ {system} เมื่อ{seen} แสดงว่าปฏิกิริยาเกิดในทิศทางใดมากกว่า", correct=direction,
                         wrongs=(other, "ไม่เกิดปฏิกิริยาทั้งสองทิศทาง", "เกิดทั้งสองทิศทางด้วยอัตราเท่ากันพอดี"),
                         topic=TOPIC_REVERSIBLE,
                         hint="ดูว่าสิ่งที่สังเกตเห็นคือสารทางซ้ายหรือทางขวาของสมการที่เพิ่มขึ้น")


@question_type(
    "chem.reversible_equilibrium_application",
    display_name={"th": "ระบุภาวะสมดุลจากข้อมูลความเข้มข้น"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_REVERSIBLE,
)
class ReversibleEquilibriumApplication(QuestionType):
    """Equilibrium starts when every concentration stops changing, not when they are equal."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        times, a, b = approach_table(rng)
        stop = equilibrium_time(times, a, b)
        rows = "; ".join(f"{t} s: [A] = {show(x)}, [B] = {show(y)}" for t, x, y in zip(times, a, b))
        labels = [f"{t} s" for t in times]
        right = f"{stop} s"
        crossing = [f"{t} s" for t, x, y in zip(times, a, b) if x == y]
        pool = [ell for ell in labels if ell != right]
        wrongs = crossing[:1] + [ell for ell in pool if ell not in crossing]
        return _labelled(stem=f"ปฏิกิริยา A ⇌ B ในภาชนะปิด วัดความเข้มข้น (mol/dm³) ได้ {rows} ระบบเข้าสู่ภาวะสมดุลครั้งแรกที่เวลาใด",
                         correct=right, wrongs=tuple(dict.fromkeys(w for w in wrongs if w != right))[:3],
                         topic=TOPIC_REVERSIBLE,
                         hint="ภาวะสมดุลเริ่มเมื่อความเข้มข้นของทุกสารหยุดเปลี่ยน ไม่ใช่เมื่อความเข้มข้นเท่ากัน")
