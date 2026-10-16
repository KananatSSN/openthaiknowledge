"""ทักษะกระบวนการทางวิทยาศาสตร์ ป.6

วิทยาศาสตร์ทั่วไป · ป.6 · เสริมทักษะ
Indicators: —

Filed like the ม.1 unit (บทนำ, no ตัวชี้วัด). ป.6 is where a class first plans a
fair test of its own: it states a hypothesis that can be tested, names what it
changes, measures and keeps the same, and draws a conclusion the data allows.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_g4 import SUBJECT

PROVENANCE = Provenance("original")


PRIMARY_SIX = {"th": "ป.6"}


PROCESS_SKILL_TOPIC = "ทักษะกระบวนการทางวิทยาศาสตร์"


class Test(NamedTuple):
    """A ป.6 fair test: its question, a testable hypothesis, and its variables.

    ``untestable`` are sentences about the same topic, most in the same
    ``ถ้า … จะ …`` shape, that no measurement in the test could check: feelings,
    looks and opinions. The choice turns on testability, not on the shape.
    """
    question: str
    hypothesis: str
    untestable: tuple[str, str, str]
    changed: str
    measured: str
    kept: str


TESTS = (
    Test("ชนิดของดินมีผลต่อการเจริญเติบโตของต้นถั่วหรือไม่",
         "ถ้าปลูกต้นถั่วในดินร่วน ต้นถั่วจะสูงกว่าต้นที่ปลูกในดินทรายเมื่อวัดในวันที่ 14",
         ("ถ้าปลูกต้นถั่วในดินร่วน ต้นถั่วจะมีความสุขมากกว่าต้นที่ปลูกในดินทราย",
          "ถ้าปลูกต้นถั่วในดินร่วน ต้นถั่วจะดูน่ารักกว่าต้นที่ปลูกในดินทรายทุกต้น",
          "ดินร่วนเป็นดินที่สวยงามที่สุด จึงเป็นดินที่ต้นไม้ทุกชนิดอยากเติบโตอยู่"),
         "ชนิดของดิน", "ความสูงของต้นถั่ว",
         "ปริมาณน้ำ ปริมาณแสง และชนิดของเมล็ดถั่ว"),
    Test("สีของภาชนะมีผลต่ออุณหภูมิของน้ำที่ตากแดดหรือไม่",
         "ถ้าใส่น้ำในกระป๋องสีดำ น้ำจะร้อนกว่าน้ำในกระป๋องสีขาวเมื่อตากแดดนานเท่ากัน",
         ("ถ้าใส่น้ำในกระป๋องสีดำ น้ำจะรู้สึกอบอุ่นและพอใจมากกว่าน้ำในกระป๋องสีขาว",
          "ถ้าใส่น้ำในกระป๋องสีดำ กระป๋องจะดูสวยงามกว่ากระป๋องสีขาวเมื่อวางตากแดด",
          "แสงแดดเป็นสิ่งที่มีประโยชน์ต่อสิ่งมีชีวิตทุกชนิดบนโลกในทุกช่วงเวลาของวัน"),
         "สีของกระป๋อง", "อุณหภูมิของน้ำ",
         "ปริมาณน้ำ ขนาดของกระป๋อง และเวลาที่ตากแดด"),
    Test("จำนวนรอบที่พันขดลวดมีผลต่อจำนวนคลิปที่แม่เหล็กไฟฟ้าดูดได้หรือไม่",
         "ถ้าพันขดลวดมากรอบขึ้น แม่เหล็กไฟฟ้าจะดูดคลิปหนีบกระดาษได้จำนวนมากขึ้น",
         ("ถ้าพันขดลวดมากรอบขึ้น แม่เหล็กไฟฟ้าจะดูน่าสนใจและน่าภูมิใจมากขึ้นกว่าเดิม",
          "ถ้าพันขดลวดอย่างตั้งใจ แม่เหล็กไฟฟ้าจะอยากดูดคลิปให้ได้มากที่สุดเท่าที่ทำได้",
          "แม่เหล็กไฟฟ้าเป็นสิ่งประดิษฐ์ที่น่าสนใจที่สุดในบรรดาสิ่งประดิษฐ์ทั้งหมดของมนุษย์"),
         "จำนวนรอบของขดลวด", "จำนวนคลิปที่ดูดได้",
         "ชนิดของตะปู ชนิดของลวด และจำนวนถ่านไฟฉาย"),
    Test("ความชันของพื้นเอียงมีผลต่อระยะที่รถของเล่นเคลื่อนที่ได้หรือไม่",
         "ถ้าพื้นเอียงชันมากขึ้น รถของเล่นจะเคลื่อนที่ได้ไกลขึ้นหลังลงจากพื้นเอียง",
         ("ถ้าพื้นเอียงชันมากขึ้น รถของเล่นจะสนุกกับการวิ่งลงจากพื้นเอียงมากขึ้นกว่าเดิม",
          "ถ้าพื้นเอียงชันมากขึ้น รถของเล่นจะดูสวยงามขึ้นขณะเคลื่อนที่ลงจากพื้นเอียง",
          "รถของเล่นสีแดงเป็นรถที่เด็กทุกคนชอบมากที่สุดเมื่อเทียบกับรถของเล่นสีอื่น"),
         "ความชันของพื้นเอียง", "ระยะที่รถของเล่นเคลื่อนที่ได้",
         "รถของเล่นคันเดิม ชนิดของพื้นผิว และจุดปล่อยรถ"),
    Test("อุณหภูมิของน้ำมีผลต่อเวลาที่เกลือละลายหมดหรือไม่",
         "ถ้าน้ำมีอุณหภูมิสูงขึ้น เกลือปริมาณเท่าเดิมจะละลายหมดโดยใช้เวลาสั้นลง",
         ("ถ้าน้ำมีอุณหภูมิสูงขึ้น เกลือจะชอบละลายในน้ำนั้นมากกว่าในน้ำที่เย็นกว่า",
          "ถ้าใช้น้ำร้อนละลายเกลือ น้ำเกลือที่ได้จะดีต่อสุขภาพมากกว่าน้ำเกลือจากน้ำเย็น",
          "เกลือเป็นเครื่องปรุงที่สำคัญที่สุดที่ทำให้อาหารทุกชนิดมีรสชาติดีขึ้นเสมอ"),
         "อุณหภูมิของน้ำ", "เวลาที่เกลือละลายหมด",
         "มวลของเกลือ ปริมาตรของน้ำ และการคน"),
    Test("ปริมาณแสงมีผลต่อการงอกของเมล็ดถั่วเขียวหรือไม่",
         "ถ้าเมล็ดถั่วเขียวได้รับแสง เมล็ดจะงอกได้จำนวนเท่ากับเมล็ดที่อยู่ในที่มืด",
         ("ถ้าเมล็ดถั่วเขียวได้รับแสง เมล็ดจะรู้สึกอบอุ่นและมีความสุขมากกว่าเมล็ดในที่มืด",
          "ถ้าเมล็ดถั่วเขียวได้รับแสง ต้นอ่อนที่งอกออกมาจะดูน่ารักกว่าต้นในที่มืด",
          "ถั่วเขียวเป็นอาหารที่มีประโยชน์ที่สุดต่อร่างกายเมื่อเทียบกับถั่วชนิดอื่นทั้งหมด"),
         "การได้รับแสง", "จำนวนเมล็ดที่งอก",
         "จำนวนเมล็ดที่เพาะ ปริมาณน้ำ และชนิดของวัสดุเพาะ"),
)


@question_type(
    "sci.process_skill_p6_foundation",
    display_name={"th": "เลือกสมมติฐานที่ตรวจสอบได้"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=PROCESS_SKILL_TOPIC,
)
class ProcessSkillP6Foundation(QuestionType):
    """The hypothesis a fair test could check, against same-topic sentences it could not."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        test = rng.choice(TESTS)
        return _labelled(
            stem=f"นักเรียนตั้งปัญหาว่า “{test.question}” ข้อใดเป็นสมมติฐานที่ตรวจสอบได้ด้วยการทดลอง",
            correct=test.hypothesis,
            wrongs=test.untestable,
            hint="สมมติฐานที่ดีบอกว่าถ้าเปลี่ยนสิ่งหนึ่งแล้ว สิ่งที่วัดได้จะเป็นอย่างไร และวัดตรวจสอบได้จริง",
            topic=PROCESS_SKILL_TOPIC,
        )


