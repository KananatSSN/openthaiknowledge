"""การทำงานของระบบหมุนเวียนเลือด

ชีวะ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 1.2 ม.2/7

Sets moved here from: science_wave_b10.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import LEVEL, SUBJECT, TOPIC, labelled, scenario_question
from otk.sets._support.science_wave_b10 import CIRCULATION_MODEL_SCENARIOS
from otk.sets._support.life_earth_diagrams import CHAMBERS, HEART_ALT, HEARTS
from otk.sets._support.ms1_diagrams import diagram_question

PROVENANCE = Provenance("original")


# One closed loop, stored once. Every ordering and "what comes next" question
# reads it, so the two circuits can never be stated inconsistently.
BLOOD_LOOP = (
    "หัวใจห้องล่างขวา", "ปอด", "หัวใจห้องบนซ้าย", "หัวใจห้องล่างซ้าย",
    "ส่วนต่าง ๆ ของร่างกาย", "หัวใจห้องบนขวา",
)


class BloodState(NamedTuple):
    """Where blood is on the loop, and what it is carrying there."""
    place: str
    state: str


BLOOD_STATES = (
    BloodState("ในหลอดเลือดที่ออกจากหัวใจห้องล่างขวา",
               "เลือดมีออกซิเจนต่ำ และกำลังเดินทางไปยังปอด"),
    BloodState("ในหลอดเลือดที่นำเลือดจากปอดกลับสู่หัวใจ",
               "เลือดมีออกซิเจนสูง และกำลังเดินทางกลับเข้าสู่หัวใจห้องบนซ้าย"),
    BloodState("ในหลอดเลือดที่ออกจากหัวใจห้องล่างซ้าย",
               "เลือดมีออกซิเจนสูง และกำลังเดินทางไปเลี้ยงส่วนต่าง ๆ ของร่างกาย"),
    BloodState("ในหลอดเลือดที่นำเลือดจากส่วนต่าง ๆ ของร่างกายกลับสู่หัวใจ",
               "เลือดมีออกซิเจนต่ำ และกำลังเดินทางกลับเข้าสู่หัวใจห้องบนขวา"),
)


# A state and two places the loop never has, offered only as wrong choices.
STATE_DECOYS = ("เลือดไม่มีทั้งออกซิเจนและคาร์บอนไดออกไซด์เลย",
                "เลือดมีออกซิเจนสูง และกำลังเดินทางไปยังปอดเพื่อปล่อยออกซิเจน")


PLACE_DECOYS = ("ในกระเพาะอาหารระหว่างการย่อยอาหาร", "ในท่อไตระหว่างทางไปกระเพาะปัสสาวะ")


@question_type(
    "body.blood_circuit_foundation",
    display_name={"th": "ออกซิเจนในเลือดที่แต่ละช่วงของการหมุนเวียน"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class BloodCircuitFoundation(QuestionType):
    """Say what the blood is carrying at one point on the loop, or where it is."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        item = rng.choice(BLOOD_STATES)
        others = [other for other in BLOOD_STATES if other.state != item.state]
        rng.shuffle(others)
        if rng.random() < 0.5:
            return labelled(
                stem=f"{item.place} เลือดอยู่ในสภาพใด",
                correct=item.state,
                wrongs=tuple(other.state for other in others) + STATE_DECOYS,
                hint="เลือดจะมีออกซิเจนสูงหลังผ่านปอดเสมอ และมีออกซิเจนต่ำหลังผ่าน"
                     "เนื้อเยื่อของร่างกายเสมอ",
            )
        return labelled(
            stem=f"สภาพที่ว่า “{item.state}” พบได้ที่ใด",
            correct=item.place,
            wrongs=tuple(other.place for other in others) + PLACE_DECOYS,
            hint="แยกก่อนว่าเลือดกำลังออกจากหัวใจหรือกำลังกลับเข้าสู่หัวใจ "
                 "แล้วจึงดูว่าเพิ่งผ่านปอดหรือเพิ่งผ่านร่างกายมา",
        )


