"""กฎความดันย่อยของดอลตัน

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.5/4

Sets moved here from: science_wave_f25.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import numeric, show
from otk.sets._support.science_wave_f24 import _find, exact
from otk.sets._support.science_wave_f25 import QUARTERS, STABLE_GASES, SUBJECT, UPPER_FIVE, gas

PROVENANCE = Provenance("original")


TOPIC_DALTON = "กฎความดันย่อยของดอลตัน"


# Vapour pressure of water, mmHg, at °C.
WATER_VAPOUR = {20: Fraction(175, 10), 25: Fraction(238, 10), 27: Fraction(267, 10), 30: Fraction(318, 10)}


@question_type(
    "chem.dalton_pressure_foundation",
    display_name={"th": "ความดันรวมและความดันย่อยของแก๊สผสม"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_DALTON,
)
class DaltonPressureFoundation(QuestionType):
    """P_total = P_A + P_B + ..."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        names = rng.sample(sorted(STABLE_GASES), rng.choice((2, 3)))
        unit = rng.choice(("mmHg", "kPa"))
        parts = [rng.randrange(10, 401, 5) if unit == "mmHg" else rng.randint(5, 80) for _ in names]
        total = sum(parts)
        hint = "ความดันรวมของแก๊สผสม = ผลรวมความดันย่อยของแก๊สแต่ละชนิด"
        if rng.random() < 0.5:
            listed = " ".join(f"{f} {x} {unit}" for f, x in zip(names, parts))
            return numeric(stem=f"แก๊สผสมในภาชนะมีความดันย่อย {listed} ความดันรวมเท่าใด", answer=total,
                           wrongs=[max(parts), total // len(parts) or 1, total + parts[0]], unit=unit,
                           topic=TOPIC_DALTON, hint=hint)
        listed = " ".join(f"{f} {x} {unit}" for f, x in zip(names[1:], parts[1:]))
        return numeric(stem=f"แก๊สผสม {', '.join(names)} มีความดันรวม {total} {unit} ถ้าความดันย่อย {listed} "
                            f"ความดันย่อยของ {names[0]} เท่าใด",
                       answer=parts[0], wrongs=[total, total + sum(parts[1:]), parts[0] + parts[1]], unit=unit,
                       topic=TOPIC_DALTON, hint=hint)


@question_type(
    "chem.dalton_pressure_fluency",
    display_name={"th": "ความดันย่อยจากเศษส่วนโมล"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_DALTON,
)
class DaltonPressureFluency(QuestionType):
    """P_A = (n_A / n_total) × P_total, or n_A back from P_A."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            a, b = rng.sample(sorted(STABLE_GASES), 2)
            na, nb = rng.sample(QUARTERS[:12], 2)
            total = rng.choice((1, 2, 3, 4, 5, 6, 8, 10)) if rng.random() < 0.5 else rng.randrange(100, 1001, 50)
            pa = na / (na + nb) * total
            return (a, b, na, nb, total, pa) if exact(pa) else None

        a, b, na, nb, total, pa = _find(rng, draw)
        unit = "atm" if total <= 10 else "kPa"
        hint = "ความดันย่อย = เศษส่วนโมล × ความดันรวม โดยเศษส่วนโมล = โมลของแก๊สนั้น ÷ โมลรวม"
        if rng.random() < 0.6:
            return numeric(stem=f"แก๊สผสมประกอบด้วย {a} {show(na)} โมล และ {b} {show(nb)} โมล มีความดันรวม {total} {unit} "
                                f"ความดันย่อยของ {a} เท่าใด",
                           answer=pa, wrongs=[total - pa, na * total, Fraction(total, 2)], unit=unit,
                           topic=TOPIC_DALTON, hint=hint)
        return numeric(stem=f"แก๊สผสมของ {a} และ {b} มีความดันรวม {total} {unit} มี {b} {show(nb)} โมล "
                            f"และ {a} มีความดันย่อย {show(pa)} {unit} แก๊ส {a} มีกี่โมล",
                       answer=na, wrongs=[nb, na + nb, pa / total],
                       unit="โมล", topic=TOPIC_DALTON, hint=hint + " (จึงได้ n_A : n_B = P_A : P_B)")


@question_type(
    "chem.dalton_pressure_application",
    display_name={"th": "เก็บแก๊สเหนือน้ำและต่อภาชนะแก๊สเข้าด้วยกัน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_DALTON,
)
class DaltonPressureApplication(QuestionType):
    """Subtract the water vapour, or spread each gas over the joined volume."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            celsius_t = rng.choice(sorted(WATER_VAPOUR))
            vapour = WATER_VAPOUR[celsius_t]
            total = rng.randrange(740, 781, 2)
            formula = rng.choice(("H₂", "O₂", "N₂"))
            return numeric(stem=f"เก็บ{gas(formula)} โดยการแทนที่น้ำที่ {celsius_t} °C ได้แก๊สเปียกที่มีความดันรวม "
                                f"{total} mmHg ถ้าความดันไอน้ำที่ {celsius_t} °C เท่ากับ {show(vapour)} mmHg "
                                f"ความดันย่อยของ {formula} เท่าใด",
                           answer=total - vapour, wrongs=[total + vapour, total, 760 - vapour], unit="mmHg",
                           topic=TOPIC_DALTON, hint="แก๊สที่เก็บเหนือน้ำมีไอน้ำปนอยู่: P_แก๊ส = P_รวม − P_ไอน้ำ")

        def draw():
            a, b = rng.sample(sorted(STABLE_GASES), 2)
            va, vb = rng.sample(range(1, 11), 2)
            pa, pb = rng.sample(range(1, 11), 2)
            total = Fraction(pa * va + pb * vb, va + vb)
            part = Fraction(pa * va, va + vb)
            return (a, b, va, vb, pa, pb, total, part) if exact(total) and exact(part) else None

        a, b, va, vb, pa, pb, total, part = _find(rng, draw)
        stem = (f"ถัง A ปริมาตร {va} L บรรจุ {a} ความดัน {pa} atm ถัง B ปริมาตร {vb} L บรรจุ {b} ความดัน {pb} atm "
                "เมื่อเปิดวาล์วต่อถังทั้งสองเข้าด้วยกันที่อุณหภูมิคงที่")
        hint = "แต่ละแก๊สขยายไปเต็มปริมาตรรวม: P_ย่อย = P₁V₁ / V_รวม แล้วความดันรวม = ผลรวมความดันย่อย"
        if rng.random() < 0.5:
            return numeric(stem=f"{stem} ความดันรวมเท่าใด", answer=total,
                           wrongs=[pa + pb, Fraction(pa + pb, 2), part], unit="atm", topic=TOPIC_DALTON, hint=hint)
        return numeric(stem=f"{stem} ความดันย่อยของ {a} เท่าใด", answer=part,
                       wrongs=[pa, total, Fraction(pa, 2)], unit="atm", topic=TOPIC_DALTON, hint=hint)
