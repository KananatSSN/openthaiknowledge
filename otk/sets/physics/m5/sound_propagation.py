"""การเกิดและการเคลื่อนที่ของเสียง และสมบัติของคลื่นเสียง

ฟิสิกส์ · ม.5 · สสวท. เพิ่มเติม
Indicators: ฟิสิกส์เพิ่มเติม 2 ม.5/5

Sets moved here from: science_wave_f8.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f8 import SUBJECT, UPPER_FIVE, _exact, speed_at

PROVENANCE = Provenance("original")


TOPIC_SOUND = "การเกิดและการเคลื่อนที่ของเสียง และสมบัติของคลื่นเสียง"


TEMPERATURES = (0, 5, 10, 15, 20, 25, 30, 35, 40)


SOUND_FACTS = (
    ("คลื่นเสียงในอากาศเป็นคลื่นชนิดใด", "คลื่นกลตามยาว",
     ("คลื่นกลตามขวาง", "คลื่นแม่เหล็กไฟฟ้าตามขวาง", "คลื่นแม่เหล็กไฟฟ้าตามยาว")),
    ("ตำแหน่งที่การกระจัดของอนุภาคอากาศเป็นศูนย์ ความดันของอากาศเป็นอย่างไร", "ความดันเปลี่ยนไปจากปกติมากที่สุด",
     ("ความดันเท่ากับความดันปกติเสมอ", "ความดันเป็นศูนย์", "ความดันเปลี่ยนน้อยที่สุด")),
    ("อัตราเร็วของเสียงในอากาศเปลี่ยนไปอย่างไรเมื่ออุณหภูมิสูงขึ้น", "เพิ่มขึ้น",
     ("ลดลง", "ไม่เปลี่ยน", "เพิ่มขึ้นแล้วลดลง")),
    ("เสียงเคลื่อนที่ในตัวกลางใดเร็วที่สุด", "ของแข็ง เช่น เหล็ก",
     ("อากาศ", "น้ำ", "สุญญากาศ")),
    ("การได้ยินเสียงคนพูดจากอีกฟากหนึ่งของกำแพงที่มีประตูเปิดอยู่ เป็นสมบัติใดของเสียง", "การเลี้ยวเบน",
     ("การสะท้อน", "การหักเห", "การแทรกสอด")),
    ("ตอนกลางคืนได้ยินเสียงจากที่ไกลชัดกว่าตอนกลางวัน เป็นผลของสมบัติใดของเสียง", "การหักเห เพราะอากาศใกล้พื้นเย็นกว่าอากาศด้านบน",
     ("การสะท้อนจากเมฆ", "การแทรกสอดของเสียงจากหลายแหล่ง", "การเลี้ยวเบนผ่านต้นไม้")),
    ("เสียงก้องที่ได้ยินหลังตะโกนใส่หน้าผาเป็นสมบัติใดของเสียง", "การสะท้อน",
     ("การหักเห", "การเลี้ยวเบน", "การแทรกสอด")),
    ("เดินผ่านหน้าลำโพงสองตัวที่ต่อกับแหล่งเสียงเดียวกัน แล้วได้ยินเสียงดังค่อยสลับกัน เป็นสมบัติใดของเสียง", "การแทรกสอด",
     ("การสะท้อน", "การหักเห", "การสั่นพ้อง")),
)


@question_type(
    "phys.sound_propagation_foundation",
    display_name={"th": "ธรรมชาติของคลื่นเสียง อัตราเร็วเสียง และสมบัติของเสียง"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SOUND,
)
class SoundPropagationFoundation(QuestionType):
    """What sound is, which property is at work, and v = 331 + 0.6T."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.55:
            stem, correct, wrongs = rng.choice(SOUND_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_SOUND,
                             hint="เสียงเป็นคลื่นกลตามยาว มีสมบัติของคลื่นครบ: สะท้อน หักเห แทรกสอด เลี้ยวเบน")
        t = rng.randint(0, 40)
        if rng.random() < 0.4:
            t = rng.choice(TEMPERATURES)
            v = speed_at(t)
            time = Fraction(rng.randint(1, 20), 2)
            d = v * time
            return numeric(
                stem=f"เสียงเดินทางในอากาศอุณหภูมิ {t} °C เป็นระยะ {show(d)} m ใช้เวลาเท่าใด (v = 331 + 0.6T)",
                answer=time, wrongs=[time * 2, time / 2, time + 1], unit="s", topic=TOPIC_SOUND,
                hint="หาอัตราเร็วจากอุณหภูมิก่อน แล้วเวลา = ระยะทาง ÷ อัตราเร็ว")
        return numeric(
            stem=f"อากาศมีอุณหภูมิ {t} °C อัตราเร็วของเสียงในอากาศเท่าใด (v = 331 + 0.6T)",
            answer=speed_at(t), wrongs=[331 + t, 331 * Fraction(3, 5) + t, 331 - Fraction(3, 5) * t if t else 340],
            unit="m/s", topic=TOPIC_SOUND, hint="v = 331 + 0.6T เมื่อ T เป็นองศาเซลเซียส")


