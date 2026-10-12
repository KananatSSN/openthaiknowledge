"""สมมติฐานของพลังค์ แบบจำลองอะตอมของโบร์ และสเปกตรัมไฮโดรเจน

ฟิสิกส์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 4 ม.6/10

Sets moved here from: science_wave_f16.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f16 import SUBJECT, SUPERSCRIPT, UPPER_SIX, _sci

PROVENANCE = Provenance("original")


TOPIC_BOHR = "สมมติฐานของพลังค์ แบบจำลองอะตอมของโบร์ และสเปกตรัมไฮโดรเจน"


LEVELS = {1: Fraction(-136, 10), 2: Fraction(-34, 10), 3: Fraction(-151, 100), 4: Fraction(-85, 100), 5: Fraction(-54, 100)}


SERIES = {1: ("อนุกรมไลแมน", "รังสีอัลตราไวโอเลต"), 2: ("อนุกรมบัลเมอร์", "แสงที่มองเห็นได้"),
          3: ("อนุกรมพาสเชน", "รังสีอินฟราเรด")}


BOHR_FACTS = (
    ("สมมติฐานของพลังค์กล่าวว่าอย่างไร", "พลังงานของคลื่นแม่เหล็กไฟฟ้าถูกปล่อยหรือดูดกลืนเป็นก้อน ๆ ขนาด hf",
     ("พลังงานของแสงมีค่าต่อเนื่องได้ทุกค่า", "พลังงานของแสงขึ้นกับความเข้มเท่านั้น", "แสงไม่มีพลังงาน")),
    ("แบบจำลองอะตอมของโบร์กล่าวว่าอิเล็กตรอนในอะตอมไฮโดรเจนเป็นอย่างไร", "อยู่ได้เฉพาะในวงโคจรที่มีพลังงานบางค่า โดยไม่แผ่คลื่นขณะอยู่ในวงโคจรนั้น",
     ("โคจรได้ทุกรัศมีและแผ่คลื่นตลอดเวลา", "อยู่นิ่งในนิวเคลียส", "กระจายอยู่ทั่วอะตอมแบบเนื้อเดียว")),
    ("อะตอมไฮโดรเจนปล่อยแสงออกมาเมื่อใด", "เมื่ออิเล็กตรอนเปลี่ยนจากระดับพลังงานสูงลงสู่ระดับพลังงานต่ำ",
     ("เมื่ออิเล็กตรอนอยู่นิ่งในระดับพลังงานเดิม", "เมื่ออิเล็กตรอนขึ้นสู่ระดับพลังงานสูง", "เมื่อนิวเคลียสหมุน")),
    ("สเปกตรัมของแก๊สไฮโดรเจนเป็นเส้นสว่างแยกกัน เพราะเหตุใด", "ระดับพลังงานในอะตอมมีค่าเฉพาะ ผลต่างพลังงานจึงมีค่าเฉพาะ",
     ("แก๊สไฮโดรเจนดูดกลืนแสงทุกสี", "ปริซึมแยกแสงไม่สมบูรณ์", "อิเล็กตรอนมีพลังงานได้ทุกค่า")),
)


@question_type(
    "phys.bohr_spectrum_foundation",
    display_name={"th": "สมมติฐานของพลังค์และแบบจำลองอะตอมของโบร์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_BOHR,
)
class BohrSpectrumFoundation(QuestionType):
    """Quantised energy, allowed orbits, and E = hf."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.45:
            stem, correct, wrongs = rng.choice(BOHR_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_BOHR,
                             hint="พลังงานเป็นก้อน E = hf อิเล็กตรอนเปลี่ยนระดับแล้วปล่อยหรือดูดโฟตอนที่พลังงานเท่ากับผลต่างระดับ")
        k = rng.choice((1, 2, 3, 4, 5, 6, 7, 8, 9, Fraction(3, 2), Fraction(5, 2), Fraction(9, 2), Fraction(15, 2)))
        exponent = rng.choice((13, 14, 15, 16))
        energy = Fraction(66, 10) * k
        e_exp = exponent - 34
        if energy >= 10:
            energy, e_exp = energy / 10, e_exp + 1
        return _labelled(
            stem=f"คลื่นแม่เหล็กไฟฟ้าความถี่ {show(k)} × 10{str(exponent).translate(SUPERSCRIPT)} Hz มีพลังงานต่อโฟตอนเท่าใด (h = 6.6 × 10⁻³⁴ J·s)",
            correct=f"{_sci(energy, e_exp)} J",
            wrongs=(f"{_sci(energy, e_exp - 1)} J", f"{_sci(energy, e_exp + 1)} J", f"{_sci(energy, -e_exp)} J"),
            topic=TOPIC_BOHR, hint="E = hf คูณแมนทิสซาแล้วบวกเลขชี้กำลัง")


