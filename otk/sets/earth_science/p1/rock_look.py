"""ลักษณะภายนอกของหิน

ธรณีวิทยา · ป.1 · สสวท. พื้นฐาน
Indicators: ว 3.2 ป.1/1

Sets moved here from: science_wave_c10.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import PRIMARY_ONE, _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c10 import LETTERS, ROCK_SCENARIOS, SUBJECT

PROVENANCE = Provenance("original")


ROCK_TOPIC = "ลักษณะภายนอกของหิน"


class Term(NamedTuple):
    """A word for something seen or felt on a rock, and what it looks like."""
    word: str
    meaning: str


TERMS = (
    Term("ผิวขรุขระ", "ลูบแล้วรู้สึกเป็นปุ่มเป็นหลุม ไม่เรียบ"),
    Term("ผิวเรียบ", "ลูบแล้วลื่นมือ ไม่มีปุ่มหรือหลุม"),
    Term("มีรูพรุน", "มีรูเล็ก ๆ จำนวนมากอยู่ทั่วทั้งก้อน"),
    Term("เป็นเงาวาว", "สะท้อนแสงเป็นประกายเมื่อหันเข้าหาแสง"),
    Term("เป็นชั้น ๆ", "เห็นเป็นแถบเรียงซ้อนกันหลายชั้น"),
    Term("เห็นเม็ดแร่", "มองเห็นเม็ดเล็ก ๆ หลายสีปนกันอยู่ในเนื้อหิน"),
)


OBSERVABLE_FACTS = (
    ("ข้อใดเป็นลักษณะภายนอกของหินที่สังเกตได้",
     "สี ผิวเรียบหรือขรุขระ และน้ำหนักของหิน",
     ("อายุของหินว่าเกิดมานานกี่ปี",
      "สถานที่ที่หินก้อนนั้นเกิดขึ้นครั้งแรก",
      "ชื่อของคนที่เก็บหินก้อนนั้นมา")),
    ("ถ้าต้องการรู้ว่าหินผิวเรียบหรือขรุขระ ควรสังเกตอย่างไร",
     "ใช้มือลูบผิวของหิน",
     ("ดมกลิ่นของหิน",
      "ฟังเสียงของหินเมื่อวางไว้เฉย ๆ",
      "ชิมรสของหิน")),
    ("ถ้าต้องการรู้ว่าหินก้อนใดหนักกว่า ควรทำอย่างไร",
     "ยกหินทั้งสองก้อนเปรียบเทียบกัน หรือนำไปชั่ง",
     ("ดูว่าหินก้อนใดมีสีเข้มกว่า",
      "ดูว่าหินก้อนใดวางอยู่ใกล้ตัวมากกว่า",
      "ดมกลิ่นว่าหินก้อนใดมีกลิ่นแรงกว่า")),
    ("ข้อใดปลอดภัยที่สุดในการสังเกตหิน",
     "ใช้ตาดูและใช้มือจับ โดยไม่นำหินเข้าปากหรือโยนเล่น",
     ("ชิมหินเพื่อดูว่ามีรสอะไร",
      "โยนหินใส่กันเพื่อดูว่าแข็งหรือไม่",
      "ทุบหินด้วยมือเปล่าให้แตก")),
)


class Rock(NamedTuple):
    """One observed rock. No two rows share a colour, a surface or a feature."""
    colour: str
    surface: str
    feature: str


ROCKS = (
    Rock("สีเทาอ่อน", "ผิวขรุขระ", "มีรูพรุนทั่วทั้งก้อนและลอยน้ำได้"),
    Rock("สีขาว", "ผิวเรียบลื่น", "ขัดแล้วเป็นเงามัน"),
    Rock("สีน้ำตาลอ่อน", "ผิวสาก", "ลูบแล้วมีเม็ดทรายหลุดติดมือ"),
    Rock("สีเทาเข้ม", "ผิวเรียบด้าน", "แตกออกเป็นแผ่นบาง ๆ ได้"),
    Rock("สีชมพูมีจุดเข้มกระจาย", "ผิวแข็งมาก", "เห็นเม็ดแร่หลายสีชัดเจน"),
    Rock("สีดำ", "ผิวมันวาวคล้ายแก้ว", "ขอบที่แตกคมมาก"),
)


def _describe(rock: Rock) -> str:
    return f"{rock.colour} {rock.surface} {rock.feature}"


def rock_record(rocks: list[Rock]) -> str:
    return " / ".join(f"หิน {letter}: {_describe(rock)}"
                      for letter, rock in zip(LETTERS, rocks))


@question_type(
    "geo.rock_look_foundation",
    display_name={"th": "คำบอกลักษณะภายนอกของหิน"},
    level=PRIMARY_ONE, subject=SUBJECT, topic=ROCK_TOPIC,
)
class RockLookFoundation(QuestionType):
    """Know the words for what a rock looks and feels like, and how to observe."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        draw = rng.random()
        if draw < 0.3:
            return _retopic(scenario_question(
                rng, OBSERVABLE_FACTS,
                hint="ลักษณะภายนอกคือสิ่งที่เราใช้ตาดูหรือใช้มือสัมผัสได้",
            ), ROCK_TOPIC)
        term = rng.choice(TERMS)
        others = [other for other in TERMS if other.word != term.word]
        if draw < 0.65:
            return _labelled(
                stem=f"หินที่“{term.word}” มีลักษณะอย่างไร",
                correct=term.meaning,
                wrongs=tuple(other.meaning for other in others),
                hint="นึกภาพว่าถ้าใช้ตาดูหรือใช้มือลูบ จะเห็นหรือรู้สึกอย่างไร",
                topic=ROCK_TOPIC,
            )
        return _labelled(
            stem=f"หินที่{term.meaning} เรียกว่ามีลักษณะอย่างไร",
            correct=term.word,
            wrongs=tuple(other.word for other in others),
            hint="นึกภาพว่าถ้าใช้ตาดูหรือใช้มือลูบ จะเห็นหรือรู้สึกอย่างไร",
            topic=ROCK_TOPIC,
        )


