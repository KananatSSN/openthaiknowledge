"""การสะท้อน การหักเห การเลี้ยวเบน และการรวมคลื่น

ฟิสิกส์ · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.5/3

Sets moved here from: science_wave_e13.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e13 import (
    BEHAVIOURS,
    DIFFRACT,
    REFLECT,
    REFRACT,
    SUBJECT,
    SUPERPOSE,
    UPPER_FIVE,
    _labelled,
    _numeric,
)

PROVENANCE = Provenance("original")


TOPIC_WAVES = "การสะท้อน การหักเห การเลี้ยวเบน และการรวมคลื่น"


BEHAVIOUR_MEANING = {
    REFLECT: "คลื่นกระทบสิ่งกีดขวางแล้วเคลื่อนที่กลับในตัวกลางเดิม",
    REFRACT: "คลื่นเคลื่อนที่ผ่านรอยต่อของตัวกลางที่ต่างกัน แล้วอัตราเร็วเปลี่ยน ทำให้ทิศทางเปลี่ยน",
    DIFFRACT: "คลื่นเคลื่อนที่อ้อมสิ่งกีดขวางหรือผ่านช่องแคบแล้วแผ่ออกไปด้านหลัง",
    SUPERPOSE: "คลื่นสองขบวนเคลื่อนที่มาพบกัน การกระจัดของตัวกลางเท่ากับผลรวมของการกระจัดของคลื่นทั้งสอง",
}


WAVE_EXAMPLES = (
    ("คลื่นน้ำกระทบผนังถาดคลื่นแล้วเคลื่อนที่ย้อนกลับ", REFLECT),
    ("คลื่นทะเลกระทบกำแพงกันคลื่นแล้วย้อนกลับออกไป", REFLECT),
    ("แสงกระทบกระจกเงาแล้วเปลี่ยนทิศกลับ", REFLECT),
    ("สัญญาณเรดาร์กระทบเครื่องบินแล้วกลับมาที่จานรับ", REFLECT),
    ("คลื่นน้ำเคลื่อนที่จากบริเวณน้ำลึกเข้าสู่น้ำตื้นแล้วหน้าคลื่นเปลี่ยนทิศ", REFRACT),
    ("หลอดดูดในแก้วน้ำดูเหมือนหักงอที่ผิวน้ำ", REFRACT),
    ("แสงผ่านแท่งแก้วปริซึมแล้วเบนออกจากแนวเดิม", REFRACT),
    ("สระว่ายน้ำดูตื้นกว่าความลึกจริงเมื่อมองจากขอบสระ", REFRACT),
    ("คลื่นน้ำผ่านช่องแคบระหว่างแผ่นกั้นแล้วแผ่ออกเป็นวงโค้งด้านหลัง", DIFFRACT),
    ("คลื่นทะเลอ้อมปลายเขื่อนกันคลื่นเข้าไปในอ่าวที่ถูกบัง", DIFFRACT),
    ("คลื่นวิทยุความยาวคลื่นยาวอ้อมภูเขาไปถึงเครื่องรับด้านหลังได้", DIFFRACT),
    ("แสงผ่านช่องแคบมาก ๆ แล้วแผ่กว้างออกบนฉาก", DIFFRACT),
    ("คลื่นน้ำจากแหล่งกำเนิดสองแหล่งพบกันเกิดแนวที่น้ำกระเพื่อมมากสลับกับแนวที่น้ำนิ่ง", SUPERPOSE),
    ("ส่งคลื่นดลในเส้นเชือกจากสองปลายมาพบกัน ตรงจุดพบกันยอดคลื่นสูงขึ้นชั่วขณะ", SUPERPOSE),
    ("หูฟังตัดเสียงรบกวนสร้างคลื่นเสียงที่หักล้างกับเสียงรบกวน", SUPERPOSE),
    ("ฟองสบู่มีแถบสีต่าง ๆ เพราะแสงที่สะท้อนจากผิวหน้าและผิวหลังของฟิล์มมารวมกัน", SUPERPOSE),
)


WAVE_TRUE = (
    ("ในการสะท้อน มุมตกกระทบเท่ากับมุมสะท้อน", REFLECT),
    ("ในการสะท้อน อัตราเร็ว ความถี่ และความยาวคลื่นของคลื่นไม่เปลี่ยน", REFLECT),
    ("ในการหักเห ความถี่ของคลื่นไม่เปลี่ยน แต่อัตราเร็วและความยาวคลื่นเปลี่ยน", REFRACT),
    ("คลื่นน้ำเคลื่อนที่ช้าลงเมื่อเข้าสู่บริเวณน้ำตื้น", REFRACT),
    ("การเลี้ยวเบนเห็นได้ชัดเมื่อช่องกว้างใกล้เคียงหรือน้อยกว่าความยาวคลื่น", DIFFRACT),
    ("คลื่นที่เลี้ยวเบนยังมีความถี่และความยาวคลื่นเท่าเดิม", DIFFRACT),
    ("สันคลื่นพบสันคลื่น การกระจัดรวมมากขึ้น เรียกว่าการแทรกสอดแบบเสริม", SUPERPOSE),
    ("สันคลื่นพบท้องคลื่นที่ขนาดเท่ากัน การกระจัดรวมเป็นศูนย์ เรียกว่าการแทรกสอดแบบหักล้าง", SUPERPOSE),
)


WAVE_FALSE = (
    "ในการสะท้อน มุมสะท้อนมีค่าเป็นสองเท่าของมุมตกกระทบ",
    "ในการหักเห ความถี่ของคลื่นเปลี่ยนไปตามตัวกลางใหม่",
    "คลื่นน้ำเคลื่อนที่เร็วขึ้นเมื่อเข้าสู่บริเวณน้ำตื้น",
    "การเลี้ยวเบนเห็นได้ชัดเมื่อช่องกว้างกว่าความยาวคลื่นมาก ๆ",
    "คลื่นสองขบวนที่พบกันจะชนกันแล้วหยุดเคลื่อนที่",
    "หลังจากคลื่นสองขบวนเคลื่อนที่ผ่านกันไปแล้ว รูปร่างของคลื่นเปลี่ยนไปถาวร",
    "การเลี้ยวเบนทำให้ความยาวคลื่นสั้นลง",
)


@question_type(
    "phys.wave_behaviour_foundation",
    display_name={"th": "ความหมายของการสะท้อน การหักเห การเลี้ยวเบน และการรวมคลื่น"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_WAVES,
)
class WaveBehaviourFoundation(QuestionType):
    """Name the behaviour from its definition, or the definition from its name."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        behaviour = rng.choice(BEHAVIOURS)
        hint = "สะท้อนคือกลับตัวกลางเดิม หักเหคือผ่านตัวกลางใหม่ เลี้ยวเบนคืออ้อมสิ่งกีดขวาง รวมคลื่นคือคลื่นซ้อนกัน"
        shape = rng.random()
        if shape < 0.5:
            mine = [e for e, b in WAVE_EXAMPLES if b == behaviour]
            others = [e for e, b in WAVE_EXAMPLES if b != behaviour]
            return _labelled(
                stem=f"ข้อใดเป็นตัวอย่างของ{behaviour}ของคลื่น",
                correct=rng.choice(mine), wrongs=tuple(others),
                topic=TOPIC_WAVES, hint=hint)
        if shape < 0.75:
            return _labelled(
                stem=f"\"{BEHAVIOUR_MEANING[behaviour]}\" คือพฤติกรรมใดของคลื่น",
                correct=behaviour, wrongs=tuple(b for b in BEHAVIOURS if b != behaviour),
                topic=TOPIC_WAVES, hint=hint)
        return _labelled(
            stem=f"{behaviour}ของคลื่นหมายถึงข้อใด",
            correct=BEHAVIOUR_MEANING[behaviour],
            wrongs=tuple(BEHAVIOUR_MEANING[b] for b in BEHAVIOURS if b != behaviour),
            topic=TOPIC_WAVES, hint=hint)


