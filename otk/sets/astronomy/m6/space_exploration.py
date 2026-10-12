"""การสำรวจอวกาศ

ดาราศาสตร์ · ม.6 · สสวท. พื้นฐาน
Indicators: ว 3.1 ม.6/10

Sets moved here from: science_wave_c9.
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
from otk.sets._support.science_wave_c6 import UPPER_SIX
from otk.sets._support.science_wave_c9 import EXPLORATION_SCENARIOS

PROVENANCE = Provenance("original")


EXPLORATION_TOPIC = "การสำรวจอวกาศ"


TELESCOPE = "กล้องโทรทรรศน์"


SATELLITE = "ดาวเทียม"


SPACECRAFT = "ยานอวกาศ"


STATION = "สถานีอวกาศ"


class Band(NamedTuple):
    """One wavelength band, what only it shows well, and where its telescope must sit."""
    name: str
    reveals: str
    placed: str


# Each band is paired with something the others cannot show as well, so a
# phenomenon names exactly one band. Ultraviolet and gamma rays are left out:
# both sit beside X-rays in what they show and where they must be placed, and
# either would give an X-ray item a second defensible answer.
BANDS = (
    Band("ช่วงคลื่นวิทยุ",
         "แก๊สไฮโดรเจนที่เย็นจัดระหว่างดาวฤกษ์ ซึ่งแผ่คลื่นยาว 21 เซนติเมตร",
         "ตั้งบนพื้นโลกได้ทั้งกลางวันและกลางคืนแม้มีเมฆ และนำจานหลายจานมาทำงานร่วมกันเพื่อเพิ่มความละเอียด"),
    Band("ช่วงอินฟราเรด",
         "ดาวฤกษ์ก่อนเกิดที่ซ่อนอยู่หลังกลุ่มฝุ่นหนาจนแสงที่ตามองเห็นผ่านออกมาไม่ได้",
         "ส่วนใหญ่ต้องอยู่นอกชั้นบรรยากาศและต้องทำให้ตัวกล้องเย็นจัด เพราะไอน้ำดูดกลืนคลื่นและความร้อนของกล้องเองรบกวน"),
    Band("ช่วงแสงที่ตามองเห็น",
         "สีและรูปร่างของดาวฤกษ์ เนบิวลา และดาวเคราะห์ในแบบเดียวกับที่ตามนุษย์มองเห็น",
         "ตั้งบนยอดเขาสูงที่อากาศแห้งและนิ่งได้ แต่ภาพจะคมที่สุดเมื่อพ้นอากาศที่ไหวตัว"),
    Band("ช่วงรังสีเอกซ์",
         "แก๊สที่ร้อนนับล้านเคลวินซึ่งไหลวนเข้าสู่หลุมดำและอยู่ในซากซูเปอร์โนวา",
         "ต้องอยู่นอกชั้นบรรยากาศเท่านั้น เพราะชั้นบรรยากาศดูดกลืนรังสีช่วงนี้ไว้ทั้งหมด"),
)


# Bands that can defensibly study another band's phenomenon, so are never
# offered as the wrong band for it: millimetre-wave radio dishes do observe
# forming stars through their dust.
DEFENSIBLE = {"ช่วงอินฟราเรด": frozenset({"ช่วงคลื่นวิทยุ"})}


# Absorbed by dust and by the air alike, so it is never right for any phenomenon
# in the table; it fills a choice left empty by ``DEFENSIBLE``.
ULTRAVIOLET = "ช่วงอัลตราไวโอเลต"


def _wrong_bands(band: Band) -> list[str]:
    """Bands that no reading makes right for ``band``'s phenomenon."""
    excluded = DEFENSIBLE.get(band.name, frozenset())
    wrongs = [other.name for other in BANDS
              if other.name != band.name and other.name not in excluded]
    return wrongs + [ULTRAVIOLET] * (3 - len(wrongs))


class Platform(NamedTuple):
    """A means of going to space, what it is for, and a job only it does well."""
    name: str
    role: str
    job: str


PLATFORMS = (
    Platform(SATELLITE,
             "โคจรรอบโลกในวงโคจรเดิม เก็บข้อมูลต่อเนื่องเป็นเวลาหลายปีโดยไม่มีคนอยู่บนนั้น",
             "ถ่ายภาพพื้นที่เพาะปลูกทั่วประเทศซ้ำทุกสัปดาห์ต่อเนื่องหลายปีจากวงโคจรผ่านขั้วโลก"),
    Platform(SPACECRAFT,
             "เดินทางออกจากวงโคจรของโลกไปถึงดาวเคราะห์หรือวัตถุอื่น เพื่อถ่ายภาพระยะใกล้ ลงจอด หรือเก็บตัวอย่าง",
             "ลงจอดบนดาวอังคารเพื่อเก็บตัวอย่างหินและดินมาวิเคราะห์"),
    Platform(STATION,
             "โคจรรอบโลกโดยมีนักบินอวกาศผลัดเปลี่ยนกันอยู่ประจำ เพื่อทำการทดลองในสภาพไร้น้ำหนัก",
             "ให้นักบินอวกาศเฝ้าดูการเจริญเติบโตของพืชในสภาพไร้น้ำหนักติดต่อกันหกเดือน"),
)


