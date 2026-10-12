"""ลักษณะและการเกิดเสียงดัง เสียงค่อย

ฟิสิกส์ · ป.5 · สสวท. พื้นฐาน
Indicators: ว 2.3 ป.5/3

Sets moved here from: science_wave_d25.
"""

from __future__ import annotations

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


LOUDNESS_TOPIC = "ลักษณะและการเกิดเสียงดัง เสียงค่อย"


LOUD_FACTS = (
    ("เสียงดังเกิดจากการสั่นแบบใด", "การสั่นที่มีแอมพลิจูด (ขนาดการสั่น) มาก",
     ("การสั่นที่มีความถี่สูง ซึ่งทำให้เสียงสูงขึ้น ไม่ใช่เสียงดังขึ้น", "การสั่นที่มีแอมพลิจูดน้อย", "การสั่นที่มีคาบเวลานาน",
      "การไม่สั่นเลย", "การสั่นที่ช้าลงเรื่อย ๆ")),
    ("เสียงค่อยเกิดจากการสั่นแบบใด", "การสั่นที่มีแอมพลิจูด (ขนาดการสั่น) น้อย",
     ("การสั่นที่มีแอมพลิจูดมาก", "การสั่นที่มีความถี่สูงมาก", "การสั่นที่มีความถี่ต่ำมาก", "การไม่สั่นเลย", "การสั่นในสุญญากาศ")),
    ("ถ้าอยู่ห่างจากแหล่งกำเนิดเสียงมากขึ้น จะได้ยินเสียงเป็นอย่างไร", "ได้ยินเสียงค่อยลง",
     ("ได้ยินเสียงดังขึ้น", "ได้ยินเสียงสูงขึ้น", "ได้ยินเสียงเท่าเดิมเสมอ", "ไม่ได้ยินเสียงทันทีที่ขยับ", "ได้ยินเสียงต่ำลงมาก")),
)


LOUD_PAIRS = (
    ("ตีกลองแรง", "ตีกลองเบา"), ("ดีดสายกีตาร์แรง", "ดีดสายกีตาร์เบา"), ("ตะโกน", "กระซิบ"), ("เคาะระนาดแรง", "เคาะระนาดเบา"),
    ("เป่านกหวีดแรง", "เป่านกหวีดเบา"), ("ปรบมือแรง", "ปรบมือเบา"), ("ลำโพงที่เปิดเสียงสูงสุด", "ลำโพงที่เปิดเสียงต่ำสุด"),
)


LOUD_HINT = "ยิ่งวัตถุสั่นด้วยแอมพลิจูดมาก เสียงยิ่งดัง ส่วนความถี่การสั่นเกี่ยวกับเสียงสูงต่ำ"


LOUDNESS_SCENARIOS = (
    ("เหตุใดการตีกลองแรง ๆ จึงให้เสียงดังกว่าการตีกลองเบา ๆ ด้วยไม้ตีอันเดียวกัน",
     "ตีแรงทำให้หน้ากลองสั่นด้วยแอมพลิจูดมากกว่า จึงเกิดเสียงดังกว่า",
     ("ตีแรงทำให้หน้ากลองสั่นถี่กว่า จึงเกิดเสียงดังกว่า", "ตีแรงทำให้หน้ากลองสั่นด้วยแอมพลิจูดน้อยกว่า", "แรงที่ใช้ตีไม่มีผลต่อความดังของเสียงกลอง")),
    ("เมื่อกระซิบพูดกับตะโกนพูดประโยคเดียวกัน เสียงทั้งสองต่างกันอย่างไรในแง่การสั่นของเส้นเสียง",
     "ตะโกนทำให้เส้นเสียงสั่นด้วยแอมพลิจูดมากกว่ากระซิบ จึงเสียงดังกว่า",
     ("ตะโกนทำให้เส้นเสียงสั่นถี่กว่ากระซิบมาก จึงเสียงสูงกว่ามาก", "กระซิบทำให้เส้นเสียงสั่นด้วยแอมพลิจูดมากกว่าตะโกน", "การสั่นของเส้นเสียงเท่ากันทั้งกระซิบและตะโกน")),
    ("เมื่อหมุนปุ่มเพิ่มระดับเสียงของลำโพง แผ่นลำโพงจะเปลี่ยนแปลงอย่างไร",
     "แผ่นลำโพงสั่นด้วยแอมพลิจูดมากขึ้น ทำให้เสียงดังขึ้น",
     ("แผ่นลำโพงสั่นถี่ขึ้นมาก ทำให้เสียงดังขึ้น", "แผ่นลำโพงสั่นด้วยแอมพลิจูดน้อยลง แต่เสียงดังขึ้นเอง", "การหมุนปุ่มไม่เกี่ยวกับการสั่นของแผ่นลำโพงเลย")),
)


DISTANCES = ("ยืนห่างลำโพง 2 เมตร", "ยืนห่างลำโพง 5 เมตร", "ยืนห่างลำโพง 10 เมตร", "ยืนห่างลำโพง 20 เมตร")


