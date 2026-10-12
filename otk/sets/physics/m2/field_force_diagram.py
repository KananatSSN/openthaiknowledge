"""แผนภาพแสดงแรงแม่เหล็ก แรงไฟฟ้า และแรงโน้มถ่วง

ฟิสิกส์ · ม.2 · สสวท. พื้นฐาน
Indicators: ว 2.2 ม.2/12

Sets moved here from: science_wave_d21.
"""

from __future__ import annotations

from random import Random
from typing import NamedTuple

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.force_diagrams import FIELD_SPECS, diagram_question
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d18 import SECONDARY_TWO

PROVENANCE = Provenance("original")


FIELD_DIAGRAM_TOPIC = "แผนภาพแสดงแรงแม่เหล็ก แรงไฟฟ้า และแรงโน้มถ่วง"


class FieldCase(NamedTuple):
    stem: str
    correct: str
    wrongs: tuple[str, str, str]


FIELD_DIAGRAM_CASES = (
    FieldCase(
        "ตะปูเหล็กวางนิ่งบนโต๊ะ อยู่ใกล้แม่เหล็กซึ่งดึงดูดไปทางขวา แผนภาพควรแสดงแรงใดบ้าง",
        "น้ำหนักชี้ลง แรงที่โต๊ะดันชี้ขึ้น และแรงแม่เหล็กชี้ไปทางขวา",
        ("แรงแม่เหล็กชี้ไปทางขวาเพียงแรงเดียว",
         "น้ำหนักชี้ลงและแรงที่โต๊ะดันชี้ขึ้น โดยไม่มีแรงแม่เหล็ก",
         "น้ำหนักชี้ขึ้น แรงที่โต๊ะดันชี้ลง และแรงแม่เหล็กชี้ไปทางซ้าย"),
    ),
    FieldCase(
        "ลูกบอลประจุลบวางนิ่งบนโต๊ะ อยู่ใกล้แท่งพลาสติกประจุลบทางซ้าย ซึ่งผลักไปทางขวา แผนภาพควรแสดงแรงใดบ้าง",
        "น้ำหนักชี้ลง แรงที่โต๊ะดันชี้ขึ้น และแรงไฟฟ้าชี้ไปทางขวา",
        ("แรงไฟฟ้าชี้ไปทางซ้ายเพียงแรงเดียว",
         "น้ำหนักชี้ลงและแรงที่โต๊ะดันชี้ขึ้น โดยไม่มีแรงไฟฟ้า",
         "น้ำหนักชี้ลง แรงที่โต๊ะดันชี้ขึ้น และแรงไฟฟ้าชี้ไปทางซ้าย"),
    ),
    FieldCase(
        "ผลไม้กำลังตกจากต้นสู่พื้น ยังไม่ถึงพื้นและไม่สัมผัสสิ่งใด แผนภาพควรแสดงแรงใดบ้าง",
        "น้ำหนักชี้ลงเพียงแรงเดียว",
        ("น้ำหนักชี้ลงและแรงที่พื้นดันชี้ขึ้น",
         "น้ำหนักชี้ขึ้นเพียงแรงเดียว",
         "ไม่มีแรงใดกระทำต่อผลไม้ขณะตก"),
    ),
)


