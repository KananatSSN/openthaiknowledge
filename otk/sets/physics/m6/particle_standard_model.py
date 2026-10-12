"""ฟิสิกส์อนุภาคและแบบจำลองมาตรฐาน

ฟิสิกส์ · ม.6 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 4 ม.6/18

Sets moved here from: science_wave_f18.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f18 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_PARTICLE = "ฟิสิกส์อนุภาคและแบบจำลองมาตรฐาน"


QUARKS = {"u": Fraction(2, 3), "d": Fraction(-1, 3), "s": Fraction(-1, 3), "c": Fraction(2, 3)}


NAMES = {"u": "อัพ", "d": "ดาวน์", "s": "สเตรนจ์", "c": "ชาร์ม"}


PARTICLE_FACTS = (
    ("ตามแบบจำลองมาตรฐาน โปรตอนประกอบด้วยควาร์กใด", "อัพ 2 ตัว และดาวน์ 1 ตัว (uud)",
     ("อัพ 1 ตัว และดาวน์ 2 ตัว (udd)", "อิเล็กตรอน 3 ตัว", "อัพ 3 ตัว (uuu)")),
    ("ตามแบบจำลองมาตรฐาน นิวตรอนประกอบด้วยควาร์กใด", "อัพ 1 ตัว และดาวน์ 2 ตัว (udd)",
     ("อัพ 2 ตัว และดาวน์ 1 ตัว (uud)", "ดาวน์ 3 ตัว (ddd)", "โปรตอนกับอิเล็กตรอน")),
    ("อนุภาคใดจัดเป็นเลปตอน", "อิเล็กตรอนและนิวทริโน", ("โปรตอนและนิวตรอน", "ควาร์กอัพ", "กลูออน")),
    ("อนุภาคสื่อแรงของแรงแม่เหล็กไฟฟ้าคืออะไร", "โฟตอน", ("กลูออน", "โบซอน W และ Z", "ฮิกส์โบซอน")),
    ("อนุภาคสื่อแรงของแรงเข้ม (แรงนิวเคลียร์ระหว่างควาร์ก) คืออะไร", "กลูออน", ("โฟตอน", "โบซอน W และ Z", "นิวทริโน")),
    ("อนุภาคสื่อแรงของแรงอ่อน ซึ่งเกี่ยวกับการสลายให้บีตา คืออะไร", "โบซอน W และ Z", ("โฟตอน", "กลูออน", "อิเล็กตรอน")),
    ("ปฏิยานุภาคของอิเล็กตรอนคืออะไร", "โพซิตรอน มีมวลเท่าอิเล็กตรอนแต่ประจุ +1", ("โปรตอน", "นิวตรอน", "นิวทริโน")),
    ("ฮิกส์โบซอนเกี่ยวข้องกับสมบัติใดของอนุภาค", "ทำให้อนุภาคมูลฐานบางชนิดมีมวล", ("ทำให้อนุภาคมีประจุ", "ทำให้อนุภาคมีสี", "ทำให้อนุภาคหมุน")),
)


GROUPS = ("ควาร์ก", "เลปตอน", "อนุภาคสื่อแรง (เกจโบซอน)", "แฮดรอน (ประกอบด้วยควาร์ก)")


PARTICLES = (
    ("อิเล็กตรอน", "เลปตอน", Fraction(-1)), ("นิวทริโน", "เลปตอน", Fraction(0)), ("มิวออน", "เลปตอน", Fraction(-1)),
    ("โพซิตรอน", "เลปตอน", Fraction(1)), ("ควาร์กอัพ", "ควาร์ก", Fraction(2, 3)), ("ควาร์กดาวน์", "ควาร์ก", Fraction(-1, 3)),
    ("ควาร์กสเตรนจ์", "ควาร์ก", Fraction(-1, 3)), ("ควาร์กชาร์ม", "ควาร์ก", Fraction(2, 3)),
    ("โฟตอน", "อนุภาคสื่อแรง (เกจโบซอน)", Fraction(0)), ("กลูออน", "อนุภาคสื่อแรง (เกจโบซอน)", Fraction(0)),
    ("โบซอน W⁺", "อนุภาคสื่อแรง (เกจโบซอน)", Fraction(1)), ("โบซอน Z", "อนุภาคสื่อแรง (เกจโบซอน)", Fraction(0)),
    ("โปรตอน", "แฮดรอน (ประกอบด้วยควาร์ก)", Fraction(1)), ("นิวตรอน", "แฮดรอน (ประกอบด้วยควาร์ก)", Fraction(0)),
    ("ไพออนบวก", "แฮดรอน (ประกอบด้วยควาร์ก)", Fraction(1)),
)


CHARGES = tuple(Fraction(x) for x in (-1, 0, 1, 2)) + (Fraction(2, 3), Fraction(-1, 3), Fraction(1, 3), Fraction(-2, 3))


APPLICATIONS = (
    ("เครื่องเพท (PET) ในโรงพยาบาล", "ใช้โพซิตรอนที่ประลัยกับอิเล็กตรอนแล้วให้รังสีแกมมาสร้างภาพอวัยวะ"),
    ("การรักษามะเร็งด้วยลำโปรตอน", "ใช้เครื่องเร่งอนุภาคเร่งโปรตอนให้ปล่อยพลังงานที่ก้อนมะเร็งโดยตรง"),
    ("เวิลด์ไวด์เว็บ (WWW)", "พัฒนาขึ้นที่เซิร์น เพื่อให้นักฟิสิกส์อนุภาคแลกเปลี่ยนข้อมูลกัน"),
    ("เครื่องเร่งอนุภาค LHC", "เร่งโปรตอนให้ชนกันด้วยพลังงานสูงเพื่อค้นหาอนุภาคใหม่ เช่น ฮิกส์โบซอน"),
    ("แสงซินโครตรอน", "แสงจากอิเล็กตรอนที่เคลื่อนที่เป็นวงโค้งด้วยความเร็วสูง ใช้ศึกษาโครงสร้างของวัสดุ"),
)


def _charge(label: str) -> str:
    if label == 0:
        return "0"
    sign = "+" if label > 0 else "−"
    return f"{sign}{abs(label)}" if label.denominator == 1 else f"{sign}{abs(label.numerator)}/{label.denominator}"


@question_type(
    "phys.particle_standard_model_foundation",
    display_name={"th": "อนุภาคมูลฐานและแบบจำลองมาตรฐาน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_PARTICLE,
)
class ParticleStandardModelFoundation(QuestionType):
    """Quarks, leptons and the force carriers."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = "แบบจำลองมาตรฐาน: ควาร์กและเลปตอนเป็นอนุภาคสสาร แรงแต่ละชนิดมีอนุภาคสื่อแรง และฮิกส์ให้มวล"
        shape = rng.randrange(3)
        if shape == 0:
            stem, correct, wrongs = rng.choice(PARTICLE_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_PARTICLE, hint=hint)
        name, group, charge = rng.choice(PARTICLES)
        if shape == 1:
            return _labelled(stem=f"{name}จัดเป็นอนุภาคกลุ่มใด", correct=group,
                             wrongs=tuple(g for g in GROUPS if g != group), topic=TOPIC_PARTICLE, hint=hint)
        choices = [c for c in CHARGES if c != charge]
        return _labelled(stem=f"{name}มีประจุไฟฟ้าเท่าใด (หน่วยประจุมูลฐาน)", correct=_charge(charge),
                         wrongs=tuple(_charge(c) for c in rng.sample(choices, 3)), topic=TOPIC_PARTICLE, hint=hint)


