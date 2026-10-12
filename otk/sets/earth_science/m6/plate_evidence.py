"""หลักฐานการเคลื่อนที่ของแผ่นธรณี

ธรณีวิทยา · ม.6 · สสวท. พื้นฐาน
Indicators: ว 3.2 ม.6/2

Sets moved here from: science_wave_c22.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c6 import UPPER_SIX
from otk.sets._support.science_wave_c10 import SUBJECT
from otk.sets._support.science_wave_c22 import EVIDENCE_FACTS, EVIDENCE_SCENARIOS

PROVENANCE = Provenance("original")


EVIDENCE_TOPIC = "หลักฐานการเคลื่อนที่ของแผ่นธรณี"


def seafloor_record(rng: Random) -> tuple[int, list[tuple[int, int]]]:
    """A spreading rate in km per million years each side, and (distance, age) rows.

    Distances are multiples of 200 km and the rates divide 200, so every age is a
    whole number of million years and rises evenly with distance.
    """
    rate = rng.choice((20, 40, 50))
    distances = sorted(rng.sample(range(200, 2000, 200), 4))
    return rate, [(distance, distance // rate) for distance in distances]


SPREADING = ("อายุหินเพิ่มขึ้นเท่า ๆ กันทั้งสองฝั่งเมื่อห่างจากสันเขา "
             "แสดงว่าพื้นมหาสมุทรใหม่เกิดที่สันเขาแล้วแยกออกไปทั้งสองข้าง")


def _rate_slips(rng: Random, rate: int, far: int) -> tuple[str, ...]:
    """Three wrong rates with the answer's rank drawn at random: halving, doubling, or the distance itself."""
    smaller = [v for v in dict.fromkeys((rate // 2, rate - 1, rate // 3)) if 0 < v < rate]
    larger = [v for v in dict.fromkeys((rate * 2, rate * 3, far, rate + rate // 2)) if v > rate]
    below = rng.randint(max(0, 3 - len(larger)), min(3, len(smaller)))
    picked = rng.sample(smaller, below) + rng.sample(larger, 3 - below)
    return tuple(f"{v} กิโลเมตรต่อล้านปี" for v in picked)


@question_type(
    "geo.plate_evidence_foundation",
    display_name={"th": "หลักฐานการเคลื่อนที่ของแผ่นธรณี"},
    level=UPPER_SIX, subject=SUBJECT, topic=EVIDENCE_TOPIC,
)
class PlateEvidenceFoundation(QuestionType):
    """Name what each kind of evidence supports, one at a time."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, EVIDENCE_FACTS,
            hint="หลักฐานที่ดีแสดงว่าสิ่งที่อยู่ห่างกันในปัจจุบันเคยอยู่ด้วยกันหรือเคยอยู่ที่อื่น",
        ), EVIDENCE_TOPIC)


@question_type(
    "geo.plate_evidence_fluency",
    display_name={"th": "อธิบายหลักฐานการแผ่ขยายของพื้นมหาสมุทรจากข้อมูล"},
    level=UPPER_SIX, subject=SUBJECT, topic=EVIDENCE_TOPIC,
)
class PlateEvidenceFluency(QuestionType):
    """Read sea-floor ages either side of a ridge and explain what they support."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        rate, rows = seafloor_record(rng)
        west = " / ".join(f"ห่างไปทางตะวันตก {d} กิโลเมตร อายุ {a} ล้านปี" for d, a in rows)
        east = " / ".join(f"ห่างไปทางตะวันออก {d} กิโลเมตร อายุ {a} ล้านปี" for d, a in rows)
        stem = f"ข้อมูลอายุหินบนพื้นมหาสมุทรที่ห่างจากสันเขากลางมหาสมุทร — {west} / {east}"
        if rng.random() < 0.5:
            return _labelled(
                stem=f"{stem} จากข้อมูลนี้ ข้อใดอธิบายหลักฐานการเคลื่อนที่ของแผ่นธรณีได้ถูกต้อง",
                correct=SPREADING,
                wrongs=("อายุหินลดลงเมื่อห่างจากสันเขากลางมหาสมุทรทั้งสองฝั่ง แสดงว่าพื้นมหาสมุทรเก่ากำลังจมลงและถูกทำลายที่สันเขา",
                        "อายุหินเพิ่มขึ้นเฉพาะฝั่งตะวันตก แสดงว่าแผ่นธรณีเคลื่อนที่ออกจากสันเขาไปทางเดียวเท่านั้น",
                        "อายุหินเท่ากันทุกตำแหน่ง แสดงว่าพื้นมหาสมุทรไม่มีการเคลื่อนที่ออกจากสันเขาเลย"),
                hint="เทียบอายุหินกับระยะห่างจากสันเขาทั้งสองฝั่ง",
                topic=EVIDENCE_TOPIC,
            )
        return _labelled(
            stem=f"{stem} จากข้อมูลนี้ พื้นมหาสมุทรแผ่ขยายออกจากสันเขาข้างละประมาณกี่กิโลเมตรต่อล้านปี",
            correct=f"{rate} กิโลเมตรต่อล้านปี",
            wrongs=_rate_slips(rng, rate, rows[-1][0]),
            hint="นำระยะห่างหารด้วยอายุหินของแถวเดียวกัน",
            topic=EVIDENCE_TOPIC,
        )


@question_type(
    "geo.plate_evidence_application",
    display_name={"th": "ใช้หลักฐานวิเคราะห์การเคลื่อนที่ของแผ่นธรณี"},
    level=UPPER_SIX, subject=SUBJECT, topic=EVIDENCE_TOPIC,
)
class PlateEvidenceApplication(QuestionType):
    """Age a rock from a spreading rate, weigh a coincidence claim, and young sea floor."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, EVIDENCE_SCENARIOS,
            hint="เชื่อมหลักฐานกับกระบวนการที่ทำให้แผ่นธรณีแยกออก เคลื่อนที่ หรือจมลง",
        ), EVIDENCE_TOPIC)
