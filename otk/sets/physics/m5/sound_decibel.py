"""ความเข้มเสียง ระดับความเข้มเสียง และการได้ยิน

ฟิสิกส์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 2 ม.5/6

Sets moved here from: science_wave_f8.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f8 import SUBJECT, UPPER_FIVE, _exact

PROVENANCE = Provenance("original")


TOPIC_LEVEL = "ความเข้มเสียง ระดับความเข้มเสียง และการได้ยิน"


LEVEL_FACTS = (
    ("หูของคนทั่วไปได้ยินเสียงในช่วงความถี่ใด", "ประมาณ 20 Hz ถึง 20,000 Hz",
     ("ประมาณ 0 Hz ถึง 200 Hz", "ประมาณ 2,000 Hz ถึง 200,000 Hz", "ทุกความถี่")),
    ("เสียงที่มีความถี่สูงกว่า 20,000 Hz เรียกว่าอะไร", "คลื่นเหนือเสียง (อัลตราซาวด์)",
     ("คลื่นใต้เสียง (อินฟราซาวด์)", "เสียงก้อง", "คลื่นกระแทก")),
    ("ระดับเสียง (เสียงสูง-ต่ำ) ขึ้นกับปริมาณใดของคลื่นเสียง", "ความถี่",
     ("แอมพลิจูด", "ความเข้มเสียง", "อัตราเร็ว")),
    ("คุณภาพเสียงที่ทำให้แยกเสียงไวโอลินกับเปียโนที่เล่นโน้ตเดียวกันได้ ขึ้นกับอะไร", "จำนวนและความเข้มของฮาร์มอนิกที่ผสมอยู่",
     ("ความถี่มูลฐานเท่านั้น", "อัตราเร็วเสียงในอากาศ", "ระยะห่างจากผู้ฟังเท่านั้น")),
    ("ความเข้มเสียงต่ำสุดที่หูคนปกติได้ยิน (ขีดเริ่มการได้ยิน) มีค่าประมาณเท่าใด", "10⁻¹² W/m²",
     ("1 W/m²", "10⁻⁶ W/m²", "10¹² W/m²")),
    ("การฟังเสียงที่มีระดับความเข้มเสียงเกิน 85 dB ติดต่อกันนาน ๆ มีผลอย่างไร", "อาจทำให้หูเสื่อมหรือสูญเสียการได้ยิน",
     ("ทำให้หูไวต่อเสียงมากขึ้น", "ไม่มีผลต่อการได้ยิน", "ทำให้ได้ยินความถี่สูงกว่า 20,000 Hz")),
)


SUPERSCRIPT = str.maketrans("-0123456789", "⁻⁰¹²³⁴⁵⁶⁷⁸⁹")


def _ten_to(n: int) -> str:
    return "1" if n == 0 else f"10{str(n).translate(SUPERSCRIPT)}"


@question_type(
    "phys.sound_decibel_foundation",
    display_name={"th": "การได้ยิน ระดับเสียง คุณภาพเสียง และมลพิษทางเสียง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_LEVEL,
)
class SoundDecibelFoundation(QuestionType):
    """What the ear hears and what each word for a sound's character means."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            stem, correct, wrongs = rng.choice(LEVEL_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_LEVEL,
                             hint="ระดับเสียงขึ้นกับความถี่ ความดังขึ้นกับความเข้มเสียง คุณภาพเสียงขึ้นกับฮาร์มอนิก")
        power = rng.choice((1, 2, 5, 10, 20, 50, 100))
        area = rng.choice([x for x in (1, 2, 4, 5, 10, 20, 50) if _exact(Fraction(power, x))])
        return numeric(
            stem=f"เสียงมีกำลัง {power} W ผ่านพื้นที่ตั้งฉาก {area} m² อย่างสม่ำเสมอ ความเข้มเสียงเท่าใด",
            answer=Fraction(power, area), wrongs=[power * area, Fraction(area, power), power],
            unit="W/m²", topic=TOPIC_LEVEL, hint="ความเข้มเสียง I = P ÷ A (กำลังต่อพื้นที่ที่ตั้งฉากกับทิศเสียง)")


