"""ปัจจัยที่มีผลต่ออัตราการเกิดปฏิกิริยาเคมีในชีวิตประจำวันและอุตสาหกรรม

เคมี · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.5/22

Sets moved here from: science_wave_e8.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple, Optional

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e8 import (
    CATALYST,
    CONCENTRATION,
    FACTORS,
    FASTER,
    SLOWER,
    SUBJECT,
    SURFACE,
    TEMPERATURE,
    UPPER_FIVE,
    _labelled,
)

PROVENANCE = Provenance("original")


TOPIC_RATE_USE = "ปัจจัยที่มีผลต่ออัตราการเกิดปฏิกิริยาเคมีในชีวิตประจำวันและอุตสาหกรรม"


class RateUse(NamedTuple):
    situation: str
    process: str        # the reaction being sped up or slowed down
    factor: str
    faster: bool


RATE_USES: tuple[RateUse, ...] = (
    RateUse("เก็บอาหารสดไว้ในตู้เย็น", "ปฏิกิริยาที่ทำให้อาหารเน่าเสีย", TEMPERATURE, False),
    RateUse("ขนส่งผลไม้ด้วยรถห้องเย็น", "ปฏิกิริยาที่ทำให้ผลไม้สุกงอมและเน่า", TEMPERATURE, False),
    RateUse("เก็บยาบางชนิดไว้ในตู้เย็นตามที่ฉลากกำหนด", "ปฏิกิริยาการสลายตัวของตัวยา", TEMPERATURE, False),
    RateUse("ใช้หม้อความดันต้มเนื้อสัตว์ให้เปื่อยเร็ว", "ปฏิกิริยาที่ทำให้เนื้อสัตว์เปื่อยนุ่ม", TEMPERATURE, True),
    RateUse("อบขนมในเตาที่มีอุณหภูมิสูง", "ปฏิกิริยาที่ทำให้ผิวขนมสุกและเปลี่ยนเป็นสีน้ำตาล", TEMPERATURE, True),
    RateUse("โรงงานผลิตแอมโมเนียเดินเครื่องที่อุณหภูมิประมาณ 450 องศาเซลเซียส",
            "ปฏิกิริยาระหว่างแก๊สไนโตรเจนกับแก๊สไฮโดรเจน", TEMPERATURE, True),
    RateUse("ผ่าฟืนเป็นชิ้นเล็กก่อนก่อไฟ", "การเผาไหม้ของไม้", SURFACE, True),
    RateUse("เคี้ยวอาหารให้ละเอียดก่อนกลืน", "การย่อยอาหารด้วยเอนไซม์", SURFACE, True),
    RateUse("ยาลดกรดชนิดผงออกฤทธิ์ได้เร็วกว่าชนิดเม็ด", "ปฏิกิริยาสะเทินกรดในกระเพาะอาหาร", SURFACE, True),
    RateUse("ฝุ่นแป้งที่ฟุ้งกระจายในโรงงานอาจลุกไหม้จนเกิดระเบิดได้", "การเผาไหม้ของแป้ง", SURFACE, True),
    RateUse("ใช้ถ่านก้อนใหญ่ในเตาเพื่อให้ไฟลุกไหม้อย่างช้า ๆ และได้นาน", "การเผาไหม้ของถ่าน", SURFACE, False),
    RateUse("ใช้ไม้ท่อนใหญ่ทำฟืนเพื่อให้ไฟค่อย ๆ ลุกไหม้ตลอดคืน", "การเผาไหม้ของไม้", SURFACE, False),
    RateUse("พัดหรือเป่าลมเข้าเตาถ่านเพื่อเพิ่มแก๊สออกซิเจนให้ไฟลุกแรงขึ้น", "การเผาไหม้ของถ่าน", CONCENTRATION, True),
    RateUse("ใช้แก๊สออกซิเจนบริสุทธิ์แทนอากาศในหัวเชื่อมโลหะ", "การเผาไหม้ของแก๊สเชื้อเพลิง", CONCENTRATION, True),
    RateUse("ใช้น้ำยาล้างห้องน้ำชนิดเข้มข้นขจัดคราบหินปูนได้เร็วกว่าชนิดเจือจาง",
            "ปฏิกิริยาระหว่างกรดกับคราบหินปูน", CONCENTRATION, True),
    RateUse("บรรจุขนมขบเคี้ยวในถุงที่เติมแก๊สไนโตรเจนแทนอากาศ",
            "ปฏิกิริยาที่ทำให้น้ำมันในขนมเหม็นหืน", CONCENTRATION, False),
    RateUse("เก็บอาหารแห้งในถุงสุญญากาศ", "ปฏิกิริยาที่ทำให้อาหารเสื่อมเสียซึ่งต้องใช้แก๊สออกซิเจน",
            CONCENTRATION, False),
    RateUse("ใช้ผงซักฟอกที่มีเอนไซม์ขจัดคราบโปรตีน", "การย่อยสลายคราบโปรตีน", CATALYST, True),
    RateUse("ติดตั้งเครื่องกรองไอเสียที่มีโลหะแพลทินัมในรถยนต์",
            "ปฏิกิริยาที่เปลี่ยนแก๊สพิษในไอเสียเป็นแก๊สที่เป็นพิษน้อยลง", CATALYST, True),
    RateUse("โรงงานผลิตแอมโมเนียใช้เหล็กในกระบวนการฮาเบอร์",
            "ปฏิกิริยาระหว่างแก๊สไนโตรเจนกับแก๊สไฮโดรเจน", CATALYST, True),
    RateUse("โรงงานผลิตกรดซัลฟิวริกใช้วาเนเดียม(V)ออกไซด์",
            "ปฏิกิริยาที่เปลี่ยนแก๊สซัลเฟอร์ไดออกไซด์เป็นแก๊สซัลเฟอร์ไตรออกไซด์", CATALYST, True),
)


# What the method itself does, so a wrong choice is a false claim about the
# method rather than a true fact that merely does not apply.
METHOD_PHRASE = {
    (TEMPERATURE, True): "ทำให้อุณหภูมิสูงขึ้น",
    (TEMPERATURE, False): "ทำให้อุณหภูมิต่ำลง",
    (SURFACE, True): "ทำให้สารมีพื้นที่ผิวมากขึ้น",
    (SURFACE, False): "ทำให้สารมีพื้นที่ผิวน้อยลง",
    (CONCENTRATION, True): "ทำให้ความเข้มข้นของสารตั้งต้นมากขึ้น",
    (CONCENTRATION, False): "ทำให้ความเข้มข้นของสารตั้งต้นลดลง",
    (CATALYST, True): "ใช้ตัวเร่งปฏิกิริยา",
}


def _use_explanation(factor: str, faster: bool, process: str, *,
                     result: Optional[bool] = None) -> str:
    result = faster if result is None else result
    return f"วิธีนี้{METHOD_PHRASE[(factor, faster)]} {process}จึง{FASTER if result else SLOWER}"


def _clear_alternatives(use: RateUse) -> list[str]:
    """Other factors that are plainly not what this method does. A fire that
    burns faster also gets hotter, so temperature is never offered as the wrong
    reason for a combustion item."""
    return [f for f in FACTORS
            if f != use.factor and (f, use.faster) in METHOD_PHRASE
            and not (f == TEMPERATURE and "เผาไหม้" in use.process)]


@question_type(
    "chem.rate_use_foundation",
    display_name={"th": "สถานการณ์ในชีวิตประจำวันใช้ปัจจัยใดควบคุมอัตราการเกิดปฏิกิริยา"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_RATE_USE,
)
class RateUseFoundation(QuestionType):
    """Name the factor a situation uses."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        use = rng.choice(RATE_USES)
        if rng.random() < 0.4:
            correct = f"ทำให้{use.process}{FASTER if use.faster else SLOWER}"
            return _labelled(
                stem=f"\"{use.situation}\" วิธีนี้มีจุดประสงค์ให้ปฏิกิริยาใดเกิดเร็วขึ้นหรือช้าลง",
                correct=correct,
                wrongs=(f"ทำให้{use.process}{SLOWER if use.faster else FASTER}",
                        f"ทำให้{use.process}หยุดเกิดทันทีและไม่กลับมาเกิดอีก",
                        "ไม่มีผลต่อปฏิกิริยาเคมีใดเลย"),
                topic=TOPIC_RATE_USE,
                hint="ถามว่าผู้ใช้วิธีนี้ต้องการผลอะไร เช่น อาหารเก็บได้นานขึ้น หรือได้ผลิตภัณฑ์เร็วขึ้น",
            )
        return _labelled(
            stem=f"\"{use.situation}\" เป็นการใช้ปัจจัยใดควบคุมอัตราการเกิดปฏิกิริยาเคมี",
            correct=use.factor, wrongs=tuple(f for f in FACTORS if f != use.factor),
            topic=TOPIC_RATE_USE,
            hint="ถามว่าวิธีนี้เปลี่ยนความร้อน ขนาดของชิ้นสาร ปริมาณสารที่ทำปฏิกิริยา หรือเติมสารที่ช่วยเร่ง",
        )