@question_type(
    "phys.wave_behaviour_fluency",
    display_name={"th": "อธิบายการสะท้อน การหักเห การเลี้ยวเบน และการรวมคลื่นจากสถานการณ์"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_WAVES,
)
class WaveBehaviourFluency(QuestionType):
    """The indicator across all four behaviours: in real scenes and as true statements."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.55:
            example, behaviour = rng.choice(WAVE_EXAMPLES)
            return _labelled(
                stem=f"\"{example}\" เป็นผลของพฤติกรรมใดของคลื่น",
                correct=behaviour, wrongs=tuple(b for b in BEHAVIOURS if b != behaviour),
                topic=TOPIC_WAVES,
                hint="ดูว่าคลื่นกลับตัวกลางเดิม เข้าตัวกลางใหม่ อ้อมสิ่งกีดขวาง หรือคลื่นสองขบวนมาซ้อนกัน")
        statement, _ = rng.choice(WAVE_TRUE)
        return _labelled(
            stem="ข้อใดกล่าวถึงพฤติกรรมของคลื่นได้ถูกต้อง",
            correct=statement, wrongs=tuple(WAVE_FALSE),
            topic=TOPIC_WAVES,
            hint="ความถี่ของคลื่นขึ้นกับแหล่งกำเนิดจึงไม่เปลี่ยน สิ่งที่เปลี่ยนเมื่อเข้าตัวกลางใหม่คืออัตราเร็วและความยาวคลื่น")


@question_type(
    "phys.wave_behaviour_application",
    display_name={"th": "คำนวณมุมสะท้อน ความยาวคลื่นหลังหักเห และการรวมคลื่น"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_WAVES,
)
class WaveBehaviourApplication(QuestionType):
    """Each behaviour with numbers: the reflected angle, the new wavelength,
    the superposed amplitude, and the gap that diffracts most."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(4)
        if shape == 0:
            angle = rng.choice(range(10, 81, 5))
            from_surface = rng.random() < 0.5
            given = 90 - angle if from_surface else angle
            where = "ทำมุมกับผิวสะท้อน" if from_surface else "ทำมุมกับเส้นแนวฉาก"
            return _numeric(
                stem=(f"คลื่นตกกระทบผิวสะท้อนเรียบโดยแนวรังสีตกกระทบ{where} {given} องศา "
                      "มุมสะท้อน (วัดจากเส้นแนวฉาก) เท่ากับกี่องศา"),
                answer=angle, wrongs=[90 - angle, 2 * angle, 180 - angle],
                unit="องศา", topic=TOPIC_WAVES,
                hint="มุมตกกระทบเท่ากับมุมสะท้อน โดยวัดจากเส้นแนวฉาก ถ้าโจทย์ให้มุมกับผิว ให้ลบออกจาก 90 องศาก่อน")
        if shape == 1:
            f = rng.choice((2, 4, 5, 10))
            v1 = rng.choice((20, 30, 40, 50, 60))
            v2 = rng.choice([v for v in (10, 15, 20, 25, 30) if v < v1])
            return _numeric(
                stem=(f"คลื่นน้ำความถี่ {f} เฮิรตซ์ เคลื่อนที่ในน้ำลึกด้วยอัตราเร็ว {v1} เซนติเมตรต่อวินาที "
                      f"เมื่อเข้าสู่น้ำตื้นมีอัตราเร็ว {v2} เซนติเมตรต่อวินาที ความยาวคลื่นในน้ำตื้นเท่าใด"),
                answer=Fraction(v2, f), wrongs=[Fraction(v1, f), Fraction(v2 * f), Fraction(f, 1) * v1 / v2],
                unit="เซนติเมตร", topic=TOPIC_WAVES,
                hint="ความถี่ไม่เปลี่ยนเมื่อหักเห ใช้ v = fλ กับอัตราเร็วในตัวกลางใหม่")
        if shape == 2:
            a, b = rng.randint(1, 9), rng.randint(1, 9)
            same = rng.random() < 0.5
            kind = "สันคลื่นกับสันคลื่น" if same else "สันคลื่นกับท้องคลื่น"
            answer = a + b if same else abs(a - b)
            if answer == 0:
                a, answer = a + 1, 1
            return _numeric(
                stem=(f"คลื่นดลในเส้นเชือกสองขบวน แอมพลิจูด {a} เซนติเมตร และ {b} เซนติเมตร "
                      f"เคลื่อนที่มาพบกันแบบ{kind} ขณะซ้อนกันพอดี การกระจัดรวมที่จุดนั้นมีขนาดเท่าใด"),
                answer=answer, wrongs=[abs(a - b) if same else a + b, max(a, b), a * b],
                unit="เซนติเมตร", topic=TOPIC_WAVES,
                hint="สันคลื่นพบสันคลื่นให้บวกกัน สันคลื่นพบท้องคลื่นให้หักล้างกัน (ลบกัน)")
        # A gap narrower than the wavelength spreads the wave even more, so the
        # clearest diffraction is always at the narrowest gap offered.
        wavelength = rng.choice((2, 3, 4, 5))
        gaps = rng.sample((1, 2, 3, 4, 5, 8, 10, 15, 20, 30, 40), 4)
        best = min(gaps)
        return _labelled(
            stem=(f"คลื่นน้ำมีความยาวคลื่น {wavelength} เซนติเมตร เคลื่อนที่ผ่านช่องเปิด ช่องกว้างเท่าใด"
                  "ทำให้เห็นการเลี้ยวเบนชัดเจนที่สุด"),
            correct=f"{best} เซนติเมตร",
            wrongs=tuple(f"{g} เซนติเมตร" for g in gaps if g != best),
            topic=TOPIC_WAVES,
            hint="ช่องยิ่งแคบเมื่อเทียบกับความยาวคลื่น คลื่นยิ่งแผ่ออกด้านหลังมาก การเลี้ยวเบนยิ่งเห็นชัด")
