"""การหมุนเวียนของอากาศตามเขตละติจูด

ธรณีวิทยา · ม.5 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 2 ม.5/4

Sets moved here from: science_wave_f78.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f78 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_CELL = "การหมุนเวียนของอากาศตามเขตละติจูด"


CELLS = (
    ("เซลล์แฮดลีย์", (0, 30), "ลมค้า", "อากาศร้อนลอยตัวที่เส้นศูนย์สูตรและจมตัวที่ละติจูดประมาณ 30 องศา"),
    ("เซลล์เฟอร์เรล", (30, 60), "ลมตะวันตก", "อยู่ระหว่างละติจูด 30 ถึง 60 องศา อากาศผิวพื้นเคลื่อนที่ไปทางขั้วโลก"),
    ("เซลล์ขั้วโลก", (60, 90), "ลมตะวันออกขั้วโลก", "อากาศเย็นจมตัวที่ขั้วโลกและเคลื่อนที่ไปทางละติจูด 60 องศา"),
)


BELTS = (
    (0, "แถบความกดอากาศต่ำบริเวณเส้นศูนย์สูตร", "ฝนตกชุก อากาศร้อนชื้น"),
    (30, "แถบความกดอากาศสูงกึ่งเขตร้อน", "อากาศแห้ง เป็นที่ตั้งของทะเลทรายใหญ่หลายแห่ง"),
    (60, "แถบความกดอากาศต่ำละติจูดกลาง", "มีเมฆและฝนมากจากแนวปะทะอากาศขั้วโลก"),
    (90, "แถบความกดอากาศสูงขั้วโลก", "หนาวเย็นและแห้ง"),
)


CELL_HINT = ("เซลล์แฮดลีย์ 0-30° ลมค้า เซลล์เฟอร์เรล 30-60° ลมตะวันตก เซลล์ขั้วโลก 60-90° ลมตะวันออกขั้วโลก "
             "อากาศลอยตัวที่ 0° และ 60° มีฝนมาก อากาศจมตัวที่ 30° และขั้วโลกแห้งแล้ง")


@question_type(
    "geo.latitude_wind_foundation",
    display_name={"th": "เซลล์การหมุนเวียนของอากาศและลมประจำเขตละติจูด"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_CELL,
)
class LatitudeWindFoundation(QuestionType):
    """Name the cell and its surface wind from the latitude."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, (lo, hi), wind, what = rng.choice(CELLS)
        lat = rng.randint(lo + 5, hi - 5)
        side = rng.choice(("เหนือ", "ใต้"))
        others = [c for c in CELLS if c[0] != name]
        roll = rng.random()
        if roll < 0.4:
            return _labelled(stem=f"บริเวณละติจูด {lat} องศา{side} อยู่ในการหมุนเวียนของอากาศแบบใด", correct=name,
                             wrongs=(*(c[0] for c in others), "เซลล์มรสุม"), topic=TOPIC_CELL, hint=CELL_HINT)
        if roll < 0.7:
            return _labelled(stem=f"ลมประจำที่พัดใกล้ผิวโลกบริเวณละติจูด {lat} องศา{side}คือลมใด", correct=wind,
                             wrongs=(*(c[2] for c in others), "ลมบกลมทะเล"), topic=TOPIC_CELL, hint=CELL_HINT)
        return _labelled(stem=f"ข้อใดเป็นลักษณะของ{name}", correct=what, wrongs=(*(c[3] for c in others), "อากาศไม่เคลื่อนที่ในแนวตั้งเลย"),
                         topic=TOPIC_CELL, hint=CELL_HINT)


