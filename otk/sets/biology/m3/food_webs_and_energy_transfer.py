"""สายใยอาหารและการถ่ายทอดพลังงาน

ชีวะ · ม.3 · สสวท. พื้นฐาน
Indicators: ว 1.1 ม.3/3

Sets moved here from: science_wave_b.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.numeric_scenario import Calc, PhysCalc, fmt, slips
from otk.sets._support.science_wave_b import LEVEL, SUBJECT, TOPIC, _labelled

PROVENANCE = Provenance("original")


class FoodWeb(NamedTuple):
    """One habitat's web: who eats whom, and the producer everything rests on.

    ``eats`` maps a consumer to everything it eats in this habitat. A web is not
    a chain — most consumers here have more than one food, which is the whole
    difference ม.3/3 turns on and the reason the ป.5 chain sets cannot cover it.
    """
    habitat: str
    producer: str
    eats: dict[str, tuple[str, ...]]


FOOD_WEBS = (
    FoodWeb("นาข้าว", "ต้นข้าว", {
        "ตั๊กแตน": ("ต้นข้าว",),
        "หนู": ("ต้นข้าว",),
        "กบ": ("ตั๊กแตน",),
        "นกกระยาง": ("กบ",),
        "งู": ("หนู", "กบ"),
        "เหยี่ยว": ("งู", "นกกระยาง"),
    }),
    FoodWeb("ทุ่งหญ้า", "หญ้า", {
        "ตั๊กแตน": ("หญ้า",),
        "กระต่าย": ("หญ้า",),
        "นกกินแมลง": ("ตั๊กแตน",),
        "จิ้งจอก": ("กระต่าย",),
        "เหยี่ยว": ("นกกินแมลง", "จิ้งจอก"),
    }),
    FoodWeb("สระน้ำ", "แพลงก์ตอนพืช", {
        "ไรน้ำ": ("แพลงก์ตอนพืช",),
        "หอยขม": ("แพลงก์ตอนพืช",),
        "ปลาเล็ก": ("ไรน้ำ",),
        "ปลาใหญ่": ("ปลาเล็ก",),
        "นกยาง": ("ปลาใหญ่", "หอยขม"),
    }),
    FoodWeb("ป่าชายเลน", "ใบโกงกางที่ร่วงลงน้ำ", {
        "ปูก้ามดาบ": ("ใบโกงกางที่ร่วงลงน้ำ",),
        "หอยนางรม": ("ใบโกงกางที่ร่วงลงน้ำ",),
        "ปลาตีน": ("ปูก้ามดาบ",),
        "นกกินปู": ("ปูก้ามดาบ",),
        "นกกระเต็น": ("ปลาตีน", "หอยนางรม"),
    }),
)


def trophic_level(web: FoodWeb, organism: str) -> int | None:
    """Trophic level counting the producer as 1, or ``None`` if it is ambiguous.

    In a web an organism can sit at two levels at once — a snake eating both a
    rat and a frog is at level 3 by one path and level 4 by another. Those have
    no single defensible answer, so they are never asked about.
    """
    if organism == web.producer:
        return 1
    prey = web.eats.get(organism)
    if not prey:
        return None
    levels = {trophic_level(web, item) for item in prey}
    if len(levels) != 1 or None in levels:
        return None
    return levels.pop() + 1


def chains_to(web: FoodWeb, organism: str) -> list[tuple[str, ...]]:
    """Every path from the producer up to ``organism``, shortest first."""
    if organism == web.producer:
        return [(organism,)]
    paths: list[tuple[str, ...]] = []
    for item in web.eats.get(organism, ()):
        paths.extend(path + (organism,) for path in chains_to(web, item))
    return sorted(paths, key=lambda path: (len(path), path))


def predators_of(web: FoodWeb, organism: str) -> tuple[str, ...]:
    return tuple(name for name, prey in web.eats.items() if organism in prey)


def _unambiguous(web: FoodWeb) -> tuple[str, ...]:
    return tuple(name for name in web.eats if trophic_level(web, name) is not None)


LEVEL_NAMES = {
    1: "ผู้ผลิต",
    2: "ผู้บริโภคลำดับที่ 1",
    3: "ผู้บริโภคลำดับที่ 2",
    4: "ผู้บริโภคลำดับที่ 3",
    5: "ผู้บริโภคลำดับที่ 4",
}


def _web_text(web: FoodWeb) -> str:
    """The web written out as one 'X กิน A และ B' line per consumer."""
    return "\n".join(
        f"{name}กิน{'และ'.join(prey)}" for name, prey in web.eats.items()
    )


# (พลังงานที่ผู้ผลิตตรึงไว้ กิโลจูล). Chosen so that dividing by ten three times
# stays whole — the ten-per-cent rule as ม.3 states it, with no rounding to hide
# a slip behind.
PRODUCER_ENERGY = (20_000, 50_000, 100_000, 200_000, 500_000, 1_000_000)


# (พลังงานของลำดับล่าง, พลังงานของลำดับถัดขึ้นไป) กิโลจูล. Real measurements are
# not all exactly ten per cent, and reading the efficiency off the data is the
# skill; a table of tens would let the answer be recited instead.
ENERGY_MEASUREMENTS = (
    (20_000, 2_000), (25_000, 2_000), (15_000, 1_800), (40_000, 6_000),
    (5_000, 1_000), (30_000, 3_600), (12_000, 1_200), (50_000, 4_000),
)


@question_type(
    "ecology.food_web_foundation",
    display_name={"th": "อ่านสายใยอาหาร: ใครกินอะไรและอยู่ลำดับใด"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class FoodWebFoundation(QuestionType):
    """Read one web: what eats a given organism, and which level an organism sits at.

    The ป.5 pilot sets work on a single linear chain, where every organism has
    exactly one food and one predator. A web is the ม.3 object, and the first
    thing it demands is being able to read more than one path at a time.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        web = rng.choice(FOOD_WEBS)
        organisms = (web.producer, *web.eats)
        if rng.random() < 0.5:
            # Who eats this one? Only organisms with exactly one predator here,
            # so the answer is single.
            candidates = [name for name in organisms
                          if len(predators_of(web, name)) == 1]
            target = rng.choice(candidates)
            answer = predators_of(web, target)[0]
            wrongs = [name for name in organisms
                      if name not in (answer, target)]
            rng.shuffle(wrongs)
            return _labelled(
                stem=f"สายใยอาหารใน{web.habitat}:\n{_web_text(web)}\n"
                     f"สิ่งมีชีวิตใดกิน{target}",
                correct=answer,
                wrongs=tuple(wrongs[:3]),
                hint="อ่านทีละบรรทัดแล้วหาบรรทัดที่มีสิ่งมีชีวิตนั้นอยู่หลังคำว่ากิน",
            )
        target = rng.choice(_unambiguous(web))
        level = trophic_level(web, target)
        assert level is not None
        return _labelled(
            stem=f"สายใยอาหารใน{web.habitat}:\n{_web_text(web)}\n"
                 f"{target}ทำหน้าที่เป็นอะไรในสายใยอาหารนี้",
            correct=LEVEL_NAMES[level],
            wrongs=tuple(name for rank, name in sorted(LEVEL_NAMES.items())
                         if rank != level)[:3],
            hint="นับจากผู้ผลิตขึ้นไปตามเส้นทางที่พลังงานถ่ายทอดมาถึงสิ่งมีชีวิตนั้น",
        )