def _telescope_clause(band: Band, shown_as: str) -> str:
    return (f"{TELESCOPE}ต้องใช้หลายช่วงความยาวคลื่น เพราะวัตถุต่างชนิดแผ่คลื่นต่างกัน "
            f"เช่น ใช้{shown_as}ศึกษา{band.reveals}")


# (true clause, false clause) for each platform. Each false clause gives the
# platform another one's role or a limit it does not have.
PLATFORM_CLAUSES = {
    SATELLITE: (f"{SATELLITE}โคจรรอบโลกเพื่อเก็บข้อมูลต่อเนื่องจากวงโคจรเดิมเป็นเวลานาน",
                f"{SATELLITE}เดินทางออกจากวงโคจรของโลกไปลงจอดบนดาวเคราะห์ดวงอื่น"),
    SPACECRAFT: (f"{SPACECRAFT}เดินทางไปถึงดาวเคราะห์หรือวัตถุอื่นเพื่อสำรวจระยะใกล้ ลงจอด หรือเก็บตัวอย่าง",
                 f"{SPACECRAFT}ต้องโคจรอยู่รอบโลกเสมอ จึงสำรวจวัตถุอื่นได้จากระยะไกลเท่านั้น"),
    STATION: (f"{STATION}ให้นักบินอวกาศอยู่ประจำเพื่อทำการทดลองในสภาพไร้น้ำหนัก",
              f"{STATION}เป็นยานไร้คนขับที่ส่งออกไปสำรวจดาวเคราะห์ชั้นนอก"),
}


def _joined(clauses: list[str]) -> str:
    return " ".join(clauses)


def _all_four(band: Band) -> str:
    """The spanning answer: every clause true."""
    return _joined([_telescope_clause(band, band.name)]
                   + [true for true, _ in PLATFORM_CLAUSES.values()])


def _one_false(band: Band, wrong_band: str, which: int) -> str:
    """The spanning answer with exactly one clause made false.

    ``which`` 0 pairs the telescope example with the wrong band; 1-3 falsify a
    platform. Every choice therefore names all four, and each wrong one differs
    from the answer in one clause only, so reading one means is never enough.
    """
    clauses = [_telescope_clause(band, wrong_band if which == 0 else band.name)]
    for index, (true, false) in enumerate(PLATFORM_CLAUSES.values(), start=1):
        clauses.append(false if index == which else true)
    return _joined(clauses)


def _assignment(pairs: list[tuple[str, str]]) -> str:
    return " / ".join(f"{job} → {means}" for job, means in pairs)


# Roles, names and placements that fit none of the platforms or bands.
ROLE_DECOYS = ("ตั้งอยู่บนพื้นโลกและรับคลื่นจากอวกาศผ่านจานขนาดใหญ่",
               "ลอยอยู่ในชั้นบรรยากาศด้วยบอลลูนเพื่อวัดลมฟ้าอากาศ")


NAME_DECOYS = (f"{TELESCOPE}ภาคพื้นดิน", "บอลลูนตรวจอากาศ")


PLACE_DECOYS = ("ตั้งไว้ในอุโมงค์ใต้ดินลึกเพื่อกันแสงรบกวนทุกชนิด",
                "ตั้งบนเรือกลางมหาสมุทรเพื่อให้ห่างจากแสงไฟในเมือง")


