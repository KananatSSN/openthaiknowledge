"""สมบัติของสิ่งมีชีวิตและการจัดระบบของสิ่งมีชีวิต

ชีวะ · ม.4 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 1 ม.4/1

Sets moved here from: science_wave_f43.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f43 import BIOLOGY, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_LIFE = "สมบัติของสิ่งมีชีวิตและการจัดระบบของสิ่งมีชีวิต"


PROPERTIES = (
    ("มีการจัดระบบภายในเซลล์และร่างกาย", ("เซลล์หลายเซลล์รวมเป็นเนื้อเยื่อและอวัยวะที่ทำงานร่วมกัน",
                                         "อะมีบาเซลล์เดียวมีออร์แกเนลล์ทำหน้าที่ต่าง ๆ")),
    ("มีเมแทบอลิซึม", ("ร่างกายย่อยอาหารและสลายกลูโคสเพื่อให้ได้พลังงาน", "พืชสังเคราะห์ด้วยแสงสร้างน้ำตาล")),
    ("รักษาดุลยภาพของร่างกาย", ("เหงื่อออกเมื่ออากาศร้อนเพื่อรักษาอุณหภูมิร่างกาย", "ไตปรับปริมาณน้ำในปัสสาวะ")),
    ("มีการเจริญเติบโตและเปลี่ยนแปลงตามวัย", ("ลูกอ๊อดเปลี่ยนเป็นกบ", "เมล็ดงอกเป็นต้นกล้าแล้วเติบโตเป็นต้นไม้")),
    ("มีการสืบพันธุ์", ("แบคทีเรียแบ่งตัวแบบทวิภาค", "ไก่วางไข่แล้วฟักเป็นลูกไก่")),
    ("ตอบสนองต่อสิ่งเร้า", ("ใบไมยราบหุบเมื่อถูกสัมผัส", "ม่านตาหดเล็กลงเมื่อแสงจ้า")),
    ("มีการปรับตัวและวิวัฒนาการ", ("ต้นกระบองเพชรมีใบเป็นหนามช่วยลดการคายน้ำ", "แบคทีเรียดื้อยาเพิ่มขึ้นในประชากร")),
)


LEVELS = ("อะตอม", "โมเลกุล", "เซลล์", "เนื้อเยื่อ", "อวัยวะ", "ระบบอวัยวะ", "สิ่งมีชีวิต", "ประชากร", "กลุ่มสิ่งมีชีวิต",
          "ระบบนิเวศ", "โลกของสิ่งมีชีวิต")


LEVEL_EXAMPLES = (
    ("เซลล์ประสาทหนึ่งเซลล์", "เซลล์"), ("กล้ามเนื้อหัวใจ", "เนื้อเยื่อ"), ("หัวใจ", "อวัยวะ"), ("ระบบหมุนเวียนเลือด", "ระบบอวัยวะ"),
    ("ช้างหนึ่งตัว", "สิ่งมีชีวิต"), ("ช้างทั้งฝูงในป่าแห่งหนึ่ง", "ประชากร"),
    ("ช้าง กวาง และต้นไม้ทุกชนิดในป่าแห่งหนึ่ง", "กลุ่มสิ่งมีชีวิต"), ("ป่าทั้งผืนรวมทั้งดิน น้ำ และอากาศ", "ระบบนิเวศ"),
    ("โมเลกุลของ DNA", "โมเลกุล"), ("ใบของพืช", "อวัยวะ"), ("ปลานิลทั้งหมดในบ่อหนึ่ง", "ประชากร"),
)


@question_type(
    "biology.life_property_foundation",
    display_name={"th": "สมบัติของสิ่งมีชีวิต"},
    level=UPPER_FOUR, subject=BIOLOGY, topic=TOPIC_LIFE,
)
class LifePropertyFoundation(QuestionType):
    """Match an example to the property of life it shows."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        prop, examples = rng.choice(PROPERTIES)
        example = rng.choice(examples)
        others = [p for p, _ in PROPERTIES if p != prop]
        if rng.random() < 0.6:
            return _labelled(stem=f"\"{example}\" แสดงสมบัติของสิ่งมีชีวิตข้อใด", correct=prop,
                             wrongs=tuple(others), topic=TOPIC_LIFE,
                             hint="สิ่งมีชีวิตมีการจัดระบบ เมแทบอลิซึม ดุลยภาพ การเจริญเติบโต การสืบพันธุ์ การตอบสนอง และการปรับตัว")
        other_examples = [e for p, es in PROPERTIES if p != prop for e in es]
        return _labelled(stem=f"ข้อใดเป็นตัวอย่างของสมบัติ \"{prop}\"", correct=example,
                         wrongs=tuple(other_examples), topic=TOPIC_LIFE,
                         hint="นึกว่าตัวอย่างนั้นเกี่ยวกับพลังงาน การรักษาสภาพ การเติบโต การสืบพันธุ์ หรือการตอบสนอง")