@question_type(
    "phys.bohr_spectrum_fluency",
    display_name={"th": "พลังงานโฟตอนจากการเปลี่ยนระดับพลังงานของอิเล็กตรอนในอะตอมไฮโดรเจน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_BOHR,
)
class BohrSpectrumFluency(QuestionType):
    """ΔE between the textbook's level energies, and the energy to ionise from a level."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        table = "(E₁ = −13.6 eV, E₂ = −3.4 eV, E₃ = −1.51 eV, E₄ = −0.85 eV, E₅ = −0.54 eV)"
        if rng.random() < 0.5:
            low, high = sorted(rng.sample(list(LEVELS), 2))
            de = LEVELS[high] - LEVELS[low]
            return numeric(
                stem=f"อิเล็กตรอนในอะตอมไฮโดรเจนเปลี่ยนจากระดับ n = {high} ลงสู่ n = {low} ปล่อยโฟตอนพลังงานกี่อิเล็กตรอนโวลต์ {table}",
                answer=de, wrongs=[-LEVELS[low] - LEVELS[high], -LEVELS[high], -LEVELS[low]], unit="eV", topic=TOPIC_BOHR,
                hint="พลังงานโฟตอน = E_สูง − E_ต่ำ (ระวังเครื่องหมายลบ)")
        if rng.random() < 0.5:
            low, high = sorted(rng.sample(list(LEVELS), 2))
            de = LEVELS[high] - LEVELS[low]
            return _labelled(
                stem=f"อิเล็กตรอนในอะตอมไฮโดรเจนที่ระดับ n = {low} ดูดกลืนโฟตอนพลังงาน {show(de)} eV จะขึ้นไปอยู่ที่ระดับใด {table}",
                correct=f"n = {high}", wrongs=tuple(f"n = {x}" for x in rng.sample([x for x in range(1, 7) if x != high], 3)),
                topic=TOPIC_BOHR, hint="ระดับใหม่มีพลังงาน E_เดิม + พลังงานโฟตอน เทียบกับตารางระดับพลังงาน")
        n = rng.choice(list(LEVELS))
        return numeric(
            stem=f"ต้องให้พลังงานอย่างน้อยกี่อิเล็กตรอนโวลต์ จึงทำให้อิเล็กตรอนที่ระดับ n = {n} ของอะตอมไฮโดรเจนหลุดออกจากอะตอม {table}",
            answer=-LEVELS[n], wrongs=[-LEVELS[1] if n != 1 else Fraction(34, 10), -LEVELS[n] * 2, Fraction(136, 10) - (-LEVELS[n]) if n != 1 else 10],
            unit="eV", topic=TOPIC_BOHR, hint="พลังงานไอออไนเซชันจากระดับ n = 0 − E_n")


@question_type(
    "phys.bohr_spectrum_application",
    display_name={"th": "อนุกรมเส้นสเปกตรัมของอะตอมไฮโดรเจน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_BOHR,
)
class BohrSpectrumApplication(QuestionType):
    """Which series a jump belongs to, and which part of the spectrum it lies in."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        low = rng.choice((1, 2, 3))
        high = rng.randint(low + 1, 7)
        name, band = SERIES[low]
        shape = rng.randrange(3)
        if shape == 2:
            top = rng.randint(2, 8)
            return numeric(
                stem=(f"อะตอมไฮโดรเจนจำนวนมากถูกกระตุ้นให้อิเล็กตรอนขึ้นไปถึงระดับ n = {top} "
                      "เมื่ออิเล็กตรอนเปลี่ยนลงสู่ระดับต่ำกว่าทุกแบบที่เป็นไปได้ จะเกิดเส้นสเปกตรัมได้มากที่สุดกี่เส้น"),
                answer=top * (top - 1) // 2, wrongs=[top - 1, top, top * (top - 1)], unit="เส้น", topic=TOPIC_BOHR,
                hint="นับทุกคู่ของระดับ n = 1 ถึง n: จำนวนเส้น = n(n − 1)/2")
        if shape == 0:
            return _labelled(
                stem=f"เส้นสเปกตรัมที่เกิดจากอิเล็กตรอนในอะตอมไฮโดรเจนเปลี่ยนจาก n = {high} ลงสู่ n = {low} อยู่ในอนุกรมใด",
                correct=name, wrongs=tuple(n for k, (n, _) in SERIES.items() if k != low) + ("อนุกรมแบร็กเกตต์",),
                topic=TOPIC_BOHR, hint="ลงสู่ n = 1 เป็นไลแมน ลงสู่ n = 2 เป็นบัลเมอร์ ลงสู่ n = 3 เป็นพาสเชน")
        return _labelled(
            stem=f"อิเล็กตรอนในอะตอมไฮโดรเจนเปลี่ยนจาก n = {high} ลงสู่ n = {low} ปล่อยคลื่นแม่เหล็กไฟฟ้าช่วงใด",
            correct=band, wrongs=tuple(b for k, (_, b) in SERIES.items() if k != low) + ("รังสีแกมมา",),
            topic=TOPIC_BOHR, hint="ลงสู่ n = 1 พลังงานมากเป็นอัลตราไวโอเลต ลงสู่ n = 2 เป็นแสงที่มองเห็น ลงสู่ n = 3 เป็นอินฟราเรด")
