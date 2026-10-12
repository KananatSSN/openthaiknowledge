"""การออกแบบวิธีแก้ปัญหาด้วยเหตุผลเชิงตรรกะ

วิทยาการคำนวณ · ป.6 · สสวท. พื้นฐาน
Indicators: ว 4.2 ป.6/1

Sets moved here from: technology_t1s5.
"""

from __future__ import annotations

import math
from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.technology_t1s3 import SUBJECT
from otk.sets._support.technology_t1s4 import _near
from otk.sets._support.technology_t1s5 import SIXTH

PROVENANCE = Provenance("original")


DESIGN_TOPIC = "การออกแบบวิธีแก้ปัญหาด้วยเหตุผลเชิงตรรกะ"


#: (a device to design, the rule it should follow, five that would fail).
#: Wrong conditions are complete rules too. Only one per row is a slip of
#: the right rule (branches swapped, "or" for "and"); with several, the right
#: rule is the one every other choice resembles, which gives it away.
DESIGNS = (
    ("ระบบรดน้ำต้นไม้อัตโนมัติ",
     "ถ้าดินแห้ง ให้รดน้ำ ถ้าดินยังชื้น ไม่ต้องรด",
     ("ถ้าดินแห้ง ไม่ต้องรด ถ้าดินชื้น ให้รดน้ำ",
      "รดน้ำทุก 10 นาทีทั้งวัน โดยไม่ต้องวัดดิน",
      "ถ้าฝนตก ให้รดน้ำเพิ่มเป็นสองเท่าของปกติ",
      "รอจนต้นไม้เหี่ยวก่อน แล้วจึงเปิดน้ำรดทีเดียว",
      "รดน้ำเฉพาะเมื่อมีคนกดปุ่มเท่านั้นทุกครั้ง")),
    ("ไฟทางเดินอัตโนมัติ",
     "ถ้ามืดและมีคนเดินผ่าน ให้เปิดไฟ ถ้าสว่างหรือไม่มีคน ให้ปิดไฟ",
     ("ถ้ามืดหรือมีคนเดินผ่าน ให้เปิดไฟ ถ้าสว่างและไม่มีคน ให้ปิดไฟ",
      "เปิดไฟทุกดวงตลอดเวลาทั้งกลางวันและกลางคืน เพื่อความปลอดภัยสูงสุด",
      "เปิดไฟตั้งแต่ 06.00 น. ถึง 18.00 น. ของทุกวัน แล้วปิดไฟในเวลาอื่น",
      "ปิดไฟทุกดวงตลอดเวลาเพื่อประหยัดไฟฟ้า แล้วให้คนเดินใช้ไฟฉายเอง",
      "เปิดไฟเมื่อมีเสียงดังผ่านเซนเซอร์ แล้วเปิดค้างไว้ไปจนถึงเช้าวันรุ่งขึ้น")),
    ("ประตูที่เปิดด้วยรหัส",
     "ถ้ารหัสที่กดตรงกับรหัสที่ตั้งไว้ ให้เปิดประตู ถ้าไม่ตรง ให้ประตูล็อกไว้",
     ("ถ้ารหัสที่กดไม่ตรงกับรหัสที่ตั้งไว้ ให้เปิดประตู ถ้าตรง ให้ประตูล็อกไว้",
      "เปิดประตูทุกครั้งที่มีคนกดปุ่มใดก็ได้ เพื่อให้ทุกคนเข้าออกได้สะดวกที่สุด",
      "เปิดประตูเมื่อกดปุ่มครบสามครั้ง ไม่ว่าตัวเลขที่กดจะเป็นตัวเลขใดก็ตาม",
      "ล็อกประตูไว้ตลอดเวลาแม้กดรหัสถูก แล้วให้เจ้าของใช้กุญแจเปิดประตูแทน",
      "เปิดประตูเมื่อมีคนยืนอยู่หน้าประตูนานเกินสิบวินาที โดยไม่ต้องกดรหัสใดเลย")),
    ("แอปพลิเคชันเตือนให้ดื่มน้ำ",
     "ถ้าผ่านไปหนึ่งชั่วโมงแล้วยังไม่ได้บันทึกว่าดื่มน้ำ ให้แจ้งเตือน",
     ("ถ้าผ่านไปหนึ่งชั่วโมงแล้วบันทึกว่าดื่มน้ำแล้ว ให้แจ้งเตือน",
      "แจ้งเตือนทุกหนึ่งนาทีตลอดทั้งวัน แม้ผู้ใช้จะดื่มน้ำไปแล้ว",
      "ไม่แจ้งเตือนเลย จนกว่าผู้ใช้จะเปิดแอปขึ้นมาดูด้วยตนเอง",
      "แจ้งเตือนเฉพาะตอนเที่ยงคืน ซึ่งเป็นเวลาที่ผู้ใช้นอนหลับอยู่",
      "แจ้งเตือนเมื่อผู้ใช้บันทึกว่าดื่มน้ำครบแปดแก้ว แล้วหยุดแจ้งทั้งวัน")),
    ("การจัดคิวใช้คอมพิวเตอร์ในห้องสมุด",
     "ให้คนที่มาถึงก่อนได้ใช้ก่อน และเมื่อใช้ครบ 20 นาทีแล้วให้สลับให้คนถัดไป",
     ("ให้คนที่มาถึงหลังสุดได้ใช้ก่อน และเมื่อใช้ครบ 20 นาทีแล้วให้สลับคนถัดไป",
      "ให้คนที่นั่งใกล้เครื่องที่สุดได้ใช้ และใช้ต่อไปได้จนกว่าจะเลิกใช้เอง",
      "ให้ทุกคนที่มาถึงแย่งกันใช้เครื่อง ใครเข้าถึงเครื่องได้ก่อนก็ใช้ได้เลย",
      "ให้คนที่อายุมากที่สุดใช้ทั้งวัน ส่วนคนอื่นรอจนห้องสมุดใกล้ปิดทำการ",
      "จับฉลากทุกเช้าว่าใครได้ใช้ทั้งวัน ส่วนคนที่ไม่ได้ให้กลับมาใหม่ในวันพรุ่งนี้")),
    ("พัดลมที่ทำงานเองตามอุณหภูมิห้อง",
     "ถ้าอุณหภูมิห้องสูงกว่า 30 องศาเซลเซียส ให้เปิดพัดลม ถ้าไม่สูงกว่า ให้ปิดพัดลม",
     ("ถ้าอุณหภูมิห้องสูงกว่า 30 องศาเซลเซียส ให้ปิดพัดลม ถ้าไม่สูงกว่า ให้เปิดพัดลม",
      "เปิดพัดลมแรงที่สุดตลอดเวลาทั้งกลางวันและกลางคืน โดยไม่ต้องวัดอุณหภูมิห้องเลย",
      "เปิดพัดลมเฉพาะเวลาที่ไม่มีคนอยู่ในห้อง และปิดพัดลมทันทีเมื่อมีคนเดินเข้ามา",
      "เปิดพัดลมทุกวันตั้งแต่ 08.00 น. ถึง 09.00 น. เพียงหนึ่งชั่วโมงแล้วปิดทั้งวัน",
      "เปิดพัดลมเมื่อมีคนกดรีโมตเท่านั้น และปิดเองเมื่อครบสองชั่วโมงไม่ว่าอากาศจะร้อนหรือไม่")),
)


