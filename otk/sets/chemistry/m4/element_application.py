"""การนำธาตุไปใช้ประโยชน์และผลกระทบ

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.4/8

Sets moved here from: science_wave_f20.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f20 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_USE = "การนำธาตุไปใช้ประโยชน์และผลกระทบ"


# (element, a use, an effect on living things or the environment)
ELEMENT_USES = (
    ("ซิลิคอน (Si)", "ทำชิปและเซลล์สุริยะ เพราะเป็นสารกึ่งตัวนำ", "ฝุ่นซิลิกาที่สูดเข้าไปนาน ๆ ทำให้ปอดเป็นพังผืด"),
    ("ไทเทเนียม (Ti)", "ทำโครงเครื่องบินและข้อต่อเทียม เพราะเบา แข็งแรง และไม่เป็นสนิม", "ค่อนข้างเฉื่อยและเข้ากับร่างกายได้ดี"),
    ("คลอรีน (Cl)", "ฆ่าเชื้อโรคในน้ำประปาและสระว่ายน้ำ", "แก๊สคลอรีนเป็นพิษ ระคายเคืองระบบทางเดินหายใจ"),
    ("ฟลูออรีน (F)", "ผสมในยาสีฟันเพื่อป้องกันฟันผุ", "ได้รับมากเกินไปทำให้ฟันตกกระ"),
    ("ตะกั่ว (Pb)", "ทำแผ่นขั้วแบตเตอรี่รถยนต์", "สะสมในร่างกาย ทำลายระบบประสาทโดยเฉพาะในเด็ก"),
    ("ปรอท (Hg)", "ใช้ในเทอร์โมมิเตอร์และหลอดฟลูออเรสเซนต์", "สะสมในห่วงโซ่อาหาร ทำลายระบบประสาท (โรคมินามาตะ)"),
    ("แคดเมียม (Cd)", "ทำแบตเตอรี่นิกเกิล-แคดเมียม", "สะสมในร่างกาย ทำให้กระดูกเปราะ (โรคอิไต-อิไต)"),
    ("สารหนู (As)", "ใช้ในสารกึ่งตัวนำบางชนิดและสารกำจัดศัตรูพืช", "ปนเปื้อนน้ำใต้ดิน ทำให้เกิดโรคผิวหนังและมะเร็ง"),
    ("นีออน (Ne)", "บรรจุในหลอดไฟโฆษณาให้แสงสีแดงส้ม", "เป็นแก๊สเฉื่อย ไม่ทำปฏิกิริยา"),
    ("ไนโตรเจน (N)", "ผลิตปุ๋ยแอมโมเนียและบรรจุถุงขนมกันการหืน", "ปุ๋ยที่ชะลงแหล่งน้ำทำให้สาหร่ายเติบโตมากเกินไป"),
    ("กำมะถัน (S)", "ผลิตกรดซัลฟิวริกและใช้วัลคาไนซ์ยาง", "แก๊สซัลเฟอร์ไดออกไซด์จากการเผาไหม้ทำให้เกิดฝนกรด"),
    ("ยูเรเนียม (U)", "ใช้เป็นเชื้อเพลิงในโรงไฟฟ้านิวเคลียร์", "กากกัมมันตรังสีต้องเก็บอย่างปลอดภัยเป็นเวลานาน"),
)


SAFE_USE = (
    ("ทิ้งหลอดฟลูออเรสเซนต์ที่เสียแล้วอย่างไรจึงเหมาะสม", "แยกทิ้งเป็นขยะอันตรายเพราะมีปรอท",
     ("ทุบให้แตกแล้วทิ้งรวมกับขยะทั่วไป", "เผาในที่โล่ง", "ฝังดินในสวนหลังบ้าน")),
    ("แบตเตอรี่รถยนต์ที่หมดสภาพควรจัดการอย่างไร", "ส่งคืนร้านหรือศูนย์รีไซเคิลเพราะมีตะกั่วและกรด",
     ("ทิ้งลงแม่น้ำ", "เผาทิ้ง", "ทิ้งรวมกับขยะอินทรีย์")),
    ("การใช้ปุ๋ยไนโตรเจนอย่างเหมาะสมทำอย่างไร", "ใช้ตามปริมาณที่พืชต้องการ ไม่ให้ชะล้างลงแหล่งน้ำ",
     ("ใส่ให้มากที่สุดเพื่อเร่งการเติบโต", "ใส่ก่อนฝนตกหนักทุกครั้ง", "เทลงคูน้ำโดยตรง")),
    ("การลดฝนกรดจากโรงไฟฟ้าถ่านหินทำได้อย่างไร", "ติดตั้งเครื่องกำจัดแก๊สซัลเฟอร์ไดออกไซด์ก่อนปล่อยออกสู่อากาศ",
     ("เพิ่มความสูงของปล่องเท่านั้น", "เผาถ่านหินให้มากขึ้น", "ปล่อยควันตอนกลางคืน")),
    ("ทำไมจึงห้ามใช้สีที่มีตะกั่วทาของเล่นเด็ก", "เด็กอาจอมหรือกัด ทำให้ได้รับตะกั่วซึ่งทำลายระบบประสาท",
     ("ตะกั่วทำให้สีซีดเร็ว", "ตะกั่วทำให้ของเล่นหนักเกินไป", "ตะกั่วทำให้ของเล่นไวไฟ")),
)


@question_type(
    "chem.element_application_foundation",
    display_name={"th": "การนำธาตุไปใช้ประโยชน์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_USE,
)
class ElementApplicationFoundation(QuestionType):
    """Which element does which job."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        chosen = rng.sample(ELEMENT_USES, 4)
        element, use, _ = chosen[0]
        hint = "นึกถึงสมบัติของธาตุที่ทำให้เหมาะกับงานนั้น เช่น เป็นสารกึ่งตัวนำ ไม่เป็นสนิม หรือฆ่าเชื้อโรคได้"
        if rng.random() < 0.5:
            return _labelled(stem=f"{element}นำไปใช้ประโยชน์ในข้อใด", correct=use,
                             wrongs=tuple(u for _, u, _ in chosen[1:]), topic=TOPIC_USE, hint=hint)
        return _labelled(stem=f"ธาตุใดนำไปใช้{use}", correct=element,
                         wrongs=tuple(e for e, _, _ in chosen[1:]), topic=TOPIC_USE, hint=hint)


