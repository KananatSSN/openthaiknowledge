"""การเปลี่ยนแปลงที่ผันกลับได้และผันกลับไม่ได้

เคมี · ป.5 · สสวท. พื้นฐาน
Indicators: ว 2.1 ป.5/4

Sets moved here from: science_wave_d6.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d1 import SUBJECT
from otk.sets._support.science_wave_d6 import FIFTH

PROVENANCE = Provenance("original")


REVERSIBLE_TOPIC = "การเปลี่ยนแปลงที่ผันกลับได้และผันกลับไม่ได้"


REVERSIBLE = (
    "น้ำแข็งละลายเป็นน้ำ", "น้ำระเหยเป็นไอน้ำ", "เทียนไขหลอมเหลว", "เกลือละลายในน้ำ", "ช็อกโกแลตละลาย",
    "น้ำเย็นลงจนเป็นน้ำแข็ง", "ไอน้ำควบแน่นเป็นหยดน้ำ", "เนยแข็งตัวในตู้เย็น",
)


IRREVERSIBLE = (
    "เผากระดาษจนเป็นเถ้า", "ทอดไข่", "ตะปูเหล็กเป็นสนิม", "กล้วยสุกจนเน่า", "ปูนซีเมนต์ที่ผสมน้ำแล้วแข็งตัว",
    "จุดไม้ขีดไฟ", "ต้มไข่จนสุก", "เผาถ่านจนเป็นเถ้า",
)


REVERSIBLE_REASON = "ไม่เกิดสารใหม่ จึงทำให้กลับเป็นสารเดิมได้"


IRREVERSIBLE_REASON = "เกิดสารใหม่ จึงทำให้กลับเป็นสารเดิมไม่ได้"


def _sorted(back: list[str], stay: list[str]) -> str:
    return f"ผันกลับได้: {', '.join(back)} / ผันกลับไม่ได้: {', '.join(stay)}"


REVERSIBLE_SCENARIOS = (
    ("เทียนไขที่หลอมเหลวไหลลงมาแล้วแข็งตัวอีกครั้ง แต่ไส้เทียนที่ไหม้กลายเป็นสีดำ ข้อใดวิเคราะห์ได้ถูกต้อง",
     "เนื้อเทียนหลอมเหลวแล้วแข็งตัวเป็นการเปลี่ยนแปลงที่ผันกลับได้ ส่วนไส้เทียนไหม้เป็นการเปลี่ยนแปลงที่ผันกลับไม่ได้",
     ("ทั้งสองอย่างผันกลับได้",
      "ทั้งสองอย่างผันกลับไม่ได้",
      "เนื้อเทียนหลอมเหลวผันกลับไม่ได้ ส่วนไส้เทียนไหม้ผันกลับได้",
      "เนื้อเทียนหลอมเหลวเกิดสารใหม่ จึงผันกลับไม่ได้",
      "ไส้เทียนไหม้ผันกลับได้เมื่อเทียนเย็นลง")),
    ("ร้านขายน้ำแข็งเก็บน้ำแข็งที่ละลายไปแช่แข็งใหม่ได้ แต่ร้านขนมปังนำขนมปังที่อบแล้วกลับไปเป็นแป้งไม่ได้ เพราะเหตุใด",
     "น้ำแข็งละลายเป็นการเปลี่ยนสถานะที่ผันกลับได้ ส่วนการอบขนมปังเกิดสารใหม่จึงผันกลับไม่ได้",
     ("น้ำแข็งเกิดสารใหม่ ส่วนขนมปังไม่เกิดสารใหม่",
      "ร้านขนมปังไม่มีตู้แช่แข็ง",
      "ขนมปังผันกลับได้ถ้าทิ้งไว้นานพอ",
      "การอบขนมปังเป็นการเปลี่ยนสถานะเหมือนน้ำแข็งละลาย",
      "น้ำแข็งที่ละลายแล้วแช่แข็งใหม่ไม่ได้")),
    ("นักเรียนละลายน้ำตาลในน้ำ แล้วอ้างว่าเป็นการเปลี่ยนแปลงที่ผันกลับไม่ได้ เพราะมองไม่เห็นน้ำตาลแล้ว ข้อใดโต้แย้งได้ดีที่สุด",
     "ถ้าระเหยน้ำออกจะได้น้ำตาลกลับคืนมา การละลายจึงเป็นการเปลี่ยนแปลงที่ผันกลับได้",
     ("ข้ออ้างถูกต้อง เพราะสิ่งที่มองไม่เห็นกลับคืนไม่ได้",
      "น้ำตาลกลายเป็นน้ำ จึงผันกลับไม่ได้",
      "การละลายเกิดสารใหม่เสมอ",
      "น้ำตาลเปลี่ยนเป็นสารใหม่ที่มองไม่เห็น",
      "ต้องเผาน้ำเชื่อมจึงจะได้น้ำตาลกลับคืนเหมือนเดิม")),
    ("ช็อกโกแลตในกระเป๋าละลายเมื่ออากาศร้อน เมื่อนำไปแช่ตู้เย็นก็แข็งตัวอีกครั้ง ข้อใดวิเคราะห์ได้ถูกต้อง",
     "เป็นการเปลี่ยนแปลงที่ผันกลับได้ เพราะช็อกโกแลตเปลี่ยนสถานะแล้วกลับเป็นสารเดิม",
     ("เป็นการเปลี่ยนแปลงที่ผันกลับไม่ได้ เพราะรูปร่างเปลี่ยนไป",
      "เกิดสารใหม่ เพราะช็อกโกแลตละลาย",
      "ช็อกโกแลตกลายเป็นน้ำตาลเมื่อแช่เย็น",
      "เป็นการเปลี่ยนแปลงทางเคมี เพราะอุณหภูมิเปลี่ยน",
      "ผันกลับไม่ได้ เพราะช็อกโกแลตที่แข็งตัวใหม่ไม่ใช่ช็อกโกแลต")),
    ("ผสมปูนซีเมนต์กับน้ำแล้วทิ้งไว้จนแข็งตัว เพื่อนบอกว่าถ้าทุบให้แตกจะได้ผงปูนซีเมนต์เดิมกลับคืน ข้อใดโต้แย้งได้ดีที่สุด",
     "ปูนที่แข็งตัวเกิดสารใหม่แล้ว การทุบได้เพียงเศษปูนแข็ง ไม่ใช่ผงปูนซีเมนต์เดิม จึงผันกลับไม่ได้",
     ("ข้ออ้างถูกต้อง เพราะผงที่ได้เหมือนผงเดิมทุกประการ",
      "ปูนแข็งตัวเพราะน้ำระเหยเท่านั้น จึงผันกลับได้",
      "ถ้าเติมน้ำลงไปอีก ปูนจะกลับเป็นผงเดิม",
      "ปูนแข็งตัวเป็นการละลาย จึงผันกลับได้",
      "การทุบทำให้เกิดปูนซีเมนต์ผงเดิมขึ้นใหม่")),
)


@question_type(
    "chem.reversible_change_foundation",
    display_name={"th": "ระบุว่าการเปลี่ยนแปลงผันกลับได้หรือไม่"},
    level=FIFTH, subject=SUBJECT, topic=REVERSIBLE_TOPIC,
)
class ReversibleChangeFoundation(QuestionType):
    """One change; which kind it is, and why."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        back = rng.random() < 0.5
        change = rng.choice(REVERSIBLE if back else IRREVERSIBLE)
        right = f"ผันกลับได้ เพราะ{REVERSIBLE_REASON}" if back else f"ผันกลับไม่ได้ เพราะ{IRREVERSIBLE_REASON}"
        return _labelled(
            stem=f"\"{change}\" เป็นการเปลี่ยนแปลงแบบใด",
            correct=right,
            wrongs=(f"ผันกลับไม่ได้ เพราะ{IRREVERSIBLE_REASON}" if back else f"ผันกลับได้ เพราะ{REVERSIBLE_REASON}",
                    "ผันกลับได้ เพราะเกิดสารใหม่" if back else "ผันกลับไม่ได้ เพราะไม่เกิดสารใหม่",
                    "ไม่ใช่การเปลี่ยนแปลง เพราะสารยังอยู่ในภาชนะเดิม",
                    "ไม่ใช่การเปลี่ยนแปลง เพราะมวลของสารไม่เปลี่ยน",
                    "บอกไม่ได้ เพราะขึ้นกับสีของสารเท่านั้น"),
            hint="ถามว่าทำให้กลับเป็นสารเดิมได้หรือไม่ ถ้าเกิดสารใหม่มักผันกลับไม่ได้",
            topic=REVERSIBLE_TOPIC,
        )


