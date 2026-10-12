"""การเปลี่ยนแปลงความเข้มข้นและอัตราการเกิดปฏิกิริยาจนถึงภาวะสมดุล

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.5/8

Sets moved here from: science_wave_f33.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f24 import _find, exact
from otk.sets._support.science_wave_f33 import SUBJECT, UPPER_FIVE, approach_table

PROVENANCE = Provenance("original")


TOPIC_APPROACH = "การเปลี่ยนแปลงความเข้มข้นและอัตราการเกิดปฏิกิริยาจนถึงภาวะสมดุล"


APPROACH_SYSTEMS = (
    ("N₂O₄(g) ⇌ 2NO₂(g)", ["N₂O₄"], ["NO₂"]), ("H₂(g) + I₂(g) ⇌ 2HI(g)", ["H₂", "I₂"], ["HI"]),
    ("N₂(g) + 3H₂(g) ⇌ 2NH₃(g)", ["N₂", "H₂"], ["NH₃"]), ("2SO₂(g) + O₂(g) ⇌ 2SO₃(g)", ["SO₂", "O₂"], ["SO₃"]),
    ("PCl₅(g) ⇌ PCl₃(g) + Cl₂(g)", ["PCl₅"], ["PCl₃", "Cl₂"]), ("CO(g) + H₂O(g) ⇌ CO₂(g) + H₂(g)", ["CO", "H₂O"], ["CO₂", "H₂"]),
)


RATE_CHANGES = (
    ("เมื่อเริ่มผสมสารตั้งต้น อัตราการเกิดปฏิกิริยาไปข้างหน้าเปลี่ยนแปลงอย่างไรจนถึงภาวะสมดุล",
     "ลดลงจนคงที่ เพราะความเข้มข้นของสารตั้งต้นลดลง",
     ("เพิ่มขึ้นจนคงที่", "คงที่ตั้งแต่เริ่มต้น", "ลดลงจนเป็นศูนย์")),
    ("เมื่อเริ่มผสมสารตั้งต้น อัตราการเกิดปฏิกิริยาย้อนกลับเปลี่ยนแปลงอย่างไรจนถึงภาวะสมดุล",
     "เริ่มจากศูนย์แล้วเพิ่มขึ้นจนคงที่ เพราะผลิตภัณฑ์เกิดมากขึ้น",
     ("ลดลงจนเป็นศูนย์", "สูงที่สุดตั้งแต่เริ่มต้น", "คงที่ตลอดเวลา")),
    ("ที่ภาวะสมดุล อัตราการเกิดปฏิกิริยาไปข้างหน้าและย้อนกลับเป็นอย่างไร", "เท่ากันและไม่เป็นศูนย์",
     ("เป็นศูนย์ทั้งคู่", "ไปข้างหน้ามากกว่าเสมอ", "ย้อนกลับมากกว่าเสมอ")),
    ("ที่ภาวะสมดุล ความเข้มข้นของสารตั้งต้นและผลิตภัณฑ์เป็นอย่างไร", "คงที่ แต่ไม่จำเป็นต้องเท่ากัน",
     ("เท่ากันเสมอ", "ผลิตภัณฑ์มากกว่าสารตั้งต้นเสมอ", "เปลี่ยนแปลงขึ้นลงตลอดเวลา")),
)


@question_type(
    "chem.equilibrium_approach_foundation",
    display_name={"th": "อัตราไปข้างหน้าและย้อนกลับจนถึงภาวะสมดุล"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_APPROACH,
)
class EquilibriumApproachFoundation(QuestionType):
    """Forward rate falls, reverse rate rises, and they meet."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(RATE_CHANGES)
        if rng.random() < 0.5:
            return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_APPROACH,
                             hint="อัตราไปข้างหน้าขึ้นกับสารตั้งต้น อัตราย้อนกลับขึ้นกับผลิตภัณฑ์")
        eq, left_side, right_side = rng.choice(APPROACH_SYSTEMS)
        from_left = rng.random() < 0.5
        start_with = " และ ".join(left_side if from_left else right_side)
        hint = "ก่อนถึงสมดุล ปฏิกิริยาเกิดไปทางที่ยังไม่มีสาร สารฝั่งที่เริ่มต้นจึงลดลง สารอีกฝั่งเพิ่มขึ้น"
        if rng.random() < 0.5:
            faster = "อัตราไปข้างหน้ามากกว่าอัตราย้อนกลับ" if from_left else "อัตราย้อนกลับมากกว่าอัตราไปข้างหน้า"
            other = "อัตราย้อนกลับมากกว่าอัตราไปข้างหน้า" if from_left else "อัตราไปข้างหน้ามากกว่าอัตราย้อนกลับ"
            return _labelled(stem=f"ระบบ {eq} ในภาชนะปิด เริ่มจาก {start_with} เท่านั้น ก่อนเข้าสู่ภาวะสมดุล "
                                  "อัตราไปข้างหน้าเทียบกับอัตราย้อนกลับเป็นอย่างไร",
                             correct=faster, wrongs=(other, "เท่ากันตลอดเวลา", "ทั้งสองเป็นศูนย์"), topic=TOPIC_APPROACH,
                             hint=hint)
        species = rng.choice(left_side + right_side)
        falls = (species in left_side) == from_left
        right = "ลดลงแล้วคงที่" if falls else "เพิ่มขึ้นแล้วคงที่"
        return _labelled(stem=f"ระบบ {eq} ในภาชนะปิด เริ่มจาก {start_with} เท่านั้น ความเข้มข้นของ {species} "
                              "เปลี่ยนแปลงอย่างไรจนถึงภาวะสมดุล",
                         correct=right, wrongs=tuple(w for w in ("ลดลงแล้วคงที่", "เพิ่มขึ้นแล้วคงที่", "ลดลงจนเป็นศูนย์",
                                                                 "คงที่ตลอดเวลา") if w != right),
                         topic=TOPIC_APPROACH, hint=hint)


