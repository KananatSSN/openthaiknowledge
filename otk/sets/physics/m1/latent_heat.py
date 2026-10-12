"""การคำนวณปริมาณความร้อนแฝงในการเปลี่ยนสถานะ

ฟิสิกส์ · ม.1 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.1/1

Sets moved here from: science_wave_g3.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.ms1_diagrams import HEATING_CURVES, diagram_question, heating_curve_alt
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d28 import FIRST_SECONDARY

PROVENANCE = Provenance("original")


LATENT_HEAT_TOPIC = "การคำนวณปริมาณความร้อนแฝงในการเปลี่ยนสถานะ"


def _thai_number(value: float) -> str:
    """A whole joule count with thousands separators, however large it gets.

    ``:g`` — which the sibling ``Q = mcΔT`` set uses — turns 2,260,000 into
    ``2.26e+06``. Latent heats are an order of magnitude larger than the heat
    capacities that set works with, so they need the long form.
    """
    return f"{value:,.0f}"


# Each pair of (stem, correct, wrongs). The first distractor of the definition
# case is the specific confusion this set exists to catch: ``c`` stated as if it
# were ``L``. They differ in exactly one clause — per degree versus per change of
# state — so a learner who has only memorised "ต่อกิโลกรัม" cannot tell them
# apart, which is the point.
LATENT_HEAT_CONCEPTS = (
    ("ความร้อนแฝงจำเพาะ (L) ของสารหมายถึงอะไร",
     "ความร้อนที่สาร 1 กิโลกรัมใช้เปลี่ยนสถานะจนหมด โดยอุณหภูมิไม่เปลี่ยน",
     ("ปริมาณความร้อนที่ทำให้สารมวล 1 กิโลกรัมมีอุณหภูมิสูงขึ้น 1 องศาเซลเซียส",
      "อุณหภูมิสูงสุดที่สารทนได้ก่อนที่จะเริ่มเปลี่ยนสถานะ",
      "ปริมาณความร้อนทั้งหมดที่สะสมอยู่ภายในสารก้อนนั้น")),
    ("ความร้อนแฝงจำเพาะ (L) ต่างจากความร้อนจำเพาะ (c) อย่างไร",
     "L ใช้กับช่วงที่เปลี่ยนสถานะโดยอุณหภูมิคงที่ ส่วน c ใช้กับช่วงที่อุณหภูมิเปลี่ยน",
     ("L ใช้กับของแข็ง ส่วน c ใช้กับของเหลวและแก๊ส",
      "L ใช้กับสารที่มีมวลมาก ส่วน c ใช้กับสารที่มีมวลน้อย",
      "ทั้งสองค่าหมายถึงสิ่งเดียวกัน ต่างกันเพียงหน่วยที่ใช้")),
    ("ขณะที่น้ำแข็งกำลังหลอมเหลวที่ 0 องศาเซลเซียส ความร้อนที่ให้เข้าไปถูกใช้ไปกับสิ่งใด",
     "ใช้แยกอนุภาคของน้ำแข็งออกจากกันจนเป็นน้ำ อุณหภูมิจึงไม่สูงขึ้น",
     ("ใช้เพิ่มอุณหภูมิของน้ำแข็งให้สูงกว่า 0 องศาเซลเซียสทันที",
      "ใช้เพิ่มมวลของน้ำแข็งให้มากขึ้นขณะหลอมเหลว",
      "ไม่ได้ถูกใช้ไปกับสิ่งใดเลย ความร้อนสูญหายไปจากระบบทั้งหมด")),
)


class Substance(NamedTuple):
    """A substance and both of its latent heats, in joules per kilogram.

    Both are carried because the pair is the distractor: a learner who reaches
    for the wrong one of a substance's two latent heats gets a number that looks
    entirely reasonable, and no other kind of wrong answer catches that.
    """
    name: str
    fusion: int             # ความร้อนแฝงจำเพาะของการหลอมเหลว (J/kg)
    vaporisation: int       # ความร้อนแฝงจำเพาะของการกลายเป็นไอ (J/kg)

    def latent(self, melting: bool) -> int:
        return self.fusion if melting else self.vaporisation

    def other(self, melting: bool) -> int:
        return self.vaporisation if melting else self.fusion


SUBSTANCES = (
    Substance("น้ำ", 333_000, 2_260_000),
    Substance("เอทานอล", 108_000, 855_000),
    Substance("ตะกั่ว", 25_000, 871_000),
)


#: 1 kg is excluded on purpose: at ``m = 1`` the "forgot to multiply by the mass"
#: and "divided instead of multiplied" mistakes both land on the right answer,
#: and the item would offer fewer than four distinct choices.
MASSES = (0.5, 2, 3, 4, 5)


# Which equation a stretch of the heating curve needs, and why. The wrong
# reasons are kept parallel to the right one so the choice turns on the physics
# rather than on which option is longest.
_FLAT = ("ใช้ Q = mL เพราะช่วงนี้อุณหภูมิคงที่ ความร้อนใช้เปลี่ยนสถานะ ไม่ได้ใช้เพิ่มอุณหภูมิ")


_SLOPED = ("ใช้ Q = mcΔT เพราะช่วงนี้อุณหภูมิของสารเปลี่ยนไป และสารยังไม่เปลี่ยนสถานะ")


_FLAT_WRONGS = (
    "ใช้ Q = mcΔT โดยแทน ΔT ด้วยอุณหภูมิของช่วงนี้ เพราะสารยังได้รับความร้อนอยู่",
    "ใช้ Q = mcΔT เพราะทุกช่วงบนกราฟใช้สมการเดียวกันได้",
    "ไม่ต้องใช้สมการใดเลย เพราะช่วงที่อุณหภูมิคงที่แสดงว่าสารไม่ได้รับความร้อน",
)


_SLOPED_WRONGS = (
    "ใช้ Q = mL เพราะอุณหภูมิของสารเพิ่มขึ้นขณะได้รับความร้อน",
    "ใช้ Q = mL เพราะช่วงนี้อุณหภูมิของสารเปลี่ยนแปลงไป",
    "ใช้ทั้ง Q = mcΔT และ Q = mL บวกกัน เพราะช่วงนี้เกิดทั้งสองอย่างพร้อมกัน",
)


STAGES = (
    ("น้ำแข็งที่ −10 °C ถูกอุ่นจนมีอุณหภูมิ 0 °C", False),
    ("น้ำแข็งที่ 0 °C หลอมเหลวจนหมดกลายเป็นน้ำที่ 0 °C", True),
    ("น้ำที่ 0 °C ถูกอุ่นจนมีอุณหภูมิ 30 °C", False),
    ("น้ำที่ 100 °C เดือดกลายเป็นไอน้ำที่ 100 °C จนหมด", True),
    ("ไอน้ำที่ 100 °C ควบแน่นเป็นน้ำที่ 100 °C จนหมด", True),
    ("น้ำที่ 60 °C ถูกทำให้เย็นลงจนเหลือ 20 °C", False),
    ("น้ำที่ 0 °C แข็งตัวเป็นน้ำแข็งที่ 0 °C จนหมด", True),
    ("{s}ที่อุณหภูมิหลอมเหลวพอดี หลอมเหลวจนหมด", True),
    ("{s}ในสถานะของเหลวถูกอุ่นให้ร้อนขึ้นอีก 15 °C", False),
    ("{s}ในสถานะของแข็งถูกอุ่นจากอุณหภูมิห้องจนถึงจุดหลอมเหลว", False),
    ("{s}ในสถานะของเหลวที่จุดเดือดพอดี กลายเป็นไอจนหมด", True),
    ("{s}ในสถานะของเหลวเย็นตัวลงจนถึงจุดเยือกแข็ง", False),
    ("{s}ที่จุดเยือกแข็งพอดี แข็งตัวจนหมด", True),
    ("ไอน้ำที่ 120 °C เย็นตัวลงจนเหลือ 100 °C", False),
    ("น้ำแข็งที่ −25 °C ถูกอุ่นจนมีอุณหภูมิ −5 °C", False),
)


LATENT_HEAT_SCENARIOS = (
    ("ไอน้ำที่ 100 องศาเซลเซียส ลวกผิวหนังได้รุนแรงกว่าน้ำเดือดที่ 100 องศาเซลเซียสเท่ากัน "
     "เพราะเหตุใด",
     "ไอน้ำต้องคายความร้อนแฝงของการกลายเป็นไอออกมาก่อนจึงจะควบแน่นเป็นน้ำ "
     "ผิวหนังจึงได้รับความร้อนเพิ่มอีกจำนวนมากนอกเหนือจากความร้อนที่ลดอุณหภูมิลง",
     ("ไอน้ำมีอุณหภูมิสูงกว่าน้ำเดือดเสมอ แม้จะวัดได้เท่ากันก็ตาม",
      "ไอน้ำมีมวลมากกว่าน้ำเดือดที่ปริมาตรเท่ากัน จึงพาความร้อนได้มากกว่า",
      "ไอน้ำดูดความร้อนจากผิวหนังเข้าไป ผิวหนังจึงเสียหาย")),
    ("น้ำแข็งที่ 0 องศาเซลเซียส ทำให้เครื่องดื่มเย็นได้ดีกว่าน้ำเย็นที่ 0 องศาเซลเซียส "
     "ที่มีมวลเท่ากัน เพราะเหตุใด",
     "น้ำแข็งต้องดูดความร้อนแฝงของการหลอมเหลวจากเครื่องดื่มไปใช้ในการละลายก่อน "
     "จึงดึงความร้อนออกจากเครื่องดื่มได้มากกว่า",
     ("น้ำแข็งมีอุณหภูมิต่ำกว่าน้ำเย็นเสมอ แม้จะวัดได้เท่ากันก็ตาม",
      "น้ำแข็งมีความร้อนจำเพาะสูงกว่าน้ำในสถานะของเหลวหลายเท่า",
      "น้ำแข็งคายความร้อนแฝงออกมาขณะละลาย เครื่องดื่มจึงเย็นลง")),
    ("การคำนวณความร้อนที่ใช้ทำให้น้ำแข็งที่ −10 องศาเซลเซียส กลายเป็นน้ำที่ 20 องศาเซลเซียส "
     "ต้องคิดกี่ขั้นตอน และใช้สมการใดบ้าง",
     "สามขั้นตอน คือ ใช้ Q = mcΔT อุ่นน้ำแข็งถึง 0 องศาเซลเซียส "
     "แล้วใช้ Q = mL หลอมน้ำแข็งที่ 0 องศาเซลเซียส แล้วใช้ Q = mcΔT อุ่นน้ำถึง 20 องศาเซลเซียส",
     ("ขั้นตอนเดียว คือ ใช้ Q = mcΔT โดยแทน ΔT ด้วย 30 องศาเซลเซียสตลอดทั้งช่วง",
      "ขั้นตอนเดียว คือ ใช้ Q = mL เพราะมีการเปลี่ยนสถานะเกิดขึ้นในกระบวนการนี้",
      "สองขั้นตอน คือ ใช้ Q = mL สองครั้ง ครั้งหนึ่งสำหรับน้ำแข็งและอีกครั้งสำหรับน้ำ")),
)


@question_type(
    "phys.latent_heat_foundation",
    display_name={"th": "บอกความหมายของความร้อนแฝงจำเพาะ"},
    level=FIRST_SECONDARY, subject=SUBJECT, topic=LATENT_HEAT_TOPIC,
)
class LatentHeatFoundation(QuestionType):
    """What ``L`` means, how it differs from ``c``, and where the energy goes."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.65:
            stage, flat = rng.choice(STAGES)
            substance = rng.choice(("น้ำ", "เอทานอล", "ตะกั่ว", "ปรอท")) if "{s}" in stage else ""
            return _labelled(
                stem=f"\"{stage.format(s=substance)}\" ต้องคำนวณความร้อนในขั้นนี้ด้วยสมการใด",
                correct=_FLAT if flat else _SLOPED,
                wrongs=_FLAT_WRONGS if flat else _SLOPED_WRONGS,
                hint="ขั้นที่อุณหภูมิเปลี่ยนใช้ Q = mcΔT ขั้นที่เปลี่ยนสถานะโดยอุณหภูมิคงที่ใช้ Q = mL",
                topic=LATENT_HEAT_TOPIC,
            )
        stem, correct, wrongs = rng.choice(LATENT_HEAT_CONCEPTS)
        return _labelled(
            stem=stem, correct=correct, wrongs=wrongs,
            hint=("ความร้อนแฝงเป็นค่าต่อมวล 1 กิโลกรัม และใช้กับช่วงที่สารเปลี่ยนสถานะ "
                  "ซึ่งอุณหภูมิไม่เปลี่ยนแปลง"),
            topic=LATENT_HEAT_TOPIC,
        )


