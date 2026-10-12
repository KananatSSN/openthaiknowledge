"""การแพร่ของแก๊สและกฎการแพร่ผ่านของเกรแฮม

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.5/5

Sets moved here from: science_wave_f25.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f24 import _find, exact
from otk.sets._support.science_wave_f25 import GASES, SUBJECT, UPPER_FIVE, gas

PROVENANCE = Provenance("original")


TOPIC_GRAHAM = "การแพร่ของแก๊สและกฎการแพร่ผ่านของเกรแฮม"


def root_ratio(heavy: int, light: int):
    """√(heavy / light) when it is exact to two places, else None."""
    ratio = Fraction(heavy, light)
    num, den = ratio.numerator, ratio.denominator
    rn, rd = round(num ** 0.5), round(den ** 0.5)
    if rn * rn == num and rd * rd == den and exact(Fraction(rn, rd)):
        return Fraction(rn, rd)
    return None


GRAHAM_PAIRS = tuple((a, b, root_ratio(GASES[b][1], GASES[a][1]))
                     for a in GASES for b in GASES
                     if GASES[a][1] < GASES[b][1] and root_ratio(GASES[b][1], GASES[a][1]))


KINETIC_FACTS = (
    ("ที่อุณหภูมิเดียวกัน โมเลกุลของแก๊สต่างชนิดกันมีพลังงานจลน์เฉลี่ยเป็นอย่างไร", "เท่ากัน",
     ("แก๊สมวลมากมีพลังงานจลน์มากกว่า", "แก๊สมวลน้อยมีพลังงานจลน์มากกว่า", "ขึ้นกับปริมาตรภาชนะ")),
    ("ที่อุณหภูมิเดียวกัน เหตุใดแก๊สที่มีมวลโมเลกุลน้อยจึงแพร่ได้เร็วกว่า",
     "พลังงานจลน์เฉลี่ยเท่ากัน โมเลกุลที่เบากว่าจึงมีอัตราเร็วมากกว่า",
     ("โมเลกุลที่เบากว่ามีพลังงานจลน์มากกว่า", "โมเลกุลที่เบากว่าชนกันน้อยกว่าเสมอ", "โมเลกุลที่เบากว่ามีขนาดใหญ่กว่า")),
    ("เมื่อเพิ่มอุณหภูมิ อัตราการแพร่ของแก๊สเป็นอย่างไร", "เพิ่มขึ้น เพราะโมเลกุลเคลื่อนที่เร็วขึ้น",
     ("ลดลง เพราะโมเลกุลขยายตัว", "ไม่เปลี่ยน เพราะมวลเท่าเดิม", "ลดลง เพราะชนกันบ่อยขึ้น")),
    ("ปล่อยแก๊ส NH₃ และ HCl จากปลายคนละด้านของหลอดแก้วพร้อมกัน วงแหวนขาวของ NH₄Cl เกิดที่ใด",
     "ใกล้ปลายด้าน HCl เพราะ NH₃ เบากว่าจึงแพร่ได้เร็วกว่า",
     ("ใกล้ปลายด้าน NH₃ เพราะ NH₃ เบากว่า", "ตรงกลางหลอดพอดี", "ใกล้ปลายด้าน HCl เพราะ HCl แพร่เร็วกว่า")),
)


@question_type(
    "chem.graham_diffusion_foundation",
    display_name={"th": "การแพร่ของแก๊สตามทฤษฎีจลน์"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_GRAHAM,
)
class GrahamDiffusionFoundation(QuestionType):
    """Lighter molecules move faster at the same temperature."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = "ที่อุณหภูมิเดียวกัน พลังงานจลน์เฉลี่ยเท่ากัน แก๊สที่มีมวลโมเลกุลน้อยเคลื่อนที่และแพร่ได้เร็วกว่า"
        if rng.random() < 0.3:
            stem, right, wrongs = rng.choice(KINETIC_FACTS)
            return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_GRAHAM, hint=hint)
        names = rng.sample(sorted(GASES), 4)
        fastest = rng.random() < 0.5
        pick = (min if fastest else max)(names, key=lambda f: GASES[f][1])
        return _labelled(stem=f"ที่อุณหภูมิและความดันเดียวกัน แก๊สใดแพร่ได้{'เร็ว' if fastest else 'ช้า'}ที่สุด",
                         correct=pick, wrongs=tuple(f for f in names if f != pick), topic=TOPIC_GRAHAM, hint=hint)


