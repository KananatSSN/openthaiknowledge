"""ภาพจากเลนส์บางและการนำไปใช้

ฟิสิกส์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 2 ม.5/11

Sets moved here from: science_wave_f9.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f9 import SUBJECT, UPPER_FIVE, _exact

PROVENANCE = Provenance("original")


TOPIC_LENS = "ภาพจากเลนส์บางและการนำไปใช้"


LENS_USES = (
    ("แว่นขยาย", "เลนส์นูน โดยวางวัตถุห่างเลนส์น้อยกว่าความยาวโฟกัส ได้ภาพเสมือนหัวตั้งขยาย"),
    ("กล้องถ่ายรูป", "เลนส์นูน โดยวัตถุอยู่ไกลกว่า 2f ได้ภาพจริงหัวกลับขนาดเล็กบนเซนเซอร์"),
    ("เครื่องฉายภาพ", "เลนส์นูน โดยวัตถุอยู่ระหว่าง f กับ 2f ได้ภาพจริงหัวกลับขยายบนจอ"),
    ("แว่นสายตาของคนสายตาสั้น", "เลนส์เว้า ช่วยกระจายแสงให้ภาพไปตกที่จอตาพอดี"),
    ("แว่นสายตาของคนสายตายาว", "เลนส์นูน ช่วยรวมแสงให้ภาพมาตกที่จอตาพอดี"),
    ("ตาแมวที่ประตู", "เลนส์เว้า ให้ภาพเสมือนหัวตั้งขนาดเล็ก เห็นมุมกว้าง"),
)


def _convex_image(s_over_f: Fraction) -> str:
    if s_over_f > 2:
        return "ภาพจริง หัวกลับ ขนาดเล็กกว่าวัตถุ"
    if s_over_f == 2:
        return "ภาพจริง หัวกลับ ขนาดเท่าวัตถุ"
    if s_over_f > 1:
        return "ภาพจริง หัวกลับ ขนาดใหญ่กว่าวัตถุ"
    return "ภาพเสมือน หัวตั้ง ขนาดใหญ่กว่าวัตถุ"


IMAGE_KINDS = ("ภาพจริง หัวกลับ ขนาดเล็กกว่าวัตถุ", "ภาพจริง หัวกลับ ขนาดเท่าวัตถุ",
               "ภาพจริง หัวกลับ ขนาดใหญ่กว่าวัตถุ", "ภาพเสมือน หัวตั้ง ขนาดใหญ่กว่าวัตถุ",
               "ภาพเสมือน หัวตั้ง ขนาดเล็กกว่าวัตถุ")


@question_type(
    "phys.thin_lens_foundation",
    display_name={"th": "ชนิดของภาพจากเลนส์บางและการใช้เลนส์"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_LENS,
)
class ThinLensFoundation(QuestionType):
    """Where the object sits against f decides the image; which lens each device uses."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        hint = "เลนส์นูน: วัตถุไกลกว่า 2f ภาพจริงเล็ก ระหว่าง f กับ 2f ภาพจริงขยาย ใกล้กว่า f ภาพเสมือนขยาย เลนส์เว้าให้ภาพเสมือนเล็กเสมอ"
        if shape == 0:
            device, use = rng.choice(LENS_USES)
            others = [u for d, u in LENS_USES if d != device]
            return _labelled(stem=f"{device}ใช้เลนส์และจัดวางอย่างไร", correct=use,
                             wrongs=tuple(others), topic=TOPIC_LENS, hint=hint)
        f = rng.randint(4, 30)
        if shape == 1:
            ratio = rng.choice((Fraction(1, 2), Fraction(3, 4), Fraction(3, 2), Fraction(5, 4), 2, 3, Fraction(5, 2), 4))
            s = f * ratio
            correct = _convex_image(ratio)
            return _labelled(
                stem=f"วางวัตถุหน้าเลนส์นูนความยาวโฟกัส {f} cm ห่างจากเลนส์ {show(s)} cm ได้ภาพชนิดใด",
                correct=correct, wrongs=tuple([k for k in IMAGE_KINDS if k != correct]),
                topic=TOPIC_LENS, hint=hint)
        s = rng.randint(2, 60)
        return _labelled(
            stem=f"วางวัตถุหน้าเลนส์เว้าความยาวโฟกัส {f} cm ห่างจากเลนส์ {s} cm ได้ภาพชนิดใด",
            correct="ภาพเสมือน หัวตั้ง ขนาดเล็กกว่าวัตถุ",
            wrongs=tuple([k for k in IMAGE_KINDS if k != "ภาพเสมือน หัวตั้ง ขนาดเล็กกว่าวัตถุ"]),
            topic=TOPIC_LENS, hint=hint)