@question_type(
    "phys.latent_heat_fluency",
    display_name={"th": "คำนวณปริมาณความร้อนในการเปลี่ยนสถานะโดยใช้สมการ Q = mL"},
    level=FIRST_SECONDARY, subject=SUBJECT, topic=LATENT_HEAT_TOPIC,
)
class LatentHeatFluency(QuestionType):
    """``Q = mL`` — the second equation ``ว 2.3 ม.1/1`` names."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        substance = rng.choice(SUBSTANCES)
        melting = rng.random() < 0.5
        mass = rng.choice(MASSES)
        latent = substance.latent(melting)
        change = "หลอมเหลว" if melting else "กลายเป็นไอ"
        kind = "การหลอมเหลว" if melting else "การกลายเป็นไอ"
        answer = mass * latent
        return _labelled(
            stem=(f"{substance.name}มวล {mass:g} กิโลกรัม ที่อุณหภูมิของการเปลี่ยนสถานะพอดี "
                  f"ต้องได้รับความร้อนเท่าใดจึง{change}จนหมด "
                  f"กำหนดให้ความร้อนแฝงจำเพาะของ{kind}เท่ากับ "
                  f"{_thai_number(latent)} จูลต่อกิโลกรัม (ใช้ Q = mL)"),
            correct=f"{_thai_number(answer)} จูล",
            wrongs=(f"{_thai_number(mass * substance.other(melting))} จูล",
                    f"{_thai_number(latent)} จูล",
                    f"{_thai_number(latent / mass)} จูล"),
            hint="Q = mL คูณมวลกับความร้อนแฝงจำเพาะของการเปลี่ยนสถานะชนิดที่โจทย์ถาม",
            topic=LATENT_HEAT_TOPIC,
        )


@question_type(
    "phys.latent_heat_application",
    display_name={"th": "เลือกสมการคำนวณปริมาณความร้อนให้ตรงกับช่วงบนกราฟ"},
    level=FIRST_SECONDARY, subject=SUBJECT, topic=LATENT_HEAT_TOPIC,
)
class LatentHeatApplication(QuestionType):
    """Given minutes, not a description — the learner has to look at the graph.

    A third of the draws name the plateau and want ``Q = mL``; the rest name one
    of the two ramps and want ``Q = mcΔT``. Asking only about the flat part would
    let a learner answer ``mL`` every time without reading anything.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        spec = rng.choice(HEATING_CURVES)
        segments = ((0, spec.warm_to, False),
                    (spec.plateau_start, spec.plateau_end, True),
                    (spec.plateau_end, spec.total, False))
        first, last, flat = rng.choice(segments)
        return diagram_question(
            spec.asset_id, heating_curve_alt(spec),
            stem=(f"จากกราฟ ปริมาณความร้อนที่สารได้รับในช่วงนาทีที่ {first} ถึงนาทีที่ {last} "
                  f"ต้องคำนวณด้วยสมการใด และเพราะเหตุใด"),
            correct=_FLAT if flat else _SLOPED,
            wrongs=_FLAT_WRONGS if flat else _SLOPED_WRONGS,
            hint=("ดูก่อนว่าช่วงนาทีที่โจทย์ถามอยู่บนส่วนที่เส้นกราฟเอียงขึ้นหรือส่วนที่ราบ "
                  "ส่วนที่เอียงคืออุณหภูมิเปลี่ยน ส่วนที่ราบคือกำลังเปลี่ยนสถานะ"),
            topic=LATENT_HEAT_TOPIC,
        )


