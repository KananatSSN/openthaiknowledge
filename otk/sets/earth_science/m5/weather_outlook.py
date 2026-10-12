"""การคาดการณ์ลมฟ้าอากาศจากแผนที่อากาศ

ธรณีวิทยา · ม.5 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/13

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


TOPIC_OUTLOOK = "การคาดการณ์ลมฟ้าอากาศจากแผนที่อากาศ"


MAP_CASES = (
    ("บริเวณความกดอากาศสูงกำลังแรงจากประเทศจีนแผ่ลงมาปกคลุมประเทศไทยตอนบน", "อากาศเย็นลง ภาคเหนือและภาคอีสานมีอากาศหนาว ท้องฟ้าโปร่ง"),
    ("ร่องมรสุมพาดผ่านภาคเหนือและภาคอีสาน", "มีฝนตกเพิ่มขึ้นและอาจตกหนักบางแห่งในภาคเหนือและภาคอีสาน"),
    ("พายุดีเปรสชันเคลื่อนตัวจากทะเลจีนใต้เข้าสู่ภาคอีสานตอนกลาง", "มีฝนตกหนักถึงหนักมากในภาคอีสาน เสี่ยงน้ำท่วมฉับพลัน"),
    ("มรสุมตะวันตกเฉียงใต้กำลังแรงพัดปกคลุมทะเลอันดามันและประเทศไทย", "ฝั่งอันดามันมีฝนตกหนักและคลื่นลมแรง"),
    ("มรสุมตะวันออกเฉียงเหนือกำลังแรงพัดปกคลุมอ่าวไทยและภาคใต้", "ภาคใต้ฝั่งอ่าวไทยมีฝนตกหนัก อ่าวไทยมีคลื่นสูง"),
    ("บริเวณความกดอากาศต่ำเนื่องจากความร้อนปกคลุมประเทศไทยตอนบนในเดือนเมษายน", "อากาศร้อนถึงร้อนจัด อาจมีพายุฤดูร้อนบางพื้นที่"),
)


OUTLOOK_HINT = ("อ่านแผนที่อากาศ: ความกดอากาศสูงจากจีน = อากาศเย็นและแห้ง ร่องมรสุมหรือหย่อมความกดอากาศต่ำ = ฝนเพิ่มขึ้น "
                "พายุหมุนเขตร้อน = ฝนหนักและลมแรง มรสุมตะวันตกเฉียงใต้ = ฝนฝั่งอันดามัน มรสุมตะวันออกเฉียงเหนือ = ฝนภาคใต้ฝั่งอ่าวไทย "
                "แล้วนำคำพยากรณ์ไปวางแผนงานและการเดินทาง")


PLANS = (
    ("ชาวประมงพื้นบ้านในอ่าวไทย", "คลื่นสูง 2-3 เมตร และมีลมแรงในอ่าวไทย", "งดออกเรือจนกว่าคลื่นลมจะสงบ",
     ("ออกเรือไกลกว่าปกติเพื่อหาปลาให้ได้มาก", "ออกเรือตามปกติเพราะไม่เกี่ยวกับประมง", "นำเรือเล็กออกไปจอดกลางทะเล")),
    ("เกษตรกรที่กำลังจะตากข้าวเปลือก", "ฝนตกหนักติดต่อกันสามวัน", "เลื่อนการตากข้าวและเก็บผลผลิตไว้ในที่ร่ม",
     ("ตากข้าวกลางแจ้งตามแผนเดิมทั้งวัน", "รีบฉีดพ่นปุ๋ยทางใบทันทีก่อนฝนตก", "เปิดน้ำเข้านาเพิ่มก่อนฝนตก")),
    ("ผู้เลี้ยงสัตว์ในภาคเหนือ", "อุณหภูมิลดลง 5-7 °C และมีอากาศหนาวจัดบนยอดดอย", "จัดเตรียมที่กำบังลมและเพิ่มความอบอุ่นให้สัตว์",
     ("ย้ายสัตว์ขึ้นไปเลี้ยงบนยอดดอย", "งดให้อาหารสัตว์", "อาบน้ำให้สัตว์บ่อยขึ้น")),
    ("บริษัทนำเที่ยวที่จะพาลูกค้าไปดำน้ำฝั่งอันดามันเดือนสิงหาคม", "มรสุมตะวันตกเฉียงใต้กำลังแรง คลื่นสูงกว่า 3 เมตร", "เลื่อนหรือเปลี่ยนไปเที่ยวฝั่งอ่าวไทยแทน",
     ("ออกเรือตามกำหนดเพราะจองไว้แล้ว", "ย้ายไปดำน้ำไกลฝั่งยิ่งขึ้นเพื่อหนีคลื่น", "ให้ลูกค้าดำน้ำโดยไม่ใส่เสื้อชูชีพ")),
    ("ชาวบ้านริมลำน้ำในพื้นที่ที่พายุดีเปรสชันกำลังจะเคลื่อนผ่าน", "ฝนตกหนักถึงหนักมาก เสี่ยงน้ำป่าไหลหลาก", "ขนย้ายสิ่งของขึ้นที่สูงและติดตามประกาศเตือนภัย",
     ("ลงไปจับปลาในลำน้ำขณะน้ำหลากเพราะปลามาก", "ตั้งแคมป์ริมลำห้วยเพื่อดูน้ำหลาก", "ไม่ต้องทำอะไรเพราะฝนจะตกเพียงเล็กน้อย")),
    ("นักเรียนที่จะเดินทางไปเข้าค่ายบนภูเขาในเดือนมกราคม", "อากาศหนาวเย็นและมีหมอกหนาในตอนเช้า", "เตรียมเสื้อกันหนาวและระวังการขับขี่ในหมอก",
     ("เตรียมเพียงเสื้อแขนสั้นเพราะอากาศร้อน", "ขับรถเร็วขึ้นช่วงเช้าที่มีหมอก", "เตรียมร่มกันแดดเท่านั้น")),
    ("เกษตรกรที่ปลูกพืชในภาคอีสานช่วงเดือนเมษายน", "อากาศร้อนจัดและอาจมีพายุฤดูร้อน ลมกระโชกแรงและลูกเห็บ", "ค้ำยันต้นไม้และเสริมความแข็งแรงของโรงเรือน",
     ("รื้อหลังคาโรงเรือนออก", "เผาเศษวัชพืชกลางแจ้งตอนลมแรง", "เก็บเกี่ยวผลผลิตที่ยังไม่แก่เพื่อขายทันที")),
)


@question_type(
    "geo.weather_outlook_foundation",
    display_name={"th": "คาดการณ์ลมฟ้าอากาศจากลักษณะบนแผนที่อากาศ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_OUTLOOK,
)
class WeatherOutlookFoundation(QuestionType):
    """From a map feature over Thailand to the weather it brings."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        feature, weather = rng.choice(MAP_CASES)
        others = [c for c in MAP_CASES if c[0] != feature]
        picked = rng.sample(others, 3)
        if rng.random() < 0.6:
            return _labelled(stem=f"แผนที่อากาศแสดงว่า{feature} ควรคาดการณ์ลมฟ้าอากาศอย่างไร", correct=weather,
                             wrongs=tuple(p[1] for p in picked), topic=TOPIC_OUTLOOK, hint=OUTLOOK_HINT)
        return _labelled(stem=f"ถ้าคาดว่า{weather} แผนที่อากาศน่าจะแสดงลักษณะใด", correct=feature, wrongs=tuple(p[0] for p in picked),
                         topic=TOPIC_OUTLOOK, hint=OUTLOOK_HINT)