@question_type(
    "chem.graham_diffusion_fluency",
    display_name={"th": "เปรียบเทียบอัตราการแพร่และเวลาที่ใช้แพร่"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_GRAHAM,
)
class GrahamDiffusionFluency(QuestionType):
    """r₁/r₂ = √(M₂/M₁); time runs the other way."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        light, heavy, ratio = rng.choice(GRAHAM_PAIRS)
        hint = "r₁/r₂ = √(M₂/M₁) และเวลาที่ใช้แพร่แปรผกผันกับอัตราการแพร่"
        masses = f"(มวลโมเลกุล {light} = {GASES[light][1]}, {heavy} = {GASES[heavy][1]})"
        ratio_sq = Fraction(GASES[heavy][1], GASES[light][1])
        if rng.random() < 0.5:
            return numeric(stem=f"ที่ภาวะเดียวกัน {gas(light)} แพร่ได้เร็วกว่า{gas(heavy)} กี่เท่า {masses}",
                           answer=ratio, wrongs=[ratio_sq, 1 / ratio if exact(1 / ratio) else ratio + 1, ratio * 2],
                           unit="เท่า", topic=TOPIC_GRAHAM, hint=hint)
        seconds = rng.randint(5, 60)
        if rng.random() < 0.5:
            return numeric(stem=f"{gas(light)} ปริมาตรหนึ่งแพร่ผ่านรูเล็ก ๆ ใช้เวลา {seconds} วินาที "
                                f"{gas(heavy)} ปริมาตรเท่ากันที่ภาวะเดียวกันจะใช้เวลากี่วินาที {masses}",
                           answer=seconds * ratio, wrongs=[seconds * ratio_sq, seconds * ratio * 2, seconds + ratio],
                           unit="วินาที", topic=TOPIC_GRAHAM, hint=hint)
        slow = seconds * ratio
        return numeric(stem=f"{gas(heavy)} ปริมาตรหนึ่งแพร่ผ่านรูเล็ก ๆ ใช้เวลา {show(slow)} วินาที "
                            f"{gas(light)} ปริมาตรเท่ากันที่ภาวะเดียวกันจะใช้เวลากี่วินาที {masses}",
                       answer=seconds, wrongs=[slow * ratio, slow, seconds * 2], unit="วินาที",
                       topic=TOPIC_GRAHAM, hint=hint)


@question_type(
    "chem.graham_diffusion_application",
    display_name={"th": "หามวลโมเลกุลของแก๊สจากอัตราการแพร่"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_GRAHAM,
)
class GrahamDiffusionApplication(QuestionType):
    """M_x = M_known × (r_known / r_x)²; then name the gas."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            known = rng.choice(sorted(GASES))
            unknown = rng.choice([f for f in sorted(GASES) if f != known])
            speed = root_ratio(GASES[known][1], GASES[unknown][1])
            if speed is None:
                return None
            return known, unknown, speed

        known, unknown, speed = _find(rng, draw)
        molar = GASES[unknown][1]
        if speed >= 1:
            relation = f"แพร่ได้เร็วกว่า{gas(known)} {show(speed)} เท่า"
        else:
            relation = f"แพร่ได้ช้ากว่า{gas(known)} {show(1 / speed)} เท่า"
        stem = f"ที่ภาวะเดียวกัน แก๊ส X {relation} (มวลโมเลกุล {known} = {GASES[known][1]})"
        hint = "r_X / r_known = √(M_known / M_X) ยกกำลังสองทั้งสองข้างแล้วแก้หา M_X"
        if rng.random() < 0.5:
            return numeric(stem=f"{stem} มวลโมเลกุลของ X เท่าใด", answer=molar,
                           wrongs=[GASES[known][1] * speed if exact(GASES[known][1] * speed) else molar * 2,
                                   molar * 2, GASES[known][1] / speed if exact(GASES[known][1] / speed) else molar + 4],
                           unit="g/mol", topic=TOPIC_GRAHAM, hint=hint)
        others = [f for f in sorted(GASES) if f not in (unknown, known)]
        return _labelled(stem=f"{stem} แก๊ส X น่าจะเป็นแก๊สใด", correct=f"{unknown} (มวลโมเลกุล {molar})",
                         wrongs=tuple(f"{f} (มวลโมเลกุล {GASES[f][1]})" for f in rng.sample(others, 3)),
                         topic=TOPIC_GRAHAM, hint=hint)