FIELD_DIAGRAM_SCENARIOS = (
    ("เพื่อนวาดแผนภาพลูกแก้วประจุลบที่ลอยนิ่งใกล้แท่งพลาสติกประจุลบ โดยให้ลูกศรแรงไฟฟ้าชี้เข้าหาแท่งพลาสติก ข้อใดแก้ไขได้ถูกต้อง",
     "ประจุชนิดเดียวกันผลักกัน ลูกศรแรงไฟฟ้าจึงควรชี้ออกจากแท่งพลาสติก",
     ("ถูกต้องแล้ว เพราะประจุชนิดเดียวกันดึงดูดกัน ลูกศรจึงชี้เข้าหาแท่งพลาสติก", "ไม่ต้องวาดแรงไฟฟ้า เพราะแรงไฟฟ้าเกิดได้เฉพาะเมื่อวัตถุสัมผัสกันเท่านั้น", "ลูกศรควรชี้ขึ้นเสมอไม่ว่าประจุใด")),
    ("คลิปหนีบกระดาษเหล็กถูกแม่เหล็กดูดจนลอยนิ่งอยู่กลางอากาศใต้แม่เหล็ก แผนภาพควรมีลูกศรใดบ้าง",
     "น้ำหนักชี้ลงและแรงแม่เหล็กชี้ขึ้น โดยยาวเท่ากัน",
     ("น้ำหนักชี้ลงเพียงแรงเดียว", "แรงแม่เหล็กชี้ลงและน้ำหนักชี้ขึ้น", "น้ำหนักและแรงแม่เหล็กชี้ลงทั้งคู่ โดยยาวเท่ากัน")),
    ("ดาวเทียมโคจรรอบโลกโดยไม่มีแรงขับเครื่องยนต์ แผนภาพแรงที่กระทำต่อดาวเทียมควรมีลูกศรใด",
     "แรงโน้มถ่วงจากโลกชี้เข้าหาโลกเพียงแรงเดียว",
     ("ไม่มีแรงกระทำต่อดาวเทียมเลย เพราะอวกาศไม่มีอากาศ", "แรงโน้มถ่วงชี้ออกจากโลก", "แรงแม่เหล็กและแรงโน้มถ่วงชี้เข้าหาโลกเท่ากัน")),
    ("ลูกบอลที่ถูกโยนขึ้นกำลังลอยสูงขึ้นในอากาศ (ไม่คิดแรงต้านอากาศ) แผนภาพแรงที่กระทำต่อลูกบอลควรมีลูกศรใด",
     "น้ำหนักชี้ลงเพียงแรงเดียว",
     ("แรงจากมือชี้ขึ้นเพียงแรงเดียว", "น้ำหนักชี้ลงและแรงจากมือชี้ขึ้น", "ไม่มีแรงใดกระทำ")),
    ("เพื่อนวาดแผนภาพตะปูเหล็กที่ถูกแม่เหล็กทางซ้ายดูด โดยให้ลูกศรแรงแม่เหล็กชี้ไปทางขวา ข้อใดแก้ไขได้ถูกต้อง",
     "แม่เหล็กดึงดูดเหล็ก ลูกศรแรงแม่เหล็กจึงควรชี้ไปทางซ้ายเข้าหาแม่เหล็ก",
     ("ถูกต้องแล้ว เพราะแม่เหล็กผลักเหล็ก ลูกศรจึงควรชี้ไปทางขวาออกจากแม่เหล็ก", "ไม่ต้องวาดแรงแม่เหล็ก เพราะแม่เหล็กกับเหล็กไม่ได้สัมผัสกันโดยตรง แรงจึงเป็นศูนย์", "ลูกศรควรชี้ขึ้นเสมอ")),
)


