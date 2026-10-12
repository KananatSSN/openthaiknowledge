"""อัตราส่วนโดยมวลของธาตุตามกฎสัดส่วนคงที่

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 3 ม.4/7

Sets moved here from: science_wave_f42.
"""

from __future__ import annotations

from fractions import Fraction
from math import gcd
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f24 import _find, exact
from otk.sets._support.science_wave_f30 import ATOMIC, atoms, mass_of
from otk.sets._support.science_wave_f42 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_RATIO = "อัตราส่วนโดยมวลของธาตุตามกฎสัดส่วนคงที่"


RATIO_COMPOUNDS = ("H₂O", "CO₂", "MgO", "CaO", "NaCl", "Fe₂O₃", "CuO", "SO₂", "SO₃", "NH₃", "CH₄", "Al₂O₃", "FeS",
                   "CaCO₃", "H₂S", "NO₂", "CO", "ZnO", "MgS", "Na₂O")


def mass_ratio(formula: str) -> tuple[str, str, Fraction, Fraction]:
    (a, na), (b, nb) = atoms(formula)[:2]
    return a, b, ATOMIC[a] * na, ATOMIC[b] * nb


def ratio_text(x: Fraction, y: Fraction) -> str:
    scale = x.denominator * y.denominator
    p, q = int(x * scale), int(y * scale)
    g = gcd(p, q)
    return f"{p // g} : {q // g}"


