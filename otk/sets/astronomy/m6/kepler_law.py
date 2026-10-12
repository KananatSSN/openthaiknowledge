"""กฎของเคพเลอร์และกฎความโน้มถ่วงของนิวตัน

ดาราศาสตร์ · ม.6 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 3 ม.6/11

Sets moved here from: science_wave_f84.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f84 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_KEPLER = "กฎของเคพเลอร์และกฎความโน้มถ่วงของนิวตัน"


KEPLER_FACTS = (
    ("กฎข้อที่ 1 ของเคพเลอร์กล่าวว่าอย่างไร", "ดาวเคราะห์โคจรรอบดวงอาทิตย์เป็นวงรี โดยมีดวงอาทิตย์อยู่ที่โฟกัสหนึ่ง",
     ("ดาวเคราะห์โคจรเป็นวงกลมมีดวงอาทิตย์อยู่ที่จุดศูนย์กลางพอดี", "เส้นที่ลากจากดวงอาทิตย์ถึงดาวเคราะห์กวาดพื้นที่เท่ากันในเวลาเท่ากัน",
      "กำลังสองของคาบแปรผันตรงกับกำลังสามของระยะทางเฉลี่ย", "ดวงอาทิตย์โคจรรอบโลก")),
    ("กฎข้อที่ 2 ของเคพเลอร์กล่าวว่าอย่างไร", "เส้นที่ลากจากดวงอาทิตย์ถึงดาวเคราะห์กวาดพื้นที่เท่ากันในเวลาเท่ากัน",
     ("ดาวเคราะห์โคจรรอบดวงอาทิตย์เป็นวงรี โดยมีดวงอาทิตย์อยู่ที่โฟกัสหนึ่ง", "กำลังสองของคาบแปรผันตรงกับกำลังสามของระยะทางเฉลี่ย",
      "ดาวเคราะห์เคลื่อนที่ด้วยอัตราเร็วคงที่ตลอดวงโคจร", "ดาวเคราะห์ทุกดวงมีคาบเท่ากัน")),
    ("กฎข้อที่ 3 ของเคพเลอร์กล่าวว่าอย่างไร", "กำลังสองของคาบแปรผันตรงกับกำลังสามของระยะทางเฉลี่ยจากดวงอาทิตย์",
     ("ดาวเคราะห์โคจรรอบดวงอาทิตย์เป็นวงรี โดยมีดวงอาทิตย์อยู่ที่โฟกัสหนึ่ง", "เส้นที่ลากจากดวงอาทิตย์ถึงดาวเคราะห์กวาดพื้นที่เท่ากันในเวลาเท่ากัน",
      "คาบแปรผันตรงกับระยะทาง", "ดาวเคราะห์ที่ไกลกว่ามีคาบสั้นกว่า")),
    ("นิวตันอธิบายว่าอะไรทำให้ดาวเคราะห์โคจรรอบดวงอาทิตย์", "แรงโน้มถ่วงระหว่างดวงอาทิตย์กับดาวเคราะห์เป็นแรงสู่ศูนย์กลาง",
     ("แรงแม่เหล็กของดวงอาทิตย์", "ลมสุริยะผลักดาวเคราะห์", "แรงเสียดทานในอวกาศ", "ดาวเคราะห์ไม่มีแรงใดกระทำ")),
    ("เคพเลอร์ตั้งกฎการเคลื่อนที่ของดาวเคราะห์จากข้อมูลของใคร", "ข้อมูลการสังเกตตำแหน่งดาวเคราะห์ของไทโค บราเฮ",
     ("การทดลองของนิวตัน", "ภาพถ่ายจากกล้องฮับเบิล", "การคำนวณของไอน์สไตน์", "ข้อมูลจากยานอวกาศวอยเอเจอร์")),
    ("ตามกฎของเคพเลอร์ โลกเคลื่อนที่เร็วที่สุดเมื่ออยู่ตำแหน่งใดในวงโคจร", "ตำแหน่งใกล้ดวงอาทิตย์ที่สุด (เพริฮีเลียน)",
     ("ตำแหน่งไกลดวงอาทิตย์ที่สุด (แอฟฮีเลียน)", "เร็วเท่ากันทุกตำแหน่ง", "ตำแหน่งที่อยู่ห่างดวงอาทิตย์ 2 AU", "ขณะเกิดจันทรุปราคา")),
    ("ตามกฎความโน้มถ่วงของนิวตัน แรงโน้มถ่วงระหว่างวัตถุสองก้อนขึ้นกับปัจจัยใด", "มวลของวัตถุทั้งสองและระยะห่างระหว่างกัน",
     ("สีและอุณหภูมิของวัตถุ", "ความเร็วในการหมุนรอบตัวเองเท่านั้น", "ปริมาตรเพียงอย่างเดียว", "ประจุไฟฟ้าของวัตถุ")),
)


KEPLER_HINT = ("เคพเลอร์ 1: วงโคจรเป็นวงรี ดวงอาทิตย์อยู่ที่โฟกัส 2: กวาดพื้นที่เท่ากันในเวลาเท่ากัน ใกล้ดวงอาทิตย์เคลื่อนที่เร็ว "
               "3: T² = a³ (T เป็นปี a เป็นหน่วยดาราศาสตร์) นิวตัน F = GMm ÷ r²")


@question_type(
    "astro.kepler_law_foundation",
    display_name={"th": "กฎสามข้อของเคพเลอร์และกฎความโน้มถ่วงของนิวตัน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_KEPLER,
)
class KeplerLawFoundation(QuestionType):
    """The three laws and gravity as the centripetal force."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(KEPLER_FACTS)
        if rng.random() < 0.4 and stem.startswith("กฎข้อที่"):
            number = next(ch for ch in stem if ch.isdigit())
            return _labelled(stem=f"\"{right}\" เป็นกฎข้อใด", correct=f"กฎข้อที่ {number} ของเคพเลอร์",
                             wrongs=(*(f"กฎข้อที่ {n} ของเคพเลอร์" for n in "123" if n != number), "กฎความโน้มถ่วงของนิวตัน"),
                             topic=TOPIC_KEPLER, hint=KEPLER_HINT)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_KEPLER, hint=KEPLER_HINT)


