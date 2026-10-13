"""การศึกษาการสังเคราะห์ด้วยแสงในอดีต

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 3 ม.5/9

Sets moved here from: science_wave_f56.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f56 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_HISTORY = "การศึกษาการสังเคราะห์ด้วยแสงในอดีต"


SCIENTISTS = (
    ("ฟาน เฮลมอนต์", "ปลูกต้นหลิวในดินที่ชั่งน้ำหนักไว้ ต้นหลิวหนักขึ้นมากแต่ดินหายไปเล็กน้อย จึงสรุปว่าน้ำหนักมาจากน้ำ"),
    ("พริสต์ลีย์", "เทียนไขที่ดับในครอบแก้วจุดติดได้อีกเมื่อใส่พืชไว้ด้วย แสดงว่าพืชเปลี่ยนอากาศให้ดีขึ้น"),
    ("อินเกนฮูซ", "พืชทำให้อากาศบริสุทธิ์ได้เฉพาะเมื่อได้รับแสง และเฉพาะส่วนที่เป็นสีเขียว"),
    ("เซเนบิเยร์", "พืชต้องใช้แก๊สคาร์บอนไดออกไซด์ในการสังเคราะห์ด้วยแสง"),
    ("เดอ โซซูร์", "น้ำหนักที่พืชเพิ่มขึ้นมากกว่าน้ำหนักของ CO₂ ที่ได้รับ จึงสรุปว่าพืชใช้น้ำด้วย"),
    ("เองเกิลมัน", "แบคทีเรียที่ต้องการออกซิเจนมารวมกลุ่มรอบสาหร่ายบริเวณที่ได้รับแสงสีแดงและสีน้ำเงินมากที่สุด"),
    ("รูเบนและคาเมน", "ใช้น้ำที่มี ¹⁸O พบว่าแก๊สออกซิเจนที่พืชปล่อยออกมามาจากน้ำ"),
    ("ฮิลล์", "คลอโรพลาสต์ที่แยกออกมาปล่อย O₂ ได้เมื่อได้รับแสงและมีสารรับอิเล็กตรอน แม้ไม่มี CO₂"),
    ("คัลวิน", "ใช้ ¹⁴CO₂ ติดตามจนพบวัฏจักรการตรึงคาร์บอนไดออกไซด์"),
)


HISTORY_HINT = ("ฟาน เฮลมอนต์: น้ำหนักจากน้ำ พริสต์ลีย์: พืชเปลี่ยนอากาศ อินเกนฮูซ: ต้องใช้แสง เองเกิลมัน: แสงแดงและน้ำเงิน "
                "รูเบนและคาเมน: O₂ มาจากน้ำ ฮิลล์: ปล่อย O₂ ได้โดยไม่ใช้ CO₂ คัลวิน: วัฏจักรตรึง CO₂")


CONCLUSIONS = (
    ("การทดลองของรูเบนและคาเมนสรุปได้ว่าอะไร", "แก๊ส O₂ ที่ได้จากการสังเคราะห์ด้วยแสงมาจากน้ำ ไม่ใช่จาก CO₂",
     ("แก๊ส O₂ ที่ได้จากการสังเคราะห์ด้วยแสงมาจาก CO₂ ไม่ใช่จากน้ำ", "น้ำตาลที่ได้จากการสังเคราะห์ด้วยแสงได้ออกซิเจนมาจากน้ำ", "พืชไม่ใช้น้ำในการสังเคราะห์ด้วยแสง")),
    ("การทดลองของเองเกิลมันแสดงว่าอะไร", "แสงสีแดงและสีน้ำเงินใช้ในการสังเคราะห์ด้วยแสงได้ดีที่สุด",
     ("แสงสีเขียวใช้ในการสังเคราะห์ด้วยแสงได้ดีที่สุด เพราะใบมีสีเขียว", "แบคทีเรียสังเคราะห์ด้วยแสงแทนสาหร่าย", "แสงทุกสีใช้ในการสังเคราะห์ด้วยแสงได้ดีเท่ากันทุกความยาวคลื่น")),
    ("การทดลองของฮิลล์ชี้ว่าการสังเคราะห์ด้วยแสงมีกี่ขั้นตอนหลัก", "ปฏิกิริยาที่ใช้แสงปล่อย O₂ แยกจากขั้นตอนที่ตรึง CO₂",
     ("มีเพียงขั้นตอนเดียวที่ต้องใช้ CO₂ ตลอด", "ปฏิกิริยาที่ใช้แสงตรึง CO₂ และปล่อย O₂ ในขั้นตอนเดียวกัน", "O₂ ได้จากการสลาย CO₂ ในคลอโรพลาสต์")),
    ("ข้อสรุปของฟาน เฮลมอนต์ผิดพลาดในส่วนใด", "ไม่ได้คำนึงถึงแก๊สในอากาศ ซึ่งเป็นแหล่งคาร์บอนของพืช",
     ("ไม่ได้คำนึงถึงน้ำที่รดลงไป ซึ่งถูกเปลี่ยนเป็นดินทั้งหมด", "ต้นหลิวไม่ได้หนักขึ้นจริง", "ไม่ได้คำนึงถึงดินที่หายไป ซึ่งเป็นแหล่งคาร์บอนของพืช")),
    ("การทดลองของพริสต์ลีย์ที่ใส่หนูกับพืชไว้ในครอบแก้วแสดงว่าอะไร", "พืชสร้างแก๊สที่ช่วยให้สัตว์หายใจได้",
     ("หนูสร้างแก๊สที่พืชใช้เพียงอย่างเดียว", "พืชและหนูใช้แก๊สเดียวกันจนหมด", "พืชและหนูหายใจด้วยแก๊สคนละชนิด")),
    ('คัลวินใช้ CO₂ ที่มีคาร์บอนกัมมันตรังสีติดตามเส้นทางของคาร์บอนในสาหร่าย สรุปได้ว่าอะไร', 'คาร์บอนจาก CO₂ ถูกตรึงเข้าสู่สารอินทรีย์ผ่านวัฏจักรของปฏิกิริยาที่เรียกว่าวัฏจักรคัลวิน',
     ('คาร์บอนจาก CO₂ ถูกปล่อยออกมาเป็นแก๊สออกซิเจนทั้งหมด', 'คาร์บอนในน้ำตาลมาจากน้ำ ไม่ได้มาจาก CO₂', 'CO₂ ไม่ได้ถูกใช้ในการสังเคราะห์ด้วยแสงเลย')),
    ('เดอ โซซูร์ชั่งมวลของพืชและแก๊สที่พืชได้รับอย่างละเอียด สรุปได้ว่าอะไร', 'น้ำเป็นสารตั้งต้นอีกชนิดหนึ่ง เพราะมวลที่พืชเพิ่มขึ้นมากกว่ามวลของ CO₂ ที่ได้รับ',
     ('ดินเป็นแหล่งมวลทั้งหมดของพืช เพราะดินในกระถางหายไปมาก', 'พืชไม่ได้ใช้ CO₂ เลย มวลที่เพิ่มมาจากแสงเท่านั้น', 'มวลของพืชเพิ่มขึ้นน้อยกว่ามวลของ CO₂ ที่ได้รับเสมอ')),
)


@question_type(
    "biology.photosynthesis_history_foundation",
    display_name={"th": "ผลงานของนักวิทยาศาสตร์ที่ศึกษาการสังเคราะห์ด้วยแสง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_HISTORY,
)
class PhotosynthesisHistoryFoundation(QuestionType):
    """Whose experiment, both ways."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        who, what = rng.choice(SCIENTISTS)
        others = rng.sample([s for s in SCIENTISTS if s[0] != who], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"\"{what}\" เป็นผลการศึกษาของใคร", correct=who, wrongs=tuple(s[0] for s in others),
                             topic=TOPIC_HISTORY, hint=HISTORY_HINT)
        return _labelled(stem=f"ข้อใดเป็นผลการศึกษาของ{who}", correct=what, wrongs=tuple(s[1] for s in others), topic=TOPIC_HISTORY,
                         hint=HISTORY_HINT)


