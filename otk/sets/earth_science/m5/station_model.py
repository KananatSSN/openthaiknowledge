"""สัญลักษณ์ลมฟ้าอากาศบนแผนที่อากาศ

ธรณีวิทยา · ม.5 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/12

Sets moved here from: science_wave_f81.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f81 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_SYMBOL = "สัญลักษณ์ลมฟ้าอากาศบนแผนที่อากาศ"


SYMBOLS = (
    ("อักษร H สีน้ำเงิน", "ศูนย์กลางบริเวณความกดอากาศสูง"),
    ("อักษร L สีแดง", "ศูนย์กลางบริเวณความกดอากาศต่ำ"),
    ("เส้นโค้งที่มีตัวเลขกำกับเช่น 1008", "ไอโซบาร์ เส้นที่ลากผ่านจุดที่มีความกดอากาศเท่ากัน"),
    ("เส้นสีน้ำเงินมีรูปสามเหลี่ยม", "แนวปะทะอากาศเย็น"),
    ("เส้นสีแดงมีรูปครึ่งวงกลม", "แนวปะทะอากาศอุ่น"),
    ("วงกลมเล็กที่ระบายทึบทั้งวง", "ท้องฟ้ามีเมฆเต็มท้องฟ้า"),
    ("วงกลมเล็กที่ไม่ระบายสีเลย", "ท้องฟ้าแจ่มใสไม่มีเมฆ"),
    ("ก้านลมที่ลากออกจากวงกลมสถานี", "ทิศทางที่ลมพัดมา"),
    ("ขีดสั้นบนปลายก้านลม", "อัตราเร็วลม"),
    ("ตัวเลขด้านบนซ้ายของวงกลมสถานี", "อุณหภูมิอากาศ"),
    ("ตัวเลขด้านล่างซ้ายของวงกลมสถานี", "อุณหภูมิจุดน้ำค้าง"),
    ("ตัวเลขสามหลักด้านบนขวาของวงกลมสถานี", "ความกดอากาศที่ระดับน้ำทะเล"),
)


SYMBOL_HINT = ("H ความกดอากาศสูง L ความกดอากาศต่ำ ไอโซบาร์ต่อจุดความกดเท่ากัน วงกลมสถานีระบายตามปริมาณเมฆ "
               "ก้านลมชี้ไปทางที่ลมพัดมา ธงสามเหลี่ยม 50 นอต ขีดยาว 10 นอต ขีดสั้น 5 นอต "
               "รหัสความกดสามหลัก ถ้า 500 ขึ้นไปเติม 9 ข้างหน้า ถ้าต่ำกว่าเติม 10 แล้วใส่จุดทศนิยมหน้าหลักสุดท้าย")


COMPASS = ("ทิศเหนือ", "ทิศตะวันออกเฉียงเหนือ", "ทิศตะวันออก", "ทิศตะวันออกเฉียงใต้", "ทิศใต้", "ทิศตะวันตกเฉียงใต้", "ทิศตะวันตก", "ทิศตะวันตกเฉียงเหนือ")


def _pressure(code: int) -> Fraction:
    return Fraction((9000 if code >= 500 else 10000) + code, 10)


@question_type(
    "geo.station_model_foundation",
    display_name={"th": "ความหมายของสัญลักษณ์บนแผนที่อากาศ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SYMBOL,
)
class StationModelFoundation(QuestionType):
    """Pressure centres, isobars, fronts, and the parts of a station model."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        symbol, meaning = rng.choice(SYMBOLS)
        others = [s for s in SYMBOLS if s[0] != symbol]
        picked = rng.sample(others, 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"บนแผนที่อากาศ สัญลักษณ์ \"{symbol}\" หมายถึงอะไร", correct=meaning, wrongs=tuple(p[1] for p in picked),
                             topic=TOPIC_SYMBOL, hint=SYMBOL_HINT)
        return _labelled(stem=f"บนแผนที่อากาศ ใช้สัญลักษณ์ใดแสดง{meaning}", correct=symbol, wrongs=tuple(p[0] for p in picked),
                         topic=TOPIC_SYMBOL, hint=SYMBOL_HINT)


