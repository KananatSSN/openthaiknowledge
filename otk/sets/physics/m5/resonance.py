"""ความถี่ธรรมชาติ การสั่นพ้อง และผลของการสั่นพ้อง

ฟิสิกส์ · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.5/4

Sets moved here from: science_wave_e13.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e13 import SUBJECT, UPPER_FIVE, _labelled, show

PROVENANCE = Provenance("original")


TOPIC_RESONANCE = "ความถี่ธรรมชาติ การสั่นพ้อง และผลของการสั่นพ้อง"


NATURAL, RESONANCE, EFFECT = "ความถี่ธรรมชาติ", "การสั่นพ้อง", "ผลของการสั่นพ้อง"


RESONANCE_TRUE = (
    ("วัตถุแต่ละชนิดมีความถี่ธรรมชาติเฉพาะตัว ซึ่งขึ้นกับสมบัติ เช่น ขนาด มวล และความยาว", NATURAL),
    ("ลูกตุ้มที่สายยาวกว่ามีความถี่ธรรมชาติต่ำกว่าลูกตุ้มที่สายสั้นกว่า", NATURAL),
    ("การสั่นพ้องเกิดเมื่อแรงกระตุ้นมีความถี่เท่ากับความถี่ธรรมชาติของวัตถุ", RESONANCE),
    ("ขณะเกิดการสั่นพ้อง วัตถุสั่นด้วยแอมพลิจูดมากที่สุด", RESONANCE),
    ("การผลักชิงช้าให้ตรงจังหวะการแกว่ง ทำให้ชิงช้าแกว่งสูงขึ้นเรื่อย ๆ", RESONANCE),
    ("ทหารเดินข้ามสะพานต้องเดินไม่พร้อมเท้า เพื่อไม่ให้สะพานสั่นพ้องจนเสียหาย", EFFECT),
    ("เสียงร้องที่มีความถี่เท่ากับความถี่ธรรมชาติของแก้วไวน์ อาจทำให้แก้วแตกได้", EFFECT),
    ("การปรับเครื่องรับวิทยุให้รับสถานีที่ต้องการ อาศัยการสั่นพ้องทางไฟฟ้า", EFFECT),
)


RESONANCE_FALSE = (
    "วัตถุทุกชนิดมีความถี่ธรรมชาติเท่ากัน",
    "การสั่นพ้องเกิดเมื่อแรงกระตุ้นมีแอมพลิจูดมากที่สุด ไม่เกี่ยวกับความถี่",
    "ลูกตุ้มที่สายยาวกว่ามีความถี่ธรรมชาติสูงกว่า",
    "การผลักชิงช้าเร็ว ๆ โดยไม่สนใจจังหวะ ทำให้ชิงช้าแกว่งสูงที่สุด",
    "การสั่นพ้องไม่มีผลเสียต่อสิ่งก่อสร้าง",
    "ขณะเกิดการสั่นพ้อง วัตถุหยุดสั่น",
    "ความถี่ธรรมชาติของวัตถุเปลี่ยนไปตามแรงที่ใช้ผลัก",
)


@question_type(
    "phys.resonance_foundation",
    display_name={"th": "ความหมายของความถี่ธรรมชาติและการสั่นพ้อง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_RESONANCE,
)
class ResonanceFoundation(QuestionType):
    """The two definitions, and the one variable a pendulum's natural frequency hangs on."""

    DEFINITIONS = (
        ("ความถี่ธรรมชาติของวัตถุหมายถึงข้อใด",
         "ความถี่ที่วัตถุสั่นเองเมื่อถูกทำให้สั่นแล้วปล่อยให้สั่นอิสระ",
         ("ความถี่ของแรงที่ใช้ผลักวัตถุ", "ความถี่สูงสุดที่หูมนุษย์ได้ยิน", "ความถี่ของไฟฟ้ากระแสสลับ")),
        ("การสั่นพ้องหมายถึงข้อใด",
         "การที่วัตถุสั่นแรงที่สุดเมื่อถูกกระตุ้นด้วยความถี่เท่ากับความถี่ธรรมชาติของวัตถุ",
         ("การที่วัตถุสองชิ้นสั่นด้วยแอมพลิจูดเท่ากัน", "การที่วัตถุหยุดสั่นเมื่อถูกกระตุ้น",
          "การที่คลื่นสะท้อนกลับจากผนัง")),
    )

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = "ความถี่ธรรมชาติเป็นสมบัติของวัตถุ การสั่นพ้องเกิดเมื่อกระตุ้นด้วยความถี่เท่ากับความถี่ธรรมชาตินั้น"
        if rng.random() < 0.4:
            stem, correct, wrongs = rng.choice(self.DEFINITIONS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_RESONANCE, hint=hint)
        lengths = sorted(rng.sample((20, 30, 40, 50, 60, 80, 100, 120), 4))
        highest = rng.random() < 0.5
        answer = lengths[0] if highest else lengths[-1]
        return _labelled(
            stem=(f"ลูกตุ้มอย่างง่ายสี่อันมีความยาวสาย {', '.join(map(str, lengths))} เซนติเมตร "
                  f"ลูกตุ้มที่ยาวเท่าใดมีความถี่ธรรมชาติ{'สูง' if highest else 'ต่ำ'}ที่สุด"),
            correct=f"{answer} เซนติเมตร",
            wrongs=tuple(f"{x} เซนติเมตร" for x in lengths if x != answer),
            topic=TOPIC_RESONANCE,
            hint="ลูกตุ้มสายสั้นแกว่งเร็ว (ความถี่สูง) ลูกตุ้มสายยาวแกว่งช้า (ความถี่ต่ำ)")


