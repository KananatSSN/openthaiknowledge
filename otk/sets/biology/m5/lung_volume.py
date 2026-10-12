"""การทำงานของปอดและปริมาตรอากาศ

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.5/7

Sets moved here from: science_wave_f61.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f61 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_LUNG = "การทำงานของปอดและปริมาตรอากาศ"


BREATH = (
    ("หายใจเข้า", "กะบังลมหดตัวเลื่อนต่ำลง กล้ามเนื้อยึดซี่โครงด้านนอกหดตัว ปริมาตรช่องอกเพิ่ม ความดันในปอดลดลง"),
    ("หายใจออก", "กะบังลมคลายตัวโค้งขึ้น กล้ามเนื้อยึดซี่โครงด้านนอกคลายตัว ปริมาตรช่องอกลดลง ความดันในปอดเพิ่มขึ้น"),
)


VOLUMES = (
    ("ปริมาตรอากาศหายใจเข้าออกปกติ (tidal volume)", "อากาศที่หายใจเข้าหรือออกแต่ละครั้งในภาวะปกติ"),
    ("ปริมาตรสำรองหายใจเข้า", "อากาศที่หายใจเข้าเพิ่มได้อีกหลังหายใจเข้าปกติ"),
    ("ปริมาตรสำรองหายใจออก", "อากาศที่หายใจออกเพิ่มได้อีกหลังหายใจออกปกติ"),
    ("ปริมาตรอากาศค้างในปอด", "อากาศที่ยังเหลืออยู่ในปอดหลังหายใจออกเต็มที่"),
    ("ความจุปอด (vital capacity)", "อากาศที่หายใจออกได้มากที่สุดหลังหายใจเข้าเต็มที่"),
)


LUNG_HINT = ("หายใจเข้า: กะบังลมและกล้ามเนื้อยึดซี่โครงด้านนอกหดตัว ช่องอกขยาย ความดันลด ความจุปอด = หายใจปกติ + สำรองเข้า + สำรองออก "
             "ความจุทั้งหมดของปอด = ความจุปอด + อากาศค้างในปอด")


@question_type(
    "biology.lung_volume_foundation",
    display_name={"th": "กลไกการหายใจเข้าและหายใจออก"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_LUNG,
)
class LungVolumeFoundation(QuestionType):
    """Diaphragm and ribs, volume and pressure."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        phase, how = rng.choice(BREATH)
        other_phase, other_how = next(b for b in BREATH if b[0] != phase)
        if rng.random() < 0.5:
            pool = ("ปอดหดตัวเองเพื่อดูดอากาศเข้า", "กะบังลมและซี่โครงไม่เคลื่อนไหว ปอดทำงานเอง",
                    "กะบังลมหดตัวโค้งขึ้น ปริมาตรช่องอกลดลง ความดันในปอดลดลง", "หัวใจบีบตัวดันอากาศเข้าและออกจากปอด")
            return _labelled(stem=f"ขณะ{phase} เกิดการเปลี่ยนแปลงใด", correct=how,
                             wrongs=(other_how, *rng.sample(pool, 2)),
                             topic=TOPIC_LUNG, hint=LUNG_HINT)
        facts = (("ในแบบจำลองขวดกระดิ่ง เมื่อดึงแผ่นยางที่ก้นขวดลง ลูกโป่งจะเป็นอย่างไร", "พองออก เหมือนปอดขณะหายใจเข้า",
                  ("แฟบลง เหมือนปอดขณะหายใจออก", "ไม่เปลี่ยนแปลง", "แตกทันที", "หดเล็กลงเท่าเดิม")),
                 ("แผ่นยางที่ก้นขวดในแบบจำลองขวดกระดิ่งเปรียบได้กับส่วนใด", "กะบังลม",
                  ("ปอด", "ท่อลม", "ซี่โครง", "หัวใจ")),
                 ("เมื่อปล่อยแผ่นยางที่ก้นขวดกระดิ่งกลับขึ้นที่เดิม ลูกโป่งจะเป็นอย่างไร", "แฟบลง เหมือนปอดขณะหายใจออก",
                  ("พองออก เหมือนปอดขณะหายใจเข้า", "ไม่เปลี่ยนแปลง", "แตกทันที", "พองใหญ่ขึ้นกว่าเดิม")),
                 ("อากาศเคลื่อนเข้าสู่ปอดได้เพราะเหตุใด", "ความดันอากาศในปอดต่ำกว่าความดันอากาศภายนอก",
                  ("ความดันในปอดสูงกว่าภายนอก", "ปอดดูดอากาศด้วยกล้ามเนื้อของปอดเอง", "หัวใจดันอากาศเข้าปอด", "อากาศมีน้ำหนักมาก")))
        stem, right, wrongs = rng.choice(facts)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_LUNG, hint=LUNG_HINT)


