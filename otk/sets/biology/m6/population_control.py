"""ปัจจัยที่ควบคุมการเติบโตของประชากร

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 5 ม.6/8

Sets moved here from: science_wave_f72.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f72 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_CONTROL = "ปัจจัยที่ควบคุมการเติบโตของประชากร"


DEPENDENT = ("การแย่งอาหารระหว่างสมาชิกเมื่อประชากรหนาแน่น", "โรคระบาดที่แพร่เร็วเมื่ออยู่กันแออัด", "การถูกผู้ล่ากินที่เพิ่มขึ้นเมื่อเหยื่อมีมาก",
             "ปรสิตที่ติดต่อกันได้ง่ายเมื่อประชากรหนาแน่น", "การสะสมของของเสียในที่อยู่ที่แออัด")


INDEPENDENT = ("น้ำท่วมฉับพลัน", "ไฟป่าจากฟ้าผ่า", "ความแห้งแล้งรุนแรง", "อากาศหนาวจัดผิดฤดู", "ภูเขาไฟระเบิด")


CONTROL_HINT = ("ปัจจัยที่ขึ้นกับความหนาแน่น เช่น การแข่งขัน โรค การล่า มีผลรุนแรงขึ้นเมื่อประชากรหนาแน่น ปัจจัยที่ไม่ขึ้นกับความหนาแน่น "
                "เช่น ภัยธรรมชาติ มีผลโดยไม่ขึ้นกับจำนวนประชากร การเปลี่ยนแปลง = เกิด + อพยพเข้า − ตาย − อพยพออก")


@question_type(
    "biology.population_control_foundation",
    display_name={"th": "ปัจจัยที่ขึ้นกับและไม่ขึ้นกับความหนาแน่นของประชากร"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_CONTROL,
)
class PopulationControlFoundation(QuestionType):
    """Density-dependent or not."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        dependent = rng.random() < 0.5
        same, other = (DEPENDENT, INDEPENDENT) if dependent else (INDEPENDENT, DEPENDENT)
        kind = "ปัจจัยที่ขึ้นกับความหนาแน่นของประชากร" if dependent else "ปัจจัยที่ไม่ขึ้นกับความหนาแน่นของประชากร"
        if rng.random() < 0.5:
            return _labelled(stem=f"ข้อใดเป็น{kind}", correct=rng.choice(same), wrongs=tuple(other), topic=TOPIC_CONTROL,
                             hint=CONTROL_HINT)
        return _labelled(stem=f"\"{rng.choice(same)}\" เป็นปัจจัยควบคุมประชากรแบบใด", correct=kind,
                         wrongs=("ปัจจัยที่ไม่ขึ้นกับความหนาแน่นของประชากร" if dependent else "ปัจจัยที่ขึ้นกับความหนาแน่นของประชากร",
                                 "การเพิ่มแบบเอ็กโพเนนเชียล", "การกระจายแบบสุ่ม"), topic=TOPIC_CONTROL, hint=CONTROL_HINT)