@question_type(
    "phys.sound_decibel_fluency",
    display_name={"th": "คำนวณระดับความเข้มเสียงในหน่วยเดซิเบล"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_LEVEL,
)
class SoundDecibelFluency(QuestionType):
    """β = 10 log(I/I₀) with I a power of ten, both ways round."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        k = rng.randint(1, 12)
        exponent = k - 12
        level = 10 * k
        hint = "β = 10 log(I/I₀) โดย I₀ = 10⁻¹² W/m²: ความเข้มเพิ่ม 10 เท่า ระดับเพิ่ม 10 dB"
        shape = rng.random()
        if shape < 0.4:
            loud, quiet = sorted(rng.sample(range(-12, 1), 2), reverse=True)
            return numeric(
                stem=(f"เสียง ก มีความเข้ม {_ten_to(loud)} W/m² และเสียง ข มีความเข้ม {_ten_to(quiet)} W/m² "
                      "ระดับความเข้มเสียงของ ก มากกว่า ข กี่เดซิเบล"),
                answer=10 * (loud - quiet), wrongs=[loud - quiet, 10 ** min(loud - quiet, 3), 10 * (loud - quiet) + 10],
                unit="dB", topic=TOPIC_LEVEL, hint=hint)
        if shape < 0.7:
            return numeric(
                stem=f"เสียงมีความเข้ม {_ten_to(exponent)} W/m² มีระดับความเข้มเสียงกี่เดซิเบล (I₀ = 10⁻¹² W/m²)",
                answer=level, wrongs=[k, 10 * abs(exponent) if exponent else 120, level + 10], unit="dB",
                topic=TOPIC_LEVEL, hint=hint)
        return _labelled(
            stem=f"เสียงมีระดับความเข้มเสียง {level} dB มีความเข้มเสียงเท่าใด (I₀ = 10⁻¹² W/m²)",
            correct=f"{_ten_to(exponent)} W/m²",
            wrongs=tuple(dict.fromkeys(f"{_ten_to(e)} W/m²" for e in (-exponent, exponent - 1, exponent + 1, exponent - 2)
                                       if e != exponent))[:3],
            topic=TOPIC_LEVEL, hint=hint)


@question_type(
    "phys.sound_decibel_application",
    display_name={"th": "ระดับความเข้มเสียงเมื่อจำนวนแหล่งกำเนิดหรือระยะห่างเปลี่ยน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_LEVEL,
)
class SoundDecibelApplication(QuestionType):
    """More sources add decibels by the log; distance takes them away by the inverse square."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        base = rng.randint(4, 9) * 10
        shape = rng.randrange(3)
        if shape == 0:
            count, add = rng.choice(((10, 10), (100, 20), (1000, 30), (2, 3), (20, 13), (200, 23)))
            thing = rng.choice(("เครื่องจักร", "ลำโพง", "พัดลมอุตสาหกรรม", "รถจักรยานยนต์"))
            return numeric(
                stem=(f"{thing}หนึ่งเครื่องทำให้ผู้ฟังได้ยินเสียง {base} dB ถ้าเปิด{thing}แบบเดียวกัน {count:,} เครื่อง"
                      "พร้อมกัน ณ ตำแหน่งเดิม ระดับความเข้มเสียงเป็นเท่าใด (log 2 ≈ 0.3)"),
                answer=base + add, wrongs=[base * count, base + count, base * 2], unit="dB", topic=TOPIC_LEVEL,
                hint="ความเข้มรวมเป็น n เท่า ระดับเพิ่ม 10 log n dB เช่น 2 เท่าเพิ่ม 3 dB 10 เท่าเพิ่ม 10 dB")
        if shape == 1:
            ratio, drop = rng.choice(((10, 20), (100, 40), (2, 6), (20, 26)))
            r = rng.randint(1, 10)
            return numeric(
                stem=(f"ห่างจากแหล่งกำเนิดเสียง {r} m ได้ยินเสียง {base + 40} dB ถ้าถอยออกไปอยู่ห่าง {r * ratio:,} m "
                      "ระดับความเข้มเสียงเป็นเท่าใด (เสียงแผ่ออกทุกทิศเท่ากัน, log 2 ≈ 0.3)"),
                answer=base + 40 - drop, wrongs=[base + 40 - drop // 2, Fraction(base + 40, ratio), base + 40 - ratio],
                unit="dB", topic=TOPIC_LEVEL,
                hint="I แปรผกผันกับ r²: ระยะเพิ่ม n เท่า ความเข้มลดเป็น 1/n² เท่า ระดับลด 20 log n dB")
        louder = rng.randint(1, 4)
        return _labelled(
            stem=f"เสียง ก มีระดับความเข้มเสียงมากกว่าเสียง ข อยู่ {10 * louder} dB ความเข้มของเสียง ก เป็นกี่เท่าของเสียง ข",
            correct=f"{10 ** louder:,} เท่า",
            wrongs=tuple(f"{x:,} เท่า" for x in (10 * louder, 10 ** (louder + 1), louder) if x != 10 ** louder)[:3]
            if louder > 1 else ("20 เท่า", "100 เท่า", "2 เท่า"),
            topic=TOPIC_LEVEL, hint="ระดับต่างกัน 10 dB ความเข้มต่างกัน 10 เท่า ต่างกัน 10n dB ความเข้มต่างกัน 10ⁿ เท่า")
