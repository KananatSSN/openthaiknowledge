"""ลักษณะและการเกิดเสียงสูง เสียงต่ำ

ฟิสิกส์ · ป.5 · สสวท. พื้นฐาน
Indicators: ว 2.3 ป.5/2

Sets moved here from: science_wave_d24.
"""

from __future__ import annotations

from itertools import permutations
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d24 import FIFTH

PROVENANCE = Provenance("original")


PITCH_TOPIC = "ลักษณะและการเกิดเสียงสูง เสียงต่ำ"


PITCH_PAIRS = (
    ("สายกีตาร์เส้นเล็ก", "สายกีตาร์เส้นใหญ่"), ("สายที่ขึงตึงมาก", "สายเดียวกันที่ขึงหย่อน"), ("สายที่สั้น", "สายชนิดเดียวกันที่ยาว"),
    ("ลูกระนาดที่สั้น", "ลูกระนาดที่ยาว"), ("ไม้บรรทัดที่ยื่นออกจากโต๊ะสั้น", "ไม้บรรทัดที่ยื่นออกจากโต๊ะยาว"),
    ("กลองใบเล็กที่หน้ากลองขึงตึง", "กลองใบใหญ่ที่หน้ากลองหย่อน"), ("ขลุ่ยเมื่อปิดรูน้อย (ลำอากาศสั้น)", "ขลุ่ยเมื่อปิดรูทุกรู (ลำอากาศยาว)"),
    ("หนังยางเส้นเล็กที่ดึงตึง", "หนังยางเส้นใหญ่ที่ดึงหย่อน"),
)


PITCH_FACTS = (
    ("เสียงสูงเกิดจากการสั่นแบบใด", "การสั่นที่ถี่ หรือมีความถี่สูง",
     ("การสั่นที่ห่าง หรือมีความถี่ต่ำ", "การสั่นแรง หรือมีแอมพลิจูดมาก ซึ่งทำให้เสียงดังขึ้น ไม่ใช่เสียงสูงขึ้น", "การสั่นที่มีคาบเวลานาน",
      "การไม่สั่นเลย", "การสั่นที่ช้าลงเรื่อย ๆ")),
    ("เสียงต่ำเกิดจากการสั่นแบบใด", "การสั่นที่ห่าง หรือมีความถี่ต่ำ",
     ("การสั่นที่ถี่ หรือมีความถี่สูง", "การสั่นแรงมาก", "การสั่นเบามาก", "การไม่สั่นเลย", "การสั่นเฉพาะในสุญญากาศ")),
    ("ความถี่ของการสั่นหมายถึงอะไร", "จำนวนครั้งที่วัตถุสั่นครบรอบในหนึ่งวินาที",
     ("ความแรงของการสั่น", "ระยะทางที่เสียงเดินทาง", "ความดังของเสียง", "น้ำหนักของวัตถุที่สั่น", "เวลาที่เสียงดังทั้งหมด")),
)


PITCH_HINT = "สิ่งที่สั่นถี่ (ความถี่สูง) ให้เสียงสูง สายสั้น เล็ก หรือตึง สั่นถี่กว่าสายยาว ใหญ่ หรือหย่อน ความแรงของการสั่นเกี่ยวกับความดัง ไม่ใช่ความสูงต่ำ"


PITCH_STEM_PREFIX = "นักเรียนดีดปลายไม้บรรทัดที่ยื่นออกจากขอบโต๊ะสองความยาว"


