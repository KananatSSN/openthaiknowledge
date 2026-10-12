"""การงอกของเมล็ดและการพักตัว

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 3 ม.5/16

Sets moved here from: science_wave_f58.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f58 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_GERM = "การงอกของเมล็ดและการพักตัว"


DORMANCY = (
    ("เปลือกเมล็ดแข็งหนาจนน้ำและแก๊สซึมผ่านไม่ได้", "ทำให้เปลือกเมล็ดเป็นแผล เช่น ขัดด้วยกระดาษทราย ตัดเปลือก หรือแช่กรดเข้มข้นระยะสั้น"),
    ("มีสารยับยั้งการงอก เช่น กรดแอบไซซิก สะสมในเมล็ด", "แช่น้ำหรือล้างเมล็ดเพื่อชะล้างสารยับยั้งออก หรือให้จิบเบอเรลลิน"),
    ("เอ็มบริโอยังเจริญไม่เต็มที่", "เก็บเมล็ดไว้ระยะหนึ่งให้เอ็มบริโอเจริญเต็มที่ก่อนนำไปเพาะ"),
    ("เมล็ดต้องการอุณหภูมิต่ำระยะหนึ่งก่อนงอก", "เก็บเมล็ดในที่เย็นชื้นระยะหนึ่งก่อนเพาะ"),
    ("เมล็ดบางชนิดต้องได้รับแสงจึงงอก", "เพาะโดยไม่กลบดินหนาเพื่อให้เมล็ดได้รับแสง"),
)


GERM_FACTS = (
    ("ปัจจัยใดจำเป็นต่อการงอกของเมล็ดส่วนใหญ่", "น้ำ แก๊สออกซิเจน และอุณหภูมิที่เหมาะสม",
     ("แสงสว่างมาก ๆ และปุ๋ยเคมีที่เพียงพอ", "ดินที่มีธาตุอาหารสมบูรณ์เท่านั้น", "แก๊สคาร์บอนไดออกไซด์ปริมาณสูง", "น้ำเกลือเข้มข้น")),
    ("น้ำช่วยให้เมล็ดงอกได้อย่างไร", "ทำให้เปลือกเมล็ดอ่อนนุ่ม และกระตุ้นเอนไซม์ย่อยอาหารสะสม",
     ("ทำให้เมล็ดหนักจนจมดิน", "ให้พลังงานแก่เอ็มบริโอโดยตรงโดยไม่ต้องย่อยอาหารสะสม", "ใช้แทนแก๊สออกซิเจนในการหายใจระดับเซลล์ของเอ็มบริโอ", "ทำให้เมล็ดพักตัวนานขึ้น")),
    ("เมล็ดที่ถูกฝังในดินที่มีน้ำขังตลอดเวลามักไม่งอกเพราะเหตุใด", "ขาดแก๊สออกซิเจนสำหรับการหายใจระดับเซลล์",
     ("ได้รับแสงมากเกินไป", "อุณหภูมิสูงเกินไป", "มีออกซิเจนมากเกินไป", "เมล็ดสังเคราะห์ด้วยแสงไม่ได้เพราะอยู่ใต้น้ำ")),
    ("การงอกของถั่วเขียวที่ใบเลี้ยงชูขึ้นเหนือดินเรียกว่าอะไร", "การงอกแบบใบเลี้ยงอยู่เหนือดิน (epigeal)",
     ("การงอกแบบใบเลี้ยงอยู่ใต้ดิน (hypogeal)", "การพักตัวของเมล็ด", "การปฏิสนธิซ้อน", "การแตกตาข้าง")),
    ("การงอกของเมล็ดข้าวโพดที่ใบเลี้ยงยังอยู่ใต้ดินเรียกว่าอะไร", "การงอกแบบใบเลี้ยงอยู่ใต้ดิน (hypogeal)",
     ("การงอกแบบใบเลี้ยงอยู่เหนือดิน (epigeal)", "การพักตัวของเมล็ด", "การแตกตาข้าง", "การปฏิสนธิซ้อน")),
    ("ระหว่างเมล็ดงอก อาหารสะสมในเมล็ดถูกนำไปใช้อย่างไร", "ถูกเอนไซม์ย่อยเป็นสารโมเลกุลเล็กแล้วลำเลียงไปใช้ในการเจริญของเอ็มบริโอ",
     ("ถูกเก็บไว้จนต้นอ่อนตาย", "ถูกส่งออกไปทางรากสู่ดินเพื่อเป็นปุ๋ยให้ต้นอ่อนดูดกลับมาใช้", "ถูกเปลี่ยนเป็นเปลือกเมล็ดใหม่ที่หนาขึ้น เพื่อป้องกันเอ็มบริโอจนกว่าจะงอก", "ใช้เป็นวัตถุดิบในการสังเคราะห์ด้วยแสงโดยตรงภายในเมล็ดที่อยู่ใต้ดิน")),
    ("ส่วนใดของเอ็มบริโองอกออกจากเมล็ดเป็นส่วนแรก", "รากแรกเกิด (radicle)",
     ("ใบเลี้ยง (cotyledon)", "ใบแท้คู่แรก (true leaf)", "ตายอด (shoot tip)", "เปลือกเมล็ด (seed coat)")),
    ("การพักตัวของเมล็ดมีประโยชน์ต่อพืชอย่างไร", "ช่วยให้เมล็ดงอกในช่วงที่สภาพแวดล้อมเหมาะสมต่อการเจริญของต้นอ่อน",
     ("ทำให้เมล็ดงอกได้ทันทีเสมอ", "ทำให้เมล็ดงอกได้โดยไม่ต้องการน้ำและออกซิเจนตลอดช่วงพักตัว", "ทำให้เมล็ดสังเคราะห์ด้วยแสงได้ระหว่างรอให้สภาพแวดล้อมเหมาะสม", "ป้องกันการปฏิสนธิ")),
)


GERM_HINT = ("เมล็ดต้องการน้ำ O₂ และอุณหภูมิเหมาะสม การพักตัวเกิดจากเปลือกแข็ง สารยับยั้ง เอ็มบริโอไม่สมบูรณ์ หรือต้องการความเย็นหรือแสง "
             "แก้ได้โดยทำเปลือกให้เป็นแผล ชะล้างสารยับยั้ง หรือให้จิบเบอเรลลิน")


CONDITIONS = (("น้ำ", "สำลีแห้ง"), ("ออกซิเจน", "จมอยู่ใต้น้ำต้มที่เย็นแล้วและมีน้ำมันปิดผิว"), ("อุณหภูมิที่เหมาะสม", "ตู้เย็นที่ 4 °C"))


@question_type(
    "biology.germination_foundation",
    display_name={"th": "ปัจจัยที่จำเป็นต่อการงอกของเมล็ด"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_GERM,
)
class GerminationFoundation(QuestionType):
    """Water, oxygen, warmth; and the two ways shoots come up."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(GERM_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_GERM, hint=GERM_HINT)


