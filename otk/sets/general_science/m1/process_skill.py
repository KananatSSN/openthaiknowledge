"""ทักษะกระบวนการทางวิทยาศาสตร์

วิทยาศาสตร์ทั่วไป · ม.1 · เสริมทักษะ
Indicators: —

Sets moved here from: science_wave_g4.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_skills import EXPERIMENT_CHARTS, chart_alt, diagram_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_g4 import FIRST_SECONDARY, INVESTIGATIONS, SUBJECT

PROVENANCE = Provenance("original")


PROCESS_SKILL_TOPIC = "ทักษะกระบวนการทางวิทยาศาสตร์"


#: Parts of an investigation that are not one of its variables.
VARIABLE_DECOYS = ("ข้อสรุปที่ได้เมื่อการทดลองเสร็จสิ้น", "สมมติฐานที่ตั้งไว้ก่อนการทดลอง",
                   "ปัญหาที่ตั้งไว้ก่อนเริ่มการทดลอง")


class Skill(NamedTuple):
    name: str
    doing: str


SKILLS = (
    Skill("การสังเกต", "ใช้ประสาทสัมผัสเก็บรายละเอียดของสิ่งที่ศึกษาโดยไม่ใส่ความเห็นของตนเอง"),
    Skill("การวัด", "ใช้เครื่องมือหาค่าปริมาณของสิ่งที่ศึกษาพร้อมระบุหน่วยให้ถูกต้อง"),
    Skill("การจำแนกประเภท", "แบ่งสิ่งของออกเป็นกลุ่มโดยใช้เกณฑ์ที่กำหนดไว้อย่างชัดเจน"),
    Skill("การลงความเห็นจากข้อมูล", "อธิบายหรือให้เหตุผลเพิ่มเติมจากสิ่งที่สังเกตได้ โดยอาศัยความรู้เดิม"),
    Skill("การพยากรณ์", "คาดคะเนสิ่งที่จะเกิดขึ้นต่อไปโดยอาศัยแบบรูปของข้อมูลที่มีอยู่"),
    Skill("การตั้งสมมติฐาน", "คาดคะเนคำตอบของปัญหาล่วงหน้าในรูปที่ตรวจสอบได้ด้วยการทดลอง"),
    Skill("การกำหนดและควบคุมตัวแปร", "ระบุว่าจะเปลี่ยนอะไร วัดอะไร และต้องทำอะไรให้เหมือนกันทุกชุดการทดลอง"),
    Skill("การตีความหมายข้อมูลและลงข้อสรุป", "อ่านแบบรูปหรือแนวโน้มจากข้อมูลที่จัดกระทำแล้ว แล้วตอบปัญหาที่ตั้งไว้"),
)


#: Pairs of (what was observed, what was inferred from it) about one scene. Both
#: sentences are reasonable; only one is a record of what the senses took in.
#: This is the distinction ม.1 learners get wrong most often, and the reason the
#: set exists — a การลงความเห็น sentence *feels* like an observation.
OBSERVATION_PAIRS = (
    ("พื้นถนนเปียกและมีน้ำขังเป็นแอ่ง", "เมื่อคืนนี้ฝนตกหนัก"),
    ("ใบของต้นไม้ต้นนี้มีสีเหลืองเกือบทั้งต้น", "ต้นไม้ต้นนี้ขาดธาตุอาหาร"),
    ("มีฟองแก๊สเกิดขึ้นที่ผิวของแผ่นโลหะในบีกเกอร์", "แผ่นโลหะกำลังทำปฏิกิริยากับกรด"),
    ("น้ำในแก้วมีหยดน้ำเกาะอยู่รอบนอกของแก้ว", "อากาศรอบแก้วมีไอน้ำอยู่มาก"),
    ("ก้อนหินก้อนนี้มีมวล 250 กรัม และมีผิวขรุขระ", "ก้อนหินก้อนนี้ถูกน้ำพัดพามาเป็นเวลานาน"),
)


#: Which of the three a question asks for, and the wording each one needs.
_VARIABLE_KINDS = (
    ("ตัวแปรต้น", "independent"),
    ("ตัวแปรตาม", "dependent"),
    ("ตัวแปรที่ต้องควบคุมให้คงที่", "controlled"),
)


@question_type(
    "sci.process_skill_foundation",
    display_name={"th": "ระบุทักษะกระบวนการทางวิทยาศาสตร์จากสิ่งที่ลงมือทำ"},
    level=FIRST_SECONDARY, subject=SUBJECT, topic=PROCESS_SKILL_TOPIC,
)
class ProcessSkillFoundation(QuestionType):
    """Name the skill from the action, or the action from the skill."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        skill = rng.choice(SKILLS)
        if rng.random() < 0.5:
            wrongs = tuple(s.name for s in SKILLS if s.name != skill.name)
            return _labelled(
                stem=f"การ{skill.doing} ตรงกับทักษะกระบวนการทางวิทยาศาสตร์ข้อใด",
                correct=skill.name, wrongs=tuple(wrongs),
                hint="ดูว่าสิ่งที่ลงมือทำคือการเก็บข้อมูล การจัดการข้อมูล หรือการคิดต่อจากข้อมูล",
                topic=PROCESS_SKILL_TOPIC,
            )
        wrongs = tuple(s.doing for s in SKILLS if s.name != skill.name)
        return _labelled(
            stem=f"ทักษะ “{skill.name}” หมายถึงการทำสิ่งใด",
            correct=skill.doing, wrongs=tuple(wrongs),
            hint="อ่านชื่อทักษะแล้วถามว่าต้องลงมือทำอะไรจริง ๆ จึงจะเรียกว่าใช้ทักษะนั้น",
            topic=PROCESS_SKILL_TOPIC,
        )