@question_type(
    "biology.photosynthesis_history_fluency",
    display_name={"th": "ข้อสรุปจากการทดลองเกี่ยวกับการสังเคราะห์ด้วยแสง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_HISTORY,
)
class PhotosynthesisHistoryFluency(QuestionType):
    """What each experiment actually lets you conclude."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(CONCLUSIONS)
        pool = [c[1] for c in CONCLUSIONS if c[1] != right]
        return _labelled(stem=stem, correct=right, wrongs=(*rng.sample(wrongs, 2), rng.choice(pool)), topic=TOPIC_HISTORY,
                         hint=HISTORY_HINT)


@question_type(
    "biology.photosynthesis_history_application",
    display_name={"th": "วิเคราะห์ข้อมูลจากการทดลองของฟาน เฮลมอนต์ และการติดฉลาก ¹⁸O"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_HISTORY,
)
class PhotosynthesisHistoryApplication(QuestionType):
    """Mass gained against soil lost; which product carries the label."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.55:
            start = Fraction(rng.randrange(10, 51, 5), 10)
            gain = rng.randrange(30, 101, 5)
            soil = rng.choice((Fraction(1, 20), Fraction(1, 10), Fraction(1, 5), Fraction(1, 4)))
            end = start + gain
            if rng.random() < 0.5:
                return numeric(stem=f"ปลูกต้นหลิวหนัก {show(start)} kg ในดิน 90 kg รดแต่น้ำเป็นเวลา 5 ปี ต้นหลิวหนัก {show(end)} kg "
                                    f"ดินหายไป {show(soil)} kg ต้นหลิวหนักเพิ่มขึ้นกี่กิโลกรัม", answer=gain,
                               wrongs=[end, gain - soil if (gain - soil) != gain else gain + 1, gain + soil], unit="kg",
                               topic=TOPIC_HISTORY, hint="น้ำหนักที่เพิ่ม = น้ำหนักสุดท้าย − น้ำหนักเริ่มต้น")
            share = soil * 100 / gain
            if (share * 100).denominator != 1:
                soil, share = Fraction(gain, 100), Fraction(1)
            return numeric(stem=f"ต้นหลิวหนักเพิ่มขึ้น {gain} kg ขณะที่ดินหายไป {show(soil)} kg น้ำหนักที่มาจากดินคิดเป็นร้อยละเท่าใดของน้ำหนักที่เพิ่มขึ้น",
                           answer=share, wrongs=[100 - share, soil * 100, share * 10], unit="%", topic=TOPIC_HISTORY,
                           hint="ร้อยละ = น้ำหนักดินที่หายไป × 100 ÷ น้ำหนักที่เพิ่มขึ้น")
        labelled = rng.choice(("น้ำ (H₂¹⁸O)", "คาร์บอนไดออกไซด์ (C¹⁸O₂)"))
        right = "แก๊ส O₂ ที่ปล่อยออกมา" if labelled.startswith("น้ำ") else "น้ำตาลและน้ำที่สร้างขึ้นใหม่ ไม่ใช่แก๊ส O₂"
        wrongs = ("น้ำตาลและน้ำที่สร้างขึ้นใหม่ ไม่ใช่แก๊ส O₂" if labelled.startswith("น้ำ") else "แก๊ส O₂ ที่ปล่อยออกมา",
                  "ไม่พบ ¹⁸O ในผลิตภัณฑ์ใดเลย", "พบ ¹⁸O ในผลิตภัณฑ์ทุกชนิดเท่ากัน")
        return _labelled(stem=f"ให้สาหร่ายสังเคราะห์ด้วยแสงโดยใช้{labelled}ที่ติดฉลาก ¹⁸O จะพบ ¹⁸O ในผลิตภัณฑ์ใด", correct=right,
                         wrongs=wrongs, topic=TOPIC_HISTORY, hint="O₂ ที่ปล่อยออกมามาจากการแยกน้ำ ออกซิเจนจาก CO₂ ไปอยู่ในน้ำตาลและน้ำที่สร้างใหม่")
