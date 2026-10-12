"""ทวิภาวะของคลื่นและอนุภาคและความยาวคลื่นเดอบรอยล์

ฟิสิกส์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 4 ม.6/12

Sets moved here from: science_wave_f17.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f17 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_BROGLIE = "ทวิภาวะของคลื่นและอนุภาคและความยาวคลื่นเดอบรอยล์"


def _exact(x) -> bool:
    return (Fraction(x) * 100).denominator == 1


BROGLIE_FACTS = (
    ("ทวิภาวะของคลื่นและอนุภาคหมายความว่าอย่างไร", "ทั้งแสงและอนุภาคแสดงสมบัติได้ทั้งแบบคลื่นและแบบอนุภาค",
     ("แสงเป็นคลื่นเท่านั้น อนุภาคเป็นอนุภาคเท่านั้น", "อนุภาคเปลี่ยนเป็นคลื่นเมื่อหยุดนิ่ง", "คลื่นทุกชนิดมีมวล")),
    ("การทดลองใดยืนยันว่าอิเล็กตรอนมีสมบัติของคลื่น", "การเลี้ยวเบนของอิเล็กตรอนผ่านผลึก",
     ("ปรากฏการณ์โฟโตอิเล็กทริก", "การหักเหของแสงผ่านปริซึม", "การสลายตัวของนิวเคลียส")),
    ("อนุภาคที่มีโมเมนตัมมากขึ้นมีความยาวคลื่นเดอบรอยล์เป็นอย่างไร", "สั้นลง",
     ("ยาวขึ้น", "เท่าเดิม", "เป็นศูนย์")),
    ("กล้องจุลทรรศน์อิเล็กตรอนเห็นรายละเอียดได้ละเอียดกว่ากล้องแสง เพราะเหตุใด", "ความยาวคลื่นของอิเล็กตรอนสั้นกว่าแสงมาก",
     ("อิเล็กตรอนมีประจุบวก", "อิเล็กตรอนเคลื่อนที่ช้ากว่าแสง", "อิเล็กตรอนไม่มีมวล")),
    ("เหตุใดเราจึงไม่เห็นสมบัติคลื่นของลูกบอลที่ขว้าง", "ความยาวคลื่นเดอบรอยล์สั้นมากเมื่อเทียบกับขนาดของสิ่งรอบตัว",
     ("ลูกบอลไม่มีโมเมนตัม", "ลูกบอลมีความยาวคลื่นยาวมาก", "ลูกบอลไม่มีมวล")),
)


SUPERSCRIPT = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")


def _normalise(x: Fraction) -> tuple[Fraction, int]:
    """x × 10⁻³⁴ written as a mantissa in [1, 10) and its power of ten."""
    exponent = -34
    while x >= 10:
        x, exponent = x / 10, exponent + 1
    while x < 1:
        x, exponent = x * 10, exponent - 1
    return x, exponent


def _other_mantissas(m_g: int, v: int, taken: set[str]) -> tuple[str, ...]:
    """Slips that change the mantissa too, so the answer is not the choice all
    the power-of-ten slips agree on: h written as the answer, and h/(mv²)."""
    out = []
    for value in (Fraction(66, 10), Fraction(66, 10) / (Fraction(m_g, 1000) * v * v)):
        mant, exp = _normalise(value)
        shown = f"{show(mant)} × 10{str(exp).translate(SUPERSCRIPT)} m"
        if shown not in taken and shown not in out:
            out.append(shown)
    return tuple(out)


# (grams, m/s, mantissa, exponent) for balls whose wavelength has a short mantissa.
BALLS = tuple((m, v, *_normalise(Fraction(66, 10) / (Fraction(m, 1000) * v)))
              for m in (10, 20, 30, 50, 60, 100, 110, 200, 300, 330, 600) for v in (1, 2, 3, 5, 10, 11, 20, 22, 30, 33)
              if _exact(_normalise(Fraction(66, 10) / (Fraction(m, 1000) * v))[0]))


@question_type(
    "phys.de_broglie_foundation",
    display_name={"th": "ทวิภาวะของคลื่นและอนุภาค"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_BROGLIE,
)
class DeBroglieFoundation(QuestionType):
    """What duality claims, what shows it, and λ = h/p for a stated momentum."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            stem, correct, wrongs = rng.choice(BROGLIE_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_BROGLIE,
                             hint="λ = h/p อนุภาคเล็กที่โมเมนตัมน้อยจึงแสดงสมบัติคลื่นชัด")
        # Momenta whose mantissa divides 6.6 exactly.
        p = rng.choice([Fraction(k, 10) for k in range(1, 100) if _exact(Fraction(66, k))])
        exponent = rng.choice((-24, -25))
        lam = Fraction(66, 10) / p * (10 if exponent == -25 else 1)
        return numeric(
            stem=(f"อนุภาคมีโมเมนตัม {show(p)} × 10{str(exponent).translate(SUPERSCRIPT)} kg·m/s มีความยาวคลื่นเดอบรอยล์เท่าใด "
                  "(h = 6.6 × 10⁻³⁴ J·s ตอบในหน่วย × 10⁻¹⁰ m)"),
            answer=lam, wrongs=[p / Fraction(66, 10), lam * 10 if exponent == -24 else lam / 10, lam * 2],
            unit="× 10⁻¹⁰ m", topic=TOPIC_BROGLIE, hint="λ = h/p: 6.6 ÷ แมนทิสซาของ p แล้วเลขชี้กำลัง −34 − (−24) = −10")


