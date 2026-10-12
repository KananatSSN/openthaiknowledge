"""ไดโคโทมัสคีย์

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 2 ม.6/5

Sets moved here from: science_wave_f53.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f53 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_KEY = "ไดโคโทมัสคีย์"


ANIMAL_TRAITS = ("มีกระดูกสันหลัง", "มีขนเป็นเส้น", "มีขนนก", "มีครีบ", "มีขาเป็นข้อปล้อง", "มีปีก", "มีเปลือกแข็งหุ้มตัว")


ANIMALS = {
    "แมว": (1, 1, 0, 0, 0, 0, 0), "ค้างคาว": (1, 1, 0, 0, 0, 1, 0), "นกพิราบ": (1, 0, 1, 0, 0, 1, 0), "ปลาทู": (1, 0, 0, 1, 0, 0, 0),
    "กบ": (1, 0, 0, 0, 0, 0, 0), "ผีเสื้อ": (0, 0, 0, 0, 1, 1, 0), "แมงมุม": (0, 0, 0, 0, 1, 0, 0), "ไส้เดือนดิน": (0, 0, 0, 0, 0, 0, 0),
    "หอยทาก": (0, 0, 0, 0, 0, 0, 1), "ปู": (0, 0, 0, 0, 1, 0, 1),
}


PLANT_TRAITS = ("มีท่อลำเลียง", "มีเมล็ด", "มีดอก", "มีใบเลี้ยงเดี่ยว", "เป็นไม้ยืนต้น")


PLANTS = {
    "มอส": (0, 0, 0, 0, 0), "เฟิร์น": (1, 0, 0, 0, 0), "สน": (1, 1, 0, 0, 1), "ข้าว": (1, 1, 1, 1, 0), "มะพร้าว": (1, 1, 1, 1, 1),
    "มะม่วง": (1, 1, 1, 0, 1), "ถั่วเขียว": (1, 1, 1, 0, 0),
}


KEY_HINT = "เริ่มที่ข้อ 1 เลือกข้อความที่ตรงกับลักษณะของสิ่งมีชีวิตทีละคู่ แล้วไปตามข้อที่ระบุจนได้ชื่อ"


def not_trait(trait: str) -> str:
    return "ไม่" + trait


def build_key(rng: Random, table: dict, traits: tuple[str, ...], names: list[str]):
    """Couplets as (number, trait, yes-target, no-target) and each name's path."""
    couplets, paths = [], {}

    def split(group: list[str], path: list[str]) -> str:
        if len(group) == 1:
            paths[group[0]] = path
            return group[0]
        options = []
        for t in range(len(traits)):
            yes = [n for n in group if table[n][t]]
            if yes and len(yes) < len(group):
                options.append((abs(2 * len(yes) - len(group)), t, yes))
        best = min(o[0] for o in options)
        _, t, yes = rng.choice([o for o in options if o[0] == best])
        no = [n for n in group if n not in yes]
        number = len(couplets) + 1
        slot = [number, traits[t], None, None]
        couplets.append(slot)
        slot[2] = split(yes, path + [f"{number}ก"])
        slot[3] = split(no, path + [f"{number}ข"])
        return f"ข้อ {number}"

    split(names, [])
    return couplets, paths


def key_text(couplets) -> str:
    def target(t: str) -> str:
        return f"ไปข้อ {t.split()[1]}" if t.startswith("ข้อ ") else f"คือ{t}"
    return " ".join(f"{n}ก {trait} {target(yes)} / {n}ข {not_trait(trait)} {target(no)}" for n, trait, yes, no in couplets)


def random_key(rng: Random):
    if rng.random() < 0.6:
        table, traits = ANIMALS, ANIMAL_TRAITS
    else:
        table, traits = PLANTS, PLANT_TRAITS
    names = rng.sample(sorted(table), rng.randint(4, 5))
    couplets, paths = build_key(rng, table, traits, names)
    return table, traits, names, couplets, paths


