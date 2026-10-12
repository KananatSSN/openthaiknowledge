"""การเคลื่อนที่แบบฮาร์มอนิกอย่างง่าย

ฟิสิกส์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 2 ม.5/1

Sets moved here from: science_wave_f7.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f7 import SUBJECT, UPPER_FIVE, _exact

PROVENANCE = Provenance("original")


TOPIC_SHM = "การเคลื่อนที่แบบฮาร์มอนิกอย่างง่าย"


def _pi(x) -> str:
    """A multiple of π, written the way a textbook answer is."""
    return "π s" if x == 1 else f"{show(x)}π s"


SHM_FACTS = (
    ("แรงดึงกลับในการเคลื่อนที่แบบฮาร์มอนิกอย่างง่ายมีลักษณะใด", "แปรผันตรงกับการกระจัดจากตำแหน่งสมดุล และมีทิศเข้าหาตำแหน่งสมดุล",
     ("มีขนาดคงตัวทุกตำแหน่ง", "แปรผันตรงกับความเร็ว และมีทิศเดียวกับความเร็ว", "เป็นศูนย์ที่ปลายทั้งสองข้าง")),
    ("ขณะวัตถุที่สั่นแบบฮาร์มอนิกอย่างง่ายผ่านตำแหน่งสมดุล ข้อใดถูกต้อง", "อัตราเร็วมากที่สุด และความเร่งเป็นศูนย์",
     ("อัตราเร็วเป็นศูนย์ และความเร่งมากที่สุด", "ทั้งอัตราเร็วและความเร่งมากที่สุด", "ทั้งอัตราเร็วและความเร่งเป็นศูนย์")),
    ("ขณะวัตถุที่สั่นแบบฮาร์มอนิกอย่างง่ายอยู่ที่ตำแหน่งการกระจัดมากที่สุด ข้อใดถูกต้อง", "อัตราเร็วเป็นศูนย์ และความเร่งมากที่สุด",
     ("อัตราเร็วมากที่สุด และความเร่งเป็นศูนย์", "ทั้งอัตราเร็วและความเร่งเป็นศูนย์", "ทั้งอัตราเร็วและความเร่งมากที่สุด")),
    ("คาบของลูกตุ้มอย่างง่ายที่แกว่งเป็นมุมเล็ก ๆ ขึ้นกับปริมาณใด", "ความยาวเชือกและความเร่งโน้มถ่วง",
     ("มวลของลูกตุ้ม", "แอมพลิจูดของการแกว่ง", "มวลของลูกตุ้มและแอมพลิจูด")),
    ("คาบของมวลติดปลายสปริงขึ้นกับปริมาณใด", "มวลของวัตถุและค่านิจของสปริง",
     ("แอมพลิจูดของการสั่น", "ความเร่งโน้มถ่วงเท่านั้น", "ความยาวของสปริงเท่านั้น")),
)


@question_type(
    "phys.shm_foundation",
    display_name={"th": "ลักษณะของการเคลื่อนที่แบบฮาร์มอนิกอย่างง่าย คาบ ความถี่ และแอมพลิจูด"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SHM,
)
class ShmFoundation(QuestionType):
    """Where speed and acceleration peak, and period, frequency and amplitude from a count."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        hint = "คาบ = เวลาต่อหนึ่งรอบ ความถี่ = จำนวนรอบต่อวินาที แอมพลิจูด = การกระจัดมากที่สุดจากตำแหน่งสมดุล"
        if shape == 0:
            stem, correct, wrongs = rng.choice(SHM_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_SHM,
                             hint="แรงดึงกลับ F = −kx: ที่ตำแหน่งสมดุลแรงเป็นศูนย์ ที่ปลายแรงมากที่สุด")
        if shape == 1:
            n = rng.choice((5, 10, 20, 25, 50))
            t = rng.choice([x for x in (2, 4, 5, 8, 10, 20, 40) if _exact(Fraction(x, n)) and _exact(Fraction(n, x))])
            what = rng.choice(("มวลติดปลายสปริง", "ลูกตุ้มอย่างง่าย"))
            period = rng.random() < 0.5
            return numeric(
                stem=f"{what}สั่นครบ {n} รอบในเวลา {t} s {'คาบ' if period else 'ความถี่'}ของการสั่นเท่าใด",
                answer=Fraction(t, n) if period else Fraction(n, t),
                wrongs=[Fraction(n, t), n * t, Fraction(t, 2 * n)] if period else [Fraction(t, n), n * t, Fraction(n, 2 * t)],
                unit="s" if period else "Hz", topic=TOPIC_SHM, hint=hint)
        span = rng.randint(2, 30) * 2
        return numeric(
            stem=f"มวลติดปลายสปริงสั่นกลับไปกลับมาระหว่างสองตำแหน่งซึ่งห่างกัน {span} cm แอมพลิจูดของการสั่นเท่าใด",
            answer=Fraction(span, 2), wrongs=[span, span * 2, Fraction(span, 4)], unit="cm", topic=TOPIC_SHM, hint=hint)