@question_type(
    "geo.rock_look_fluency",
    display_name={"th": "บรรยายลักษณะหินจากบันทึกการสังเกต"},
    level=PRIMARY_ONE, subject=SUBJECT, topic=ROCK_TOPIC,
)
class RockLookFluency(QuestionType):
    """Read an observation record of four rocks and answer from it alone."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        rocks = rng.sample(ROCKS, 4)
        record = f"บันทึกการสังเกตหิน 4 ก้อน — {rock_record(rocks)}"
        index = rng.randrange(4)
        rock = rocks[index]
        draw = rng.random()
        if draw < 0.35:
            return _labelled(
                stem=f"{record} จากบันทึกนี้ หินก้อนใด{rock.feature}",
                correct=f"หิน {LETTERS[index]}",
                wrongs=tuple(f"หิน {letter}" for letter in LETTERS if letter != LETTERS[index]),
                hint="หาคำในคำถามจากบันทึก แล้วดูว่าอยู่ในแถวของหินก้อนใด",
                topic=ROCK_TOPIC,
            )
        if draw < 0.7:
            return _labelled(
                stem=f"{record} จากบันทึกนี้ หินก้อนใดมี{rock.colour}และ{rock.surface}",
                correct=f"หิน {LETTERS[index]}",
                wrongs=tuple(f"หิน {letter}" for letter in LETTERS if letter != LETTERS[index]),
                hint="หาสีและผิวที่ถามในบันทึก แล้วดูว่าอยู่ในแถวของหินก้อนใด",
                topic=ROCK_TOPIC,
            )
        return _labelled(
            stem=f"{record} จากบันทึกนี้ หิน {LETTERS[index]} มีลักษณะภายนอกอย่างไร",
            correct=_describe(rock),
            wrongs=tuple(_describe(other) for other in rocks if other != rock),
            hint="อ่านเฉพาะแถวของหินก้อนที่ถาม",
            topic=ROCK_TOPIC,
        )


@question_type(
    "geo.rock_look_application",
    display_name={"th": "ใช้ลักษณะภายนอกของหินในสถานการณ์จริง"},
    level=PRIMARY_ONE, subject=SUBJECT, topic=ROCK_TOPIC,
)
class RockLookApplication(QuestionType):
    """Tell rocks apart fairly, and choose a rock for a job by how it looks and feels."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, ROCK_SCENARIOS,
            hint="นึกว่าลักษณะใดของหินที่เกี่ยวกับเรื่องที่ถาม",
        ), ROCK_TOPIC)
