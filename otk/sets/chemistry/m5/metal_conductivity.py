"""การนำไฟฟ้า การให้และรับอิเล็กตรอนของโลหะกับอโลหะ

เคมี · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.5/6

Sets moved here from: science_wave_e2.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.chemistry import Element, full_name
from otk.sets._support.science_wave_a5 import METAL, NONMETAL, TABLE_POOL, metal_class
from otk.sets._support.science_wave_e2 import SUBJECT, _labelled

PROVENANCE = Provenance("original")


TOPIC_CONDUCTIVITY = "การนำไฟฟ้า การให้และรับอิเล็กตรอนของโลหะกับอโลหะ"


GIVES, RECEIVES = "ให้อิเล็กตรอน", "รับอิเล็กตรอน"


CONDUCTS_WELL, CONDUCTS_POORLY = "นำไฟฟ้าได้ดี", "นำไฟฟ้าได้ไม่ดี"


def _metal_label(kind: str) -> str:
    conduct = CONDUCTS_WELL if kind == METAL else CONDUCTS_POORLY
    verb = GIVES if kind == METAL else RECEIVES
    return f"{conduct} และมีแนวโน้ม{verb}"


CONDUCTIVITY_POOL: tuple[Element, ...] = tuple(
    el for el in TABLE_POOL if metal_class(el) in (METAL, NONMETAL)
)


@question_type(
    "chem.metal_conductivity_foundation",
    display_name={"th": "โลหะหรืออโลหะนำไฟฟ้าได้ดีกว่า"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_CONDUCTIVITY,
)
class MetalConductivityFoundation(QuestionType):
    """One fact at a time — conductivity, or electron-giving/receiving."""

    FACTS = (
        ("ธาตุกลุ่มใดนำไฟฟ้าได้ดีกว่ากัน ระหว่างโลหะกับอโลหะ", METAL),
        ("ธาตุกลุ่มใดมีแนวโน้มให้อิเล็กตรอน ระหว่างโลหะกับอโลหะ", METAL),
        ("ธาตุกลุ่มใดมีแนวโน้มรับอิเล็กตรอน ระหว่างโลหะกับอโลหะ", NONMETAL),
        ("ธาตุกลุ่มใดมีอิเล็กตรอนที่เคลื่อนที่ได้อิสระทั่วทั้งก้อนธาตุ ระหว่างโลหะกับอโลหะ", METAL),
        ("เมื่อเกิดสารประกอบไอออนิก ธาตุกลุ่มใดมักกลายเป็นไอออนบวก ระหว่างโลหะกับอโลหะ", METAL),
        ("เมื่อเกิดสารประกอบไอออนิก ธาตุกลุ่มใดมักกลายเป็นไอออนลบ ระหว่างโลหะกับอโลหะ", NONMETAL),
    )
    FILLERS = ("ทั้งสองกลุ่มเท่ากัน", "ไม่มีกลุ่มใดเลย", "ธาตุแก๊สมีตระกูลเท่านั้น", "ขึ้นอยู่กับสีของธาตุ")

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, kind = rng.choice(self.FACTS)
        return _labelled(
            stem=stem,
            correct=kind,
            wrongs=(NONMETAL if kind == METAL else METAL, *self.FILLERS),
            topic=TOPIC_CONDUCTIVITY,
            hint="โลหะมีอิเล็กตรอนวงนอกที่เคลื่อนที่ได้อิสระ นำไฟฟ้าได้ดีและเสียอิเล็กตรอนง่าย ส่วนอโลหะรับอิเล็กตรอนเข้ามาจนวงนอกเต็ม",
        )


@question_type(
    "chem.metal_conductivity_fluency",
    display_name={"th": "เปรียบเทียบการนำไฟฟ้าและการให้/รับอิเล็กตรอนของโลหะกับอโลหะ"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_CONDUCTIVITY,
)
class MetalConductivityFluency(QuestionType):
    """State the full comparison between the two groups at once."""

    EXAMPLES = {METAL: ("โซเดียม", "แมกนีเซียม", "อะลูมิเนียม", "เหล็ก", "ทองแดง"),
                NONMETAL: ("คลอรีน", "ออกซิเจน", "กำมะถัน", "ไนโตรเจน", "ฟลูออรีน")}

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        kind = rng.choice((METAL, NONMETAL))
        other = NONMETAL if kind == METAL else METAL
        first, second = rng.sample(self.EXAMPLES[kind], 2)
        return _labelled(
            stem=(f"ธาตุกลุ่ม{kind} เช่น {first} และ{second} "
                  "มีสมบัติการนำไฟฟ้าและแนวโน้มการให้/รับอิเล็กตรอนอย่างไร"),
            correct=_metal_label(kind),
            wrongs=(
                _metal_label(other),
                f"{CONDUCTS_WELL if kind == METAL else CONDUCTS_POORLY} และมีแนวโน้ม"
                f"{RECEIVES if kind == METAL else GIVES}",
                f"{CONDUCTS_POORLY if kind == METAL else CONDUCTS_WELL} และมีแนวโน้ม"
                f"{GIVES if kind == METAL else RECEIVES}",
                "ไม่นำไฟฟ้า และไม่ให้หรือรับอิเล็กตรอนเลย",
                "นำไฟฟ้าได้เฉพาะเมื่อหลอมเหลว และให้และรับอิเล็กตรอนเท่า ๆ กัน",
            ),
            topic=TOPIC_CONDUCTIVITY,
            hint="จับคู่สมบัติการนำไฟฟ้ากับแนวโน้มการให้/รับอิเล็กตรอนของกลุ่มธาตุเดียวกันเสมอ",
        )


@question_type(
    "chem.metal_conductivity_application",
    display_name={"th": "ธาตุที่กำหนด → การนำไฟฟ้าและการให้/รับอิเล็กตรอน"},
    level={"th": "ม.5"}, subject=SUBJECT, topic=TOPIC_CONDUCTIVITY,
)
class MetalConductivityApplication(QuestionType):
    """Apply the metal/nonmetal rule to one named element, not a bare group."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        el = rng.choice(CONDUCTIVITY_POOL)
        kind = metal_class(el)
        other = NONMETAL if kind == METAL else METAL
        return _labelled(
            stem=f"ธาตุ {full_name(el)} ({kind}) มีสมบัติการนำไฟฟ้าและแนวโน้มการให้/รับอิเล็กตรอนอย่างไร",
            correct=_metal_label(kind),
            wrongs=(
                _metal_label(other),
                f"{CONDUCTS_WELL if kind == METAL else CONDUCTS_POORLY} และมีแนวโน้ม"
                f"{RECEIVES if kind == METAL else GIVES}",
                f"{CONDUCTS_POORLY if kind == METAL else CONDUCTS_WELL} และมีแนวโน้ม"
                f"{GIVES if kind == METAL else RECEIVES}",
            ),
            topic=TOPIC_CONDUCTIVITY,
            hint="ดูก่อนว่าธาตุนี้เป็นโลหะหรืออโลหะ แล้วใช้สมบัติของกลุ่มนั้น",
        )