HALVING_HINT = ("ทายเลขตรงกลางของช่วงที่เหลือ คือ (เลขต่ำสุด + เลขสูงสุด) ÷ 2 แล้วปัดเศษทิ้ง "
                "ถ้าได้ยินว่า มากกว่า ช่วงใหม่เริ่มจากเลขที่ทายบวก 1 ถ้าได้ยินว่า น้อยกว่า "
                "ช่วงใหม่จบที่เลขที่ทายลบ 1")


def middle(low: int, high: int) -> int:
    return (low + high) // 2


def most_guesses(top: int) -> int:
    """Worst case of halving 1..top: the smallest k with 2**k - 1 >= top."""
    return math.ceil(math.log2(top + 1))


@question_type(
    "comp.logic_design_foundation",
    display_name={"th": "ออกแบบเงื่อนไขการทำงานเพื่อแก้ปัญหาในชีวิตประจำวัน"},
    level=SIXTH, subject=SUBJECT, topic=DESIGN_TOPIC,
)
class LogicDesignFoundation(QuestionType):
    def build(self, rng: Random, **params):
        device, rule, wrongs = rng.choice(DESIGNS)
        return _labelled(
            stem=f"ต้องการออกแบบ{device} เงื่อนไขการทำงานข้อใดเหมาะสมที่สุด",
            correct=rule, wrongs=tuple(wrongs),
            hint="เงื่อนไขที่ดีตรวจสิ่งที่เป็นต้นเหตุของปัญหา แล้วบอกให้ชัดว่าทำอะไรเมื่อจริงและเมื่อไม่จริง",
            topic=DESIGN_TOPIC,
        )


