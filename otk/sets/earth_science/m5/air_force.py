"""แรงที่มีผลต่อการหมุนเวียนของอากาศ

ธรณีวิทยา · ม.5 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/3

Sets moved here from: science_wave_f78.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f78 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_FORCE = "แรงที่มีผลต่อการหมุนเวียนของอากาศ"


FORCES = (
    ("แรงเนื่องจากความแตกต่างของความกดอากาศ", "ผลักอากาศจากบริเวณความกดอากาศสูงไปต่ำ ยิ่งไอโซบาร์ชิดกันยิ่งแรง"),
    ("แรงคอริออลิส", "ทำให้อากาศที่เคลื่อนที่เบนไปทางขวาในซีกโลกเหนือและทางซ้ายในซีกโลกใต้"),
    ("แรงสู่ศูนย์กลาง", "ทำให้อากาศเคลื่อนที่เป็นแนวโค้งรอบศูนย์กลางความกดอากาศ"),
    ("แรงเสียดทาน", "ทำให้ลมใกล้ผิวโลกช้าลงและพัดตัดไอโซบาร์เข้าหาความกดอากาศต่ำ"),
)


FORCE_HINT = ("อากาศเคลื่อนจากความกดสูงไปต่ำ แรงคอริออลิสเบนขวาในซีกโลกเหนือ เป็นศูนย์ที่เส้นศูนย์สูตร แรงเสียดทานทำให้ลมผิวพื้นช้าลง "
              "ซีกโลกเหนือลมพัดทวนเข็มนาฬิกาเข้าหาความกดต่ำ และตามเข็มนาฬิกาออกจากความกดสูง")


@question_type(
    "geo.air_force_foundation",
    display_name={"th": "แรงที่กระทำต่ออากาศที่เคลื่อนที่"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_FORCE,
)
class AirForceFoundation(QuestionType):
    """Each force and what it does."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, effect = rng.choice(FORCES)
        others = [f for f in FORCES if f[0] != name]
        if rng.random() < 0.3:
            facts = (("แรงคอริออลิสมีค่าเป็นศูนย์ที่ใด", "ที่เส้นศูนย์สูตร", ("ที่ขั้วโลก", "ที่ละติจูด 45 องศา", "ทุกที่เท่ากัน", "ที่ละติจูด 60 องศา")),
                     ("ลมที่พัดขนานกับไอโซบาร์ในบรรยากาศชั้นบนเกิดจากสมดุลของแรงใด", "แรงเนื่องจากความแตกต่างของความกดอากาศกับแรงคอริออลิส",
                      ("แรงเสียดทานกับแรงโน้มถ่วง", "แรงสู่ศูนย์กลางเท่านั้น", "แรงเสียดทานเพียงอย่างเดียว", "แรงลอยตัวกับแรงโน้มถ่วง")))
            stem, right, wrongs = rng.choice(facts)
            return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_FORCE, hint=FORCE_HINT)
        if rng.random() < 0.5:
            pool = [f[1] for f in others] + ["ทำให้อากาศเคลื่อนที่จากความกดต่ำไปสูง", "ทำให้ลมหยุดนิ่งเหนือมหาสมุทร"]
            return _labelled(stem=f"{name}มีผลต่อการเคลื่อนที่ของอากาศอย่างไร", correct=effect, wrongs=tuple(pool), topic=TOPIC_FORCE,
                             hint=FORCE_HINT)
        pool = [f[0] for f in others] + ["แรงลอยตัว", "แรงแม่เหล็กโลก"]
        return _labelled(stem=f"แรงใด{effect}", correct=name, wrongs=tuple(pool), topic=TOPIC_FORCE, hint=FORCE_HINT)


