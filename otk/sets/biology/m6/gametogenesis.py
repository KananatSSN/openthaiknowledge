"""การสร้างเซลล์สืบพันธุ์และการปฏิสนธิของมนุษย์

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.6/14

Sets moved here from: science_wave_f69.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f69 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_GAMETE = "การสร้างเซลล์สืบพันธุ์และการปฏิสนธิของมนุษย์"


SPERM_STEPS = ("สเปอร์มาโทโกเนียม", "สเปอร์มาโทไซต์ระยะแรก", "สเปอร์มาโทไซต์ระยะที่สอง", "สเปอร์มาทิด", "อสุจิ")


EGG_STEPS = ("โอโอโกเนียม", "โอโอไซต์ระยะแรก", "โอโอไซต์ระยะที่สอง", "เซลล์ไข่")


PLOIDY = (("สเปอร์มาโทโกเนียม", 2), ("สเปอร์มาโทไซต์ระยะแรก", 2), ("สเปอร์มาโทไซต์ระยะที่สอง", 1), ("สเปอร์มาทิด", 1),
          ("อสุจิ", 1), ("โอโอโกเนียม", 2), ("โอโอไซต์ระยะแรก", 2), ("โอโอไซต์ระยะที่สอง", 1), ("โพลาร์บอดี", 1), ("ไซโกต", 2))


GAMETE_HINT = ("สเปอร์มาโทโกเนียม (2n) → สเปอร์มาโทไซต์ระยะแรก (2n) → ไมโอซิส I → ระยะที่สอง (n) → ไมโอซิส II → สเปอร์มาทิด → อสุจิ "
               "1 เซลล์ระยะแรกให้อสุจิ 4 ตัว โอโอไซต์ระยะแรก 1 เซลล์ให้เซลล์ไข่ 1 เซลล์กับโพลาร์บอดี")


@question_type(
    "biology.gametogenesis_foundation",
    display_name={"th": "ขั้นตอนการสร้างอสุจิและเซลล์ไข่"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_GAMETE,
)
class GametogenesisFoundation(QuestionType):
    """The next cell along each line."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        steps = SPERM_STEPS if rng.random() < 0.55 else EGG_STEPS
        i = rng.randrange(len(steps) - 1)
        pool = [s for s in SPERM_STEPS + EGG_STEPS if s not in (steps[i], steps[i + 1])] + ["โพลาร์บอดี"]
        if rng.random() < 0.3:
            facts = (("การสร้างอสุจิเกิดขึ้นที่ใด", "หลอดสร้างอสุจิในอัณฑะ", ("หลอดเก็บอสุจิ", "ต่อมลูกหมาก", "ท่อปัสสาวะ", "ถุงสร้างน้ำเลี้ยงอสุจิ")),
                     ("ในการตกไข่ เซลล์ที่หลุดออกจากรังไข่คือเซลล์ใด", "โอโอไซต์ระยะที่สอง",
                      ("โอโอโกเนียม", "โอโอไซต์ระยะแรก", "ไซโกต", "โพลาร์บอดีที่สอง")),
                     ("โอโอไซต์ระยะที่สองแบ่งไมโอซิส II จนเสร็จเมื่อใด", "เมื่ออสุจิเข้าผสม",
                      ("ก่อนเกิด", "เมื่อเข้าสู่วัยรุ่น", "ขณะอยู่ในมดลูก", "ไม่แบ่งอีกเลย")))
            stem, right, wrongs = rng.choice(facts)
            return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_GAMETE, hint=GAMETE_HINT)
        return _labelled(stem=f"ในการสร้าง{'อสุจิ' if steps is SPERM_STEPS else 'เซลล์ไข่'} เซลล์ที่เจริญต่อจาก{steps[i]}คือเซลล์ใด",
                         correct=steps[i + 1], wrongs=tuple(pool), topic=TOPIC_GAMETE, hint=GAMETE_HINT)


