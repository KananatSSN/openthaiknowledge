"""การเปลี่ยนพลังงานทดแทนเป็นพลังงานไฟฟ้า

ฟิสิกส์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 3 ม.5/11

Sets moved here from: science_wave_f12.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import G, _labelled, numeric, show
from otk.sets._support.science_wave_f12 import SUBJECT, UPPER_FIVE, _exact

PROVENANCE = Provenance("original")


TOPIC_RENEWABLE = "การเปลี่ยนพลังงานทดแทนเป็นพลังงานไฟฟ้า"


SOURCES = (
    ("เซลล์สุริยะ", "พลังงานแสงเป็นพลังงานไฟฟ้าโดยตรง"),
    ("กังหันลม", "พลังงานจลน์ของลมหมุนกังหันและเครื่องกำเนิดไฟฟ้า"),
    ("เขื่อนผลิตไฟฟ้า", "พลังงานศักย์ของน้ำเปลี่ยนเป็นพลังงานจลน์หมุนกังหันและเครื่องกำเนิดไฟฟ้า"),
    ("โรงไฟฟ้าความร้อนใต้พิภพ", "ความร้อนจากใต้ดินทำให้น้ำเดือดเป็นไอหมุนกังหัน"),
    ("โรงไฟฟ้าชีวมวล", "พลังงานเคมีในเศษวัสดุการเกษตรเผาให้ความร้อนผลิตไอน้ำหมุนกังหัน"),
    ("โรงไฟฟ้าพลังงานคลื่น", "การขึ้นลงของคลื่นทะเลขับเครื่องกำเนิดไฟฟ้า"),
)


@question_type(
    "phys.renewable_electricity_foundation",
    display_name={"th": "การเปลี่ยนพลังงานทดแทนแต่ละแบบเป็นพลังงานไฟฟ้า"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_RENEWABLE,
)
class RenewableElectricityFoundation(QuestionType):
    """Which conversion each renewable plant makes."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        chosen = rng.sample(SOURCES, 4)
        plant, how = chosen[0]
        hint = "นอกจากเซลล์สุริยะ แหล่งพลังงานส่วนใหญ่ใช้หมุนกังหันที่ต่อกับเครื่องกำเนิดไฟฟ้า"
        if rng.random() < 0.5:
            return _labelled(stem=f"{plant}เปลี่ยนพลังงานอย่างไร", correct=how,
                             wrongs=tuple(h for _, h in chosen[1:]), topic=TOPIC_RENEWABLE, hint=hint)
        return _labelled(stem=f"แหล่งผลิตไฟฟ้าใดเปลี่ยน{how}", correct=plant,
                         wrongs=tuple(p for p, _ in chosen[1:]), topic=TOPIC_RENEWABLE, hint=hint)


