"""แร่และการใช้ประโยชน์

ธรณีวิทยา · ม.4 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/8

Sets moved here from: science_wave_f76.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f76 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_MINERAL = "แร่และการใช้ประโยชน์"


MOHS = ("ทัลก์", "ยิปซัม", "แคลไซต์", "ฟลูออไรต์", "อะพาไทต์", "ออร์โทเคลส", "ควอตซ์", "โทแพซ", "คอรันดัม", "เพชร")


MINERALS = (
    ("แคลไซต์", "ทำปฏิกิริยากับกรดไฮโดรคลอริกเจือจางเกิดฟองแก๊ส", "ใช้ทำปูนซีเมนต์และปูนขาว"),
    ("แมกนีไทต์", "ดูดติดแม่เหล็ก", "เป็นสินแร่เหล็ก"),
    ("ควอตซ์", "แข็งมาก ขีดกระจกเป็นรอยได้ และไม่มีแนวแตกเรียบ", "ใช้ทำแก้วและอุปกรณ์อิเล็กทรอนิกส์"),
    ("ยิปซัม", "อ่อนมาก ใช้เล็บขีดเป็นรอยได้", "ใช้ทำปูนปลาสเตอร์และเป็นส่วนผสมของปูนซีเมนต์"),
    ("กาลีนา", "สีเทาเงินวาว หนักมาก แตกเป็นก้อนสี่เหลี่ยม", "เป็นสินแร่ตะกั่ว"),
    ("แคสซิเทอไรต์", "สีน้ำตาลเข้มถึงดำ หนักมาก", "เป็นสินแร่ดีบุก"),
    ("ฟลูออไรต์", "มีหลายสี แตกเป็นรูปทรงแปดหน้า เรืองแสงเมื่อได้รับรังสีอัลตราไวโอเลต", "ใช้ในการถลุงเหล็กและผลิตกรดไฮโดรฟลูออริก"),
)


MINERAL_HINT = ("ระบุแร่จากความแข็ง (มาตราโมส์ 1 ทัลก์ ถึง 10 เพชร) สีผงละเอียด ความวาว แนวแตก ความหนาแน่น การดูดแม่เหล็ก "
                "และการทำปฏิกิริยากับกรด แร่ที่แข็งกว่าขีดแร่ที่อ่อนกว่าเป็นรอยได้")


@question_type(
    "geo.mineral_id_foundation",
    display_name={"th": "สมบัติเด่นของแร่และการใช้ประโยชน์"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MINERAL,
)
class MineralIdFoundation(QuestionType):
    """Name the mineral from its telltale test, or say what it is used for."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        name, test, use = rng.choice(MINERALS)
        others = rng.sample([m for m in MINERALS if m[0] != name], 3)
        roll = rng.random()
        if roll < 0.4:
            return _labelled(stem=f"แร่ที่ \"{test}\" น่าจะเป็นแร่ใด", correct=name, wrongs=tuple(m[0] for m in others), topic=TOPIC_MINERAL,
                             hint=MINERAL_HINT)
        if roll < 0.7:
            return _labelled(stem=f"แร่{name}ใช้ประโยชน์อย่างไร", correct=use, wrongs=tuple(m[2] for m in others), topic=TOPIC_MINERAL,
                             hint=MINERAL_HINT)
        return _labelled(stem=f"แร่ใด{use}", correct=name, wrongs=tuple(m[0] for m in others), topic=TOPIC_MINERAL, hint=MINERAL_HINT)


