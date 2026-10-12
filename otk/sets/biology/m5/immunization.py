"""ภูมิคุ้มกันก่อเองและภูมิคุ้มกันรับมา

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.5/16

Sets moved here from: science_wave_f63.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f63 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_IMMUNE = "ภูมิคุ้มกันก่อเองและภูมิคุ้มกันรับมา"


ACTIVE = ("ฉีดวัคซีนป้องกันโรคหัด", "หยอดวัคซีนโปลิโอ", "ฉีดท็อกซอยด์ป้องกันบาดทะยัก", "หายจากโรคอีสุกอีใสแล้วไม่เป็นซ้ำ",
          "ฉีดวัคซีนไข้หวัดใหญ่ประจำปี")


PASSIVE = ("ฉีดเซรุ่มแก้พิษงูหลังถูกงูกัด", "ทารกได้รับแอนติบอดีจากแม่ผ่านรก", "ทารกได้รับแอนติบอดีจากน้ำนมแม่",
           "ฉีดอิมมูโนโกลบูลินหลังถูกสุนัขบ้ากัด", "ฉีดเซรุ่มแก้พิษบาดทะยักให้ผู้บาดเจ็บ")


IMMUNE_FEATURES = {
    "ภูมิคุ้มกันก่อเอง": ("ร่างกายสร้างแอนติบอดีและเซลล์ความจำขึ้นเอง", "ใช้เวลาหลายวันถึงหลายสัปดาห์จึงเกิดผล", "อยู่ได้นานหลายปี"),
    "ภูมิคุ้มกันรับมา": ("ได้รับแอนติบอดีสำเร็จรูปจากภายนอก", "ได้ผลทันที", "อยู่ได้ไม่นาน เพราะไม่มีเซลล์ความจำ"),
}


IMMUNE_HINT = ("ภูมิคุ้มกันก่อเองได้จากวัคซีนหรือการติดเชื้อ ร่างกายสร้างเอง ช้าแต่นาน ภูมิคุ้มกันรับมาได้แอนติบอดีสำเร็จรูป "
               "เช่น เซรุ่ม หรือจากแม่ ได้ผลทันทีแต่สั้น")


@question_type(
    "biology.immunization_foundation",
    display_name={"th": "ตัวอย่างภูมิคุ้มกันก่อเองและภูมิคุ้มกันรับมา"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_IMMUNE,
)
class ImmunizationFoundation(QuestionType):
    """Vaccine or serum?"""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        active = rng.random() < 0.5
        same, other = (ACTIVE, PASSIVE) if active else (PASSIVE, ACTIVE)
        kind = "ภูมิคุ้มกันก่อเอง" if active else "ภูมิคุ้มกันรับมา"
        if rng.random() < 0.5:
            return _labelled(stem=f"ข้อใดเป็นการได้รับ{kind}", correct=rng.choice(same), wrongs=tuple(other), topic=TOPIC_IMMUNE,
                             hint=IMMUNE_HINT)
        return _labelled(stem=f"\"{rng.choice(same)}\" ทำให้เกิดภูมิคุ้มกันแบบใด", correct=kind,
                         wrongs=("ภูมิคุ้มกันรับมา" if active else "ภูมิคุ้มกันก่อเอง", "กลไกไม่จำเพาะเพียงอย่างเดียว", "ภาวะภูมิแพ้"),
                         topic=TOPIC_IMMUNE, hint=IMMUNE_HINT)


@question_type(
    "biology.immunization_fluency",
    display_name={"th": "เปรียบเทียบภูมิคุ้มกันก่อเองและภูมิคุ้มกันรับมา"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_IMMUNE,
)
class ImmunizationFluency(QuestionType):
    """Speed, source and how long each lasts; and which to use when."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            kind = rng.choice(sorted(IMMUNE_FEATURES))
            other = next(k for k in IMMUNE_FEATURES if k != kind)
            feature = rng.choice(IMMUNE_FEATURES[kind])
            if rng.random() < 0.5:
                extra = ("เกิดจากเซลล์เม็ดเลือดแดงสร้างแอนติบอดี", "ไม่เกี่ยวข้องกับแอนติบอดีเลย", "ได้จากการรับประทานยาปฏิชีวนะ")
                return _labelled(stem=f"ข้อใดเป็นลักษณะของ{kind}", correct=feature,
                                 wrongs=(*rng.sample(IMMUNE_FEATURES[other], 2), rng.choice(extra)), topic=TOPIC_IMMUNE, hint=IMMUNE_HINT)
            return _labelled(stem=f"ภูมิคุ้มกันที่ \"{feature}\" เป็นแบบใด", correct=kind,
                             wrongs=(other, *rng.sample(("กลไกไม่จำเพาะ", "ภาวะภูมิต้านตนเอง", "ภาวะภูมิแพ้", "ภูมิคุ้มกันบกพร่อง"), 2)),
                             topic=TOPIC_IMMUNE, hint=IMMUNE_HINT)
        cases = (("ผู้ที่เพิ่งถูกงูเห่ากัดควรได้รับการรักษาแบบใด", "ฉีดเซรุ่มแก้พิษงู เพราะต้องการแอนติบอดีทันที",
                  ("ฉีดวัคซีนป้องกันพิษงู เพราะภูมิคุ้มกันอยู่ได้นาน", "รอให้ร่างกายสร้างแอนติบอดีต่อพิษงูขึ้นเอง",
                   "ให้ยาปฏิชีวนะเพียงอย่างเดียว เพราะพิษงูเป็นเชื้อแบคทีเรีย")),
                 ("ผู้ที่จะเดินทางไปพื้นที่ที่มีโรคระบาดในอีกสองเดือนควรทำอย่างไร", "ฉีดวัคซีนล่วงหน้า ให้ร่างกายสร้างภูมิคุ้มกันก่อเอง",
                  ("ฉีดเซรุ่มตอนนี้ เพราะแอนติบอดีสำเร็จรูปอยู่ได้หลายปี", "ไม่ต้องทำอะไร เพราะร่างกายจะสร้างภูมิคุ้มกันได้ทันทีเมื่อติดเชื้อ",
                   "รับเลือดจากผู้ที่เคยป่วย เพื่อให้เกิดภูมิคุ้มกันก่อเองถาวร")),
                 ("เหตุใดเด็กจึงต้องรับวัคซีนบางชนิดซ้ำหลายครั้ง", "กระตุ้นให้สร้างแอนติบอดีและเซลล์ความจำมากพอ",
                  ("เพราะวัคซีนครั้งแรกเป็นพิษ จึงต้องฉีดซ้ำเพื่อแก้พิษ", "เพื่อให้ได้แอนติบอดีจากแม่เพิ่มขึ้นทุกครั้ง",
                   "เพราะวัคซีนเป็นภูมิคุ้มกันรับมา ซึ่งหมดไปภายในไม่กี่สัปดาห์")))
        stem, right, wrongs = rng.choice(cases)
        return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_IMMUNE, hint=IMMUNE_HINT)


