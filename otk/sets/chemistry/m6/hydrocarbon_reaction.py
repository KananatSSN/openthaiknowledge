"""ประเภทและปฏิกิริยาของสารประกอบไฮโดรคาร์บอน

เคมี · ม.6 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.6/7

Sets moved here from: science_wave_f28.
"""

from __future__ import annotations

from fractions import Fraction
from math import gcd
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f27 import ALKANE, ALKENE, ALKYNE, COMPOUNDS, atoms_of
from otk.sets._support.science_wave_f28 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_HYDRO = "ประเภทและปฏิกิริยาของสารประกอบไฮโดรคาร์บอน"


SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


AROMATIC = "อะโรมาติกไฮโดรคาร์บอน"


def formula(atoms: dict[str, int]) -> str:
    order = ["C", "H"] + sorted(k for k in atoms if k not in ("C", "H"))
    return "".join(k + (str(atoms[k]).translate(SUB) if atoms[k] > 1 else "") for k in order if atoms.get(k))


HYDROCARBONS = tuple((c[0], c[1], c[2]) for c in COMPOUNDS if c[2] in (ALKANE, ALKENE, ALKYNE)) + (
    # Toluene is left out: hot KMnO₄ oxidises its side chain, so "no change" would be disputable.
    ("เบนซีน", "C₆H₆", AROMATIC),
)


# class: (with Br₂ in the dark, with Br₂ in light, with KMnO₄)
TESTS = {
    ALKANE: ("ไม่เปลี่ยนแปลง สีน้ำตาลแดงของ Br₂ ยังคงอยู่", "สีของ Br₂ จางลงช้า ๆ และเกิดแก๊ส HBr",
             "ไม่เปลี่ยนแปลง สีม่วงยังคงอยู่"),
    ALKENE: ("สีน้ำตาลแดงของ Br₂ จางหายทันที", "สีน้ำตาลแดงของ Br₂ จางหายทันที",
             "สีม่วงจางหาย และเกิดตะกอนสีน้ำตาล (MnO₂)"),
    ALKYNE: ("สีน้ำตาลแดงของ Br₂ จางหายทันที", "สีน้ำตาลแดงของ Br₂ จางหายทันที",
             "สีม่วงจางหาย และเกิดตะกอนสีน้ำตาล (MnO₂)"),
    AROMATIC: ("ไม่เปลี่ยนแปลง สีน้ำตาลแดงของ Br₂ ยังคงอยู่", "ไม่เปลี่ยนแปลง สีน้ำตาลแดงของ Br₂ ยังคงอยู่",
               "ไม่เปลี่ยนแปลง สีม่วงยังคงอยู่"),
}


CLASS_LABELS = (ALKANE, ALKENE, ALKYNE, AROMATIC)


def combustion(atoms: dict[str, int]) -> tuple[int, int, int, int]:
    """Smallest whole numbers for CxHy + O₂ → CO₂ + H₂O."""
    x, y = atoms["C"], atoms["H"]
    # fuel CxHy : O₂ : CO₂ : H₂O = 1 : x + y/4 : x : y/2, scaled by 4 then reduced.
    fuel, oxygen, co2, water = 4, 4 * x + y, 4 * x, 2 * y
    k = gcd(gcd(fuel, oxygen), gcd(co2, water))
    return fuel // k, oxygen // k, co2 // k, water // k


