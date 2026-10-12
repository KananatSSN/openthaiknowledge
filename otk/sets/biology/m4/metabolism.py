"""ปฏิกิริยาเคมีในสิ่งมีชีวิต

ชีวะ · ม.4 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 1 ม.4/8

Sets moved here from: science_wave_f45.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f45 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_REACTION = "ปฏิกิริยาเคมีในสิ่งมีชีวิต"


REACTIONS = (
    ("การสังเคราะห์ด้วยแสง", "แอแนบอลิซึม", "ดูดพลังงาน"), ("การสร้างโปรตีนจากกรดอะมิโน", "แอแนบอลิซึม", "ดูดพลังงาน"),
    ("การสร้างไกลโคเจนในตับ", "แอแนบอลิซึม", "ดูดพลังงาน"), ("การสังเคราะห์ DNA", "แอแนบอลิซึม", "ดูดพลังงาน"),
    ("การหายใจระดับเซลล์", "แคแทบอลิซึม", "คายพลังงาน"), ("การย่อยแป้งเป็นกลูโคส", "แคแทบอลิซึม", "คายพลังงาน"),
    ("การสลายไขมันเป็นกรดไขมันและกลีเซอรอล", "แคแทบอลิซึม", "คายพลังงาน"),
    ("การสลาย ATP เป็น ADP และฟอสเฟต", "แคแทบอลิซึม", "คายพลังงาน"),
)


ENERGY_FACTS = (
    ("ATP มีบทบาทอย่างไรในเซลล์", "เป็นตัวถ่ายทอดพลังงานจากปฏิกิริยาคายพลังงานไปยังปฏิกิริยาดูดพลังงาน",
     ("เป็นเอนไซม์ที่ลดพลังงานก่อกัมมันต์ของปฏิกิริยาดูดพลังงาน", "เป็นสารพันธุกรรมที่ควบคุมการสร้างโปรตีนในเซลล์", "เป็นโครงสร้างของเยื่อหุ้มเซลล์ที่ควบคุมการผ่านเข้าออกของสาร")),
    ("เมแทบอลิซึมหมายถึงอะไร", "ปฏิกิริยาเคมีทั้งหมดที่เกิดขึ้นในสิ่งมีชีวิต",
     ("เฉพาะปฏิกิริยาย่อยอาหารในทางเดินอาหาร", "เฉพาะปฏิกิริยาสร้างสารในเซลล์", "การเคลื่อนที่และการเจริญเติบโตของสิ่งมีชีวิต")),
    ("พลังงานก่อกัมมันต์ในปฏิกิริยาในเซลล์คืออะไร", "พลังงานต่ำสุดที่ต้องได้รับเพื่อเริ่มปฏิกิริยา",
     ("พลังงานที่ปฏิกิริยาคายออกมา", "พลังงานที่เก็บอยู่ในพันธะของ ATP หนึ่งโมเลกุล", "พลังงานสูงสุดที่ปฏิกิริยาคายออกมา")),
    ("เพราะเหตุใดปฏิกิริยาในเซลล์จึงเกิดได้ที่อุณหภูมิร่างกาย", "มีเอนไซม์ช่วยลดพลังงานก่อกัมมันต์",
     ("ร่างกายมีอุณหภูมิสูงมาก", "ปฏิกิริยาในเซลล์ไม่ต้องใช้พลังงาน", "เซลล์มีความดันสูงจนปฏิกิริยาเกิดเร็ว")),
)


@question_type(
    "biology.metabolism_foundation",
    display_name={"th": "แอแนบอลิซึมและแคแทบอลิซึม"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_REACTION,
)
class MetabolismFoundation(QuestionType):
    """Building up takes energy; breaking down releases it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        reaction, kind, energy = rng.choice(REACTIONS)
        if rng.random() < 0.5:
            right = f"{kind} เพราะ{energy}"
            other_kind = "แคแทบอลิซึม" if kind == "แอแนบอลิซึม" else "แอแนบอลิซึม"
            other_energy = "คายพลังงาน" if energy == "ดูดพลังงาน" else "ดูดพลังงาน"
            return _labelled(stem=f"{reaction}จัดเป็นปฏิกิริยาแบบใด", correct=right,
                             wrongs=(f"{other_kind} เพราะ{other_energy}", f"{kind} เพราะ{other_energy}",
                                     f"{other_kind} เพราะ{energy}"),
                             topic=TOPIC_REACTION, hint="แอแนบอลิซึมสร้างสารโมเลกุลใหญ่และดูดพลังงาน แคแทบอลิซึมสลายสารและคายพลังงาน")
        match = [r[0] for r in REACTIONS if r[1] == kind]
        others = [r[0] for r in REACTIONS if r[1] != kind]
        return _labelled(stem=f"ข้อใดเป็นปฏิกิริยาแบบ{kind}", correct=rng.choice(match), wrongs=tuple(others),
                         topic=TOPIC_REACTION, hint="แอแนบอลิซึมสร้างสารโมเลกุลใหญ่ แคแทบอลิซึมสลายสาร")


@question_type(
    "biology.metabolism_fluency",
    display_name={"th": "พลังงานในปฏิกิริยาเคมีของเซลล์และ ATP"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_REACTION,
)
class MetabolismFluency(QuestionType):
    """ATP carries energy between reactions; enzymes lower the barrier."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(ENERGY_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_REACTION,
                         hint="ATP ถ่ายทอดพลังงาน เอนไซม์ลดพลังงานก่อกัมมันต์")


@question_type(
    "biology.metabolism_application",
    display_name={"th": "คำนวณพลังงานและ ATP ในปฏิกิริยาของเซลล์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_REACTION,
)
class MetabolismApplication(QuestionType):
    """ATP → ADP releases about 30.5 kJ/mol; count the energy a job needs."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            moles = Fraction(rng.randrange(1, 41), 2)
            per = Fraction(305, 10)
            return numeric(stem=f"การสลาย ATP เป็น ADP ปล่อยพลังงานประมาณ 30.5 kJ/mol ถ้าเซลล์สลาย ATP {show(moles)} โมล จะได้พลังงานกี่ kJ",
                           answer=moles * per, wrongs=[moles * 30, per, moles * per * 2], unit="kJ", topic=TOPIC_REACTION,
                           hint="พลังงาน = จำนวนโมล × 30.5 kJ/mol")
        reactant = rng.randrange(100, 401, 10)
        peak = reactant + rng.randrange(50, 201, 10)
        lowered = peak - rng.randrange(20, peak - reactant, 10) if peak - reactant > 20 else peak - 10
        return numeric(stem=f"ปฏิกิริยาในเซลล์มีพลังงานสารตั้งต้น {reactant} kJ ต้องมีพลังงานถึง {peak} kJ จึงเกิดปฏิกิริยา "
                            f"เมื่อมีเอนไซม์ลดลงเหลือ {lowered} kJ เอนไซม์ลดพลังงานก่อกัมมันต์ลงกี่ kJ",
                       answer=peak - lowered, wrongs=[lowered - reactant, peak - reactant, lowered], unit="kJ",
                       topic=TOPIC_REACTION, hint="พลังงานก่อกัมมันต์ = ยอด − สารตั้งต้น เอนไซม์ลดส่วนนี้ลง")