@question_type(
    "geo.air_force_fluency",
    display_name={"th": "ทิศทางลมรอบศูนย์กลางความกดอากาศในแต่ละซีกโลก"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_FORCE,
)
class AirForceFluency(QuestionType):
    """In or out, clockwise or not, by hemisphere and centre."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.25:
            a, b = rng.sample(range(0, 81, 5), 2)
            places = {a: "สถานี ก", b: "สถานี ข"}
            bigger = places[max(a, b)]
            return _labelled(stem=f"ลมพัดด้วยอัตราเร็วเท่ากันที่สถานี ก ละติจูด {a} องศา และสถานี ข ละติจูด {b} องศา แรงคอริออลิสที่สถานีใดมากกว่า",
                             correct=bigger, wrongs=("สถานี ข" if bigger == "สถานี ก" else "สถานี ก", "เท่ากันทั้งสองสถานี", "เป็นศูนย์ทั้งสองสถานี"),
                             topic=TOPIC_FORCE, hint=FORCE_HINT + " แรงคอริออลิสเพิ่มขึ้นตามละติจูดและอัตราเร็วลม")
        if rng.random() < 0.45:
            north = rng.random() < 0.5
            heading = rng.choice(("ทิศเหนือ", "ทิศใต้", "ทิศตะวันออก", "ทิศตะวันตก"))
            right_of = {"ทิศเหนือ": "ทิศตะวันออก", "ทิศใต้": "ทิศตะวันตก", "ทิศตะวันออก": "ทิศใต้", "ทิศตะวันตก": "ทิศเหนือ"}
            left_of = {v: k for k, v in right_of.items()}
            answer = right_of[heading] if north else left_of[heading]
            return _labelled(stem=f"มวลอากาศในซีกโลก{'เหนือ' if north else 'ใต้'}เคลื่อนที่ไปทาง{heading} แรงคอริออลิสทำให้เบนไปทางใด",
                             correct=answer, wrongs=tuple(d for d in ("ทิศเหนือ", "ทิศใต้", "ทิศตะวันออก", "ทิศตะวันตก") if d != answer),
                             topic=TOPIC_FORCE, hint=FORCE_HINT)
        north = rng.random() < 0.5
        low = rng.random() < 0.5
        inward = "พัดเข้าหาศูนย์กลาง" if low else "พัดออกจากศูนย์กลาง"
        clockwise = (north and not low) or (not north and low)
        right = f"{inward} หมุน{'ตามเข็มนาฬิกา' if clockwise else 'ทวนเข็มนาฬิกา'}"
        options = [f"{a} หมุน{b}" for a in ("พัดเข้าหาศูนย์กลาง", "พัดออกจากศูนย์กลาง") for b in ("ตามเข็มนาฬิกา", "ทวนเข็มนาฬิกา")]
        places = {(True, True): ("พายุไต้ฝุ่นเหนือทะเลจีนใต้", "พายุเฮอริเคนในทะเลแคริบเบียน", "พายุไซโคลนในอ่าวเบงกอล"),
                  (False, True): ("พายุไซโคลนนอกชายฝั่งออสเตรเลีย", "พายุหมุนเขตร้อนใกล้เกาะมาดากัสการ์"),
                  (True, False): ("บริเวณความกดอากาศสูงเหนือไซบีเรียในฤดูหนาว", "บริเวณความกดอากาศสูงเหนือมหาสมุทรแปซิฟิกเหนือ"),
                  (False, False): ("บริเวณความกดอากาศสูงเหนือมหาสมุทรอินเดียตอนใต้", "บริเวณความกดอากาศสูงเหนือทวีปออสเตรเลียในฤดูหนาว")}
        where = rng.choice(places[(north, low)] + (f"ศูนย์กลางความกดอากาศ{'ต่ำ' if low else 'สูง'}ในซีกโลก{'เหนือ' if north else 'ใต้'}",))
        return _labelled(stem=f"ลมผิวพื้นรอบ{where}มีลักษณะอย่างไร",
                         correct=right, wrongs=tuple(o for o in options if o != right), topic=TOPIC_FORCE, hint=FORCE_HINT)


@question_type(
    "geo.air_force_application",
    display_name={"th": "คำนวณความชันของความกดอากาศ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_FORCE,
)
class AirForceApplication(QuestionType):
    """Pressure difference per 100 km: the steeper, the stronger the wind."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        diff = rng.randrange(4, 41, 2)
        distance = rng.choice((100, 200, 250, 400, 500, 800, 1000))
        grad = Fraction(diff * 100, distance)
        if (grad * 100).denominator != 1:
            distance = 200
            grad = Fraction(diff * 100, distance)
        if rng.random() < 0.6:
            return numeric(stem=f"ความกดอากาศที่สองสถานีต่างกัน {diff} hPa และอยู่ห่างกัน {distance} km ความชันของความกดอากาศเป็นกี่ hPa ต่อ 100 km",
                           answer=grad, wrongs=[Fraction(diff, distance) if (Fraction(diff, distance) * 100).denominator == 1 else grad * 2, diff, grad * 10],
                           unit="hPa ต่อ 100 km", topic=TOPIC_FORCE, hint="ความชัน = ผลต่างความกดอากาศ ÷ ระยะทาง × 100")
        a = (rng.randrange(4, 21, 2), rng.choice((100, 200, 400)))
        b = (rng.randrange(4, 21, 2), rng.choice((100, 200, 400)))
        while Fraction(a[0], a[1]) == Fraction(b[0], b[1]):
            b = (b[0] + 2, b[1])
        stronger = "บริเวณ ก" if Fraction(a[0], a[1]) > Fraction(b[0], b[1]) else "บริเวณ ข"
        return _labelled(stem=f"บริเวณ ก ความกดอากาศต่างกัน {a[0]} hPa ในระยะ {a[1]} km บริเวณ ข ต่างกัน {b[0]} hPa ในระยะ {b[1]} km "
                              f"บริเวณใดน่าจะมีลมแรงกว่า", correct=stronger,
                         wrongs=("บริเวณ ข" if stronger == "บริเวณ ก" else "บริเวณ ก", "ลมแรงเท่ากัน", "ไม่มีลมทั้งสองบริเวณ"),
                         topic=TOPIC_FORCE, hint="ความกดอากาศเปลี่ยนมากในระยะสั้น (ไอโซบาร์ชิด) ลมยิ่งแรง")
