"""สารละลายบัฟเฟอร์

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.5/22

Sets moved here from: science_wave_f37.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.distractors import near_length_sample
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f24 import _find
from otk.sets._support.science_wave_f36 import log_note, ph_of, sci_text, tabled
from otk.sets._support.science_wave_f37 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_BUFFER = "สารละลายบัฟเฟอร์"


BUFFERS = (("CH₃COOH", "CH₃COONa"), ("HF", "NaF"), ("HCOOH", "HCOONa"), ("H₂CO₃", "NaHCO₃"),
           ("NH₃", "NH₄Cl"), ("NaH₂PO₄", "Na₂HPO₄"), ("HCN", "KCN"))


NOT_BUFFERS = (("HCl", "NaCl"), ("NaOH", "NaCl"), ("HNO₃", "KNO₃"), ("HCl", "NaOH"), ("KOH", "KCl"), ("H₂SO₄", "Na₂SO₄"),
               ("NaOH", "CH₃COONa"), ("HNO₃", "CH₃COOH"), ("Ca(OH)₂", "CaCl₂"), ("HClO₄", "KClO₄"))


# (buffer, what is added, the reaction that soaks it up)
BUFFER_ACTIONS = (
    ("CH₃COOH/CH₃COO⁻", "กรดเล็กน้อย", "CH₃COO⁻ + H₃O⁺ → CH₃COOH + H₂O"),
    ("CH₃COOH/CH₃COO⁻", "เบสเล็กน้อย", "CH₃COOH + OH⁻ → CH₃COO⁻ + H₂O"),
    ("NH₃/NH₄⁺", "กรดเล็กน้อย", "NH₃ + H₃O⁺ → NH₄⁺ + H₂O"),
    ("NH₃/NH₄⁺", "เบสเล็กน้อย", "NH₄⁺ + OH⁻ → NH₃ + H₂O"),
    ("H₂CO₃/HCO₃⁻", "กรดเล็กน้อย", "HCO₃⁻ + H₃O⁺ → H₂CO₃ + H₂O"),
    ("H₂CO₃/HCO₃⁻", "เบสเล็กน้อย", "H₂CO₃ + OH⁻ → HCO₃⁻ + H₂O"),
    ("HF/F⁻", "กรดเล็กน้อย", "F⁻ + H₃O⁺ → HF + H₂O"),
    ("HF/F⁻", "เบสเล็กน้อย", "HF + OH⁻ → F⁻ + H₂O"),
)


@question_type(
    "chem.buffer_foundation",
    display_name={"th": "องค์ประกอบของสารละลายบัฟเฟอร์"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_BUFFER,
)
class BufferFoundation(QuestionType):
    """A weak acid with its salt, or a weak base with its salt."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        right = rng.choice(BUFFERS)
        text = lambda pair: f"{pair[0]} กับ {pair[1]}"
        wrongs = near_length_sample(rng, NOT_BUFFERS, text(right), key=text)
        if rng.random() < 0.6:
            return _labelled(stem="สารคู่ใดผสมกันแล้วได้สารละลายบัฟเฟอร์", correct=text(right),
                             wrongs=tuple(text(w) for w in wrongs), topic=TOPIC_BUFFER,
                             hint="บัฟเฟอร์ = กรดอ่อนกับเกลือของกรดอ่อนนั้น หรือเบสอ่อนกับเกลือของเบสอ่อนนั้น")
        facts = (
            ("สารละลายบัฟเฟอร์มีสมบัติอย่างไร", "รักษา pH ให้เปลี่ยนแปลงน้อยเมื่อเติมกรดหรือเบสเล็กน้อย",
             ("มี pH เท่ากับ 7 เสมอ ไม่ว่าจะเติมกรดหรือเบสเท่าใด", "เปลี่ยน pH ได้มากเมื่อเติมกรดหรือเบสเพียงเล็กน้อย", "ทำให้สารละลายเป็นกลางทันทีเมื่อเติมกรดหรือเบส")),
            ("บัฟเฟอร์ในเลือดของคนที่ช่วยรักษา pH ประมาณ 7.4 คือคู่ใด", "H₂CO₃/HCO₃⁻",
             ("HCl/Cl⁻", "NaOH/Na⁺", "H₂SO₄/SO₄²⁻")),
            ("บัฟเฟอร์ภายในเซลล์ที่สำคัญคือคู่ใด", "H₂PO₄⁻/HPO₄²⁻", ("HNO₃/NO₃⁻", "H₂SO₄/SO₄²⁻", "HClO₄/ClO₄⁻")),
        )
        stem, right_text, wrongs_text = rng.choice(facts)
        return _labelled(stem=stem, correct=right_text, wrongs=wrongs_text, topic=TOPIC_BUFFER,
                         hint="บัฟเฟอร์มีทั้งกรดอ่อนไว้รับ OH⁻ และคู่เบสไว้รับ H₃O⁺")


@question_type(
    "chem.buffer_fluency",
    display_name={"th": "สารละลายบัฟเฟอร์รักษา pH ได้อย่างไร"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_BUFFER,
)
class BufferFluency(QuestionType):
    """Added acid meets the conjugate base; added base meets the weak acid."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        buffer, added, reaction = rng.choice(BUFFER_ACTIONS)
        same = [a[2] for a in BUFFER_ACTIONS if a[0] == buffer and a[2] != reaction]
        others = [a[2] for a in BUFFER_ACTIONS if a[0] != buffer]
        return _labelled(stem=f"เติม{added}ลงในบัฟเฟอร์ {buffer} สมการใดแสดงการรักษา pH", correct=reaction,
                         wrongs=(*same, *rng.sample(others, 3 - len(same))), topic=TOPIC_BUFFER,
                         hint="เติมกรด: คู่เบสในบัฟเฟอร์รับ H₃O⁺ เติมเบส: กรดอ่อนในบัฟเฟอร์ให้ H⁺ แก่ OH⁻")


@question_type(
    "chem.buffer_application",
    display_name={"th": "คำนวณ pH ของสารละลายบัฟเฟอร์"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_BUFFER,
)
class BufferApplication(QuestionType):
    """[H₃O⁺] = Ka × [HA] ÷ [A⁻]."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        def draw():
            ka = Fraction(rng.choice((1, 2, 4, 5))) / Fraction(10) ** rng.randint(4, 6)
            acid = rng.choice((Fraction(1, 10), Fraction(1, 5), Fraction(1, 2), Fraction(1)))
            salt = rng.choice((Fraction(1, 10), Fraction(1, 5), Fraction(1, 2), Fraction(1)))
            h = ka * acid / salt
            return (ka, acid, salt, h) if tabled(h) else None

        ka, acid, salt, h = _find(rng, draw)
        name = rng.choice(("HA", "HX", "HB"))
        return numeric(stem=f"บัฟเฟอร์ประกอบด้วยกรดอ่อน {name} {show(acid)} mol/dm³ กับเกลือ Na{name[1:]} {show(salt)} mol/dm³ "
                            f"ถ้า Ka ของ {name} = {sci_text(ka)} สารละลายนี้มี pH เท่าใด{log_note(h)}",
                       answer=ph_of(h), wrongs=[ph_of(ka) if ph_of(ka) != ph_of(h) else ph_of(h) + 1, 14 - ph_of(h),
                                                ph_of(h) + 1], unit="", topic=TOPIC_BUFFER,
                       hint="[H₃O⁺] = Ka × [กรดอ่อน] ÷ [เกลือ] แล้ว pH = −log[H₃O⁺]")
