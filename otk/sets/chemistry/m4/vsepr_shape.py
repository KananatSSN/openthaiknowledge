"""รูปร่างโมเลกุลและสภาพขั้วของโมเลกุลโคเวเลนต์

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.4/17

Sets moved here from: science_wave_f23.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f23 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_SHAPE = "รูปร่างโมเลกุลและสภาพขั้วของโมเลกุลโคเวเลนต์"


SHAPES = {
    (2, 0): "เส้นตรง", (3, 0): "สามเหลี่ยมแบนราบ", (2, 1): "มุมงอ", (4, 0): "ทรงสี่หน้า",
    (3, 1): "พีระมิดฐานสามเหลี่ยม", (2, 2): "มุมงอ", (5, 0): "พีระมิดคู่ฐานสามเหลี่ยม",
    (4, 1): "ทรงสี่หน้าบิดเบี้ยว", (3, 2): "รูปตัวที", (2, 3): "เส้นตรง", (6, 0): "ทรงแปดหน้า",
    (5, 1): "พีระมิดฐานสี่เหลี่ยม", (4, 2): "สี่เหลี่ยมแบนราบ",
}


SHAPE_NAMES = tuple(sorted(set(SHAPES.values())))


# (formula, Thai name, atoms bonded to the centre, lone pairs on the centre, polar, bond angle or None)
SHAPE_MOLECULES = (
    ("CO₂", "คาร์บอนไดออกไซด์", 2, 0, False, 180), ("BeCl₂", "เบริลเลียมคลอไรด์", 2, 0, False, 180),
    ("CS₂", "คาร์บอนไดซัลไฟด์", 2, 0, False, 180), ("HCN", "ไฮโดรเจนไซยาไนด์", 2, 0, True, 180),
    ("BF₃", "โบรอนไตรฟลูออไรด์", 3, 0, False, 120), ("BCl₃", "โบรอนไตรคลอไรด์", 3, 0, False, 120),
    ("SO₃", "ซัลเฟอร์ไตรออกไซด์", 3, 0, False, 120), ("CH₂O", "เมทานาล", 3, 0, True, None),
    ("SO₂", "ซัลเฟอร์ไดออกไซด์", 2, 1, True, None), ("O₃", "โอโซน", 2, 1, True, None),
    ("CH₄", "มีเทน", 4, 0, False, Fraction(219, 2)), ("CCl₄", "คาร์บอนเตตระคลอไรด์", 4, 0, False, Fraction(219, 2)),
    ("SiCl₄", "ซิลิคอนเตตระคลอไรด์", 4, 0, False, Fraction(219, 2)), ("CH₃Cl", "คลอโรมีเทน", 4, 0, True, None),
    ("CH₂Cl₂", "ไดคลอโรมีเทน", 4, 0, True, None), ("CHCl₃", "ไตรคลอโรมีเทน", 4, 0, True, None),
    ("NH₃", "แอมโมเนีย", 3, 1, True, 107), ("PCl₃", "ฟอสฟอรัสไตรคลอไรด์", 3, 1, True, None),
    ("NF₃", "ไนโตรเจนไตรฟลูออไรด์", 3, 1, True, None), ("PH₃", "ฟอสฟีน", 3, 1, True, None),
    ("H₂O", "น้ำ", 2, 2, True, Fraction(209, 2)), ("H₂S", "ไฮโดรเจนซัลไฟด์", 2, 2, True, None),
    ("OF₂", "ออกซิเจนไดฟลูออไรด์", 2, 2, True, None), ("SCl₂", "ซัลเฟอร์ไดคลอไรด์", 2, 2, True, None),
    ("PCl₅", "ฟอสฟอรัสเพนตะคลอไรด์", 5, 0, False, None), ("PF₅", "ฟอสฟอรัสเพนตะฟลูออไรด์", 5, 0, False, None),
    ("SF₄", "ซัลเฟอร์เตตระฟลูออไรด์", 4, 1, True, None), ("ClF₃", "คลอรีนไตรฟลูออไรด์", 3, 2, True, None),
    ("BrF₃", "โบรมีนไตรฟลูออไรด์", 3, 2, True, None), ("XeF₂", "ซีนอนไดฟลูออไรด์", 2, 3, False, 180),
    ("SF₆", "ซัลเฟอร์เฮกซะฟลูออไรด์", 6, 0, False, 90), ("BrF₅", "โบรมีนเพนตะฟลูออไรด์", 5, 1, True, None),
    ("IF₅", "ไอโอดีนเพนตะฟลูออไรด์", 5, 1, True, None), ("XeF₄", "ซีนอนเตตระฟลูออไรด์", 4, 2, False, 90),
)


ANGLES = (90, Fraction(209, 2), 107, Fraction(219, 2), 120, 180)


POLAR_WHY = "มีขั้ว เพราะสภาพขั้วของพันธะไม่หักล้างกัน"


NONPOLAR_WHY = "ไม่มีขั้ว เพราะสภาพขั้วของพันธะหักล้างกันหมด"


POLARITY_CHOICES = (POLAR_WHY, NONPOLAR_WHY, "มีขั้ว เพราะสภาพขั้วของพันธะหักล้างกันหมด",
                    "ไม่มีขั้ว เพราะสภาพขั้วของพันธะไม่หักล้างกัน")


def shape_of(m) -> str:
    return SHAPES[(m[2], m[3])]


def _shape_wrongs(rng: Random, right: str, groups: int) -> tuple[str, ...]:
    """Shapes with the same number of electron groups first, then any other."""
    near = sorted({s for (b, ell), s in SHAPES.items() if b + ell == groups and s != right})
    far = sorted(set(SHAPE_NAMES) - set(near) - {right})
    rng.shuffle(near)
    rng.shuffle(far)
    return tuple((near + far)[:3])


@question_type(
    "chem.vsepr_shape_foundation",
    display_name={"th": "รูปร่างโมเลกุลจากจำนวนคู่อิเล็กตรอนรอบอะตอมกลาง"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_SHAPE,
)
class VseprShapeFoundation(QuestionType):
    """Bonded atoms and lone pairs on the centre fix the shape."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            bonded, lone = rng.choice(sorted(SHAPES))
            right = SHAPES[(bonded, lone)]
            lone_text = "ไม่มีอิเล็กตรอนคู่โดดเดี่ยว" if lone == 0 else f"มีอิเล็กตรอนคู่โดดเดี่ยว {lone} คู่"
            return _labelled(stem=f"อะตอมกลางสร้างพันธะกับอะตอมอื่น {bonded} อะตอม และ{lone_text} "
                                  "ตามทฤษฎี VSEPR โมเลกุลมีรูปร่างแบบใด",
                             correct=right, wrongs=_shape_wrongs(rng, right, bonded + lone), topic=TOPIC_SHAPE,
                             hint="กลุ่มอิเล็กตรอนรอบอะตอมกลางผลักกันให้อยู่ห่างกันมากที่สุด "
                                  "รูปร่างโมเลกุลดูจากตำแหน่งของอะตอม ไม่นับคู่โดดเดี่ยว")
        m = rng.choice(SHAPE_MOLECULES)
        groups = m[2] + m[3]
        return numeric(stem=f"ในโมเลกุล {m[0]} ({m[1]}) อะตอมกลางมีกลุ่มอิเล็กตรอน (คู่ร่วมพันธะและคู่โดดเดี่ยว) "
                            "รอบตัวทั้งหมดกี่กลุ่ม",
                       answer=groups, wrongs=[m[2] if m[3] else groups + 1, groups + 2, groups - 1 or 5],
                       unit="กลุ่ม", topic=TOPIC_SHAPE,
                       hint="เขียนโครงสร้างลิวอิส นับอะตอมที่ต่อกับอะตอมกลาง (พันธะคู่หรือพันธะสามนับเป็น 1 กลุ่ม) "
                            "แล้วบวกคู่โดดเดี่ยวบนอะตอมกลาง")


