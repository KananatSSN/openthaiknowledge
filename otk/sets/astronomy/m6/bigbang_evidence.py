"""หลักฐานที่สนับสนุนทฤษฎีบิกแบง

ดาราศาสตร์ · ม.6 · สสวท. พื้นฐาน
Indicators: ว 3.1 ม.6/2

Sets moved here from: science_wave_c6.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c1 import SUBJECT
from otk.sets._support.science_wave_c6 import EVIDENCE_FACTS, EVIDENCE_SCENARIOS, UPPER_SIX

PROVENANCE = Provenance("original")


EVIDENCE_TOPIC = "หลักฐานที่สนับสนุนทฤษฎีบิกแบง"


HUBBLE = "ความสัมพันธ์ระหว่างความเร็วกับระยะทางของกาแล็กซี"


CMB = "ไมโครเวฟพื้นหลังจากอวกาศ"


class Galaxy(NamedTuple):
    """A measured galaxy: how far away, and how fast it is receding."""
    name: str
    distance: int
    speed: int


# v = H0 d with H0 taken as 70 km/s per Mpc, so the table is internally exact and
# a learner reading it can recover the straight-line relation.
HUBBLE_CONSTANT = 70


GALAXIES = (
    Galaxy("กาแล็กซี A", 20, 20 * HUBBLE_CONSTANT),
    Galaxy("กาแล็กซี B", 50, 50 * HUBBLE_CONSTANT),
    Galaxy("กาแล็กซี C", 120, 120 * HUBBLE_CONSTANT),
    Galaxy("กาแล็กซี D", 300, 300 * HUBBLE_CONSTANT),
)


# Distances a measured table draws four of, in megaparsecs.
DISTANCE_POOL = (10, 20, 30, 40, 50, 60, 80, 100, 120, 150, 200, 250, 300, 400)


def measured_galaxies(rng: Random) -> tuple[Galaxy, ...]:
    """Four galaxies at drawn distances, nearest first, each on v = H0 d exactly."""
    distances = sorted(rng.sample(DISTANCE_POOL, 4))
    return tuple(Galaxy(galaxy.name, distance, distance * HUBBLE_CONSTANT)
                 for galaxy, distance in zip(GALAXIES, distances))


PROPORTIONAL = "ยิ่งอยู่ไกล ยิ่งถอยห่างเร็วขึ้นเป็นสัดส่วนกัน"


INVERSE = "ยิ่งอยู่ไกล ยิ่งถอยห่างช้าลง"


UNRELATED = "ความเร็วไม่เกี่ยวกับระยะทาง"


APPROACHING = "กาแล็กซีทั้งหมดกำลังเคลื่อนเข้าหาเรา"


# The one answer that reaches both bodies of evidence the indicator names.
BOTH_EVIDENCE = (f"{HUBBLE}แสดงว่าเอกภพกำลังขยายตัว "
                 f"จึงเคยเล็กและหนาแน่นกว่านี้ ส่วน{CMB}"
                 "คือแสงที่เหลือจากยุคที่เอกภพร้อนและโปร่งใสขึ้นเป็นครั้งแรก "
                 "หลักฐานทั้งสองจึงชี้ไปที่จุดเริ่มต้นที่ร้อนและหนาแน่นเหมือนกัน")


BOTH_WRONGS = (
    f"{HUBBLE}แสดงว่าเอกภพกำลังหดตัว "
    f"ส่วน{CMB}คือความร้อนที่ดาวฤกษ์ในปัจจุบันแผ่ออกมา "
    "หลักฐานทั้งสองจึงชี้ว่าเอกภพในอดีตใหญ่และเย็นกว่าปัจจุบัน ไม่เคยร้อนและหนาแน่น",
    f"{HUBBLE}แสดงว่าเอกภพมีขนาดคงที่ "
    f"ส่วน{CMB}มาจากใจกลางกาแล็กซีของเราเพียงทิศเดียว "
    "หลักฐานทั้งสองจึงไม่ได้บอกอะไรเกี่ยวกับจุดเริ่มต้นของเอกภพ",
    f"{HUBBLE}เป็นหลักฐานเพียงอย่างเดียวที่ใช้ได้ "
    f"ส่วน{CMB}ยังไม่เคยตรวจพบจริง "
    "ทฤษฎีบิกแบงจึงอาศัยเพียงการที่กาแล็กซีถอยห่างออกไปเท่านั้น",
)


RELATION_DECOYS = ("กาแล็กซีที่ใกล้ที่สุดถอยห่างเร็วที่สุด และกาแล็กซีที่ไกลอยู่นิ่ง",
                   "ความเร็วเพิ่มขึ้นเป็นกำลังสองของระยะทาง")


MORE_BOTH_WRONGS = (
    f"{HUBBLE}แสดงว่ากาแล็กซีทั้งหมดเคลื่อนเข้าหาเรา "
    f"ส่วน{CMB}คือคลื่นที่ส่งมาจากดาวเทียมของมนุษย์ "
    "หลักฐานทั้งสองจึงชี้ว่าเอกภพกำลังยุบตัวเข้าหากาแล็กซีของเรา",
    f"{HUBBLE}แสดงว่าเอกภพกำลังขยายตัว "
    f"แต่{CMB}ไม่เกี่ยวกับอดีตของเอกภพเลย "
    "เพราะเป็นเพียงคลื่นรบกวนจากชั้นบรรยากาศของโลกที่พบได้ทุกทิศ",
    # Two that keep one half of the answer word for word and break the other.
    f"{HUBBLE}แสดงว่าเอกภพกำลังขยายตัว จึงเคยเล็กและหนาแน่นกว่านี้ "
    f"ส่วน{CMB}คือแสงจากดาวฤกษ์รุ่นแรกที่เพิ่งเกิดขึ้นเมื่อไม่นานมานี้ "
    "หลักฐานทั้งสองจึงชี้ว่าเอกภพเพิ่งเริ่มมีดาวฤกษ์ ไม่ได้ชี้ไปที่จุดเริ่มต้นที่ร้อนและหนาแน่น",
    f"{HUBBLE}แสดงว่ากาแล็กซีทั้งหมดถอยห่างออกจากกาแล็กซีของเรา เราจึงอยู่ตรงศูนย์กลางของการขยายตัว "
    f"ส่วน{CMB}คือแสงที่เหลือจากยุคที่เอกภพร้อนและโปร่งใสขึ้นเป็นครั้งแรก "
    "หลักฐานทั้งสองจึงชี้ว่ากาแล็กซีของเราคือจุดที่บิกแบงเริ่มต้น",
)


@question_type(
    "astro.bigbang_evidence_foundation",
    display_name={"th": "หลักฐานของทฤษฎีบิกแบง"},
    level=UPPER_SIX, subject=SUBJECT, topic=EVIDENCE_TOPIC,
)
class BigBangEvidenceFoundation(QuestionType):
    """Know what redshift shows and what the background radiation is."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, EVIDENCE_FACTS,
            hint="แยกให้ชัดว่าหลักฐานแต่ละอย่างวัดอะไร และบอกอะไรเกี่ยวกับอดีตของเอกภพ",
        ), EVIDENCE_TOPIC)


