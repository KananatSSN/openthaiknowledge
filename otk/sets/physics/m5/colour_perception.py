"""การมองเห็นสี สีของวัตถุ การผสมสารสีและแสงสี และการบอดสี

ฟิสิกส์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 2 ม.5/13

Sets moved here from: science_wave_f9.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_e15 import COLOUR_NAME, LIGHT_NAME, PIGMENTS, B, R
from otk.sets._support.science_wave_e15 import G as GREEN
from otk.sets._support.science_wave_f9 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_COLOUR = "การมองเห็นสี สีของวัตถุ การผสมสารสีและแสงสี และการบอดสี"


WHITE = frozenset({R, GREEN, B})


CONES = {R: "เซลล์รูปกรวยที่ไวต่อแสงสีแดง", GREEN: "เซลล์รูปกรวยที่ไวต่อแสงสีเขียว",
         B: "เซลล์รูปกรวยที่ไวต่อแสงสีน้ำเงิน"}


COLOUR_FACTS = (
    ("เซลล์รับแสงชนิดใดในจอตาทำให้มองเห็นสีได้", "เซลล์รูปกรวย",
     ("เซลล์รูปแท่ง", "เซลล์ประสาทตาทุกชนิดเท่ากัน", "เลนส์ตา")),
    ("เซลล์รูปกรวยในจอตาของคนมีกี่ชนิด", "สามชนิด ไวต่อแสงสีแดง สีเขียว และสีน้ำเงิน",
     ("ชนิดเดียว ไวต่อแสงทุกสีเท่ากัน", "สองชนิด ไวต่อแสงสีขาวและสีดำเท่านั้น", "เจ็ดชนิด ตามสีของรุ้ง แต่ละชนิดไวต่อสีเดียว")),
    ("การบอดสีเกิดจากสาเหตุใด", "เซลล์รูปกรวยบางชนิดขาดไปหรือทำงานบกพร่อง",
     ("เลนส์ตาขุ่น", "เซลล์รูปแท่งมีมากเกินไป", "จอตาไม่รับแสงเลย")),
    ("ตาบอดสีแดง-เขียวพบในเพศชายมากกว่าเพศหญิง เพราะเหตุใด", "ยีนอยู่บนโครโมโซม X ซึ่งเพศชายมีเพียงแท่งเดียว",
     ("เพศชายมีเซลล์รูปแท่งน้อยกว่าเพศหญิง", "เพศชายใช้สายตามากกว่า", "ยีนอยู่บนโครโมโซม Y ซึ่งมีเฉพาะในเพศชาย")),
    ("แสงสีปฐมภูมิสามสีคือข้อใด", "แสงสีแดง แสงสีเขียว และแสงสีน้ำเงิน",
     ("แสงสีแดง แสงสีเหลือง และแสงสีน้ำเงิน", "แสงสีเหลือง แสงสีฟ้า และแสงสีแดงม่วง", "แสงสีขาว แสงสีดำ และแสงสีเทา")),
    ("สารสีปฐมภูมิที่ใช้ในเครื่องพิมพ์สีคือข้อใด", "สีฟ้า (ไซแอน) สีแดงม่วง (มาเจนตา) และสีเหลือง",
     ("สีแดง สีเขียว และสีน้ำเงิน", "สีขาว สีดำ และสีเทา", "สีแดง สีส้ม และสีเหลือง")),
)


def _bare(name: str) -> str:
    return name.split(" (")[0]


def _others(correct: str, rng: Random) -> tuple[str, ...]:
    """Three other colour names, one of them as long as the answer.

    "สีแดงม่วง (มาเจนตา)" is twice as long as "สีขาว"; a random three would let
    the length of the answer point to it.
    """
    names = [n for n in COLOUR_NAME.values() if n != correct]
    closest = min(names, key=lambda n: (abs(len(n) - len(correct)), rng.random()))
    return (closest, *rng.sample([n for n in names if n != closest], 2))


@question_type(
    "phys.colour_perception_foundation",
    display_name={"th": "การมองเห็นสี เซลล์รูปกรวย และการผสมแสงสี"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_COLOUR,
)
class ColourPerceptionFoundation(QuestionType):
    """The three cones, and lights adding up."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            stem, correct, wrongs = rng.choice(COLOUR_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_COLOUR,
                             hint="ตามีเซลล์รูปกรวยสามชนิด สมองแปลสัดส่วนการกระตุ้นของทั้งสามเป็นสี")
        count = rng.choice((2, 2, 3))
        lights = rng.sample([c for c in COLOUR_NAME if c and c != WHITE], count)
        total = frozenset().union(*lights)
        listed = " ".join(LIGHT_NAME[c] for c in lights)
        correct = COLOUR_NAME[total]
        # Names without the bracketed loan words, which only two colours carry.
        return _labelled(stem=f"ฉาย{listed}ซ้อนกันบนฉากสีขาว บริเวณที่แสงซ้อนกันเห็นเป็นสีใด",
                         correct=_bare(correct), wrongs=tuple(_bare(n) for n in _others(correct, rng)), topic=TOPIC_COLOUR,
                         hint="แสงสีรวมกันแบบบวก: แดง + เขียว = เหลือง เขียว + น้ำเงิน = ฟ้า แดง + น้ำเงิน = แดงม่วง ครบสามสี = ขาว")