@question_type(
    "chem.equilibrium_approach_fluency",
    display_name={"th": "ความเข้มข้นที่เปลี่ยนไปของสารที่ไม่ได้วัดจนถึงภาวะสมดุล"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_APPROACH,
)
class EquilibriumApproachFluency(QuestionType):
    """The change in one species fixes the change in every other by the coefficients."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        systems = (("N₂O₄ ⇌ 2NO₂", "N₂O₄", 1, "NO₂", 2), ("2SO₂ + O₂ ⇌ 2SO₃", "O₂", 1, "SO₃", 2),
                   ("H₂ + I₂ ⇌ 2HI", "H₂", 1, "HI", 2), ("N₂ + 3H₂ ⇌ 2NH₃", "H₂", 3, "NH₃", 2),
                   ("PCl₅ ⇌ PCl₃ + Cl₂", "PCl₅", 1, "Cl₂", 1), ("2NO₂ ⇌ N₂O₄", "NO₂", 2, "N₂O₄", 1))

        def draw():
            eq, r, cr, p, cp = rng.choice(systems)
            start = Fraction(rng.randrange(20, 201, 10), 100)
            used = Fraction(rng.randrange(5, int(start * 100), 5), 100)
            made = used * cp / cr
            return (eq, r, cr, p, cp, start, used, made) if exact(made) else None

        eq, r, cr, p, cp, start, used, made = _find(rng, draw)
        left = start - used
        if rng.random() < 0.5:
            return numeric(stem=f"ปฏิกิริยา {eq} เริ่มต้น [{r}] = {show(start)} mol/dm³ และไม่มีผลิตภัณฑ์ ที่ภาวะสมดุล "
                                f"[{r}] = {show(left)} mol/dm³ ความเข้มข้นของ {p} ที่ภาวะสมดุลเท่าใด",
                           answer=made, wrongs=[used, left, made * 2 if made * 2 != used else made + 1],
                           unit="mol/dm³", topic=TOPIC_APPROACH,
                           hint="สารตั้งต้นที่ลดลงกับผลิตภัณฑ์ที่เกิดเป็นไปตามอัตราส่วนสัมประสิทธิ์ในสมการ")
        return numeric(stem=f"ปฏิกิริยา {eq} เริ่มต้น [{r}] = {show(start)} mol/dm³ และไม่มีผลิตภัณฑ์ ที่ภาวะสมดุล "
                            f"[{p}] = {show(made)} mol/dm³ ความเข้มข้นของ {r} ที่ภาวะสมดุลเท่าใด",
                       answer=left, wrongs=[start - made if start - made > 0 and start - made != left else start,
                                            used, start], unit="mol/dm³", topic=TOPIC_APPROACH,
                       hint="หา [สารตั้งต้นที่ใช้ไป] จากผลิตภัณฑ์ที่เกิดด้วยอัตราส่วนในสมการ แล้วลบออกจากค่าเริ่มต้น")


@question_type(
    "chem.equilibrium_approach_application",
    display_name={"th": "ร้อยละของสารตั้งต้นที่เปลี่ยนไปจนถึงภาวะสมดุล"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_APPROACH,
)
class EquilibriumApproachApplication(QuestionType):
    """Read the table to equilibrium, then how much of A turned into B."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        times, a, b = approach_table(rng)
        rows = "; ".join(f"{t} s: [A] = {show(x)}" for t, x in zip(times, a))
        if rng.random() < 0.5:
            percent = (a[0] - a[-1]) / a[0] * 100
            return numeric(stem=f"ปฏิกิริยา A ⇌ B ในภาชนะปิด เริ่มจาก A อย่างเดียว วัดได้ {rows} (mol/dm³) "
                                "ที่ภาวะสมดุล A เปลี่ยนเป็น B ไปร้อยละเท่าใด",
                           answer=percent, wrongs=[100 - percent, a[-1] / a[0] * 100 if a[-1] / a[0] * 100 != 100 - percent else percent / 2,
                                                   percent / 2], unit="%", topic=TOPIC_APPROACH,
                           hint="ร้อยละที่เปลี่ยน = (ความเข้มข้นที่ลดลง ÷ ความเข้มข้นเริ่มต้น) × 100")
        return numeric(stem=f"ปฏิกิริยา A ⇌ B ในภาชนะปิด เริ่มจาก A อย่างเดียว วัดได้ {rows} (mol/dm³) "
                            "ความเข้มข้นของ B ที่ภาวะสมดุลเท่าใด",
                       answer=b[-1], wrongs=[a[-1], a[0], b[-1] * 2], unit="mol/dm³", topic=TOPIC_APPROACH,
                       hint="A หนึ่งโมเลกุลเปลี่ยนเป็น B หนึ่งโมเลกุล [B] ที่สมดุล = [A] เริ่มต้น − [A] ที่สมดุล")