@question_type(
    "biology.immunization_application",
    display_name={"th": "การลดลงของแอนติบอดีที่ได้รับมา"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_IMMUNE,
)
class ImmunizationApplication(QuestionType):
    """Borrowed antibody halves every half-life; nothing replaces it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        half = rng.choice((10, 14, 20, 21, 25, 30))
        n = rng.randint(1, 5)
        start = rng.randrange(1, 21) * 2 ** n * 10
        left = Fraction(start, 2 ** n)
        source = rng.choice(("เซรุ่มที่ฉีดให้", "แอนติบอดีที่ทารกได้รับจากแม่", "อิมมูโนโกลบูลินที่ฉีดให้"))
        if rng.random() < 0.6:
            return numeric(stem=f"ระดับ{source}เริ่มต้น {start} หน่วย และลดลงครึ่งหนึ่งทุก {half} วัน เมื่อผ่านไป {half * n} วันจะเหลือกี่หน่วย",
                           answer=left, wrongs=[start - left, Fraction(start, n + 1) if (Fraction(start, n + 1) * 100).denominator == 1
                                                else left * 2, left / 2 if (left / 2 * 100).denominator == 1 else left + 1], unit="หน่วย",
                           topic=TOPIC_IMMUNE, hint="ผ่านไป n ครึ่งชีวิต เหลือ เริ่มต้น ÷ 2ⁿ ภูมิคุ้มกันรับมาไม่มีเซลล์ความจำจึงไม่ถูกสร้างเพิ่ม")
        return numeric(stem=f"ระดับ{source}ลดจาก {start} หน่วยเหลือ {show(left)} หน่วย ถ้าลดลงครึ่งหนึ่งทุก {half} วัน ใช้เวลากี่วัน",
                       answer=half * n, wrongs=[half * (n + 1), half, half * 2 ** n if 2 ** n != n else half * 3], unit="วัน",
                       topic=TOPIC_IMMUNE, hint="นับว่าลดลงครึ่งหนึ่งกี่ครั้ง แล้วคูณด้วยครึ่งชีวิต")
