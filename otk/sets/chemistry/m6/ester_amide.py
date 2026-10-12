"""ปฏิกิริยาเอสเทอริฟิเคชัน การสังเคราะห์เอไมด์ ไฮโดรลิซิส และสะปอนนิฟิเคชัน

เคมี · ม.6 · สสวท. เพิ่มเติม
Indicators: เคมีเพิ่มเติม 1 ม.6/8

Sets moved here from: science_wave_f28.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric, show
from otk.sets._support.science_wave_f28 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_ESTER = "ปฏิกิริยาเอสเทอริฟิเคชัน การสังเคราะห์เอไมด์ ไฮโดรลิซิส และสะปอนนิฟิเคชัน"


# (acid name, acyl part as written before COO, root for the -oate name, sodium salt name)
ACIDS = (("กรดเมทาโนอิก", "H", "เมทาโนเอต"), ("กรดเอทาโนอิก", "CH₃", "เอทาโนเอต"),
         ("กรดโพรพาโนอิก", "CH₃CH₂", "โพรพาโนเอต"), ("กรดบิวทาโนอิก", "CH₃(CH₂)₂", "บิวทาโนเอต"))


# (alcohol name, alkyl part, alkyl name)
ALCOHOLS = (("เมทานอล", "CH₃", "เมทิล"), ("เอทานอล", "CH₂CH₃", "เอทิล"), ("โพรพาน-1-ออล", "CH₂CH₂CH₃", "โพรพิล"),
            ("บิวทาน-1-ออล", "(CH₂)₃CH₃", "บิวทิล"))


# (amine name, alkyl part as written after N, N-substituent name, condensed formula)
AMINES = (("เมทานามีน", "CH₃", "N-เมทิล", "CH₃NH₂"), ("เอทานามีน", "CH₂CH₃", "N-เอทิล", "CH₃CH₂NH₂"))


REACTIONS = ("เอสเทอริฟิเคชัน", "การสังเคราะห์เอไมด์", "ไฮโดรลิซิส", "สะปอนนิฟิเคชัน")


def acid_formula(acid) -> str:
    return f"{acid[1]}COOH"


def alcohol_formula(alcohol) -> str:
    return {"CH₃": "CH₃OH", "CH₂CH₃": "CH₃CH₂OH", "CH₂CH₂CH₃": "CH₃CH₂CH₂OH", "(CH₂)₃CH₃": "CH₃(CH₂)₃OH"}[alcohol[1]]


def ester(acid, alcohol) -> tuple[str, str]:
    return f"{alcohol[2]}{acid[2]}", f"{acid[1]}COO{alcohol[1]}"


def amide(acid, amine) -> tuple[str, str]:
    root = acid[2].replace("โนเอต", "นาไมด์")
    return f"{amine[2]}{root}", f"{acid[1]}CONH{amine[1]}"


def salt(acid) -> tuple[str, str]:
    return f"โซเดียม{acid[2]}", f"{acid[1]}COONa"


@question_type(
    "chem.ester_amide_foundation",
    display_name={"th": "ระบุชนิดของปฏิกิริยาจากสมการ"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_ESTER,
)
class EsterAmideFoundation(QuestionType):
    """Acid + alcohol, acid + amine, ester + water, ester + base."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        acid, alcohol, amine = rng.choice(ACIDS), rng.choice(ALCOHOLS), rng.choice(AMINES)
        e_name, e_formula = ester(acid, alcohol)
        kind = rng.choice(REACTIONS)
        if kind == "เอสเทอริฟิเคชัน":
            eq = f"{acid_formula(acid)} + {alcohol_formula(alcohol)} → {e_formula} + H₂O (มี H₂SO₄ เป็นตัวเร่ง)"
        elif kind == "การสังเคราะห์เอไมด์":
            eq = f"{acid_formula(acid)} + {amine[3]} → {amide(acid, amine)[1]} + H₂O"
        elif kind == "ไฮโดรลิซิส":
            eq = f"{e_formula} + H₂O → {acid_formula(acid)} + {alcohol_formula(alcohol)} (มีกรดเป็นตัวเร่ง)"
        else:
            eq = f"{e_formula} + NaOH → {salt(acid)[1]} + {alcohol_formula(alcohol)}"
        return _labelled(stem=f"ปฏิกิริยา {eq} เป็นปฏิกิริยาประเภทใด", correct=kind,
                         wrongs=tuple(r for r in REACTIONS if r != kind), topic=TOPIC_ESTER,
                         hint="กรด + แอลกอฮอล์ → เอสเทอร์ (เอสเทอริฟิเคชัน) กรด + เอมีน → เอไมด์ "
                              "เอสเทอร์ + น้ำ → กรด + แอลกอฮอล์ (ไฮโดรลิซิส) เอสเทอร์ + เบส → เกลือ + แอลกอฮอล์ (สะปอนนิฟิเคชัน)")


