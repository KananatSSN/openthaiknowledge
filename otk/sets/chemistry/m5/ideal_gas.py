"""กฎของอาโวกาโดรและกฎแก๊สอุดมคติ

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.5/3

Sets moved here from: science_wave_f25.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f24 import KELVINS, _find, celsius, exact
from otk.sets._support.science_wave_f25 import (
    GASES,
    QUARTERS,
    STABLE_GASES,
    STP_VOLUME,
    SUBJECT,
    UPPER_FIVE,
    gas,
)

PROVENANCE = Provenance("original")


TOPIC_IDEAL = "กฎของอาโวกาโดรและกฎแก๊สอุดมคติ"


R = Fraction(821, 10000)


R_TEXT = "(R = 0.0821 L·atm/(mol·K))"


def ideal_case(rng: Random):
    """P (atm), V (L), n (mol), T (K) that satisfy PV = nRT with P exact."""
    def draw():
        t = rng.choice(KELVINS)
        n = rng.choice(QUARTERS)
        v = rng.choice(range(1, 41))
        p = n * R * t / v
        return (p, v, n, t) if exact(p) and Fraction(1, 10) <= p <= 30 else None
    return _find(rng, draw)


@question_type(
    "chem.ideal_gas_foundation",
    display_name={"th": "กฎของอาโวกาโดรและปริมาตรแก๊สที่ STP"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_IDEAL,
)
class IdealGasFoundation(QuestionType):
    """Equal volumes hold equal moles; a mole takes 22.4 L at STP."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            def draw():
                v1 = rng.randint(1, 40)
                n1, n2 = rng.sample(QUARTERS, 2)
                v2 = v1 * n2 / n1
                return (v1, n1, n2, v2) if exact(v2) else None

            v1, n1, n2, v2 = _find(rng, draw)
            return numeric(stem=f"แก๊ส {show(n1)} โมล มีปริมาตร {v1} L ที่อุณหภูมิและความดันคงที่ "
                                f"แก๊ส {show(n2)} โมล จะมีปริมาตรเท่าใด",
                           answer=v2, wrongs=[v1 * n1 / n2, v1 * n2, v1 + n2 - n1 if v1 + n2 > n1 else v1 * 2],
                           unit="L", topic=TOPIC_IDEAL,
                           hint="กฎของอาโวกาโดร: ที่ T และ P คงที่ V₁/n₁ = V₂/n₂")
        formula = rng.choice(sorted(STABLE_GASES))
        n = rng.choice(QUARTERS)
        mass = n * GASES[formula][1]
        hint = "ที่ STP (0 °C, 1 atm) แก๊ส 1 โมลมีปริมาตร 22.4 L และจำนวนโมล = มวล ÷ มวลโมเลกุล"
        if kind == 1:
            return numeric(stem=f"{gas(formula)} {show(mass)} กรัม ที่ STP มีปริมาตรกี่ลิตร "
                                f"(มวลโมเลกุล {GASES[formula][1]})",
                           answer=n * STP_VOLUME, wrongs=[mass * STP_VOLUME, n * Fraction(245, 10), STP_VOLUME],
                           unit="L", topic=TOPIC_IDEAL, hint=hint)
        return numeric(stem=f"{gas(formula)} ปริมาตร {show(n * STP_VOLUME)} L ที่ STP มีมวลกี่กรัม "
                            f"(มวลโมเลกุล {GASES[formula][1]})",
                       answer=mass, wrongs=[n, mass * 2, GASES[formula][1]], unit="กรัม", topic=TOPIC_IDEAL, hint=hint)


@question_type(
    "chem.ideal_gas_fluency",
    display_name={"th": "คำนวณด้วยกฎแก๊สอุดมคติ PV = nRT"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_IDEAL,
)
class IdealGasFluency(QuestionType):
    """Hide one of P, V, n and T and solve PV = nRT for it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        p, v, n, t = ideal_case(rng)
        hide = rng.choice("PVnT")
        hint = "PV = nRT โดย P เป็น atm, V เป็น L และ T เป็นเคลวิน (K = °C + 273)"
        given = {"P": f"ความดัน {show(p)} atm", "V": f"ปริมาตร {v} L", "n": f"{show(n)} โมล",
                 "T": f"อุณหภูมิ {celsius(t)}"}
        known = " ".join(given[k] for k in "nVTP" if k != hide)
        if hide == "P":
            return numeric(stem=f"แก๊ส {known} มีความดันกี่ atm {R_TEXT}", answer=p,
                           wrongs=[n * R * (t - 273) / v if t != 273 else p * 2, n * t / v, p * 10], unit="atm",
                           topic=TOPIC_IDEAL, hint=hint)
        if hide == "V":
            return numeric(stem=f"แก๊ส {known} มีปริมาตรกี่ลิตร {R_TEXT}", answer=v,
                           wrongs=[p / (n * R * t), v * 2, n * STP_VOLUME if n * STP_VOLUME != v else v + 1],
                           unit="L", topic=TOPIC_IDEAL, hint=hint)
        if hide == "n":
            return numeric(stem=f"แก๊สที่มี{known} มีจำนวนกี่โมล {R_TEXT}", answer=n,
                           wrongs=[n * 2, n + 1, Fraction(v) / STP_VOLUME if exact(Fraction(v) / STP_VOLUME) else n * 4],
                           unit="โมล", topic=TOPIC_IDEAL, hint=hint)
        return numeric(stem=f"แก๊ส {known} มีอุณหภูมิกี่เคลวิน {R_TEXT}", answer=t,
                       wrongs=[t - 273 if t != 273 else 546, t + 273, t * 2], unit="K", topic=TOPIC_IDEAL, hint=hint)


@question_type(
    "chem.ideal_gas_application",
    display_name={"th": "มวลโมเลกุลของแก๊สจากกฎแก๊สอุดมคติ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_IDEAL,
)
class IdealGasApplication(QuestionType):
    """M = mRT / PV: find the molar mass, then name the gas."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        p, v, n, t = ideal_case(rng)
        formula = rng.choice(sorted(STABLE_GASES))
        molar = GASES[formula][1]
        mass = n * molar
        stem = (f"แก๊สชนิดหนึ่งหนัก {show(mass)} กรัม มีปริมาตร {v} L ที่ความดัน {show(p)} atm "
                f"และอุณหภูมิ {celsius(t)}")
        hint = "n = PV/RT แล้วมวลโมเลกุล = มวล ÷ n (หรือ M = mRT/PV)"
        if rng.random() < 0.5:
            return numeric(stem=f"{stem} มวลโมเลกุลของแก๊สนี้เท่าใด {R_TEXT}", answer=molar,
                           wrongs=[molar * 2, mass, n], unit="g/mol", topic=TOPIC_IDEAL, hint=hint)
        others = [f for f in sorted(STABLE_GASES) if f != formula]
        return _labelled(stem=f"{stem} แก๊สนี้น่าจะเป็นแก๊สใด {R_TEXT}", correct=f"{formula} (มวลโมเลกุล {molar})",
                         wrongs=tuple(f"{f} (มวลโมเลกุล {GASES[f][1]})" for f in rng.sample(others, 3)),
                         topic=TOPIC_IDEAL, hint=hint)