@question_type(
    "ecology.energy_transfer_fluency",
    display_name={"th": "การถ่ายทอดพลังงานระหว่างลำดับขั้นในสายใยอาหาร"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class EnergyTransferFluency(PhysCalc):
    """Put numbers on the transfer: ten per cent up, ten times down, and read it back.

    ม.3/3 is about the energy that moves along the web, not only about who eats
    whom. Without the arithmetic, "พลังงานลดลงเมื่อขึ้นลำดับ" is a slogan; with
    it, the shape of the pyramid follows.
    """

    def draw(self, rng: Random) -> Calc:
        which = rng.random()
        if which < 0.4:
            energy = rng.choice(PRODUCER_ENERGY)
            steps = rng.randint(1, 3)
            answer = energy // 10 ** steps
            return Calc(
                f"ผู้ผลิตในระบบนิเวศหนึ่งตรึงพลังงานไว้ {energy:,} กิโลจูล "
                "ถ้าการถ่ายทอดพลังงานแต่ละลำดับขั้นเป็นไปตามกฎร้อยละ 10 "
                f"ผู้บริโภคลำดับที่ {steps} จะได้รับพลังงานประมาณเท่าใด (กิโลจูล)",
                fmt(answer),
                # หารด้วยสิบผิดจำนวนครั้ง หรือเข้าใจว่า "ร้อยละ 10" คือหายไปร้อยละ 10
                # ต่อขั้น ซึ่งเป็นการอ่านกฎกลับด้านที่พบบ่อยที่สุด
                wrongs=slips(fmt(answer), energy // 10 ** (steps + 1),
                             energy // 10 ** max(steps - 1, 0),
                             energy * 9 ** steps // 10 ** steps),
                hint=r"E_n = E_1 \times (0.1)^{n}")
        if which < 0.7:
            energy = rng.choice(PRODUCER_ENERGY) // 100
            return Calc(
                f"ผู้บริโภคลำดับที่ 2 ในระบบนิเวศหนึ่งได้รับพลังงาน {energy:,} กิโลจูล "
                "ถ้าการถ่ายทอดพลังงานเป็นไปตามกฎร้อยละ 10 "
                "ผู้ผลิตในระบบนิเวศนี้ตรึงพลังงานไว้ประมาณเท่าใด (กิโลจูล)",
                fmt(energy * 100),
                # ย้อนขึ้นไปผิดจำนวนขั้น หรือหารแทนการคูณ
                wrongs=slips(fmt(energy * 100), energy * 10, energy * 1000,
                             energy // 10),
                hint=r"\text{ย้อนกลับหนึ่งลำดับขั้นคือคูณด้วย } 10")
        lower, upper = rng.choice(ENERGY_MEASUREMENTS)
        percent = upper * 100 // lower
        return Calc(
            f"วัดพลังงานสะสมในลำดับขั้นหนึ่งได้ {lower:,} กิโลจูล และในลำดับถัดขึ้นไป "
            f"ได้ {upper:,} กิโลจูล พลังงานถ่ายทอดขึ้นไปได้ร้อยละเท่าใด",
            fmt(percent),
            # กลับเศษกับส่วน ลืมคูณร้อย หรือตอบสิบเพราะจำกฎมาโดยไม่คำนวณ
            wrongs=slips(fmt(percent), lower * 100 // upper, upper // lower, 10),
            hint=r"\text{ร้อยละ} = \frac{E_{2}}{E_{1}} \times 100")


@question_type(
    "ecology.food_web_application",
    display_name={"th": "วิเคราะห์สายใยอาหารเมื่อสิ่งมีชีวิตหนึ่งหายไป"},
    level=LEVEL, subject=SUBJECT, topic=TOPIC,
)
class FoodWebApplication(QuestionType):
    """Trace what a loss does across a web that has more than one path.

    The ป.5 application set follows a cascade down one chain. A web behaves
    differently: a consumer with two foods survives losing one, and a consumer
    with one food does not. Telling those two apart is the reasoning ม.3/3 wants
    a model to support.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        web = rng.choice(FOOD_WEBS)
        which = rng.randrange(3)
        if which == 0:
            return self._sole_food(web, rng)
        if which == 1:
            return self._alternative_food(web, rng)
        return self._paths(web, rng)

    def _sole_food(self, web: FoodWeb, rng: Random) -> GeneratedQuestion:
        """Which consumer is hit hardest — the one with nothing else to eat."""
        organisms = (web.producer, *web.eats)
        candidates = [
            name for name in organisms
            if any(len(web.eats[other]) == 1 for other in predators_of(web, name))
        ]
        lost = rng.choice(candidates)
        hit = [other for other in predators_of(web, lost)
               if len(web.eats[other]) == 1]
        answer = rng.choice(hit)
        # Only organisms that do not eat the lost one at all, so no wrong choice
        # is defensible as a second-best answer.
        wrongs = [name for name in organisms
                  if name not in (lost, answer)
                  and lost not in web.eats.get(name, ())]
        rng.shuffle(wrongs)
        return _labelled(
            stem=f"สายใยอาหารใน{web.habitat}:\n{_web_text(web)}\n"
                 f"ถ้า{lost}หายไปจากพื้นที่นี้ทั้งหมด สิ่งมีชีวิตใดได้รับผลกระทบรุนแรงที่สุด",
            correct=f"{answer} เพราะกิน{lost}เป็นอาหารเพียงอย่างเดียวในสายใยนี้",
            wrongs=tuple(f"{name} เพราะกิน{lost}เป็นอาหารเพียงอย่างเดียวในสายใยนี้"
                         for name in wrongs[:3]),
            hint="หาสิ่งมีชีวิตที่มีอาหารเพียงชนิดเดียว แล้วดูว่าอาหารชนิดนั้น"
                 "คือสิ่งที่หายไปหรือไม่",
        )

    def _alternative_food(self, web: FoodWeb, rng: Random) -> GeneratedQuestion:
        """A consumer with two foods loses one — the point of a web over a chain."""
        candidates = [name for name, prey in web.eats.items() if len(prey) >= 2]
        eater = rng.choice(candidates)
        prey = list(web.eats[eater])
        rng.shuffle(prey)
        lost, kept = prey[0], prey[1]
        return _labelled(
            stem=f"สายใยอาหารใน{web.habitat}:\n{_web_text(web)}\n"
                 f"ถ้า{lost}ลดจำนวนลงมาก {eater}น่าจะเป็นอย่างไร",
            correct=f"ยังอยู่ได้ เพราะยังกิน{kept}ได้อีกทางหนึ่ง แต่จะกิน{kept}มากขึ้น",
            wrongs=(
                f"หายไปทันทีทั้งหมด เพราะ{lost}เป็นอาหารเพียงอย่างเดียวของ{eater}",
                f"เพิ่มจำนวนขึ้น เพราะเมื่อ{lost}น้อยลงก็มีคู่แข่งน้อยลง",
                f"ไม่เปลี่ยนแปลงเลย เพราะ{eater}ไม่ได้กิน{lost}อยู่แล้ว",
            ),
            hint="ดูว่าสิ่งมีชีวิตนั้นมีอาหารกี่ชนิดในสายใยนี้ "
                 "ถ้ามีมากกว่าหนึ่งชนิดก็ยังมีทางเลือก",
        )

    def _paths(self, web: FoodWeb, rng: Random) -> GeneratedQuestion:
        """How many routes the energy can take — a web has more than one."""
        candidates = [name for name in web.eats if len(chains_to(web, name)) >= 2]
        if not candidates:
            return self._alternative_food(web, rng)
        target = rng.choice(candidates)
        count = len(chains_to(web, target))
        return _labelled(
            stem=f"สายใยอาหารใน{web.habitat}:\n{_web_text(web)}\n"
                 f"พลังงานจาก{web.producer}ถ่ายทอดไปถึง{target}ได้กี่เส้นทาง",
            correct=f"{count} เส้นทาง",
            wrongs=tuple(f"{number} เส้นทาง" for number in
                         (count + 1, count - 1, count + 2) if number >= 1)[:3],
            hint="ไล่จากผู้ผลิตขึ้นไปทีละขั้น แล้วนับทุกเส้นทางที่ไปจบที่สิ่งมีชีวิตนั้น",
        )
