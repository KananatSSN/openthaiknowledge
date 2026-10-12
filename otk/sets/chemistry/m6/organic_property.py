"""จุดเดือดและการละลายน้ำของสารประกอบอินทรีย์

เคมี · ม.6 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.6/6

Sets moved here from: science_wave_f27.
"""

from __future__ import annotations

from itertools import combinations, permutations
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, show
from otk.sets._support.science_wave_f27 import (
    ACID,
    ALCOHOL,
    ALDEHYDE,
    ALKANE,
    AMIDE,
    AMINE,
    COMPOUNDS,
    ESTER,
    ETHER,
    KETONE,
    SUBJECT,
    UPPER_SIX,
    atoms_of,
    carbons,
    molecular,
)

PROVENANCE = Provenance("original")


TOPIC_PROPERTY = "จุดเดือดและการละลายน้ำของสารประกอบอินทรีย์"


MASS = {"C": 12, "H": 1, "O": 16, "N": 14, "Cl": 35.5}


def molar_mass(condensed: str):
    total = sum(MASS[k] * v for k, v in atoms_of(condensed).items())
    return int(total) if total == int(total) else total


# Rough strength of the forces between molecules, by class, for molecules of similar mass.
CLASS_RANK = {ALKANE: 0, ETHER: 1, ALDEHYDE: 2, KETONE: 2, ESTER: 2, AMINE: 3, ALCOHOL: 4, ACID: 5, AMIDE: 6}


WITH_BP = tuple(c for c in COMPOUNDS if c[4] is not None and c[2] in CLASS_RANK)


def higher_boiling(a, b):
    """The textbook's pick, or None where no rule decides or the data disagree.

    Same class, both straight: more carbons boils higher. Same formula, same
    class: the straight chain boils higher than the branched one. Different
    class and molar masses within 4: the class with stronger forces.
    """
    if a[2] == b[2] and a[3] and b[3] and carbons(a) != carbons(b):
        pick = a if carbons(a) > carbons(b) else b
    elif a[2] == b[2] and molecular(a[1]) == molecular(b[1]) and a[3] != b[3]:
        pick = a if a[3] else b
    elif (CLASS_RANK[a[2]] != CLASS_RANK[b[2]]
          and abs(molar_mass(a[1]) - molar_mass(b[1])) <= 4):
        pick = a if CLASS_RANK[a[2]] > CLASS_RANK[b[2]] else b
    else:
        return None
    other = b if pick is a else a
    return pick if pick[4] > other[4] else None


BP_PAIRS = tuple((a, b) for a, b in combinations(WITH_BP, 2) if higher_boiling(a, b))


BP_TRIPLES = tuple(t for t in combinations(WITH_BP, 3) if all(higher_boiling(a, b) for a, b in combinations(t, 2)))


# Classes whose short members dissolve in water: fewer carbons, better.
SOLUBLE_SERIES = (ALCOHOL, ACID, ALDEHYDE, KETONE, AMIDE, AMINE)


