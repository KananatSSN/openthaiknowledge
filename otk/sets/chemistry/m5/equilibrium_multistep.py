"""ค่าคงที่สมดุลของปฏิกิริยาหลายขั้นตอน

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.5/11

Sets moved here from: science_wave_f34.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import numeric, show
from otk.sets._support.science_wave_f24 import _find, exact
from otk.sets._support.science_wave_f34 import K_SYSTEMS, SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_MULTI = "ค่าคงที่สมดุลของปฏิกิริยาหลายขั้นตอน"


KS = tuple(Fraction(x, 100) for x in (10, 20, 25, 40, 50, 80, 125, 200, 250, 400, 500, 1000, 2000, 2500))


STEPS = (
    ("N₂(g) + O₂(g) ⇌ 2NO(g)", "2NO(g) + O₂(g) ⇌ 2NO₂(g)", "N₂(g) + 2O₂(g) ⇌ 2NO₂(g)"),
    ("H₂CO₃(aq) ⇌ H⁺(aq) + HCO₃⁻(aq)", "HCO₃⁻(aq) ⇌ H⁺(aq) + CO₃²⁻(aq)", "H₂CO₃(aq) ⇌ 2H⁺(aq) + CO₃²⁻(aq)"),
    ("C(s) + CO₂(g) ⇌ 2CO(g)", "2CO(g) + O₂(g) ⇌ 2CO₂(g)", "C(s) + O₂(g) ⇌ CO₂(g)"),
    ("SO₂(g) + ½O₂(g) ⇌ SO₃(g)", "SO₃(g) + H₂O(g) ⇌ H₂SO₄(g)", "SO₂(g) + ½O₂(g) + H₂O(g) ⇌ H₂SO₄(g)"),
    ("2NO₂(g) ⇌ N₂O₄(g)", "N₂O₄(g) + O₂(g) ⇌ 2NO₃(g)", "2NO₂(g) + O₂(g) ⇌ 2NO₃(g)"),
)


@question_type(
    "chem.equilibrium_multistep_foundation",
    display_name={"th": "ค่า K ของปฏิกิริยาย้อนกลับและเมื่อคูณสมการ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_MULTI,
)
class EquilibriumMultistepFoundation(QuestionType):
    """Reverse: 1/K. Multiply by n: Kⁿ. Halve: √K."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        system = rng.choice(K_SYSTEMS)
        kind = rng.randrange(3)
        hint = "กลับสมการ: K' = 1/K คูณสมการด้วย n: K' = Kⁿ หารสมการด้วย 2: K' = √K"
        if kind == 0:
            k = rng.choice([v for v in KS if exact(1 / v)])
            return numeric(stem=f"ปฏิกิริยา {system[0]} มี K = {show(k)} ปฏิกิริยาย้อนกลับมีค่าคงที่สมดุลเท่าใด",
                           answer=1 / k, wrongs=[k, k * 2, 2 / k], unit="", topic=TOPIC_MULTI, hint=hint)
        if kind == 1:
            k = rng.choice([v for v in KS if exact(v * v)])
            return numeric(stem=f"ปฏิกิริยา {system[0]} มี K = {show(k)} ถ้าคูณสมการด้วย 2 ค่าคงที่สมดุลใหม่เท่าใด",
                           answer=k * k, wrongs=[k * 2, k, k * k * 2], unit="", topic=TOPIC_MULTI, hint=hint)
        root = rng.choice((Fraction(1, 2), Fraction(1, 5), 2, 3, 4, 5, 10, 20))
        return numeric(stem=f"ปฏิกิริยา {system[0]} มี K = {show(root * root)} ถ้าหารสัมประสิทธิ์ในสมการด้วย 2 "
                            "ค่าคงที่สมดุลใหม่เท่าใด",
                       answer=root, wrongs=[root * root / 2 if exact(root * root / 2) else root * 2, root * root, root * 2],
                       unit="", topic=TOPIC_MULTI, hint=hint)


@question_type(
    "chem.equilibrium_multistep_fluency",
    display_name={"th": "ค่า K ของปฏิกิริยารวมจากปฏิกิริยาย่อย"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_MULTI,
)
class EquilibriumMultistepFluency(QuestionType):
    """Adding reactions multiplies their K."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            k1, k2 = rng.choice(KS), rng.choice(KS)
            k = k1 * k2
            return (k1, k2, k) if exact(k) else None

        k1, k2, k = _find(rng, draw)
        step1, step2, total = rng.choice(STEPS)
        return numeric(stem=f"ขั้นที่ 1: {step1} K₁ = {show(k1)} ขั้นที่ 2: {step2} K₂ = {show(k2)} "
                            f"ปฏิกิริยารวม {total} มีค่าคงที่สมดุลเท่าใด",
                       answer=k, wrongs=[k1 + k2, k1 / k2 if exact(k1 / k2) and k1 / k2 != k else k * 2,
                                         k2 / k1 if exact(k2 / k1) and k2 / k1 != k else k + 1], unit="", topic=TOPIC_MULTI,
                       hint="เมื่อบวกสมการเข้าด้วยกัน ค่า K ของปฏิกิริยารวม = K₁ × K₂")


@question_type(
    "chem.equilibrium_multistep_application",
    display_name={"th": "หาค่า K ของขั้นที่ไม่ทราบจากปฏิกิริยารวม"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_MULTI,
)
class EquilibriumMultistepApplication(QuestionType):
    """K_total = K₁ × K₂, so the missing step is K_total ÷ the known one; or a reversed step."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        step1, step2, total = rng.choice(STEPS)
        if rng.random() < 0.5:
            def draw():
                k1, k2 = rng.choice(KS), rng.choice(KS)
                return (k1, k2, k1 * k2) if exact(k1 * k2) else None

            k1, k2, k = _find(rng, draw)
            return numeric(stem=f"ปฏิกิริยารวม {total} มี K = {show(k)} ถ้าขั้นที่ 1 {step1} มี K₁ = {show(k1)} "
                                f"ขั้นที่ 2 {step2} มี K₂ เท่าใด",
                           answer=k2, wrongs=[k * k1 if exact(k * k1) and k * k1 != k2 else k2 * 2, k - k1 if k - k1 > 0 and k - k1 != k2 else k2 + 1,
                                              k1 if k1 != k2 else k1 * 2], unit="", topic=TOPIC_MULTI,
                           hint="K รวม = K₁ × K₂ จึงได้ K₂ = K รวม ÷ K₁")

        def draw():
            k1, k2 = rng.choice(KS), rng.choice(KS)
            k = k1 / k2
            return (k1, k2, k) if exact(k) and exact(1 / k2) else None

        k1, k2, k = _find(rng, draw)
        reverse2 = " ⇌ ".join(reversed(step2.split(" ⇌ ")))
        return numeric(stem=f"ปฏิกิริยา (1) {step1} มี K₁ = {show(k1)} ปฏิกิริยา (2) {reverse2} มี K₂ = {show(k2)} "
                            f"ถ้าต้องการปฏิกิริยา {total} ซึ่งได้จาก (1) บวกกับ (2) ที่กลับทิศแล้ว จะมีค่าคงที่สมดุลเท่าใด",
                       answer=k, wrongs=[k1 * k2 if k1 * k2 != k else k * 2, k2 / k1 if exact(k2 / k1) and k2 / k1 != k else k + 1,
                                         k * 2], unit="", topic=TOPIC_MULTI,
                       hint="กลับสมการ (2) ได้ค่าคงที่ 1/K₂ แล้วบวกกับ (1): K = K₁ × (1/K₂)")