@question_type(
    "body.blood_circuit_fluency",
    display_name={"th": "เส้นทางการหมุนเวียนเลือดผ่านปอดและผ่านร่างกาย"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class BloodCircuitFluency(QuestionType):
    """Follow the blood all the way round the closed loop.

    ``ม.2/7`` asks how the system *works*, and the relation that carries the whole
    answer is the order: blood leaving the right ventricle must reach the lung
    before it can reach the body.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            index = rng.randrange(len(BLOOD_LOOP))
            current = BLOOD_LOOP[index]
            following = BLOOD_LOOP[(index + 1) % len(BLOOD_LOOP)]
            others = [name for name in BLOOD_LOOP if name != following]
            rng.shuffle(others)
            return labelled(
                stem=f"เลือดที่ออกจาก “{current}” จะไปถึงที่ใดต่อไป",
                correct=following,
                wrongs=tuple(others[:3]),
                hint="เลือดต้องผ่านปอดเพื่อรับออกซิเจนก่อนเสมอ จึงจะถูกส่งไปเลี้ยง"
                     "ร่างกายได้",
            )
        correct = " → ".join(BLOOD_LOOP)
        swapped = list(BLOOD_LOOP)
        swapped[1], swapped[4] = swapped[4], swapped[1]
        rotated = BLOOD_LOOP[2:] + BLOOD_LOOP[:2]
        return labelled(
            stem="ข้อใดเรียงลำดับการหมุนเวียนของเลือด โดยเริ่มจากหัวใจห้องล่างขวา "
                 "ได้ถูกต้อง",
            correct=correct,
            wrongs=(" → ".join(reversed(BLOOD_LOOP)), " → ".join(swapped),
                    " → ".join(rotated)),
            hint="อ่านข้อความที่โจทย์กำหนดจุดเริ่มต้นให้ดี แล้วไล่ตามลำดับ "
                 "ปอดก่อน ร่างกายทีหลัง",
        )


@question_type(
    "body.circulation_model_application",
    display_name={"th": "ตีความแบบจำลองและความผิดปกติของการหมุนเวียนเลือด"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class CirculationModelApplication(QuestionType):
    """Read the tubing-and-bulb model, then follow the loop into real cases.

    Two items ask about the model — what it shows and where it stops being a good
    likeness — which is as close as multiple choice gets to ``โดยใช้แบบจำลอง``.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return scenario_question(
            rng, CIRCULATION_MODEL_SCENARIOS,
            hint="ไล่ตามวงปิดทีละช่วง และถามทุกครั้งว่าเลือดช่วงนั้นเพิ่งผ่านปอด"
                 "หรือเพิ่งผ่านร่างกายมา",
        )


#: For each chamber: where its blood goes next, where it came from, and whether
#: that blood is rich in oxygen. Read off ``BLOOD_LOOP``.
CHAMBER_ROLES = {
    "หัวใจห้องบนขวา": ("หัวใจห้องล่างขวา", "ส่วนต่าง ๆ ของร่างกาย", False),
    "หัวใจห้องล่างขวา": ("ปอด", "หัวใจห้องบนขวา", False),
    "หัวใจห้องบนซ้าย": ("หัวใจห้องล่างซ้าย", "ปอด", True),
    "หัวใจห้องล่างซ้าย": ("ส่วนต่าง ๆ ของร่างกาย", "หัวใจห้องบนซ้าย", True),
}


@question_type(
    "body.heart_diagram",
    display_name={"th": "อ่านแผนภาพหัวใจและการไหลของเลือด"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class HeartDiagram(QuestionType):
    """Four numbered chambers with the loop drawn as arrows; the numbering changes between pictures.

    Name a chamber, find the chamber that sends blood to the lungs or the body,
    or say whether a chamber's blood is rich or poor in oxygen.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        spec = rng.choice(HEARTS)
        chamber = rng.choice(CHAMBERS)
        number = spec.numbers[CHAMBERS.index(chamber)]
        hint = ("ภาพมองหัวใจจากด้านหน้า ด้านซ้ายของภาพจึงเป็นซีกขวาของร่างกาย "
                "ซีกขวารับเลือดจากร่างกายแล้วส่งไปปอด ซีกซ้ายรับเลือดจากปอดแล้วส่งไปทั่วร่างกาย")
        kind = rng.randrange(3)
        if kind == 0:
            return diagram_question(
                spec.asset_id, HEART_ALT,
                stem="จากแผนภาพหัวใจ (ด้านบนคือปอด ด้านล่างคือส่วนต่าง ๆ ของร่างกาย) "
                     f"ห้องหมายเลข {number} คือห้องใด",
                correct=chamber,
                wrongs=tuple(c for c in CHAMBERS if c != chamber),
                hint=hint, topic=TOPIC,
            )
        if kind == 1:
            pumps_to = rng.choice(("ปอด", "ส่วนต่าง ๆ ของร่างกาย"))
            sender = next(c for c, (to, _, _) in CHAMBER_ROLES.items() if to == pumps_to)
            target = spec.numbers[CHAMBERS.index(sender)]
            return diagram_question(
                spec.asset_id, HEART_ALT,
                stem="จากแผนภาพหัวใจ (ด้านบนคือปอด ด้านล่างคือส่วนต่าง ๆ ของร่างกาย) "
                     f"ห้องหมายเลขใดสูบฉีดเลือดออกไปยัง{pumps_to}",
                correct=f"ห้องหมายเลข {target}",
                wrongs=tuple(f"ห้องหมายเลข {n}" for n in spec.numbers if n != target),
                hint=hint, topic=TOPIC,
            )
        rich = CHAMBER_ROLES[chamber][2]
        rich_text = "เลือดที่มีออกซิเจนสูง เพราะเพิ่งรับมาจากปอดหรือกำลังส่งไปเลี้ยงร่างกาย"
        poor_text = "เลือดที่มีออกซิเจนต่ำ เพราะเพิ่งกลับมาจากร่างกายหรือกำลังส่งไปฟอกที่ปอด"
        return diagram_question(
            spec.asset_id, HEART_ALT,
            stem="จากแผนภาพหัวใจ (ด้านบนคือปอด ด้านล่างคือส่วนต่าง ๆ ของร่างกาย) "
                 f"เลือดในห้องหมายเลข {number} เป็นเลือดแบบใด",
            correct=rich_text if rich else poor_text,
            wrongs=(poor_text if rich else rich_text,
                    "เลือดที่ไม่มีทั้งออกซิเจนและคาร์บอนไดออกไซด์เลย",
                    "เลือดที่มีออกซิเจนเท่ากันทุกห้อง เพราะหัวใจผสมเลือดทุกห้องเข้าด้วยกัน"),
            hint=hint, topic=TOPIC,
        )