@question_type(
    "chem.rate_use_fluency",
    display_name={"th": "อธิบายการใช้ปัจจัยที่มีผลต่ออัตราการเกิดปฏิกิริยาในชีวิตประจำวันและอุตสาหกรรม"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_RATE_USE,
)
class RateUseFluency(QuestionType):
    """The indicator's verb, อธิบาย: which factor, which way, on which reaction."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        use = rng.choice(RATE_USES)
        correct = _use_explanation(use.factor, use.faster, use.process)
        # The right factor with the wrong result, and a factor the method does not touch.
        backwards = _use_explanation(use.factor, use.faster, use.process, result=not use.faster)
        alternatives = _clear_alternatives(use)
        other = rng.choice(alternatives)
        # Spares that differ from the answer in more than one part, so it is
        # not the choice every wrong agrees on. A factor the method does not
        # touch makes the choice false whichever way it says the rate goes.
        spares = [_use_explanation(other, use.faster, use.process, result=not use.faster)]
        spares += [_use_explanation(f, use.faster, use.process) for f in alternatives if f != other][:1]
        wrongs = (
            backwards,
            _use_explanation(other, use.faster, use.process),
            "วิธีนี้ไม่เกี่ยวกับอัตราการเกิดปฏิกิริยา เป็นเพียงการเปลี่ยนสถานะของสาร",
            *spares,
        )
        return _labelled(
            stem=f"\"{use.situation}\" ข้อใดอธิบายเหตุผลได้ถูกต้อง",
            correct=correct, wrongs=wrongs,
            topic=TOPIC_RATE_USE,
            hint="ระบุให้ได้ทั้งปัจจัยที่ใช้ และทิศทาง: วิธีนี้ต้องการให้ปฏิกิริยาเกิดเร็วขึ้นหรือช้าลง",
        )


@question_type(
    "chem.rate_use_application",
    display_name={"th": "สถานการณ์ใดใช้หลักการควบคุมอัตราการเกิดปฏิกิริยาแบบเดียวกัน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_RATE_USE,
)
class RateUseApplication(QuestionType):
    """Transfer: find another situation that uses the same factor the same way."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        paired = [u for u in RATE_USES
                  if sum(1 for v in RATE_USES if (v.factor, v.faster) == (u.factor, u.faster)) >= 2]
        use = rng.choice(paired)
        same = [v for v in RATE_USES if v != use and (v.factor, v.faster) == (use.factor, use.faster)]
        correct = rng.choice(same).situation
        other_factors = rng.sample([f for f in FACTORS if f != use.factor], 3)
        wrongs = tuple(rng.choice([v for v in RATE_USES if v.factor == f]).situation
                       for f in other_factors)
        return _labelled(
            stem=(f"\"{use.situation}\" สถานการณ์ในข้อใดใช้หลักการควบคุมอัตราการเกิดปฏิกิริยา"
                  "แบบเดียวกัน"),
            correct=correct, wrongs=wrongs,
            topic=TOPIC_RATE_USE,
            hint="หาปัจจัยที่สถานการณ์แรกใช้ และดูว่าต้องการให้ปฏิกิริยาเร็วขึ้นหรือช้าลง แล้วหาข้อที่ใช้ทั้งสองอย่างเหมือนกัน",
        )