@question_type(
    "astro.space_exploration_foundation",
    display_name={"th": "กล้องโทรทรรศน์ช่วงคลื่นต่าง ๆ และยานพาหนะอวกาศ"},
    level=UPPER_SIX, subject=SUBJECT, topic=EXPLORATION_TOPIC,
)
class SpaceExplorationFoundation(QuestionType):
    """Match a band to what it shows or where it sits, or a platform to its role."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        draw = rng.random()
        if draw < 0.35:
            platform = rng.choice(PLATFORMS)
            others = [other for other in PLATFORMS if other.name != platform.name]
            if rng.random() < 0.5:
                return _labelled(
                    stem=f"ข้อใดอธิบายหน้าที่ของ“{platform.name}”ในการสำรวจอวกาศได้ถูกต้อง",
                    correct=platform.role,
                    wrongs=tuple([other.role for other in others] + list(ROLE_DECOYS)),
                    hint="ถามว่ามีคนอยู่บนนั้นหรือไม่ และอยู่รอบโลกหรือเดินทางออกไปไกล",
                    topic=EXPLORATION_TOPIC,
                )
            return _labelled(
                stem=f"สิ่งใดที่“{platform.role}”",
                correct=platform.name,
                wrongs=tuple([other.name for other in others] + list(NAME_DECOYS)),
                hint="ถามว่ามีคนอยู่บนนั้นหรือไม่ และอยู่รอบโลกหรือเดินทางออกไปไกล",
                topic=EXPLORATION_TOPIC,
            )
        band = rng.choice(BANDS)
        others = [other for other in BANDS if other.name != band.name]
        if draw < 0.7:
            return _labelled(
                stem=f"นักดาราศาสตร์ต้องการศึกษา{band.reveals} "
                     f"ควรใช้{TELESCOPE}ช่วงความยาวคลื่นใด",
                correct=band.name,
                wrongs=tuple(_wrong_bands(band)),
                hint="วัตถุที่ร้อนมากแผ่คลื่นสั้น วัตถุที่เย็นแผ่คลื่นยาว",
                topic=EXPLORATION_TOPIC,
            )
        return _labelled(
            stem=f"{TELESCOPE}{band.name}ควรตั้งไว้ที่ใด และเพราะเหตุใด",
            correct=band.placed,
            wrongs=tuple([other.placed for other in others] + list(PLACE_DECOYS)),
            hint="ถามว่าชั้นบรรยากาศปล่อยให้คลื่นช่วงนั้นผ่านลงมาถึงพื้นได้มากเพียงใด",
            topic=EXPLORATION_TOPIC,
        )


@question_type(
    "astro.space_exploration_fluency",
    display_name={"th": "อธิบายการสำรวจอวกาศด้วยกล้องโทรทรรศน์ ดาวเทียม ยานอวกาศ และสถานีอวกาศ"},
    level=UPPER_SIX, subject=SUBJECT, topic=EXPLORATION_TOPIC,
)
class SpaceExplorationFluency(QuestionType):
    """Explain exploration by all four means the indicator names, in one answer.

    The indicator's one assessable verb governs all four, so by the multi-object
    rule every answer this set accepts holds all four.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        band = rng.choice(BANDS)
        if rng.random() < 0.5:
            wrong_band = rng.choice(_wrong_bands(band))
            falsified = rng.sample(range(4), 3)
            return _labelled(
                stem=f"ข้อใดอธิบายการสำรวจอวกาศโดยใช้{TELESCOPE}ในช่วงความยาวคลื่นต่าง ๆ "
                     f"{SATELLITE} {SPACECRAFT} และ{STATION} ได้ถูกต้องทั้งหมด",
                correct=_all_four(band),
                wrongs=tuple(_one_false(band, wrong_band, which) for which in falsified),
                hint="ตรวจทีละส่วน ข้อที่ผิดจะผิดอย่างน้อยหนึ่งส่วน",
                topic=EXPLORATION_TOPIC,
            )
        # Match four jobs to the four means. The telescope job is never swapped
        # with a platform: an orbiting telescope is itself a satellite, so that
        # swap could be defended. A wrong assignment either names the wrong band
        # or swaps two platforms, which no reading makes right.
        wrong_band = rng.choice(_wrong_bands(band))
        telescope_job = (f"ศึกษา{band.reveals}", f"{TELESCOPE}{band.name}")
        platform_jobs = [(platform.job, platform.name) for platform in PLATFORMS]
        correct = [telescope_job, *platform_jobs]
        swaps = [(1, 2), (1, 3), (2, 3)]
        rng.shuffle(swaps)
        wrongs = [[(telescope_job[0], f"{TELESCOPE}{wrong_band}"), *platform_jobs]]
        for first, second in swaps[:2]:
            swapped = list(correct)
            swapped[first] = (correct[first][0], correct[second][1])
            swapped[second] = (correct[second][0], correct[first][1])
            wrongs.append(swapped)
        return _labelled(
            stem="จับคู่งานสำรวจอวกาศทั้งสี่อย่างกับเครื่องมือหรือยานพาหนะที่เหมาะสมที่สุด "
                 "ข้อใดจับคู่ได้ถูกต้องทั้งหมด",
            correct=_assignment(correct),
            wrongs=tuple(_assignment(one) for one in wrongs),
            hint="งานที่ต้องมีคนอยู่นาน งานที่ต้องไปถึงที่ และงานที่ต้องเฝ้าดูโลกซ้ำ ๆ ใช้ต่างกัน",
            topic=EXPLORATION_TOPIC,
        )


@question_type(
    "astro.space_exploration_application",
    display_name={"th": "นำความรู้เทคโนโลยีอวกาศมาประยุกต์ใช้"},
    level=UPPER_SIX, subject=SUBJECT, topic=EXPLORATION_TOPIC,
)
class SpaceExplorationApplication(QuestionType):
    """Choose the right means for a new job, and carry space technology into daily life."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, EXPLORATION_SCENARIOS,
            hint="ถามว่างานนั้นต้องรับคลื่นช่วงใด ต้องไปถึงที่ ต้องมีคน หรือต้องเฝ้าดูซ้ำ ๆ",
        ), EXPLORATION_TOPIC)
