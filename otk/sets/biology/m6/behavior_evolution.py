"""พฤติกรรมกับวิวัฒนาการของระบบประสาท

ชีวะ · ม.6 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.6/18

Sets moved here from: science_wave_f70.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f70 import SUBJECT, UPPER_SIX

PROVENANCE = Provenance("original")


TOPIC_EVOL = "พฤติกรรมกับวิวัฒนาการของระบบประสาท"


LEVELS = (
    ("โพรโทซัว เช่น พารามีเซียม", "ไม่มีเซลล์ประสาท", "ไคนีซิสและแทกซิสอย่างง่าย"),
    ("ไฮดรา", "ร่างแหประสาท", "ตอบสนองทั้งตัวต่อสิ่งเร้า เช่น หดตัวเมื่อถูกสัมผัส"),
    ("พลานาเรีย", "ปมประสาทที่หัวและเส้นประสาทแบบขั้นบันได", "แทกซิส และเรียนรู้อย่างง่ายได้บ้าง"),
    ("แมลง", "ปมประสาทสมองและเส้นประสาทด้านท้อง", "สัญชาตญาณซับซ้อน เช่น การสร้างรัง และเรียนรู้ได้"),
    ("สัตว์เลี้ยงลูกด้วยน้ำนม", "สมองส่วนหน้าเจริญมาก", "เรียนรู้ได้หลายแบบ และบางชนิดใช้เหตุผลได้"),
)


EVOL_HINT = ("ระบบประสาทยิ่งซับซ้อน พฤติกรรมยิ่งซับซ้อน สัตว์ที่ระบบประสาทง่ายแสดงพฤติกรรมแต่กำเนิดเป็นหลัก "
             "สัตว์ที่สมองเจริญมากเรียนรู้และใช้เหตุผลได้")


EVOL_FACTS = (
    ("เหตุใดสัตว์ที่มีอายุขัยสั้นมักอาศัยพฤติกรรมแต่กำเนิดเป็นหลัก", "ไม่มีเวลาพอเรียนรู้ พฤติกรรมที่ติดตัวมาช่วยให้อยู่รอดได้ทันที",
     ("สัตว์เหล่านี้ไม่มีระบบประสาทเลย จึงแสดงได้เฉพาะพฤติกรรมแต่กำเนิด", "พฤติกรรมแต่กำเนิดต้องฝึกนาน", "พฤติกรรมเรียนรู้เป็นอันตรายเสมอ", "สิ่งแวดล้อมของสัตว์เหล่านี้ไม่เปลี่ยนแปลงเลย จึงไม่ต้องปรับพฤติกรรมใหม่",
      "สัตว์เหล่านี้ใช้เหตุผลได้ดีกว่า")),
    ("การที่สัตว์เลี้ยงลูกด้วยน้ำนมเลี้ยงลูกนานเกี่ยวข้องกับพฤติกรรมอย่างไร", "ลูกมีเวลาเรียนรู้พฤติกรรมที่ซับซ้อนจากพ่อแม่",
     ("ทำให้ลูกไม่ต้องเรียนรู้อะไรเลยเพราะพ่อแม่ทำให้", "ทำให้ระบบประสาทเล็กลง", "ทำให้พฤติกรรมแต่กำเนิดของลูกหายไปทั้งหมด", "ไม่มีความเกี่ยวข้องกัน",
      "ทำให้ลูกแสดงเฉพาะไคนีซิส")),
    ("พฤติกรรมการใช้เหตุผลพบในสัตว์กลุ่มใดเป็นหลัก", "สัตว์ที่สมองส่วนหน้าเจริญมาก เช่น ลิงชิมแปนซีและคน",
     ("สัตว์ที่มีร่างแหประสาท เช่น ไฮดราและแมงกะพรุน", "สิ่งมีชีวิตเซลล์เดียว เช่น อะมีบาและพารามีเซียม", "หนอนตัวแบนที่มีปมประสาท เช่น พลานาเรีย", "ฟองน้ำ", "แมงกะพรุน")),
    ("หนอนผีเสื้อที่ฟักออกจากไข่กินใบพืชชนิดที่แม่วางไข่ได้ทันทีโดยไม่ต้องเรียนรู้ แสดงถึงอะไร", "พฤติกรรมแต่กำเนิดที่ถูกกำหนดโดยพันธุกรรม",
     ("การเรียนรู้แบบใช้เหตุผลที่อาศัยประสบการณ์", "การฝังใจกับแม่", "การมีเงื่อนไข", "แฮบิชูเอชัน", "การเรียนรู้แบบลองผิดลองถูกจนจำได้")),
    ("กาและอีกาบางชนิดใช้กิ่งไม้เขี่ยหนอนออกจากโพรง แสดงว่าสัตว์เหล่านี้มีอะไร", "สมองที่เจริญพอจะเรียนรู้และแก้ปัญหาได้",
     ("ระบบประสาทแบบร่างแหที่ไม่มีสมองรวมศูนย์", "เฉพาะรีเฟล็กซ์อย่างง่ายที่ไม่ต้องใช้สมอง", "ไม่มีการเรียนรู้เลย", "เฉพาะไคนีซิส", "ไม่มีสมอง")),
    ("พฤติกรรมที่ช่วยให้สัตว์อยู่รอดมักถูกคัดเลือกไว้อย่างไร", "สัตว์ที่มีพฤติกรรมเหมาะสมอยู่รอดและมีลูกมาก ถ่ายทอดพฤติกรรมที่มีพันธุกรรมเป็นพื้นฐานต่อไป",
     ("สัตว์ตั้งใจเปลี่ยนพฤติกรรมของตนเอง แล้วถ่ายทอดพฤติกรรมที่เรียนรู้นั้นให้ลูกทางพันธุกรรม", "พฤติกรรมเกิดขึ้นแบบสุ่มโดยไม่มีผลต่อการอยู่รอด จึงถ่ายทอดต่อไปได้ทุกแบบเท่ากัน", "พฤติกรรมทุกชนิดถ่ายทอดทางพันธุกรรมได้ รวมทั้งพฤติกรรมที่เรียนรู้ภายหลัง", "สิ่งแวดล้อมไม่มีผล")),
)


@question_type(
    "biology.behavior_evolution_foundation",
    display_name={"th": "ความซับซ้อนของระบบประสาทกับพฤติกรรม"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_EVOL,
)
class BehaviorEvolutionFoundation(QuestionType):
    """Match nervous system and typical behaviour to the animal."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        animal, system, behaviour = rng.choice(LEVELS)
        others = rng.sample([ell for ell in LEVELS if ell[0] != animal], 3)
        roll = rng.random()
        if roll < 0.35:
            return _labelled(stem=f"{animal}มีระบบประสาทแบบใด", correct=system, wrongs=tuple(ell[1] for ell in others), topic=TOPIC_EVOL, hint=EVOL_HINT)
        if roll < 0.7:
            return _labelled(stem=f"{animal}แสดงพฤติกรรมลักษณะใดเป็นหลัก", correct=behaviour, wrongs=tuple(ell[2] for ell in others),
                             topic=TOPIC_EVOL, hint=EVOL_HINT)
        return _labelled(stem=f"สัตว์ที่มี{system} และแสดงพฤติกรรม{behaviour} คือข้อใด", correct=animal, wrongs=tuple(ell[0] for ell in others),
                         topic=TOPIC_EVOL, hint=EVOL_HINT)


