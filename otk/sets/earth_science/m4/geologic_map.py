"""แผนที่ภูมิประเทศและแผนที่ธรณีวิทยา

ธรณีวิทยา · ม.4 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/12

Sets moved here from: science_wave_f77.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f77 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_MAP = "แผนที่ภูมิประเทศและแผนที่ธรณีวิทยา"


MAP_FACTS = (
    ("เส้นชั้นความสูงที่อยู่ชิดกันมากบอกอะไร", "พื้นที่บริเวณนั้นลาดชันมาก", ("พื้นที่บริเวณนั้นราบเรียบมาก", "มีแม่น้ำไหลผ่านเสมอ", "บริเวณนั้นเป็นทะเลลึก", "ความสูงลดลงครึ่งหนึ่ง")),
    ("เส้นชั้นความสูงที่เป็นวงปิดซ้อนกันโดยค่าสูงขึ้นเข้าหาตรงกลางแสดงลักษณะใด", "ยอดเขาหรือเนินเขา",
     ("แอ่งหรือหลุม", "แม่น้ำหรือลำธาร", "หน้าผาริมทะเล", "ที่ราบลุ่มน้ำท่วมถึง")),
    ("เมื่อเส้นชั้นความสูงตัดผ่านลำน้ำ จะหักเป็นรูปตัว V ชี้ไปทางใด", "ทางต้นน้ำ", ("ทางปลายน้ำ", "ทางทิศเหนือเสมอ", "ทางทิศตะวันออกเสมอ", "ไม่หักเลย")),
    ("แผนที่ธรณีวิทยาแสดงข้อมูลใดเป็นหลัก", "ชนิดและอายุของหิน แนวการวางตัวของชั้นหิน และรอยเลื่อน",
     ("ถนนและชุมชนเท่านั้น", "ปริมาณน้ำฝนรายเดือน", "อุณหภูมิอากาศเฉลี่ย ความชื้น และปริมาณน้ำฝนรายเดือน", "ถนน ชุมชน และแนวสายไฟฟ้าแรงสูงในพื้นที่")),
    ("แผนที่ธรณีวิทยาใช้ประโยชน์ด้านใด", "หาแหล่งแร่และน้ำบาดาล และประเมินพื้นที่เสี่ยงดินถล่มหรือรอยเลื่อน",
     ("พยากรณ์อากาศรายวัน", "นำทางในเมืองและบอกตำแหน่งของชุมชนและถนนสายหลักในพื้นที่", "พยากรณ์อากาศรายวัน และวัดปริมาณน้ำฝนที่ตกในแต่ละพื้นที่", "วางแผนตารางเรียน")),
)


MAP_HINT = ("เส้นชั้นความสูงเชื่อมจุดที่สูงเท่ากัน ชิดกันแสดงความลาดชัน ระยะจริง = ระยะในแผนที่ × มาตราส่วน "
            "ความชัน = ผลต่างความสูง ÷ ระยะทางราบ แผนที่ธรณีวิทยาแสดงชนิดหิน อายุ และโครงสร้าง")


@question_type(
    "geo.geologic_map_foundation",
    display_name={"th": "อ่านสัญลักษณ์บนแผนที่ภูมิประเทศและแผนที่ธรณีวิทยา"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MAP,
)
class GeologicMapFoundation(QuestionType):
    """Contours, valleys, hills, and what a geological map shows."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(MAP_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_MAP, hint=MAP_HINT)


@question_type(
    "geo.geologic_map_fluency",
    display_name={"th": "คำนวณระยะจริงจากมาตราส่วนแผนที่"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MAP,
)
class GeologicMapFluency(QuestionType):
    """Map distance × scale, in kilometres."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        scale = rng.choice((10000, 25000, 50000, 100000, 250000))
        cm = Fraction(rng.randrange(5, 201), 10)
        km = cm * scale / 100000
        if (km * 100).denominator != 1:
            cm = Fraction(rng.randrange(1, 21))
            km = cm * scale / 100000
        if rng.random() < 0.6:
            return numeric(stem=f"แผนที่มาตราส่วน 1 : {scale:,} วัดระยะระหว่างสองจุดได้ {show(cm)} cm ระยะจริงเป็นกี่กิโลเมตร", answer=km,
                           wrongs=[km * 10, km / 10, cm * scale / 100], unit="km", topic=TOPIC_MAP,
                           hint="ระยะจริง (cm) = ระยะในแผนที่ × มาตราส่วน แล้วหารด้วย 100,000 เพื่อเป็นกิโลเมตร")
        return numeric(stem=f"สองหมู่บ้านห่างกันจริง {show(km)} km บนแผนที่มาตราส่วน 1 : {scale:,} จะห่างกันกี่เซนติเมตร", answer=cm,
                       wrongs=[cm * 10, cm / 10, km * 100], unit="cm", topic=TOPIC_MAP, hint="ระยะในแผนที่ = ระยะจริง (cm) ÷ มาตราส่วน")


@question_type(
    "geo.geologic_map_application",
    display_name={"th": "คำนวณความสูงและความลาดชันจากเส้นชั้นความสูง"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MAP,
)
class GeologicMapApplication(QuestionType):
    """Count contour gaps for height; rise ÷ run for slope."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        interval = rng.choice((10, 20, 25, 50, 100))
        if rng.random() < 0.5:
            base = rng.randrange(0, 501, interval)
            gaps = rng.randint(2, 12)
            top = base + interval * gaps
            return numeric(stem=f"แผนที่มีช่วงชั้นความสูง {interval} m จุด ก อยู่บนเส้น {base} m จุด ข อยู่สูงกว่าจุด ก ไป {gaps} เส้น "
                                f"จุด ข สูงจากระดับทะเลปานกลางกี่เมตร", answer=top, wrongs=[base + gaps, interval * gaps, top + interval], unit="m",
                           topic=TOPIC_MAP, hint="ความสูง = ความสูงเริ่มต้น + จำนวนช่วง × ช่วงชั้นความสูง")
        rise = interval * rng.randint(2, 10)
        run = rng.choice((100, 200, 250, 400, 500, 1000, 2000))
        slope = Fraction(rise * 100, run)
        return numeric(stem=f"ระหว่างสองจุดที่ห่างกันในแนวราบ {run:,} m มีความสูงต่างกัน {rise} m ความลาดชันเฉลี่ยเป็นร้อยละเท่าใด",
                       answer=slope, wrongs=[Fraction(run, rise) if (Fraction(run, rise) * 100).denominator == 1 else slope * 2, slope / 10, rise], unit="%",
                       topic=TOPIC_MAP, hint="ความลาดชัน (%) = ผลต่างความสูง ÷ ระยะทางราบ × 100")
