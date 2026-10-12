"""จุดเดือดและจุดเยือกแข็งของสารละลาย

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 3 ม.4/11

Sets moved here from: science_wave_f43.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f24 import _find, exact
from otk.sets._support.science_wave_f43 import CHEMISTRY, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_COLLIGATIVE = "จุดเดือดและจุดเยือกแข็งของสารละลาย"


# (solvent, boiling point, Kb, freezing point, Kf)
SOLVENTS = (
    ("น้ำ", Fraction(100), Fraction(51, 100), Fraction(0), Fraction(186, 100)),
    ("เบนซีน", Fraction(801, 10), Fraction(253, 100), Fraction(55, 10), Fraction(512, 100)),
    ("กรดแอซีติก", Fraction(1181, 10), Fraction(307, 100), Fraction(166, 10), Fraction(390, 100)),
    ("แนฟทาลีน", Fraction(218), Fraction(580, 100), Fraction(80), Fraction(680, 100)),
)


NONELECTROLYTES = (("กลูโคส", 180), ("ซูโครส", 342), ("ยูเรีย", 60), ("กลีเซอรอล", 92), ("แนฟทาลีน", 128))


def colligative_case(rng: Random, water_only: bool = False):
    def draw():
        solvent = SOLVENTS[0] if water_only else rng.choice(SOLVENTS)
        solute, m = rng.choice(NONELECTROLYTES if solvent[0] != "แนฟทาลีน" else NONELECTROLYTES[:4])
        molality = Fraction(rng.randrange(1, 13), rng.choice((1, 2, 4)))
        solvent_g = rng.choice((100, 200, 250, 500, 1000))
        grams = molality * m * solvent_g / 1000
        boiling = molality * solvent[2]
        freezing = molality * solvent[4]
        ok = all(exact(x) for x in (grams, boiling, freezing))
        return (solvent, solute, m, molality, solvent_g, grams, boiling, freezing) if ok else None
    return _find(rng, draw)


@question_type(
    "chem.colligative_foundation",
    display_name={"th": "เปรียบเทียบจุดเดือดและจุดเยือกแข็งของสารละลายกับตัวทำละลาย"},
    level=UPPER_FOUR, subject=CHEMISTRY, topic=TOPIC_COLLIGATIVE,
)
class ColligativeFoundation(QuestionType):
    """A nonvolatile solute raises the boiling point and lowers the freezing point."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            facts = (
                ("สารละลายน้ำตาลในน้ำมีจุดเดือดเทียบกับน้ำบริสุทธิ์อย่างไร", "สูงกว่า", ("ต่ำกว่า", "เท่ากัน", "บอกไม่ได้")),
                ("สารละลายน้ำตาลในน้ำมีจุดเยือกแข็งเทียบกับน้ำบริสุทธิ์อย่างไร", "ต่ำกว่า", ("สูงกว่า", "เท่ากัน", "บอกไม่ได้")),
                ("เมื่อโมแลลิตีของสารละลายเพิ่มขึ้น จุดเดือดของสารละลายเป็นอย่างไร", "สูงขึ้น",
                 ("ต่ำลง", "ไม่เปลี่ยน", "สูงขึ้นแล้วคงที่ทันที")),
                ("การโรยเกลือบนถนนที่มีน้ำแข็งในฤดูหนาวใช้หลักการใด", "สารละลายมีจุดเยือกแข็งต่ำกว่าน้ำบริสุทธิ์",
                 ("เกลือทำปฏิกิริยาคายความร้อนละลายน้ำแข็ง", "เกลือทำให้น้ำมีจุดเดือดต่ำลง", "เกลือดูดซับน้ำแข็งไว้")),
                ("การเติมสารกันเยือกแข็งในหม้อน้ำรถยนต์ช่วยอย่างไร", "ทำให้น้ำในหม้อน้ำเยือกแข็งยากขึ้นและเดือดยากขึ้น",
                 ("ทำให้น้ำเดือดง่ายขึ้น", "ทำให้เครื่องยนต์เย็นลงทันที", "ทำให้น้ำไม่ระเหยเลย")),
            )
            stem, right, wrongs = rng.choice(facts)
            return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_COLLIGATIVE,
                             hint="ตัวละลายที่ไม่ระเหยทำให้จุดเดือดสูงขึ้นและจุดเยือกแข็งต่ำลงตามโมแลลิตี")
        solvent, solute, m, molality, solvent_g, grams, boiling, freezing = colligative_case(rng)
        higher = rng.random() < 0.5
        values = sorted(rng.sample([Fraction(x, 2) for x in range(1, 9)], 3))
        pick = values[-1] if higher else values[0]
        labels = {v: f"{solute} {show(v)} mol/kg" for v in values}
        return _labelled(stem=f"สารละลาย{solute}ใน{solvent[0]}ที่โมแลลิตีต่างกัน ข้อใดมีจุด{'เดือดสูงที่สุด' if higher else 'เยือกแข็งสูงที่สุด'}",
                         correct=labels[pick], wrongs=tuple(labels[v] for v in values if v != pick) + (f"{solvent[0]}บริสุทธิ์"
                                                                                              if higher else f"{solute} {show(values[-1] + 1)} mol/kg",),
                         topic=TOPIC_COLLIGATIVE,
                         hint="โมแลลิตีมาก จุดเดือดสูงขึ้นมากและจุดเยือกแข็งต่ำลงมาก ตัวทำละลายบริสุทธิ์จุดเยือกแข็งสูงสุด")


