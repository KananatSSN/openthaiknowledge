"""กฎรวมแก๊ส

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.5/2

Sets moved here from: science_wave_f24.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import numeric, show
from otk.sets._support.science_wave_f24 import (
    ATMS,
    KELVINS,
    SUBJECT,
    UPPER_FIVE,
    _find,
    _volume,
    celsius,
    exact,
)

PROVENANCE = Provenance("original")


TOPIC_COMBINED = "กฎรวมแก๊ส"


MMHG = (380, 570, 608, 684, 722, 740, 750, 760, 780, 798, 836, 912, 1140, 1520)


def _combined(rng: Random, pressures, volume):
    """P₁, V₁, T₁, P₂, T₂ with V₂ = P₁V₁T₂ / (P₂T₁) exact."""
    def draw():
        p1, p2 = rng.sample(pressures, 2)
        t1, t2 = rng.sample(KELVINS, 2)
        v1, unit = volume()
        v2 = Fraction(p1 * v1 * t2) / (p2 * t1)
        return (p1, v1, t1, p2, t2, v2, unit) if exact(v2) else None
    return _find(rng, draw)


COMBINED_HINT = "กฎรวมแก๊ส: P₁V₁/T₁ = P₂V₂/T₂ โดย T เป็นเคลวิน และความดันสองสถานะต้องใช้หน่วยเดียวกัน"


@question_type(
    "chem.combined_gas_foundation",
    display_name={"th": "กฎรวมแก๊ส: หาปริมาตรที่ภาวะใหม่"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_COMBINED,
)
class CombinedGasFoundation(QuestionType):
    """V₂ = P₁V₁T₂ / (P₂T₁)."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        p1, v1, t1, p2, t2, v2, unit = _combined(rng, ATMS, lambda: _volume(rng))
        return numeric(stem=f"แก๊สปริมาตร {show(v1)} {unit} ความดัน {show(p1)} atm อุณหภูมิ {celsius(t1)} "
                            f"ถ้าเปลี่ยนความดันเป็น {show(p2)} atm และอุณหภูมิเป็น {celsius(t2)} ปริมาตรของแก๊สจะเป็นเท่าใด",
                       answer=v2, wrongs=[p1 * v1 / p2, p2 * v1 * t2 / (p1 * t1), Fraction(p1 * v1 * t1) / (p2 * t2)],
                       unit=unit, topic=TOPIC_COMBINED, hint=COMBINED_HINT)


@question_type(
    "chem.combined_gas_fluency",
    display_name={"th": "กฎรวมแก๊ส: หาความดันหรืออุณหภูมิที่ภาวะใหม่"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_COMBINED,
)
class CombinedGasFluency(QuestionType):
    """Rearrange for P₂ or T₂; T₂ comes back in kelvin and is asked in °C."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        p1, v1, t1, p2, t2, v2, unit = _combined(rng, ATMS, lambda: _volume(rng))
        if rng.random() < 0.5 or t2 == 273:
            return numeric(stem=f"แก๊สปริมาตร {show(v1)} {unit} ความดัน {show(p1)} atm อุณหภูมิ {celsius(t1)} "
                                f"ถ้าทำให้ปริมาตรเป็น {show(v2)} {unit} ที่อุณหภูมิ {celsius(t2)} ความดันของแก๊สจะเป็นเท่าใด",
                           answer=p2, wrongs=[p1 * v1 / v2, p1 * v2 / v1, p2 * t1 / t2],
                           unit="atm", topic=TOPIC_COMBINED, hint=COMBINED_HINT)
        return numeric(stem=f"แก๊สปริมาตร {show(v1)} {unit} ความดัน {show(p1)} atm อุณหภูมิ {celsius(t1)} "
                            f"ถ้าต้องการให้แก๊สมีปริมาตร {show(v2)} {unit} ที่ความดัน {show(p2)} atm ต้องมีอุณหภูมิกี่ °C",
                       answer=t2 - 273, wrongs=[t2, (t2 - 273) * 2 or 10, t1 - 273 + 10 if t1 != t2 - 10 else t2 - 263],
                       unit="°C", topic=TOPIC_COMBINED, allow_negative=True, hint=COMBINED_HINT)


@question_type(
    "chem.combined_gas_application",
    display_name={"th": "กฎรวมแก๊สในสถานการณ์และการเปลี่ยนหน่วยความดัน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_COMBINED,
)
class CombinedGasApplication(QuestionType):
    """Pressures in mmHg against atm, or a gas brought to STP (0 °C, 1 atm)."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            def draw():
                p1 = rng.choice(MMHG)
                t1 = rng.choice([t for t in KELVINS if t != 273])
                v1 = rng.randrange(50, 1001, 50)
                v2 = Fraction(p1 * v1 * 273, 760 * t1)
                return (p1, t1, v1, v2) if exact(v2) else None

            p1, t1, v1, v2 = _find(rng, draw)
            return numeric(stem=f"เก็บแก๊สได้ {v1} mL ที่ความดัน {p1} mmHg อุณหภูมิ {celsius(t1)} "
                                "ถ้าเปลี่ยนเป็นภาวะมาตรฐาน (STP: 0 °C และ 1 atm = 760 mmHg) แก๊สนี้มีปริมาตรกี่ mL",
                           answer=v2, wrongs=[Fraction(p1 * v1, 760), Fraction(760 * v1 * 273, p1 * t1) if p1 else v1,
                                              Fraction(p1 * v1 * t1, 760 * 273)],
                           unit="mL", topic=TOPIC_COMBINED, hint=COMBINED_HINT + " (STP: 273 K, 760 mmHg)")

        def draw():
            p1 = rng.choice(MMHG)
            p2 = rng.choice(ATMS)
            t1, t2 = rng.sample(KELVINS, 2)
            # A rising balloon meets lower pressure and colder air.
            if p2 * 760 >= p1 or t2 >= t1:
                return None
            v1, unit = _volume(rng)
            v2 = Fraction(p1 * v1 * t2) / (p2 * 760 * t1)
            return (p1, v1, t1, p2, t2, v2, unit) if exact(v2) else None

        p1, v1, t1, p2, t2, v2, unit = _find(rng, draw)
        return numeric(stem=f"บอลลูนบรรจุแก๊ส {show(v1)} {unit} ที่ความดัน {p1} mmHg อุณหภูมิ {celsius(t1)} "
                            f"เมื่อลอยไปถึงจุดที่ความดัน {show(p2)} atm อุณหภูมิ {celsius(t2)} บอลลูนมีปริมาตรเท่าใด "
                            "(1 atm = 760 mmHg)",
                       answer=v2, wrongs=[Fraction(p1 * v1 * t2) / (p2 * t1), v2 * t1 / t2, Fraction(p1 * v1) / (p2 * 760)],
                       unit=unit, topic=TOPIC_COMBINED, hint=COMBINED_HINT)
