"""แรงลัพธ์ของแรงสองแรงที่ทำมุมต่อกัน

ฟิสิกส์ · ม.4 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 1 ม.4/4

Sets moved here from: science_wave_f3.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import SUBJECT, UPPER_FOUR, _labelled, numeric

PROVENANCE = Provenance("original")


TOPIC_ANGLE = "แรงลัพธ์ของแรงสองแรงที่ทำมุมต่อกัน"


# (F1, F2, R) with R² = F1² + F2² + 2F1F2cosθ exact at each angle.
AT_60 = ((3, 5, 7), (5, 3, 7), (7, 8, 13), (8, 7, 13), (5, 16, 19), (16, 5, 19))


AT_90 = ((3, 4, 5), (6, 8, 10), (5, 12, 13), (8, 15, 17), (9, 12, 15), (12, 16, 20), (7, 24, 25))


AT_120 = ((3, 8, 7), (8, 3, 7), (5, 8, 7), (8, 5, 7), (7, 15, 13), (15, 7, 13), (5, 21, 19))


def resultant_squared(f1: int, f2: int, angle: int) -> Fraction:
    cos = {0: 1, 60: Fraction(1, 2), 90: 0, 120: Fraction(-1, 2), 180: -1}[angle]
    return f1 * f1 + f2 * f2 + 2 * f1 * f2 * cos


@question_type(
    "phys.force_angle_foundation",
    display_name={"th": "ขนาดของแรงลัพธ์เมื่อมุมระหว่างแรงเปลี่ยน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_ANGLE,
)
class ForceAngleFoundation(QuestionType):
    """The limits: in line, opposite, and the range in between."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        f1, f2 = sorted(rng.sample(range(2, 30), 2))
        shape = rng.randrange(3)
        hint = "แรงลัพธ์มากที่สุดเมื่อแรงทำมุม 0° (บวกกัน) และน้อยที่สุดเมื่อทำมุม 180° (ลบกัน)"
        if shape == 0:
            return numeric(stem=f"แรง {f1} N และ {f2} N ทำมุม 0° ต่อกัน แรงลัพธ์มีขนาดเท่าใด",
                           answer=f1 + f2, wrongs=[f2 - f1, f2, f1 * f2], unit="N", topic=TOPIC_ANGLE, hint=hint)
        if shape == 1:
            return numeric(stem=f"แรง {f1} N และ {f2} N ทำมุม 180° ต่อกัน แรงลัพธ์มีขนาดเท่าใด",
                           answer=f2 - f1, wrongs=[f1 + f2, f1, f2], unit="N", topic=TOPIC_ANGLE, hint=hint)
        return _labelled(
            stem=f"แรง {f1} N และ {f2} N กระทำต่อวัตถุเดียวกัน โดยทำมุมใดก็ได้ แรงลัพธ์อยู่ในช่วงใด",
            correct=f"ตั้งแต่ {f2 - f1} N ถึง {f1 + f2} N",
            wrongs=(f"ตั้งแต่ 0 N ถึง {f1 + f2} N", f"ตั้งแต่ {f1} N ถึง {f2} N",
                    f"เท่ากับ {f1 + f2} N เสมอ"),
            topic=TOPIC_ANGLE, hint=hint)


@question_type(
    "phys.force_angle_fluency",
    display_name={"th": "คำนวณแรงลัพธ์ของแรงสองแรงที่ทำมุม 60° 90° และ 120°"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_ANGLE,
)
class ForceAngleFluency(QuestionType):
    """R² = F₁² + F₂² + 2F₁F₂cos θ at the angles where it comes out whole."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        angle, bank = rng.choice(((60, AT_60), (90, AT_90), (120, AT_120)))
        f1, f2, r = rng.choice(bank)
        k = rng.choice((1, 1, 2, 3))
        f1, f2, r = f1 * k, f2 * k, r * k
        assert resultant_squared(f1, f2, angle) == r * r
        return numeric(
            stem=f"แรง {f1} N และ {f2} N กระทำต่อวัตถุที่จุดเดียวกัน โดยทำมุม {angle}° ต่อกัน แรงลัพธ์มีขนาดเท่าใด",
            answer=r, wrongs=[f1 + f2, abs(f1 - f2), f1 + f2 - 1], unit="N", topic=TOPIC_ANGLE,
            hint="R² = F₁² + F₂² + 2F₁F₂cos θ (cos 60° = ½, cos 90° = 0, cos 120° = −½)")


@question_type(
    "phys.force_angle_application",
    display_name={"th": "องค์ประกอบของแรงและแรงที่ทำให้สมดุล"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_ANGLE,
)
class ForceAngleApplication(QuestionType):
    """Split a force into components, or find the third force that balances two."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            f = rng.randint(2, 20) * 5
            angle = rng.choice((37, 53))
            horizontal = rng.random() < 0.5
            # With the angle to the horizontal: cos 37° = 0.8, sin 37° = 0.6.
            cos = Fraction(4, 5) if angle == 37 else Fraction(3, 5)
            sin = Fraction(3, 5) if angle == 37 else Fraction(4, 5)
            answer = f * (cos if horizontal else sin)
            return numeric(
                stem=(f"ดึงกล่องด้วยเชือกที่ทำมุม {angle}° กับแนวระดับด้วยแรง {f} N องค์ประกอบของแรงใน"
                      f"แนว{'ระดับ' if horizontal else 'ดิ่ง'}มีขนาดเท่าใด (sin 37° = 0.6, cos 37° = 0.8)"),
                answer=answer, wrongs=[f * (sin if horizontal else cos), f, Fraction(f, 2)],
                unit="N", topic=TOPIC_ANGLE,
                hint="องค์ประกอบที่อยู่ติดมุมใช้ cos องค์ประกอบที่อยู่ตรงข้ามมุมใช้ sin และ sin 53° = cos 37°")
        angle, bank = rng.choice(((60, AT_60), (90, AT_90), (120, AT_120)))
        f1, f2, r = rng.choice(bank)
        return numeric(
            stem=(f"แรง {f1} N และ {f2} N ทำมุม {angle}° ต่อกันกระทำต่อห่วงวงหนึ่ง ต้องออกแรงที่สามขนาดเท่าใด "
                  "ห่วงจึงอยู่ในสมดุล"),
            answer=r, wrongs=[f1 + f2, abs(f1 - f2), f1 * f2], unit="N", topic=TOPIC_ANGLE,
            hint="แรงที่สามต้องมีขนาดเท่ากับแรงลัพธ์ของสองแรงแรก และมีทิศตรงข้าม")
