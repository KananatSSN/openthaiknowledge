"""การถ่ายทอดพลังงานในระบบนิเวศ

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 5 ม.6/1

Sets moved here from: science_wave_f70.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f70 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_ENERGY = "การถ่ายทอดพลังงานในระบบนิเวศ"


CHAINS = (("หญ้า", "ตั๊กแตน", "กบ", "งู", "เหยี่ยว"), ("สาหร่าย", "ไรน้ำ", "ลูกปลา", "ปลาช่อน", "นกกระเต็น"),
          ("ข้าว", "หนู", "งู", "เหยี่ยว"), ("แพลงก์ตอนพืช", "แพลงก์ตอนสัตว์", "ปลาเล็ก", "ปลาใหญ่"))


ENERGY_HINT = ("ผู้ผลิตตรึงพลังงานจากแสง พลังงานถ่ายทอดไปลำดับถัดไปประมาณร้อยละ 10 ที่เหลือสูญเสียเป็นความร้อนจากการหายใจ "
               "และอยู่ในส่วนที่ไม่ถูกกิน พีระมิดพลังงานจึงมีฐานกว้างเสมอ")


@question_type(
    "biology.energy_flow_foundation",
    display_name={"th": "ลำดับขั้นการกินในโซ่อาหาร"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_ENERGY,
)
class EnergyFlowFoundation(QuestionType):
    """Producers, consumers of each order, and decomposers."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        chain = rng.choice(CHAINS)
        roles = ("ผู้ผลิต", "ผู้บริโภคลำดับที่ 1", "ผู้บริโภคลำดับที่ 2", "ผู้บริโภคลำดับที่ 3", "ผู้บริโภคลำดับที่ 4")
        i = rng.randrange(len(chain))
        text = " → ".join(chain)
        if rng.random() < 0.6:
            pool = [r for r in roles + ("ผู้ย่อยสลาย",) if r != roles[i]]
            return _labelled(stem=f"ในโซ่อาหาร {text} {chain[i]}อยู่ในลำดับขั้นใด", correct=roles[i], wrongs=tuple(pool),
                             topic=TOPIC_ENERGY, hint=ENERGY_HINT)
        facts = (("สิ่งมีชีวิตกลุ่มใดเปลี่ยนพลังงานแสงเป็นพลังงานเคมีในระบบนิเวศ", "ผู้ผลิต", ("ผู้บริโภคพืช", "ผู้บริโภคสัตว์", "ผู้ย่อยสลาย", "ผู้บริโภคที่กินทั้งพืชและสัตว์")),
                 ("ผู้ย่อยสลาย เช่น เห็ดราและแบคทีเรีย มีบทบาทอย่างไร", "ย่อยซากสิ่งมีชีวิตให้ธาตุอาหารกลับคืนสู่ระบบนิเวศ",
                  ("สร้างอาหารจากแสง", "เป็นผู้ล่าลำดับสูงสุด", "ทำให้พลังงานหมุนเวียนกลับไปเป็นแสง", "ตรึงแก๊สออกซิเจนจากอากาศ")),
                 ("เหตุใดโซ่อาหารส่วนใหญ่จึงมีลำดับขั้นไม่เกิน 4-5 ลำดับ", "พลังงานลดลงมากในแต่ละลำดับจนไม่พอเลี้ยงลำดับถัดไป",
                  ("สัตว์ผู้ล่ามีจำนวนมากเกินไป", "ผู้ผลิตมีพลังงานน้อยที่สุด", "พลังงานเพิ่มขึ้นทุกลำดับจนเกินพอ", "ผู้ย่อยสลายกินผู้ล่าทั้งหมด")))
        stem, right, wrongs = rng.choice(facts)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_ENERGY, hint=ENERGY_HINT)


