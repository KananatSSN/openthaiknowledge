"""วิวัฒนาการของเอกภพหลังบิกแบง

ดาราศาสตร์ · ม.6 · สสวท. พื้นฐาน
Indicators: ว 3.1 ม.6/1

Sets moved here from: science_wave_c6, science_wave_f82.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled as _labelled_science_wave_c6
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c1 import SUBJECT
from otk.sets._support.science_wave_c6 import UNIVERSE_FACTS, UNIVERSE_SCENARIOS, UPPER_SIX

PROVENANCE = Provenance("original")


UNIVERSE_TOPIC = "วิวัฒนาการของเอกภพหลังบิกแบง"


class Epoch(NamedTuple):
    """One stage of the universe's evolution, as a timeline would list it."""
    when: str
    event: str
    temperature: str


# Ordered. Each ``event`` is a different threshold, so no two rows answer alike.
EPOCHS = (
    Epoch("ประมาณ 10⁻⁶ วินาทีหลังบิกแบง",
          "ควาร์กรวมตัวกันเป็นโปรตอนและนิวตรอนเมื่อเอกภพเย็นลงพอ",
          "สูงกว่า 10¹² เคลวิน"),
    Epoch("ประมาณ 3 นาทีหลังบิกแบง",
          "โปรตอนและนิวตรอนรวมกันเป็นนิวเคลียสของไฮโดรเจนและฮีเลียม",
          "ประมาณ 10⁹ เคลวิน"),
    Epoch("ประมาณ 380,000 ปีหลังบิกแบง",
          "นิวเคลียสจับอิเล็กตรอนเป็นอะตอม เอกภพจึงโปร่งใสให้แสงผ่าน",
          "ประมาณ 3,000 เคลวิน"),
    Epoch("ประมาณหลายร้อยล้านปีหลังบิกแบง",
          "แก๊สยุบรวมกันจนเกิดดาวฤกษ์และกาแล็กซีรุ่นแรกขึ้นในเอกภพ",
          "ต่ำกว่า 100 เคลวิน"),
    Epoch("ปัจจุบัน ประมาณ 13,800 ล้านปีหลังบิกแบง",
          "เอกภพยังขยายตัวต่อไป และมีกาแล็กซีกระจายอยู่ทั่วทั้งเอกภพ",
          "ประมาณ 2.7 เคลวิน"),
)


def _timeline() -> str:
    return " / ".join(f"{epoch.when}: {epoch.event} (อุณหภูมิ{epoch.temperature})"
                      for epoch in EPOCHS)


ENERGY = "พลังงาน"


MATTER = "สสาร"


SIZE = "ขนาด"


TEMPERATURE = "อุณหภูมิ"


# The four things ``ม.6/1`` names, each as one clause of a single answer.
SPANNING = (f"{SIZE}ขยายใหญ่ขึ้นและ{TEMPERATURE}ลดลงตลอด "
            f"{ENERGY}ส่วนหนึ่งเปลี่ยนเป็น{MATTER} "
            f"แล้วรวมตัวเป็นอะตอม ดาวฤกษ์ และกาแล็กซี")


SPANNING_WRONGS = (
    f"{SIZE}ขยายใหญ่ขึ้นตลอด {TEMPERATURE}สูงขึ้นตลอด "
    f"{ENERGY}คงที่ และ{MATTER}สลายกลับไปเป็น{ENERGY}ทั้งหมด",
    f"{SIZE}คงที่ {TEMPERATURE}คงที่ "
    f"{ENERGY}และ{MATTER}ในเอกภพจึงไม่เคยเปลี่ยนแปลงเลย",
    f"{SIZE}หดเล็กลงตลอด {TEMPERATURE}สูงขึ้นตลอด "
    f"และ{MATTER}ถูกบีบรวมกลับไปเป็น{ENERGY}จนไม่เหลือกาแล็กซี",
)


TOPIC_TIMELINE = "วิวัฒนาการของเอกภพหลังบิกแบง"


