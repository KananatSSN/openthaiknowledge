"""แรงแม่เหล็กที่กระทำต่อประจุและเส้นลวดที่มีกระแสไฟฟ้า

ฟิสิกส์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 3 ม.6/2

Sets moved here from: science_wave_f12.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f12 import (
    DIRECTIONS,
    NAME_OF,
    SUBJECT,
    UPPER_SIX,
    _exact,
    cross,
)

PROVENANCE = Provenance("original")


TOPIC_MAG_FORCE = "แรงแม่เหล็กที่กระทำต่อประจุและเส้นลวดที่มีกระแสไฟฟ้า"


SINES = ((90, Fraction(1)), (30, Fraction(1, 2)), (37, Fraction(3, 5)), (53, Fraction(4, 5)))


@question_type(
    "phys.magnetic_force_charge_foundation",
    display_name={"th": "แรงแม่เหล็กที่กระทำต่อเส้นลวดที่มีกระแสไฟฟ้า F = ILB sin θ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_MAG_FORCE,
)
class MagneticForceChargeFoundation(QuestionType):
    """F = ILB sin θ, and the forces between parallel currents."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            same = rng.random() < 0.5
            return _labelled(
                stem=f"เส้นลวดตรงยาวสองเส้นวางขนานกัน มีกระแสไฟฟ้าทิศ{'เดียวกัน' if same else 'ตรงข้ามกัน'} แรงระหว่างเส้นลวดเป็นอย่างไร",
                correct="ดึงดูดกัน" if same else "ผลักกัน",
                wrongs=("ผลักกัน" if same else "ดึงดูดกัน", "ไม่มีแรงกระทำ", "บิดให้หมุนรอบกัน"),
                topic=TOPIC_MAG_FORCE, hint="กระแสทิศเดียวกันดูดกัน กระแสทิศตรงข้ามผลักกัน")
        angle, sin = rng.choice(SINES)
        i, length, b = rng.choice([(i, Fraction(ell * 5, 100), Fraction(t, 10)) for i in range(1, 21) for ell in range(1, 21)
                                   for t in range(1, 11) if _exact(i * Fraction(ell * 5, 100) * Fraction(t, 10) * sin)])
        force = i * length * b * sin
        stated = "(sin 30° = 0.5, sin 37° = 0.6, sin 53° = 0.8)"
        return numeric(
            stem=(f"เส้นลวดยาว {show(length)} m มีกระแสไฟฟ้า {i} A วางทำมุม {angle}° กับสนามแม่เหล็ก {show(b)} T "
                  f"แรงแม่เหล็กที่กระทำต่อเส้นลวดเท่าใด {stated if angle != 90 else ''}").strip(),
            answer=force, wrongs=[i * length * b if sin != 1 else force * 2, i * b, force / 2 if sin != 1 else i * length],
            unit="N", topic=TOPIC_MAG_FORCE, hint="F = ILB sin θ โดย θ เป็นมุมระหว่างเส้นลวดกับสนาม")


@question_type(
    "phys.magnetic_force_charge_fluency",
    display_name={"th": "แรงแม่เหล็กต่อประจุที่เคลื่อนที่และรัศมีการเคลื่อนที่เป็นวงกลม"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_MAG_FORCE,
)
class MagneticForceChargeFluency(QuestionType):
    """F = qvB for a charge crossing a field, and r = mv/qB for an ion."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            q = rng.randint(1, 20)
            v = rng.randint(1, 20) * 100
            b = Fraction(rng.randint(1, 10), 10)
            force = q * v * b / 1000
            return numeric(
                stem=f"อนุภาคประจุ {q} μC เคลื่อนที่ด้วยความเร็ว {v:,} m/s ตั้งฉากกับสนามแม่เหล็ก {show(b)} T ได้รับแรงกี่มิลลินิวตัน",
                answer=force, wrongs=[force * 1000, force * 10, q * v / 1000], unit="mN", topic=TOPIC_MAG_FORCE,
                hint="F = qvB (q เป็นคูลอมบ์) แล้วแปลงเป็นมิลลินิวตัน")
        # r (cm) = m v / (q B) with m = a × 10⁻²⁶ kg, v = b × 10⁵ m/s, q = 1.6 × 10⁻¹⁹ C.
        a, speed, field = rng.choice([(a, s, f) for a in (Fraction(16, 10), Fraction(32, 10), Fraction(48, 10),
                                                          Fraction(64, 10), 8)
                                      for s in (1, 2, 3, 4, 5) for f in (Fraction(1, 10), Fraction(1, 5), Fraction(2, 5),
                                                                         Fraction(1, 2), 1)
                                      if _exact(a * s / (Fraction(16, 10) * f))])
        radius = a * speed / (Fraction(16, 10) * field)
        return numeric(
            stem=(f"ไอออนมวล {show(a)} × 10⁻²⁶ kg ประจุ +1.6 × 10⁻¹⁹ C เคลื่อนที่ด้วยความเร็ว {speed} × 10⁵ m/s "
                  f"เข้าไปตั้งฉากกับสนามแม่เหล็ก {show(field)} T เคลื่อนที่เป็นวงกลมรัศมีกี่เซนติเมตร"),
            answer=radius, wrongs=[radius * 10, radius / 10, radius * 2], unit="cm", topic=TOPIC_MAG_FORCE,
            hint="แรงแม่เหล็กเป็นแรงสู่ศูนย์กลาง: qvB = mv²/r ดังนั้น r = mv/(qB)")


@question_type(
    "phys.magnetic_force_charge_application",
    display_name={"th": "ทิศของแรงแม่เหล็กต่อประจุและเส้นลวดตามกฎมือขวา"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_MAG_FORCE,
)
class MagneticForceChargeApplication(QuestionType):
    """F ∝ q v × B: a proton, an electron, or a current-carrying wire."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        motion = rng.choice(list(DIRECTIONS))
        field = rng.choice([n for n, v in DIRECTIONS.items()
                            if sum(a * b for a, b in zip(v, DIRECTIONS[motion])) == 0])
        what = rng.choice(("โปรตอน", "อิเล็กตรอน", "เส้นลวดตรง"))
        force = cross(DIRECTIONS[motion], DIRECTIONS[field])
        if what == "อิเล็กตรอน":
            force = tuple(-x for x in force)
        name = NAME_OF[force]
        moving = f"มีกระแสไฟฟ้าทิศ{motion}" if what == "เส้นลวดตรง" else f"เคลื่อนที่ทิศ{motion}"
        return _labelled(
            stem=f"{what}{moving} ในสนามแม่เหล็กที่มีทิศ{field} ได้รับแรงแม่เหล็กทิศใด",
            correct=f"ทิศ{name}", wrongs=tuple(f"ทิศ{w}" for w in rng.sample([n for n in DIRECTIONS if n != name], 3)),
            topic=TOPIC_MAG_FORCE,
            hint="F = qv × B: ชี้นิ้วตามความเร็ว (หรือกระแส) งอเข้าหาสนาม นิ้วโป้งชี้ทิศแรงต่อประจุบวก อิเล็กตรอนได้แรงทิศตรงข้าม")