PITCH_SCENARIOS = (
    ("กีตาร์มีสายทั้งเส้นเล็กและเส้นใหญ่ขึงตึงเท่ากัน เหตุใดสายเส้นเล็กจึงให้เสียงสูงกว่าสายเส้นใหญ่เมื่อดีด",
     "สายเส้นเล็กสั่นได้ถี่กว่าสายเส้นใหญ่ ความถี่การสั่นที่สูงกว่าจึงให้เสียงสูงกว่า",
     ("สายเส้นเล็กสั่นได้ห่างกว่าสายเส้นใหญ่", "สายเส้นเล็กมีแอมพลิจูดการสั่นมากกว่าจึงเสียงสูงกว่า", "ขนาดของสายไม่มีผลต่อระดับเสียงที่เกิดขึ้น")),
    ("ระนาดมีลูกระนาดยาวสั้นต่างกัน เหตุใดลูกระนาดที่สั้นกว่าจึงให้เสียงสูงกว่าลูกที่ยาวกว่า",
     "ลูกระนาดที่สั้นกว่าสั่นได้ถี่กว่า จึงให้เสียงที่มีระดับสูงกว่า",
     ("ลูกระนาดที่สั้นกว่ามีน้ำหนักเบากว่าจึงเสียงดังกว่า", "ลูกระนาดที่ยาวกว่าสั่นได้ถี่กว่าเสมอ", "ความยาวของลูกระนาดไม่เกี่ยวข้องกับระดับเสียง")),
    ("มอเตอร์พัดลมที่หมุนเร็วขึ้นมักมีเสียงหึ่งที่ระดับเสียงสูงขึ้นด้วย เหตุใดจึงเป็นเช่นนั้น",
     "การหมุนที่เร็วขึ้นทำให้ชิ้นส่วนสั่นด้วยความถี่สูงขึ้น จึงได้ยินเสียงในระดับที่สูงขึ้น",
     ("การหมุนเร็วขึ้นทำให้แอมพลิจูดการสั่นมากขึ้นเท่านั้น ไม่กระทบระดับเสียง", "การหมุนเร็วขึ้นทำให้ความถี่การสั่นลดลง", "ความเร็วในการหมุนไม่มีผลต่อระดับเสียงของมอเตอร์")),
)


STRING_NAMES = ("สาย ก", "สาย ข", "สาย ค")


