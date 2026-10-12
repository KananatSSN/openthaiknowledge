"""ความเข้มข้นของสารละลาย

เคมี · ม.2 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.2/5

Sets moved here from: science_wave_d10.
"""

from __future__ import annotations

from decimal import Decimal
from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c23 import Part
from otk.sets._support.science_wave_c24 import parts_item
from otk.sets._support.science_wave_d1 import SUBJECT
from otk.sets._support.science_wave_d9 import SECONDARY_TWO

PROVENANCE = Provenance("original")


CONCENTRATION_TOPIC = "ความเข้มข้นของสารละลาย"


VV, MM, MV = "ปริมาตรต่อปริมาตร", "มวลต่อมวล", "มวลต่อปริมาตร"


class Mixture(NamedTuple):
    unit: str
    solute: str
    solute_unit: str
    whole_unit: str


MIXTURES = {
    VV: Mixture(VV, "เอทานอล", "ลูกบาศก์เซนติเมตร", "ลูกบาศก์เซนติเมตร"),
    MM: Mixture(MM, "เกลือแกง", "กรัม", "กรัม"),
    MV: Mixture(MV, "น้ำตาลทราย", "กรัม", "ลูกบาศก์เซนติเมตร"),
}


def draw_solution(rng: Random, unit: str) -> tuple[int, int, int]:
    """Solute amount, solution amount and the whole-number percentage."""
    percent = rng.choice((5, 10, 15, 20, 25, 40))
    whole = rng.choice((40, 80, 100, 200, 400))
    return percent * whole // 100, whole, percent


def describe(mix: Mixture, solute: int, whole: int) -> str:
    if mix.unit == MM:
        return f"ละลาย{mix.solute} {solute} {mix.solute_unit} ในน้ำ {whole - solute} กรัม"
    return f"มี{mix.solute} {solute} {mix.solute_unit} ในสารละลายทั้งหมด {whole} {mix.whole_unit}"


CONCENTRATION_SCENARIOS = (
    ("ต้องการเตรียมน้ำเกลือเข้มข้นร้อยละ 0.9 โดยมวลต่อปริมาตร จำนวน 500 ลูกบาศก์เซนติเมตร ต้องใช้เกลือกี่กรัม",
     "4.5 กรัม", ("0.9 กรัม", "45 กรัม", "9 กรัม", "450 กรัม", "0.45 กรัม")),
    ("น้ำส้มสายชูเข้มข้นร้อยละ 5 โดยปริมาตร ถ้านำมา 100 ลูกบาศก์เซนติเมตรเติมน้ำจนได้ 250 ลูกบาศก์เซนติเมตร ความเข้มข้นใหม่เป็นเท่าใด",
     "ร้อยละ 2 โดยปริมาตร", ("ร้อยละ 5 โดยปริมาตร", "ร้อยละ 12.5 โดยปริมาตร", "ร้อยละ 3 โดยปริมาตร",
                              "ร้อยละ 40 โดยปริมาตร", "ร้อยละ 7 โดยปริมาตร")),
    ("แอลกอฮอล์ล้างแผลขวดหนึ่งระบุว่า \"เอทิลแอลกอฮอล์ 70% v/v\" ข้อความนี้หมายความว่าอย่างไร",
     "ในสารละลาย 100 ลูกบาศก์เซนติเมตร มีเอทิลแอลกอฮอล์ 70 ลูกบาศก์เซนติเมตร",
     ("ในน้ำ 100 ลูกบาศก์เซนติเมตร มีเอทิลแอลกอฮอล์ 70 ลูกบาศก์เซนติเมตร",
      "ในสารละลาย 100 กรัม มีเอทิลแอลกอฮอล์ 70 กรัม",
      "ขวดนี้มีเอทิลแอลกอฮอล์ 70 ลูกบาศก์เซนติเมตรเสมอไม่ว่าขวดจะใหญ่เท่าใด",
      "ในสารละลาย 70 ลูกบาศก์เซนติเมตร มีเอทิลแอลกอฮอล์ 100 ลูกบาศก์เซนติเมตร",
      "ในสารละลาย 100 ลูกบาศก์เซนติเมตร มีน้ำ 70 ลูกบาศก์เซนติเมตร")),
)


def _num(value: Decimal) -> str:
    return f"{value.normalize():f}"


PREPARED = ((VV, "เอทานอล", "ลูกบาศก์เซนติเมตร", "ลูกบาศก์เซนติเมตร"),
            (MM, "เกลือแกง", "กรัม", "กรัม"),
            (MV, "น้ำตาลทราย", "กรัม", "ลูกบาศก์เซนติเมตร"))


def prepare_solution(rng: Random) -> GeneratedQuestion:
    """How much solute a stated amount of solution at a stated percentage needs."""
    unit, solute, solute_unit, whole_unit = rng.choice(PREPARED)
    percent = Decimal(rng.choice(("0.9", "2", "4", "5", "10", "15", "20", "25")))
    whole = rng.choice((100, 200, 250, 400, 500, 1000))
    answer = percent * whole / 100
    pool = (percent * whole / 10, percent, percent * whole / 1000, answer * 2, Decimal(whole) - answer)
    wrongs = tuple(dict.fromkeys(f"{_num(w)} {solute_unit}" for w in pool if w != answer and w > 0))
    return _labelled(
        stem=(f"ต้องการเตรียมสารละลาย{solute}เข้มข้นร้อยละ {_num(percent)} โดย{unit} จำนวน {whole} {whole_unit} "
              f"ต้องใช้{solute}กี่{solute_unit}"),
        correct=f"{_num(answer)} {solute_unit}",
        wrongs=wrongs,
        hint="ปริมาณตัวละลาย = ร้อยละ × ปริมาณสารละลายทั้งหมด ÷ 100",
        topic=CONCENTRATION_TOPIC,
    )