@question_type(
    "phys.thin_lens_fluency",
    display_name={"th": "คำนวณระยะภาพและกำลังขยายของเลนส์นูน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_LENS,
)
class ThinLensFluency(QuestionType):
    """1/f = 1/s + 1/s′ and m = s′/s for a converging lens forming a real image."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        f, s = rng.choice([(f, s) for f in range(5, 41, 5) for s in range(f + f // 4 + 1, 4 * f + 1)
                           if _exact(Fraction(s * f, s - f)) and _exact(Fraction(f, s - f))])
        image = Fraction(s * f, s - f)
        if rng.random() < 0.55:
            return numeric(
                stem=f"วางวัตถุห่างจากเลนส์นูนความยาวโฟกัส {f} cm เป็นระยะ {s} cm ภาพเกิดห่างจากเลนส์เท่าใด",
                answer=image, wrongs=[s - f, Fraction(s * f, s + f), s + f], unit="cm", topic=TOPIC_LENS,
                hint="1/f = 1/s + 1/s′ ดังนั้น s′ = sf ÷ (s − f)")
        return numeric(
            stem=f"วางวัตถุห่างจากเลนส์นูนความยาวโฟกัส {f} cm เป็นระยะ {s} cm ภาพมีกำลังขยายเท่าใด",
            answer=image / s, wrongs=[s / image, image, Fraction(f, s)], unit="เท่า", topic=TOPIC_LENS,
            hint="หา s′ ก่อน แล้วกำลังขยาย m = s′/s = ขนาดภาพ/ขนาดวัตถุ")


@question_type(
    "phys.thin_lens_application",
    display_name={"th": "ขนาดภาพ เลนส์เว้า และกำลังของเลนส์"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_LENS,
)
class ThinLensApplication(QuestionType):
    """Image height on a screen, the virtual image of a diverging lens, and power in diopters."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        if shape == 0:
            f, s, h = rng.choice([(f, s, h) for f in range(5, 41, 5) for s in range(f + f // 4 + 1, 4 * f + 1)
                                  for h in (1, 2, 3, 4, 5, 6, 8, 10)
                                  if _exact(Fraction(s * f, s - f)) and _exact(Fraction(h * f, s - f))])
            image = Fraction(s * f, s - f)
            return numeric(
                stem=(f"วัตถุสูง {h} cm วางห่างเลนส์นูนความยาวโฟกัส {f} cm เป็นระยะ {s} cm "
                      "ภาพที่ปรากฏบนฉากสูงเท่าใด"),
                answer=h * image / s, wrongs=[h * s / image, h, h * image / f], unit="cm", topic=TOPIC_LENS,
                hint="หา s′ จาก 1/f = 1/s + 1/s′ แล้วขนาดภาพ = ขนาดวัตถุ × s′/s")
        if shape == 1:
            f, s = rng.choice([(f, s) for f in range(5, 41, 5) for s in range(5, 61) if _exact(Fraction(s * f, s + f))])
            return numeric(
                stem=f"วางวัตถุห่างจากเลนส์เว้าความยาวโฟกัส {f} cm เป็นระยะ {s} cm ภาพเสมือนเกิดห่างจากเลนส์เท่าใด",
                answer=Fraction(s * f, s + f), wrongs=[Fraction(s * f, abs(s - f)) if s != f else s * 2, s + f,
                                                       Fraction(s + f, 2)],
                unit="cm", topic=TOPIC_LENS,
                hint="เลนส์เว้า f เป็นลบ: 1/(−f) = 1/s + 1/s′ ได้ s′ = −sf ÷ (s + f) ภาพอยู่ด้านเดียวกับวัตถุ")
        f = rng.choice((10, 20, 25, 40, 50, 100, 200))
        concave = rng.random() < 0.5
        power = Fraction(100, f) * (-1 if concave else 1)
        kind = "เลนส์เว้า" if concave else "เลนส์นูน"
        return numeric(
            stem=f"แว่นตาใช้{kind}ความยาวโฟกัส {f} cm เลนส์มีกำลังกี่ไดออปเตอร์",
            answer=power, wrongs=[-power, Fraction(f, 100) * (-1 if concave else 1), power * 10], unit="D",
            topic=TOPIC_LENS, allow_negative=True,
            hint="กำลังของเลนส์ P = 1/f โดย f เป็นเมตร เลนส์นูนเป็นบวก เลนส์เว้าเป็นลบ")
