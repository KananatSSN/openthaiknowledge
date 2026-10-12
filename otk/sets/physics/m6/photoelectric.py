"""ปรากฏการณ์โฟโตอิเล็กทริก

ฟิสิกส์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 4 ม.6/11

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


TOPIC_PHOTO = "ปรากฏการณ์โฟโตอิเล็กทริก"


HC = 1240


# Wavelengths (nm) at which 1,240/λ is exact.
LIGHTS = (124, 155, 160, 200, 248, 250, 310, 400, 496, 500, 620)


METALS = (("ซีเซียม", Fraction(21, 10)), ("โพแทสเซียม", Fraction(23, 10)), ("โซเดียม", Fraction(5, 2)),
          ("แคลเซียม", Fraction(29, 10)), ("สังกะสี", Fraction(43, 10)), ("ทองแดง", Fraction(47, 10)))


PHOTO_FACTS = (
    ("ในปรากฏการณ์โฟโตอิเล็กทริก พลังงานจลน์สูงสุดของโฟโตอิเล็กตรอนขึ้นกับอะไร", "ความถี่ของแสงและชนิดของโลหะ",
     ("ความเข้มของแสงเท่านั้น", "เวลาที่ฉายแสง", "พื้นที่ของแผ่นโลหะ")),
    ("เพิ่มความเข้มของแสงที่ทำให้เกิดโฟโตอิเล็กตรอนอยู่แล้ว จะเกิดผลใด", "จำนวนโฟโตอิเล็กตรอนเพิ่มขึ้น แต่พลังงานจลน์สูงสุดเท่าเดิม",
     ("พลังงานจลน์สูงสุดเพิ่มขึ้น", "ไม่มีโฟโตอิเล็กตรอนหลุดออกมา", "ความถี่ขีดเริ่มลดลง")),
    ("ฉายแสงที่มีความถี่ต่ำกว่าความถี่ขีดเริ่มลงบนโลหะ แม้แสงจะเข้มมาก จะเกิดอะไรขึ้น", "ไม่มีโฟโตอิเล็กตรอนหลุดออกมา",
     ("มีโฟโตอิเล็กตรอนหลุดออกมาช้า ๆ", "โฟโตอิเล็กตรอนมีพลังงานจลน์สูงมาก", "โลหะเปลี่ยนเป็นประจุลบ")),
    ("ฟังก์ชันงานของโลหะคืออะไร", "พลังงานน้อยที่สุดที่ทำให้อิเล็กตรอนหลุดออกจากผิวโลหะ",
     ("พลังงานจลน์ของโฟโตอิเล็กตรอน", "พลังงานของโฟตอนทุกตัว", "ความต่างศักย์ระหว่างขั้วไฟฟ้า")),
    ("ปรากฏการณ์โฟโตอิเล็กทริกสนับสนุนแนวคิดใดเกี่ยวกับแสง", "แสงประกอบด้วยก้อนพลังงานที่เรียกว่าโฟตอน",
     ("แสงเป็นคลื่นต่อเนื่องเท่านั้น", "แสงเป็นคลื่นเสียง", "แสงไม่มีพลังงาน")),
)


@question_type(
    "phys.photoelectric_foundation",
    display_name={"th": "ปรากฏการณ์โฟโตอิเล็กทริกและพลังงานจลน์สูงสุดของโฟโตอิเล็กตรอน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_PHOTO,
)
class PhotoelectricFoundation(QuestionType):
    """What frequency and intensity each change, and Eₖ = hf − W in electron volts."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.45:
            stem, correct, wrongs = rng.choice(PHOTO_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_PHOTO,
                             hint="โฟตอนหนึ่งตัวให้พลังงานแก่อิเล็กตรอนหนึ่งตัว Eₖ สูงสุด = hf − W ความเข้มเพิ่มแค่จำนวนโฟตอน")
        energy = Fraction(rng.randint(25, 80), 10)
        metal, work = rng.choice([m for m in METALS if m[1] < energy])
        return numeric(
            stem=f"โฟตอนพลังงาน {show(energy)} eV ตกกระทบผิว{metal}ซึ่งมีฟังก์ชันงาน {show(work)} eV โฟโตอิเล็กตรอนมีพลังงานจลน์สูงสุดเท่าใด",
            answer=energy - work, wrongs=[energy + work, energy, work], unit="eV", topic=TOPIC_PHOTO,
            hint="Eₖ สูงสุด = พลังงานโฟตอน − ฟังก์ชันงาน")