@question_type(
    "biology.population_control_fluency",
    display_name={"th": "ผลของปัจจัยต่าง ๆ ต่อการเปลี่ยนแปลงของประชากร"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_CONTROL,
)
class PopulationControlFluency(QuestionType):
    """Predator-prey swings, and what a factor does to numbers."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        facts = (
            ("ประชากรกระต่ายเพิ่มขึ้นมาก ต่อมาประชากรหมาป่าที่ล่ากระต่ายจะเป็นอย่างไร", "เพิ่มขึ้นตามในเวลาต่อมา",
             ("ลดลงทันทีเพราะเหยื่อมีมาก", "คงที่ตลอดไม่ว่าเหยื่อเท่าใด", "หายไปทั้งหมด", "ไม่มีความสัมพันธ์กัน", "เปลี่ยนไปล่าพืชแทน")),
            ("เมื่อประชากรผู้ล่าเพิ่มขึ้นจนกินเหยื่อมาก ประชากรเหยื่อจะเป็นอย่างไรต่อมา", "ลดลง แล้วประชากรผู้ล่าจึงลดลงตาม",
             ("เพิ่มขึ้นตลอด", "คงที่ไม่เปลี่ยนแปลง", "เพิ่มเป็นสองเท่าทันทีเพราะไม่มีผู้ล่า", "ไม่ได้รับผลใด ๆ เพราะผู้ล่ามีอาหารอื่น", "กลายเป็นผู้ล่าแทน")),
            ("เหตุใดโรคระบาดจึงเป็นปัจจัยที่ขึ้นกับความหนาแน่น", "สมาชิกอยู่ใกล้กันมาก เชื้อจึงแพร่ได้เร็วและกว้าง",
             ("เชื้อโรคเกิดเฉพาะในที่แห้งแล้ง จึงไม่เกี่ยวกับความหนาแน่น", "โรคฆ่าสมาชิกเท่ากันทุกความหนาแน่น", "โรคเกิดจากสภาพอากาศเท่านั้น", "สมาชิกยิ่งมากยิ่งไม่ติดเชื้อ เพราะมีภูมิคุ้มกันร่วมกัน")),
            ("การนำศัตรูธรรมชาติมาควบคุมศัตรูพืชอาศัยหลักการใด", "เพิ่มการล่า ซึ่งขึ้นกับความหนาแน่นของศัตรูพืช",
             ("เพิ่มอาหารให้ศัตรูพืช", "ทำให้เกิดน้ำท่วมจนศัตรูพืชตาย", "เพิ่มพื้นที่อยู่ให้ศัตรูพืช", "ลดจำนวนผู้ผลิตที่เป็นอาหารของศัตรูพืชทั้งหมด", "เพิ่มการใช้สารเคมีกำจัดศัตรูพืชทุกชนิดในพื้นที่")),
            ("ไฟป่าฆ่าสัตว์ในพื้นที่ร้อยละ 80 ไม่ว่าประชากรจะมีมากหรือน้อย ไฟป่าจึงจัดเป็นปัจจัยแบบใด", "ปัจจัยที่ไม่ขึ้นกับความหนาแน่นของประชากร",
             ("ปัจจัยที่ขึ้นกับความหนาแน่นของประชากร", "การแข่งขันภายในประชากร", "การล่าเหยื่อ", "ปรสิต")),
            ('การแข่งขันแย่งอาหารภายในประชากรเป็นปัจจัยแบบใด', 'ปัจจัยที่ขึ้นกับความหนาแน่น เพราะยิ่งสมาชิกมาก อาหารต่อตัวยิ่งน้อย',
             ('ปัจจัยที่ไม่ขึ้นกับความหนาแน่น เพราะเกิดเท่ากันทุกกรณี', 'ไม่ใช่ปัจจัยที่ควบคุมขนาดประชากรเลย', 'ปัจจัยทางกายภาพแบบเดียวกับอุณหภูมิและแสง', 'ปัจจัยที่เกิดได้เฉพาะในประชากรพืช', 'ปัจจัยที่ทำให้ประชากรเพิ่มขึ้นเสมอไม่ว่าจะหนาแน่นเพียงใด')),
            ('ฤดูหนาวที่หนาวจัดผิดปกติทำให้แมลงตายจำนวนมาก ไม่ว่าจะมีแมลงมากหรือน้อย จัดเป็นปัจจัยแบบใด', 'ปัจจัยที่ไม่ขึ้นกับความหนาแน่นของประชากร',
             ('ปัจจัยที่ขึ้นกับความหนาแน่นของประชากร', 'การแข่งขันภายในประชากร', 'การล่าเหยื่อ', 'ภาวะปรสิต')),
            ('ขีดจำกัดการรองรับของสิ่งแวดล้อมหมายถึงอะไร', 'ขนาดประชากรสูงสุดที่สิ่งแวดล้อมรองรับได้อย่างยั่งยืน',
             ('จำนวนสมาชิกที่เกิดใหม่ในหนึ่งปี', 'จำนวนผู้ล่าสูงสุดที่อยู่ในพื้นที่', 'ขนาดพื้นที่ที่ประชากรใช้เป็นที่อยู่', 'อัตราการตายเฉลี่ยของประชากรในหนึ่งปี', 'จำนวนชนิดของสิ่งมีชีวิตในพื้นที่นั้น')),
        )
        stem, right, wrongs = rng.choice(facts)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_CONTROL, hint=CONTROL_HINT)


@question_type(
    "biology.population_control_application",
    display_name={"th": "คำนวณการเปลี่ยนแปลงขนาดประชากร"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_CONTROL,
)
class PopulationControlApplication(QuestionType):
    """Births and immigrants in, deaths and emigrants out."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        while True:
            start = rng.randrange(200, 5001, 50)
            births, deaths = rng.randrange(10, 401, 5), rng.randrange(10, 401, 5)
            immig, emig = rng.randrange(0, 151, 5), rng.randrange(0, 151, 5)
            end = start + births + immig - deaths - emig
            if end >= start // 2 and end != start:
                break
        if rng.random() < 0.6:
            return numeric(stem=f"ประชากรนกมี {start} ตัว ในหนึ่งปีมีการเกิด {births} ตัว ตาย {deaths} ตัว อพยพเข้า {immig} ตัว และอพยพออก {emig} ตัว "
                                f"เมื่อสิ้นปีมีนกกี่ตัว", answer=end,
                           wrongs=[start + births - deaths, start + births + deaths + immig + emig, start + births - deaths + emig - immig],
                           unit="ตัว", topic=TOPIC_CONTROL, hint=CONTROL_HINT)
        change = end - start
        return numeric(stem=f"ประชากรนกในหนึ่งปีมีการเกิด {births} ตัว ตาย {deaths} ตัว อพยพเข้า {immig} ตัว และอพยพออก {emig} ตัว "
                            f"ประชากรเปลี่ยนแปลงสุทธิกี่ตัว (ติดลบถ้าลดลง)", answer=change,
                       wrongs=[births - deaths, immig - emig, births + immig + deaths + emig], unit="ตัว", allow_negative=True,
                       topic=TOPIC_CONTROL, hint=CONTROL_HINT)