@question_type(
    "geo.mineral_id_fluency",
    display_name={"th": "ใช้มาตราความแข็งของโมส์ระบุแร่"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MINERAL,
)
class MineralIdFluency(QuestionType):
    """A scratch test puts the hardness between two Mohs minerals."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            lo = rng.randrange(0, 8)
            hi = lo + rng.choice((1, 2))
            return self._range(rng, lo, hi)
        i = rng.randrange(len(MOHS))
        if rng.random() < 0.5:
            return numeric(stem=f"{MOHS[i]}มีความแข็งตามมาตราโมส์เท่าใด", answer=i + 1, wrongs=[10 - i if 10 - i != i + 1 else i + 2, i + 2, i],
                           unit="", topic=TOPIC_MINERAL, hint=MINERAL_HINT)
        j = rng.choice([k for k in range(len(MOHS)) if k != i])
        harder = MOHS[max(i, j)]
        return _labelled(stem=f"ถ้านำ{MOHS[i]}กับ{MOHS[j]}มาขีดกัน แร่ใดจะเป็นรอย", correct=MOHS[min(i, j)],
                         wrongs=(harder, "เป็นรอยทั้งสองแร่เท่ากัน", "ไม่เป็นรอยทั้งสองแร่"), topic=TOPIC_MINERAL, hint=MINERAL_HINT)

    @staticmethod
    def _range(rng: Random, lo: int, hi: int) -> GeneratedQuestion:
        right = f"มากกว่า {lo + 1} แต่น้อยกว่า {hi + 1}"
        wrongs = (f"น้อยกว่า {lo + 1}", f"มากกว่า {hi + 1}", f"มากกว่า {hi + 1} แต่น้อยกว่า {min(hi + 3, 10)}" if hi + 1 < 10 else "เท่ากับ 10")
        return _labelled(stem=f"แร่ตัวอย่างขีด{MOHS[lo]}เป็นรอยได้ แต่ถูก{MOHS[hi]}ขีดเป็นรอย ความแข็งของแร่ตัวอย่างอยู่ในช่วงใด",
                         correct=right, wrongs=wrongs, topic=TOPIC_MINERAL, hint=MINERAL_HINT)


@question_type(
    "geo.mineral_id_application",
    display_name={"th": "ระบุแร่จากผลการทดสอบหลายอย่าง"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_MINERAL,
)
class MineralIdApplication(QuestionType):
    """Combine hardness, acid and magnet results."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        # name: (hardness, streak, lustre, fizzes with acid, magnetic)
        table = {"แคลไซต์": ("ขีดด้วยเหรียญทองแดงเป็นรอย", "สีขาว", "วาวแบบแก้ว", True, False),
                 "ควอตซ์": ("ขีดกระจกเป็นรอยได้", "สีขาว", "วาวแบบแก้ว", False, False),
                 "แมกนีไทต์": ("ขีดกระจกเป็นรอยได้เล็กน้อย", "สีดำ", "วาวแบบโลหะ", False, True),
                 "ยิปซัม": ("ใช้เล็บขีดเป็นรอย", "สีขาว", "วาวแบบแก้วถึงมุก", False, False),
                 "กาลีนา": ("ขีดด้วยเหรียญทองแดงเป็นรอย", "สีเทาดำ", "วาวแบบโลหะ", False, False),
                 "ฮีมาไทต์": ("ขีดกระจกเป็นรอยได้", "สีน้ำตาลแดง", "วาวแบบโลหะถึงด้าน", False, False),
                 "ไพไรต์": ("ขีดกระจกเป็นรอยได้", "สีดำอมเขียว", "วาวแบบโลหะสีทองเหลือง", False, False)}
        name = rng.choice(sorted(table))
        hard, streak, lustre, acid, mag = table[name]
        description = (f"แร่ตัวอย่าง{hard} สีผงละเอียด{streak} {lustre} "
                       f"{'เกิดฟองแก๊สเมื่อหยดกรดไฮโดรคลอริกเจือจาง' if acid else 'ไม่เกิดฟองแก๊สกับกรดเจือจาง'} "
                       f"และ{'ดูดติดแม่เหล็ก' if mag else 'ไม่ดูดติดแม่เหล็ก'}")
        return _labelled(stem=f"{description} แร่นี้น่าจะเป็นแร่ใด", correct=name, wrongs=tuple([n for n in table if n != name]),
                         topic=TOPIC_MINERAL, hint=MINERAL_HINT + " สีผงของแร่คงที่กว่าสีของก้อนแร่")