@question_type(
    "biology.life_property_fluency",
    display_name={"th": "ระดับการจัดระบบของสิ่งมีชีวิต"},
    level=UPPER_FOUR, subject=BIOLOGY, topic=TOPIC_LIFE,
)
class LifePropertyFluency(QuestionType):
    """From atoms to the biosphere, each level built of the one below."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            example, level = rng.choice(LEVEL_EXAMPLES)
            near = [ell for ell in LEVELS if ell != level]
            i = LEVELS.index(level)
            close = [LEVELS[j] for j in (i - 1, i + 1) if 0 <= j < len(LEVELS)]
            far = [ell for ell in near if ell not in close]
            return _labelled(stem=f"\"{example}\" จัดอยู่ในระดับการจัดระบบใด", correct=level,
                             wrongs=(*close, *rng.sample(far, 3 - len(close))), topic=TOPIC_LIFE,
                             hint="เซลล์ → เนื้อเยื่อ → อวัยวะ → ระบบอวัยวะ → สิ่งมีชีวิต → ประชากร → กลุ่มสิ่งมีชีวิต → ระบบนิเวศ")
        i = rng.randrange(len(LEVELS) - 1)
        right = LEVELS[i + 1]
        others = [ell for ell in LEVELS if ell not in (right, LEVELS[i])]
        return _labelled(stem=f"ระดับการจัดระบบที่อยู่ถัดขึ้นไปจาก \"{LEVELS[i]}\" คือข้อใด", correct=right,
                         wrongs=tuple(others), topic=TOPIC_LIFE,
                         hint="อะตอม → โมเลกุล → เซลล์ → เนื้อเยื่อ → อวัยวะ → ระบบอวัยวะ → สิ่งมีชีวิต → ประชากร → กลุ่มสิ่งมีชีวิต → ระบบนิเวศ → โลกของสิ่งมีชีวิต")


@question_type(
    "biology.life_property_application",
    display_name={"th": "ตัดสินว่าสิ่งใดเป็นสิ่งมีชีวิตจากสมบัติ"},
    level=UPPER_FOUR, subject=BIOLOGY, topic=TOPIC_LIFE,
)
class LifePropertyApplication(QuestionType):
    """A single property, such as growth, is not enough; living things show them all."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        cases = (
            ("ผลึกเกลือที่ใหญ่ขึ้นในสารละลายอิ่มตัว", "ไม่ใช่สิ่งมีชีวิต เพราะแม้จะใหญ่ขึ้นแต่ไม่มีเมแทบอลิซึมและไม่สืบพันธุ์"),
            ("ไฟที่ลุกลามและใช้ออกซิเจน", "ไม่ใช่สิ่งมีชีวิต เพราะไม่มีเซลล์และไม่มีการสืบพันธุ์ที่ถ่ายทอดลักษณะ"),
            ("ยีสต์ในแป้งขนมปังที่ทำให้แป้งฟู", "เป็นสิ่งมีชีวิต เพราะมีเซลล์ มีเมแทบอลิซึม และสืบพันธุ์ได้"),
            ("เมล็ดถั่วแห้งที่เก็บไว้ในขวด", "เป็นสิ่งมีชีวิตในระยะพักตัว เพราะงอกและเติบโตได้เมื่อได้รับน้ำ"),
            ("ไวรัสนอกเซลล์เจ้าบ้าน", "มีสมบัติบางอย่างของสิ่งมีชีวิต แต่เพิ่มจำนวนได้เฉพาะในเซลล์เจ้าบ้าน"),
            ("หุ่นยนต์ที่เคลื่อนที่หนีสิ่งกีดขวาง", "ไม่ใช่สิ่งมีชีวิต เพราะแม้ตอบสนองได้แต่ไม่มีเซลล์ เมแทบอลิซึม และการสืบพันธุ์"),
        )
        case, right = rng.choice(cases)
        others = [c[1] for c in cases if c[1] != right]
        return _labelled(stem=f"\"{case}\" ข้อใดสรุปได้เหมาะสมที่สุด", correct=right, wrongs=tuple(others),
                         topic=TOPIC_LIFE, hint="สิ่งมีชีวิตต้องแสดงสมบัติหลายอย่างร่วมกัน ไม่ใช่เพียงอย่างเดียว")
