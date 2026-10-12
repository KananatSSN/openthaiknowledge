"""ประเภทของปฏิกิริยาการเกิดพอลิเมอร์

เคมี · ม.6 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.6/11

Sets moved here from: science_wave_f28.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.distractors import near_length_sample
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f28 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_POLYMER = "ประเภทของปฏิกิริยาการเกิดพอลิเมอร์"


ADDITION, CONDENSATION = "แบบเติม", "แบบควบแน่น"


# (polymer, monomer(s), monomer structure, type, small molecule lost)
POLYMERS = (
    ("พอลิเอทิลีน (PE)", "เอทีน", "CH₂=CH₂", ADDITION, None),
    ("พอลิโพรพิลีน (PP)", "โพรพีน", "CH₂=CHCH₃", ADDITION, None),
    ("พอลิไวนิลคลอไรด์ (PVC)", "ไวนิลคลอไรด์", "CH₂=CHCl", ADDITION, None),
    ("พอลิสไตรีน (PS)", "สไตรีน", "CH₂=CHC₆H₅", ADDITION, None),
    ("พอลิเตตระฟลูออโรเอทิลีน (เทฟลอน)", "เตตระฟลูออโรเอทีน", "CF₂=CF₂", ADDITION, None),
    ("พอลิเมทิลเมทาคริเลต (อะคริลิก)", "เมทิลเมทาคริเลต", "CH₂=C(CH₃)COOCH₃", ADDITION, None),
    ("ยางธรรมชาติ (พอลิไอโซพรีน)", "ไอโซพรีน", "CH₂=C(CH₃)CH=CH₂", ADDITION, None),
    ("ไนลอน 6,6", "กรดเฮกเซนไดโออิกและเฮกเซน-1,6-ไดแอมีน", "HOOC(CH₂)₄COOH กับ H₂N(CH₂)₆NH₂", CONDENSATION, "H₂O"),
    ("พอลิเอทิลีนเทเรฟทาเลต (PET)", "กรดเทเรฟทาลิกและเอทิลีนไกลคอล", "HOOCC₆H₄COOH กับ HOCH₂CH₂OH",
     CONDENSATION, "H₂O"),
    ("โปรตีน", "กรดอะมิโน", "H₂NCH(R)COOH", CONDENSATION, "H₂O"),
    ("แป้งและเซลลูโลส", "กลูโคส", "C₆H₁₂O₆", CONDENSATION, "H₂O"),
    ("เบกาไลต์", "ฟีนอลและเมทานาล", "C₆H₅OH กับ HCHO", CONDENSATION, "H₂O"),
)


# (polymer, repeating unit, monomer molar mass)
REPEATS = (("พอลิเอทิลีน", "–CH₂–CH₂–", 28), ("พอลิโพรพิลีน", "–CH₂–CH(CH₃)–", 42),
           ("พอลิไวนิลคลอไรด์", "–CH₂–CHCl–", Fraction(125, 2)), ("พอลิสไตรีน", "–CH₂–CH(C₆H₅)–", 104),
           ("เทฟลอน", "–CF₂–CF₂–", 100))


@question_type(
    "chem.polymerization_foundation",
    display_name={"th": "ประเภทของปฏิกิริยาการเกิดพอลิเมอร์จากชื่อพอลิเมอร์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_POLYMER,
)
class PolymerizationFoundation(QuestionType):
    """Addition joins C=C monomers; condensation joins two groups and loses a small molecule."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        polymer, monomer, _, kind, _ = rng.choice(POLYMERS)
        hint = ("แบบเติม: มอนอเมอร์มีพันธะคู่ C=C และได้พอลิเมอร์เพียงอย่างเดียว "
                "แบบควบแน่น: มอนอเมอร์มีหมู่ฟังก์ชันสองหมู่ และได้โมเลกุลเล็ก เช่น H₂O ออกมาด้วย")
        if rng.random() < 0.5:
            return _labelled(stem=f"{polymer} เกิดจาก{monomer}ด้วยปฏิกิริยาการเกิดพอลิเมอร์แบบใด", correct=kind,
                             wrongs=(ADDITION if kind == CONDENSATION else CONDENSATION, "แบบแทนที่", "แบบสะปอนนิฟิเคชัน"),
                             topic=TOPIC_POLYMER, hint=hint)
        others = [p for p in POLYMERS if p[3] != kind]
        return _labelled(stem=f"พอลิเมอร์ใดเกิดจากปฏิกิริยาการเกิดพอลิเมอร์{kind}", correct=polymer,
                         wrongs=tuple(p[0] for p in rng.sample(others, 3)), topic=TOPIC_POLYMER, hint=hint)