@question_type(
    "biology.lung_volume_fluency",
    display_name={"th": "ความหมายของปริมาตรอากาศในปอด"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_LUNG,
)
class LungVolumeFluency(QuestionType):
    """Name each spirometer volume, and back."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, meaning = rng.choice(VOLUMES)
        others = rng.sample([v for v in VOLUMES if v[0] != name], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"{name}หมายถึงข้อใด", correct=meaning, wrongs=tuple(v[1] for v in others), topic=TOPIC_LUNG, hint=LUNG_HINT)
        return _labelled(stem=f"\"{meaning}\" เรียกว่าอะไร", correct=name, wrongs=tuple(v[0] for v in others), topic=TOPIC_LUNG, hint=LUNG_HINT)


@question_type(
    "biology.lung_volume_application",
    display_name={"th": "คำนวณความจุปอดและปริมาตรอากาศที่หายใจต่อนาที"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_LUNG,
)
class LungVolumeApplication(QuestionType):
    """Add the volumes; tidal volume × breaths per minute."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        tidal = rng.randrange(400, 651, 50)
        irv = rng.randrange(2000, 3301, 100)
        erv = rng.randrange(900, 1401, 100)
        rv = rng.randrange(1000, 1501, 100)
        vc = tidal + irv + erv
        intro = (f"ผลการวัดด้วยสไปโรมิเตอร์: หายใจเข้าออกปกติ {tidal} mL ปริมาตรสำรองหายใจเข้า {irv} mL "
                 f"ปริมาตรสำรองหายใจออก {erv} mL และอากาศค้างในปอด {rv} mL")
        kind = rng.randrange(4)
        if kind == 0:
            return numeric(stem=f"{intro} ความจุปอดเป็นกี่มิลลิลิตร", answer=vc, wrongs=[vc + rv, irv + erv, tidal + irv], unit="mL",
                           topic=TOPIC_LUNG, hint=LUNG_HINT)
        if kind == 1:
            return numeric(stem=f"{intro} ความจุทั้งหมดของปอดเป็นกี่มิลลิลิตร", answer=vc + rv, wrongs=[vc, vc + rv - tidal, irv + erv + rv],
                           unit="mL", topic=TOPIC_LUNG, hint=LUNG_HINT)
        if kind == 2:
            return numeric(stem=f"{intro} หลังหายใจเข้าเต็มที่แล้วเป่าลมออกให้มากที่สุด จะเป่าได้กี่มิลลิลิตร", answer=vc,
                           wrongs=[vc + rv, tidal + erv, irv], unit="mL", topic=TOPIC_LUNG, hint=LUNG_HINT)
        rate = rng.randint(12, 20)
        return numeric(stem=f"คนหนึ่งหายใจเข้าออกครั้งละ {tidal} mL นาทีละ {rate} ครั้ง ปริมาตรอากาศที่หายใจต่อนาทีเป็นกี่ลิตร",
                       answer=Fraction(tidal * rate, 1000), wrongs=[tidal * rate, Fraction(tidal, 1000), rate], unit="ลิตร",
                       topic=TOPIC_LUNG, hint="ปริมาตรต่อนาที = ปริมาตรต่อครั้ง × จำนวนครั้งต่อนาที แล้วแปลง mL เป็นลิตร (÷ 1,000)")