@question_type(
    "biology.dichotomous_key_foundation",
    display_name={"th": "หลักการของไดโคโทมัสคีย์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_KEY,
)
class DichotomousKeyFoundation(QuestionType):
    """Two contrasting statements a step; n organisms need n - 1 couplets."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.45:
            n = rng.randint(3, 30)
            return numeric(stem=f"ไดโคโทมัสคีย์ที่ใช้ระบุสิ่งมีชีวิต {n} ชนิดให้แยกออกจากกันทั้งหมด ต้องมีข้อความเป็นคู่อย่างน้อยกี่คู่",
                           answer=n - 1, wrongs=[n, 2 * n, n // 2 + 1], unit="คู่", topic=TOPIC_KEY,
                           hint="แต่ละคู่แยกกลุ่มออกเป็น 2 กลุ่ม ครั้งหนึ่งเพิ่มจำนวนกลุ่มได้ 1 กลุ่ม จึงต้องใช้ n − 1 คู่")
        facts = (
            ("ไดโคโทมัสคีย์แต่ละข้อประกอบด้วยข้อความลักษณะใด", "ข้อความ 2 ข้อความที่มีลักษณะตรงข้ามกัน",
             ("ข้อความ 3 ข้อความที่เลือกได้หลายข้อ", "ข้อความเดียวที่บอกชื่อสิ่งมีชีวิต", "ข้อความที่มีลักษณะเหมือนกัน", "รูปภาพของสิ่งมีชีวิตเท่านั้น")),
            ("ลักษณะใดเหมาะที่จะใช้สร้างไดโคโทมัสคีย์มากที่สุด", "ลักษณะที่สังเกตได้ชัดเจนและไม่เปลี่ยนตามสภาพแวดล้อม",
             ("ขนาดตัวที่เปลี่ยนตามอายุ", "สีที่เปลี่ยนตามฤดูกาล", "ความชอบของผู้สังเกต", "จำนวนตัวที่พบในวันสำรวจ")),
            ("ข้อความใดเป็นคู่ที่เหมาะสมในไดโคโทมัสคีย์", "มีกระดูกสันหลัง / ไม่มีกระดูกสันหลัง",
             ("มีกระดูกสันหลัง / มีขนเป็นเส้น", "ตัวใหญ่ / ตัวสวย", "มีปีก / มีปีกสีสวย", "อาศัยในน้ำ / มีครีบ")),
        )
        stem, right, wrongs = rng.choice(facts)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_KEY, hint=KEY_HINT)


@question_type(
    "biology.dichotomous_key_fluency",
    display_name={"th": "ใช้ไดโคโทมัสคีย์ระบุสิ่งมีชีวิต"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_KEY,
)
class DichotomousKeyFluency(QuestionType):
    """Walk the key with the traits given."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        table, traits, names, couplets, paths = random_key(rng)
        target = rng.choice(names)
        described = []
        for step in paths[target]:
            number = int(step[:-1])
            trait = couplets[number - 1][1]
            described.append(trait if step.endswith("ก") else not_trait(trait))
        return _labelled(stem=f"จากไดโคโทมัสคีย์ต่อไปนี้ {key_text(couplets)} สิ่งมีชีวิตที่{' และ'.join(described)} คือข้อใด",
                         correct=target, wrongs=tuple([n for n in names if n != target]), topic=TOPIC_KEY, hint=KEY_HINT)


@question_type(
    "biology.dichotomous_key_application",
    display_name={"th": "หาเส้นทางในไดโคโทมัสคีย์ของสิ่งมีชีวิตที่กำหนด"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_KEY,
)
class DichotomousKeyApplication(QuestionType):
    """Given the organism, the reader must know its traits and trace the route."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        table, traits, names, couplets, paths = random_key(rng)
        target = rng.choice(names)
        routes = {n: " → ".join(p) for n, p in paths.items()}
        wrongs = [routes[n] for n in names if n != target and routes[n] != routes[target]]
        return _labelled(stem=f"จากไดโคโทมัสคีย์ต่อไปนี้ {key_text(couplets)} การระบุ{target}ต้องผ่านข้อความตามลำดับใด",
                         correct=routes[target], wrongs=tuple(wrongs), topic=TOPIC_KEY, hint=KEY_HINT)
