"""พลังงานทดแทน

ธรณีวิทยา · ม.2 · สสวท. พื้นฐาน
Indicators: ว 3.2 ม.2/3

Sets moved here from: science_wave_c19.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b8 import LEVEL as MIDDLE_TWO
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c10 import SUBJECT
from otk.sets._support.science_wave_c13 import _swapped, _swaps
from otk.sets._support.science_wave_c15 import FIVE_LETTERS
from otk.sets._support.science_wave_c19 import RENEWABLE_SCENARIOS

PROVENANCE = Provenance("original")


RENEWABLE_TOPIC = "พลังงานทดแทน"


class Energy(NamedTuple):
    """A renewable energy, with its advantage and its limit in one summary."""
    name: str
    summary: str


ENERGIES = (
    Energy("พลังงานแสงอาทิตย์",
           "ข้อดี: ไม่ก่อมลพิษขณะผลิตไฟฟ้าและติดตั้งบนหลังคาได้ / ข้อจำกัด: ผลิตไม่ได้ในเวลากลางคืนและได้น้อยเมื่อมีเมฆมาก"),
    Energy("พลังงานลม",
           "ข้อดี: ไม่ก่อมลพิษและใช้ได้ทั้งกลางวันกลางคืน / ข้อจำกัด: ต้องมีลมพัดแรงสม่ำเสมอ และกังหันมีเสียงดัง"),
    Energy("พลังงานน้ำ",
           "ข้อดี: ผลิตไฟฟ้าได้มากและควบคุมได้ตามต้องการ / ข้อจำกัด: การสร้างเขื่อนทำให้ป่าและที่อยู่ของสัตว์ถูกน้ำท่วม"),
    Energy("พลังงานชีวมวล",
           "ข้อดี: ใช้เศษวัสดุการเกษตรที่เหลือทิ้งให้เกิดประโยชน์ / ข้อจำกัด: การเผาทำให้เกิดฝุ่นและควัน ถ้าจัดการไม่ดี"),
    Energy("พลังงานความร้อนใต้พิภพ",
           "ข้อดี: ผลิตไฟฟ้าได้ต่อเนื่องไม่ขึ้นกับสภาพอากาศ / ข้อจำกัด: ใช้ได้เฉพาะพื้นที่ที่มีแหล่งความร้อนใต้ดิน เช่น บ่อน้ำพุร้อน"),
)


class Locality(NamedTuple):
    """A community, and the one renewable energy its own resources suit."""
    situation: str
    energy: str


# Each case names what the place has and what it lacks, so exactly one energy
# uses a resource the place actually has.
LOCALITIES = (
    Locality("หมู่บ้านบนพื้นที่ราบโล่ง แดดจัดเกือบทั้งปี ไม่มีลมแรง ไม่มีลำน้ำไหลผ่าน และไม่มีเศษวัสดุการเกษตร",
             "พลังงานแสงอาทิตย์"),
    Locality("ชุมชนบนแหลมริมทะเลที่มีลมพัดแรงสม่ำเสมอทั้งปี แต่มีเมฆฝนมาก และไม่มีลำน้ำหรือเศษวัสดุการเกษตร",
             "พลังงานลม"),
    Locality("ชุมชนในหุบเขาที่มีลำธารไหลแรงตลอดปี มีป่าหนาบังแดด ลมสงบ และไม่มีเศษวัสดุการเกษตร",
             "พลังงานน้ำ"),
    Locality("ชุมชนเกษตรที่มีแกลบและชานอ้อยเหลือทิ้งจำนวนมากทุกปี แต่มีเมฆฝนมาก ไม่มีลมแรง และไม่มีลำน้ำไหลผ่าน",
             "พลังงานชีวมวล"),
    Locality("อำเภอหนึ่งมีบ่อน้ำพุร้อนอุณหภูมิสูงผุดขึ้นจากใต้ดินตลอดปี แต่มีเมฆฝนมาก ลมสงบ และไม่มีลำน้ำ",
             "พลังงานความร้อนใต้พิภพ"),
)


# A second locality for each energy, again with only that one resource on hand.
MORE_LOCALITIES = (
    Locality("โรงเรียนบนเกาะกลางทะเลที่มีแดดจัดตลอดปี ลมสงบในฤดูฝน ไม่มีลำน้ำ "
             "และไม่มีเศษวัสดุการเกษตร", "พลังงานแสงอาทิตย์"),
    Locality("หมู่บ้านบนสันเขาโล่งที่ลมพัดแรงตลอดทั้งวันทั้งคืน มีหมอกและเมฆปกคลุมบ่อย "
             "ไม่มีลำน้ำไหลผ่าน และไม่มีเศษวัสดุการเกษตร", "พลังงานลม"),
    Locality("หมู่บ้านใต้น้ำตกที่มีน้ำไหลแรงตลอดปี อยู่ในหุบที่แดดส่องถึงน้อย ลมสงบ "
             "และไม่มีเศษวัสดุการเกษตร", "พลังงานน้ำ"),
    Locality("ฟาร์มสุกรขนาดใหญ่ที่มีมูลสัตว์และเศษอาหารสัตว์เหลือจำนวนมากทุกวัน "
             "แต่มีเมฆฝนมาก ลมสงบ และไม่มีลำน้ำไหลผ่าน", "พลังงานชีวมวล"),
    Locality("ตำบลหนึ่งมีไอน้ำร้อนพวยพุ่งจากรอยแยกใต้ดินตลอดปี แต่มีเมฆฝนมาก ลมสงบ "
             "และไม่มีเศษวัสดุการเกษตร", "พลังงานความร้อนใต้พิภพ"),
)


def _match_energies(letters: list[str]) -> str:
    return " / ".join(f"{energy.name} → {letter}" for energy, letter in zip(ENERGIES, letters))


@question_type(
    "geo.renewable_energy_foundation",
    display_name={"th": "เลือกพลังงานทดแทนให้เหมาะกับท้องถิ่น"},
    level=MIDDLE_TWO, subject=SUBJECT, topic=RENEWABLE_TOPIC,
)
class RenewableEnergyFoundation(QuestionType):
    """Propose the renewable energy that suits a locality — the second free verb."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        place = rng.choice(LOCALITIES + MORE_LOCALITIES)
        others = [energy.name for energy in ENERGIES if energy.name != place.energy]
        rng.shuffle(others)
        return _labelled(
            stem=f"{place.situation} ควรเสนอให้ใช้พลังงานทดแทนประเภทใดจึงเหมาะสมกับท้องถิ่นนี้ที่สุด",
            correct=place.energy,
            wrongs=tuple(others[:3]),
            hint="หาทรัพยากรที่ท้องถิ่นนี้มีอยู่จริง และตัดพลังงานที่ท้องถิ่นนี้ขาดทรัพยากรออก",
            topic=RENEWABLE_TOPIC,
        )