@question_type(
    "chem.polymerization_fluency",
    display_name={"th": "ประเภทของปฏิกิริยาการเกิดพอลิเมอร์จากโครงสร้างมอนอเมอร์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_POLYMER,
)
class PolymerizationFluency(QuestionType):
    """Read the monomer: a C=C means addition, two reacting groups mean condensation."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        polymer, monomer, structure, kind, lost = rng.choice(POLYMERS)
        roll = rng.random()
        if roll < 0.35:
            others = [p for p in POLYMERS if p[3] != kind]
            return _labelled(stem=f"มอนอเมอร์ใดเกิดพอลิเมอร์ด้วยปฏิกิริยา{kind}", correct=structure,
                             wrongs=tuple(p[2] for p in near_length_sample(rng, others, structure, key=lambda p: p[2])), topic=TOPIC_POLYMER,
                             hint="แบบเติมต้องมี C=C ส่วนแบบควบแน่นต้องมีหมู่ฟังก์ชันสองหมู่ที่ทำปฏิกิริยากันได้")
        if roll < 0.55:
            none = "ไม่มีโมเลกุลเล็กออกมา ได้พอลิเมอร์อย่างเดียว"
            each = "ได้ {} ออกมาทุกครั้งที่มอนอเมอร์ต่อกัน".format
            right = each(lost) if lost else none
            wrongs = [w for w in (each("H₂O"), none, each("CO₂"), each("H₂")) if w != right]
            return _labelled(stem=f"การเกิด{polymer}จาก{monomer} ({structure}) ได้สารใดนอกจากพอลิเมอร์", correct=right,
                             wrongs=tuple(wrongs[:3]), topic=TOPIC_POLYMER,
                             hint="แบบควบแน่นเสียโมเลกุลเล็ก (ส่วนใหญ่คือ H₂O) ทุกครั้งที่มอนอเมอร์ต่อกัน แบบเติมไม่เสียอะไรเลย")
        if kind == ADDITION:
            right = "แบบเติม เพราะมอนอเมอร์มีพันธะคู่ C=C ที่เปิดออกได้"
        else:
            right = "แบบควบแน่น เพราะมอนอเมอร์มีหมู่ฟังก์ชันที่ทำปฏิกิริยากันได้"
        wrongs = ("แบบเติม เพราะมอนอเมอร์มีพันธะคู่ C=C ที่เปิดออกได้", "แบบควบแน่น เพราะมอนอเมอร์มีพันธะคู่ C=C ที่เปิดออกได้",
                  "แบบควบแน่น เพราะมอนอเมอร์มีหมู่ฟังก์ชันที่ทำปฏิกิริยากันได้",
                  "แบบเติม เพราะมอนอเมอร์มีหมู่ฟังก์ชันสองหมู่ที่ทำปฏิกิริยากันได้")
        return _labelled(stem=f"มอนอเมอร์ {structure} เกิดพอลิเมอร์ ({polymer}) ด้วยปฏิกิริยาแบบใด", correct=right,
                         wrongs=tuple(w for w in wrongs if w != right)[:3], topic=TOPIC_POLYMER,
                         hint="มองหาพันธะคู่ C=C (แบบเติม) หรือหมู่ -COOH -OH -NH₂ ที่ทำปฏิกิริยาแล้วเสีย H₂O (แบบควบแน่น)")


@question_type(
    "chem.polymerization_application",
    display_name={"th": "หน่วยซ้ำและจำนวนมอนอเมอร์ในพอลิเมอร์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_POLYMER,
)
class PolymerizationApplication(QuestionType):
    """The repeating unit of an addition polymer, and n = polymer mass ÷ monomer mass."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        polymer, unit, mass = rng.choice(REPEATS)
        if rng.random() < 0.4:
            others = [r[1] for r in REPEATS if r[1] != unit]
            return _labelled(stem=f"หน่วยซ้ำของ{polymer}คือข้อใด", correct=unit, wrongs=tuple(others),
                             topic=TOPIC_POLYMER,
                             hint="ในพอลิเมอร์แบบเติม พันธะคู่ของมอนอเมอร์เปิดเป็นพันธะเดี่ยว หน่วยซ้ำมีอะตอมเท่ากับมอนอเมอร์")
        n = rng.randrange(200, 5001, 100)
        return numeric(stem=f"{polymer}สายหนึ่งมีมวลโมเลกุล {show(n * mass)} ถ้ามวลโมเลกุลของมอนอเมอร์เท่ากับ {show(mass)} "
                            "พอลิเมอร์สายนี้เกิดจากมอนอเมอร์กี่โมเลกุล",
                       answer=n, wrongs=[n * 2, n // 2, n + 100], unit="โมเลกุล", topic=TOPIC_POLYMER,
                       hint="พอลิเมอร์แบบเติมไม่เสียอะตอมใดออกไป จำนวนมอนอเมอร์ = มวลพอลิเมอร์ ÷ มวลมอนอเมอร์")
