"""การตอบสนองของร่างกายต่อสิ่งแปลกปลอม

ชีวะ · ม.4 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.4/5

Sets moved here from: science_wave_b20.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import SUBJECT, scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_b19 import UPPER_FOUR, Fact, _fact_question
from otk.sets._support.science_wave_b20 import IMMUNE_SCENARIOS, IMMUNE_TOPIC

PROVENANCE = Provenance("original")


IMMUNE_FACTS = (
    Fact("การตอบสนองของร่างกายแบบไม่จำเพาะหมายถึงอะไร",
         "กลไกที่ร่างกายใช้ต้านสิ่งแปลกปลอมทุกชนิดในแบบเดียวกัน "
         "โดยไม่เลือกว่าเป็นเชื้อชนิดใดและไม่เก็บความจำไว้ใช้ครั้งต่อไป"),
    Fact("ด่านแรกของการตอบสนองแบบไม่จำเพาะคืออะไร",
         "ผิวหนังและเยื่อเมือกที่กั้นไม่ให้เชื้อเข้าสู่ร่างกาย ร่วมกับสารคัดหลั่ง "
         "เช่น น้ำตาและน้ำย่อย ซึ่งทำลายเชื้อทั่วไปได้"),
    Fact("การอักเสบเกิดขึ้นได้อย่างไรและมีประโยชน์อย่างไร",
         "หลอดเลือดบริเวณที่ติดเชื้อขยายตัว เลือดและเซลล์เม็ดเลือดขาวจึงมาถึง"
         "บริเวณนั้นได้มากขึ้น จึงเห็นเป็นอาการบวม แดง ร้อน"),
    Fact("ฟาโกไซโทซิสคือกระบวนการใด",
         "การที่เซลล์เม็ดเลือดขาวบางชนิดโอบกลืนแล้วย่อยสลายสิ่งแปลกปลอม "
         "โดยทำกับเชื้อทุกชนิดในแบบเดียวกัน"),
    Fact("การตอบสนองแบบจำเพาะต่างจากแบบไม่จำเพาะอย่างไร",
         "ตอบสนองต่อแอนติเจนแต่ละชนิดโดยเฉพาะ ใช้เวลาเริ่มต้นนานกว่า "
         "แต่เก็บเซลล์ความจำไว้ให้ตอบสนองต่อเชื้อเดิมได้เร็วและแรงขึ้น"),
    Fact("เซลล์บีมีบทบาทอย่างไรในการตอบสนองแบบจำเพาะ",
         "เซลล์บีที่จำเพาะต่อแอนติเจนจะแบ่งตัวและเปลี่ยนเป็นเซลล์พลาสมา "
         "ซึ่งสร้างแอนติบอดีออกมาจับกับแอนติเจนชนิดนั้น"),
    Fact("เซลล์ทีมีบทบาทอย่างไรในการตอบสนองแบบจำเพาะ",
         "เซลล์ทีผู้ช่วยกระตุ้นเซลล์บีและเซลล์อื่นให้ทำงาน "
         "ส่วนเซลล์ทีพิฆาตทำลายเซลล์ของร่างกายที่ติดเชื้อไวรัสหรือผิดปกติไป"),
    Fact("เหตุใดการได้รับวัคซีนจึงช่วยป้องกันโรคได้",
         "วัคซีนกระตุ้นการตอบสนองแบบจำเพาะให้สร้างเซลล์ความจำไว้ล่วงหน้า "
         "เมื่อได้รับเชื้อจริงร่างกายจึงตอบสนองได้เร็วและแรงพอที่จะไม่เกิดโรค"),
)


class Defence(NamedTuple):
    """One defence, which kind it is, and the reason that settles the kind."""
    example: str
    kind: str
    reason: str


DEFENCES = (
    Defence("ผิวหนังที่ไม่มีบาดแผลกั้นเชื้อโรคไว้ภายนอกร่างกาย", "ไม่จำเพาะ",
            "เป็นด่านกั้นทางกายภาพที่กันเชื้อทุกชนิดเหมือนกัน "
            "โดยร่างกายไม่ต้องเคยรู้จักเชื้อนั้นมาก่อน"),
    Defence("แผลที่นิ้วบวม แดง และร้อนหลังถูกมีดบาด", "ไม่จำเพาะ",
            "เป็นการอักเสบซึ่งเกิดขึ้นในแบบเดียวกันไม่ว่าเชื้อที่เข้ามาจะเป็นชนิดใด"),
    Defence("เซลล์เม็ดเลือดขาวโอบกลืนแบคทีเรียที่เข้าสู่ร่างกาย", "ไม่จำเพาะ",
            "เป็นฟาโกไซโทซิสที่กลืนกินสิ่งแปลกปลอมทุกชนิดโดยไม่เลือกแอนติเจน"),
    Defence("น้ำตาชะล้างและทำลายเชื้อที่เข้าตา", "ไม่จำเพาะ",
            "เป็นสารคัดหลั่งที่มีเอนไซม์ทำลายผนังเซลล์ของแบคทีเรียได้ทั่วไป"),
    Defence("ร่างกายสร้างแอนติบอดีต่อไวรัสหัดหลังได้รับวัคซีน", "จำเพาะ",
            "แอนติบอดีที่สร้างขึ้นจับได้กับแอนติเจนของเชื้อนั้นเพียงชนิดเดียว"),
    Defence("ผู้ที่เคยเป็นอีสุกอีใสแล้วมักไม่เป็นซ้ำอีก", "จำเพาะ",
            "ร่างกายเก็บเซลล์ความจำต่อเชื้อชนิดนั้นไว้ "
            "จึงตอบสนองได้เร็วและแรงขึ้นเมื่อพบเชื้อเดิมอีกครั้ง"),
    Defence("เซลล์ทีพิฆาตทำลายเซลล์ของร่างกายที่ติดเชื้อไวรัส", "จำเพาะ",
            "เซลล์ทีจะจดจำและทำลายเฉพาะเซลล์ที่แสดงแอนติเจนของเชื้อนั้น"),
)


# The order an item asks about. This is the content of the แผนผัง the indicator
# also names; the item can ask a learner to read it, not to draw it.
DEFENCE_ORDER = (
    "ผิวหนังและเยื่อเมือกกั้นเชื้อไว้ไม่ให้เข้าสู่ร่างกาย",
    "การอักเสบและฟาโกไซโทซิสจัดการเชื้อที่ผ่านด่านแรกเข้ามา",
    "เซลล์ที่กลืนเชื้อนำเสนอแอนติเจนของเชื้อนั้นแก่เซลล์ที",
    "เซลล์ทีผู้ช่วยกระตุ้นให้เซลล์บีสร้างแอนติบอดีที่จำเพาะต่อแอนติเจนนั้น",
    "เซลล์ความจำถูกเก็บไว้เพื่อตอบสนองต่อเชื้อเดิมได้เร็วขึ้นในครั้งต่อไป",
)


@question_type(
    "body.immune_response_foundation",
    display_name={"th": "การตอบสนองของร่างกายต่อสิ่งแปลกปลอม"},
    level=UPPER_FOUR, subject=SUBJECT, topic=IMMUNE_TOPIC,
)
class ImmuneResponseFoundation(QuestionType):
    """Explain each defence — the ``อธิบาย`` half of ``ม.4/5``."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _fact_question(
            rng, IMMUNE_FACTS, topic=IMMUNE_TOPIC,
            hint="ถามว่ากลไกนั้นทำกับเชื้อทุกชนิดเหมือนกันหรือเลือกทำกับเชื้อ"
                 "ชนิดเดียว และเก็บความจำไว้หรือไม่",
        )