@question_type(
    "phys.de_broglie_fluency",
    display_name={"th": "คำนวณความยาวคลื่นเดอบรอยล์จากมวลและความเร็ว"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_BROGLIE,
)
class DeBroglieFluency(QuestionType):
    """λ = h/(mv) for a thrown ball and for a slow particle."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        m_g, v, mant, exponent = rng.choice(BALLS)
        label = lambda e: f"{show(mant)} × 10{str(e).translate(SUPERSCRIPT)} m"
        return _labelled(
            stem=f"ลูกบอลมวล {m_g} g เคลื่อนที่ด้วยความเร็ว {v} m/s มีความยาวคลื่นเดอบรอยล์เท่าใด (h = 6.6 × 10⁻³⁴ J·s)",
            correct=label(exponent), wrongs=(label(exponent + 3), label(exponent - 1), label(-exponent), *_other_mantissas(m_g, v, {label(e) for e in (exponent, exponent + 3, exponent - 1, -exponent)})),
            topic=TOPIC_BROGLIE, hint="λ = h/(mv) มวลเป็นกิโลกรัม ได้ความยาวคลื่นสั้นมากจนสังเกตไม่ได้")


@question_type(
    "phys.de_broglie_application",
    display_name={"th": "ความยาวคลื่นเดอบรอยล์เมื่อความเร็วหรือมวลของอนุภาคเปลี่ยน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_BROGLIE,
)
class DeBroglieApplication(QuestionType):
    """λ ∝ 1/(mv): change the speed or compare two particles."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            factor = rng.choice((2, 4, 5, Fraction(1, 2), 10))
            change = f"เพิ่มเป็น {factor} เท่า" if factor > 1 else "ลดลงครึ่งหนึ่ง"
            lam = rng.choice([Fraction(x, 10) for x in range(1, 41) if _exact(Fraction(x, 10) / factor)])
            return numeric(
                stem=f"อิเล็กตรอนมีความยาวคลื่นเดอบรอยล์ {show(lam)} nm ถ้าอัตราเร็ว{change} (ไม่คิดผลสัมพัทธภาพ) ความยาวคลื่นใหม่เท่าใด",
                answer=lam / factor, wrongs=[lam * factor, lam, lam / factor / factor], unit="nm", topic=TOPIC_BROGLIE,
                hint="λ = h/(mv) แปรผกผันกับอัตราเร็ว")
        ratio = rng.choice((2, 4, 1836))
        pair = {2: ("ดิวเทอรอน", "โปรตอน"), 4: ("อนุภาคแอลฟา", "โปรตอน"), 1836: ("โปรตอน", "อิเล็กตรอน")}[ratio]
        return numeric(
            stem=(f"{pair[0]}มีมวลประมาณ {ratio:,} เท่าของ{pair[1]} ถ้าทั้งสองมีอัตราเร็วเท่ากัน ความยาวคลื่นเดอบรอยล์ของ"
                  f"{pair[1]}เป็นกี่เท่าของ{pair[0]}"),
            answer=ratio, wrongs=[Fraction(1, ratio) if ratio < 100 else 1, ratio * 2, 1 if ratio < 100 else 43],
            unit="เท่า", topic=TOPIC_BROGLIE, hint="อัตราเร็วเท่ากัน λ แปรผกผันกับมวล อนุภาคเบากว่ามีความยาวคลื่นยาวกว่า")
