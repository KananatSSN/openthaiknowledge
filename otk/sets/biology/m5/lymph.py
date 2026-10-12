"""ระบบน้ำเหลือง

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.5/14

Sets moved here from: science_wave_f63.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f63 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_LYMPH = "ระบบน้ำเหลือง"


LYMPH_FACTS = (
    ("น้ำเหลืองเกิดจากอะไร", "ของเหลวที่ซึมออกจากหลอดเลือดฝอยไปอยู่รอบเซลล์แล้วเข้าสู่หลอดน้ำเหลือง",
     ("เซลล์เม็ดเลือดแดงที่แตกออกแล้วปล่อยของเหลวภายในเซลล์เข้าสู่หลอดน้ำเหลือง",
      "น้ำดีที่ไหลออกจากตับแล้วซึมเข้าสู่หลอดน้ำเหลืองบริเวณลำไส้เล็ก",
      "ปัสสาวะที่ไตดูดกลับแล้วส่งเข้าหลอดน้ำเหลืองแทนหลอดเลือด",
      "เหงื่อที่ซึมกลับเข้าผิวหนังแล้วรวมกันเป็นของเหลวในหลอดน้ำเหลือง")),
    ("น้ำเหลืองแตกต่างจากพลาสมาอย่างไร", "มีโปรตีนน้อยกว่าและไม่มีเซลล์เม็ดเลือดแดง",
     ("มีโปรตีนมากกว่ามากและมีเซลล์เม็ดเลือดแดงปน", "มีเพลตเลตมากกว่าและไม่มีเซลล์เม็ดเลือดขาว",
      "มีเซลล์เม็ดเลือดแดงมากกว่าและไม่มีโปรตีน", "ไม่มีน้ำเป็นองค์ประกอบ แต่มีโปรตีนมากกว่า")),
    ("หลอดน้ำเหลืองมีลักษณะอย่างไร", "ผนังบาง มีลิ้นกั้นให้น้ำเหลืองไหลทางเดียวกลับสู่หัวใจ",
     ("ผนังหนามีกล้ามเนื้อมาก สูบฉีดน้ำเหลืองไปทั่วร่างกายได้เอง",
      "ผนังบาง ไม่มีลิ้น น้ำเหลืองจึงไหลไปกลับได้ทั้งสองทิศทาง",
      "ผนังหนา เชื่อมต่อกับอาร์เทอรีโดยตรงเพื่อรับเลือดจากหัวใจ",
      "ผนังบาง มีเซลล์เม็ดเลือดแดงไหลอยู่เต็มเหมือนหลอดเลือดเวน")),
    ("น้ำเหลืองเคลื่อนที่ได้เพราะเหตุใด", "การหดตัวของกล้ามเนื้อลายรอบหลอดน้ำเหลืองและลิ้นกันไหลย้อน",
     ("หัวใจสูบฉีดน้ำเหลืองโดยตรงผ่านอาร์เทอรีที่ต่อกับหลอดน้ำเหลือง",
      "แรงโน้มถ่วงเพียงอย่างเดียว น้ำเหลืองจึงไหลจากศีรษะลงสู่เท้า",
      "ไตดูดน้ำเหลืองเข้าหาตัวเพื่อกรองของเสียออกเป็นปัสสาวะ",
      "ปอดดูดน้ำเหลืองขึ้นมาขณะหายใจออกด้วยแรงดันในช่องอก")),
    ("ระบบน้ำเหลืองมีหน้าที่สำคัญข้อใด", "นำของเหลวรอบเซลล์กลับสู่ระบบหมุนเวียนเลือดและช่วยกำจัดสิ่งแปลกปลอม",
     ("สูบฉีดเลือดที่มีออกซิเจนไปเลี้ยงเซลล์ทั่วร่างกายแทนหัวใจเมื่อออกกำลังกาย",
      "แลกเปลี่ยนแก๊สออกซิเจนและคาร์บอนไดออกไซด์กับอากาศภายนอก",
      "สร้างน้ำดีสำหรับย่อยไขมันและส่งไปเก็บไว้ที่ถุงน้ำดี",
      "กรองของเสียออกจากเลือดแล้วขับออกนอกร่างกายเป็นปัสสาวะ")),
    ("เซลล์ชนิดใดพบมากในน้ำเหลือง", "ลิมโฟไซต์", ("เซลล์เม็ดเลือดแดง", "เพลตเลต", "เซลล์ประสาท", "เซลล์กล้ามเนื้อ")),
    ("น้ำเหลืองกลับเข้าสู่ระบบหมุนเวียนเลือดที่ใด", "เวนใต้กระดูกไหปลาร้า",
     ("อาร์เทอรีที่ขา", "หัวใจห้องล่างซ้ายโดยตรง", "หลอดเลือดฝอยในปอด", "เวนตับ")),
)


ORGANS = (
    ("ต่อมน้ำเหลือง", "กรองสิ่งแปลกปลอมในน้ำเหลืองและเป็นที่อยู่ของลิมโฟไซต์"),
    ("ม้าม", "ทำลายเซลล์เม็ดเลือดแดงที่หมดอายุและสร้างลิมโฟไซต์"),
    ("ต่อมไทมัส", "เป็นที่เจริญเต็มที่ของ T ลิมโฟไซต์"),
    ("ทอนซิล", "ดักจับเชื้อโรคที่เข้าทางปากและจมูก"),
    ("ไขกระดูก", "สร้างเซลล์เม็ดเลือดทุกชนิดรวมทั้งลิมโฟไซต์"),
)


LYMPH_HINT = ("น้ำเหลืองคือของเหลวรอบเซลล์ที่เข้าสู่หลอดน้ำเหลือง ไหลทางเดียวกลับเข้าเวนใต้กระดูกไหปลาร้า "
              "ต่อมน้ำเหลืองกรองเชื้อโรค ไทมัสเป็นที่เจริญของ T ลิมโฟไซต์ ม้ามทำลายเม็ดเลือดแดงเก่า")


@question_type(
    "biology.lymph_foundation",
    display_name={"th": "น้ำเหลืองและหลอดน้ำเหลือง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_LYMPH,
)
class LymphFoundation(QuestionType):
    """Where lymph comes from, how it moves, where it goes back."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(LYMPH_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_LYMPH, hint=LYMPH_HINT)


