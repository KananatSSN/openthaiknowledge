"""สมบัติของสารประกอบไอออนิก

เคมี · ม.4 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.4/12

Sets moved here from: science_wave_f21.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f21 import SUBJECT, UPPER_FOUR, _pairs, formula, name

PROVENANCE = Provenance("original")


TOPIC_PROPERTY = "สมบัติของสารประกอบไอออนิก"


PROPERTY_FACTS = (
    ("สารประกอบไอออนิกมีจุดหลอมเหลวสูง เพราะเหตุใด", "แรงยึดเหนี่ยวระหว่างไอออนบวกและไอออนลบในผลึกแข็งแรงมาก",
     ("โมเลกุลมีขนาดใหญ่และมีมวลมาก", "มีพันธะไฮโดรเจนระหว่างโมเลกุลจำนวนมากและแข็งแรง", "อิเล็กตรอนเคลื่อนที่อิสระทั่วทั้งผลึก")),
    ("ผลึกสารประกอบไอออนิกเปราะ แตกง่ายเมื่อถูกทุบ เพราะเหตุใด", "ชั้นไอออนเลื่อน ไอออนประจุเดียวกันมาอยู่ตรงกันจึงผลักกัน",
     ("พันธะไอออนิกอ่อนมาก ผลึกจึงแตกออกเมื่อถูกทุบเพียงเบา ๆ", "ผลึกมีน้ำอยู่ภายใน จึงแตกง่ายเมื่อแห้ง", "อิเล็กตรอนอิสระหลุดออกจากผลึกเมื่อถูกทุบ")),
    ("สารประกอบไอออนิกนำไฟฟ้าได้เมื่อใด", "เมื่อหลอมเหลวหรือละลายน้ำ เพราะไอออนเคลื่อนที่ได้",
     ("เมื่อเป็นของแข็ง เพราะมีอิเล็กตรอนอิสระ", "ไม่นำไฟฟ้าในทุกสถานะ", "เฉพาะเมื่อเป็นแก๊ส")),
    ("เมื่อสารประกอบไอออนิกละลายน้ำ เกิดอะไรขึ้น", "ไอออนแยกออกจากกันและถูกโมเลกุลน้ำล้อมรอบ",
     ("โมเลกุลของสารแตกเป็นอะตอมที่เป็นกลาง", "เกิดพันธะโคเวเลนต์กับน้ำจนเป็นสารใหม่", "ไอออนรวมกันเป็นโมเลกุลใหม่กับน้ำ")),
)


STATES = (("ของแข็ง", False), ("หลอมเหลว", True), ("สารละลายในน้ำ", True))


# Compounds for comparing lattice strength: (formula, cation charge, anion charge, sum of ionic radii in pm).
LATTICE = (("NaF", 1, 1, 235), ("NaCl", 1, 1, 283), ("NaBr", 1, 1, 298), ("NaI", 1, 1, 322), ("KF", 1, 1, 271),
           ("KCl", 1, 1, 319), ("KBr", 1, 1, 334), ("MgO", 2, 2, 212), ("CaO", 2, 2, 240), ("BaO", 2, 2, 275),
           ("MgF₂", 2, 1, 205), ("CaF₂", 2, 1, 233), ("LiF", 1, 1, 209))


def _stronger(a, b) -> bool | None:
    """True if a has the stronger lattice: ion charges decide first, then the smaller ions."""
    qa, qb = a[1] * a[2], b[1] * b[2]
    if qa != qb:
        return qa > qb
    if a[3] == b[3]:
        return None
    return a[3] < b[3]


@question_type(
    "chem.ionic_property_foundation",
    display_name={"th": "จุดหลอมเหลว ความเปราะ และการนำไฟฟ้าของสารประกอบไอออนิก"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_PROPERTY,
)
class IonicPropertyFoundation(QuestionType):
    """Why ionic solids are hard, brittle and conduct only when their ions can move."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            stem, correct, wrongs = rng.choice(PROPERTY_FACTS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs, topic=TOPIC_PROPERTY,
                             hint="ไอออนในผลึกยึดกันแน่นแต่อยู่กับที่ ต้องหลอมเหลวหรือละลายน้ำไอออนจึงเคลื่อนที่นำไฟฟ้าได้")
        cation, anion = rng.choice([p for p in _pairs() if p[1][0] in ("Cl", "Br", "I", "NO₃", "SO₄") and p[0][0] in ("Na", "K", "Mg", "Ca", "Zn", "Cu")])
        state, conducts = rng.choice(STATES)
        return _labelled(stem=f"{name(cation, anion)} ({formula(cation, anion)}) ในสถานะ{state} นำไฟฟ้าได้หรือไม่",
                         correct="นำไฟฟ้าได้ เพราะไอออนเคลื่อนที่ได้" if conducts else "ไม่นำไฟฟ้า เพราะไอออนอยู่กับที่ในโครงผลึก",
                         wrongs=("ไม่นำไฟฟ้า เพราะไอออนอยู่กับที่ในโครงผลึก" if conducts else "นำไฟฟ้าได้ เพราะไอออนเคลื่อนที่ได้",
                                 "นำไฟฟ้าได้ เพราะมีอิเล็กตรอนอิสระ", "ไม่นำไฟฟ้า เพราะไม่มีไอออนอยู่ในผลึกเลย"),
                         topic=TOPIC_PROPERTY, hint="ไอออนต้องเคลื่อนที่ได้จึงนำไฟฟ้า: หลอมเหลวหรือละลายน้ำนำไฟฟ้า ของแข็งไม่นำ")