@question_type(
    "phys.pitch_foundation",
    display_name={"th": "บอกลักษณะการสั่นที่ทำให้เกิดเสียงสูง"},
    level=FIFTH, subject=SUBJECT, topic=PITCH_TOPIC,
)
class PitchFoundation(QuestionType):
    """High pitch is fast vibration; which of two sources sounds higher."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            stem, right, wrongs = rng.choice(PITCH_FACTS)
            return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), hint=PITCH_HINT, topic=PITCH_TOPIC)
        high, low = rng.choice(PITCH_PAIRS)
        ask_high = rng.random() < 0.5
        a, b = (high, low) if rng.random() < 0.5 else (low, high)
        right = high if ask_high else low
        return _labelled(stem=f"เปรียบเทียบ{a}กับ{b} สิ่งใดให้เสียง{'สูง' if ask_high else 'ต่ำ'}กว่า", correct=right,
                         wrongs=(low if ask_high else high, "ให้เสียงสูงต่ำเท่ากัน", "บอกไม่ได้ เพราะขึ้นกับความดังเท่านั้น"),
                         hint=PITCH_HINT, topic=PITCH_TOPIC)


@question_type(
    "phys.pitch_fluency",
    display_name={"th": "ระบุตัวแปร ทดลอง และอธิบายการเกิดเสียงสูงเสียงต่ำ"},
    level=FIFTH, subject=SUBJECT, topic=PITCH_TOPIC,
)
class PitchFluency(QuestionType):
    """The ruler at two lengths, or a table of lengths against vibrations counted."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            short = rng.randint(5, 10)
            long_ = short + rng.randint(5, 10)
            return _labelled(
                stem=(f"{PITCH_STEM_PREFIX} ส่วนที่ยื่นออกมา {short} เซนติเมตร "
                      f"สั่นถี่และเกิดเสียงสูง ส่วนที่ยื่นออกมา {long_} เซนติเมตร สั่นห่างและเกิดเสียงต่ำ "
                      "จากผลการทดลองนี้ ข้อใดอธิบายการเกิดเสียงสูงเสียงต่ำได้ถูกต้อง"),
                correct="ส่วนที่สั่นถี่กว่า (ความถี่สูงกว่า) ทำให้เกิดเสียงสูงกว่า ส่วนที่สั่นห่างกว่า (ความถี่ต่ำกว่า) ทำให้เกิดเสียงต่ำกว่า",
                wrongs=("ส่วนที่สั่นถี่กว่าทำให้เกิดเสียงต่ำกว่า ส่วนที่สั่นห่างกว่าทำให้เกิดเสียงสูงกว่า",
                        "ความยาวของไม้บรรทัดที่ยื่นออกมาไม่มีผลต่อระดับเสียงที่เกิดขึ้นเลย",
                        "ส่วนที่สั่นถี่กว่าทำให้เกิดเสียงดังกว่า ไม่เกี่ยวกับความสูงต่ำของเสียง"),
                hint="เปรียบเทียบความถี่การสั่นของแต่ละส่วนกับระดับเสียงสูงต่ำที่เกิดขึ้นในผลการทดลอง",
                topic=PITCH_TOPIC,
            )
        lengths = sorted(rng.sample(range(10, 41, 5), 3))
        base = rng.choice((30, 40, 50, 60))
        counts = [base * 60 // ell for ell in lengths]
        table = " / ".join(f"ยาว {ell} cm สั่น {c} ครั้งต่อวินาที" for ell, c in zip(lengths, counts))
        variable = rng.choice(("ความยาวของสายยาง", "ความยาวของไม้บรรทัดที่ยื่นออกมา", "ความยาวของสายกีตาร์"))
        return _labelled(stem=f"นักเรียนเปลี่ยน{variable} แล้วนับการสั่นได้ดังนี้ {table} ข้อสรุปใดถูกต้อง",
                         correct="ยิ่งสั้น ยิ่งสั่นถี่ และให้เสียงสูงขึ้น",
                         wrongs=("ยิ่งสั้น ยิ่งสั่นห่าง และให้เสียงต่ำลง", "ยิ่งยาว ยิ่งสั่นถี่ และให้เสียงสูงขึ้น", "ความยาวไม่มีผลต่อความถี่และระดับเสียง"),
                         hint="ตัวแปรต้นคือความยาว ตัวแปรตามคือความถี่การสั่นและระดับเสียง", topic=PITCH_TOPIC)


@question_type(
    "phys.pitch_application",
    display_name={"th": "ใช้ความรู้เรื่องความถี่การสั่นอธิบายระดับเสียงสูงต่ำ"},
    level=FIFTH, subject=SUBJECT, topic=PITCH_TOPIC,
)
class PitchApplication(QuestionType):
    """Authored instruments, and three strings of one kind ordered by length."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            return _retopic(scenario_question(rng, PITCH_SCENARIOS, hint=PITCH_HINT), PITCH_TOPIC)
        lengths = rng.sample(range(20, 81, 5), 3)
        order = [n for _, n in sorted(zip(lengths, STRING_NAMES))]
        high_first = rng.random() < 0.5
        right = " > ".join(order) if high_first else " > ".join(reversed(order))
        perms = [" > ".join(p) for p in permutations(STRING_NAMES) if " > ".join(p) != right]
        instrument = rng.choice(("พิณ", "จะเข้", "กีตาร์ที่ทำเอง", "ซอ"))
        table = " ".join(f"{n} ยาว {ell} cm" for n, ell in zip(STRING_NAMES, lengths))
        return _labelled(stem=f"{instrument}มีสายชนิดเดียวกันขึงตึงเท่ากันสามเส้น {table} เมื่อดีด ข้อใดเรียงเสียงจาก{'สูงไปต่ำ' if high_first else 'ต่ำไปสูง'}ได้ถูกต้อง",
                         correct=right, wrongs=tuple(perms), hint=PITCH_HINT, topic=PITCH_TOPIC)