@question_type(
    "phys.resonance_fluency",
    display_name={"th": "อธิบายความถี่ธรรมชาติ การสั่นพ้อง และผลของการสั่นพ้อง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_RESONANCE,
)
class ResonanceFluency(QuestionType):
    """The indicator across its three objects: one true account among three wrong ones."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        statement, _ = rng.choice(RESONANCE_TRUE)
        return _labelled(
            stem="ข้อใดกล่าวถึงความถี่ธรรมชาติและการสั่นพ้องได้ถูกต้อง",
            correct=statement, wrongs=tuple(RESONANCE_FALSE),
            topic=TOPIC_RESONANCE,
            hint="การสั่นพ้องต้องการความถี่ที่ตรงกัน ไม่ใช่แรงที่มาก")


@question_type(
    "phys.resonance_application",
    display_name={"th": "ใช้การสั่นพ้องกับลูกตุ้มบาร์ตัน ชิงช้า และแก้ว"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_RESONANCE,
)
class ResonanceApplication(QuestionType):
    """Which pendulum picks up the driver's swing, when to push a swing, what shatters a glass."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(3)
        if shape == 0:
            lengths = rng.sample((20, 30, 40, 50, 60, 70, 80, 90), 4)
            driver = rng.choice(lengths)
            labels = ("ก", "ข", "ค", "ง")
            listing = " ".join(f"ลูกตุ้ม {lab} ยาว {x} เซนติเมตร" for lab, x in zip(labels, lengths))
            answer = labels[lengths.index(driver)]
            return _labelled(
                stem=(f"แขวนลูกตุ้มสี่อันบนเชือกเส้นเดียวกัน: {listing} แล้วแกว่งลูกตุ้มตัวขับที่ยาว "
                      f"{driver} เซนติเมตรบนเชือกเส้นเดียวกัน ลูกตุ้มใดแกว่งด้วยแอมพลิจูดมากที่สุด"),
                correct=f"ลูกตุ้ม {answer}",
                wrongs=tuple(f"ลูกตุ้ม {lab}" for lab in labels if lab != answer),
                topic=TOPIC_RESONANCE,
                hint="ลูกตุ้มที่ยาวเท่ากับตัวขับมีความถี่ธรรมชาติเท่ากับความถี่ของแรงกระตุ้น จึงเกิดการสั่นพ้อง")
        if shape == 1:
            period = rng.choice((2, 3, 4, 5))
            wrongs = list(dict.fromkeys(x for x in (Fraction(period, 2), Fraction(period + 1),
                                                    Fraction(period * 3, 2), Fraction(period, 4),
                                                    Fraction(2 * period + 1, 2)) if x != period))[:3]
            return _labelled(
                stem=(f"ชิงช้าแกว่งไป-กลับครบหนึ่งรอบใช้เวลา {period} วินาที ควรผลักชิงช้าทุก ๆ กี่วินาที "
                      "(ช่วงสั้นที่สุด) เพื่อให้ชิงช้าแกว่งสูงขึ้นเรื่อย ๆ"),
                correct=f"{period} วินาที",
                wrongs=tuple(f"{show(x)} วินาที" for x in wrongs),
                topic=TOPIC_RESONANCE,
                hint="ผลักให้ตรงจังหวะการแกว่ง คือทุก ๆ หนึ่งคาบ ความถี่ของแรงกระตุ้นจึงเท่ากับความถี่ธรรมชาติ")
        f = rng.choice((400, 500, 600, 700, 800, 900, 1000, 1200))
        return _labelled(
            stem=(f"แก้วใบหนึ่งมีความถี่ธรรมชาติ {f:,} เฮิรตซ์ เสียงความถี่เท่าใดมีโอกาสทำให้แก้ว"
                  "สั่นพ้องจนแตกได้มากที่สุด ถ้าความดังเท่ากัน"),
            correct=f"{f:,} เฮิรตซ์",
            wrongs=(f"{f // 2:,} เฮิรตซ์", f"{f + 150:,} เฮิรตซ์", f"{f * 3 // 2:,} เฮิรตซ์"),
            topic=TOPIC_RESONANCE,
            hint="การสั่นพ้องเกิดเมื่อความถี่ของเสียงเท่ากับความถี่ธรรมชาติของแก้ว")