@question_type(
    "chem.vsepr_shape_fluency",
    display_name={"th": "รูปร่างและมุมพันธะของโมเลกุลที่กำหนด"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_SHAPE,
)
class VseprShapeFluency(QuestionType):
    """From a formula: draw the Lewis structure, then read off the shape or angle."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        with_angle = [m for m in SHAPE_MOLECULES if m[5] is not None]
        if rng.random() < 0.35:
            m = rng.choice(with_angle)
            return numeric(stem=f"มุมพันธะในโมเลกุล {m[0]} ({m[1]}) มีค่าประมาณกี่องศา",
                           answer=m[5], wrongs=rng.sample([a for a in ANGLES if a != m[5]], 3), unit="องศา",
                           topic=TOPIC_SHAPE,
                           hint="เส้นตรง 180° สามเหลี่ยมแบนราบ 120° ทรงสี่หน้า 109.5° "
                                "คู่โดดเดี่ยวผลักแรงกว่าจึงบีบมุมให้เล็กลง (NH₃ 107° H₂O 104.5°)")
        m = rng.choice(SHAPE_MOLECULES)
        right = shape_of(m)
        return _labelled(stem=f"โมเลกุล {m[0]} ({m[1]}) มีรูปร่างแบบใด", correct=right,
                         wrongs=_shape_wrongs(rng, right, m[2] + m[3]), topic=TOPIC_SHAPE,
                         hint="นับอะตอมที่ต่อกับอะตอมกลางและคู่โดดเดี่ยวบนอะตอมกลาง แล้วเทียบกับรูปร่างตามทฤษฎี VSEPR")


@question_type(
    "chem.vsepr_shape_application",
    display_name={"th": "สภาพขั้วของโมเลกุลจากรูปร่าง"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_SHAPE,
)
class VseprShapeApplication(QuestionType):
    """Polar bonds cancel only in a symmetrical shape with identical outer atoms."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = ("ดูรูปร่างโมเลกุล ถ้าสมมาตรและอะตอมรอบอะตอมกลางเป็นชนิดเดียวกัน สภาพขั้วของพันธะหักล้างกัน "
                "โมเลกุลไม่มีขั้ว")
        if rng.random() < 0.5:
            m = rng.choice(SHAPE_MOLECULES)
            right = POLAR_WHY if m[4] else NONPOLAR_WHY
            return _labelled(stem=f"โมเลกุล {m[0]} ({m[1]}) มีสภาพขั้วอย่างไร", correct=right,
                             wrongs=tuple(c for c in POLARITY_CHOICES if c != right), topic=TOPIC_SHAPE, hint=hint)
        polar = rng.random() < 0.5
        match = [m for m in SHAPE_MOLECULES if m[4] == polar]
        others = [m for m in SHAPE_MOLECULES if m[4] != polar]
        pick = rng.choice(match)
        return _labelled(stem=f"โมเลกุลใด{'มีขั้ว' if polar else 'ไม่มีขั้ว'}", correct=pick[0],
                         wrongs=tuple(m[0] for m in rng.sample(others, 3)), topic=TOPIC_SHAPE, hint=hint)