@question_type(
    "comp.logic_design_fluency",
    display_name={"th": "ทายเลขด้วยการแบ่งครึ่งช่วง"},
    level=SIXTH, subject=SUBJECT, topic=DESIGN_TOPIC,
)
class LogicDesignFluency(QuestionType):
    """Trace one step of halving a range."""
    invent_numbers = True  # computed answer: near values on the short side cannot be right

    def build(self, rng: Random, **params):
        top = rng.choice((16, 20, 25, 30, 40, 50, 60, 64, 80, 100))
        first = middle(1, top)
        secret = rng.choice([n for n in range(1, top + 1) if n != first])
        higher = secret > first
        low, high = (first + 1, top) if higher else (1, first - 1)
        second = middle(low, high)
        wrongs = _near(second, (middle(1, first) if higher else middle(first, top),
                                (low + high + 1) // 2, first + 1 if higher else first - 1))
        return _labelled(
            stem=(f"เพื่อนคิดเลขไว้หนึ่งจำนวนตั้งแต่ 1 ถึง {top} เราทายเลขตรงกลางทุกครั้ง "
                  f"โดยใช้ (เลขต่ำสุด + เลขสูงสุด) ÷ 2 ปัดเศษทิ้ง ครั้งแรกทาย {first} "
                  f"เพื่อนตอบว่า เลขที่คิด{'มากกว่า' if higher else 'น้อยกว่า'} {first} ครั้งที่สองควรทายเลขใด"),
            correct=str(second), wrongs=tuple(str(w) for w in rng.sample(wrongs, 3)),
            hint=HALVING_HINT, topic=DESIGN_TOPIC,
        )


@question_type(
    "comp.logic_design_application",
    display_name={"th": "เปรียบเทียบวิธีแก้ปัญหาด้วยจำนวนครั้งที่ต้องทาย"},
    level=SIXTH, subject=SUBJECT, topic=DESIGN_TOPIC,
)
class LogicDesignApplication(QuestionType):
    """How many guesses halving needs at most, and how that beats counting up."""

    def build(self, rng: Random, **params):
        top = rng.choice((7, 15, 16, 20, 31, 32, 50, 63, 100))
        halving = most_guesses(top)
        if rng.random() < 0.5:
            return _labelled(
                stem=(f"เพื่อนคิดเลขไว้หนึ่งจำนวนตั้งแต่ 1 ถึง {top} และบอกได้ว่าเลขที่ทาย "
                      f"มากกว่า น้อยกว่า หรือถูกต้อง ถ้าทายเลขตรงกลางของช่วงที่เหลือทุกครั้ง "
                      f"ต้องทายอย่างมากกี่ครั้งจึงจะได้คำตอบแน่นอน"),
                correct=f"{halving} ครั้ง",
                wrongs=tuple(f"{w} ครั้ง" for w in rng.sample(
                    _near(halving, (top, top // 2, halving + 1, halving - 1)), 3)),
                hint=("ทายหนึ่งครั้งตัดช่วงเหลือไม่ถึงครึ่ง ทาย k ครั้งจึงหาเลขได้จากช่วงยาวถึง "
                      "2 ยกกำลัง k ลบ 1 จำนวน"),
                topic=DESIGN_TOPIC,
            )
        saved = top - halving
        return _labelled(
            stem=(f"เพื่อนคิดเลขไว้หนึ่งจำนวนตั้งแต่ 1 ถึง {top} วิธีที่หนึ่งทายเรียงจาก 1 ขึ้นไปทีละตัว "
                  f"วิธีที่สองทายเลขตรงกลางของช่วงที่เหลือทุกครั้ง โดยเพื่อนบอกได้ว่ามากกว่าหรือน้อยกว่า "
                  f"ในกรณีที่ต้องทายมากที่สุด วิธีที่สองทายน้อยกว่าวิธีที่หนึ่งกี่ครั้ง"),
            correct=f"{saved} ครั้ง",
            wrongs=tuple(f"{w} ครั้ง" for w in rng.sample(
                _near(saved, (top - halving - 1, top // 2, top - halving + 1, halving)), 3)),
            hint=(f"ทายทีละตัวอาจต้องทายถึง {top} ครั้ง ส่วนการแบ่งครึ่งต้องทายอย่างมาก k ครั้ง "
                  f"เมื่อ k เป็นจำนวนน้อยที่สุดที่ 2 ยกกำลัง k ลบ 1 ไม่น้อยกว่า {top}"),
            topic=DESIGN_TOPIC,
        )
