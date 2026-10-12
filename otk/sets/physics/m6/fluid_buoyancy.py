"""แรงพยุงจากของไหล

ฟิสิกส์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 4 ม.6/4

Sets moved here from: science_wave_f1.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_f1 import (
    FLUIDS,
    SUBJECT,
    UPPER_SIX,
    G,
    _labelled,
    _num,
    _numeric,
)

PROVENANCE = Provenance("adapted", sources=('sheet_database/Faii/ข้อสอบแรง.pdf',))


TOPIC_BUOYANCY = "แรงพยุงจากของไหล"


OBJECTS = ("ก้อนหิน", "แท่งเหล็ก", "ก้อนโลหะ", "แท่งทองเหลือง")


_SOLIDS = (("ก้อนไม้", 600), ("ก้อนน้ำแข็ง", 920), ("แท่งอะลูมิเนียม", 2700), ("แท่งเหล็ก", 7800),
           ("ก้อนพลาสติก", 950), ("ก้อนยาง", 1100), ("ก้อนตะกั่ว", 11300), ("ไม้ก๊อก", 240))


_FLUIDS = (("น้ำ", 1000), ("น้ำทะเล", 1030), ("น้ำมัน", 900), ("ปรอท", 13600), ("แอลกอฮอล์", 790))


DENSITY_PAIRS = tuple((s, f) for s in _SOLIDS for f in _FLUIDS if s[1] != f[1])


@question_type(
    "phys.fluid_buoyancy_foundation",
    display_name={"th": "ระบุหลักของอาร์คิมีดิสและเงื่อนไขการจมการลอย"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_BUOYANCY,
)
class FluidBuoyancyFoundation(QuestionType):
    """Archimedes' principle and the density rule, before any numbers."""

    FACTS = (
        ("ขนาดของแรงพยุงที่ของไหลกระทำต่อวัตถุเท่ากับข้อใด",
         "น้ำหนักของของไหลที่ถูกวัตถุแทนที่",
         ("น้ำหนักของวัตถุทั้งก้อน",
          "น้ำหนักของของไหลทั้งหมดในภาชนะ",
          "ครึ่งหนึ่งของน้ำหนักของของไหลที่ถูกแทนที่"),
         "หลักของอาร์คิมีดิส — แรงพยุงเท่ากับน้ำหนักของของไหลที่ถูกแทนที่"),
        ("วัตถุจะจมในของเหลวเมื่อใด",
         "เมื่อความหนาแน่นของวัตถุมากกว่าความหนาแน่นของของเหลว",
         ("เมื่อความหนาแน่นของวัตถุน้อยกว่าความหนาแน่นของของเหลว",
          "เมื่อความหนาแน่นของวัตถุเท่ากับความหนาแน่นของของเหลว",
          "เมื่อวัตถุมีปริมาตรมากกว่าของเหลว"),
         "เทียบความหนาแน่น ไม่ใช่มวลหรือปริมาตรอย่างใดอย่างหนึ่ง"),
        ("วัตถุที่ลอยปริ่มในของเหลวพอดี แสดงว่าข้อใดถูกต้อง",
         "ความหนาแน่นของวัตถุเท่ากับความหนาแน่นของของเหลว",
         ("ความหนาแน่นของวัตถุมากกว่าของเหลว",
          "ความหนาแน่นของวัตถุน้อยกว่าของเหลวมาก",
          "วัตถุไม่มีน้ำหนัก"),
         "ลอยปริ่มคือแรงพยุงเท่ากับน้ำหนักพอดีขณะจมทั้งก้อน"),
        ("แรงพยุงที่ของเหลวกระทำต่อวัตถุที่จมทั้งก้อนขึ้นกับสิ่งใด",
         "ความหนาแน่นของของเหลวและปริมาตรของวัตถุที่จม",
         ("ความหนาแน่นของวัตถุและมวลของวัตถุ",
          "ความลึกที่วัตถุจมอยู่",
          "รูปร่างของวัตถุ"),
         "F พยุง = ρVg โดย ρ เป็นของของเหลว และ V เป็นปริมาตรส่วนที่จม"),
    )

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.65:
            (thing, rho), (fluid, rho_f) = rng.choice(DENSITY_PAIRS)
            sinks = rho > rho_f
            return _labelled(
                stem=(f"{thing}มีความหนาแน่น {_num(rho)} kg/m³ ปล่อยลงใน{fluid}ซึ่งมีความหนาแน่น {_num(rho_f)} kg/m³ "
                      f"{thing}จะจมหรือลอย และแรงพยุงขณะนั้นเทียบกับน้ำหนักเป็นอย่างไร"),
                correct=("จม เพราะแม้จมทั้งก้อน แรงพยุงก็ยังน้อยกว่าน้ำหนัก" if sinks
                         else "ลอย โดยจมเพียงบางส่วนจนแรงพยุงเท่ากับน้ำหนักพอดี"),
                wrongs=(("ลอย โดยจมเพียงบางส่วนจนแรงพยุงเท่ากับน้ำหนักพอดี" if sinks
                         else "จม เพราะแม้จมทั้งก้อน แรงพยุงก็ยังน้อยกว่าน้ำหนัก"),
                        "ลอยปริ่ม เพราะแรงพยุงเท่ากับน้ำหนักขณะจมทั้งก้อน",
                        "ลอยขึ้นพ้นของเหลวทั้งก้อน เพราะแรงพยุงมากกว่าน้ำหนักตลอดเวลา"),
                topic=TOPIC_BUOYANCY, hint="เทียบความหนาแน่นของวัตถุกับของของเหลว มากกว่าจม น้อยกว่าลอย",
            )
        stem, correct, wrongs, hint = rng.choice(self.FACTS)
        return _labelled(stem=stem, correct=correct, wrongs=wrongs,
                         topic=TOPIC_BUOYANCY, hint=hint)