@question_type(
    "phys.latent_heat_scenario",
    display_name={"th": "ใช้ความร้อนแฝงอธิบายสถานการณ์ในชีวิตประจำวัน"},
    level=FIRST_SECONDARY, subject=SUBJECT, topic=LATENT_HEAT_TOPIC,
)
class LatentHeatScenario(QuestionType):
    """Steam scalds, ice chills, and the three-step calculation.

    A fourth set on one indicator, and it earns the place: the first three ask
    what ``L`` is, how to multiply by it, and when to reach for it. None of them
    asks why it matters, and every worked example a ม.1 tutor uses for latent
    heat is one of these three.
    """
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            mass = rng.choice((0.5, 2, 3, 4, 5))
            start = rng.choice((20, 30, 40, 50, 60, 70, 80))
            heat = mass * 4200 * (100 - start)
            boil = mass * 2_260_000
            return _labelled(
                stem=(f"ต้องการเปลี่ยนน้ำมวล {mass:g} กิโลกรัมที่ {start} °C ให้เป็นไอน้ำที่ 100 °C จนหมด "
                      "(c ของน้ำ = 4,200 J/kg·°C, L กลายเป็นไอของน้ำ = 2,260,000 J/kg) ต้องใช้ความร้อนรวมเท่าใด"),
                correct=f"{_thai_number(heat + boil)} จูล",
                wrongs=(f"{_thai_number(heat)} จูล", f"{_thai_number(boil)} จูล",
                        f"{_thai_number(mass * 4200 * 100 + boil)} จูล"),
                hint="แยกเป็นสองขั้น: อุ่นน้ำถึง 100 °C ด้วย Q = mcΔT แล้วทำให้เดือดจนหมดด้วย Q = mL จากนั้นนำมาบวกกัน",
                topic=LATENT_HEAT_TOPIC,
            )
        if rng.random() < 0.6:
            mass = rng.choice((0.5, 2, 3, 4, 5))
            warm = rng.choice((10, 20, 30, 40, 50))
            melt = mass * 333_000
            heat = mass * 4200 * warm
            return _labelled(
                stem=(f"ต้องการเปลี่ยนน้ำแข็งมวล {mass:g} กิโลกรัมที่ 0 °C ให้เป็นน้ำที่ {warm} °C "
                      "(L หลอมเหลวของน้ำ = 333,000 J/kg, c ของน้ำ = 4,200 J/kg·°C) ต้องใช้ความร้อนรวมเท่าใด"),
                correct=f"{_thai_number(melt + heat)} จูล",
                wrongs=(f"{_thai_number(heat)} จูล", f"{_thai_number(melt)} จูล", f"{_thai_number(melt - heat)} จูล"
                        if melt != 2 * heat else f"{_thai_number(melt + 2 * heat)} จูล"),
                hint="แยกเป็นสองขั้น: หลอมน้ำแข็งด้วย Q = mL แล้วอุ่นน้ำด้วย Q = mcΔT จากนั้นนำมาบวกกัน",
                topic=LATENT_HEAT_TOPIC,
            )
        return _retopic(scenario_question(
            rng, LATENT_HEAT_SCENARIOS,
            hint=("การเปลี่ยนสถานะดูดหรือคายความร้อนจำนวนมากโดยที่อุณหภูมิไม่เปลี่ยน "
                  "ให้คิดแยกเป็นช่วงเปลี่ยนอุณหภูมิกับช่วงเปลี่ยนสถานะเสมอ"),
        ), LATENT_HEAT_TOPIC)