@question_type(
    "phys.photoelectric_fluency",
    display_name={"th": "คำนวณพลังงานโฟตอน พลังงานจลน์ และความต่างศักย์หยุดยั้ง"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_PHOTO,
)
class PhotoelectricFluency(QuestionType):
    """E = hc/λ with hc = 1,240 eV·nm, then Eₖ and the stopping voltage."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        wl = rng.choice(LIGHTS)
        energy = Fraction(HC, wl)
        if rng.random() < 0.4:
            return numeric(stem=f"แสงความยาวคลื่น {wl} nm มีพลังงานโฟตอนกี่อิเล็กตรอนโวลต์ (hc = 1,240 eV·nm)",
                           answer=energy, wrongs=[energy * 10, Fraction(wl, HC) * 10, energy / 2], unit="eV",
                           topic=TOPIC_PHOTO, hint="E = hc/λ = 1,240/λ(nm) eV")
        options = [m for m in METALS if m[1] < energy]
        if not options:
            wl = rng.choice((124, 155, 160, 200, 248))
            energy = Fraction(HC, wl)
            options = [m for m in METALS if m[1] < energy]
        metal, work = rng.choice(options)
        return numeric(
            stem=(f"ฉายแสงความยาวคลื่น {wl} nm ลงบน{metal} (ฟังก์ชันงาน {show(work)} eV) ความต่างศักย์หยุดยั้งกี่โวลต์ "
                  "(hc = 1,240 eV·nm)"),
            answer=energy - work, wrongs=[energy, energy + work, work], unit="V", topic=TOPIC_PHOTO,
            hint="หาพลังงานโฟตอน 1,240/λ ก่อน แล้ว eV_s = Eₖ สูงสุด = hf − W")


@question_type(
    "phys.photoelectric_application",
    display_name={"th": "ความยาวคลื่นขีดเริ่มและการเลือกโลหะให้เกิดโฟโตอิเล็กตรอน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_PHOTO,
)
class PhotoelectricApplication(QuestionType):
    """λ₀ = hc/W, and which metals a given light can free electrons from."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            work = rng.choice((2, Fraction(5, 2), Fraction(31, 10), 4, 5, Fraction(62, 10), 8))
            return numeric(
                stem=f"โลหะมีฟังก์ชันงาน {show(work)} eV แสงที่ทำให้เกิดโฟโตอิเล็กตรอนได้ต้องมีความยาวคลื่นไม่เกินกี่นาโนเมตร (hc = 1,240 eV·nm)",
                answer=HC / work, wrongs=[HC * work, HC / work / 2, HC / work * 2], unit="nm", topic=TOPIC_PHOTO,
                hint="ความยาวคลื่นขีดเริ่ม λ₀ = hc/W แสงที่ยาวกว่านี้มีพลังงานไม่พอ")
        wl = rng.choice(LIGHTS)
        energy = Fraction(HC, wl)
        chosen = rng.sample(METALS, 4)
        emits = [name for name, w in chosen if w < energy]
        names = [name for name, _ in chosen]
        listed = " ".join(f"{name} ({show(w)} eV)" for name, w in chosen)
        correct = "ทุกโลหะ" if len(emits) == 4 else "ไม่มีโลหะใดเลย" if not emits else " ".join(emits)
        wrong_pool = {"ทุกโลหะ", "ไม่มีโลหะใดเลย", " ".join(names[:2]), " ".join(names[2:]), names[0], names[-1],
                      " ".join(names[:3])}
        wrong_pool.discard(correct)
        return _labelled(
            stem=f"ฉายแสงความยาวคลื่น {wl} nm ลงบนโลหะ: {listed} โลหะใดปล่อยโฟโตอิเล็กตรอน (hc = 1,240 eV·nm)",
            correct=correct, wrongs=tuple(sorted(wrong_pool)[:3]), topic=TOPIC_PHOTO,
            hint="หาพลังงานโฟตอน 1,240/λ แล้วเลือกโลหะที่ฟังก์ชันงานน้อยกว่าพลังงานโฟตอน")