@question_type(
    "geo.latitude_wind_fluency",
    display_name={"th": "แถบความกดอากาศและภูมิอากาศตามละติจูด"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_CELL,
)
class LatitudeWindFluency(QuestionType):
    """Wet where air rises, dry where it sinks."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        lat, belt, climate = rng.choice(BELTS)
        others = [b for b in BELTS if b[0] != lat]
        shown = max(0, min(90, lat + rng.randint(-3, 3)))
        side = "" if shown == 0 else rng.choice((" เหนือ", " ใต้"))
        if rng.random() < 0.5:
            return _labelled(stem=f"บริเวณละติจูดประมาณ {shown} องศา{side}มีภูมิอากาศลักษณะใด", correct=climate, wrongs=tuple(b[2] for b in others),
                             topic=TOPIC_CELL, hint=CELL_HINT)
        return _labelled(stem=f"บริเวณละติจูดประมาณ {shown} องศา{side}เป็นแถบความกดอากาศใด", correct=belt, wrongs=tuple(b[1] for b in others),
                         topic=TOPIC_CELL, hint=CELL_HINT)


@question_type(
    "geo.latitude_wind_application",
    display_name={"th": "ทิศทางลมค้าและผลต่อภูมิอากาศของพื้นที่จริง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_CELL,
)
class LatitudeWindApplication(QuestionType):
    """Trade-wind directions, and real places explained by the cells."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.45:
            north = rng.random() < 0.5
            wind = rng.choice(("ลมค้า", "ลมตะวันตก", "ลมตะวันออกขั้วโลก"))
            right = {("ลมค้า", True): "ลมตะวันออกเฉียงเหนือ", ("ลมค้า", False): "ลมตะวันออกเฉียงใต้",
                     ("ลมตะวันตก", True): "ลมตะวันตกเฉียงใต้", ("ลมตะวันตก", False): "ลมตะวันตกเฉียงเหนือ",
                     ("ลมตะวันออกขั้วโลก", True): "ลมตะวันออกเฉียงเหนือ", ("ลมตะวันออกขั้วโลก", False): "ลมตะวันออกเฉียงใต้"}[(wind, north)]
            return _labelled(stem=f"{wind}ในซีกโลก{'เหนือ' if north else 'ใต้'}พัดมาจากทิศใด", correct=right,
                             wrongs=tuple(w for w in ("ลมตะวันออกเฉียงเหนือ", "ลมตะวันออกเฉียงใต้", "ลมตะวันตกเฉียงใต้", "ลมตะวันตกเฉียงเหนือ") if w != right),
                             topic=TOPIC_CELL, hint=CELL_HINT + " ลมค้าเบนจากแรงคอริออลิสจึงพัดมาจากทิศตะวันออก")
        cases = (("ทะเลทรายสะฮาราอยู่บริเวณละติจูดประมาณ 30 องศาเหนือ เหตุใดจึงแห้งแล้ง", "อากาศจมตัวที่แถบความกดอากาศสูงกึ่งเขตร้อน จึงไม่ค่อยเกิดเมฆและฝน",
                  ("อากาศร้อนลอยตัวมากจนความชื้นระเหยหายไปก่อนเกิดเมฆและฝน", "อยู่ใกล้ขั้วโลกจึงหนาวจนไอน้ำในอากาศควบแน่นไม่ได้", "ไม่มีแรงคอริออลิสที่ละติจูดนี้", "ลมตะวันตกพัดความชื้นเข้ามาตลอดปี")),
                 ("ป่าดิบชื้นลุ่มน้ำแอมะซอนใกล้เส้นศูนย์สูตรมีฝนชุกเพราะเหตุใด", "อากาศร้อนชื้นลอยตัวที่แถบความกดอากาศต่ำ จึงเกิดเมฆและฝนมาก",
                  ("อากาศเย็นจมตัวลงมาปะทะความชื้น จึงเกิดเมฆและฝนตกมาก", "มีแถบความกดอากาศสูงปกคลุมตลอดปี อากาศจึงอิ่มตัวง่าย", "อยู่ในเซลล์ขั้วโลก ลมหนาวจึงพาความชื้นมาควบแน่น", "ลมตะวันออกขั้วโลกพัดผ่านและพาฝนมาจากขั้วโลก")),
                 ("เรือใบในอดีตใช้เส้นทางที่ละติจูด 10-20 องศาเพื่อข้ามมหาสมุทรไปทางตะวันตก เพราะเหตุใด", "มีลมค้าพัดจากทิศตะวันออกอย่างสม่ำเสมอ",
                  ("มีลมตะวันตกพัดแรงตลอดปี", "เป็นเขตลมสงบตลอดเวลา", "มีลมตะวันออกขั้วโลกพัดผ่าน", "กระแสลมพัดจากทิศใต้ไปเหนือเท่านั้น")),
                 ("ยุโรปตะวันตกที่ละติจูดประมาณ 50 องศามีฝนตกกระจายตลอดปีเพราะเหตุใด", "ลมตะวันตกพัดพาความชื้นจากมหาสมุทรเข้าสู่แผ่นดิน",
                  ("ลมค้าพัดพาความชื้นจากมหาสมุทรเข้ามาทางทิศตะวันออก", "อยู่ในแถบความกดอากาศสูงกึ่งเขตร้อนที่อากาศลอยตัว", "อากาศจมตัวตลอดปี จึงมีฝนตกกระจาย", "อยู่ใกล้เส้นศูนย์สูตรที่อากาศร้อนชื้นลอยตัว")),
                 ("ทะเลทรายคาลาฮารีและทะเลทรายในออสเตรเลียอยู่ใกล้ละติจูด 25-30 องศาใต้ เหตุใดจึงแห้งแล้ง", "อยู่ใต้แถบความกดอากาศสูงกึ่งเขตร้อนที่อากาศจมตัว",
                  ("อยู่ใต้แถบความกดอากาศต่ำที่เส้นศูนย์สูตรที่อากาศลอยตัว", "อยู่ในเซลล์ขั้วโลกที่อากาศเย็นและแห้งตลอดปี", "มีลมตะวันตกพัดความชื้นเข้ามาจนหมดก่อนถึงแผ่นดิน", "อากาศร้อนลอยตัวแรงตลอดปี")),
                 ("อินโดนีเซียซึ่งอยู่ใกล้เส้นศูนย์สูตรมีเมฆและพายุฝนฟ้าคะนองเกือบทุกวันเพราะเหตุใด", "อยู่ในแนวที่ลมค้าจากสองซีกโลกมาบรรจบและอากาศลอยตัว",
                  ("อยู่ใต้แถบความกดอากาศสูงกึ่งเขตร้อนที่อากาศจมตัว", "มีอากาศจมตัวตลอดปี ความชื้นจึงควบแน่นเป็นฝน", "อยู่ในเขตลมตะวันออกขั้วโลกที่พาอากาศเย็นมาปะทะ", "ไม่มีแสงอาทิตย์ส่องถึง")))
        stem, right, wrongs = rng.choice(cases)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_CELL, hint=CELL_HINT)