@question_type(
    "chem.definite_proportion_foundation",
    display_name={"th": "อัตราส่วนโดยมวลของธาตุในสารประกอบ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_RATIO,
)
class DefiniteProportionFoundation(QuestionType):
    """Every sample of a compound holds its elements in the same mass ratio."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        formula = rng.choice([f for f in RATIO_COMPOUNDS if len(atoms(f)) == 2])
        a, b, ma, mb = mass_ratio(formula)
        if rng.random() < 0.5:
            def draw():
                k = Fraction(rng.randrange(1, 41), rng.choice((2, 4, 10)))
                return k if exact(ma * k) and exact(mb * k) else None

            k = _find(rng, draw)
            sample = lambda x, y: f"{a} {show(x)} กรัม กับ {b} {show(y)} กรัม"
            right_sample = sample(ma * k, mb * k)
            wrongs = [sample(mb * k, ma * k), sample(ma * k, mb * k * 2), sample(ma * k * 2, mb * k + 1)]
            wrongs = [w for w in dict.fromkeys(wrongs) if w != right_sample]
            while len(wrongs) < 3:
                wrongs.append(sample(ma * k + 1, mb * k))
            return _labelled(stem=f"ข้อมูลใดเป็นมวลของธาตุในตัวอย่าง {formula} ที่รวมกันพอดี (มวลอะตอม {a} = {show(ATOMIC[a])}, "
                                  f"{b} = {show(ATOMIC[b])})",
                             correct=right_sample, wrongs=tuple(wrongs[:3]), topic=TOPIC_RATIO,
                             hint="ตัวอย่างของสารประกอบเดียวกันต้องมีอัตราส่วนมวลของธาตุเท่ากันทุกตัวอย่าง")
        right = ratio_text(ma, mb)
        counts = dict(atoms(formula))
        wrongs = {ratio_text(ATOMIC[a], ATOMIC[b]), ratio_text(Fraction(counts[a]), Fraction(counts[b])), ratio_text(mb, ma)}
        wrongs.discard(right)
        wrongs = sorted(wrongs)
        while len(wrongs) < 3:
            wrongs.append(ratio_text(ma + ATOMIC[a], mb))
        given = ", ".join(f"{e} = {show(ATOMIC[e])}" for e in (a, b))
        return _labelled(stem=f"ใน {formula} มวลของ {a} ต่อ {b} เป็นอัตราส่วนเท่าใด (มวลอะตอม {given})", correct=right,
                         wrongs=tuple(dict.fromkeys(wrongs))[:3], topic=TOPIC_RATIO,
                         hint="มวลของธาตุ = มวลอะตอม × จำนวนอะตอมในสูตร แล้วทอนอัตราส่วนให้เป็นเลขจำนวนเต็มน้อยที่สุด")


@question_type(
    "chem.definite_proportion_fluency",
    display_name={"th": "ร้อยละโดยมวลของธาตุในสารประกอบ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_RATIO,
)
class DefiniteProportionFluency(QuestionType):
    """% element = mass of that element in the formula ÷ formula mass × 100."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            formula = rng.choice(RATIO_COMPOUNDS)
            element, count = rng.choice(atoms(formula))
            percent = ATOMIC[element] * count / mass_of(formula) * 100
            return (formula, element, count, percent) if exact(percent) else None

        formula, element, count, percent = _find(rng, draw)
        given = ", ".join(f"{e} = {show(ATOMIC[e])}" for e, _ in atoms(formula))
        if rng.random() < 0.5:
            def draw2():
                sample = Fraction(rng.randrange(1, 81), rng.choice((1, 2, 4)))
                part = sample * percent / 100
                return (sample, part) if exact(sample) and exact(part) else None

            sample, part = _find(rng, draw2)
            return numeric(stem=f"{formula} {show(sample)} กรัม มี {element} อยู่กี่กรัม (มวลอะตอม {given})", answer=part,
                           wrongs=[sample - part if sample - part != part else part * 2, part * 2, sample],
                           unit="กรัม", topic=TOPIC_RATIO,
                           hint="มวลของธาตุ = มวลตัวอย่าง × (ร้อยละโดยมวลของธาตุ ÷ 100)")
        return numeric(stem=f"{formula} มี {element} อยู่ร้อยละโดยมวลเท่าใด (มวลอะตอม {given})", answer=percent,
                       wrongs=[ATOMIC[element] / mass_of(formula) * 100 if count > 1 and exact(ATOMIC[element] / mass_of(formula) * 100) else 100 - percent,
                               100 - percent, percent / 2 if exact(percent / 2) else percent + 1],
                       unit="%", topic=TOPIC_RATIO, hint="ร้อยละโดยมวล = (มวลอะตอม × จำนวนอะตอม ÷ มวลสูตร) × 100")


@question_type(
    "chem.definite_proportion_application",
    display_name={"th": "มวลของธาตุที่รวมกันพอดีตามกฎสัดส่วนคงที่"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_RATIO,
)
class DefiniteProportionApplication(QuestionType):
    """The fixed ratio scales to any sample."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            formula = rng.choice([f for f in RATIO_COMPOUNDS if len(atoms(f)) == 2])
            a, b, ma, mb = mass_ratio(formula)
            k = Fraction(rng.randrange(1, 41), rng.choice((2, 4, 5, 10)))
            ga, gb = ma * k, mb * k
            extra = Fraction(rng.randrange(1, 21), 2)
            return (formula, a, b, ga, gb, extra) if exact(ga) and exact(gb) else None

        formula, a, b, ga, gb, extra = _find(rng, draw)
        if rng.random() < 0.5:
            return numeric(stem=f"ธาตุ {a} {show(ga)} กรัม รวมกับ {b} พอดีได้ {formula} ต้องใช้ {b} กี่กรัม "
                                f"(มวลอะตอม {a} = {show(ATOMIC[a])}, {b} = {show(ATOMIC[b])})",
                           answer=gb, wrongs=[ga, ga + gb, gb * 2], unit="กรัม", topic=TOPIC_RATIO,
                           hint="ใช้อัตราส่วนมวลของธาตุในสูตรซึ่งคงที่เสมอ")
        return numeric(stem=f"ผสม {a} {show(ga)} กรัม กับ {b} {show(gb + extra)} กรัม ให้เกิด {formula} จนปฏิกิริยาสิ้นสุด "
                            f"จะเหลือ {b} กี่กรัม (มวลอะตอม {a} = {show(ATOMIC[a])}, {b} = {show(ATOMIC[b])})",
                       answer=extra, wrongs=[gb, gb + extra, extra * 2], unit="กรัม", topic=TOPIC_RATIO,
                       hint="หามวลของ B ที่รวมกับ A พอดีตามอัตราส่วนคงที่ ส่วนที่เกินคือส่วนที่เหลือ")