@question_type(
    "chem.element_application_fluency",
    display_name={"th": "ผลกระทบของธาตุต่อสิ่งมีชีวิตและสิ่งแวดล้อม"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_USE,
)
class ElementApplicationFluency(QuestionType):
    """Which element causes which harm."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        chosen = rng.sample(ELEMENT_USES, 4)
        element, _, effect = chosen[0]
        hint = "โลหะหนักอย่างตะกั่ว ปรอท และแคดเมียมสะสมในร่างกาย แก๊สบางชนิดเป็นพิษหรือทำให้เกิดฝนกรด"
        if rng.random() < 0.5:
            return _labelled(stem=f"ข้อใดเป็นผลกระทบของ{element}", correct=effect,
                             wrongs=tuple(e for _, _, e in chosen[1:]), topic=TOPIC_USE, hint=hint)
        return _labelled(stem=f"ผลกระทบ \"{effect}\" เกิดจากธาตุใด", correct=element,
                         wrongs=tuple(e for e, _, _ in chosen[1:]), topic=TOPIC_USE, hint=hint)


@question_type(
    "chem.element_application_application",
    display_name={"th": "การใช้และกำจัดธาตุอย่างปลอดภัยและเหมาะสม"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_USE,
)
class ElementApplicationApplication(QuestionType):
    """Using and disposing of elements so the harm is avoided."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            stem, correct, wrongs = rng.choice(SAFE_USE)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_USE,
                             hint="ลดการปล่อยธาตุอันตรายสู่สิ่งแวดล้อม แยกขยะอันตราย และใช้ในปริมาณที่เหมาะสม")
        chosen = rng.sample(ELEMENT_USES, 4)
        element, use, effect = chosen[0]
        return _labelled(stem=f"ธาตุที่ใช้{use} แต่ {effect} คือธาตุใด", correct=element,
                         wrongs=tuple(e for e, _, _ in chosen[1:]), topic=TOPIC_USE,
                         hint="จับคู่ทั้งประโยชน์และผลกระทบของธาตุเดียวกัน")
