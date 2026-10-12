"""ทฤษฎีกรด-เบส

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.5/14

Sets moved here from: science_wave_f35.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f35 import BL_REACTIONS, SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_THEORY = "ทฤษฎีกรด-เบส"


ARRHENIUS_ACIDS = ("HCl", "HNO₃", "H₂SO₄", "CH₃COOH", "HF", "HBr")


ARRHENIUS_BASES = ("NaOH", "KOH", "Ca(OH)₂", "Ba(OH)₂", "LiOH")


NEITHER = ("NaCl", "C₂H₅OH", "C₆H₁₂O₆", "KNO₃", "CH₄")


# (equation, Lewis acid (pair acceptor), Lewis base (pair donor))
LEWIS = (
    ("BF₃ + NH₃ → F₃B–NH₃", "BF₃", "NH₃"),
    ("Cu²⁺ + 4NH₃ → [Cu(NH₃)₄]²⁺", "Cu²⁺", "NH₃"),
    ("Ag⁺ + 2NH₃ → [Ag(NH₃)₂]⁺", "Ag⁺", "NH₃"),
    ("AlCl₃ + Cl⁻ → AlCl₄⁻", "AlCl₃", "Cl⁻"),
    ("H⁺ + OH⁻ → H₂O", "H⁺", "OH⁻"),
    ("Fe³⁺ + 6H₂O → [Fe(H₂O)₆]³⁺", "Fe³⁺", "H₂O"),
    ("BCl₃ + Cl⁻ → BCl₄⁻", "BCl₃", "Cl⁻"),
    ("Zn²⁺ + 4OH⁻ → [Zn(OH)₄]²⁻", "Zn²⁺", "OH⁻"),
)


DEFINITIONS = {
    "อาร์เรเนียส": ("กรดคือสารที่ละลายน้ำแล้วให้ H₃O⁺ (H⁺) เบสคือสารที่ละลายน้ำแล้วให้ OH⁻"),
    "เบรินสเตด-ลาวรี": ("กรดคือสารที่ให้โปรตอน (H⁺) เบสคือสารที่รับโปรตอน"),
    "ลิวอิส": ("กรดคือสารที่รับคู่อิเล็กตรอน เบสคือสารที่ให้คู่อิเล็กตรอน"),
}


@question_type(
    "chem.acid_base_theory_foundation",
    display_name={"th": "นิยามกรด-เบสตามทฤษฎีต่าง ๆ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_THEORY,
)
class AcidBaseTheoryFoundation(QuestionType):
    """Arrhenius: H⁺/OH⁻ in water. Brønsted-Lowry: proton donor/acceptor. Lewis: pair acceptor/donor."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = "อาร์เรเนียส: ให้ H⁺ หรือ OH⁻ ในน้ำ เบรินสเตด-ลาวรี: ให้หรือรับโปรตอน ลิวอิส: รับหรือให้คู่อิเล็กตรอน"
        if rng.random() < 0.4:
            theory = rng.choice(sorted(DEFINITIONS))
            wrong_swap = {"อาร์เรเนียส": "กรดคือสารที่ละลายน้ำแล้วให้ OH⁻ เบสคือสารที่ละลายน้ำแล้วให้ H₃O⁺",
                          "เบรินสเตด-ลาวรี": "กรดคือสารที่รับโปรตอน เบสคือสารที่ให้โปรตอน",
                          "ลิวอิส": "กรดคือสารที่ให้คู่อิเล็กตรอน เบสคือสารที่รับคู่อิเล็กตรอน"}
            others = [v for k, v in DEFINITIONS.items() if k != theory]
            return _labelled(stem=f"ตามทฤษฎีกรด-เบสของ{theory} กรดและเบสหมายถึงอะไร", correct=DEFINITIONS[theory],
                             wrongs=(wrong_swap[theory], *others), topic=TOPIC_THEORY, hint=hint)
        kind = rng.choice(("กรด", "เบส"))
        pick = rng.choice(ARRHENIUS_ACIDS if kind == "กรด" else ARRHENIUS_BASES)
        wrong_pool = list(NEITHER) + list(ARRHENIUS_BASES if kind == "กรด" else ARRHENIUS_ACIDS) + ["NH₃"] * (kind == "เบส")
        return _labelled(stem=f"สารใดเป็น{kind}ตามทฤษฎีของอาร์เรเนียส", correct=pick,
                         wrongs=tuple(sorted(set(wrong_pool))), topic=TOPIC_THEORY,
                         hint="กรดอาร์เรเนียสแตกตัวให้ H⁺ ในน้ำ เบสอาร์เรเนียสแตกตัวให้ OH⁻ ในน้ำ (NH₃ ไม่มี OH⁻ ในสูตร)")