@question_type(
    "geo.weather_outlook_fluency",
    display_name={"th": "วางแผนการประกอบอาชีพและการดำเนินชีวิตตามคำพยากรณ์อากาศ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_OUTLOOK,
)
class WeatherOutlookFluency(QuestionType):
    """Choose the sensible plan for a job given the forecast."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.3:
            low = Fraction(rng.randint(30, 229), 10)
            while low in (Fraction(8), Fraction(16)):
                low += Fraction(1, 10)
            right = "หนาวจัด" if low < 8 else "หนาว" if low < 16 else "เย็น"
            return _labelled(stem=f"คำพยากรณ์ระบุว่าอุณหภูมิต่ำสุดบนยอดดอยเป็น {show(low)} °C ตามเกณฑ์กรมอุตุนิยมวิทยา "
                                  f"(เย็น 16.0-22.9 °C หนาว 8.0-15.9 °C หนาวจัดไม่เกิน 7.9 °C) อากาศเป็นแบบใด",
                             correct=right, wrongs=tuple(o for o in ("เย็น", "หนาว", "หนาวจัด", "ร้อน") if o != right),
                             topic=TOPIC_OUTLOOK, hint="เทียบอุณหภูมิต่ำสุดกับเกณฑ์ของกรมอุตุนิยมวิทยา")
        if roll < 0.55:
            wave = Fraction(rng.choice([n for n in range(2, 9) if n != 4]), 2)
            limit = 2
            unsafe = wave > limit
            right = "งดออกเรือจนกว่าคลื่นจะลดลง" if unsafe else "ออกเรือได้แต่ควรติดตามประกาศและระมัดระวัง"
            return _labelled(stem=f"คำพยากรณ์ระบุว่าทะเลมีคลื่นสูง {show(wave)} เมตร ถ้ามีคำแนะนำให้เรือเล็กงดออกจากฝั่งเมื่อคลื่นสูงเกิน {limit} เมตร "
                                  f"ชาวประมงเรือเล็กควรทำอย่างไร", correct=right,
                             wrongs=("ออกเรือได้แต่ควรติดตามประกาศและระมัดระวัง" if unsafe else "งดออกเรือจนกว่าคลื่นจะลดลง",
                                     "ออกเรือไปไกลกว่าปกติเพื่อหาปลาให้ได้มาก", "ออกเรือตอนกลางคืนแทนเพื่อหลบคลื่น"),
                             topic=TOPIC_OUTLOOK, hint="เทียบความสูงคลื่นที่พยากรณ์กับเกณฑ์ที่แนะนำ")
        who, forecast, right, wrongs = rng.choice(PLANS)
        return _labelled(stem=f"คำพยากรณ์อากาศแจ้งว่า{forecast} {who}ควรวางแผนอย่างไรเหมาะสมที่สุด", correct=right,
                         wrongs=tuple(wrongs), topic=TOPIC_OUTLOOK, hint=OUTLOOK_HINT)


@question_type(
    "geo.weather_outlook_application",
    display_name={"th": "คำนวณเวลาที่พายุมาถึง พื้นที่ฝนตก และแนวโน้มความกดอากาศ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_OUTLOOK,
)
class WeatherOutlookApplication(QuestionType):
    """Storm arrival, the share of an area with rain, and falling pressure."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.35:
            speed = rng.choice((10, 12, 15, 18, 20, 25, 30))
            hours = rng.randint(4, 48)
            storm = rng.choice(("พายุดีเปรสชัน", "พายุโซนร้อน", "พายุไต้ฝุ่น"))
            return numeric(stem=f"ศูนย์กลาง{storm}อยู่ห่างจากชายฝั่ง {show(speed * hours)} km และเคลื่อนเข้าหาฝั่งด้วยอัตราเร็ว {speed} km/h "
                                f"อีกกี่ชั่วโมงจะถึงชายฝั่ง", answer=hours,
                           wrongs=[hours * 2, hours + 12, Fraction(hours, 2) if hours % 2 == 0 else hours + 5], unit="ชั่วโมง", topic=TOPIC_OUTLOOK,
                           hint="เวลา = ระยะทาง ÷ อัตราเร็ว")
        if roll < 0.7:
            share = rng.choice((20, 30, 40, 60, 70, 80))
            units = rng.choice((10, 15, 20, 25, 30, 40, 50))
            while (share * units) % 100:
                units = rng.choice((10, 20, 30, 40, 50))
            place = rng.choice(("อำเภอ", "ตำบล"))
            return numeric(stem=f"กรมอุตุนิยมวิทยาพยากรณ์ว่ามีฝนตกร้อยละ {share} ของพื้นที่ จังหวัดหนึ่งมี {units} {place} "
                                f"คาดว่าจะมีฝนตกประมาณกี่{place}", answer=Fraction(share * units, 100),
                           wrongs=[units - Fraction(share * units, 100) or units // 2, share, Fraction(share * units, 100) + 2], unit=place,
                           topic=TOPIC_OUTLOOK, hint="ร้อยละของพื้นที่ที่มีฝน × จำนวนพื้นที่ทั้งหมด ÷ 100")
        start = rng.randrange(1000, 1013)
        hours = rng.choice((2, 3, 4, 6, 8, 12))
        rate = Fraction(rng.randint(1, 6), 2)
        drop = rate * hours
        if rng.random() < 0.5:
            return numeric(stem=f"ความกดอากาศที่สถานีหนึ่งลดลงจาก {start} hPa เป็น {show(start - drop)} hPa ในเวลา {hours} ชั่วโมง "
                                f"ความกดอากาศลดลงเฉลี่ยชั่วโมงละกี่ hPa", answer=rate,
                           wrongs=[drop, rate * 2, drop + hours], unit="hPa", topic=TOPIC_OUTLOOK, hint="อัตรา = ความกดอากาศที่ลดลง ÷ เวลา")
        return _labelled(stem=f"ความกดอากาศที่สถานีหนึ่งลดลงจาก {start} hPa เป็น {show(start - drop)} hPa ในเวลา {hours} ชั่วโมง "
                              f"และเมฆเพิ่มขึ้น ควรคาดการณ์อย่างไร", correct="มีโอกาสเกิดฝนหรือพายุเพราะบริเวณความกดอากาศต่ำกำลังเข้ามา",
                         wrongs=("อากาศจะแจ่มใสเพราะความกดอากาศสูงกำลังเข้ามา", "อากาศจะหนาวจัดและแห้งทันที", "ไม่มีการเปลี่ยนแปลงลมฟ้าอากาศ"),
                         topic=TOPIC_OUTLOOK, hint="ความกดอากาศลดลงต่อเนื่องร่วมกับเมฆเพิ่มขึ้น แสดงว่าความกดอากาศต่ำหรือพายุกำลังเข้ามา")