@question_type(
    "chem.ester_amide_fluency",
    display_name={"th": "ผลิตภัณฑ์ของเอสเทอริฟิเคชันและไฮโดรลิซิส"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_ESTER,
)
class EsterAmideFluency(QuestionType):
    """Alkyl from the alcohol, -oate from the acid; hydrolysis runs it backwards."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        acid, alcohol = rng.choice(ACIDS), rng.choice(ALCOHOLS)
        e_name, e_formula = ester(acid, alcohol)
        hint = "ชื่อเอสเทอร์ = หมู่แอลคิลจากแอลกอฮอล์ + ชื่อกรดที่เปลี่ยน -โอิก เป็น -โอเอต"
        kind = rng.randrange(3)
        if kind == 0:
            wrongs = {ester(a, b)[0] for a in ACIDS for b in ALCOHOLS} - {e_name}
            swapped = [ester(a, b)[0] for a in ACIDS for b in ALCOHOLS
                       if a[2].startswith(alcohol[2][:3]) and b[2].startswith(acid[2][:3])]
            pool = sorted(wrongs)
            picks = [w for w in swapped if w != e_name][:1]
            picks += rng.sample([w for w in pool if w not in picks], 3 - len(picks))
            return _labelled(stem=f"{acid[0]} ทำปฏิกิริยากับ{alcohol[0]} (มี H₂SO₄ เป็นตัวเร่ง) ได้เอสเทอร์ชื่อใด",
                             correct=e_name, wrongs=tuple(picks), topic=TOPIC_ESTER, hint=hint)
        if kind == 1:
            wrongs = sorted({ester(a, b)[1] for a in ACIDS for b in ALCOHOLS} - {e_formula})
            return _labelled(stem=f"{acid_formula(acid)} + {alcohol_formula(alcohol)} → X + H₂O สาร X มีสูตรโครงสร้างใด",
                             correct=e_formula, wrongs=tuple(wrongs), topic=TOPIC_ESTER, hint=hint)
        right = f"{acid[0]} และ{alcohol[0]}"
        others = [f"{a[0]} และ{b[0]}" for a in ACIDS for b in ALCOHOLS if (a, b) != (acid, alcohol)]
        return _labelled(stem=f"ไฮโดรลิซิส {e_name} ({e_formula}) ด้วยน้ำโดยมีกรดเป็นตัวเร่ง ได้ผลิตภัณฑ์ใด",
                         correct=right, wrongs=tuple(others), topic=TOPIC_ESTER,
                         hint="ไฮโดรลิซิสแยกเอสเทอร์กลับเป็นกรดคาร์บอกซิลิกและแอลกอฮอล์ที่ใช้สร้างเอสเทอร์นั้น")


@question_type(
    "chem.ester_amide_application",
    display_name={"th": "สะปอนนิฟิเคชันและการสังเคราะห์เอไมด์"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_ESTER,
)
class EsterAmideApplication(QuestionType):
    """Soap from fat and NaOH, and amides from acids and amines."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.randrange(3)
        if kind == 0:
            moles = rng.choice([Fraction(n, 4) for n in range(1, 17)])
            if rng.random() < 0.5:
                return numeric(stem=f"ไขมัน (ไตรกลีเซอไรด์) {show(moles)} โมล ทำปฏิกิริยาสะปอนนิฟิเคชันพอดีกับ NaOH กี่กรัม "
                                    "(มวลสูตร NaOH = 40)",
                               answer=moles * 3 * 40, wrongs=[moles * 40, moles * 3, moles * 2 * 40], unit="กรัม",
                               topic=TOPIC_ESTER,
                               hint="ไตรกลีเซอไรด์ 1 โมลมีหมู่เอสเทอร์ 3 หมู่ จึงใช้ NaOH 3 โมล ได้สบู่ 3 โมลและกลีเซอรอล 1 โมล")
            return numeric(stem=f"ไขมัน (ไตรกลีเซอไรด์) {show(moles)} โมล ทำปฏิกิริยาสะปอนนิฟิเคชันกับ NaOH มากเกินพอ "
                                "ได้สบู่ (เกลือโซเดียมของกรดไขมัน) กี่โมล",
                           answer=moles * 3, wrongs=[moles, moles * 2, moles * 3 + 1], unit="โมล", topic=TOPIC_ESTER,
                           hint="ไตรกลีเซอไรด์ 1 โมล + NaOH 3 โมล → สบู่ 3 โมล + กลีเซอรอล 1 โมล")
        acid = rng.choice(ACIDS)
        if kind == 1:
            alcohol = rng.choice(ALCOHOLS)
            e_name, e_formula = ester(acid, alcohol)
            right = f"{salt(acid)[0]} และ{alcohol[0]}"
            others = [f"{salt(a)[0]} และ{b[0]}" for a in ACIDS for b in ALCOHOLS if (a, b) != (acid, alcohol)]
            others += [f"{acid[0]} และ{alcohol[0]}"]
            return _labelled(stem=f"{e_name} ({e_formula}) ทำปฏิกิริยากับสารละลาย NaOH ได้ผลิตภัณฑ์ใด", correct=right,
                             wrongs=(f"{acid[0]} และ{alcohol[0]}", *rng.sample(others[:-1], 2)), topic=TOPIC_ESTER,
                             hint="สะปอนนิฟิเคชัน: เอสเทอร์ + NaOH → เกลือโซเดียมของกรด + แอลกอฮอล์ (ไม่ได้กรดอิสระ)")
        amine = rng.choice(AMINES)
        a_name, a_formula = amide(acid, amine)
        others = sorted({amide(a, b)[0] for a in ACIDS for b in AMINES} - {a_name})
        wrong_ester = ester(acid, ALCOHOLS[AMINES.index(amine)])[0]
        return _labelled(stem=f"{acid[0]} ทำปฏิกิริยากับ{amine[0]} ({amine[3]}) ได้เอไมด์ใด", correct=f"{a_name} ({a_formula})",
                         wrongs=(wrong_ester, *rng.sample(others, 2)), topic=TOPIC_ESTER,
                         hint="กรด + เอมีน → เอไมด์ + น้ำ ชื่อเอไมด์ = N-หมู่แอลคิลจากเอมีน + ชื่อกรดที่เปลี่ยน -โอิก เป็น -เอไมด์")