TIMELINE = (
    ("เอกภพขยายตัวอย่างรวดเร็วมากในช่วงสั้น ๆ (อินฟเลชัน)", "ภายในเสี้ยววินาทีแรก"),
    ("พลังงานเปลี่ยนเป็นอนุภาคและปฏิยานุภาคจำนวนมาก เช่น ควาร์ก อิเล็กตรอน", "ภายในเสี้ยววินาทีแรก หลังอินฟเลชัน"),
    ("ควาร์กรวมกันเป็นโปรตอนและนิวตรอน", "ประมาณหนึ่งในล้านวินาทีถึงหนึ่งวินาที"),
    ("โปรตอนและนิวตรอนรวมกันเป็นนิวเคลียสของฮีเลียม", "ประมาณ 3 นาทีแรก"),
    ("นิวเคลียสจับอิเล็กตรอนเป็นอะตอม เอกภพโปร่งแสง เกิดไมโครเวฟพื้นหลัง", "ประมาณ 380,000 ปี"),
    ("เกิดดาวฤกษ์และกาแล็กซีรุ่นแรก", "ประมาณหลายร้อยล้านปี"),
)


TIMELINE_FACTS = (
    ("เมื่อเอกภพขยายตัว อุณหภูมิของเอกภพเปลี่ยนแปลงอย่างไร", "ลดลงเรื่อย ๆ",
     ("สูงขึ้นเรื่อย ๆ", "คงที่ตลอด", "ลดลงแล้วกลับสูงขึ้นทุก 1 ล้านปี", "สูงขึ้นเฉพาะช่วง 3 นาทีแรก")),
    ("เอกภพเกิดขึ้นเมื่อประมาณกี่ปีมาแล้ว", "ประมาณ 13,800 ล้านปี",
     ("ประมาณ 4,600 ล้านปี", "ประมาณ 380,000 ปี", "ประมาณ 1,000 ล้านปี", "ประมาณ 100,000 ล้านปี")),
    ("ธาตุที่เกิดขึ้นมากที่สุดในช่วงแรกของเอกภพคือธาตุใด", "ไฮโดรเจนและฮีเลียม",
     ("คาร์บอนและออกซิเจน", "เหล็กและนิกเกิล", "ยูเรเนียมและทองคำ", "ซิลิคอนและอะลูมิเนียม")),
    ("เหตุใดเอกภพจึงโปร่งแสงเมื่ออายุประมาณ 380,000 ปี", "อิเล็กตรอนถูกจับเป็นอะตอม แสงจึงเคลื่อนที่ได้โดยไม่ถูกกระเจิง",
     ("ดาวฤกษ์รุ่นแรกส่องสว่าง", "ควาร์กรวมกันเป็นโปรตอน", "หลุมดำขนาดใหญ่ดูดกลืนแสงทั้งหมด เอกภพจึงมืดสนิทไประยะหนึ่ง", "เอกภพหยุดขยายตัวชั่วคราว แสงจึงเดินทางได้ไกลขึ้นเป็นครั้งแรก")),
    ("ตามทฤษฎีบิกแบง สสารในเอกภพระยะแรกเกิดขึ้นจากอะไร", "พลังงานเปลี่ยนเป็นสสารตามสมการ E = mc²",
     ("การระเบิดของดาวฤกษ์รุ่นแรก", "การชนกันของกาแล็กซีจำนวนมากที่เกิดขึ้นพร้อมกัน", "การหลอมรวมของเหล็กที่แกนของดาวฤกษ์รุ่นแรก", "สสารที่มีอยู่ก่อนบิกแบง")),
)


TIMELINE_HINT = ("หลังบิกแบง เอกภพขยายตัวและเย็นลง: อินฟเลชัน → อนุภาคมูลฐาน → โปรตอนนิวตรอน → นิวเคลียสฮีเลียม (3 นาที) → "
                 "อะตอมและไมโครเวฟพื้นหลัง (380,000 ปี) → ดาวฤกษ์และกาแล็กซีรุ่นแรก")