PROPERTY_FACTS = (
    ("เมื่อจำนวนคาร์บอนในโมเลกุลแอลกอฮอล์เพิ่มขึ้น การละลายน้ำเป็นอย่างไร",
     "ลดลง เพราะส่วนไฮโดรคาร์บอนที่ไม่มีขั้วมีขนาดใหญ่ขึ้น",
     ("เพิ่มขึ้น เพราะเกิดพันธะไฮโดรเจนได้มากขึ้น", "ไม่เปลี่ยน เพราะมีหมู่ -OH หมู่เดียวเท่าเดิม",
      "เพิ่มขึ้น เพราะมวลโมเลกุลมากขึ้นจึงละลายได้มากขึ้น")),
    ("เมื่อจำนวนคาร์บอนในแอลเคนสายตรงเพิ่มขึ้น จุดเดือดเป็นอย่างไร",
     "สูงขึ้น เพราะแรงแผ่กระจายลอนดอนเพิ่มขึ้นตามขนาดโมเลกุล",
     ("ต่ำลง เพราะโมเลกุลใหญ่เคลื่อนที่ช้าและชนกันน้อยลง", "ไม่เปลี่ยน เพราะไม่มีขั้วเหมือนเดิมทุกโมเลกุลในอนุกรม",
      "สูงขึ้น เพราะเกิดพันธะไฮโดรเจนมากขึ้น")),
    ("แอลเคนที่มีกิ่งมีจุดเดือดต่ำกว่าไอโซเมอร์สายตรงเพราะเหตุใด",
     "โมเลกุลที่มีกิ่งมีรูปร่างกะทัดรัด พื้นที่ผิวสัมผัสน้อย แรงลอนดอนจึงน้อยกว่า",
     ("โมเลกุลที่มีกิ่งมีมวลโมเลกุลน้อยกว่าไอโซเมอร์สายตรงที่มีจำนวนคาร์บอนเท่ากัน", "โมเลกุลที่มีกิ่งมีพันธะโคเวเลนต์น้อยกว่า",
      "โมเลกุลที่มีกิ่งมีขั้วมากกว่า จึงเกิดพันธะไฮโดรเจนกับตัวเองได้น้อยลง")),
    ("กรดคาร์บอกซิลิกมีจุดเดือดสูงกว่าแอลกอฮอล์ที่มีมวลโมเลกุลใกล้เคียงกันเพราะเหตุใด",
     "โมเลกุลของกรดเกิดพันธะไฮโดรเจนระหว่างกันได้แข็งแรงกว่า (เกิดเป็นคู่ไดเมอร์)",
     ("โมเลกุลของแอลกอฮอล์เกิดพันธะไฮโดรเจนได้ แต่กรดคาร์บอกซิลิกเกิดไม่ได้", "กรดคาร์บอกซิลิกเป็นสารประกอบไอออนิก จึงมีจุดเดือดสูงกว่าแอลกอฮอล์", "แอลกอฮอล์เป็นโมเลกุลไม่มีขั้ว ระหว่างโมเลกุลจึงมีเพียงแรงลอนดอน")),
    ("แอลเคนไม่ละลายน้ำเพราะเหตุใด", "แอลเคนไม่มีขั้ว จึงดึงดูดกับโมเลกุลน้ำที่มีขั้วได้ไม่ดี",
     ("แอลเคนมีจุดเดือดสูงเกินไป จึงไม่แยกตัวไปผสมกับน้ำ", "แอลเคนทำปฏิกิริยากับน้ำเกิดเป็นสารใหม่ที่ไม่ละลาย", "แอลเคนเกิดพันธะไฮโดรเจนกับตัวเองแข็งแรงมาก")),
    ("อีเทอร์มีจุดเดือดต่ำกว่าแอลกอฮอล์ที่เป็นไอโซเมอร์กันเพราะเหตุใด",
     "อีเทอร์ไม่มี H ต่อกับ O จึงไม่เกิดพันธะไฮโดรเจนระหว่างโมเลกุลของตัวเอง",
     ("อีเทอร์มีมวลโมเลกุลน้อยกว่าแอลกอฮอล์ที่มีจำนวนคาร์บอนเท่ากันมาก", "อีเทอร์ไม่มีขั้วเลย ระหว่างโมเลกุลจึงมีแต่แรงลอนดอน", "อีเทอร์เกิดพันธะไฮโดรเจนระหว่างโมเลกุลได้มากกว่าแอลกอฮอล์")),
)


def _mass_label(c) -> str:
    return f"{c[0]} ({c[1]}, มวลโมเลกุล {show(molar_mass(c[1]))})"


