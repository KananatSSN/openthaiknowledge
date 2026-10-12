"""ความดันเกจและความดันสัมบูรณ์

ฟิสิกส์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 4 ม.6/3

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


TOPIC_GAUGE_PRESSURE = "ความดันเกจและความดันสัมบูรณ์"


ATM = 100000                             # Pa, the atmospheric pressure used here


DEPTHS = (0.1, 0.2, 0.5, 1, 2, 2.5, 4, 5, 10)


DEPTH_POINTS = (("ก", 0.5), ("ข", 1), ("ค", 1.5), ("ง", 2), ("จ", 3), ("ฉ", 4), ("ช", 5))


@question_type(
    "phys.gauge_pressure_foundation",
    display_name={"th": "แยกความดันเกจ ความดันสัมบูรณ์ และความดันบรรยากาศ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_GAUGE_PRESSURE,
)
class GaugePressureFoundation(QuestionType):
    """What the three pressures mean, and what the instruments read."""

    FACTS = (
        ("ความดันเกจหมายถึงข้อใด",
         "ความดันที่วัดเทียบกับความดันบรรยากาศ",
         ("ความดันที่วัดเทียบกับสุญญากาศ",
          "ความดันบรรยากาศที่ระดับน้ำทะเล",
          "ผลรวมของความดันบรรยากาศกับความดันของของเหลว"),
         "เกจอ่านค่าเป็นศูนย์เมื่ออยู่ในอากาศปกติ"),
        ("ความดันสัมบูรณ์ที่ความลึกหนึ่งในของเหลวหาได้จากข้อใด",
         "ความดันบรรยากาศบวกกับความดันเกจที่ความลึกนั้น",
         ("ความดันบรรยากาศลบด้วยความดันเกจ",
          "ความดันเกจเพียงอย่างเดียว",
          "ความดันบรรยากาศเพียงอย่างเดียว"),
         "P สัมบูรณ์ = P บรรยากาศ + ρgh"),
        ("ความดันของของเหลวที่ความลึกหนึ่งขึ้นกับสิ่งใด",
         "ความหนาแน่นของของเหลวและความลึกจากผิวของเหลว",
         ("รูปร่างและความกว้างของภาชนะ",
          "ปริมาตรทั้งหมดของของเหลวในภาชนะ",
          "พื้นที่ก้นภาชนะ"),
         "P = ρgh — ไม่มีพจน์ของรูปทรงภาชนะอยู่ในสูตร"),
        ("เครื่องมือในข้อใดใช้วัดความดันบรรยากาศ",
         "บารอมิเตอร์",
         ("แมนอมิเตอร์", "เครื่องอัดไฮดรอลิก", "เครื่องชั่งสปริง"),
         "บารอมิเตอร์วัดความดันบรรยากาศ ส่วนแมนอมิเตอร์วัดความดันของแก๊สในภาชนะ"),
        ("เครื่องอัดไฮดรอลิกอาศัยหลักการใด",
         "ความดันที่เพิ่มให้ของเหลวในภาชนะปิดถ่ายทอดไปทุกส่วนเท่ากัน",
         ("ของเหลวมีความหนาแน่นมากกว่าของแข็ง",
          "แรงพยุงของของเหลวมากกว่าน้ำหนักของวัตถุ",
          "ความดันของของเหลวลดลงเมื่อความลึกเพิ่มขึ้น"),
         "หลักของปาสกาล — ความดันที่เพิ่มถ่ายทอดเท่ากันทั่วของเหลว"),
    )

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.35:
            (a, da), (b, db) = rng.sample(DEPTH_POINTS, 2)
            liquid = rng.choice(("น้ำ", "น้ำทะเล", "น้ำมัน"))
            deeper = a if da > db else b
            shallower = b if da > db else a
            return _labelled(
                stem=(f"ในถัง{liquid}ใบเดียวกัน จุด{a}ลึก {_num(da)} เมตร และจุด{b}ลึก {_num(db)} เมตร "
                      "จุดใดมีความดันเกจมากกว่า"),
                correct=f"จุด{deeper} เพราะลึกกว่า ความดัน ρgh จึงมากกว่า",
                wrongs=(f"จุด{shallower} เพราะใกล้ผิวของเหลวมากกว่า", "เท่ากัน เพราะอยู่ในถังเดียวกัน",
                        f"จุด{shallower} เพราะลึกกว่า ความดัน ρgh จึงมากกว่า"),
                topic=TOPIC_GAUGE_PRESSURE, hint="ในของเหลวชนิดเดียวกัน ความดันเกจขึ้นกับความลึกเท่านั้น",
            )
        if roll < 0.65:
            gauge = rng.choice([g for g in range(10_000, 300_001, 10_000) if g != ATM])
            if rng.random() < 0.5:
                return _labelled(
                    stem=(f"ความดันเกจที่ก้นสระวัดได้ {_num(gauge)} พาสคัล ถ้าความดันบรรยากาศเท่ากับ {_num(ATM)} พาสคัล "
                          "ความดันสัมบูรณ์ที่ก้นสระเท่ากับเท่าใด"),
                    correct=f"{_num(ATM + gauge)} พาสคัล",
                    wrongs=(f"{_num(gauge)} พาสคัล", f"{_num(ATM + 2 * gauge)} พาสคัล", f"{_num(ATM)} พาสคัล"),
                    topic=TOPIC_GAUGE_PRESSURE, hint="P สัมบูรณ์ = P บรรยากาศ + P เกจ",
                )
            return _labelled(
                stem=(f"ความดันสัมบูรณ์ภายในยางรถวัดได้ {_num(ATM + gauge)} พาสคัล ถ้าความดันบรรยากาศเท่ากับ "
                      f"{_num(ATM)} พาสคัล เกจวัดลมยางจะอ่านได้เท่าใด"),
                correct=f"{_num(gauge)} พาสคัล",
                wrongs=(f"{_num(ATM + gauge)} พาสคัล", f"{_num(ATM + 2 * gauge)} พาสคัล", f"{_num(ATM)} พาสคัล"),
                topic=TOPIC_GAUGE_PRESSURE, hint="เกจอ่านค่าเทียบกับบรรยากาศ: P เกจ = P สัมบูรณ์ − P บรรยากาศ",
            )
        stem, correct, wrongs, hint = rng.choice(self.FACTS)
        return _labelled(stem=stem, correct=correct, wrongs=wrongs,
                         topic=TOPIC_GAUGE_PRESSURE, hint=hint)


@question_type(
    "phys.gauge_pressure_fluency",
    display_name={"th": "คำนวณความดันเกจของของเหลวด้วย P = ρgh"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_GAUGE_PRESSURE,
)
class GaugePressureFluency(QuestionType):
    """The sheet's ข้อ 6 and ข้อ 7: gauge pressure at a stated depth."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, rho = rng.choice(FLUIDS)
        depth = rng.choice(DEPTHS)
        answer = rho * G * depth
        return _numeric(
            stem=(f"ถังเปิดใบหนึ่งบรรจุ{name}ซึ่งมีความหนาแน่น {rho} กิโลกรัมต่อลูกบาศก์เมตร "
                  f"จงหาความดันเกจที่จุดซึ่งอยู่ลึกจากผิว{name} {_num(depth)} เมตร "
                  f"(กำหนดให้ g = {G} เมตรต่อวินาที²)"),
            answer=answer, unit="พาสคัล",
            # Dropping g, and dropping the depth, are the two usual slips.
            slips=(rho * depth, rho * G, answer / 2, rho * G * depth * 2),
            fillers=(answer + 1000, answer + 500, answer + 100),
            topic=TOPIC_GAUGE_PRESSURE,
            hint="P = ρgh โดย ρ เป็นความหนาแน่น g = 10 และ h เป็นความลึกจากผิวของเหลว",
        )