@question_type(
    "astro.universe_evolution_foundation",
    display_name={"th": "จุดกำเนิดและการขยายตัวของเอกภพ"},
    level=UPPER_SIX, subject=SUBJECT, topic=UNIVERSE_TOPIC,
)
class UniverseEvolutionFoundation(QuestionType):
    """Know the hot dense start, the first elements, and why it cooled."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, UNIVERSE_FACTS,
            hint="นึกว่าเอกภพขยายตัวและเย็นลงเรื่อย ๆ นับจากบิกแบง",
        ), UNIVERSE_TOPIC)


@question_type(
    "astro.cosmic_timeline_foundation",
    display_name={"th": "เหตุการณ์และการเปลี่ยนแปลงของเอกภพหลังบิกแบง"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_TIMELINE,
)
class CosmicTimelineFoundation(QuestionType):
    """Events, their times, temperature and the first elements."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            stem, right, wrongs = rng.choice(TIMELINE_FACTS)
            return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_TIMELINE, hint=TIMELINE_HINT)
        # The two "first fraction of a second" rows share a time, so only the later four are asked by time.
        event, when = rng.choice(TIMELINE[2:])
        others = [w for e, w in TIMELINE[2:] if e != event] + ["ประมาณ 13,800 ล้านปี"]
        return _labelled(stem=f"เหตุการณ์ \"{event}\" เกิดขึ้นเมื่อเอกภพมีอายุเท่าใด", correct=when, wrongs=tuple(others),
                         topic=TOPIC_TIMELINE, hint=TIMELINE_HINT)


@question_type(
    "astro.universe_evolution_fluency",
    display_name={"th": "วิวัฒนาการของเอกภพจากเส้นเวลา"},
    level=UPPER_SIX, subject=SUBJECT, topic=UNIVERSE_TOPIC,
)
class UniverseEvolutionFluency(QuestionType):
    """Read the timeline and describe all four things the indicator names.

    ``พลังงาน สสาร ขนาด อุณหภูมิ`` sit under one verb, so by the multi-object rule
    the ``exact`` answer has to reach every one of them.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem = ("เส้นเวลาของวิวัฒนาการของเอกภพหลังบิกแบงเป็นดังนี้ "
                f"{_timeline()} ")
        draw = rng.random()
        if draw < 0.4:
            return _labelled_science_wave_c6(
                stem=stem + "จากข้อมูลนี้ ข้อใดสรุปการเปลี่ยนแปลงของพลังงาน สสาร "
                            "ขนาด และอุณหภูมิของเอกภพได้ถูกต้อง",
                correct=SPANNING, wrongs=SPANNING_WRONGS,
                hint="ตอบให้ครบทั้งสี่เรื่อง แล้วตรวจทิศทางของแต่ละเรื่องจากเส้นเวลา",
                topic=UNIVERSE_TOPIC,
            )
        epoch = rng.choice(EPOCHS)
        others = [other for other in EPOCHS if other.when != epoch.when]
        rng.shuffle(others)
        if draw < 0.7:
            return _labelled_science_wave_c6(
                stem=stem + f"จากข้อมูลนี้ ใน{epoch.when} เกิดอะไรขึ้น",
                correct=epoch.event,
                wrongs=tuple(other.event for other in others[:3]),
                hint="หาช่วงเวลาที่โจทย์ถามบนเส้นเวลา แล้วอ่านเหตุการณ์ที่กำกับไว้",
                topic=UNIVERSE_TOPIC,
            )
        return _labelled_science_wave_c6(
            stem=stem + f"จากข้อมูลนี้ ขณะที่{epoch.event} "
                        "เอกภพมีอุณหภูมิประมาณเท่าใด",
            correct=epoch.temperature,
            wrongs=tuple(other.temperature for other in others[:3]),
            hint="หาเหตุการณ์ที่โจทย์ถาม แล้วอ่านอุณหภูมิในวงเล็บของแถวนั้น",
            topic=UNIVERSE_TOPIC,
        )


@question_type(
    "astro.cosmic_timeline_fluency",
    display_name={"th": "ลำดับเหตุการณ์ของเอกภพ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_TIMELINE,
)
class CosmicTimelineFluency(QuestionType):
    """Which of two or four events came first or last."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        idx = sorted(rng.sample(range(len(TIMELINE)), 4))
        first = rng.random() < 0.5
        right = TIMELINE[idx[0] if first else idx[-1]][0]
        return _labelled(stem=f"เหตุการณ์ใดเกิดขึ้น{'ก่อน' if first else 'หลัง'}สุดในบรรดาตัวเลือก", correct=right,
                         wrongs=tuple(TIMELINE[i][0] for i in idx if TIMELINE[i][0] != right), topic=TOPIC_TIMELINE, hint=TIMELINE_HINT)


