"""ความแรงของกรดและเบส

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.5/16

Sets moved here from: science_wave_f36.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f24 import _find, exact
from otk.sets._support.science_wave_f36 import SUBJECT, SUP, UPPER_FIVE, sci, sci_text

PROVENANCE = Provenance("original")


TOPIC_STRENGTH = "ความแรงของกรดและเบส"


STRONG_ACIDS = ("HCl", "HBr", "HI", "HNO₃", "H₂SO₄", "HClO₄")


WEAK_ACIDS = ("CH₃COOH", "HF", "HCN", "H₂CO₃", "HCOOH", "H₂S")


STRONG_BASES = ("NaOH", "KOH", "LiOH", "Ca(OH)₂", "Ba(OH)₂")


WEAK_BASES = ("NH₃", "CH₃NH₂")


GROUPS = {"กรดแก่": STRONG_ACIDS, "กรดอ่อน": WEAK_ACIDS, "เบสแก่": STRONG_BASES, "เบสอ่อน": WEAK_BASES}


PERCENTS = tuple(Fraction(x, 10) for x in (5, 10, 12, 13, 15, 20, 25, 40, 50))


CONCS = (Fraction(1, 20), Fraction(1, 10), Fraction(1, 5), Fraction(1, 2), Fraction(1), Fraction(1, 4))


@question_type(
    "chem.acid_strength_foundation",
    display_name={"th": "กรดแก่ กรดอ่อน เบสแก่ และเบสอ่อน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_STRENGTH,
)
class AcidStrengthFoundation(QuestionType):
    """Strong ones ionise completely; weak ones only in part."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = "กรดแก่และเบสแก่แตกตัวได้เกือบ 100% กรดอ่อนและเบสอ่อนแตกตัวได้เพียงบางส่วน"
        if rng.random() < 0.6:
            group = rng.choice(sorted(GROUPS))
            pick = rng.choice(GROUPS[group])
            others = [x for g, xs in GROUPS.items() if g != group for x in xs]
            return _labelled(stem=f"สารใดเป็น{group}", correct=pick, wrongs=tuple(others), topic=TOPIC_STRENGTH,
                             hint=hint)
        facts = (
            ("สารละลาย HCl และ CH₃COOH เข้มข้นเท่ากัน ข้อใดถูกต้อง", "HCl มี [H₃O⁺] มากกว่า เพราะแตกตัวได้สมบูรณ์",
             ("มี [H₃O⁺] เท่ากันเพราะเข้มข้นเท่ากัน", "CH₃COOH มี [H₃O⁺] มากกว่า", "CH₃COOH นำไฟฟ้าได้ดีกว่า")),
            ("ค่า Ka ของกรดอ่อนบอกอะไร", "ความสามารถในการแตกตัว Ka มากแสดงว่ากรดแรงกว่า",
             ("ความเข้มข้นของกรด", "จำนวน H ในโมเลกุลกรด", "อัตราการเกิดปฏิกิริยาของกรด")),
            ("กรดอ่อนเมื่อเจือจางลง ร้อยละการแตกตัวเป็นอย่างไร", "เพิ่มขึ้น แม้ [H₃O⁺] จะลดลง",
             ("ลดลง", "เท่าเดิมเสมอ", "เพิ่มขึ้น และ [H₃O⁺] ก็เพิ่มขึ้นด้วย")),
        )
        stem, right, wrongs = rng.choice(facts)
        return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_STRENGTH, hint=hint)