@question_type(
    "geo.station_model_fluency",
    display_name={"th": "อ่านก้านลม ปริมาณเมฆ และรหัสความกดอากาศ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SYMBOL,
)
class StationModelFluency(QuestionType):
    """Wind speed from barbs, direction from the shaft, pressure from the code."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.4:
            pennant, full, half = rng.randint(0, 1), rng.randint(0, 4), rng.randint(0, 1)
            if pennant + full + half == 0:
                full = 1
            speed = 50 * pennant + 10 * full + 5 * half
            parts = [p for p in (f"ธงสามเหลี่ยม {pennant} อัน" if pennant else "", f"ขีดยาว {full} ขีด" if full else "",
                                  f"ขีดสั้น {half} ขีด" if half else "") if p]
            return numeric(stem=f"ก้านลมบนแผนที่อากาศมี{' '.join(parts)} ลมพัดด้วยอัตราเร็วกี่นอต", answer=speed,
                           wrongs=[pennant + full + half, 10 * (pennant + full + half), speed + 5], unit="นอต", topic=TOPIC_SYMBOL,
                           hint="ธงสามเหลี่ยม 50 นอต ขีดยาว 10 นอต ขีดสั้น 5 นอต แล้วนำมารวมกัน")
        if roll < 0.7:
            code = rng.choice([c for c in range(20, 1000) if c >= 800 or c <= 400])
            right = _pressure(code)
            wrong = Fraction((10000 if code >= 500 else 9000) + code, 10)
            return _labelled(stem=f"รหัสความกดอากาศบนแบบจำลองสถานีเป็น {code:03d} ความกดอากาศจริงเป็นเท่าใด", correct=f"{show(right)} hPa",
                             wrongs=(f"{show(wrong)} hPa", f"{code} hPa", f"{show(Fraction(code, 10))} hPa"), topic=TOPIC_SYMBOL, hint=SYMBOL_HINT)
        shaft = rng.randrange(8)
        return _labelled(stem=f"ก้านลมบนวงกลมสถานีลากชี้ไปทาง{COMPASS[shaft]} ลมที่สถานีนี้คือลมใด", correct=f"ลมพัดมาจาก{COMPASS[shaft]}",
                         wrongs=(f"ลมพัดไปทาง{COMPASS[shaft]}", f"ลมพัดมาจาก{COMPASS[(shaft + 4) % 8]}", f"ลมพัดมาจาก{COMPASS[(shaft + 2) % 8]}"),
                         topic=TOPIC_SYMBOL, hint=SYMBOL_HINT)


@question_type(
    "geo.station_model_application",
    display_name={"th": "คำนวณจากแบบจำลองสถานีและไอโซบาร์"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SYMBOL,
)
class StationModelApplication(QuestionType):
    """Knots to km/h, dew-point spread, and pressure across isobars."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.35:
            knots = rng.randrange(5, 101, 5)
            return numeric(stem=f"แบบจำลองสถานีแสดงลมพัดด้วยอัตราเร็ว {knots} นอต (1 นอต = 1.852 km/h) ลมพัดด้วยอัตราเร็วกี่ km/h",
                           answer=knots * Fraction(1852, 1000), wrongs=[Fraction(knots * 1000, 1852) if (Fraction(knots * 1000, 1852) * 100).denominator == 1 else knots * 2,
                                                                        knots, knots * Fraction(1852, 1000) + 10],
                           unit="km/h", topic=TOPIC_SYMBOL, hint="อัตราเร็ว (km/h) = อัตราเร็ว (นอต) × 1.852")
        if roll < 0.65:
            temp = rng.randint(18, 38)
            dew = temp - rng.randint(1, 15)
            spread = temp - dew
            if rng.random() < 0.5:
                return numeric(stem=f"แบบจำลองสถานีแสดงอุณหภูมิอากาศ {temp} °C และอุณหภูมิจุดน้ำค้าง {dew} °C ผลต่างทั้งสองค่าเป็นกี่ °C",
                               answer=spread, wrongs=[temp + dew, spread + 2, dew], unit="°C", topic=TOPIC_SYMBOL,
                               hint="ผลต่าง = อุณหภูมิอากาศ − จุดน้ำค้าง ยิ่งน้อย อากาศยิ่งใกล้อิ่มตัว")
            a_temp = temp
            b_temp = rng.randint(18, 38)
            b_dew = b_temp - rng.randint(1, 15)
            while b_temp - b_dew == spread:
                b_dew -= 1
            closer = "สถานี ก" if spread < b_temp - b_dew else "สถานี ข"
            return _labelled(stem=f"สถานี ก อุณหภูมิ {a_temp} °C จุดน้ำค้าง {dew} °C สถานี ข อุณหภูมิ {b_temp} °C จุดน้ำค้าง {b_dew} °C "
                                  f"สถานีใดมีโอกาสเกิดหมอกหรือเมฆมากกว่า", correct=closer,
                             wrongs=("สถานี ข" if closer == "สถานี ก" else "สถานี ก", "โอกาสเท่ากัน", "ไม่มีโอกาสทั้งสองสถานี"),
                             topic=TOPIC_SYMBOL, hint="อุณหภูมิอากาศกับจุดน้ำค้างยิ่งใกล้กัน อากาศยิ่งใกล้อิ่มตัว มีโอกาสเกิดหมอกหรือเมฆมาก")
        interval = rng.choice((2, 4))
        start = rng.randrange(996, 1021, interval)
        lines = rng.randint(1, 6)
        rising = rng.random() < 0.5
        end = start + interval * lines if rising else start - interval * lines
        if rng.random() < 0.5:
            return numeric(stem=f"บนแผนที่อากาศลากไอโซบาร์ทุก ๆ {interval} hPa จุด ก อยู่บนเส้น {start} hPa จุด ข อยู่ถัดไปอีก {lines} เส้น "
                                f"ไปทางบริเวณความกดอากาศ{'สูง' if rising else 'ต่ำ'} ความกดอากาศที่จุด ข เป็นกี่ hPa",
                           answer=end, wrongs=[start + lines if rising else start - lines, end + interval if rising else end - interval,
                                               start - interval * lines if rising else start + interval * lines],
                           unit="hPa", topic=TOPIC_SYMBOL, hint="ความกดอากาศเปลี่ยนไปเส้นละเท่ากับช่วงไอโซบาร์")
        return numeric(stem=f"จุด ก อยู่บนไอโซบาร์ {start} hPa จุด ข อยู่บนไอโซบาร์ {end} hPa และแผนที่ลากไอโซบาร์ทุก ๆ {interval} hPa "
                            f"ระหว่างจุด ก กับจุด ข มีช่วงระหว่างไอโซบาร์กี่ช่วง", answer=lines,
                       wrongs=[abs(end - start), lines + 1, lines * interval + 1], unit="ช่วง", topic=TOPIC_SYMBOL,
                       hint="จำนวนช่วง = ผลต่างความกดอากาศ ÷ ช่วงไอโซบาร์")
