"""กรอบของปัญหาในชุมชน

การออกแบบและเทคโนโลยี · ม.2 · สสวท. พื้นฐาน
Indicators: ว 4.1 ม.2/2

Sets moved here from: technology_t2s2.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.technology_t1 import SUBJECT
from otk.sets._support.technology_t1s4 import _near
from otk.sets._support.technology_t2s2 import M2

PROVENANCE = Provenance("original")


FRAME_TOPIC = "กรอบของปัญหาในชุมชน"


PROBLEM, CAUSE, AFFECTED, CONDITION = "ปัญหา", "สาเหตุ", "ผู้ได้รับผลกระทบ", "เงื่อนไขหรือข้อจำกัด"


FRAME_PARTS = (PROBLEM, CAUSE, AFFECTED, CONDITION)


FRAMES = (
    {PROBLEM: "น้ำท่วมขังถนนหน้าตลาดทุกครั้งที่ฝนตกหนัก",
     CAUSE: "ท่อระบายน้ำหน้าตลาดอุดตันด้วยขยะ",
     AFFECTED: "แม่ค้าและผู้ที่มาซื้อของในตลาด",
     CONDITION: "ต้องแก้ไขโดยไม่ปิดตลาด และใช้งบประมาณของชุมชนไม่เกิน 5,000 บาท"},
    {PROBLEM: "ผู้สูงอายุในชุมชนลื่นล้มที่ทางเดินไปศาลาประชาคม",
     CAUSE: "ทางเดินเป็นพื้นกระเบื้องที่ลื่นเมื่อเปียก และไม่มีราวจับ",
     AFFECTED: "ผู้สูงอายุที่มาร่วมกิจกรรมที่ศาลาประชาคม",
     CONDITION: "ต้องทำเสร็จก่อนงานประจำปีในอีกหนึ่งเดือน"},
    {PROBLEM: "ผลไม้ของสวนในชุมชนเน่าเสียก่อนขายได้หมด",
     CAUSE: "ไม่มีที่เก็บผลไม้ที่เย็นและอากาศถ่ายเท",
     AFFECTED: "เกษตรกรเจ้าของสวนผลไม้",
     CONDITION: "ต้องใช้ไฟฟ้าน้อย เพราะสวนอยู่ไกลสายส่งไฟฟ้า"},
    {PROBLEM: "นักเรียนข้ามถนนหน้าโรงเรียนไม่ปลอดภัยในช่วงเช้า",
     CAUSE: "รถขับเร็วและไม่มีสัญญาณเตือนให้ชะลอ",
     AFFECTED: "นักเรียนและผู้ปกครองที่มาส่งลูก",
     CONDITION: "ต้องได้รับอนุญาตจากหน่วยงานที่ดูแลถนนก่อนติดตั้งสิ่งใด"},
    {PROBLEM: "กลิ่นเหม็นจากกองขยะเศษอาหารท้ายหมู่บ้าน",
     CAUSE: "ขยะเศษอาหารถูกทิ้งรวมกับขยะอื่นและไม่ได้แยกไปจัดการ",
     AFFECTED: "ครอบครัวที่อยู่ใกล้กองขยะ",
     CONDITION: "ต้องใช้พื้นที่ว่างที่มีอยู่เดิมของหมู่บ้านเท่านั้น"},
)


FRAME_HINT = ("กรอบของปัญหาบอกว่าปัญหาคืออะไร เกิดจากอะไร ใครได้รับผลกระทบ "
              "และวิธีแก้ต้องอยู่ภายใต้เงื่อนไขหรือข้อจำกัดใด")


GATHERING = (
    ("ความคิดเห็นของชาวบ้านต่อวิธีแก้ปัญหาที่เสนอ", "สอบถามหรือใช้แบบสอบถามกับชาวบ้าน"),
    ("ปริมาณขยะเศษอาหารที่เกิดขึ้นในแต่ละวัน", "ชั่งน้ำหนักขยะทุกวันต่อเนื่องหนึ่งสัปดาห์"),
    ("ความกว้างของทางเดินที่จะติดราวจับ", "วัดด้วยตลับเมตรที่ตำแหน่งจริง"),
    ("จำนวนรถที่ผ่านหน้าโรงเรียนช่วงเช้า", "นับและบันทึกจำนวนรถในช่วงเวลาที่กำหนด"),
    ("วิธีที่ชุมชนอื่นเคยใช้แก้ปัญหาแบบเดียวกัน", "ค้นหาจากเอกสารหรือเว็บไซต์ของหน่วยงานที่น่าเชื่อถือ"),
    ("อุณหภูมิในที่เก็บผลไม้ตลอดวัน", "ติดเทอร์โมมิเตอร์และบันทึกค่าทุกชั่วโมง"),
)


SURVEY_CAUSES = (
    ("ทิ้งขยะลงท่อระบายน้ำ", "ท่อมีขนาดเล็กเกินไป", "ไม่มีการลอกท่อ", "ถนนต่ำกว่าบ้านเรือน"),
    ("รถขับเร็ว", "ไม่มีทางม้าลาย", "ไม่มีป้ายเตือน", "ไม่มีเจ้าหน้าที่ช่วยข้ามถนน"),
)


@question_type(
    "tech.community_problem_foundation",
    display_name={"th": "สรุปกรอบของปัญหาในชุมชน"},
    level=M2, subject=SUBJECT, topic=FRAME_TOPIC,
)
class CommunityProblemFoundation(QuestionType):
    def build(self, rng: Random, **params):
        frame = rng.choice(FRAMES)
        part = rng.choice(FRAME_PARTS)
        if rng.random() < 0.5:
            return _labelled(
                stem=f"ในการสรุปกรอบของปัญหาของชุมชน “{frame[part]}” จัดเป็นส่วนใดของกรอบปัญหา",
                correct=part, wrongs=tuple(p for p in FRAME_PARTS if p != part),
                hint=FRAME_HINT, topic=FRAME_TOPIC,
            )
        return _labelled(
            stem=f"ปัญหาของชุมชนหนึ่งคือ “{frame[PROBLEM]}” ข้อใดคือ{part}ในกรอบของปัญหานี้"
            if part != PROBLEM else
            f"ชุมชนหนึ่งพบว่า{frame[CAUSE]} ข้อใดคือปัญหาในกรอบของปัญหานี้",
            correct=frame[part], wrongs=tuple(frame[p] for p in FRAME_PARTS if p != part),
            hint=FRAME_HINT, topic=FRAME_TOPIC,
        )


@question_type(
    "tech.community_problem_fluency",
    display_name={"th": "เลือกวิธีรวบรวมข้อมูลให้เหมาะกับข้อมูลที่ต้องการ"},
    level=M2, subject=SUBJECT, topic=FRAME_TOPIC,
)
class CommunityProblemFluency(QuestionType):
    def build(self, rng: Random, **params):
        index = rng.randrange(len(GATHERING))
        info, method = GATHERING[index]
        others = rng.sample([row for i, row in enumerate(GATHERING) if i != index], 3)
        hint = "ข้อมูลความคิดเห็นได้จากการสอบถาม ข้อมูลตัวเลขได้จากการวัด นับ หรือชั่ง ข้อมูลความรู้ได้จากแหล่งที่น่าเชื่อถือ"
        if rng.random() < 0.5:
            return _labelled(stem=f"ต้องการรู้{info} ควรรวบรวมข้อมูลด้วยวิธีใด",
                             correct=method, wrongs=tuple(m for _, m in others), hint=hint, topic=FRAME_TOPIC)
        return _labelled(stem=f"การ{method} เหมาะสำหรับรวบรวมข้อมูลใด",
                         correct=info, wrongs=tuple(i for i, _ in others), hint=hint, topic=FRAME_TOPIC)


@question_type(
    "tech.community_problem_application",
    display_name={"th": "วิเคราะห์ข้อมูลที่รวบรวมจากชุมชน"},
    level=M2, subject=SUBJECT, topic=FRAME_TOPIC,
)
class CommunityProblemApplication(QuestionType):
    """A drawn survey: the most-named cause, or one cause's percentage."""

    def build(self, rng: Random, **params):
        causes = rng.choice(SURVEY_CAUSES)
        total = rng.choice((20, 25, 50))
        cuts = sorted(rng.sample(range(1, total), 3))
        counts = [cuts[0], cuts[1] - cuts[0], cuts[2] - cuts[1], total - cuts[2]]
        while len(set(counts)) < 4:
            cuts = sorted(rng.sample(range(1, total), 3))
            counts = [cuts[0], cuts[1] - cuts[0], cuts[2] - cuts[1], total - cuts[2]]
        listed = " ".join(f"{c} {n} คน" for c, n in zip(causes, counts))
        intro = f"สำรวจความเห็นของคนในชุมชน {total} คน ว่าสาเหตุหลักของปัญหาคืออะไร ผลคือ {listed}"
        if rng.random() < 0.5:
            top = causes[counts.index(max(counts))]
            return _labelled(
                stem=f"{intro} สาเหตุใดที่คนในชุมชนเห็นว่าเป็นสาเหตุหลักมากที่สุด",
                correct=top, wrongs=tuple(c for c in causes if c != top),
                hint="เปรียบเทียบจำนวนคนที่เลือกแต่ละสาเหตุ",
                topic=FRAME_TOPIC,
            )
        index = rng.randrange(4)
        percent = counts[index] * 100 // total
        return _labelled(
            stem=f"{intro} คนที่เลือก “{causes[index]}” คิดเป็นร้อยละเท่าใดของผู้ตอบทั้งหมด",
            correct=f"ร้อยละ {percent}",
            wrongs=tuple(f"ร้อยละ {w}" for w in rng.sample(
                _near(percent, (counts[index], 100 - percent, percent + 10, percent - 5)), 3)),
            hint=f"ร้อยละ = จำนวนคนที่เลือก ÷ จำนวนผู้ตอบทั้งหมด × 100 เมื่อผู้ตอบมี {total} คน",
            topic=FRAME_TOPIC,
        )
