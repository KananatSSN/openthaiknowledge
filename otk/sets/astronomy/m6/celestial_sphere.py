"""ทรงกลมฟ้าและระบบพิกัดของดาว

ดาราศาสตร์ · ม.6 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/13

Sets moved here from: science_wave_f85.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f85 import SUBJECT, TOWNS, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_SPHERE = "ทรงกลมฟ้าและระบบพิกัดของดาว"


DIRS = ((0, "ทิศเหนือ"), (45, "ทิศตะวันออกเฉียงเหนือ"), (90, "ทิศตะวันออก"), (135, "ทิศตะวันออกเฉียงใต้"), (180, "ทิศใต้"),
        (225, "ทิศตะวันตกเฉียงใต้"), (270, "ทิศตะวันตก"), (315, "ทิศตะวันตกเฉียงเหนือ"))


SPHERE_POINTS = (
    ("จุดจอมฟ้า (ซีนิท)", "จุดบนทรงกลมฟ้าที่อยู่เหนือศีรษะผู้สังเกตพอดี"),
    ("จุดเนเดอร์", "จุดบนทรงกลมฟ้าที่อยู่ใต้เท้าผู้สังเกต ตรงข้ามกับจุดจอมฟ้า"),
    ("เส้นขอบฟ้า", "วงกลมที่แบ่งทรงกลมฟ้าเป็นครึ่งที่มองเห็นและมองไม่เห็น ห่างจุดจอมฟ้า 90 องศา"),
    ("เส้นเมริเดียนท้องถิ่น", "เส้นที่ลากจากจุดทิศเหนือผ่านจุดจอมฟ้าไปยังจุดทิศใต้บนขอบฟ้า"),
    ("ขั้วฟ้าเหนือ", "จุดที่แกนหมุนของโลกต่อออกไปทางเหนือตัดทรงกลมฟ้า"),
    ("เส้นศูนย์สูตรฟ้า", "วงกลมที่ได้จากการขยายระนาบเส้นศูนย์สูตรโลกออกไปตัดทรงกลมฟ้า"),
    ("เส้นสุริยวิถี", "เส้นทางที่ดวงอาทิตย์ปรากฏเคลื่อนที่บนทรงกลมฟ้าในรอบหนึ่งปี"),
)


SPHERE_HINT = ("ระบบขอบฟ้าใช้มุมเงย (0-90° จากขอบฟ้า) และมุมทิศ (0° ทิศเหนือ วนผ่านทิศตะวันออก 90° ทิศใต้ 180° ทิศตะวันตก 270°) "
               "ระบบศูนย์สูตรใช้ไรต์แอสเซนชัน (0-24 ชั่วโมง, 1 ชั่วโมง = 15°) และเดคลิเนชัน (-90° ถึง +90° จากศูนย์สูตรฟ้า) "
               "มุมเงยของขั้วฟ้าเหนือเท่ากับละติจูดของผู้สังเกต")


@question_type(
    "astro.celestial_sphere_foundation",
    display_name={"th": "จุดและเส้นสำคัญบนทรงกลมฟ้า"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_SPHERE,
)
class CelestialSphereFoundation(QuestionType):
    """Zenith, nadir, horizon, meridian, poles, celestial equator, ecliptic; the two systems."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            facts = (("ระบบพิกัดขอบฟ้าใช้ค่าใดระบุตำแหน่งดาว", "มุมทิศและมุมเงย",
                      ("ไรต์แอสเซนชันและเดคลิเนชัน", "ละติจูดและลองจิจูดของผู้สังเกต", "โชติมาตรและสี", "ระยะทางและมวล")),
                     ("ระบบพิกัดศูนย์สูตรใช้ค่าใดระบุตำแหน่งดาว", "ไรต์แอสเซนชันและเดคลิเนชัน",
                      ("มุมทิศและมุมเงย", "ละติจูดและลองจิจูดของผู้สังเกต", "โชติมาตรและสี", "ระยะทางและมวล")),
                     ("เหตุใดพิกัดศูนย์สูตรของดาวฤกษ์จึงเหมาะใช้ทำแผนที่ดาว", "ค่าแทบไม่เปลี่ยนตามเวลาและตำแหน่งผู้สังเกต",
                      ("ค่าเปลี่ยนทุกนาทีตามการหมุนของโลก", "ใช้ได้เฉพาะที่ขั้วโลก", "ใช้ได้เฉพาะกับดวงอาทิตย์", "ไม่ต้องทราบตำแหน่งดาวเลย")),
                     ("เหตุใดพิกัดขอบฟ้าของดาวดวงเดียวกันจึงต่างกันเมื่อดูจากต่างสถานที่หรือต่างเวลา", "ระบบขอบฟ้าอ้างอิงขอบฟ้าและทิศของผู้สังเกตแต่ละคน",
                      ("ดาวเปลี่ยนตำแหน่งในอวกาศทุกชั่วโมง", "ดาวอยู่ใกล้โลกมาก", "ทรงกลมฟ้ามีหลายชั้น", "โลกหยุดหมุนในเวลากลางคืน")))
            stem, right, wrongs = rng.choice(facts)
            return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_SPHERE, hint=SPHERE_HINT)
        name, what = rng.choice(SPHERE_POINTS)
        picked = rng.sample([p for p in SPHERE_POINTS if p[0] != name], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"บนแบบจำลองทรงกลมฟ้า {name} คืออะไร", correct=what, wrongs=tuple(p[1] for p in picked),
                             topic=TOPIC_SPHERE, hint=SPHERE_HINT)
        return _labelled(stem=f"บนแบบจำลองทรงกลมฟ้า ข้อใดคือ{what}", correct=name, wrongs=tuple(p[0] for p in picked),
                         topic=TOPIC_SPHERE, hint=SPHERE_HINT)