@question_type(
    "chem.hydrocarbon_reaction_foundation",
    display_name={"th": "ระบุประเภทไฮโดรคาร์บอนจากผลการทดสอบ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_HYDRO,
)
class HydrocarbonReactionFoundation(QuestionType):
    """Unsaturated compounds decolourise Br₂ and KMnO₄; alkanes and benzene do not."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = ("แอลคีนและแอลไคน์ฟอกจางสี Br₂ ได้ทันทีในที่มืดและทำให้สีม่วงของ KMnO₄ จางพร้อมเกิดตะกอนสีน้ำตาล "
                "แอลเคนทำปฏิกิริยากับ Br₂ เฉพาะในที่สว่างและให้ HBr ส่วนเบนซีนไม่ฟอกจางสีทั้งสองอย่าง")
        kind = rng.randrange(3)
        if kind == 0:
            name, condensed, cls = rng.choice(HYDROCARBONS)
            test, index = rng.choice((("เมื่อเติมสารละลาย Br₂ ในที่มืด", 0), ("เมื่อเติมสารละลาย Br₂ ในที่สว่าง", 1),
                                      ("เมื่อเติมสารละลาย KMnO₄", 2)))
            right = TESTS[cls][index]
            pool = sorted({t[i] for t in TESTS.values() for i in range(3)} - {right})
            return _labelled(stem=f"{name} ({condensed}) {test} จะสังเกตเห็นอะไร", correct=right,
                             wrongs=tuple(pool), topic=TOPIC_HYDRO, hint=hint)
        if kind == 1:
            cls = rng.choice(CLASS_LABELS)
            dark, light, mn = TESTS[cls]
            unsaturated = cls in (ALKENE, ALKYNE)
            answer = "แอลคีนหรือแอลไคน์" if unsaturated else cls
            options = ("แอลคีนหรือแอลไคน์", ALKANE, AROMATIC, "แอลกอฮอล์")
            return _labelled(stem=f"ไฮโดรคาร์บอน X: เติม Br₂ ในที่มืด {dark} เติม Br₂ ในที่สว่าง {light} "
                                  f"เติม KMnO₄ {mn} X น่าจะเป็นสารประเภทใด",
                             correct=answer, wrongs=tuple(o for o in options if o != answer), topic=TOPIC_HYDRO,
                             hint=hint)
        name, condensed, cls = rng.choice(HYDROCARBONS)
        answer = "ไฮโดรคาร์บอนอิ่มตัว" if cls == ALKANE else AROMATIC if cls == AROMATIC else "ไฮโดรคาร์บอนไม่อิ่มตัว"
        return _labelled(stem=f"{name} ({condensed}) จัดเป็นไฮโดรคาร์บอนประเภทใด", correct=answer,
                         wrongs=tuple(o for o in ("ไฮโดรคาร์บอนอิ่มตัว", "ไฮโดรคาร์บอนไม่อิ่มตัว", AROMATIC,
                                                  "ไม่ใช่ไฮโดรคาร์บอน") if o != answer),
                         topic=TOPIC_HYDRO, hint="อิ่มตัว = มีแต่พันธะเดี่ยว ไม่อิ่มตัว = มี C=C หรือ C≡C อะโรมาติก = มีวงเบนซีน")


@question_type(
    "chem.hydrocarbon_reaction_fluency",
    display_name={"th": "ดุลสมการและคำนวณปฏิกิริยาการเผาไหม้ของไฮโดรคาร์บอน"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_HYDRO,
)
class HydrocarbonReactionFluency(QuestionType):
    """CxHy + (x + y/4) O₂ → x CO₂ + (y/2) H₂O, cleared to whole numbers."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, condensed, _ = rng.choice(HYDROCARBONS)
        atoms = atoms_of(condensed)
        fuel, oxygen, co2, water = combustion(atoms)
        f = formula(atoms)
        hint = "ดุล C ด้วย CO₂ ดุล H ด้วย H₂O แล้วดุล O ด้วย O₂ ถ้าได้เศษส่วนให้คูณทั้งสมการ"
        kind = rng.randrange(3)
        if kind == 0:
            return numeric(stem=f"เมื่อดุลสมการการเผาไหม้สมบูรณ์ของ {name} ({f}) ด้วยเลขจำนวนเต็มน้อยที่สุด "
                                f"__{f} + __O₂ → __CO₂ + __H₂O สัมประสิทธิ์ของ O₂ เท่าใด",
                           answer=oxygen, wrongs=[oxygen + fuel, co2 + water, oxygen * 2], unit="", topic=TOPIC_HYDRO,
                           hint=hint)
        moles = rng.choice((Fraction(1, 2), 1, Fraction(3, 2), 2, 3, 4, 5))
        if kind == 1:
            product, per, mass = rng.choice((("CO₂", Fraction(co2, fuel), 44), ("H₂O", Fraction(water, fuel), 18)))
            return numeric(stem=f"เผา {name} ({f}) {show(moles)} โมลอย่างสมบูรณ์ จะได้ {product} กี่กรัม "
                                f"(มวลโมเลกุล {product} = {mass})",
                           answer=moles * per * mass, wrongs=[moles * mass, moles * per, moles * per * mass * 2],
                           unit="กรัม", topic=TOPIC_HYDRO, hint="โมลผลิตภัณฑ์ = โมลเชื้อเพลิง × อัตราส่วนในสมการ แล้วคูณมวลโมเลกุล")
        return numeric(stem=f"เผา {name} ({f}) {show(moles)} โมลอย่างสมบูรณ์ ต้องใช้แก๊สออกซิเจนกี่โมล",
                       answer=moles * Fraction(oxygen, fuel), wrongs=[moles * oxygen, moles * Fraction(co2, fuel),
                                                                      moles * 2],
                       unit="โมล", topic=TOPIC_HYDRO, hint="O₂ ที่ใช้ต่อโมลเชื้อเพลิง = x + y/4 สำหรับ CxHy")


@question_type(
    "chem.hydrocarbon_reaction_application",
    display_name={"th": "ผลิตภัณฑ์ของไฮโดรคาร์บอนกับโบรมีนและเปอร์แมงกาเนต"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_HYDRO,
)
class HydrocarbonReactionApplication(QuestionType):
    """Addition across C=C or C≡C, substitution on an alkane in light, a diol from KMnO₄."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, condensed, cls = rng.choice([h for h in HYDROCARBONS if h[2] != AROMATIC])
        atoms = atoms_of(condensed)
        c, h = atoms["C"], atoms["H"]
        if rng.random() < 0.35:
            moles = rng.choice((1, 2, 3, Fraction(1, 2), Fraction(3, 2)))
            per = {ALKANE: 0, ALKENE: 1, ALKYNE: 2}[cls]
            if per == 0:
                return self.build(rng)
            return numeric(stem=f"{name} ({condensed}) {show(moles)} โมล ทำปฏิกิริยาพอดีกับ Br₂ ในที่มืดได้มากที่สุดกี่โมล",
                           answer=moles * per, wrongs=[moles * (3 - per), moles * 4, moles + 1], unit="โมล",
                           topic=TOPIC_HYDRO, hint="พันธะคู่หนึ่งพันธะรับ Br₂ ได้ 1 โมเลกุล พันธะสามรับได้ 2 โมเลกุล")
        if cls == ALKANE:
            right = f"{formula({'C': c, 'H': h - 1, 'Br': 1})} และ HBr"
            wrongs = (formula({"C": c, "H": h, "Br": 2}), f"{formula({'C': c, 'H': h - 2, 'Br': 2})} และ H₂",
                      "ไม่เกิดปฏิกิริยา")
            test = "Br₂ ในที่สว่าง"
        elif rng.random() < 0.5:
            right = formula({"C": c, "H": h, "Br": 2})
            wrongs = (f"{formula({'C': c, 'H': h - 1, 'Br': 1})} และ HBr", formula({"C": c, "H": h + 2, "Br": 2}),
                      "ไม่เกิดปฏิกิริยา")
            test = "Br₂ 1 โมล ในที่มืด"
        else:
            right = formula({"C": c, "H": h + 2 if cls == ALKENE else h, "O": 2})
            wrongs = (formula({"C": c, "H": h, "O": 1}), formula({"C": c, "H": h + 4, "O": 2}), "ไม่เกิดปฏิกิริยา")
            test = "สารละลาย KMnO₄ (ผลิตภัณฑ์อินทรีย์ที่มีหมู่ -OH สองหมู่)" if cls == ALKENE else \
                "สารละลาย KMnO₄ (ผลิตภัณฑ์อินทรีย์)"
            if cls == ALKYNE:
                return self.build(rng)
        return _labelled(stem=f"{name} ({condensed}) ทำปฏิกิริยากับ {test} ได้ผลิตภัณฑ์ใด", correct=right,
                         wrongs=wrongs, topic=TOPIC_HYDRO,
                         hint="แอลคีน: Br₂ เข้าไปที่ C=C (การเติม) แอลเคน: Br แทนที่ H หนึ่งอะตอมและได้ HBr (การแทนที่) "
                              "แอลคีนกับ KMnO₄ ได้แอลกอฮอล์ที่มี -OH สองหมู่")