@question_type(
    "phys.field_force_diagram_foundation",
    display_name={"th": "บอกแรงแม่เหล็ก แรงไฟฟ้า หรือแรงโน้มถ่วงที่ควรอยู่ในแผนภาพ"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=FIELD_DIAGRAM_TOPIC,
)
class FieldForceDiagramFoundation(QuestionType):
    """Which forces belong in the diagram of an object near a field source."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.75:
            side = rng.choice(("ซ้าย", "ขวา"))
            if rng.random() < 0.4:
                thing = rng.choice(("ตะปูเหล็ก", "คลิปหนีบกระดาษเหล็ก", "น็อตเหล็ก", "ลูกเหล็กกลม"))
                source = f"{rng.choice(('แม่เหล็กแท่ง', 'แม่เหล็กเกือกม้า'))}ที่วางอยู่ทางด้าน{side}"
                force, toward = "แรงแม่เหล็ก", side
            else:
                thing_charge = rng.choice(("บวก", "ลบ"))
                rod_charge = rng.choice(("บวก", "ลบ"))
                thing = f"{rng.choice(('ลูกบอลเล็ก', 'ลูกพิท', 'ลูกโป่ง'))}ประจุ{thing_charge}"
                source = f"{rng.choice(('แท่งพลาสติก', 'แท่งแก้ว', 'หวี'))}ประจุ{rod_charge}ที่อยู่ทางด้าน{side}"
                away = "ขวา" if side == "ซ้าย" else "ซ้าย"
                force, toward = "แรงไฟฟ้า", (side if thing_charge != rod_charge else away)
            opposite = "ขวา" if toward == "ซ้าย" else "ซ้าย"
            other = "แรงไฟฟ้า" if force == "แรงแม่เหล็ก" else "แรงแม่เหล็ก"
            return _labelled(
                stem=f"{thing}วางนิ่งบนโต๊ะ ใกล้{source} แผนภาพควรแสดงแรงใดบ้าง",
                correct=f"น้ำหนักชี้ลง แรงที่โต๊ะดันชี้ขึ้น และ{force}ชี้ไปทาง{toward}",
                wrongs=(f"น้ำหนักชี้ลง แรงที่โต๊ะดันชี้ขึ้น และ{force}ชี้ไปทาง{opposite}",
                        f"น้ำหนักชี้ลงและแรงที่โต๊ะดันชี้ขึ้น โดยไม่มี{force}",
                        f"น้ำหนักชี้ลง แรงที่โต๊ะดันชี้ขึ้น และ{other}ชี้ไปทาง{toward}",
                        # Two things wrong at once.
                        f"น้ำหนักชี้ลง แรงที่โต๊ะดันชี้ขึ้น และ{other}ชี้ไปทาง{opposite}",
                        f"น้ำหนักชี้ขึ้น แรงที่โต๊ะดันชี้ลง และ{force}ชี้ไปทาง{opposite}"),
                hint="มีแรงโน้มถ่วง (น้ำหนัก) เสมอ ส่วนแรงที่พื้นดันและแรงจากสนามอื่นมีเมื่อวัตถุสัมผัสพื้นหรืออยู่ในสนามนั้น",
                topic=FIELD_DIAGRAM_TOPIC,
            )
        case = rng.choice(FIELD_DIAGRAM_CASES)
        return _labelled(
            stem=case.stem, correct=case.correct, wrongs=case.wrongs,
            hint="มีแรงโน้มถ่วง (น้ำหนัก) เสมอ ส่วนแรงที่พื้นดันและแรงจากสนามอื่นมีเมื่อวัตถุสัมผัสพื้นหรืออยู่ในสนามนั้น",
            topic=FIELD_DIAGRAM_TOPIC,
        )


@question_type(
    "phys.field_force_diagram_fluency",
    display_name={"th": "อ่านและระบุแรงจากแผนภาพแรงแม่เหล็ก แรงไฟฟ้า และน้ำหนัก"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=FIELD_DIAGRAM_TOPIC,
)
class FieldForceDiagramFluency(QuestionType):
    """The student is shown the drawn diagram and names the forces on it."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        spec = rng.choice(FIELD_SPECS)
        weight = spec.of("W").newtons
        field = next(a for a in spec.arrows if a.symbol in ("FM", "FE"))
        sideways = "ขวา" if field.direction == "right" else "ซ้าย"
        correct = (f"{field.name} {field.newtons} นิวตัน ไปทาง{sideways} "
                   f"ส่วนน้ำหนักและแรงที่โต๊ะดันมีขนาด {weight} นิวตันเท่ากัน จึงหักล้างกันพอดี")
        other = "แรงแม่เหล็ก" if field.name == "แรงไฟฟ้า" else "แรงไฟฟ้า"
        opposite = "ซ้าย" if sideways == "ขวา" else "ขวา"
        balanced = f"ส่วนน้ำหนักและแรงที่โต๊ะดันมีขนาด {weight} นิวตันเท่ากัน จึงหักล้างกันพอดี"
        # The mistakes share their slips, so the answer is not the one choice
        # every other choice is a single change away from.
        wrongs = [
            f"{field.name} {field.newtons} นิวตัน ไปทาง{opposite} {balanced}",
            f"{other} {field.newtons} นิวตัน ไปทาง{opposite} {balanced}",
            f"{field.name} {field.newtons} นิวตัน ไปทาง{opposite} "
            f"ส่วนน้ำหนัก {weight} นิวตันมากกว่าแรงที่โต๊ะดัน วัตถุจึงกดโต๊ะจมลงไป",
        ]
        return diagram_question(
            spec,
            stem="จากแผนภาพ ข้อใดอธิบายแรงที่กระทำต่อวัตถุได้ถูกต้อง",
            correct=correct,
            wrongs=tuple(dict.fromkeys(w for w in wrongs if w != correct))[:3],
            hint="ดูสัญลักษณ์บนลูกศร: FM คือแรงแม่เหล็ก FE คือแรงไฟฟ้า W คือน้ำหนัก และ N คือแรงที่โต๊ะดัน",
            topic=FIELD_DIAGRAM_TOPIC,
        )


@question_type(
    "phys.field_force_diagram_application",
    display_name={"th": "อ่านและแก้ไขแผนภาพแรงแม่เหล็ก แรงไฟฟ้า และแรงโน้มถ่วง"},
    level=SECONDARY_TWO, subject=SUBJECT, topic=FIELD_DIAGRAM_TOPIC,
)
class FieldForceDiagramApplication(QuestionType):
    """Authored cases, a clip held up by a magnet, and two sideways field forces."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.35:
            weight = rng.choice((0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.8, 1, 1.5, 2))
            thing = rng.choice(("คลิปหนีบกระดาษเหล็ก", "ตะปูเหล็ก", "ลูกเหล็กกลม", "แหวนเหล็ก"))
            return _labelled(
                stem=(f"{thing}หนัก {weight:g} นิวตัน ถูกแม่เหล็กที่อยู่ด้านบนดูดจนลอยนิ่งกลางอากาศโดยไม่สัมผัสแม่เหล็ก "
                      "ในแผนภาพ ลูกศรแรงแม่เหล็กควรเป็นอย่างไร"),
                correct=f"{weight:g} นิวตัน ชี้ขึ้น ยาวเท่าลูกศรน้ำหนัก",
                wrongs=(f"{weight:g} นิวตัน ชี้ลง ทิศเดียวกับน้ำหนัก", f"{weight * 2:g} นิวตัน ชี้ขึ้น ยาวเป็นสองเท่าของน้ำหนัก",
                        "ไม่ต้องวาด เพราะแม่เหล็กไม่ได้สัมผัสวัตถุ"),
                hint="วัตถุลอยนิ่ง แรงลัพธ์เป็นศูนย์ แรงแม่เหล็กจึงเท่ากับน้ำหนักและมีทิศตรงข้าม",
                topic=FIELD_DIAGRAM_TOPIC,
            )
        if roll < 0.7:
            magnetic, electric = rng.randint(2, 12), rng.randint(2, 12)
            m_side = rng.choice(("ขวา", "ซ้าย"))
            e_side = rng.choice(("ขวา", "ซ้าย"))
            net = (magnetic if m_side == "ขวา" else -magnetic) + (electric if e_side == "ขวา" else -electric)
            answer = "แรงลัพธ์ในแนวราบเป็นศูนย์" if net == 0 else f"แรงลัพธ์ในแนวราบ {abs(net)} นิวตัน ไปทาง{'ขวา' if net > 0 else 'ซ้าย'}"
            options = [f"แรงลัพธ์ในแนวราบ {magnetic + electric} นิวตัน ไปทาง{m_side}",
                       f"แรงลัพธ์ในแนวราบ {abs(net) or magnetic} นิวตัน ไปทาง{'ซ้าย' if net > 0 else 'ขวา'}",
                       "แรงลัพธ์ในแนวราบเป็นศูนย์", f"แรงลัพธ์ในแนวราบ {max(magnetic, electric)} นิวตัน ไปทาง{m_side}",
                       f"แรงลัพธ์ในแนวราบ {magnetic + electric + 2} นิวตัน ไปทาง{e_side}"]
            return _labelled(
                stem=(f"วัตถุบนโต๊ะลื่นมีแรงแม่เหล็ก {magnetic} นิวตัน ไปทาง{m_side} และแรงไฟฟ้า {electric} นิวตัน "
                      f"ไปทาง{e_side} ในแนวเดียวกัน แรงลัพธ์ในแนวราบเป็นอย่างไร"),
                correct=answer,
                wrongs=tuple([o for o in dict.fromkeys(options) if o != answer][:3]),
                hint="แรงทิศเดียวกันบวกกัน ทิศตรงข้ามลบกัน แรงลัพธ์ชี้ไปทางแรงที่มากกว่า",
                topic=FIELD_DIAGRAM_TOPIC,
            )
        return _retopic(scenario_question(
            rng, FIELD_DIAGRAM_SCENARIOS,
            hint="ประจุชนิดเดียวกันผลักกัน ชนิดต่างกันดึงดูดกัน แรงแม่เหล็กและแรงโน้มถ่วงในสถานการณ์เหล่านี้ล้วนดึงดูด",
        ), FIELD_DIAGRAM_TOPIC)