@question_type(
    "sci.process_skill_fluency",
    display_name={"th": "แยกการสังเกตออกจากการลงความเห็นจากข้อมูล"},
    level=FIRST_SECONDARY, subject=SUBJECT, topic=PROCESS_SKILL_TOPIC,
)
class ProcessSkillFluency(QuestionType):
    """Which sentence is what the senses recorded, and which is already a reason.

    Both directions are asked, because a learner who has memorised "observations
    are short" gets the ``การลงความเห็น`` direction wrong.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        index = rng.randrange(len(OBSERVATION_PAIRS))
        observed, inferred = OBSERVATION_PAIRS[index]
        others = [p for i, p in enumerate(OBSERVATION_PAIRS) if i != index]
        pair = rng.sample(others, 2)
        if rng.random() < 0.5:
            return _labelled(
                stem="ข้อใดเป็นการสังเกต ไม่ใช่การลงความเห็นจากข้อมูล",
                correct=observed,
                wrongs=(inferred, pair[0][1], pair[1][1]),
                hint=("การสังเกตคือสิ่งที่รับรู้ได้ด้วยประสาทสัมผัสตรง ๆ "
                      "ถ้าประโยคนั้นบอกสาเหตุหรือเหตุผล แสดงว่าเป็นการลงความเห็นแล้ว"),
                topic=PROCESS_SKILL_TOPIC,
            )
        return _labelled(
            stem="ข้อใดเป็นการลงความเห็นจากข้อมูล ไม่ใช่การสังเกต",
            correct=inferred,
            wrongs=(observed, pair[0][0], pair[1][0]),
            hint=("การลงความเห็นคือการอธิบายสาเหตุเพิ่มเติมจากสิ่งที่สังเกตได้ "
                  "โดยอาศัยความรู้เดิม ไม่ใช่สิ่งที่ประสาทสัมผัสรับรู้โดยตรง"),
            topic=PROCESS_SKILL_TOPIC,
        )


@question_type(
    "sci.process_skill_variables",
    display_name={"th": "ระบุตัวแปรต้น ตัวแปรตาม และตัวแปรควบคุมจากการทดลอง"},
    level=FIRST_SECONDARY, subject=SUBJECT, topic=PROCESS_SKILL_TOPIC,
)
class ProcessSkillVariables(QuestionType):
    """The three variables, from the same investigation the hypothesis came from.

    The distractors are always the *other two* variables of the same experiment,
    never variables from a different one. A learner who can eliminate by subject
    matter has not identified anything; the choice has to turn on which one is
    changed, which is measured, and which is held the same.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        case = rng.choice(INVESTIGATIONS)
        label, field = rng.choice(_VARIABLE_KINDS)
        correct = getattr(case, field)
        wrongs = tuple(getattr(case, other) for _, other in _VARIABLE_KINDS
                       if other != field)
        return _labelled(
            stem=(f"การทดลองหนึ่งตั้งปัญหาว่า “{case.question}” "
                  f"ในการทดลองนี้ {label}คือข้อใด"),
            correct=correct,
            wrongs=wrongs + (rng.choice(VARIABLE_DECOYS),),
            hint=("ตัวแปรต้นคือสิ่งที่ผู้ทดลองจงใจเปลี่ยน ตัวแปรตามคือสิ่งที่วัดผล "
                  "ตัวแปรควบคุมคือสิ่งที่ต้องทำให้เหมือนกันทุกชุดการทดลอง"),
            topic=PROCESS_SKILL_TOPIC,
        )


