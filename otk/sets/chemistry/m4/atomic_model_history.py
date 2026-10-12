"""วิวัฒนาการของแบบจำลองอะตอม

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.4/1

Sets moved here from: science_wave_f19.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f19 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_MODEL = "วิวัฒนาการของแบบจำลองอะตอม"


MODELS = (
    ("ดอลตัน", "อะตอมเป็นทรงกลมตันขนาดเล็กที่แบ่งแยกไม่ได้"),
    ("ทอมสัน", "อะตอมเป็นทรงกลมประจุบวกที่มีอิเล็กตรอนประจุลบกระจายอยู่ทั่วไป"),
    ("รัทเทอร์ฟอร์ด", "อะตอมมีนิวเคลียสขนาดเล็กมากตรงกลางซึ่งมีประจุบวกและมวลเกือบทั้งหมด โดยมีอิเล็กตรอนอยู่รอบนอก"),
    ("โบร์", "อิเล็กตรอนเคลื่อนที่รอบนิวเคลียสเป็นชั้น ๆ ตามระดับพลังงาน"),
    ("กลุ่มหมอก", "อิเล็กตรอนเคลื่อนที่รวดเร็วรอบนิวเคลียส บอกได้เพียงโอกาสที่จะพบในบริเวณต่าง ๆ"),
)


EVIDENCE = (
    ("รังสีแคโทดเบนเข้าหาแผ่นประจุบวกเมื่อผ่านสนามไฟฟ้า", "อะตอมมีอนุภาคประจุลบเป็นองค์ประกอบ", "ทอมสัน"),
    ("ยิงอนุภาคแอลฟาผ่านแผ่นทองคำบาง อนุภาคส่วนใหญ่ทะลุผ่านไปเป็นเส้นตรง", "ภายในอะตอมส่วนใหญ่เป็นที่ว่าง", "รัทเทอร์ฟอร์ด"),
    ("ยิงอนุภาคแอลฟาผ่านแผ่นทองคำบาง มีอนุภาคจำนวนน้อยมากสะท้อนกลับ", "มีนิวเคลียสขนาดเล็กมาก มีประจุบวกและมวลมากอยู่ตรงกลางอะตอม", "รัทเทอร์ฟอร์ด"),
    ("สเปกตรัมของธาตุเป็นเส้นสว่างแยกกันเฉพาะตัว", "อิเล็กตรอนอยู่ในระดับพลังงานที่มีค่าเฉพาะ", "โบร์"),
    ("พลังงานไอออไนเซชันลำดับต่าง ๆ ของธาตุเพิ่มขึ้นเป็นช่วง ๆ", "อิเล็กตรอนจัดเรียงตัวเป็นชั้น ๆ ตามระดับพลังงาน", "โบร์"),
    ("ธาตุรวมกันเป็นสารประกอบด้วยอัตราส่วนโดยมวลคงที่", "สารประกอบเกิดจากอะตอมของธาตุรวมกันในอัตราส่วนที่แน่นอน", "ดอลตัน"),
)


ORDER = ("ดอลตัน", "ทอมสัน", "รัทเทอร์ฟอร์ด", "โบร์", "กลุ่มหมอก")


@question_type(
    "chem.atomic_model_history_foundation",
    display_name={"th": "แบบจำลองอะตอมของนักวิทยาศาสตร์แต่ละคน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MODEL,
)
class AtomicModelHistoryFoundation(QuestionType):
    """Which model is whose."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        chosen = rng.sample(MODELS, 4)
        who, model = chosen[0]
        hint = "ดอลตัน: ทรงกลมตัน ทอมสัน: ทรงกลมประจุบวกมีอิเล็กตรอนแทรก รัทเทอร์ฟอร์ด: มีนิวเคลียส โบร์: ระดับพลังงาน กลุ่มหมอก: โอกาสพบอิเล็กตรอน"
        name = lambda w: w if w == "กลุ่มหมอก" else f"แบบจำลองของ{w}"
        if rng.random() < 0.5:
            return _labelled(stem=f"{name(who)}อธิบายอะตอมไว้อย่างไร", correct=model,
                             wrongs=tuple(m for _, m in chosen[1:]), topic=TOPIC_MODEL, hint=hint)
        return _labelled(stem=f"แบบจำลองอะตอมใดกล่าวว่า{model}", correct=name(who),
                         wrongs=tuple(name(w) for w, _ in chosen[1:]), topic=TOPIC_MODEL, hint=hint)


