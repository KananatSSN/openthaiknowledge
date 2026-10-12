"""คู่กรด-เบสตามทฤษฎีเบรินสเตด-ลาวรี

เคมี · ม.5 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 2 ม.5/15

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


TOPIC_PAIR = "คู่กรด-เบสตามทฤษฎีเบรินสเตด-ลาวรี"


PAIRS = (("HCl", "Cl⁻"), ("H₂O", "OH⁻"), ("H₃O⁺", "H₂O"), ("NH₄⁺", "NH₃"), ("CH₃COOH", "CH₃COO⁻"),
         ("H₂CO₃", "HCO₃⁻"), ("HCO₃⁻", "CO₃²⁻"), ("HF", "F⁻"), ("H₂PO₄⁻", "HPO₄²⁻"), ("HPO₄²⁻", "PO₄³⁻"),
         ("H₃PO₄", "H₂PO₄⁻"), ("H₂SO₄", "HSO₄⁻"), ("HSO₄⁻", "SO₄²⁻"), ("H₂S", "HS⁻"), ("HS⁻", "S²⁻"),
         ("HNO₃", "NO₃⁻"), ("HCN", "CN⁻"), ("NH₃", "NH₂⁻"))


CONJ_BASE = dict(PAIRS)


CONJ_ACID = {b: a for a, b in PAIRS}


AMPHIPROTIC = sorted(set(CONJ_BASE) & set(CONJ_ACID))


ONLY_ACID = ("HCl", "HNO₃", "HF", "HCN", "CH₃COOH")


ONLY_BASE = ("Cl⁻", "NO₃⁻", "CO₃²⁻", "F⁻", "CN⁻", "SO₄²⁻", "S²⁻", "PO₄³⁻")


@question_type(
    "chem.conjugate_pair_foundation",
    display_name={"th": "คู่เบสของกรดและคู่กรดของเบส"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_PAIR,
)
class ConjugatePairFoundation(QuestionType):
    """The conjugate base has one H⁺ fewer; the conjugate acid one H⁺ more."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        acid, base = rng.choice(PAIRS)
        pool = sorted({x for p in PAIRS for x in p} - {acid, base})
        if rng.random() < 0.5:
            near = [x for x in (CONJ_ACID.get(acid), CONJ_BASE.get(base)) if x and x not in (acid, base)]
            first = list(dict.fromkeys(near))[:1]
            wrongs = first + rng.sample([p for p in pool if p not in near], 3 - len(first))
            return _labelled(stem=f"คู่เบสของ {acid} คือข้อใด", correct=base, wrongs=tuple(wrongs), topic=TOPIC_PAIR,
                             hint="คู่เบส = กรดที่เสีย H⁺ ไป 1 ตัว (H ลดลง 1 และประจุลดลง 1)")
        near = [x for x in (CONJ_BASE.get(base), CONJ_ACID.get(acid)) if x and x not in (acid, base)]
        first = list(dict.fromkeys(near))[:1]
        wrongs = first + rng.sample([p for p in pool if p not in near], 3 - len(first))
        return _labelled(stem=f"คู่กรดของ {base} คือข้อใด", correct=acid, wrongs=tuple(wrongs), topic=TOPIC_PAIR,
                         hint="คู่กรด = เบสที่รับ H⁺ มา 1 ตัว (H เพิ่ม 1 และประจุเพิ่ม 1)")


@question_type(
    "chem.conjugate_pair_fluency",
    display_name={"th": "ระบุคู่กรด-เบสในปฏิกิริยา"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_PAIR,
)
class ConjugatePairFluency(QuestionType):
    """Each acid pairs with the base it becomes."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        eq, acid, base, conj_acid, conj_base = rng.choice(BL_REACTIONS)
        if rng.random() < 0.5:
            right = rng.choice((f"{acid} กับ {conj_base}", f"{conj_acid} กับ {base}"))
            wrong_pairs = [f"{acid} กับ {base}", f"{conj_acid} กับ {conj_base}", f"{acid} กับ {conj_acid}",
                           f"{base} กับ {conj_base}"]
            return _labelled(stem=f"ข้อใดเป็นคู่กรด-เบสในปฏิกิริยา {eq}", correct=right,
                             wrongs=tuple(wrong_pairs), topic=TOPIC_PAIR,
                             hint="คู่กรด-เบสต่างกันเพียง H⁺ หนึ่งตัว และอยู่คนละฝั่งของสมการ")
        right = f"{acid}/{conj_base} และ {conj_acid}/{base}"
        wrongs = (f"{acid}/{base} และ {conj_acid}/{conj_base}", f"{acid}/{conj_acid} และ {base}/{conj_base}",
                  f"{base}/{conj_base} และ {acid}/{conj_acid}")
        return _labelled(stem=f"ปฏิกิริยา {eq} มีคู่กรด-เบส (กรด/คู่เบส) ตามข้อใด", correct=right, wrongs=wrongs,
                         topic=TOPIC_PAIR, hint="กรดที่ให้ H⁺ กลายเป็นคู่เบสของมัน เบสที่รับ H⁺ กลายเป็นคู่กรดของมัน")


@question_type(
    "chem.conjugate_pair_application",
    display_name={"th": "สารที่เป็นได้ทั้งกรดและเบส"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_PAIR,
)
class ConjugatePairApplication(QuestionType):
    """Amphiprotic species can give and take a proton."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        pick = rng.choice(AMPHIPROTIC)
        if rng.random() < 0.5:
            return _labelled(stem="สารใดเป็นได้ทั้งกรดและเบสตามทฤษฎีเบรินสเตด-ลาวรี", correct=pick,
                             wrongs=tuple(ONLY_ACID + ONLY_BASE), topic=TOPIC_PAIR,
                             hint="สารที่มี H ให้ได้และยังรับ H⁺ ได้ เช่น H₂O HCO₃⁻ HSO₄⁻ H₂PO₄⁻")
        return _labelled(stem=f"{pick} เมื่อทำหน้าที่เป็นกรดและเป็นเบส จะได้คู่เบสและคู่กรดตามข้อใด",
                         correct=f"เป็นกรดได้ {CONJ_BASE[pick]} เป็นเบสได้ {CONJ_ACID[pick]}",
                         wrongs=(f"เป็นกรดได้ {CONJ_ACID[pick]} เป็นเบสได้ {CONJ_BASE[pick]}",
                                 f"เป็นกรดได้ {CONJ_BASE[pick]} เป็นเบสได้ {CONJ_BASE[pick]}",
                                 f"เป็นกรดได้ {CONJ_ACID[pick]} เป็นเบสได้ {CONJ_ACID[pick]}"),
                         topic=TOPIC_PAIR, hint="เป็นกรด: เสีย H⁺ ได้คู่เบส เป็นเบส: รับ H⁺ ได้คู่กรด")