@question_type(
    "sci.process_skill_application",
    display_name={"th": "ตีความหมายข้อมูลจากกราฟผลการทดลองและลงข้อสรุป"},
    level=FIRST_SECONDARY, subject=SUBJECT, topic=PROCESS_SKILL_TOPIC,
)
class ProcessSkillApplication(QuestionType):
    """Read the drawn chart, then answer one of three things about it.

    The chart's bars are numbered, not named, so the stem supplies the
    experiment. Two of the three questions are answered by reading the picture;
    the third asks what the reading licenses a learner to *conclude*, which is
    where การตีความหมายข้อมูล stops being การอ่านกราฟ.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        spec = rng.choice(EXPERIMENT_CHARTS)
        best, worst = spec.best, spec.worst
        others = [n for n in (1, 2, 3, 4) if n != best]
        kind = rng.randrange(4)
        if kind == 3:
            stem = (f"กราฟแสดง{spec.unit_th} ของชุดการทดลองที่ 1 ถึง 4 "
                    f"จากกราฟ ชุดการทดลองใดให้ค่าน้อยที่สุด")
            correct = f"ชุดที่ {worst}"
            wrongs = tuple(f"ชุดที่ {n}" for n in (1, 2, 3, 4) if n != worst)
        elif kind == 0:
            stem = (f"กราฟแสดง{spec.unit_th} ของชุดการทดลองที่ 1 ถึง 4 "
                    f"จากกราฟ ชุดการทดลองใดให้ค่ามากที่สุด")
            correct = f"ชุดที่ {best}"
            wrongs = tuple(f"ชุดที่ {n}" for n in others)
        elif kind == 1:
            stem = (f"กราฟแสดง{spec.unit_th} ของชุดการทดลองที่ 1 ถึง 4 "
                    f"จากกราฟ ค่าที่วัดได้ของชุดที่ {best} มากกว่าชุดที่ {worst} อยู่เท่าใด")
            high, low = max(spec.values), min(spec.values)
            # The three named misreadings: reading one bar instead of the
            # difference (either bar), and adding the two instead of subtracting.
            unit = spec.unit_short
            wrongs = (f"{high} {unit}", f"{low} {unit}", f"{high + low} {unit}")
            correct = f"{high - low} {unit}"
        else:
            stem = (f"กราฟแสดง{spec.unit_th} ของชุดการทดลองที่ 1 ถึง 4 "
                    f"ซึ่งต่างกันที่ปริมาณของปัจจัยที่ศึกษาเท่านั้น "
                    f"ข้อสรุปใดกล่าวได้จากกราฟนี้")
            correct = (f"ชุดที่ {best} ให้ค่าที่วัดได้มากที่สุด "
                       f"ปัจจัยที่ศึกษาจึงมีผลต่อสิ่งที่วัด")
            wrongs = tuple(rng.sample((
                "ปัจจัยที่ศึกษาไม่มีผลต่อสิ่งที่วัดเลย เพราะทุกชุดได้ค่าที่ต่างกัน",
                "ยิ่งเพิ่มปัจจัยที่ศึกษามากขึ้น ค่าที่วัดได้จะยิ่งมากขึ้นเสมอทุกชุด",
                f"ชุดที่ {worst} ให้ค่าที่วัดได้มากที่สุด จึงเป็นชุดที่ดีที่สุด",
                "ปัจจัยที่ศึกษาเป็นตัวแปรตาม เพราะเป็นสิ่งที่อ่านค่าได้จากกราฟ",
                f"ชุดที่ {best} และชุดที่ {worst} ให้ค่าเท่ากัน จึงยังสรุปไม่ได้",
            ), 3))
        return diagram_question(
            spec.asset_id, chart_alt(spec),
            stem=stem, correct=correct, wrongs=wrongs,
            hint=("อ่านความสูงของแต่ละแท่งเทียบกับเส้นตารางบนแกนตั้งก่อน "
                  "แล้วจึงตอบเฉพาะสิ่งที่กราฟบอกได้จริง"),
            topic=PROCESS_SKILL_TOPIC,
        )