@question_type(
    "chem.atomic_model_history_fluency",
    display_name={"th": "ผลการทดลองที่เป็นประจักษ์พยานของแบบจำลองอะตอม"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MODEL,
)
class AtomicModelHistoryFluency(QuestionType):
    """From an observation to what it proves, and to whose model it supports."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        observed, meaning, who = rng.choice(EVIDENCE)
        hint = "นึกถึงการทดลองที่นำไปสู่แบบจำลองนั้น: หลอดรังสีแคโทด การยิงแอลฟาผ่านแผ่นทอง และสเปกตรัมเส้น"
        if rng.random() < 0.5:
            others = sorted({m for _, m, _ in EVIDENCE if m != meaning})
            return _labelled(stem=f"ผลการทดลอง \"{observed}\" สนับสนุนข้อสรุปใด", correct=meaning,
                             wrongs=tuple(others), topic=TOPIC_MODEL, hint=hint)
        return _labelled(stem=f"ผลการทดลอง \"{observed}\" นำไปสู่แบบจำลองอะตอมของใคร", correct=who,
                         wrongs=tuple(w for w in ("ดอลตัน", "ทอมสัน", "รัทเทอร์ฟอร์ด", "โบร์") if w != who),
                         topic=TOPIC_MODEL, hint=hint)


@question_type(
    "chem.atomic_model_history_application",
    display_name={"th": "ลำดับวิวัฒนาการและข้อจำกัดของแบบจำลองอะตอม"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MODEL,
)
class AtomicModelHistoryApplication(QuestionType):
    """Which model came before which, and what an older model could not explain."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            picked = sorted(rng.sample(range(len(ORDER)), rng.choice((3, 4))))
            right = " → ".join(ORDER[i] for i in picked)
            names = [ORDER[i] for i in picked]
            wrongs = set()
            while len(wrongs) < 3:
                shuffled = names[:]
                rng.shuffle(shuffled)
                text = " → ".join(shuffled)
                if text != right:
                    wrongs.add(text)
            return _labelled(stem=f"เรียงลำดับการเสนอแบบจำลองอะตอมของ{' '.join(rng.sample(names, len(names)))} จากก่อนไปหลัง",
                             correct=right, wrongs=tuple(sorted(wrongs)), topic=TOPIC_MODEL,
                             hint="ลำดับ: ดอลตัน → ทอมสัน → รัทเทอร์ฟอร์ด → โบร์ → กลุ่มหมอก")
        cases = (
            ("แบบจำลองของดอลตันอธิบายข้อใดไม่ได้", "อะตอมมีอนุภาคประจุลบอยู่ภายใน"),
            ("แบบจำลองของทอมสันอธิบายข้อใดไม่ได้", "อนุภาคแอลฟาบางส่วนสะท้อนกลับจากแผ่นทองคำ"),
            ("แบบจำลองของรัทเทอร์ฟอร์ดอธิบายข้อใดไม่ได้", "สเปกตรัมของไฮโดรเจนเป็นเส้นแยกกัน"),
            ("แบบจำลองของโบร์อธิบายข้อใดได้ไม่ดี", "สเปกตรัมของอะตอมที่มีอิเล็กตรอนหลายตัว"),
        )
        stem, right = rng.choice(cases)
        return _labelled(stem=stem, correct=right, wrongs=tuple(r for s, r in cases if r != right),
                         topic=TOPIC_MODEL, hint="แบบจำลองใหม่เกิดขึ้นเมื่อมีผลการทดลองที่แบบจำลองเดิมอธิบายไม่ได้")