VARIABLES = (
    ("ตัวแปรต้น (สิ่งที่จงใจเปลี่ยน)", "changed"),
    ("ตัวแปรตาม (สิ่งที่วัดผล)", "measured"),
    ("ตัวแปรควบคุม (สิ่งที่ต้องทำให้เหมือนกัน)", "kept"),
)


VARIABLE_DECOYS = ("ปัญหาที่ตั้งไว้ก่อนเริ่มการทดลอง", "ข้อสรุปที่ได้หลังการทดลอง")


@question_type(
    "sci.process_skill_p6_fluency",
    display_name={"th": "ระบุตัวแปรต้น ตัวแปรตาม และตัวแปรควบคุม"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=PROCESS_SKILL_TOPIC,
)
class ProcessSkillP6Fluency(QuestionType):
    """One of the three variables; the wrong choices are the other two of the same test."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        test = rng.choice(TESTS)
        label, field = rng.choice(VARIABLES)
        return _labelled(
            stem=f"การทดลองหนึ่งตั้งปัญหาว่า “{test.question}” ข้อใดเป็น{label}ของการทดลองนี้",
            correct=getattr(test, field),
            wrongs=tuple(getattr(test, other) for _, other in VARIABLES if other != field)
                   + (rng.choice(VARIABLE_DECOYS),),
            hint="ตัวแปรต้นคือสิ่งที่จงใจเปลี่ยน ตัวแปรตามคือสิ่งที่วัด ตัวแปรควบคุมคือสิ่งที่ทำให้เหมือนกันทุกชุด",
            topic=PROCESS_SKILL_TOPIC,
        )


class Trial(NamedTuple):
    """A fair test whose result the stem gives as a table.

    ``trend`` is what the test really shows, so the drawn numbers never teach
    a result the world does not give.
    """
    setup: str
    changed: str
    levels: tuple[str, str, str, str]
    measured: str
    unit: str
    trend: str


TRIALS = (
    Trial("นักเรียนปล่อยรถของเล่นคันเดิมจากพื้นเอียงที่ความชันต่างกัน",
          "ความชันของพื้นเอียง", ("10 องศา", "20 องศา", "30 องศา", "40 องศา"),
          "ระยะที่รถเคลื่อนที่ได้", "เซนติเมตร", "up"),
    Trial("นักเรียนพันขดลวดรอบตะปูจำนวนรอบต่างกันแล้วต่อกับถ่านไฟฉายก้อนเดิม",
          "จำนวนรอบของขดลวด", ("10 รอบ", "20 รอบ", "30 รอบ", "40 รอบ"),
          "จำนวนคลิปที่ดูดได้", "ตัว", "up"),
    Trial("นักเรียนละลายเกลือช้อนเดียวกันในน้ำที่อุณหภูมิต่างกัน",
          "อุณหภูมิของน้ำ", ("20 องศาเซลเซียส", "40 องศาเซลเซียส", "60 องศาเซลเซียส", "80 องศาเซลเซียส"),
          "เวลาที่เกลือละลายหมด", "วินาที", "down"),
    Trial("นักเรียนวางก้อนน้ำแข็งขนาดเท่ากันในห้องที่อุณหภูมิต่างกัน",
          "อุณหภูมิของห้อง", ("20 องศาเซลเซียส", "25 องศาเซลเซียส", "30 องศาเซลเซียส", "35 องศาเซลเซียส"),
          "เวลาที่น้ำแข็งละลายหมด", "นาที", "down"),
    Trial("นักเรียนแขวนลูกตุ้มมวลต่างกันกับเชือกเส้นเดิมที่ยาวเท่ากัน แล้วปล่อยจากมุมเดียวกัน",
          "มวลของลูกตุ้ม", ("50 กรัม", "100 กรัม", "150 กรัม", "200 กรัม"),
          "จำนวนรอบที่ลูกตุ้มแกว่งได้ใน 30 วินาที", "รอบ", "flat"),
)


def trial_results(rng: Random, trend: str) -> list[int]:
    """Four results in the order of the levels: rising, falling, or level within ±1."""
    if trend == "flat":
        # Within ±1 of one value and never in order, so no reading shows a trend.
        base = rng.randint(14, 22)
        while True:
            values = [base + rng.choice((-1, 0, 1)) for _ in range(4)]
            if values != sorted(values) and values != sorted(values, reverse=True):
                return values
    start = rng.randint(10, 30)
    values = [start]
    for _ in range(3):
        values.append(values[-1] + rng.randint(4, 9))
    return values if trend == "up" else values[::-1]


@question_type(
    "sci.process_skill_p6_application",
    display_name={"th": "ลงข้อสรุปจากตารางผลการทดลอง"},
    level=PRIMARY_SIX, subject=SUBJECT, topic=PROCESS_SKILL_TOPIC,
)
class ProcessSkillP6Application(QuestionType):
    """Read a fair test's table and choose the conclusion its numbers support.

    Each test shows the trend it really has, with drawn numbers; the wrong
    choices are the other two trends and the conclusion that swaps which
    variable caused which.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        trial = rng.choice(TRIALS)
        trend = trial.trend
        values = trial_results(rng, trend)
        table = " / ".join(f"{level}: {value} {trial.unit}" for level, value in zip(trial.levels, values))
        up = f"เมื่อ{trial.changed}มากขึ้น {trial.measured}มากขึ้น"
        down = f"เมื่อ{trial.changed}มากขึ้น {trial.measured}น้อยลง"
        flat = f"{trial.changed}ไม่มีผลต่อ{trial.measured}อย่างชัดเจน"
        swapped = f"เมื่อ{trial.measured}มากขึ้น ทำให้{trial.changed}มากขึ้น"
        correct = {"up": up, "down": down, "flat": flat}[trend]
        return _labelled(
            stem=(f"{trial.setup} ได้ผลดังนี้ {table} "
                  "ข้อใดเป็นข้อสรุปที่สอดคล้องกับข้อมูลนี้มากที่สุด"),
            correct=correct,
            wrongs=tuple(s for s in (up, down, flat, swapped) if s != correct),
            hint="ไล่ดูตัวเลขจากค่าแรกไปค่าสุดท้ายว่าเพิ่มขึ้น ลดลง หรือเกือบเท่าเดิม แล้วตรวจว่าข้อสรุปพูดถึงสิ่งที่เปลี่ยนก่อน",
            topic=PROCESS_SKILL_TOPIC,
        )