@question_type(
    "chem.reversible_change_fluency",
    display_name={"th": "วิเคราะห์และจัดกลุ่มการเปลี่ยนแปลงที่ผันกลับได้และผันกลับไม่ได้"},
    level=FIFTH, subject=SUBJECT, topic=REVERSIBLE_TOPIC,
)
class ReversibleChangeFluency(QuestionType):
    """Five changes; sort every one into reversible or not."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        count = rng.choice((2, 3))
        chosen = rng.sample(REVERSIBLE, count) + rng.sample(IRREVERSIBLE, 5 - count)
        rng.shuffle(chosen)
        back = [c for c in chosen if c in REVERSIBLE]
        stay = [c for c in chosen if c in IRREVERSIBLE]
        wrongs = []
        for item in rng.sample(chosen, 3):
            if item in back:
                wrongs.append(_sorted([c for c in back if c != item], stay + [item]))
            else:
                wrongs.append(_sorted(back + [item], [c for c in stay if c != item]))
        # Two changes misplaced at once, so the answer is not the grouping
        # every wrong differs from by a single move.
        for pair in (rng.sample(chosen, 2) for _ in range(2)):
            moved = set(pair)
            wrongs.append(_sorted([c for c in back if c not in moved] + [c for c in stay if c in moved],
                                  [c for c in stay if c not in moved] + [c for c in back if c in moved]))
        wrongs = list(dict.fromkeys(wrongs))
        return _labelled(
            stem=(f"การเปลี่ยนแปลงต่อไปนี้ ได้แก่ {', '.join(chosen)} "
                  "ข้อใดวิเคราะห์และจัดกลุ่มการเปลี่ยนแปลงได้ถูกต้อง"),
            correct=_sorted(back, stay),
            wrongs=tuple(wrongs),
            hint="ถามทีละข้อว่าทำให้กลับเป็นสารเดิมได้หรือไม่",
            topic=REVERSIBLE_TOPIC,
        )


@question_type(
    "chem.reversible_change_application",
    display_name={"th": "วิเคราะห์การเปลี่ยนแปลงที่ผันกลับได้และไม่ได้ในสถานการณ์จริง"},
    level=FIFTH, subject=SUBJECT, topic=REVERSIBLE_TOPIC,
)
class ReversibleChangeApplication(QuestionType):
    """A burning candle, ice against bread, and a claim about dissolved sugar."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, REVERSIBLE_SCENARIOS,
            hint="แยกการเปลี่ยนแปลงแต่ละส่วน แล้วถามว่ากลับเป็นสารเดิมได้หรือไม่",
        ), REVERSIBLE_TOPIC)