@question_type(
    "biology.germination_fluency",
    display_name={"th": "สาเหตุการพักตัวของเมล็ดและวิธีแก้"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_GERM,
)
class GerminationFluency(QuestionType):
    """Match the cause of dormancy to the way to break it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        cause, fix = rng.choice(DORMANCY)
        others = rng.sample([d for d in DORMANCY if d[0] != cause], 3)
        seed = rng.choice(("เมล็ดมะขาม", "เมล็ดพืชชนิดหนึ่ง", "เมล็ดไม้ป่า", "เมล็ดพืชตระกูลถั่ว"))
        if rng.random() < 0.55:
            return _labelled(stem=f"{seed}พักตัวเพราะ{cause} ควรแก้การพักตัวอย่างไร", correct=fix, wrongs=tuple(d[1] for d in others),
                             topic=TOPIC_GERM, hint=GERM_HINT)
        return _labelled(stem=f"วิธี \"{fix}\" ใช้แก้การพักตัวของเมล็ดที่มีสาเหตุใด", correct=cause, wrongs=tuple(d[0] for d in others),
                         topic=TOPIC_GERM, hint=GERM_HINT)


@question_type(
    "biology.germination_application",
    display_name={"th": "วิเคราะห์ผลการทดลองการงอกของเมล็ด"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_GERM,
)
class GerminationApplication(QuestionType):
    """Germination percentage, and what a missing condition tells you."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            total = rng.choice((20, 25, 40, 50, 80, 100, 200))
            grew = rng.randrange(1, total + 1)
            answer = Fraction(grew * 100, total)
            seed = rng.choice(("ถั่วเขียว", "ข้าวโพด", "พริก", "ทานตะวัน", "ข้าว"))
            if rng.random() < 0.5:
                return numeric(stem=f"เพาะเมล็ด{seed} {total} เมล็ด งอก {grew} เมล็ด ร้อยละการงอกเป็นเท่าใด", answer=answer,
                               wrongs=[grew, 100 - answer or 50, Fraction(total - grew, 1) or 1], unit="%", topic=TOPIC_GERM,
                               hint="ร้อยละการงอก = จำนวนที่งอก × 100 ÷ จำนวนที่เพาะ")
            return numeric(stem=f"เมล็ด{seed}ล็อตหนึ่งมีร้อยละการงอก {show(answer)} ถ้าเพาะ {total} เมล็ด คาดว่าจะงอกกี่เมล็ด", answer=grew,
                           wrongs=[total - grew or total, answer if answer != grew else grew + 1, total], unit="เมล็ด", topic=TOPIC_GERM,
                           hint="จำนวนที่งอก = จำนวนที่เพาะ × ร้อยละการงอก ÷ 100")
        missing, setup = rng.choice(CONDITIONS)
        others = [c[0] for c in CONDITIONS if c[0] != missing]
        return _labelled(stem=f"จานที่ 1 เพาะเมล็ดถั่วเขียวบนสำลีชื้นที่อุณหภูมิห้อง เมล็ดงอก จานที่ 2 เพาะใน{setup} เมล็ดไม่งอก "
                              f"ผลการทดลองนี้แสดงว่าการงอกของเมล็ดต้องอาศัยปัจจัยใด", correct=missing,
                         wrongs=(*others, "แสงสว่าง"), topic=TOPIC_GERM,
                         hint="เทียบสองชุดที่ต่างกันเพียงปัจจัยเดียว ปัจจัยนั้นคือสิ่งที่ทำให้ผลต่างกัน")