@question_type(
    "chem.acid_strength_fluency",
    display_name={"th": "คำนวณร้อยละการแตกตัวของกรดอ่อน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_STRENGTH,
)
class AcidStrengthFluency(QuestionType):
    """% ionised = [H₃O⁺] ÷ C × 100."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        # A generic weak acid: made-up data on a named acid would contradict its real Ka.
        acid = rng.choice(("HA", "HX", "HB"))
        c, p = rng.choice(CONCS), rng.choice(PERCENTS)
        h = c * p / 100
        hint = "ร้อยละการแตกตัว = ([H₃O⁺] ที่สมดุล ÷ ความเข้มข้นเริ่มต้นของกรด) × 100"
        if rng.random() < 0.5:
            return numeric(stem=f"สารละลายกรดอ่อน {acid} เข้มข้น {show(c)} mol/dm³ มี [H₃O⁺] = {sci_text(h)} mol/dm³ "
                                f"กรดนี้แตกตัวได้ร้อยละเท่าใด",
                           answer=p, wrongs=[p * 10, p / 10 if exact(p / 10) else p + 1, 100 - p], unit="%",
                           topic=TOPIC_STRENGTH, hint=hint)
        mantissa, power = sci(h)
        return numeric(stem=f"สารละลายกรดอ่อน {acid} เข้มข้น {show(c)} mol/dm³ แตกตัวได้ {show(p)}% [H₃O⁺] ที่สมดุลเท่ากับ "
                            f"a × 10{str(power).translate(SUP)} mol/dm³ ค่า a เท่าใด",
                       answer=mantissa, wrongs=[mantissa * 2 if mantissa * 2 < 10 else mantissa / 2, p if p != mantissa else p + 1,
                                                mantissa + 1 if mantissa + 1 < 10 else mantissa - 1], unit="",
                       topic=TOPIC_STRENGTH, hint=hint)


@question_type(
    "chem.acid_strength_application",
    display_name={"th": "ค่าคงที่การแตกตัว Ka และการเปรียบเทียบความแรงของกรด"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_STRENGTH,
)
class AcidStrengthApplication(QuestionType):
    """Ka ≈ [H₃O⁺]² ÷ C for a weak acid (C − x ≈ C); larger Ka, stronger acid."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            names = rng.sample(("HA", "HB", "HC", "HD", "HX"), 3)
            values = rng.sample([(m, e) for m in (1, 2, 4, 5, 6, 8) for e in (-4, -5, -6, -7, -9, -10)], 3)
            if len({e for _, e in values}) < 3:
                values = [(values[0][0], -4), (values[1][0], -6), (values[2][0], -9)]
            ka = {n: Fraction(m) * Fraction(10) ** e for n, (m, e) in zip(names, values)}
            strong = rng.random() < 0.5
            pick = (max if strong else min)(names, key=ka.get)
            listed = ", ".join(f"{n} Ka = {sci_text(v)}" for n, v in ka.items())
            return _labelled(stem=f"จากค่า Ka: {listed} กรดใดเป็นกรด{'แรง' if strong else 'อ่อน'}ที่สุด", correct=pick,
                             wrongs=tuple(n for n in names if n != pick) + ("แรงเท่ากันทุกตัว",), topic=TOPIC_STRENGTH,
                             hint="Ka มากกว่า กรดแตกตัวได้มากกว่าจึงแรงกว่า เทียบเลขชี้กำลังก่อน")

        def draw():
            c = rng.choice(CONCS)
            h = Fraction(rng.choice((1, 2, 3, 4, 5, 6)), 1) * Fraction(1, 10 ** rng.choice((2, 3)))
            if h >= c / 20:
                return None
            ka = h * h / c
            mantissa, _ = sci(ka)
            return (c, h, ka) if exact(mantissa) else None

        c, h, ka = _find(rng, draw)
        acid = rng.choice(("HA", "HX", "HB"))
        mantissa, power = sci(ka)
        return numeric(stem=f"สารละลายกรดอ่อน {acid} เข้มข้น {show(c)} mol/dm³ มี [H₃O⁺] = {sci_text(h)} mol/dm³ "
                            f"ถ้าถือว่าความเข้มข้นของกรดที่เหลือ ≈ ความเข้มข้นเริ่มต้น ค่า Ka = a × 10{str(power).translate(SUP)} ค่า a เท่าใด",
                       answer=mantissa, wrongs=[sci(h / c)[0], sci(h * h)[0],
                                                mantissa * 2 if mantissa * 2 < 10 else mantissa / 2],
                       unit="", topic=TOPIC_STRENGTH, hint="Ka = [H₃O⁺][A⁻] ÷ [HA] ≈ [H₃O⁺]² ÷ C")