@question_type(
    "chem.colligative_fluency",
    display_name={"th": "คำนวณจุดเดือดและจุดเยือกแข็งของสารละลาย"},
    level=UPPER_FOUR, subject=CHEMISTRY, topic=TOPIC_COLLIGATIVE,
)
class ColligativeFluency(QuestionType):
    """ΔTb = Kb·m and ΔTf = Kf·m."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        solvent, solute, m, molality, solvent_g, grams, boiling, freezing = colligative_case(rng)
        name, tb, kb, tf, kf = solvent
        stem = f"ละลาย{solute} (มวลต่อโมล {m}) {show(grams)} กรัม ใน{name} {solvent_g} กรัม"
        if rng.random() < 0.5:
            return numeric(stem=f"{stem} สารละลายมีจุดเดือดกี่ °C (จุดเดือดของ{name} {show(tb)} °C, Kb = {show(kb)} °C·kg/mol)",
                           answer=tb + boiling, wrongs=[tb - boiling, tb + kb, tb + boiling * 2], unit="°C", topic=TOPIC_COLLIGATIVE,
                           allow_negative=True, hint="m = โมลตัวละลาย ÷ มวลตัวทำละลาย (kg) แล้ว จุดเดือด = จุดเดือดตัวทำละลาย + Kb·m")
        return numeric(stem=f"{stem} สารละลายมีจุดเยือกแข็งกี่ °C (จุดเยือกแข็งของ{name} {show(tf)} °C, Kf = {show(kf)} °C·kg/mol)",
                       answer=tf - freezing, wrongs=[tf + freezing, tf - kf if tf - kf != tf - freezing else tf - kf * 2, tf - freezing * 2],
                       unit="°C", topic=TOPIC_COLLIGATIVE, allow_negative=True,
                       hint="m = โมลตัวละลาย ÷ มวลตัวทำละลาย (kg) แล้ว จุดเยือกแข็ง = จุดเยือกแข็งตัวทำละลาย − Kf·m")


@question_type(
    "chem.colligative_application",
    display_name={"th": "หามวลโมเลกุลของตัวละลายจากจุดเดือดหรือจุดเยือกแข็ง"},
    level=UPPER_FOUR, subject=CHEMISTRY, topic=TOPIC_COLLIGATIVE,
)
class ColligativeApplication(QuestionType):
    """m = ΔT ÷ K, then molar mass = grams ÷ (m × kg of solvent)."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        solvent, solute, m, molality, solvent_g, grams, boiling, freezing = colligative_case(rng)
        name, tb, kb, tf, kf = solvent
        if rng.random() < 0.5:
            return numeric(stem=f"ละลายสาร X {show(grams)} กรัม ใน{name} {solvent_g} กรัม สารละลายเดือดที่ {show(tb + boiling)} °C "
                                f"(จุดเดือดของ{name} {show(tb)} °C, Kb = {show(kb)} °C·kg/mol) สาร X มีมวลโมเลกุลเท่าใด",
                           answer=m, wrongs=[m * 2, m / 2 if exact(m / 2) else m + 10, grams], unit="g/mol", topic=TOPIC_COLLIGATIVE,
                           hint="m = ΔTb ÷ Kb → โมล = m × kg ตัวทำละลาย → มวลโมเลกุล = มวล ÷ โมล")
        return numeric(stem=f"ละลายสาร X {show(grams)} กรัม ใน{name} {solvent_g} กรัม สารละลายเยือกแข็งที่ {show(tf - freezing)} °C "
                            f"(จุดเยือกแข็งของ{name} {show(tf)} °C, Kf = {show(kf)} °C·kg/mol) สาร X มีมวลโมเลกุลเท่าใด",
                       answer=m, wrongs=[m * 2, m / 2 if exact(m / 2) else m + 10, grams], unit="g/mol", topic=TOPIC_COLLIGATIVE,
                       hint="m = ΔTf ÷ Kf → โมล = m × kg ตัวทำละลาย → มวลโมเลกุล = มวล ÷ โมล")
