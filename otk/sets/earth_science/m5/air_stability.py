"""เสถียรภาพอากาศและการเกิดเมฆ

ธรณีวิทยา · ม.5 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/8

Sets moved here from: science_wave_f79.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f79 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_STABLE = "เสถียรภาพอากาศและการเกิดเมฆ"


STABLE_FACTS = (
    ("อากาศไม่มีเสถียรภาพหมายถึงข้อใด", "กลุ่มอากาศที่ยกตัวขึ้นอุ่นกว่าอากาศรอบข้าง จึงลอยตัวสูงขึ้นต่อไปได้เอง",
     ("กลุ่มอากาศที่ยกตัวขึ้นเย็นกว่าอากาศรอบข้าง จึงจมกลับลงมา", "อากาศไม่เคลื่อนที่เลย เพราะอุณหภูมิไม่เปลี่ยนตามความสูง", "กลุ่มอากาศที่ยกตัวขึ้นเย็นกว่าอากาศรอบข้าง จึงลอยสูงขึ้นต่อไปได้", "อากาศที่อุณหภูมิไม่เปลี่ยนตามความสูง จึงไม่มีกลุ่มอากาศใดยกตัวได้")),
    ("อากาศมีเสถียรภาพหมายถึงข้อใด", "กลุ่มอากาศที่ยกตัวขึ้นเย็นกว่าอากาศรอบข้าง จึงจมกลับลงมา",
     ("กลุ่มอากาศที่ยกตัวขึ้นอุ่นกว่าอากาศรอบข้าง จึงลอยตัวสูงขึ้นต่อไปได้เอง", "อากาศที่มีพายุฝนฟ้าคะนองและเมฆก่อตัวสูง", "อากาศที่มีเมฆคิวมูโลนิมบัส", "กลุ่มอากาศที่ยกตัวขึ้นอุ่นกว่าอากาศรอบข้าง จึงจมกลับลงมา")),
    ("อากาศไม่มีเสถียรภาพมักทำให้เกิดเมฆแบบใด", "เมฆก่อตัวในแนวตั้ง เช่น คิวมูลัสและคิวมูโลนิมบัส",
     ("เมฆแผ่นเป็นชั้น เช่น สเตรตัส", "เมฆแผ่นเป็นชั้นบาง ๆ เช่น สเตรตัสและอัลโตสเตรตัส", "หมอกบาง ๆ ติดพื้น และเมฆเซอร์รัสบนท้องฟ้าสูง", "เมฆเซอร์รัสเพียงอย่างเดียว")),
    ("อากาศมีเสถียรภาพที่ถูกบังคับให้ยกตัวมักทำให้เกิดเมฆแบบใด", "เมฆแผ่นเป็นชั้น เช่น สเตรตัสและนิมโบสเตรตัส",
     ("เมฆคิวมูโลนิมบัสก่อตัวสูง", "พายุฝนฟ้าคะนองรุนแรง", "เมฆก่อตัวในแนวตั้ง เช่น คิวมูลัสและคิวมูโลนิมบัส", "พายุฝนฟ้าคะนองรุนแรงพร้อมลูกเห็บตกหนัก")),
    ("อุณหภูมิผกผัน (inversion) คือสภาพใด", "อุณหภูมิอากาศสูงขึ้นตามความสูง ทำให้อากาศมีเสถียรภาพมาก",
     ("อุณหภูมิลดลงเร็วมากตามความสูง", "อากาศลอยตัวแรงจนเกิดพายุ เพราะอากาศด้านบนอุ่นกว่า", "อุณหภูมิลดลงเร็วมากตามความสูง อากาศจึงไม่มีเสถียรภาพ", "อากาศไม่มีเสถียรภาพสัมบูรณ์ จึงลอยตัวขึ้นได้ตลอดเวลา")),
    ("เหตุใดหมอกควันในภาคเหนือช่วงเช้าฤดูหนาวจึงสะสมอยู่ใกล้พื้น", "เกิดอุณหภูมิผกผัน อากาศมีเสถียรภาพ ฝุ่นควันจึงลอยตัวขึ้นไม่ได้",
     ("อากาศไม่มีเสถียรภาพ ฝุ่นจึงลอยสูง", "เกิดอุณหภูมิผกผัน อากาศไม่มีเสถียรภาพ ฝุ่นจึงลอยตัวสูงขึ้น", "อากาศไม่มีเสถียรภาพ ฝุ่นควันจึงลอยตัวสูงจนเห็นเป็นหมอกหนา", "แสงแดดแรงจนฝุ่นหนักขึ้น")),
    ("กลุ่มอากาศที่ลอยตัวขึ้นอุณหภูมิลดลงเพราะเหตุใด", "ความกดอากาศลดลง อากาศจึงขยายตัวและเย็นลง",
     ("อากาศได้รับความร้อนจากดวงอาทิตย์น้อยลงเท่านั้น", "ความกดอากาศเพิ่มขึ้น อากาศจึงถูกอัดตัวและเย็นลง", "อากาศสูญเสียไอน้ำทั้งหมดจึงเย็นลง", "แรงโน้มถ่วงดึงความร้อนลงมา")),
    ("จุดน้ำค้างคืออะไร", "อุณหภูมิที่อากาศเย็นลงจนไอน้ำอิ่มตัวและเริ่มควบแน่น",
     ("อุณหภูมิที่ไอน้ำในอากาศเดือดกลายเป็นแก๊สทั้งหมด", "อุณหภูมิที่อากาศร้อนขึ้นจนไอน้ำระเหยออกไปหมด", "อุณหภูมิที่น้ำแข็งละลาย", "อุณหภูมิเฉลี่ยของอากาศทั้งวัน")),
    ("เหตุใดอากาศอิ่มตัวที่ยกตัวขึ้นจึงเย็นลงช้ากว่าอากาศแห้ง", "ไอน้ำควบแน่นปล่อยความร้อนแฝงให้กลุ่มอากาศ",
     ("อากาศอิ่มตัวได้รับแสงอาทิตย์มากกว่า", "อากาศอิ่มตัวไม่ขยายตัวเลยเมื่อยกตัวขึ้น", "อากาศอิ่มตัวหนักกว่าจึงไม่ยกตัว", "ไอน้ำควบแน่นดูดความร้อนแฝงออกจากอากาศ")),
)


STABLE_HINT = ("กลุ่มอากาศยกตัวแล้วเย็นลงแบบแอเดียแบติก ถ้ายังอุ่นกว่าอากาศรอบข้างจะลอยต่อ (ไม่มีเสถียรภาพ เมฆก่อตัวแนวตั้ง) "
               "ถ้าเย็นกว่าจะจมกลับ (มีเสถียรภาพ เมฆแผ่เป็นชั้นหรือไม่เกิดเมฆ) อากาศแห้งเย็นลง 10 °C ต่อ km อากาศอิ่มตัว 6 °C ต่อ km")


@question_type(
    "geo.air_stability_foundation",
    display_name={"th": "เสถียรภาพอากาศและชนิดของเมฆ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_STABLE,
)
class AirStabilityFoundation(QuestionType):
    """Stable and unstable air, clouds, inversions."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(STABLE_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_STABLE, hint=STABLE_HINT)