@question_type(
    "body.immune_response_fluency",
    display_name={"th": "แยกการตอบสนองแบบไม่จำเพาะออกจากแบบจำเพาะ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=IMMUNE_TOPIC,
)
class ImmuneResponseFluency(QuestionType):
    """Say which kind a given defence is, and why it is that kind."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            index = rng.randrange(len(DEFENCE_ORDER) - 1)
            following = DEFENCE_ORDER[index + 1]
            others = [step for step in DEFENCE_ORDER if step != following]
            rng.shuffle(others)
            return _labelled(
                stem=f"ในการตอบสนองต่อเชื้อที่เข้าสู่ร่างกาย เมื่อ"
                     f"“{DEFENCE_ORDER[index]}” แล้ว ขั้นต่อไปคือข้อใด",
                correct=following, wrongs=tuple(others[:3]),
                hint="การตอบสนองแบบไม่จำเพาะเกิดก่อนและเร็วกว่า "
                     "ส่วนแบบจำเพาะตามมาทีหลังและจบที่การเก็บความจำ",
                topic=IMMUNE_TOPIC,
            )
        item = rng.choice(DEFENCES)
        others = [f"แบบ{other.kind} เพราะ{other.reason}" for other in DEFENCES
                  if other.example != item.example]
        rng.shuffle(others)
        return _labelled(
            stem=f"“{item.example}” เป็นการตอบสนองต่อสิ่งแปลกปลอมแบบใด "
                 f"และเพราะเหตุใด",
            correct=f"แบบ{item.kind} เพราะ{item.reason}",
            wrongs=tuple(others[:3]),
            hint="เหตุผลที่ถูกต้องต้องอธิบายกรณีนี้ได้จริง "
                 "ไม่ใช่เพียงระบุชนิดของการตอบสนองให้ถูก",
            topic=IMMUNE_TOPIC,
        )


@question_type(
    "body.immune_response_application",
    display_name={"th": "วิเคราะห์การตอบสนองของระบบภูมิคุ้มกัน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=IMMUNE_TOPIC,
)
class ImmuneResponseApplication(QuestionType):
    """Read a result — or a given แผนผัง — back to the response behind it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, IMMUNE_SCENARIOS,
            hint="ถามว่ากลไกที่เกี่ยวข้องเลือกทำกับเชื้อชนิดเดียวหรือไม่ "
                 "และร่างกายสร้างมันขึ้นเองหรือได้รับมาสำเร็จรูป",
        ), IMMUNE_TOPIC)