@question_type(
    "biology.gametogenesis_fluency",
    display_name={"th": "เปรียบเทียบการสร้างอสุจิและเซลล์ไข่ และการปฏิสนธิ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_GAMETE,
)
class GametogenesisFluency(QuestionType):
    """Four sperm against one egg, and what happens at fertilisation."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        facts = (
            ("การสร้างเซลล์ไข่ต่างจากการสร้างอสุจิอย่างไร", "โอโอไซต์ระยะแรก 1 เซลล์ได้เซลล์ไข่เพียง 1 เซลล์ ส่วนที่เหลือเป็นโพลาร์บอดี",
             ("โอโอไซต์ระยะแรก 1 เซลล์ได้เซลล์ไข่ 4 เซลล์ที่มีขนาดเท่ากันเหมือนอสุจิ", "ไม่มีการแบ่งแบบไมโอซิส",
              "เซลล์ไข่ที่ได้มีโครโมโซม 2n เพราะการสร้างเซลล์ไข่ไม่มีการแบ่งแบบไมโอซิส", "ได้เซลล์ไข่ 2 เซลล์")),
            ("เซลล์ไข่มีขนาดใหญ่กว่าโพลาร์บอดีมากเพราะเหตุใด", "ไซโทพลาซึมแบ่งไม่เท่ากัน เซลล์ไข่ได้อาหารสะสมไว้เกือบทั้งหมด",
             ("เซลล์ไข่มีโครโมโซมมากกว่าโพลาร์บอดี จึงต้องมีไซโทพลาซึมมากกว่า", "โพลาร์บอดีแบ่งตัวต่ออีกหลายครั้งจนเซลล์มีขนาดเล็กลงเรื่อย ๆ", "เซลล์ไข่ดูดน้ำเข้ามา", "โพลาร์บอดีเป็นเซลล์ตาย")),
            ("อะโครโซมที่ส่วนหัวของอสุจิมีหน้าที่อะไร", "มีเอนไซม์ย่อยชั้นที่หุ้มเซลล์ไข่เพื่อให้อสุจิเข้าไปได้",
             ("สร้างพลังงานให้หางอสุจิใช้ในการว่ายไปหาเซลล์ไข่", "เก็บโครโมโซมชุดเดียว (n) ที่จะเข้าผสมกับเซลล์ไข่", "ช่วยให้อสุจิแบ่งตัว", "สร้างฮอร์โมนเพศชาย")),
            ("ส่วนกลางของอสุจิมีไมโทคอนเดรียจำนวนมากเพื่ออะไร", "สร้าง ATP ให้หางอสุจิเคลื่อนที่",
             ("เก็บสารพันธุกรรมของอสุจิ", "ย่อยชั้นที่หุ้มเซลล์ไข่ให้อสุจิเข้าไป", "กำหนดเพศของลูก", "สร้างอสุจิใหม่")),
            ("การปฏิสนธิของมนุษย์โดยปกติเกิดขึ้นเมื่อใด", "เมื่ออสุจิพบโอโอไซต์ระยะที่สองในท่อนำไข่ ภายในหนึ่งวันหลังตกไข่",
             ("เมื่อเซลล์ไข่ฝังตัวในมดลูกแล้ว ประมาณหนึ่งสัปดาห์หลังตกไข่", "ขณะโอโอไซต์ระยะแรกยังอยู่ในรังไข่ ก่อนการตกไข่ภายในรูขุมไข่", "เมื่อเซลล์ไข่ถึงช่องคลอด", "ก่อนการตกไข่หนึ่งสัปดาห์")),
            ("เหตุใดอสุจิเพียงตัวเดียวจึงเข้าผสมกับเซลล์ไข่ได้", "เมื่ออสุจิตัวแรกเข้าไป เยื่อหุ้มเซลล์ไข่เปลี่ยนแปลงป้องกันอสุจิตัวอื่น",
             ("อสุจิตัวอื่นตายทันทีที่หลั่งออกมา เหลือเพียงตัวเดียวที่ไปถึงเซลล์ไข่", "เซลล์ไข่มีรูให้อสุจิเข้าได้รูเดียว เมื่ออสุจิตัวแรกเข้าไปแล้วรูจึงปิด", "อสุจิตัวอื่นไม่มีหาง", "มดลูกดักอสุจิไว้")),
            ("เพศของลูกถูกกำหนดโดยอะไร", "อสุจิที่มีโครโมโซม X หรือ Y ที่เข้าผสมกับเซลล์ไข่",
             ("เซลล์ไข่ที่มีโครโมโซม X หรือ Y", "จำนวนอสุจิที่เข้าผสมกับเซลล์ไข่ในครั้งนั้น", "ฮอร์โมนเพศของแม่ขณะตั้งครรภ์ในช่วงแรก", "อุณหภูมิของมดลูก")),
        )
        stem, right, wrongs = rng.choice(facts)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_GAMETE, hint=GAMETE_HINT)


@question_type(
    "biology.gametogenesis_application",
    display_name={"th": "จำนวนเซลล์สืบพันธุ์และจำนวนโครโมโซมในแต่ละระยะ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_GAMETE,
)
class GametogenesisApplication(QuestionType):
    """Four sperm or one egg per starting cell; n or 2n per stage."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            name, sets = rng.choice(PLOIDY)
            diploid = 46
            return numeric(stem=f"เซลล์ร่างกายของคนมีโครโมโซม 46 แท่ง {name}มีโครโมโซมกี่แท่ง", answer=diploid // 2 * sets,
                           wrongs=[diploid if sets == 1 else 23, 92, 69], unit="แท่ง", topic=TOPIC_GAMETE, hint=GAMETE_HINT)
        k = rng.randrange(2, 201)
        cases = ((f"สเปอร์มาโทไซต์ระยะแรก {k} เซลล์ สร้างอสุจิได้กี่ตัว", 4 * k, [k, 2 * k, 8 * k], "ตัว"),
                 (f"สเปอร์มาโทไซต์ระยะที่สอง {k} เซลล์ สร้างอสุจิได้กี่ตัว", 2 * k, [4 * k, k, 8 * k], "ตัว"),
                 (f"โอโอไซต์ระยะแรก {k} เซลล์ สร้างเซลล์ไข่ได้กี่เซลล์", k, [4 * k, 2 * k, 3 * k], "เซลล์"),
                 (f"โอโอไซต์ระยะแรก {k} เซลล์ที่แบ่งไมโอซิสจนเสร็จ ได้โพลาร์บอดีรวมอย่างน้อยกี่เซลล์", 2 * k, [k, 3 * k, 4 * k], "เซลล์"))
        stem, answer, wrongs, unit = rng.choice(cases)
        return numeric(stem=stem, answer=answer, wrongs=wrongs, unit=unit, topic=TOPIC_GAMETE,
                       hint=GAMETE_HINT + " (ถ้าโพลาร์บอดีแรกไม่แบ่งต่อ จะได้โพลาร์บอดี 2 เซลล์ต่อโอโอไซต์)")