@question_type(
    "astro.celestial_sphere_fluency",
    display_name={"th": "อ่านมุมทิศ มุมเงย และมุมเงยของขั้วฟ้า"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_SPHERE,
)
class CelestialSphereFluency(QuestionType):
    """Azimuth to direction and back; pole altitude equals latitude; zenith distance."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.35:
            az, name = rng.choice(DIRS)
            others = [d for d in DIRS if d[0] != az]
            picked = rng.sample(others, 3)
            if rng.random() < 0.5:
                return _labelled(stem=f"ดาวดวงหนึ่งมีมุมทิศ {az}° (วัดจากทิศเหนือวนไปทางทิศตะวันออก) ดาวอยู่ทางทิศใด", correct=name,
                                 wrongs=tuple(p[1] for p in picked), topic=TOPIC_SPHERE, hint=SPHERE_HINT)
            return _labelled(stem=f"ดาวที่อยู่ทาง{name}มีมุมทิศเท่าใด (วัดจากทิศเหนือวนไปทางทิศตะวันออก)", correct=f"{az}°",
                             wrongs=tuple(f"{p[0]}°" for p in picked), topic=TOPIC_SPHERE, hint=SPHERE_HINT)
        town, lat = rng.choice(TOWNS)
        if roll < 0.7:
            return numeric(stem=f"ผู้สังเกตที่{town} (ละติจูดประมาณ {lat}° เหนือ) จะเห็นขั้วฟ้าเหนือ (ใกล้ดาวเหนือ) มีมุมเงยประมาณกี่องศา",
                           answer=lat, wrongs=[90 - lat, lat + 10, 90], unit="องศา", topic=TOPIC_SPHERE, hint="มุมเงยของขั้วฟ้าเหนือ = ละติจูดของผู้สังเกต")
        alt = rng.randint(5, 85)
        return numeric(stem=f"ดาวดวงหนึ่งมีมุมเงย {alt}° ดาวอยู่ห่างจากจุดจอมฟ้ากี่องศา", answer=90 - alt,
                       wrongs=[alt, 180 - alt, 90 - alt + 10], unit="องศา", topic=TOPIC_SPHERE, hint="ระยะห่างจากจุดจอมฟ้า = 90° − มุมเงย")


@question_type(
    "astro.celestial_sphere_application",
    display_name={"th": "คำนวณมุมเงยสูงสุดของดาวและแปลงไรต์แอสเซนชัน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_SPHERE,
)
class CelestialSphereApplication(QuestionType):
    """Meridian altitude 90 − |φ − δ|; zenith star has δ = φ; hours × 15°."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        town, lat = rng.choice(TOWNS)
        if roll < 0.45:
            dec = rng.choice([d for d in range(-60, 71) if d != lat])
            return numeric(stem=f"ผู้สังเกตที่{town} (ละติจูดประมาณ {lat}° เหนือ) ดาวดวงหนึ่งมีเดคลิเนชัน {dec:+d}° "
                                f"เมื่อดาวผ่านเส้นเมริเดียน จะมีมุมเงยกี่องศา", answer=90 - abs(lat - dec),
                           wrongs=[abs(lat - dec), 90 - lat, 90 - abs(dec)], unit="องศา", topic=TOPIC_SPHERE,
                           hint="มุมเงยขณะผ่านเมริเดียน = 90° − |ละติจูด − เดคลิเนชัน|")
        if roll < 0.7:
            return numeric(stem=f"ดาวที่ผ่านจุดจอมฟ้าของผู้สังเกตที่{town} (ละติจูดประมาณ {lat}° เหนือ) มีเดคลิเนชันกี่องศา", answer=lat,
                           wrongs=[90 - lat, 90, lat + 10], unit="องศา", topic=TOPIC_SPHERE, hint="ดาวผ่านจุดจอมฟ้าเมื่อเดคลิเนชันเท่ากับละติจูด")
        hours = rng.randint(1, 23)
        if rng.random() < 0.5:
            return numeric(stem=f"ดาวดวงหนึ่งมีไรต์แอสเซนชัน {hours} ชั่วโมง คิดเป็นมุมกี่องศา", answer=hours * 15,
                           wrongs=[hours * 60, hours * 24, hours + 15], unit="องศา", topic=TOPIC_SPHERE, hint="1 ชั่วโมง = 15°")
        return numeric(stem=f"ดาวดวงหนึ่งมีไรต์แอสเซนชัน {hours * 15}° คิดเป็นกี่ชั่วโมง", answer=hours,
                       wrongs=[hours * 15, Fraction(hours * 15, 24) if (Fraction(hours * 15, 24) * 100).denominator == 1 else hours + 12, hours * 4],
                       unit="ชั่วโมง", topic=TOPIC_SPHERE, hint="1 ชั่วโมง = 15°")