@question_type(
    "biology.lymph_fluency",
    display_name={"th": "อวัยวะในระบบน้ำเหลืองและหน้าที่"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_LYMPH,
)
class LymphFluency(QuestionType):
    """Lymph nodes, spleen, thymus, tonsils and marrow."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, role = rng.choice(ORGANS)
        others = rng.sample([o for o in ORGANS if o[0] != name], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"{name}มีหน้าที่อย่างไร", correct=role, wrongs=tuple(o[1] for o in others), topic=TOPIC_LYMPH,
                             hint=LYMPH_HINT)
        return _labelled(stem=f"อวัยวะใด{role}", correct=name, wrongs=tuple(o[0] for o in others), topic=TOPIC_LYMPH, hint=LYMPH_HINT)


@question_type(
    "biology.lymph_application",
    display_name={"th": "ปริมาณน้ำเหลืองและผลเมื่อระบบน้ำเหลืองผิดปกติ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_LYMPH,
)
class LymphApplication(QuestionType):
    """What the capillaries do not take back becomes lymph."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            filtered = rng.randrange(16, 31)
            back = rng.choice((80, 85, 90))
            lymph = Fraction(filtered * (100 - back), 100)
            return numeric(stem=f"ในหนึ่งวันของเหลวซึมออกจากหลอดเลือดฝอย {filtered} ลิตร และถูกดูดกลับเข้าหลอดเลือดฝอยร้อยละ {back} "
                                f"ของเหลวที่เหลือกลายเป็นน้ำเหลืองวันละกี่ลิตร", answer=lymph,
                           wrongs=[Fraction(filtered * back, 100), filtered, 100 - back], unit="ลิตร", topic=TOPIC_LYMPH,
                           hint="น้ำเหลือง = ของเหลวที่ซึมออก × (100 − ร้อยละที่ดูดกลับ) ÷ 100")
        cases = (("ถ้าหลอดน้ำเหลืองที่ขาถูกอุดตันจากพยาธิ จะเกิดอะไรขึ้น", "ขาบวมเพราะของเหลวคั่งอยู่รอบเซลล์ (โรคเท้าช้าง)",
                  ("ขาลีบเล็กลงเพราะขาดเลือด", "เลือดออกที่ขา", "ขาไม่เปลี่ยนแปลง")),
                 ("เมื่อติดเชื้อที่ลำคอ มักคลำพบต่อมน้ำเหลืองที่คอโตขึ้นเพราะเหตุใด", "ลิมโฟไซต์เพิ่มจำนวนเพื่อต่อสู้กับเชื้อโรค",
                  ("ต่อมน้ำเหลืองสะสมไขมัน", "เลือดไหลออกจากต่อม", "ต่อมน้ำเหลืองสร้างเม็ดเลือดแดงเพิ่ม")),
                 ("ไขมันที่ถูกดูดซึมที่ลำไส้เล็กเข้าสู่ระบบน้ำเหลืองทางใด", "หลอดน้ำเหลืองแล็กเทียลในวิลลัส",
                  ("หลอดเลือดฝอยไปตับโดยตรง", "ต่อมไทมัส", "ม้าม")))
        stem, right, wrongs = rng.choice(cases)
        return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_LYMPH, hint=LYMPH_HINT)