@question_type(
    "chem.organic_property_foundation",
    display_name={"th": "เหตุผลของจุดเดือดและการละลายน้ำของสารประกอบอินทรีย์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_PROPERTY,
)
class OrganicPropertyFoundation(QuestionType):
    """Hydrogen bonding, size and shape explain the trends."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            stem, right, wrongs = rng.choice(PROPERTY_FACTS)
            return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_PROPERTY,
                             hint="จุดเดือดขึ้นกับแรงระหว่างโมเลกุล การละลายน้ำขึ้นกับการเกิดพันธะไฮโดรเจนกับน้ำ")
        cls = rng.choice(SOLUBLE_SERIES)
        series = [c for c in COMPOUNDS if c[2] == cls and c[3]]
        if len({carbons(c) for c in series}) < 2:
            return self.build(rng)
        chosen = rng.sample(series, min(3, len(series)))
        if len({carbons(c) for c in chosen}) < len(chosen):
            return self.build(rng)
        best = min(chosen, key=carbons)
        others = [c for c in chosen if c is not best]
        fillers = [c for c in COMPOUNDS if c[2] == ALKANE and c[3] and c not in others]
        while len(others) < 3:
            others.append(rng.choice([f for f in fillers if f not in others]))
        return _labelled(stem="สารใดละลายน้ำได้ดีที่สุด", correct=f"{best[0]} ({best[1]})",
                         wrongs=tuple(f"{c[0]} ({c[1]})" for c in others), topic=TOPIC_PROPERTY,
                         hint="สารที่มีหมู่มีขั้วซึ่งเกิดพันธะไฮโดรเจนกับน้ำได้ และมีส่วนไฮโดรคาร์บอนสั้นที่สุด ละลายน้ำได้ดีที่สุด")


@question_type(
    "chem.organic_property_fluency",
    display_name={"th": "เปรียบเทียบจุดเดือดของสารประกอบอินทรีย์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_PROPERTY,
)
class OrganicPropertyFluency(QuestionType):
    """Class first for similar masses; size within a series; branching lowers it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        a, b = rng.choice(BP_PAIRS)
        if rng.random() < 0.5:
            a, b = b, a
        right = higher_boiling(a, b)
        other = b if right is a else a
        return _labelled(stem=f"{_mass_label(a)} กับ {_mass_label(b)} สารใดมีจุดเดือดสูงกว่า",
                         correct=right[0], wrongs=(other[0], "มีจุดเดือดเท่ากัน", "บอกไม่ได้จากข้อมูลนี้"),
                         topic=TOPIC_PROPERTY,
                         hint="มวลใกล้กัน: ดูแรงระหว่างโมเลกุล (กรด > แอลกอฮอล์ > แอลดีไฮด์/คีโตน/เอสเทอร์ > อีเทอร์ > แอลเคน) "
                              "ประเภทเดียวกัน: สายยาวกว่าเดือดสูงกว่า และสายตรงเดือดสูงกว่าสายมีกิ่ง")


@question_type(
    "chem.organic_property_application",
    display_name={"th": "เรียงลำดับจุดเดือดของสารประกอบอินทรีย์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_PROPERTY,
)
class OrganicPropertyApplication(QuestionType):
    """Order three compounds by boiling point, or explain a measured pair."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            trio = sorted(rng.choice(BP_TRIPLES), key=lambda c: -c[4])
            shown = rng.sample(trio, 3)
            order = tuple(c[0] for c in trio)
            others = [" > ".join(p) for p in permutations(order) if p != order]
            return _labelled(stem=f"เรียงจุดเดือดของ {', '.join(_mass_label(c) for c in shown)} จากสูงไปต่ำ",
                             correct=" > ".join(order), wrongs=tuple(others), topic=TOPIC_PROPERTY,
                             hint="เทียบทีละคู่: ประเภทสาร (แรงระหว่างโมเลกุล) ความยาวสาย และการมีกิ่ง")
        a, b = rng.choice(BP_PAIRS)
        x = higher_boiling(a, b)
        y = b if x is a else a
        if x[2] == y[2] and x[3] and y[3]:
            right = f"{x[0]} มีสายคาร์บอนยาวกว่า แรงแผ่กระจายลอนดอนจึงมากกว่า"
        elif x[2] == y[2]:
            right = f"{x[0]} เป็นสายตรง มีพื้นที่ผิวสัมผัสมากกว่าไอโซเมอร์ที่มีกิ่ง"
        else:
            right = f"{x[0]} เป็น{x[2]} ซึ่งมีแรงยึดเหนี่ยวระหว่างโมเลกุลแข็งแรงกว่า{y[2]}"
        wrongs = (f"{y[0]} มีแรงยึดเหนี่ยวระหว่างโมเลกุลแข็งแรงกว่า จึงต้องใช้พลังงานมากกว่าในการแยกโมเลกุล",
                  f"พันธะโคเวเลนต์ภายในโมเลกุล {x[0]} แข็งแรงกว่า จึงต้องใช้พลังงานมากกว่าในการสลายพันธะ",
                  f"{x[0]} ไม่มีขั้ว จึงเดือดยากกว่าสารที่มีขั้ว")
        return _labelled(stem=f"{_mass_label(x)} มีจุดเดือด {x[4]} °C สูงกว่า {_mass_label(y)} ที่มีจุดเดือด {y[4]} °C "
                              "เหตุผลที่เหมาะสมที่สุดคือข้อใด",
                         correct=right, wrongs=wrongs, topic=TOPIC_PROPERTY,
                         hint="การเดือดต้องเอาชนะแรงระหว่างโมเลกุล ไม่ได้สลายพันธะภายในโมเลกุล")