def dilute_solution(rng: Random) -> GeneratedQuestion:
    """Adding water keeps the solute; the new percentage of a diluted solution."""
    start, first = Decimal(rng.choice((5, 10, 20, 40))), rng.choice((50, 100, 200))
    factor = rng.choice((2, 4, 5, 10))
    final = first * factor
    answer = start / factor
    pool = (start, start * factor, start - answer, Decimal(first) / final, answer * 2)
    wrongs = tuple(dict.fromkeys(f"ร้อยละ {_num(w)} โดยปริมาตร" for w in pool if w != answer and w > 0))
    return _labelled(
        stem=(f"สารละลายเอทานอลเข้มข้นร้อยละ {_num(start)} โดยปริมาตร ถ้านำมา {first} ลูกบาศก์เซนติเมตร "
              f"เติมน้ำจนได้ {final} ลูกบาศก์เซนติเมตร ความเข้มข้นใหม่เป็นเท่าใด"),
        correct=f"ร้อยละ {_num(answer)} โดยปริมาตร",
        wrongs=wrongs,
        hint="ปริมาณเอทานอลเท่าเดิมหลังเติมน้ำ จึงหารด้วยปริมาตรใหม่ทั้งหมด",
        topic=CONCENTRATION_TOPIC,
    )


@question_type(
    "chem.concentration_foundation",
    display_name={"th": "คำนวณความเข้มข้นเป็นร้อยละในหน่วยเดียว"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=CONCENTRATION_TOPIC,
)
class ConcentrationFoundation(QuestionType):
    """One solution; its concentration in the unit named."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        unit = rng.choice((VV, MM, MV))
        mix = MIXTURES[unit]
        solute, whole, percent = draw_solution(rng, unit)
        solvent = whole - solute
        slips = [round(100 * solute / solvent, 1) if solvent else None, round(100 * whole / solute, 1),
                 round(solute / whole, 2), percent * 2, percent / 2]
        wrongs = [w for w in dict.fromkeys(slips) if w not in (None, percent)][:3]
        return _labelled(
            stem=f"สารละลายหนึ่ง{describe(mix, solute, whole)} สารละลายนี้มีความเข้มข้นร้อยละโดย{unit}เท่าใด",
            correct=f"{percent}",
            wrongs=tuple(f"{w:g}" for w in wrongs),
            hint="ร้อยละ = ปริมาณตัวละลาย ÷ ปริมาณสารละลายทั้งหมด × 100 (ไม่ใช่ปริมาณตัวทำละลาย)",
            topic=CONCENTRATION_TOPIC,
        )


@question_type(
    "chem.concentration_fluency",
    display_name={"th": "ระบุปริมาณตัวละลายเป็นร้อยละโดยปริมาตร มวล และมวลต่อปริมาตร"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=CONCENTRATION_TOPIC,
)
class ConcentrationFluency(QuestionType):
    """Three solutions, one per unit; state all three concentrations."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        labels = ("ก", "ข", "ค")
        units = [VV, MM, MV]
        rng.shuffle(units)
        rows, parts = [], []
        for label, unit in zip(labels, units):
            mix = MIXTURES[unit]
            solute, whole, percent = draw_solution(rng, unit)
            rows.append(f"สารละลาย {label}: {describe(mix, solute, whole)}")
            wrong = round(100 * solute / (whole - solute), 1)
            parts.append(Part(f"สารละลาย {label}", f"ร้อยละ {percent} โดย{unit}", f"ร้อยละ {wrong:g} โดย{unit}"))
        return parts_item(
            rng, tuple(parts),
            stem=(f"ข้อมูลสารละลาย 3 ชนิด — {' / '.join(rows)} "
                  "ข้อใดระบุความเข้มข้นของสารละลายทั้งสามได้ถูกต้องทั้งหมด"),
            hint="ทุกหน่วยหารด้วยปริมาณสารละลายทั้งหมด ถ้าให้มวลน้ำมา ต้องบวกมวลตัวละลายก่อน",
            topic=CONCENTRATION_TOPIC,
        )


@question_type(
    "chem.concentration_application",
    display_name={"th": "เตรียมและเจือจางสารละลายตามความเข้มข้นที่ต้องการ"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=CONCENTRATION_TOPIC,
)
class ConcentrationApplication(QuestionType):
    """Making saline, diluting vinegar, and reading a label, with preparations and dilutions drawn fresh."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.3:
            return prepare_solution(rng)
        if roll < 0.6:
            return dilute_solution(rng)
        return _retopic(scenario_question(
            rng, CONCENTRATION_SCENARIOS,
            hint="ใช้นิยามร้อยละกลับด้าน หรือจำไว้ว่าการเติมน้ำไม่เปลี่ยนปริมาณตัวละลาย",
        ), CONCENTRATION_TOPIC)
