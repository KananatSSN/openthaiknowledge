"""มาตราส่วน ทิศ และสัญลักษณ์

ภูมิศาสตร์ · ม.2 · สสวท. พื้นฐาน
Indicators: ส 5.1 ม.2/2
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.kit.classify import Category, ClassifyType
from otk.sets._support.geography import (
    DIRECTIONS, M2, SUBJECT, choices, mirrored, number, stage, turned,
)

PROVENANCE = Provenance("original")


TOPIC = "มาตราส่วน ทิศ และสัญลักษณ์"

SCALES = (25_000, 50_000, 100_000, 200_000, 250_000, 500_000, 1_000_000)
CM_PER_KM = 100_000
SCALE_HINT = "มาตราส่วน 1 : N หมายถึง 1 เซนติเมตรบนแผนที่เท่ากับ N เซนติเมตรบนพื้นที่จริง และ 1 กิโลเมตร = 100,000 เซนติเมตร"


def ratio(n) -> str:
    return f"1 : {number(n)}"


def _exact(x: Fraction) -> bool:
    return (x * 100).denominator == 1


def _map_and_ground(rng: Random) -> tuple[Fraction, int, Fraction]:
    """A map distance (cm), a scale and the ground distance (km), all exact to 2 places."""
    while True:
        scale = rng.choice(SCALES)
        cm = Fraction(rng.randint(2, 24), 2)
        km = cm * scale / CM_PER_KM
        if _exact(km) and _exact(km * 10) and _exact(km / 10):
            return cm, scale, km


@question_type(
    "geog.map_to_ground_m2",
    display_name={"th": "ใช้มาตราส่วนหาระยะทางจริงจากระยะบนแผนที่"},
    level=M2, subject=SUBJECT, topic=TOPIC,
)
@stage(1)
class MapToGround(QuestionType):
    def build(self, rng: Random, **params):
        cm, scale, km = _map_and_ground(rng)
        return choices(
            stem=(f"แผนที่มาตราส่วน {ratio(scale)} ระยะระหว่างสองจุดบนแผนที่วัดได้ {number(cm)} เซนติเมตร "
                  "ระยะทางจริงเป็นกี่กิโลเมตร"),
            correct=f"{number(km)} กิโลเมตร",
            wrongs=[("units.wrong_conversion", f"{number(km * 10)} กิโลเมตร"),
                    ("units.wrong_conversion", f"{number(km / 10)} กิโลเมตร"),
                    f"{number(km * 2)} กิโลเมตร", f"{number(km + 1)} กิโลเมตร"],
            hint=SCALE_HINT, topic=TOPIC)


@question_type(
    "geog.ground_to_map_m2",
    display_name={"th": "ใช้มาตราส่วนหาระยะบนแผนที่จากระยะทางจริง"},
    level=M2, subject=SUBJECT, topic=TOPIC,
)
@stage(2)
class GroundToMap(QuestionType):
    def build(self, rng: Random, **params):
        cm, scale, km = _map_and_ground(rng)
        return choices(
            stem=(f"สองหมู่บ้านอยู่ห่างกันจริง {number(km)} กิโลเมตร ถ้าเขียนลงในแผนที่มาตราส่วน "
                  f"{ratio(scale)} จะห่างกันกี่เซนติเมตรบนแผนที่"),
            correct=f"{number(cm)} เซนติเมตร",
            wrongs=[("units.wrong_conversion", f"{number(cm * 10)} เซนติเมตร"),
                    ("units.wrong_conversion", f"{number(cm / 10)} เซนติเมตร"),
                    f"{number(cm * 2)} เซนติเมตร", f"{number(cm + 1)} เซนติเมตร"],
            hint=SCALE_HINT, topic=TOPIC)


@question_type(
    "geog.find_scale_m2",
    display_name={"th": "หามาตราส่วนจากระยะบนแผนที่และระยะทางจริง"},
    level=M2, subject=SUBJECT, topic=TOPIC,
)
@stage(3)
class FindScale(QuestionType):
    def build(self, rng: Random, **params):
        cm, scale, km = _map_and_ground(rng)
        return choices(
            stem=(f"ระยะทางจริงระหว่างสองเมือง {number(km)} กิโลเมตร บนแผนที่วัดได้ {number(cm)} เซนติเมตร "
                  "แผนที่นี้มีมาตราส่วนเท่าใด"),
            correct=ratio(scale),
            wrongs=[("units.wrong_conversion", ratio(scale // 10)),
                    ("units.wrong_conversion", ratio(scale * 10)),
                    # Converted km to m only, not to cm.
                    ("units.not_converted", ratio(scale // 100)),
                    ratio(scale * 2)],
            hint="แปลงระยะทางจริงเป็นเซนติเมตรก่อน แล้วหารด้วยระยะบนแผนที่ จะได้ N ใน 1 : N",
            topic=TOPIC)


@question_type(
    "geog.scale_detail_m2",
    display_name={"th": "เปรียบเทียบมาตราส่วนใหญ่และมาตราส่วนเล็ก"},
    level=M2, subject=SUBJECT, topic=TOPIC,
)
@stage(2)
class ScaleDetail(QuestionType):
    def build(self, rng: Random, **params):
        four = rng.sample(SCALES, 4)
        detail = rng.random() < 0.5
        correct = min(four) if detail else max(four)
        other = max(four) if detail else min(four)
        ask = ("แสดงรายละเอียดของพื้นที่ได้มากที่สุด" if detail
               else "แสดงพื้นที่ได้กว้างที่สุด")
        return choices(
            stem=f"แผนที่ขนาดกระดาษเท่ากัน 4 ฉบับมีมาตราส่วนต่างกัน แผนที่มาตราส่วนใด{ask}",
            correct=ratio(correct),
            wrongs=[ratio(other), *(ratio(s) for s in four if s not in (correct, other))],
            hint="ตัวเลขหลัง 1 : ยิ่งน้อย มาตราส่วนยิ่งใหญ่ แสดงพื้นที่แคบแต่มีรายละเอียดมาก",
            topic=TOPIC)


AZIMUTH_HINT = "มุมอะซิมุทวัดจากทิศเหนือตามเข็มนาฬิกา: ทิศเหนือ 0 องศา ทิศตะวันออก 90 ทิศใต้ 180 ทิศตะวันตก 270"


def degrees(n: int) -> str:
    return f"{n % 360} องศา"


@question_type(
    "geog.azimuth_m2",
    display_name={"th": "บอกค่ามุมอะซิมุทของทิศหลักและทิศรอง"},
    level=M2, subject=SUBJECT, topic=TOPIC,
)
@stage(1)
class Azimuth(QuestionType):
    def build(self, rng: Random, **params):
        i = rng.randrange(8)
        way = DIRECTIONS[i]
        if rng.random() < 0.5:
            mirror = DIRECTIONS.index(mirrored(way))
            return choices(
                stem=f"{way}มีมุมอะซิมุทกี่องศา",
                correct=degrees(45 * i),
                wrongs=[("direction.left_right_swapped", degrees(45 * mirror)),
                        ("direction.opposite", degrees(45 * i + 180)),
                        degrees(45 * i + 45), degrees(45 * i - 45), degrees(45 * i + 90)],
                hint=AZIMUTH_HINT, topic=TOPIC)
        return choices(
            stem=f"มุมอะซิมุท {degrees(45 * i)} ชี้ไปทางทิศใด",
            correct=way,
            wrongs=[("direction.left_right_swapped", mirrored(way)),
                    ("direction.opposite", turned(way, 4)),
                    turned(way, 1), turned(way, -1), turned(way, 2)],
            hint=AZIMUTH_HINT, topic=TOPIC)


@question_type(
    "geog.back_azimuth_m2",
    display_name={"th": "หามุมอะซิมุทย้อนกลับ"},
    level=M2, subject=SUBJECT, topic=TOPIC,
)
@stage(3)
class BackAzimuth(QuestionType):
    def build(self, rng: Random, **params):
        angle = rng.choice([a for a in range(5, 360, 5) if a % 90])
        return choices(
            stem=(f"จากจุด ก มองไปยังจุด ข ได้มุมอะซิมุท {degrees(angle)} "
                  "ถ้ายืนที่จุด ข แล้วมองกลับไปยังจุด ก จะได้มุมอะซิมุทเท่าใด"),
            correct=degrees(angle + 180),
            wrongs=[("direction.opposite", degrees(angle)),
                    degrees(360 - angle), degrees(angle + 90), degrees(angle + 270)],
            hint="มุมอะซิมุทย้อนกลับต่างจากมุมเดิม 180 องศา ถ้ามุมเดิมน้อยกว่า 180 ให้บวก 180 ถ้ามากกว่าให้ลบ 180",
            topic=TOPIC)


@question_type(
    "geog.map_symbol_m2",
    display_name={"th": "จำแนกสัญลักษณ์บนแผนที่แบบจุด เส้น และพื้นที่"},
    level=M2, subject=SUBJECT, topic=TOPIC,
)
@stage(2)
class MapSymbol(ClassifyType):
    ASKS = ("pick",)           # three groups: a classify question would offer three choices
    PICK_STEM = "บนแผนที่ ข้อใดมักแสดงด้วย{category}"
    CATEGORIES = [
        Category("สัญลักษณ์แบบจุด", ("ที่ตั้งโรงเรียน", "ที่ตั้งวัด", "ที่ตั้งสถานีตำรวจ",
                                     "ที่ตั้งโรงพยาบาล", "ที่ตั้งเมืองหลวง")),
        Category("สัญลักษณ์แบบเส้น", ("ถนน", "ทางรถไฟ", "เส้นแบ่งเขตจังหวัด",
                                      "เส้นชั้นความสูง", "คลองส่งน้ำ")),
        Category("สัญลักษณ์แบบพื้นที่", ("บริเวณป่าไม้", "บริเวณนาข้าว", "บริเวณเขตชุมชน",
                                         "บริเวณทะเลสาบ", "บริเวณสวนยางพารา")),
    ]