@question_type(
    "phys.sound_propagation_fluency",
    display_name={"th": "คำนวณอัตราเร็ว ระยะเสียงสะท้อน และความยาวคลื่นเสียงตามอุณหภูมิ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SOUND,
)
class SoundPropagationFluency(QuestionType):
    """Temperature from speed, an echo's distance, and a wavelength in warm air."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        t = rng.choice(TEMPERATURES)
        v = speed_at(t)
        shape = rng.randrange(3)
        if shape == 0:
            t = rng.choice(TEMPERATURES[1:])
            v = speed_at(t)
            return numeric(
                stem=f"วัดอัตราเร็วของเสียงในอากาศได้ {show(v)} m/s อากาศมีอุณหภูมิเท่าใด (v = 331 + 0.6T)",
                answer=t, wrongs=[v - 331, (v - 331) * Fraction(3, 5), t + 10], unit="°C",
                topic=TOPIC_SOUND, hint="T = (v − 331) ÷ 0.6")
        if shape == 1:
            echo = rng.choice([x for x in (Fraction(1, 5), Fraction(2, 5), Fraction(1, 2), 1, Fraction(3, 2), 2, 3, 4)
                               if _exact(v * x / 2)])
            return numeric(
                stem=(f"ตะโกนใส่หน้าผาในวันที่อากาศมีอุณหภูมิ {t} °C ได้ยินเสียงสะท้อนกลับหลังจากตะโกน {show(echo)} s "
                      "หน้าผาอยู่ห่างเท่าใด (v = 331 + 0.6T)"),
                answer=v * echo / 2, wrongs=[v * echo, Fraction(v) / echo, 340 * Fraction(echo) / 2],
                unit="m", topic=TOPIC_SOUND, hint="เสียงเดินทางไปและกลับ: ระยะ = v × t ÷ 2")
        f = rng.choice([x for x in (100, 200, 250, 400, 500, 1000, 2000) if _exact(v / x)])
        return numeric(
            stem=f"ส้อมเสียงความถี่ {f} Hz สั่นในอากาศที่มีอุณหภูมิ {t} °C ความยาวคลื่นเสียงเท่าใด (v = 331 + 0.6T)",
            answer=v / f, wrongs=[Fraction(331, f), v * f / 1000, Fraction(340, f)], unit="m", topic=TOPIC_SOUND,
            hint="หาอัตราเร็วจากอุณหภูมิก่อน แล้ว λ = v ÷ f")


@question_type(
    "phys.sound_propagation_application",
    display_name={"th": "การแทรกสอดของเสียงจากลำโพงสองตัว"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_SOUND,
)
class SoundPropagationApplication(QuestionType):
    """Loud and quiet spots from the path difference in wavelengths."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        t = rng.choice(TEMPERATURES)
        v = speed_at(t)
        if rng.random() < 0.5:
            wl = rng.choice([x for x in (Fraction(1, 4), Fraction(1, 2), 1, 2) if _exact(v / x)])
            f = v / wl
            half = rng.choice([h for h in range(1, 7) if _exact(wl * h / 2)])
            loud = half % 2 == 0
            near = rng.randint(2, 10)
            return _labelled(
                stem=(f"ลำโพงสองตัวต่อกับแหล่งกำเนิดเดียวกันให้เสียงความถี่ {show(f)} Hz ในอากาศอุณหภูมิ {t} °C "
                      f"จุด P อยู่ห่างลำโพงตัวหนึ่ง {near} m และอีกตัว {show(near + wl * half / 2)} m "
                      "ที่จุด P ได้ยินเสียงอย่างไร (v = 331 + 0.6T)"),
                correct="ดัง เพราะคลื่นเสริมกัน" if loud else "ค่อย เพราะคลื่นหักล้างกัน",
                wrongs=("ค่อย เพราะคลื่นหักล้างกัน" if loud else "ดัง เพราะคลื่นเสริมกัน",
                        "ดังค่อยสลับกันเป็นจังหวะ เพราะเกิดบีต", "ไม่ได้ยินเสียงเลย เพราะเสียงเลี้ยวเบนออกไป"),
                topic=TOPIC_SOUND,
                hint="หา λ = v/f แล้วดูผลต่างระยะทาง: เป็นจำนวนเต็มเท่าของ λ ได้ยินดัง เป็นจำนวนคี่เท่าของ λ/2 ได้ยินค่อย")
        gap = rng.choice([x for x in (Fraction(1, 4), Fraction(1, 2), Fraction(3, 4), 1, Fraction(5, 4), 2)
                          if _exact(v / (2 * x))])
        return numeric(
            stem=(f"ลำโพงสองตัวต่อกับแหล่งกำเนิดเดียวกันในอากาศอุณหภูมิ {t} °C จุด P มีผลต่างระยะทางจากลำโพงทั้งสอง "
                  f"{show(gap)} m ความถี่ต่ำสุดที่ทำให้ได้ยินเสียงค่อยที่สุดที่ P เท่าใด (v = 331 + 0.6T)"),
            answer=v / (2 * gap), wrongs=[v / gap, v / (4 * gap), v * gap], unit="Hz", topic=TOPIC_SOUND,
            hint="เสียงค่อยครั้งแรกเมื่อผลต่างระยะทาง = λ/2 ดังนั้น λ = 2 × ผลต่างระยะทาง และ f = v/λ")
