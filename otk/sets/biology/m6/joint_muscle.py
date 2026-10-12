"""ข้อต่อและการทำงานของกล้ามเนื้อโครงร่าง

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.6/11

Sets moved here from: science_wave_f68.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f68 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_JOINT = "ข้อต่อและการทำงานของกล้ามเนื้อโครงร่าง"


JOINTS = (
    ("ข้อต่อแบบลูกกลมในเบ้า", ("ข้อไหล่", "ข้อสะโพก"), "เคลื่อนไหวได้รอบทิศทาง"),
    ("ข้อต่อแบบบานพับ", ("ข้อศอก", "ข้อเข่า", "ข้อนิ้วมือ"), "เคลื่อนไหวได้ในแนวเดียวคล้ายบานพับประตู"),
    ("ข้อต่อแบบเดือย", ("ข้อต่อระหว่างกระดูกสันหลังข้อที่ 1 และ 2",), "หมุนรอบแกนได้ เช่น การส่ายหน้า"),
    ("ข้อต่อแบบอานม้า", ("ข้อต่อที่โคนนิ้วหัวแม่มือ",), "เคลื่อนไหวได้สองแนวตั้งฉากกัน"),
    ("ข้อต่อแบบเลื่อน", ("ข้อต่อระหว่างกระดูกข้อมือ", "ข้อต่อระหว่างกระดูกข้อเท้า"), "กระดูกเลื่อนไถลผ่านกันได้เล็กน้อย"),
    ("ข้อต่อที่เคลื่อนไหวไม่ได้", ("รอยต่อของกะโหลกศีรษะ",), "กระดูกยึดติดกันแน่น"),
)


JOINT_HINT = ("ไหล่และสะโพกเป็นลูกกลมในเบ้า ศอกและเข่าเป็นบานพับ ข้อที่ส่ายหน้าเป็นแบบเดือย โคนนิ้วหัวแม่มือเป็นแบบอานม้า "
              "ข้อมือเป็นแบบเลื่อน เอ็นยึดข้อเชื่อมกระดูกกับกระดูก เอ็นยึดกระดูกเชื่อมกล้ามเนื้อกับกระดูก")


JOINT_FACTS = (
    ("เมื่องอแขน กล้ามเนื้อไบเซปส์และไตรเซปส์ทำงานอย่างไร", "ไบเซปส์หดตัว ไตรเซปส์คลายตัว",
     ("ไบเซปส์คลายตัว ไตรเซปส์หดตัว", "หดตัวทั้งสองมัด", "คลายตัวทั้งสองมัด", "ไบเซปส์ยืดออกดันกระดูก")),
    ("เมื่อเหยียดแขน กล้ามเนื้อไบเซปส์และไตรเซปส์ทำงานอย่างไร", "ไตรเซปส์หดตัว ไบเซปส์คลายตัว",
     ("ไบเซปส์หดตัว ไตรเซปส์คลายตัว", "หดตัวทั้งสองมัด", "คลายตัวทั้งสองมัด", "ไตรเซปส์ยืดออกดันกระดูก")),
    ("เอ็นยึดข้อ (ligament) ทำหน้าที่อะไร", "ยึดกระดูกกับกระดูกบริเวณข้อต่อ",
     ("ยึดกล้ามเนื้อกับกระดูก", "สร้างเซลล์เม็ดเลือด", "หล่อลื่นข้อต่อ", "ส่งกระแสประสาท")),
    ("เอ็นยึดกระดูก (tendon) ทำหน้าที่อะไร", "ยึดกล้ามเนื้อกับกระดูก",
     ("ยึดกระดูกกับกระดูก", "สร้างน้ำไขข้อ", "ลดแรงกระแทกระหว่างกระดูกสันหลัง", "สร้างเซลล์เม็ดเลือด")),
    ("น้ำไขข้อมีหน้าที่อะไร", "หล่อลื่นและลดการเสียดสีของกระดูกที่ข้อต่อ",
     ("ยึดกระดูกให้ติดกัน", "สร้างกล้ามเนื้อใหม่", "ส่งกระแสประสาท", "ลำเลียงออกซิเจน")),
    ("กล้ามเนื้อโครงร่างทำให้กระดูกเคลื่อนที่ได้อย่างไร", "หดตัวดึงกระดูกได้อย่างเดียว จึงต้องมีกล้ามเนื้อคู่ที่ทำงานตรงข้ามกัน",
     ("ผลักกระดูกออกได้โดยตรง", "หดและดันกระดูกได้เท่ากัน", "ทำงานโดยไม่ต้องยึดกับกระดูก", "ใช้น้ำไขข้อดันกระดูก")),
)


@question_type(
    "biology.joint_muscle_foundation",
    display_name={"th": "ชนิดของข้อต่อในร่างกายมนุษย์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_JOINT,
)
class JointMuscleFoundation(QuestionType):
    """Name the joint, and how it moves."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind, examples, moves = rng.choice(JOINTS)
        example = rng.choice(examples)
        others = rng.sample([j for j in JOINTS if j[0] != kind], 3)
        roll = rng.random()
        if roll < 0.4:
            return _labelled(stem=f"{example}เป็นข้อต่อชนิดใด", correct=kind, wrongs=tuple(j[0] for j in others), topic=TOPIC_JOINT, hint=JOINT_HINT)
        if roll < 0.7:
            return _labelled(stem=f"ข้อใดเป็นตัวอย่างของ{kind}", correct=example, wrongs=tuple(rng.choice(j[1]) for j in others),
                             topic=TOPIC_JOINT, hint=JOINT_HINT)
        return _labelled(stem=f"{kind}เคลื่อนไหวได้อย่างไร", correct=moves, wrongs=tuple(j[2] for j in others), topic=TOPIC_JOINT, hint=JOINT_HINT)


