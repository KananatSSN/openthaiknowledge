"""แรงไฟฟ้าตามกฎของคูลอมบ์

ฟิสิกส์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 3 ม.5/2

Sets moved here from: science_wave_f10.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f10 import (
    DISTANCES,
    MICRO,
    SUBJECT,
    UPPER_FIVE,
    K,
    _charge,
    _exact,
)

PROVENANCE = Provenance("original")


TOPIC_COULOMB = "แรงไฟฟ้าตามกฎของคูลอมบ์"


def _coulomb(q1: int, q2: int, r: Fraction) -> Fraction:
    return K * abs(q1 * q2) * MICRO * MICRO / (r * r)


@question_type(
    "phys.coulomb_force_foundation",
    display_name={"th": "แรงดึงดูดและแรงผลักระหว่างประจุ และการเปลี่ยนแปลงตามระยะห่าง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_COULOMB,
)
class CoulombForceFoundation(QuestionType):
    """Like repels, unlike attracts; F goes as q₁q₂ and as 1/r²."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            q1, q2 = rng.choice((-1, 1)) * rng.randint(1, 9), rng.choice((-1, 1)) * rng.randint(1, 9)
            same = (q1 > 0) == (q2 > 0)
            return _labelled(
                stem=f"จุดประจุ {_charge(q1)} และ {_charge(q2)} วางห่างกันระยะหนึ่ง แรงระหว่างประจุเป็นแรงแบบใด",
                correct="แรงผลัก" if same else "แรงดึงดูด",
                wrongs=("แรงดึงดูด" if same else "แรงผลัก", "ไม่มีแรงกระทำ", "แรงผลักสลับกับแรงดึงดูด"),
                topic=TOPIC_COULOMB, hint="ประจุชนิดเดียวกันผลักกัน ประจุต่างชนิดดูดกัน")
        change_q = rng.choice((1, 2, 3))
        change_r = rng.choice((Fraction(1, 2), 1, 2, 3))
        if change_q == 1 and change_r == 1:
            change_r = 2
        factor = Fraction(change_q) / (change_r * change_r)
        f = rng.randint(1, 20) * 9
        parts = []
        if change_q != 1:
            parts.append(f"ประจุหนึ่งเพิ่มเป็น {change_q} เท่า")
        if change_r != 1:
            parts.append("ระยะห่างลดลงครึ่งหนึ่ง" if change_r == Fraction(1, 2) else f"ระยะห่างเพิ่มเป็น {change_r} เท่า")
        return numeric(
            stem=f"จุดประจุสองจุดออกแรงต่อกัน {f} N ถ้า{' และ'.join(parts)} แรงจะเป็นเท่าใด",
            answer=f * factor, wrongs=[f * change_q / change_r, f * change_q * change_r * change_r, f],
            unit="N", topic=TOPIC_COULOMB, hint="F = kq₁q₂/r² แรงแปรผันตรงกับผลคูณของประจุ และผกผันกับระยะห่างกำลังสอง")


@question_type(
    "phys.coulomb_force_fluency",
    display_name={"th": "คำนวณแรงไฟฟ้าระหว่างจุดประจุสองจุดตามกฎของคูลอมบ์"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_COULOMB,
)
class CoulombForceFluency(QuestionType):
    """F = kq₁q₂/r² with charges in μC, and the distance back from a force."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        q1, q2, r = rng.choice([(a, b, r) for a in range(1, 11) for b in range(1, 11) for r in DISTANCES
                                if _exact(_coulomb(a, b, r)) and Fraction(1, 100) <= _coulomb(a, b, r) <= 10000])
        f = _coulomb(q1, q2, r)
        if rng.random() < 0.6:
            return numeric(
                stem=(f"จุดประจุ {q1} μC และ {q2} μC วางห่างกัน {show(r * 100)} cm แรงไฟฟ้าระหว่างประจุมีขนาดเท่าใด "
                      "(k = 9 × 10⁹ N·m²/C²)"),
                answer=f, wrongs=[f * r, f * r * r * 100, f / 2], unit="N", topic=TOPIC_COULOMB,
                hint="F = kq₁q₂/r² แปลง μC เป็น 10⁻⁶ C และ cm เป็น m ก่อน")
        return numeric(
            stem=(f"จุดประจุ {q1} μC และ {q2} μC ออกแรงต่อกัน {show(f)} N อยู่ห่างกันกี่เซนติเมตร "
                  "(k = 9 × 10⁹ N·m²/C²)"),
            answer=r * 100, wrongs=[r * r * 10000, r * 200, r * 50], unit="cm", topic=TOPIC_COULOMB,
            hint="r² = kq₁q₂/F แล้วถอดรากที่สอง")


@question_type(
    "phys.coulomb_force_application",
    display_name={"th": "แรงไฟฟ้าลัพธ์บนจุดประจุจากประจุหลายตัว"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_COULOMB,
)
class CoulombForceApplication(QuestionType):
    """Three charges in a line, or at a right angle: add the two forces as vectors."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            # A at 0, test charge at x = d1, B at d1 + d2; all positive, so the forces oppose.
            q, qa, qb, d1, d2 = rng.choice(
                [(q, a, b, d1, d2) for q in (1, 2) for a in range(1, 10) for b in range(1, 10)
                 for d1 in (Fraction(1, 10), Fraction(3, 10)) for d2 in (Fraction(1, 10), Fraction(3, 10))
                 if a * d2 * d2 != b * d1 * d1 and _exact(_coulomb(q, a, d1)) and _exact(_coulomb(q, b, d2))])
            fa, fb = _coulomb(q, qa, d1), _coulomb(q, qb, d2)
            return numeric(
                stem=(f"จุดประจุ A = +{qa} μC และ B = +{qb} μC อยู่บนแนวเส้นตรง วางประจุ +{q} μC ไว้ระหว่าง A กับ B "
                      f"ห่าง A {show(d1 * 100)} cm และห่าง B {show(d2 * 100)} cm แรงลัพธ์บนประจุนี้มีขนาดเท่าใด "
                      "(k = 9 × 10⁹ N·m²/C²)"),
                answer=abs(fa - fb), wrongs=[fa + fb, max(fa, fb), min(fa, fb)], unit="N", topic=TOPIC_COULOMB,
                hint="A และ B ผลักประจุบวกไปคนละทาง แรงลัพธ์จึงเป็นผลต่างของแรงทั้งสอง")
        f1, f2, total = rng.choice(((3, 4, 5), (6, 8, 10), (5, 12, 13), (9, 12, 15), (8, 15, 17)))
        scale = Fraction(rng.choice((1, 2, 5, 10)), rng.choice((1, 10)))
        return numeric(
            stem=(f"จุดประจุ Q ได้รับแรงไฟฟ้าจากประจุสองตัวซึ่งตั้งฉากกัน ขนาด {show(f1 * scale)} N และ "
                  f"{show(f2 * scale)} N แรงลัพธ์บน Q มีขนาดเท่าใด"),
            answer=total * scale, wrongs=[(f1 + f2) * scale, abs(f2 - f1) * scale, (f1 + f2) * scale / 2],
            unit="N", topic=TOPIC_COULOMB, hint="แรงเป็นเวกเตอร์ แรงสองแรงตั้งฉากกันรวมกันด้วย R = √(F₁² + F₂²)")