@question_type(
    "phys.fluid_buoyancy_fluency",
    display_name={"th": "คำนวณแรงพยุงจากน้ำหนักที่ชั่งในอากาศและในของเหลว"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_BUOYANCY,
)
class FluidBuoyancyFluency(QuestionType):
    """The sheet's ข้อ 21, 22 and 24: two spring-scale readings."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        in_air = round(rng.uniform(20, 80), 1)
        buoyant = round(rng.uniform(3, min(18, in_air - 2)), 1)
        in_water = round(in_air - buoyant, 1)
        buoyant = round(in_air - in_water, 1)           # re-derive after rounding
        item = rng.choice(OBJECTS)
        return _numeric(
            stem=(f"ชั่ง{item}ก้อนหนึ่งในอากาศได้ {_num(in_air)} นิวตัน "
                  f"แต่เมื่อชั่งขณะจมอยู่ในน้ำทั้งก้อนได้ {_num(in_water)} นิวตัน "
                  f"จงหาแรงพยุงที่น้ำกระทำต่อ{item}นี้"),
            answer=buoyant, unit="นิวตัน",
            # Adding the two readings, and reporting one of them unchanged.
            slips=(in_air + in_water, in_water, in_air, buoyant * 2),
            fillers=(buoyant + 1, buoyant + 2.5, buoyant + 5),
            topic=TOPIC_BUOYANCY,
            hint="แรงพยุง = น้ำหนักที่ชั่งในอากาศ − น้ำหนักที่ชั่งในของเหลว",
        )


@question_type(
    "phys.fluid_buoyancy_application",
    display_name={"th": "ใช้ F = ρVg หาแรงพยุงหรือปริมาตรที่จม"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_BUOYANCY,
)
class FluidBuoyancyApplication(QuestionType):
    """The sheet's ข้อ 23 and 25, run in both directions."""

    VOLUMES = (0.001, 0.002, 0.005, 0.01, 0.02, 0.05, 0.1, 0.5, 1, 2)

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, rho = rng.choice(FLUIDS)
        volume = rng.choice(self.VOLUMES)
        force = rho * volume * G
        if rng.random() < 0.5:
            return _numeric(
                stem=(f"จุ่ม{rng.choice(OBJECTS)}ซึ่งมีปริมาตร {_num(volume)} ลูกบาศก์เมตร "
                      f"ลงใน{name}ที่มีความหนาแน่น {rho} กิโลกรัมต่อลูกบาศก์เมตร จนจมทั้งก้อน "
                      f"จงหาแรงพยุงที่{name}กระทำต่อวัตถุ (กำหนดให้ g = {G} เมตรต่อวินาที²)"),
                answer=force, unit="นิวตัน",
                slips=(rho * volume, volume * G, force * 2, rho * G),
                fillers=(force + 10, force + 50, force + 100),
                topic=TOPIC_BUOYANCY,
                hint="F พยุง = ρVg โดย ρ เป็นความหนาแน่นของของเหลว และ V เป็นปริมาตรส่วนที่จม",
            )
        return _numeric(
            stem=(f"วัตถุก้อนหนึ่งจมอยู่ใน{name}ทั้งก้อน โดย{name}มีความหนาแน่น {rho} กิโลกรัมต่อลูกบาศก์เมตร "
                  f"ถ้าแรงพยุงที่กระทำต่อวัตถุเท่ากับ {_num(force)} นิวตัน จงหาปริมาตรของวัตถุ "
                  f"(กำหนดให้ g = {G} เมตรต่อวินาที²)"),
            answer=volume, unit="ลูกบาศก์เมตร",
            slips=(force / rho, force / G, volume * 2, volume / 2),
            fillers=(volume + 0.5, volume + 1, volume + 2),
            topic=TOPIC_BUOYANCY,
            hint="จาก F พยุง = ρVg จะได้ V = F / (ρg)",
        )