@question_type(
    "biology.joint_muscle_fluency",
    display_name={"th": "กล้ามเนื้อที่ทำงานตรงข้ามกัน เอ็น และน้ำไขข้อ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_JOINT,
)
class JointMuscleFluency(QuestionType):
    """Biceps against triceps, ligament against tendon, synovial fluid."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.45:
            moves = (("งอแขนที่ข้อศอก", "กล้ามเนื้อไบเซปส์"), ("เหยียดแขนที่ข้อศอก", "กล้ามเนื้อไตรเซปส์"),
                     ("เหยียดขาที่ข้อเข่า", "กล้ามเนื้อต้นขาด้านหน้า"), ("งอขาที่ข้อเข่า", "กล้ามเนื้อต้นขาด้านหลัง"),
                     ("เขย่งปลายเท้า", "กล้ามเนื้อน่อง"))
            move, muscle = rng.choice(moves)
            pool = [m for _, m in moves if m != muscle]
            return _labelled(stem=f"ขณะ{move} กล้ามเนื้อมัดใดหดตัวเป็นหลัก", correct=muscle, wrongs=tuple(pool),
                             topic=TOPIC_JOINT, hint=JOINT_HINT)
        stem, right, wrongs = rng.choice(JOINT_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_JOINT, hint=JOINT_HINT)


@question_type(
    "biology.joint_muscle_application",
    display_name={"th": "คำนวณแรงของกล้ามเนื้อจากหลักคาน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_JOINT,
)
class JointMuscleApplication(QuestionType):
    """Muscle force × its arm = load × its arm, about the elbow."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        muscle_arm = rng.choice((3, 4, 5))
        load_arm = rng.choice((25, 30, 32, 35, 40))
        load = rng.choice((10, 20, 30, 40, 50, 60))
        force = Fraction(load * load_arm, muscle_arm)
        if (force * 100).denominator != 1:
            load_arm = muscle_arm * 8
            force = Fraction(load * load_arm, muscle_arm)
        if rng.random() < 0.6:
            return numeric(stem=f"ถือวัตถุหนัก {load} N ไว้ที่มือซึ่งอยู่ห่างข้อศอก {load_arm} cm กล้ามเนื้อไบเซปส์ยึดกับกระดูกห่างข้อศอก {muscle_arm} cm "
                                f"ถ้าแขนท่อนล่างอยู่ในแนวระดับและอยู่นิ่ง ไบเซปส์ต้องออกแรงกี่นิวตัน", answer=force,
                           wrongs=[load, Fraction(load * muscle_arm, load_arm) if (Fraction(load * muscle_arm, load_arm) * 100).denominator == 1
                                   else load * 2, load * load_arm], unit="N", topic=TOPIC_JOINT,
                           hint="ข้อศอกเป็นจุดหมุน แรงไบเซปส์ × ระยะถึงข้อศอก = น้ำหนักวัตถุ × ระยะถึงข้อศอก")
        return numeric(stem=f"ไบเซปส์ออกแรง {show(force)} N ที่ระยะ {muscle_arm} cm จากข้อศอก ถือวัตถุไว้ที่มือห่างข้อศอก {load_arm} cm "
                            f"ในแนวระดับอย่างสมดุล วัตถุหนักกี่นิวตัน", answer=load,
                       wrongs=[force, force * muscle_arm, load * 2], unit="N", topic=TOPIC_JOINT,
                       hint="น้ำหนักวัตถุ = แรงไบเซปส์ × ระยะของไบเซปส์ ÷ ระยะของวัตถุ")