@question_type(
    "phys.shm_fluency",
    display_name={"th": "คำนวณความถี่เชิงมุม อัตราเร็วสูงสุด และความเร่งสูงสุดของการสั่น"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SHM,
)
class ShmFluency(QuestionType):
    """ω = √(k/m), v_max = Aω, a_max = Aω², and T = 2π/ω."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        w = rng.randint(2, 20)
        m = Fraction(rng.choice((1, 2, 4, 5, 10, 20, 50)), 10)
        k = m * w * w
        shape = rng.randrange(4)
        given = f"มวล {show(m)} kg ติดปลายสปริงค่านิจ {show(k)} N/m สั่นแบบฮาร์มอนิกอย่างง่าย"
        if shape == 0:
            return numeric(stem=f"{given} ความถี่เชิงมุมเท่าใด", answer=w,
                           wrongs=[w * w, 2 * w, Fraction(w, 2)], unit="rad/s", topic=TOPIC_SHM,
                           hint="ω = √(k/m)")
        amp = Fraction(rng.randint(1, 20), 100)
        if shape == 1:
            return numeric(stem=f"{given} ด้วยแอมพลิจูด {show(amp * 100)} cm อัตราเร็วสูงสุดเท่าใด",
                           answer=amp * w, wrongs=[amp * w * w, amp * 100 * w, amp * w / 2], unit="m/s",
                           topic=TOPIC_SHM, hint="ω = √(k/m) แล้ว v สูงสุด = Aω (A เป็นเมตร)")
        if shape == 2:
            return numeric(stem=f"{given} ด้วยแอมพลิจูด {show(amp * 100)} cm ความเร่งสูงสุดเท่าใด",
                           answer=amp * w * w, wrongs=[amp * w, amp * 100 * w * w, amp * w * w / 2], unit="m/s²",
                           topic=TOPIC_SHM, hint="ω = √(k/m) แล้ว a สูงสุด = Aω² (A เป็นเมตร)")
        # Only ω that leave 2/ω exact in front of π.
        w = rng.choice((2, 4, 5, 8, 10, 20))
        given = f"มวล {show(m)} kg ติดปลายสปริงค่านิจ {show(m * w * w)} N/m สั่นแบบฮาร์มอนิกอย่างง่าย"
        period = Fraction(2, w)
        return _labelled(stem=f"{given} คาบของการสั่นเท่าใด", correct=_pi(period),
                         wrongs=tuple(dict.fromkeys(_pi(x) for x in (Fraction(1, w), Fraction(w, 2), Fraction(4, w),
                                                                    Fraction(2 * w)) if x != period))[:3],
                         topic=TOPIC_SHM, hint="T = 2π/ω = 2π√(m/k)")


@question_type(
    "phys.shm_application",
    display_name={"th": "คาบของลูกตุ้มอย่างง่ายและมวลติดปลายสปริงเมื่อเปลี่ยนเงื่อนไข"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SHM,
)
class ShmApplication(QuestionType):
    """T = 2π√(l/g) and T = 2π√(m/k) with π² ≈ 10, and how T scales."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        if shape == 0:
            # With π² ≈ 10 and g = 10, T² = 4l.
            t = rng.choice((Fraction(1), Fraction(6, 5), Fraction(2), Fraction(12, 5), Fraction(3),
                            Fraction(4), Fraction(4, 5), Fraction(8, 5), Fraction(14, 5)))
            if rng.random() < 0.5:
                return numeric(
                    stem=f"ลูกตุ้มอย่างง่ายยาว {show(t * t / 4)} m แกว่งเป็นมุมเล็ก ๆ มีคาบเท่าใด (g = 10 m/s², π² ≈ 10)",
                    answer=t, wrongs=[t * t, 2 * t, t / 2], unit="s", topic=TOPIC_SHM,
                    hint="T = 2π√(l/g) เมื่อ π² ≈ g จะได้ T² = 4l")
            return numeric(
                stem=f"ต้องการลูกตุ้มอย่างง่ายที่มีคาบ {show(t)} s ต้องใช้เชือกยาวเท่าใด (g = 10 m/s², π² ≈ 10)",
                answer=t * t / 4, wrongs=[t * t, t / 4, t / 2], unit="m", topic=TOPIC_SHM,
                hint="T = 2π√(l/g) เมื่อ π² ≈ g จะได้ l = T²/4")
        if shape == 1:
            # T² = 40m/k with π² ≈ 10.
            m, k, t = rng.choice([(Fraction(mm, 10), kk, t) for mm in (1, 2, 4, 5, 10, 20) for kk in (4, 10, 16, 40, 90, 160)
                                  for t in (Fraction(1, 5), Fraction(2, 5), Fraction(1, 2), 1, Fraction(3, 2), 2)
                                  if 40 * Fraction(mm, 10) / kk == Fraction(t) ** 2])
            return numeric(
                stem=f"มวล {show(m)} kg ติดปลายสปริงค่านิจ {k} N/m สั่นแบบฮาร์มอนิกอย่างง่าย มีคาบเท่าใด (π² ≈ 10)",
                answer=t, wrongs=[Fraction(t) ** 2, 2 * t, Fraction(t) / 2], unit="s", topic=TOPIC_SHM,
                hint="T = 2π√(m/k) ดังนั้น T² = 4π²m/k = 40m/k")
        what, quantity = rng.choice((("ลูกตุ้มอย่างง่าย", "ความยาวเชือก"), ("มวลติดปลายสปริง", "มวล"),
                                     ("มวลติดปลายสปริง", "ค่านิจของสปริง"), ("ลูกตุ้มอย่างง่าย", "ความเร่งโน้มถ่วง")))
        grows = quantity in ("ความยาวเชือก", "มวล")
        # T goes as the square root of the change, or of its reciprocal; only exact results.
        factor, root = rng.choice([(f, r) for f, r in ((4, 2), (16, 4), (25, 5), (Fraction(1, 4), Fraction(1, 2)),
                                                       (Fraction(1, 16), Fraction(1, 4)), (9, 3))
                                   if _exact(r if grows else 1 / Fraction(r))])
        answer = Fraction(root) if grows else 1 / Fraction(root)
        change = f"เพิ่มเป็น {show(factor)} เท่า" if factor > 1 else f"ลดเหลือ 1/{int(1 / factor)} เท่า"
        return numeric(
            stem=f"{what}มีคาบ T ถ้า{quantity}{change} โดยปริมาณอื่นคงเดิม คาบใหม่เป็นกี่เท่าของ T",
            answer=answer, wrongs=[factor, 1 / Fraction(answer), Fraction(answer) * 2], unit="เท่า", topic=TOPIC_SHM,
            hint="T = 2π√(l/g) และ T = 2π√(m/k): คาบแปรผันตามรากที่สองของ l หรือ m และผกผันกับรากที่สองของ g หรือ k")