@question_type(
    "chem.ionic_property_fluency",
    display_name={"th": "เปรียบเทียบจุดหลอมเหลวของสารประกอบไอออนิกจากประจุและขนาดไอออน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_PROPERTY,
)
class IonicPropertyFluency(QuestionType):
    """Higher charges and smaller ions pull harder, so the lattice melts higher."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        a, b = rng.choice([(x, y) for x in LATTICE for y in LATTICE if x != y and _stronger(x, y) is not None])
        winner, loser = (a, b) if _stronger(a, b) else (b, a)
        return _labelled(
            stem=(f"{a[0]} (ประจุไอออน {a[1]}+ และ {a[2]}−, ผลรวมรัศมีไอออน {a[3]} pm) กับ {b[0]} (ประจุไอออน {b[1]}+ และ "
                  f"{b[2]}−, ผลรวมรัศมีไอออน {b[3]} pm) สารใดมีจุดหลอมเหลวสูงกว่า"),
            correct=winner[0], wrongs=(loser[0], "เท่ากัน", "บอกไม่ได้"), topic=TOPIC_PROPERTY,
            hint="ประจุมากและไอออนเล็ก แรงดึงดูดในผลึกยิ่งมาก จุดหลอมเหลวยิ่งสูง (ดูประจุก่อน แล้วจึงดูขนาด)")


@question_type(
    "chem.ionic_property_application",
    display_name={"th": "เรียงลำดับจุดหลอมเหลวและใช้สมบัติของสารประกอบไอออนิก"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_PROPERTY,
)
class IonicPropertyApplication(QuestionType):
    """Order a halide series by melting point, or pick the compound that fits a use."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            groups = (("NaF", "NaCl", "NaBr", "NaI"), ("KF", "KCl", "KBr"), ("MgO", "CaO", "BaO"), ("LiF", "NaF", "KF"))
            wanted = rng.choice(groups)
            series = [x for x in LATTICE if x[0] in wanted]
            three = rng.sample(series, 3)
            ordered = sorted(three, key=lambda t: t[3])
            right = " > ".join(t[0] for t in ordered)
            wrongs = set()
            while len(wrongs) < 3:
                shuffled = three[:]
                rng.shuffle(shuffled)
                text = " > ".join(t[0] for t in shuffled)
                if text != right:
                    wrongs.add(text)
            return _labelled(stem=f"เรียงลำดับจุดหลอมเหลวของ {' '.join(f'{t[0]} ({t[3]} pm)' for t in three)} จากมากไปน้อย (ตัวเลขคือผลรวมรัศมีไอออน)",
                             correct=right, wrongs=tuple(sorted(wrongs)), topic=TOPIC_PROPERTY,
                             hint="ประจุเท่ากัน ไอออนยิ่งเล็ก แรงยึดเหนี่ยวยิ่งมาก จุดหลอมเหลวยิ่งสูง")
        uses = (("ใช้บุเตาหลอมโลหะ เพราะทนความร้อนสูงมาก", "MgO"), ("ใช้เป็นเกลือปรุงอาหาร", "NaCl"),
                ("ใช้ในยาสีฟันป้องกันฟันผุ", "NaF"), ("ใช้ทำปูนขาวปรับสภาพดินกรด", "CaO"))
        use, right = rng.choice(uses)
        return _labelled(stem=f"สารประกอบไอออนิกใดเหมาะที่จะ{use}", correct=right,
                         wrongs=tuple(u for _, u in uses if u != right), topic=TOPIC_PROPERTY,
                         hint="เลือกจากสมบัติ: จุดหลอมเหลวสูง ความปลอดภัยในการบริโภค หรือไอออนที่มีประโยชน์")