@question_type(
    "chem.acid_base_theory_fluency",
    display_name={"th": "ระบุกรดและเบสเบรินสเตด-ลาวรีในปฏิกิริยา"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_THEORY,
)
class AcidBaseTheoryFluency(QuestionType):
    """Whoever gives up H⁺ is the acid; whoever takes it is the base."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        eq, acid, base, conj_acid, conj_base = rng.choice(BL_REACTIONS)
        want = rng.choice(("กรด", "เบส"))
        right = acid if want == "กรด" else base
        other = base if want == "กรด" else acid
        options = [other, conj_acid, conj_base]
        return _labelled(stem=f"ในปฏิกิริยาไปข้างหน้า {eq} สารใดทำหน้าที่เป็น{want}ตามทฤษฎีเบรินสเตด-ลาวรี", correct=right,
                         wrongs=tuple(options),
                         topic=TOPIC_THEORY,
                         hint="สารที่เสีย H⁺ (มี H น้อยลงหนึ่งอะตอมทางขวา) คือกรด สารที่รับ H⁺ คือเบส")


@question_type(
    "chem.acid_base_theory_application",
    display_name={"th": "กรดและเบสตามทฤษฎีของลิวอิส และเปรียบเทียบทฤษฎี"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_THEORY,
)
class AcidBaseTheoryApplication(QuestionType):
    """Lewis acids take a lone pair; some substances are bases only by the wider theories."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            eq, acid, base = rng.choice(LEWIS)
            want = rng.choice(("กรด", "เบส"))
            right = f"{acid} เพราะรับคู่อิเล็กตรอน" if want == "กรด" else f"{base} เพราะให้คู่อิเล็กตรอน"
            wrongs = (f"{base} เพราะรับคู่อิเล็กตรอน" if want == "กรด" else f"{acid} เพราะให้คู่อิเล็กตรอน",
                      f"{acid} เพราะให้โปรตอน" if want == "กรด" else f"{base} เพราะรับโปรตอน",
                      f"{base} เพราะให้คู่อิเล็กตรอน" if want == "กรด" else f"{acid} เพราะรับคู่อิเล็กตรอน")
            return _labelled(stem=f"ในปฏิกิริยา {eq} สารใดเป็น{want}ตามทฤษฎีของลิวอิส", correct=right, wrongs=wrongs,
                             topic=TOPIC_THEORY,
                             hint="กรดลิวอิสมีออร์บิทัลว่างรับคู่อิเล็กตรอน (ไอออนบวก BF₃ AlCl₃) เบสลิวอิสมีคู่อิเล็กตรอนโดดเดี่ยว")
        cases = (
            ("NH₃", "เป็นเบสตามเบรินสเตด-ลาวรีและลิวอิส แต่ไม่เป็นเบสตามอาร์เรเนียส"),
            ("BF₃", "เป็นกรดตามลิวอิสเท่านั้น เพราะไม่มี H⁺ ให้"),
            ("NaOH", "เป็นเบสได้ตามทั้งสามทฤษฎี"),
            ("HCl", "เป็นกรดตามอาร์เรเนียสและเบรินสเตด-ลาวรี"),
            ("Cu²⁺", "เป็นกรดตามลิวอิสเท่านั้น เพราะรับคู่อิเล็กตรอนจากลิแกนด์"),
        )
        name, right = rng.choice(cases)
        others = [c[1] for c in cases if c[0] != name]
        return _labelled(stem=f"ข้อใดกล่าวถึง {name} ได้ถูกต้อง", correct=right, wrongs=tuple(others),
                         topic=TOPIC_THEORY, hint="ทฤษฎีของลิวอิสกว้างที่สุด เบรินสเตด-ลาวรีรองลงมา อาร์เรเนียสแคบที่สุด (ต้องอยู่ในน้ำ)")