@question_type(
    "geo.air_stability_fluency",
    display_name={"th": "ตัดสินเสถียรภาพอากาศจากอุณหภูมิและอัตราการลดลงของอุณหภูมิ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_STABLE,
)
class AirStabilityFluency(QuestionType):
    """Parcel against surroundings; environmental lapse rate against 6 and 10."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            height = rng.choice((500, 1000, 1500, 2000, 2500, 3000))
            parcel = rng.randint(5, 30)
            around = parcel + rng.choice([d for d in range(-6, 7) if d != 0])
            warmer = parcel > around
            right = ("ไม่มีเสถียรภาพ กลุ่มอากาศจะลอยตัวสูงขึ้นต่อไป" if warmer else "มีเสถียรภาพ กลุ่มอากาศจะจมกลับลงมา")
            return _labelled(stem=f"กลุ่มอากาศยกตัวถึงความสูง {show(height)} m มีอุณหภูมิ {parcel} °C ขณะที่อากาศรอบข้างที่ระดับเดียวกันมีอุณหภูมิ {around} °C "
                                  f"อากาศบริเวณนี้มีเสถียรภาพแบบใด",
                             correct=right, wrongs=("มีเสถียรภาพ กลุ่มอากาศจะจมกลับลงมา" if warmer else "ไม่มีเสถียรภาพ กลุ่มอากาศจะลอยตัวสูงขึ้นต่อไป",
                                                    "ไม่มีเสถียรภาพ กลุ่มอากาศจะจมกลับลงมา", "มีเสถียรภาพ กลุ่มอากาศจะลอยตัวสูงขึ้นต่อไป"),
                             topic=TOPIC_STABLE, hint=STABLE_HINT)
        rate = Fraction(rng.choice([n for n in range(20, 141, 5) if n not in (60, 100)]), 10)
        right = ("มีเสถียรภาพสัมบูรณ์" if rate < 6 else "ไม่มีเสถียรภาพสัมบูรณ์" if rate > 10 else "มีเสถียรภาพแบบมีเงื่อนไข")
        return _labelled(stem=f"อุณหภูมิอากาศรอบข้างลดลง {show(rate)} °C ต่อความสูง 1 km (อากาศแห้งลดลง 10 °C ต่อ km อากาศอิ่มตัวลดลง 6 °C ต่อ km) "
                              f"อากาศบริเวณนี้มีเสถียรภาพแบบใด",
                         correct=right, wrongs=tuple(o for o in ("มีเสถียรภาพสัมบูรณ์", "ไม่มีเสถียรภาพสัมบูรณ์", "มีเสถียรภาพแบบมีเงื่อนไข",
                                                                "ไม่สามารถเกิดเมฆได้ทุกกรณี") if o != right),
                         topic=TOPIC_STABLE, hint=STABLE_HINT + " ถ้าอากาศรอบข้างลดลงช้ากว่า 6 มีเสถียรภาพสัมบูรณ์ เร็วกว่า 10 ไม่มีเสถียรภาพสัมบูรณ์ "
                                                               "อยู่ระหว่างนั้นขึ้นกับว่ากลุ่มอากาศอิ่มตัวหรือไม่")


@question_type(
    "geo.air_stability_application",
    display_name={"th": "คำนวณอุณหภูมิกลุ่มอากาศที่ยกตัวและความสูงฐานเมฆ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_STABLE,
)
class AirStabilityApplication(QuestionType):
    """Dry cooling to the cloud base, then saturated cooling above it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        rule = "(อากาศไม่อิ่มตัวเย็นลง 10 °C ต่อ km อากาศอิ่มตัวเย็นลง 6 °C ต่อ km และถือว่าจุดน้ำค้างคงที่)"
        temp = rng.randint(24, 36)
        dew = temp - rng.randint(3, 15)
        base = Fraction(temp - dew, 10)
        roll = rng.random()
        if roll < 0.35:
            return numeric(stem=f"อากาศที่ผิวพื้นอุณหภูมิ {temp} °C จุดน้ำค้าง {dew} °C {rule} ฐานเมฆจะอยู่สูงกี่เมตร",
                           answer=base * 1000, wrongs=[Fraction(temp - dew, 6) * 1000 if (Fraction(temp - dew, 6) * 100000).denominator == 1 else base * 2000,
                                                       (temp - dew) * 10, base * 1000 + 500],
                           unit="m", topic=TOPIC_STABLE, hint="ฐานเมฆอยู่ที่ระดับที่อุณหภูมิลดลงจนเท่าจุดน้ำค้าง ความสูง = (T − Td) ÷ 10 km")
        if roll < 0.65:
            height = Fraction(rng.randrange(2, int(base * 10) + 1), 10) if base >= Fraction(2, 10) else base
            return numeric(stem=f"อากาศไม่อิ่มตัวที่ผิวพื้นอุณหภูมิ {temp} °C จุดน้ำค้าง {dew} °C ยกตัวขึ้นสูง {show(height * 1000)} m {rule} "
                                f"กลุ่มอากาศมีอุณหภูมิกี่ °C", answer=temp - 10 * height,
                           wrongs=[temp - 6 * height, temp - height, temp - 10 * height - 2], unit="°C", topic=TOPIC_STABLE,
                           hint="ต่ำกว่าฐานเมฆ อุณหภูมิลดลง 10 °C ต่อ km", allow_negative=True)
        top = base + Fraction(rng.randint(5, 25), 10)
        answer = dew - 6 * (top - base)
        return numeric(stem=f"อากาศที่ผิวพื้นอุณหภูมิ {temp} °C จุดน้ำค้าง {dew} °C ถูกยกตัวข้ามภูเขาสูง {show(top * 1000)} m {rule} "
                            f"เมื่อถึงยอดเขากลุ่มอากาศมีอุณหภูมิกี่ °C", answer=answer,
                       wrongs=[temp - 10 * top, temp - 6 * top, dew - 10 * (top - base)], unit="°C", topic=TOPIC_STABLE,
                       hint="ยกตัวแบบแห้งจนถึงฐานเมฆ (อุณหภูมิเท่าจุดน้ำค้าง) แล้วเย็นลง 6 °C ต่อ km ที่เหลือ", allow_negative=True)