# More rows: the set drew from five, so a learner met them all in a few
# tries. Each added row is a situation no other row describes, since every
# row's answer is a distractor for the others, and has five wrong readings.
REVERSIBLE_SCENARIOS += (
    ('ตากผ้าเปียกจนแห้ง แล้วผ้าเปียกฝนอีกครั้ง การเปลี่ยนแปลงของน้ำในผ้าเป็นแบบใด',
     'ผันกลับได้ เพราะน้ำระเหยไปแล้วผ้าก็เปียกน้ำได้อีก',
     ('ผันกลับไม่ได้ เพราะผ้ากลายเป็นสารใหม่', 'ผันกลับไม่ได้ เพราะน้ำหายไปจากโลก', 'เป็นการเปลี่ยนแปลงทางเคมี', 'ผ้าเปลี่ยนเป็นกระดาษ', 'ไม่มีการเปลี่ยนแปลงเกิดขึ้น')),
    ('ไข่ที่ต้มสุกแล้วจะกลับเป็นไข่ดิบได้หรือไม่ เพราะเหตุใด',
     'ไม่ได้ เพราะความร้อนทำให้ไข่เปลี่ยนเป็นสารที่มีสมบัติใหม่',
     ('ได้ ถ้าแช่ไข่ในน้ำเย็น', 'ได้ ถ้าตั้งทิ้งไว้ข้ามคืน', 'ได้ เพราะไข่แค่เปลี่ยนสถานะ', 'ได้ ถ้าเขย่าไข่แรง ๆ', 'ไม่ได้ เพราะไข่ระเหยไปหมด')),
    ('การหลอมเหล็กให้เป็นของเหลวแล้วเทลงแม่พิมพ์ให้เย็นเป็นรูปใหม่ เป็นการเปลี่ยนแปลงแบบใด',
     'ผันกลับได้ เพราะเป็นการเปลี่ยนสถานะของเหล็ก เหล็กยังเป็นเหล็ก',
     ('ผันกลับไม่ได้ เพราะเหล็กเปลี่ยนเป็นสารใหม่', 'เป็นการเกิดสนิม', 'เหล็กกลายเป็นทองแดง', 'เป็นการเผาไหม้ของเหล็ก', 'เหล็กหายไปไม่เหลือ')),
    ('ข้าวเหนียวมะม่วงที่บูดมีกลิ่นเปรี้ยว นำไปแช่เย็นจะกลับมาสดเหมือนเดิมหรือไม่',
     'ไม่ได้ เพราะการบูดเป็นการเปลี่ยนแปลงที่เกิดสารใหม่ ผันกลับไม่ได้',
     ('ได้ เพราะความเย็นทำให้สดเหมือนเดิม', 'ได้ ถ้าแช่นานพอ', 'ได้ เพราะการบูดเป็นการละลาย', 'ได้ ถ้าใส่น้ำตาลเพิ่ม', 'ไม่ได้ เพราะข้าวเหนียวกลายเป็นน้ำแข็ง')),
)