@question_type(
    "astro.kepler_law_fluency",
    display_name={"th": "ใช้กฎของเคพเลอร์และนิวตันเปรียบเทียบการโคจร"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_KEPLER,
)
class KeplerLawFluency(QuestionType):
    """Faster at perihelion; farther means longer years; gravity by distance and mass."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.35:
            points = rng.sample(range(1, 50), 4)
            names = ("ตำแหน่ง ก", "ตำแหน่ง ข", "ตำแหน่ง ค", "ตำแหน่ง ง")
            fast = rng.random() < 0.5
            pick = points.index(min(points) if fast else max(points))
            table = " ".join(f"{n} ห่างดวงอาทิตย์ {show(Fraction(p, 10))} AU" for n, p in zip(names, points))
            return _labelled(stem=f"ดาวหางดวงหนึ่งโคจรเป็นวงรี {table} ดาวหางเคลื่อนที่{'เร็ว' if fast else 'ช้า'}ที่สุดที่ตำแหน่งใด",
                             correct=names[pick], wrongs=tuple(n for n in names if n != names[pick]), topic=TOPIC_KEPLER, hint=KEPLER_HINT)
        if roll < 0.65:
            planets = (("ดาวพุธ", 4), ("ดาวศุกร์", 7), ("โลก", 10), ("ดาวอังคาร", 15), ("ดาวพฤหัสบดี", 52), ("ดาวเสาร์", 95), ("ดาวยูเรนัส", 192), ("ดาวเนปจูน", 301))
            picked = rng.sample(planets, 4)
            longest = rng.random() < 0.5
            right = (max if longest else min)(picked, key=lambda p: p[1])[0]
            return _labelled(stem=f"ตามกฎข้อที่ 3 ของเคพเลอร์ ดาวเคราะห์ใดมีคาบการโคจร{'ยาว' if longest else 'สั้น'}ที่สุด", correct=right,
                             wrongs=tuple(p[0] for p in picked if p[0] != right), topic=TOPIC_KEPLER, hint=KEPLER_HINT)
        k = rng.randint(2, 5)
        what = rng.choice(("ระยะห่าง", "มวลของดาวเคราะห์"))
        if what == "ระยะห่าง":
            right = f"ลดลงเหลือ 1/{k * k} เท่า"
            wrongs = (f"ลดลงเหลือ 1/{k} เท่า", f"เพิ่มขึ้น {k * k} เท่า", f"เพิ่มขึ้น {k} เท่า")
            stem = f"ถ้าระยะห่างระหว่างดวงอาทิตย์กับดาวเคราะห์เพิ่มขึ้น {k} เท่า แรงโน้มถ่วงระหว่างกันจะเปลี่ยนอย่างไร"
        else:
            right = f"เพิ่มขึ้น {k} เท่า"
            wrongs = (f"เพิ่มขึ้น {k * k} เท่า", f"ลดลงเหลือ 1/{k} เท่า", f"ลดลงเหลือ 1/{k * k} เท่า")
            stem = f"ถ้ามวลของดาวเคราะห์เพิ่มขึ้น {k} เท่า โดยระยะห่างเท่าเดิม แรงโน้มถ่วงระหว่างดวงอาทิตย์กับดาวเคราะห์จะเปลี่ยนอย่างไร"
        return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_KEPLER, hint=KEPLER_HINT)


@question_type(
    "astro.kepler_law_application",
    display_name={"th": "คำนวณคาบการโคจรด้วยกฎข้อที่ 3 ของเคพเลอร์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_KEPLER,
)
class KeplerLawApplication(QuestionType):
    """T² = a³ both ways, with perfect squares and cubes."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        root = rng.randint(1, 10)
        if root == 1:
            root = rng.randint(2, 10)
        a = root * root
        period = root ** 3
        body = rng.choice(("ดาวเคราะห์น้อยดวงหนึ่ง", "ดาวหางดวงหนึ่ง", "ดาวเคราะห์แคระดวงหนึ่ง", "วัตถุในแถบไคเปอร์ดวงหนึ่ง"))
        if rng.random() < 0.5:
            return numeric(stem=f"{body}โคจรรอบดวงอาทิตย์โดยมีระยะทางเฉลี่ย {a} AU (T² = a³ เมื่อ T เป็นปีและ a เป็น AU) มีคาบการโคจรกี่ปี",
                           answer=period, wrongs=[a * a, Fraction(a * 3, 2), a], unit="ปี", topic=TOPIC_KEPLER, hint="T = √(a³)")
        return numeric(stem=f"{body}มีคาบการโคจรรอบดวงอาทิตย์ {period} ปี (T² = a³ เมื่อ T เป็นปีและ a เป็น AU) มีระยะทางเฉลี่ยจากดวงอาทิตย์กี่ AU",
                       answer=a, wrongs=[period, root, Fraction(period * 2, 3) if (Fraction(period * 2, 3) * 100).denominator == 1 else period * 2],
                       unit="AU", topic=TOPIC_KEPLER, hint="a = ∛(T²)")