@question_type(
    "phys.particle_standard_model_fluency",
    display_name={"th": "ประจุของแฮดรอนจากควาร์กที่เป็นส่วนประกอบ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_PARTICLE,
)
class ParticleStandardModelFluency(QuestionType):
    """Add the quark charges; an antiquark carries the opposite charge."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            quarks = [rng.choice("udsc") for _ in range(3)]
            total = sum(QUARKS[q] for q in quarks)
            listed = " ".join(f"{NAMES[q]} ({q})" for q in quarks)
            stem = f"แบริออนหนึ่งประกอบด้วยควาร์ก {listed} มีประจุไฟฟ้าเท่าใด (หน่วยประจุมูลฐาน)"
        else:
            q, anti = rng.choice("udsc"), rng.choice("udsc")
            total = QUARKS[q] - QUARKS[anti]
            stem = (f"มีซอนหนึ่งประกอบด้วยควาร์ก{NAMES[q]} ({q}) กับปฏิควาร์ก{NAMES[anti]} (แอนติ-{anti}) "
                    "มีประจุไฟฟ้าเท่าใด (หน่วยประจุมูลฐาน)")
        options = [Fraction(x) for x in (-2, -1, 0, 1, 2)] + [Fraction(1, 3), Fraction(-1, 3), Fraction(2, 3)]
        wrongs = tuple(_charge(x) for x in rng.sample([o for o in options if o != total], 3))
        return _labelled(stem=stem, correct=_charge(total), wrongs=wrongs, topic=TOPIC_PARTICLE,
                         hint="ควาร์ก u และ c มีประจุ +2/3, d และ s มีประจุ −1/3 ปฏิควาร์กมีประจุตรงข้าม แล้วนำมารวมกัน")


@question_type(
    "phys.particle_standard_model_application",
    display_name={"th": "การใช้ประโยชน์จากการค้นคว้าวิจัยด้านฟิสิกส์อนุภาค"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_PARTICLE,
)
class ParticleStandardModelApplication(QuestionType):
    """From accelerators to hospitals and the web."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        chosen = rng.sample(APPLICATIONS, 4)
        thing, how = chosen[0]
        hint = "งานวิจัยฟิสิกส์อนุภาคต้องใช้เครื่องเร่งอนุภาค ตัวตรวจวัด และเครือข่ายข้อมูล ซึ่งนำไปใช้ต่อในการแพทย์และเทคโนโลยี"
        if rng.random() < 0.5:
            return _labelled(stem=f"{thing}เกี่ยวข้องกับการค้นคว้าด้านฟิสิกส์อนุภาคอย่างไร", correct=how,
                             wrongs=tuple(h for _, h in chosen[1:]), topic=TOPIC_PARTICLE, hint=hint)
        return _labelled(stem=f"ข้อใด{how}", correct=thing, wrongs=tuple(t for t, _ in chosen[1:]),
                         topic=TOPIC_PARTICLE, hint=hint)