@question_type(
    "astro.universe_evolution_application",
    display_name={"th": "วิเคราะห์วิวัฒนาการของเอกภพ"},
    level=UPPER_SIX, subject=SUBJECT, topic=UNIVERSE_TOPIC,
)
class UniverseEvolutionApplication(QuestionType):
    """Test the explosion myth, look-back time, and where the centre is."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, UNIVERSE_SCENARIOS,
            hint="นึกว่าอวกาศเองขยายตัว และแสงต้องใช้เวลาเดินทาง",
        ), UNIVERSE_TOPIC)


@question_type(
    "astro.cosmic_timeline_application",
    display_name={"th": "คำนวณอุณหภูมิเมื่อเอกภพขยายตัวและสัดส่วนธาตุแรกเริ่ม"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_TIMELINE,
)
class CosmicTimelineApplication(QuestionType):
    """Temperature falls as 1/size; hydrogen and helium at 3 : 1 by mass."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.55:
            temp = rng.choice((3000, 6000, 12000, 30000, 60000))
            factor = rng.choice((2, 4, 5, 10, 20, 25, 50, 100))
            if rng.random() < 0.6:
                return numeric(stem=f"อุณหภูมิของรังสีในเอกภพแปรผกผันกับขนาดของเอกภพ ถ้าขณะหนึ่งอุณหภูมิเป็น {show(temp)} K "
                                    f"เมื่อเอกภพขยายขนาดเป็น {factor} เท่า อุณหภูมิเป็นกี่ K", answer=Fraction(temp, factor),
                               wrongs=[temp * factor, temp - factor, Fraction(temp, factor * 2)], unit="K", topic=TOPIC_TIMELINE,
                               hint="อุณหภูมิใหม่ = อุณหภูมิเดิม ÷ จำนวนเท่าที่ขยาย")
            return numeric(stem=f"อุณหภูมิของรังสีในเอกภพแปรผกผันกับขนาดของเอกภพ อุณหภูมิลดลงจาก {show(temp)} K เป็น {show(Fraction(temp, factor))} K "
                                f"เอกภพขยายขนาดขึ้นกี่เท่า", answer=factor, wrongs=[factor * 2, temp - Fraction(temp, factor), factor + 10],
                           unit="เท่า", topic=TOPIC_TIMELINE, hint="จำนวนเท่า = อุณหภูมิเดิม ÷ อุณหภูมิใหม่")
        mass = rng.choice((4, 8, 12, 20, 40, 60, 100, 200))
        helium = rng.random() < 0.5
        return numeric(stem=f"สสารปกติในยุคแรกของเอกภพมีไฮโดรเจนต่อฮีเลียมประมาณ 3 : 1 โดยมวล ในแก๊สดั้งเดิม {mass} หน่วยมวล "
                            f"มี{'ฮีเลียม' if helium else 'ไฮโดรเจน'}กี่หน่วยมวล",
                       answer=Fraction(mass, 4) if helium else Fraction(3 * mass, 4),
                       wrongs=[Fraction(3 * mass, 4) if helium else Fraction(mass, 4), Fraction(mass, 3), mass],
                       unit="หน่วยมวล", topic=TOPIC_TIMELINE, hint="ฮีเลียม 1 ส่วนจาก 4 ส่วน ไฮโดรเจน 3 ส่วนจาก 4 ส่วน")