@question_type(
    "phys.gauge_pressure_application",
    display_name={"th": "หาความดันสัมบูรณ์และแรงดันที่ก้นภาชนะ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_GAUGE_PRESSURE,
)
class GaugePressureApplication(QuestionType):
    """Absolute pressure, and F = PA on a horizontal bottom (the sheet's ข้อ 10).

    Only the flat bottom is asked for. On a vertical wall the pressure varies
    with depth and ``F = PA`` with a single pressure is wrong — the mistake the
    sheet's own ข้อ 5 makes.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, rho = rng.choice(FLUIDS)
        depth = rng.choice((1, 2, 2.5, 4, 5))
        gauge = rho * G * depth
        if rng.random() < 0.5:
            return _numeric(
                stem=(f"ถังเปิดใบหนึ่งบรรจุ{name}ซึ่งมีความหนาแน่น {rho} กิโลกรัมต่อลูกบาศก์เมตร สูง {_num(depth)} เมตร "
                      f"ถ้าความดันบรรยากาศเท่ากับ {ATM} พาสคัล จงหาความดันสัมบูรณ์ที่ก้นถัง "
                      f"(กำหนดให้ g = {G} เมตรต่อวินาที²)"),
                answer=ATM + gauge, unit="พาสคัล",
                slips=(gauge, ATM - gauge, ATM, ATM + gauge * 2),
                fillers=(ATM + gauge + 1000, ATM + gauge + 5000, ATM + gauge + 500),
                topic=TOPIC_GAUGE_PRESSURE,
                hint=f"P สัมบูรณ์ = P บรรยากาศ + ρgh โดย ρgh = {_num(gauge)} พาสคัล",
            )
        side_a = rng.choice((1, 2, 3))
        side_b = rng.choice((1, 2, 4))
        area = side_a * side_b
        return _numeric(
            stem=(f"ถังก้นเรียบรูปสี่เหลี่ยมมีก้นถังกว้าง {side_a} เมตร ยาว {side_b} เมตร "
                  f"บรรจุ{name}ซึ่งมีความหนาแน่น {rho} กิโลกรัมต่อลูกบาศก์เมตร สูง {_num(depth)} เมตร "
                  f"จงหาแรงที่{name}ดันก้นถัง (กำหนดให้ g = {G} เมตรต่อวินาที²)"),
            answer=gauge * area, unit="นิวตัน",
            # Reporting the pressure instead of the force, and dividing by the
            # area rather than multiplying.
            slips=(gauge, gauge / area, gauge * area * 2, area),
            fillers=(gauge * area + 1000, gauge * area + 5000, gauge * area + 500),
            topic=TOPIC_GAUGE_PRESSURE,
            hint=(f"หาความดันที่ก้นถังจาก P = ρgh ได้ {_num(gauge)} พาสคัล "
                  f"แล้วใช้ F = PA โดย A = {_num(area)} ตารางเมตร"),
        )