@question_type(
    "phys.loudness_foundation",
    display_name={"th": "บอกลักษณะการสั่นที่ทำให้เกิดเสียงดัง"},
    level=FIFTH, subject=SUBJECT, topic=LOUDNESS_TOPIC,
)
class LoudnessFoundation(QuestionType):
    """Amplitude makes loudness; which of two actions is louder."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            stem, right, wrongs = rng.choice(LOUD_FACTS)
            return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), hint=LOUD_HINT, topic=LOUDNESS_TOPIC)
        loud, soft = rng.choice(LOUD_PAIRS)
        ask_loud = rng.random() < 0.5
        right = loud if ask_loud else soft
        return _labelled(stem=f"ระหว่าง{loud}กับ{soft} ข้อใดทำให้วัตถุสั่นด้วยแอมพลิจูด{'มาก' if ask_loud else 'น้อย'}กว่าและเกิดเสียง{'ดัง' if ask_loud else 'ค่อย'}กว่า",
                         correct=right, wrongs=(soft if ask_loud else loud, "ดังเท่ากันเสมอ", "บอกไม่ได้ เพราะขึ้นกับความถี่เท่านั้น"),
                         hint=LOUD_HINT, topic=LOUDNESS_TOPIC)


@question_type(
    "phys.loudness_fluency",
    display_name={"th": "ออกแบบการทดลองและอธิบายการเกิดเสียงดังเสียงค่อย"},
    level=FIFTH, subject=SUBJECT, topic=LOUDNESS_TOPIC,
)
class LoudnessFluency(QuestionType):
    """The ruler plucked hard and soft, or a table of pluck force against how far the end swings."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        length = rng.randint(8, 20)
        if rng.random() < 0.4:
            return _labelled(
                stem=(f"นักเรียนดีดปลายไม้บรรทัดที่ยื่นออกจากขอบโต๊ะ {length} เซนติเมตรเท่ากันทั้งสองครั้ง ครั้งแรกดีดแรง "
                      "ปลายไม้บรรทัดสั่นด้วยแอมพลิจูดมากและเสียงดัง ครั้งที่สองดีดเบา ปลายไม้บรรทัดสั่นด้วยแอมพลิจูดน้อยและเสียงค่อย "
                      "จากผลการทดลองนี้ ข้อใดอธิบายการเกิดเสียงดังเสียงค่อยได้ถูกต้อง"),
                correct="การสั่นที่มีแอมพลิจูดมากกว่าทำให้เกิดเสียงดังกว่า การสั่นที่มีแอมพลิจูดน้อยกว่าทำให้เกิดเสียงค่อยกว่า",
                wrongs=("การสั่นที่มีแอมพลิจูดมากกว่าทำให้เกิดเสียงค่อยกว่า การสั่นที่มีแอมพลิจูดน้อยกว่าทำให้เกิดเสียงดังกว่า",
                        "ความถี่การสั่นที่มากกว่าทำให้เสียงดังกว่า ไม่เกี่ยวกับแอมพลิจูดของการสั่น",
                        "แรงที่ใช้ดีดไม่มีผลต่อความดังของเสียงที่เกิดขึ้นเลย"),
                hint="ทั้งสองครั้งความยาวส่วนที่ยื่นออกมาเท่ากัน สิ่งที่ต่างกันคือแรงที่ใช้ดีดซึ่งเปลี่ยนแอมพลิจูดการสั่น",
                topic=LOUDNESS_TOPIC,
            )
        swings = sorted(rng.sample(range(1, 16), 3))
        levels = sorted(rng.sample(range(45, 91, 5), 3))
        table = " / ".join(f"ดีด{w} ปลายไม้บรรทัดแกว่ง {s} mm วัดเสียงได้ {d} dB"
                           for w, s, d in zip(("เบา", "ปานกลาง", "แรง"), swings, levels))
        return _labelled(stem=f"นักเรียนดีดไม้บรรทัดที่ยื่นออกมา {length} cm เท่ากันทุกครั้ง ได้ผลดังนี้ {table} ข้อสรุปใดถูกต้อง",
                         correct="ยิ่งดีดแรง ไม้บรรทัดยิ่งสั่นด้วยแอมพลิจูดมาก และเสียงยิ่งดัง",
                         wrongs=("ยิ่งดีดแรง ไม้บรรทัดยิ่งสั่นด้วยแอมพลิจูดน้อย และเสียงยิ่งค่อย", "ยิ่งดีดแรง เสียงยิ่งสูงขึ้นเพราะความถี่มากขึ้น",
                                 "แรงที่ใช้ดีดไม่มีผลต่อความดังของเสียง"),
                         hint="ตัวแปรต้นคือแรงที่ใช้ดีด ตัวแปรที่คงที่คือความยาวส่วนที่ยื่น ดูว่าขนาดการแกว่งและระดับเสียงเปลี่ยนตามอย่างไร",
                         topic=LOUDNESS_TOPIC)


@question_type(
    "phys.loudness_application",
    display_name={"th": "ใช้ความรู้เรื่องแอมพลิจูดการสั่นอธิบายความดังของเสียง"},
    level=FIFTH, subject=SUBJECT, topic=LOUDNESS_TOPIC,
)
class LoudnessApplication(QuestionType):
    """Authored cases, and who hears a speaker loudest from their distances."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            return _retopic(scenario_question(rng, LOUDNESS_SCENARIOS, hint=LOUD_HINT), LOUDNESS_TOPIC)
        kids = rng.sample(("ต้น", "ฝน", "มะลิ", "ภูมิ", "ข้าวหอม", "ปลา", "บอส", "น้ำใส"), 4)
        spots = rng.sample(DISTANCES, 4)
        loudest = rng.random() < 0.5
        key = lambda sp: int(sp.split()[1])
        pick = kids[spots.index((min if loudest else max)(spots, key=key))]
        table = " ".join(f"{k}{sp}" for k, sp in zip(kids, spots))
        return _labelled(stem=f"ลำโพงเปิดเพลงเสียงเท่าเดิม {table} ใครได้ยินเสียง{'ดัง' if loudest else 'ค่อย'}ที่สุด", correct=pick,
                         wrongs=tuple(k for k in kids if k != pick), hint="ยิ่งอยู่ใกล้แหล่งกำเนิดเสียง ยิ่งได้ยินเสียงดัง", topic=LOUDNESS_TOPIC)