@question_type(
    "biology.energy_flow_fluency",
    display_name={"th": "พีระมิดจำนวน มวลชีวภาพ และพลังงาน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_ENERGY,
)
class EnergyFlowFluency(QuestionType):
    """Only the energy pyramid is never inverted."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        facts = (
            ("พีระมิดชนิดใดมีฐานกว้างเสมอและไม่มีทางกลับหัว", "พีระมิดพลังงาน", ("พีระมิดจำนวน", "พีระมิดมวลชีวภาพ", "ทุกชนิดกลับหัวได้")),
            ("ต้นมะม่วงหนึ่งต้นมีเพลี้ยหลายพันตัวอาศัยอยู่ พีระมิดจำนวนของระบบนี้มีลักษณะอย่างไร", "ฐานแคบกว่าชั้นถัดไป (กลับหัว)",
             ("ฐานกว้างที่สุดเสมอ", "ทุกชั้นกว้างเท่ากัน", "ไม่สามารถเขียนได้")),
            ("ในแหล่งน้ำบางแห่ง มวลของแพลงก์ตอนพืชน้อยกว่ามวลของแพลงก์ตอนสัตว์ในขณะหนึ่งได้เพราะเหตุใด",
             "แพลงก์ตอนพืชเพิ่มจำนวนเร็วมากและถูกกินอย่างรวดเร็ว", ("แพลงก์ตอนสัตว์เป็นผู้ผลิต", "พลังงานเพิ่มขึ้นในลำดับถัดไป", "แพลงก์ตอนพืชไม่ถูกกิน")),
            ("พลังงานส่วนใหญ่ที่ไม่ถูกถ่ายทอดไปยังลำดับถัดไปสูญเสียไปอย่างไร", "เป็นความร้อนจากการหายใจและอยู่ในส่วนที่ไม่ถูกกินหรือย่อยไม่ได้",
             ("ถูกเก็บไว้ในผู้ผลิตตลอดไป", "เปลี่ยนกลับเป็นแสง", "ถูกผู้บริโภคลำดับสุดท้ายเก็บไว้ทั้งหมด")),
            ('ถ้าผู้ผลิตตรึงพลังงานได้ 10,000 หน่วย ผู้บริโภคลำดับที่สองจะได้รับพลังงานประมาณกี่หน่วยตามกฎสิบเปอร์เซ็นต์', '100 หน่วย',
             ('1,000 หน่วย', '10 หน่วย', '5,000 หน่วย')),
            ('เหตุใดโซ่อาหารส่วนใหญ่จึงมีเพียง 4 ถึง 5 ลำดับขั้น', 'พลังงานลดลงมากในแต่ละลำดับ จนไม่พอเลี้ยงลำดับที่สูงขึ้นไปอีก',
             ('ผู้บริโภคลำดับสูงไม่ต้องใช้พลังงานในการดำรงชีวิต จึงไม่จำเป็นต้องมีลำดับเพิ่ม', 'สัตว์ผู้ล่ามีอายุสั้นเกินกว่าจะกินเหยื่อได้ครบทุกลำดับในโซ่อาหารเดียวกัน', 'พลังงานเพิ่มขึ้นในแต่ละลำดับจนผู้บริโภคลำดับสูงใช้ไม่หมดและต้องหยุดกิน')),
            ('พีระมิดมวลชีวภาพของป่าดิบมีลักษณะอย่างไร', 'ฐานกว้างที่สุด เพราะมวลของต้นไม้มากกว่าผู้บริโภคทุกลำดับ',
             ('กลับหัว เพราะมวลรวมของสัตว์ทุกชนิดในป่ามากกว่ามวลของต้นไม้ทั้งหมด', 'ทุกชั้นกว้างเท่ากัน เพราะมวลถูกถ่ายทอดไปยังลำดับถัดไปได้ทั้งหมดไม่มีสูญเสีย', 'ยอดกว้างที่สุด เพราะผู้ล่าลำดับสูงสุดมีขนาดตัวใหญ่ที่สุดในระบบนิเวศ')),
        )
        stem, right, wrongs = rng.choice(facts)
        pool = [r for _, r, _ in facts if r != right]
        return _labelled(stem=stem, correct=right, wrongs=(*rng.sample(wrongs, 2), rng.choice(pool)), topic=TOPIC_ENERGY, hint=ENERGY_HINT)


@question_type(
    "biology.energy_flow_application",
    display_name={"th": "คำนวณพลังงานที่ถ่ายทอดในโซ่อาหาร"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_ENERGY,
)
class EnergyFlowApplication(QuestionType):
    """Multiply by the transfer share at each step."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        chain = rng.choice(CHAINS)
        share = rng.choice((10, 10, 20))
        steps = rng.randint(1, len(chain) - 1)
        base = rng.randrange(1, 100) * 10 ** rng.randint(3, 5)
        energy = Fraction(base) * Fraction(share, 100) ** steps
        text = " → ".join(chain)
        if (energy * 100).denominator != 1:
            base = 10 ** 6
            energy = Fraction(base) * Fraction(share, 100) ** steps
        if rng.random() < 0.6:
            return numeric(stem=f"ในโซ่อาหาร {text} {chain[0]}ตรึงพลังงานได้ {base:,} kJ ถ้าพลังงานถ่ายทอดไปลำดับถัดไปร้อยละ {share} "
                                f"{chain[steps]}ได้รับพลังงานกี่กิโลจูล", answer=energy,
                           wrongs=[energy * Fraction(100, share), energy * Fraction(share, 100) if (energy * Fraction(share, 100) * 100).denominator == 1
                                   else energy * 2, Fraction(base * share, 100)], unit="kJ", topic=TOPIC_ENERGY,
                           hint="พลังงานที่ลำดับถัดไป = พลังงานเดิม × ร้อยละที่ถ่ายทอด ÷ 100 ทำซ้ำตามจำนวนลำดับ")
        return numeric(stem=f"ในโซ่อาหาร {text} {chain[steps]}ได้รับพลังงาน {show(energy)} kJ ถ้าพลังงานถ่ายทอดร้อยละ {share} ต่อลำดับ "
                            f"{chain[0]}ตรึงพลังงานไว้กี่กิโลจูล", answer=base,
                       wrongs=[energy * Fraction(100, share), base * 10, energy * 10], unit="kJ", topic=TOPIC_ENERGY,
                       hint="ย้อนกลับทีละลำดับโดยคูณด้วย 100 ÷ ร้อยละที่ถ่ายทอด")