@question_type(
    "geo.renewable_energy_fluency",
    display_name={"th": "เปรียบเทียบข้อดีและข้อจำกัดของพลังงานทดแทนแต่ละประเภท"},
    level=MIDDLE_TWO, subject=SUBJECT, topic=RENEWABLE_TOPIC,
)
class RenewableEnergyFluency(QuestionType):
    """Place all five energies against their advantages and limits; each wrong choice swaps two."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shuffled = list(ENERGIES)
        rng.shuffle(shuffled)
        listing = " / ".join(f"{letter}. {energy.summary}"
                             for letter, energy in zip(FIVE_LETTERS, shuffled))
        letter_of = {energy.name: FIVE_LETTERS[i] for i, energy in enumerate(shuffled)}
        right = [letter_of[energy.name] for energy in ENERGIES]
        return _labelled(
            stem=f"ข้อมูลที่รวบรวมได้เกี่ยวกับพลังงานทดแทน 5 ประเภท — {listing} "
                 "ข้อใดเปรียบเทียบข้อดีและข้อจำกัดของพลังงานทดแทนแต่ละประเภทได้ถูกต้องทั้งหมด",
            correct=_match_energies(right),
            wrongs=tuple(_match_energies(_swapped(right, i, j)) for i, j in _swaps(rng, 3, 5)),
            hint="ข้อจำกัดมักบอกสิ่งที่พลังงานนั้นต้องพึ่งพา เริ่มจับคู่จากข้อจำกัดที่ชัดที่สุด",
            topic=RENEWABLE_TOPIC,
        )


@question_type(
    "geo.renewable_energy_application",
    display_name={"th": "ประเมินการใช้พลังงานทดแทนในสถานการณ์จริง"},
    level=MIDDLE_TWO, subject=SUBJECT, topic=RENEWABLE_TOPIC,
)
class RenewableEnergyApplication(QuestionType):
    """Night on a solar roof, mixing sources, and weighing a bagasse plant."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, RENEWABLE_SCENARIOS,
            hint="ชั่งข้อดีกับข้อจำกัดของพลังงานนั้นในสถานการณ์ที่ถาม",
        ), RENEWABLE_TOPIC)
