"""การเปลี่ยนแปลงแทนที่

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 5 ม.6/5

Sets moved here from: science_wave_f71.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f71 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_SUCC = "การเปลี่ยนแปลงแทนที่"


PRIMARY = ("ลาวาที่เย็นตัวเป็นหินใหม่หลังภูเขาไฟระเบิด", "ลานหินที่ธารน้ำแข็งละลายถอยออกไป", "เกาะใหม่ที่เกิดจากภูเขาไฟใต้ทะเล",
           "หน้าผาหินที่เพิ่งพังทลายจนเห็นหินเปล่า", "เนินทรายใหม่ริมทะเลที่ยังไม่มีดิน")


SECONDARY = ("ป่าที่ถูกไฟไหม้แต่ดินยังอยู่", "ไร่ร้างที่ถูกทิ้งไว้หลายปี", "ป่าที่ถูกตัดโค่นแล้วปล่อยทิ้งไว้", "ทุ่งหญ้าหลังน้ำท่วมลดลง",
             "นาข้าวที่เลิกทำนาแล้วปล่อยรกร้าง")


PRIMARY_STAGES = ("ไลเคน", "มอส", "หญ้าและพืชล้มลุก", "ไม้พุ่ม", "ไม้ยืนต้น")


SUCC_HINT = ("การแทนที่ปฐมภูมิเริ่มบนพื้นที่ไม่มีดิน สิ่งมีชีวิตบุกเบิกเช่นไลเคนช่วยสร้างดิน การแทนที่ทุติยภูมิเกิดบนพื้นที่ที่ยังมีดิน "
             "จึงเริ่มจากหญ้าและเกิดเร็วกว่า ทั้งสองแบบดำเนินไปจนถึงสังคมสมบูรณ์")


@question_type(
    "biology.succession_foundation",
    display_name={"th": "การเปลี่ยนแปลงแทนที่แบบปฐมภูมิและทุติยภูมิ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_SUCC,
)
class SuccessionFoundation(QuestionType):
    """Primary or secondary, from where it starts."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        primary = rng.random() < 0.5
        same, other = (PRIMARY, SECONDARY) if primary else (SECONDARY, PRIMARY)
        kind = "การเปลี่ยนแปลงแทนที่แบบปฐมภูมิ" if primary else "การเปลี่ยนแปลงแทนที่แบบทุติยภูมิ"
        if rng.random() < 0.5:
            return _labelled(stem=f"ข้อใดเป็นจุดเริ่มต้นของ{kind}", correct=rng.choice(same), wrongs=tuple(other),
                             topic=TOPIC_SUCC, hint=SUCC_HINT)
        return _labelled(stem=f"การเปลี่ยนแปลงแทนที่ที่เกิดใน{rng.choice(same)}เป็นแบบใด", correct=kind,
                         wrongs=("การเปลี่ยนแปลงแทนที่แบบทุติยภูมิ" if primary else "การเปลี่ยนแปลงแทนที่แบบปฐมภูมิ", "สังคมสมบูรณ์ที่ไม่เปลี่ยนแปลง",
                                 "ไบโอแมกนิฟิเคชัน"), topic=TOPIC_SUCC, hint=SUCC_HINT)


@question_type(
    "biology.succession_fluency",
    display_name={"th": "ลำดับขั้นและลักษณะของการเปลี่ยนแปลงแทนที่"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_SUCC,
)
class SuccessionFluency(QuestionType):
    """Pioneers, the order of stages, and the climax."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            i = rng.randrange(len(PRIMARY_STAGES) - 1)
            pool = [p for p in PRIMARY_STAGES if p not in (PRIMARY_STAGES[i], PRIMARY_STAGES[i + 1])] + ["ปะการัง", "สัตว์กินพืชขนาดใหญ่"]
            return _labelled(stem=f"ในการเปลี่ยนแปลงแทนที่แบบปฐมภูมิบนหินเปล่า สิ่งมีชีวิตที่ขึ้นต่อจาก{PRIMARY_STAGES[i]}คือข้อใด",
                             correct=PRIMARY_STAGES[i + 1], wrongs=tuple(pool), topic=TOPIC_SUCC, hint=SUCC_HINT)
        facts = (("สิ่งมีชีวิตบุกเบิกบนหินเปล่ามักเป็นอะไร", "ไลเคน", ("ต้นไม้ใหญ่", "หญ้า", "ไม้พุ่ม", "สัตว์กินพืช")),
                 ("ไลเคนช่วยให้พืชอื่นขึ้นได้ในภายหลังเพราะเหตุใด", "ปล่อยกรดทำให้หินผุ และซากสะสมเป็นดิน",
                  ("สร้างร่มเงาให้ต้นไม้ใหญ่", "ดูดน้ำออกจากหิน", "ฆ่าแมลงที่เป็นศัตรูพืช", "ปล่อยไนเตรตจำนวนมากทันที")),
                 ("เหตุใดการเปลี่ยนแปลงแทนที่แบบทุติยภูมิจึงเกิดเร็วกว่าแบบปฐมภูมิ", "มีดิน เมล็ด และรากพืชเหลืออยู่แล้ว",
                  ("มีแสงมากกว่า", "ไม่มีสิ่งมีชีวิตแข่งขัน", "เริ่มจากไลเคนเสมอ", "อุณหภูมิสูงกว่าเสมอ")),
                 ("สังคมสมบูรณ์ (climax community) หมายถึงข้อใด", "สังคมที่ค่อนข้างคงที่เมื่อการแทนที่ดำเนินไปจนสุด",
                  ("สังคมแรกที่เกิดบนหินเปล่า", "สังคมที่มีแต่ไลเคน", "สังคมที่เปลี่ยนแปลงเร็วที่สุด", "สังคมหลังไฟไหม้ทันที")))
        stem, right, wrongs = rng.choice(facts)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_SUCC, hint=SUCC_HINT)


@question_type(
    "biology.succession_application",
    display_name={"th": "วิเคราะห์ข้อมูลการเปลี่ยนแปลงแทนที่"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_SUCC,
)
class SuccessionApplication(QuestionType):
    """Put stages of a described site in order."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            chunk = [PRIMARY_STAGES[i] for i in sorted(rng.sample(range(len(PRIMARY_STAGES)), 4))]
        else:
            stages = ("หญ้าและวัชพืช", "ไม้พุ่ม", "ไม้ยืนต้นที่เติบโตเร็ว", "ป่าที่เป็นสังคมสมบูรณ์")
            chunk = list(stages)
        wrongs: dict[str, None] = {}   # insertion-ordered: a set's order changes per process
        while len(wrongs) < 3:
            c = chunk[:]
            rng.shuffle(c)
            if c != chunk:
                wrongs[" → ".join(c)] = None
        site = ("บนลาวาที่เย็นตัวแล้ว" if chunk[0] in PRIMARY_STAGES else "ในไร่ร้างที่ถูกทิ้งไว้")
        return _labelled(stem=f"ข้อใดเรียงลำดับการเปลี่ยนแปลงแทนที่{site}ได้ถูกต้อง", correct=" → ".join(chunk), wrongs=tuple(wrongs),
                         topic=TOPIC_SUCC, hint=SUCC_HINT)