@question_type(
    "biology.behavior_evolution_fluency",
    display_name={"th": "เรียงลำดับความซับซ้อนของพฤติกรรม"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_EVOL,
)
class BehaviorEvolutionFluency(QuestionType):
    """Simple to complex behaviours, and animals by what they can do."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            order = ["ไคนีซิส", "แทกซิส", "รีเฟล็กซ์ต่อเนื่อง", "การมีเงื่อนไข", "การใช้เหตุผล"]
            picked = sorted(rng.sample(range(len(order)), 3))
            chunk = [order[i] for i in picked]
            wrongs: dict[str, None] = {}   # insertion-ordered: a set's order changes per process
            while len(wrongs) < 3:
                c = chunk[:]
                rng.shuffle(c)
                if c != chunk:
                    wrongs[" → ".join(c)] = None
            return _labelled(stem="ข้อใดเรียงพฤติกรรมจากซับซ้อนน้อยไปมากได้ถูกต้อง", correct=" → ".join(chunk), wrongs=tuple(wrongs),
                             topic=TOPIC_EVOL, hint=EVOL_HINT)
        four = sorted(rng.sample(range(len(LEVELS)), 4))
        most = rng.random() < 0.5
        right = LEVELS[four[-1]][0] if most else LEVELS[four[0]][0]
        return _labelled(stem=f"สัตว์ใดน่าจะแสดงพฤติกรรมที่เกิดจากการเรียนรู้ได้{'มากที่สุด' if most else 'น้อยที่สุด'}", correct=right,
                         wrongs=tuple(LEVELS[i][0] for i in four if LEVELS[i][0] != right), topic=TOPIC_EVOL, hint=EVOL_HINT)


@question_type(
    "biology.behavior_evolution_application",
    display_name={"th": "อธิบายพฤติกรรมด้วยวิวัฒนาการของระบบประสาท"},
    level=UPPER_SIX, subject=SUBJECT, topic=TOPIC_EVOL,
)
class BehaviorEvolutionApplication(QuestionType):
    """Why lifespan, parental care and brains shape behaviour."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        stem, right, wrongs = rng.choice(EVOL_FACTS)
        return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_EVOL, hint=EVOL_HINT)
