"""การหมุนเวียนของน้ำผิวหน้าในมหาสมุทร

ธรณีวิทยา · ม.6 · สสวท. พื้นฐาน
Indicators: ว 3.2 ม.6/11

Sets moved here from: science_wave_c25.
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
from otk.sets._support.science_wave_c6 import UPPER_SIX
from otk.sets._support.science_wave_c10 import SUBJECT
from otk.sets._support.science_wave_c24 import parts_item
from otk.sets._support.science_wave_c25 import OCEAN_PARTS, OCEAN_SCENARIOS

PROVENANCE = Provenance("original")


OCEAN_TOPIC = "การหมุนเวียนของน้ำผิวหน้าในมหาสมุทร"


class Current(NamedTuple):
    name: str
    coast: str
    warm: bool


CURRENTS = (
    Current("กระแสน้ำกัลฟ์สตรีม", "ชายฝั่งตะวันออกของทวีปอเมริกาเหนือ", True),
    Current("กระแสน้ำคุโรชิโอะ", "ชายฝั่งตะวันออกของทวีปเอเชีย ผ่านประเทศญี่ปุ่น", True),
    Current("กระแสน้ำบราซิล", "ชายฝั่งตะวันออกของทวีปอเมริกาใต้", True),
    Current("กระแสน้ำแคลิฟอร์เนีย", "ชายฝั่งตะวันตกของทวีปอเมริกาเหนือ", False),
    Current("กระแสน้ำฮัมโบลต์", "ชายฝั่งตะวันตกของทวีปอเมริกาใต้ ผ่านประเทศเปรูและชิลี", False),
    Current("กระแสน้ำเบงเกวลา", "ชายฝั่งตะวันตกของทวีปแอฟริกาตอนใต้", False),
    Current("กระแสน้ำอะกะลัส", "ชายฝั่งตะวันออกของทวีปแอฟริกาตอนใต้", True),
    Current("กระแสน้ำออสเตรเลียตะวันออก", "ชายฝั่งตะวันออกของทวีปออสเตรเลีย", True),
    Current("กระแสน้ำแคนารี", "ชายฝั่งตะวันตกของทวีปแอฟริกาตอนเหนือ", False),
    Current("กระแสน้ำออสเตรเลียตะวันตก", "ชายฝั่งตะวันตกของทวีปออสเตรเลีย", False),
)


WARM = "กระแสน้ำอุ่น"


COLD = "กระแสน้ำเย็น"


POLEWARD = "ไหลจากเขตศูนย์สูตรไปทางขั้วโลก"


EQUATORWARD = "ไหลจากขั้วโลกมาทางเขตศูนย์สูตร"


@question_type(
    "geo.ocean_currents_foundation",
    display_name={"th": "จำแนกกระแสน้ำอุ่นและกระแสน้ำเย็นจากตำแหน่งชายฝั่ง"},
    level=UPPER_SIX, subject=SUBJECT, topic=OCEAN_TOPIC,
)
class OceanCurrentsFoundation(QuestionType):
    """A named current and the coast it follows; warm or cold, and which way."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        current = rng.choice(CURRENTS)
        combos = [f"{kind} {way}" for kind in (WARM, COLD) for way in (POLEWARD, EQUATORWARD)]
        correct = f"{WARM} {POLEWARD}" if current.warm else f"{COLD} {EQUATORWARD}"
        lead = rng.choice(("", "บนแผนที่กระแสน้ำผิวหน้า ", "นักเดินเรือบันทึกว่า"))
        return _labelled(
            stem=f"{lead}{current.name}ไหลเลียบ{current.coast} จัดเป็นกระแสน้ำชนิดใด และไหลไปทางใด",
            correct=correct,
            wrongs=tuple(combo for combo in combos if combo != correct),
            hint="ชายฝั่งตะวันออกของทวีปรับน้ำอุ่นที่ไหลมาจากศูนย์สูตร ชายฝั่งตะวันตกรับน้ำเย็นที่ไหลมาจากขั้วโลก",
            topic=OCEAN_TOPIC,
        )


OCEAN_ASK = ("ข้อใดอธิบายปัจจัยที่ทำให้เกิดการหมุนเวียนของน้ำผิวหน้าในมหาสมุทร "
             "และรูปแบบการหมุนเวียนได้ถูกต้องทั้งหมด")


# What the question opens on. Each ends where ``OCEAN_ASK`` begins, and none
# changes which statement of the parts is true.
OCEAN_LEADS = (
    "",
    "ทุ่นลอยที่ติดตามตำแหน่งด้วยดาวเทียมกลางมหาสมุทรแปซิฟิกเหนือ เคลื่อนเป็นวงขนาดใหญ่อยู่หลายปี ",
    "จากแผนที่กระแสน้ำผิวหน้าของมหาสมุทรแอตแลนติกเหนือและแอตแลนติกใต้ ",
    "เรือใบที่แล่นข้ามมหาสมุทรมักวางเส้นทางให้ไปตามกระแสน้ำผิวหน้า ",
    "ครูใช้พัดลมเป่าผิวน้ำในอ่างที่มีแผ่นไม้กั้นขอบแทนทวีป แล้วชวนนักเรียนเทียบกับมหาสมุทรจริง ",
)


@question_type(
    "geo.ocean_currents_fluency",
    display_name={"th": "อธิบายปัจจัยและรูปแบบการหมุนเวียนของน้ำผิวหน้าในมหาสมุทร"},
    level=UPPER_SIX, subject=SUBJECT, topic=OCEAN_TOPIC,
)
class OceanCurrentsFluency(QuestionType):
    """The factors and the pattern explained together; each wrong choice falsifies one."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return parts_item(
            rng, OCEAN_PARTS,
            stem=rng.choice(OCEAN_LEADS) + OCEAN_ASK,
            hint="ตรวจทีละส่วน ข้อที่ผิดจะผิดอย่างน้อยหนึ่งส่วน",
            topic=OCEAN_TOPIC,
        )


@question_type(
    "geo.ocean_currents_application",
    display_name={"th": "วิเคราะห์วงวนของกระแสน้ำผิวหน้าในสถานการณ์จริง"},
    level=UPPER_SIX, subject=SUBJECT, topic=OCEAN_TOPIC,
)
class OceanCurrentsApplication(QuestionType):
    """Garbage patches, drifting toy ducks, and weakened trade winds."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        return _retopic(scenario_question(
            rng, OCEAN_SCENARIOS,
            hint="นึกว่าลมขับน้ำผิวหน้าอย่างไร และน้ำผิวหน้าไหลเป็นวงวนรอบมหาสมุทรอย่างไร",
        ), OCEAN_TOPIC)