@question_type(
    "astro.bigbang_evidence_fluency",
    display_name={"th": "อ่านหลักฐานที่สนับสนุนทฤษฎีบิกแบง"},
    level=UPPER_SIX, subject=SUBJECT, topic=EVIDENCE_TOPIC,
)
class BigBangEvidenceFluency(QuestionType):
    """Read the measurements and reach both bodies of evidence the indicator names."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        galaxies = measured_galaxies(rng)
        table = " / ".join(
            f"{galaxy.name}: ระยะทาง {galaxy.distance} เมกะพาร์เซก "
            f"ความเร็วถอยห่าง {galaxy.speed} กิโลเมตรต่อวินาที"
            for galaxy in galaxies)
        stem = f"จากการวัดกาแล็กซีสี่แห่ง ได้ผลดังนี้ {table} "
        draw = rng.random()
        if draw < 0.3:
            return _labelled(
                stem=stem + "จากข้อมูลนี้ ความเร็วถอยห่างสัมพันธ์กับระยะทางอย่างไร",
                correct=PROPORTIONAL,
                wrongs=tuple((INVERSE, UNRELATED, APPROACHING, *RELATION_DECOYS)),
                hint="เทียบความเร็วกับระยะทางของแต่ละกาแล็กซีทีละคู่",
                topic=EVIDENCE_TOPIC,
            )
        if draw < 0.6:
            galaxy = rng.choice(galaxies)
            others = [other for other in galaxies if other.name != galaxy.name]
            return _labelled(
                stem=stem + f"จากข้อมูลนี้ “{galaxy.name}” มีความเร็วถอยห่างเท่าใด",
                correct=f"{galaxy.speed} กิโลเมตรต่อวินาที",
                # The last two are slips a reader makes: taking 100 km/s for every
                # megaparsec, and copying one zero too many. Both run as long as the
                # answer, so the farthest galaxy's answer is not always the longest.
                # A slip can land on another galaxy's speed, so repeats are dropped.
                wrongs=tuple(dict.fromkeys(
                    [f"{other.speed} กิโลเมตรต่อวินาที" for other in others]
                    + [f"{galaxy.distance} กิโลเมตรต่อวินาที",
                       f"{galaxy.distance * 100} กิโลเมตรต่อวินาที",
                       f"{galaxy.speed * 10} กิโลเมตรต่อวินาที"])),
                hint="หาชื่อกาแล็กซีที่โจทย์ถาม แล้วอ่านความเร็วในแถวนั้น",
                topic=EVIDENCE_TOPIC,
            )
        return _labelled(
            stem=stem + f"เมื่อนำข้อมูลนี้มารวมกับการตรวจพบ{CMB} "
                        "ข้อใดอธิบายได้ถูกต้องว่าหลักฐานทั้งสองสนับสนุนทฤษฎีบิกแบงอย่างไร",
            correct=BOTH_EVIDENCE, wrongs=tuple(BOTH_WRONGS + MORE_BOTH_WRONGS),
            hint="ตอบให้ครบทั้งสองหลักฐาน แล้วตรวจว่าแต่ละอย่างบอกอะไรเกี่ยวกับอดีต",
            topic=EVIDENCE_TOPIC,
        )


@question_type(
    "astro.bigbang_evidence_application",
    display_name={"th": "วิเคราะห์หลักฐานทางจักรวาลวิทยา"},
    level=UPPER_SIX, subject=SUBJECT, topic=EVIDENCE_TOPIC,
)
class BigBangEvidenceApplication(QuestionType):
    """Weigh a blueshift, a one-sided background, and a measurement that disagrees."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, EVIDENCE_SCENARIOS,
            hint="ถามว่าหลักฐานนั้นทำนายอะไรไว้ และการวัดตรงกับคำทำนายหรือไม่",
        ), EVIDENCE_TOPIC)