@question_type(
    "phys.colour_perception_fluency",
    display_name={"th": "การผสมสารสีและสีของวัตถุภายใต้แสงสี"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_COLOUR,
)
class ColourPerceptionFluency(QuestionType):
    """Pigments keep only what every one of them reflects; a lit object keeps what it reflects of the light."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            names = rng.sample(list(PIGMENTS), rng.choice((2, 2, 3)))
            reflected = frozenset.intersection(*(PIGMENTS[n] for n in names))
            correct = COLOUR_NAME[reflected]
            return _labelled(stem=f"ผสมสาร{'กับสาร'.join(names)}ในปริมาณเท่ากัน ดูภายใต้แสงขาว เห็นเป็นสีใด",
                             correct=correct, wrongs=_others(correct, rng), topic=TOPIC_COLOUR,
                             hint="สารสีแต่ละชนิดดูดกลืนแสงบางสี สารผสมสะท้อนเฉพาะแสงที่ทุกสารสะท้อนร่วมกัน")
        body = rng.choice([c for c in COLOUR_NAME if c])
        light = rng.choice([c for c in COLOUR_NAME if c and c != WHITE])
        thing = rng.choice(("เสื้อ", "ลูกบอล", "กระดาษ", "ร่ม", "หมวก"))
        correct = COLOUR_NAME[body & light]
        return _labelled(stem=f"{thing}ที่เห็นเป็น{COLOUR_NAME[body]}ในแสงขาว เมื่อนำไปไว้ใต้{LIGHT_NAME[light]} จะเห็นเป็นสีใด",
                         correct=correct, wrongs=_others(correct, rng), topic=TOPIC_COLOUR,
                         hint="วัตถุสะท้อนเฉพาะแสงสีของตัวเอง ถ้าแสงที่ส่องไม่มีสีนั้นเลยจะเห็นเป็นสีดำ")


@question_type(
    "phys.colour_perception_application",
    display_name={"th": "การบอดสีและการเลือกแสงสีหรือสารสีให้ได้สีที่ต้องการ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_COLOUR,
)
class ColourPerceptionApplication(QuestionType):
    """Which cone is missing, which light to add, and a stage lit to hide a colour."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        if shape == 0:
            missing = rng.choice((R, GREEN, B))
            confused = {R: "สีแดงกับสีเขียว", GREEN: "สีแดงกับสีเขียว", B: "สีน้ำเงินกับสีเหลือง"}[missing]
            weak = {R: "แสงสีแดง", GREEN: "แสงสีเขียว", B: "แสงสีน้ำเงิน"}[missing]
            return _labelled(
                stem=f"คนที่มองเห็น{weak}ได้ไม่ชัดและแยก{confused}ได้ยาก น่าจะขาดเซลล์ชนิดใด",
                correct=CONES[missing],
                wrongs=(*(CONES[c] for c in (R, GREEN, B) if c != missing), "เซลล์รูปแท่ง"),
                topic=TOPIC_COLOUR, hint="แต่ละสีปฐมภูมิถูกรับด้วยเซลล์รูปกรวยชนิดหนึ่ง ขาดชนิดใดก็รับสีนั้นไม่ได้")
        if shape == 1:
            start = rng.choice([c for c in COLOUR_NAME if c and len(c) == 1])
            target = rng.choice([c for c in COLOUR_NAME if len(c) == 2 and start < c])
            add = target - start
            correct = LIGHT_NAME[add]
            return _labelled(
                stem=f"ฉาย{LIGHT_NAME[start]}บนฉากสีขาว ต้องฉายแสงสีใดเพิ่มอีกหนึ่งสีจึงเห็นเป็น{COLOUR_NAME[target]}",
                correct=correct,
                wrongs=tuple([LIGHT_NAME[c] for c in COLOUR_NAME if c and c != add and c != WHITE]),
                topic=TOPIC_COLOUR, hint="แสงสีรวมกันแบบบวก หาแสงปฐมภูมิที่ยังขาดให้ครบตามสีที่ต้องการ")
        body = rng.choice([c for c in COLOUR_NAME if c and c != WHITE])
        # The light that makes this object look black: none of what it reflects.
        dark = [c for c in COLOUR_NAME if c and not (c & body)]
        light = rng.choice(dark)
        return _labelled(
            stem=f"บนเวทีต้องการให้ชุดที่เห็นเป็น{COLOUR_NAME[body]}ในแสงขาวดูเป็นสีดำ ควรส่องด้วยแสงสีใด",
            correct=LIGHT_NAME[light],
            wrongs=tuple([LIGHT_NAME[c] for c in COLOUR_NAME if c and c & body]),
            topic=TOPIC_COLOUR, hint="วัตถุดูเป็นสีดำเมื่อแสงที่ส่องไม่มีแสงสีที่วัตถุสะท้อนเลย")