@question_type(
    "phys.renewable_electricity_fluency",
    display_name={"th": "คำนวณกำลังไฟฟ้าจากเซลล์สุริยะและพลังน้ำ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_RENEWABLE,
)
class RenewableElectricityFluency(QuestionType):
    """Output power = efficiency × input: sunlight on a panel, or water falling through a dam."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            area = Fraction(rng.randint(2, 40), 2)
            sun = rng.choice((800, 1000))
            eff = rng.choice((15, 18, 20, 22, 25))
            power = area * sun * eff / 100
            return numeric(
                stem=(f"แผงเซลล์สุริยะพื้นที่ {show(area)} m² ได้รับแสงอาทิตย์ {sun:,} W/m² มีประสิทธิภาพร้อยละ {eff} "
                      "ผลิตกำลังไฟฟ้าได้เท่าใด"),
                answer=power, wrongs=[area * sun, area * sun * (100 - eff) / 100, sun * eff / 100],
                unit="W", topic=TOPIC_RENEWABLE, hint="กำลังไฟฟ้า = ประสิทธิภาพ × ความเข้มแสง × พื้นที่")
        flow = rng.randint(1, 20)
        h = rng.randint(2, 20) * 5
        eff = rng.choice((70, 75, 80, 85, 90))
        power = Fraction(flow * 1000 * G * h * eff, 100) / 1000
        return numeric(
            stem=(f"น้ำไหลผ่านกังหันของเขื่อน {flow} m³/s ตกจากความสูง {h} m ระบบมีประสิทธิภาพร้อยละ {eff} "
                  "ผลิตกำลังไฟฟ้าได้กี่กิโลวัตต์ (ความหนาแน่นน้ำ 1,000 kg/m³, g = 10 m/s²)"),
            answer=power, wrongs=[flow * G * h, power * 1000 / eff * 100 / 1000, flow * 1000 * G * h],
            unit="kW", topic=TOPIC_RENEWABLE,
            hint="มวลน้ำต่อวินาที = 1,000 × อัตราการไหล กำลัง = ประสิทธิภาพ × (m/t)gh")


@question_type(
    "phys.renewable_electricity_application",
    display_name={"th": "ความคุ้มค่าของเทคโนโลยีด้านพลังงานไฟฟ้า"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_RENEWABLE,
)
class RenewableElectricityApplication(QuestionType):
    """Energy bills in kWh, and the years a solar roof or an LED swap takes to pay back."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        price = rng.choice((4, 5, Fraction(9, 2), 6))
        if rng.random() < 0.5:
            old, new, hours, lamps = rng.choice([(o, n, h, ell) for o, n in ((60, 9), (100, 15), (40, 6), (60, 10), (100, 12))
                                                 for h in (4, 5, 6, 8, 10) for ell in range(2, 11)
                                                 if _exact(Fraction((o - n) * h * 30 * ell, 1000) * price)])
            days = 30
            saved = Fraction((old - new) * hours * days * lamps, 1000) * price
            return numeric(
                stem=(f"เปลี่ยนหลอดไส้ {old} W จำนวน {lamps} หลอด เป็นหลอด LED {new} W ที่ให้แสงสว่างเท่ากัน "
                      f"เปิดวันละ {hours} ชั่วโมง ประหยัดค่าไฟฟ้าได้กี่บาทใน {days} วัน (ค่าไฟหน่วยละ {show(price)} บาท)"),
                answer=saved, wrongs=[Fraction(old * hours * days * lamps, 1000) * price,
                                      Fraction((old - new) * hours * days, 1000) * price, saved * 1000],
                unit="บาท", topic=TOPIC_RENEWABLE,
                hint="พลังงานที่ประหยัด (kWh) = ผลต่างกำลัง (kW) × ชั่วโมงรวม แล้วคูณราคาต่อหน่วย (1 หน่วย = 1 kWh)")
        kw = rng.choice((3, 5, 10))
        cost = kw * rng.choice((30000, 35000, 40000))
        units = kw * rng.choice((120, 125, 130, 140, 150))
        yearly = units * 12 * price
        years = Fraction(cost, 1) / yearly
        if not _exact(years):
            cost = int(yearly * rng.choice((4, 5, 6, 7, 8)))
            years = Fraction(cost) / yearly
        return numeric(
            stem=(f"ติดตั้งเซลล์สุริยะบนหลังคาขนาด {kw} kW ราคา {cost:,} บาท ผลิตไฟฟ้าได้เดือนละ {units:,} หน่วย "
                  f"ถ้าค่าไฟหน่วยละ {show(price)} บาท ต้องใช้กี่ปีจึงคืนทุน"),
            answer=years, wrongs=[years * 12, Fraction(cost) / (units * price), years / 2], unit="ปี",
            topic=TOPIC_RENEWABLE, hint="เงินที่ประหยัดต่อปี = หน่วยต่อเดือน × 12 × ราคาต่อหน่วย แล้วระยะคืนทุน = ราคาติดตั้ง ÷ เงินที่ประหยัดต่อปี")
