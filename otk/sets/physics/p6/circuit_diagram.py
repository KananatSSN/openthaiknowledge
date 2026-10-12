"""แผนภาพและการต่อวงจรไฟฟ้าอย่างง่าย

ฟิสิกส์ · ป.6 · สสวท. พื้นฐาน
Indicators: ว 2.3 ป.6/2

Sets moved here from: science_wave_d26.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.circuit_symbols import FAULT_CIRCUITS, diagram_question, layout_alt
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d14 import SUBJECT
from otk.sets._support.science_wave_d26 import SIXTH

PROVENANCE = Provenance("original")


CIRCUIT_DIAGRAM_TOPIC = "แผนภาพและการต่อวงจรไฟฟ้าอย่างง่าย"


CIRCUIT_DIAGRAM_FACTS = (
    ("เหตุใดจึงใช้สัญลักษณ์แทนส่วนประกอบเมื่อเขียนแผนภาพวงจรไฟฟ้า", "เพื่อให้สื่อสารและเข้าใจตรงกันได้ง่ายและรวดเร็ว",
     ("เพราะกฎหมายห้ามวาดรูปจริง", "เพราะสัญลักษณ์ทำให้วงจรทำงานดีขึ้น", "เพราะอุปกรณ์จริงไม่มีรูปร่างแน่นอน",
      "เพื่อให้แผนภาพมีสีสวยงาม", "เพราะสัญลักษณ์ทำให้ไฟฟ้าไหลเร็วขึ้น")),
    ("ในแผนภาพวงจรไฟฟ้า เส้นตรงที่เชื่อมสัญลักษณ์แทนสิ่งใด", "สายไฟ",
     ("หลอดไฟ", "เซลล์ไฟฟ้า", "สวิตช์", "กระแสไฟฟ้าที่ไหลย้อนกลับ", "ขอบของโต๊ะที่วางวงจร")),
    ("สัญลักษณ์เซลล์ไฟฟ้ามีเส้นยาวและเส้นสั้น เส้นยาวแทนสิ่งใด", "ขั้วบวก",
     ("ขั้วลบ", "สายดิน", "สวิตช์", "หลอดไฟ", "ความยาวของถ่าน")),
    ("แผนภาพวงจรที่หลอดไฟจะสว่างได้ต้องมีลักษณะใด", "เส้นจากขั้วหนึ่งของเซลล์ไฟฟ้าผ่านหลอดไฟกลับถึงอีกขั้วหนึ่งครบเป็นวงปิด",
     ("มีเส้นเชื่อมเพียงด้านเดียว", "มีสวิตช์เปิดวงจรอยู่", "หลอดไฟอยู่นอกวง", "เซลล์ไฟฟ้าอยู่ห่างจากหลอดมาก ๆ",
      "เส้นเชื่อมทุกเส้นขาดตรงกลาง")),
    ("ประโยชน์ของการเขียนแผนภาพวงจรก่อนต่อวงจรจริงคือข้อใด", "ช่วยวางแผนการต่อให้ครบวงจรและตรวจหาจุดผิดได้ก่อนลงมือ",
     ("ทำให้ถ่านไฟฉายใช้ได้นานขึ้น", "ทำให้หลอดไฟสว่างขึ้น", "ไม่จำเป็นต้องมีสายไฟ", "ทำให้วงจรไม่ต้องมีเซลล์ไฟฟ้า",
      "ทำให้กระแสไฟฟ้าไหลได้โดยไม่ต้องต่อครบวงจร")),
)


CIRCUIT_DIAGRAM_SCENARIOS = (
    ("เพื่อนวาดแผนภาพวงจรไฟฟ้าโดยต่อเซลล์ไฟฟ้า สายไฟ และหลอดไฟเป็นเส้นตรงยาวโดยไม่บรรจบกันเป็นวง ข้อใดแก้ไขได้ถูกต้อง",
     "ต้องต่อสายไฟให้ครบเป็นวงปิด โดยปลายทั้งสองข้างของวงจรเชื่อมต่อกลับมาที่เซลล์ไฟฟ้า",
     ("ถูกต้องแล้ว วงจรไฟฟ้าไม่จำเป็นต้องเป็นวงปิด", "ควรต่อเซลล์ไฟฟ้าเพิ่มอีกหนึ่งเซลล์แทนการแก้ไขรูปวงจร", "ควรตัดหลอดไฟออกจากวงจรแทน")),
    ("นักเรียนสองคนต่อวงจรไฟฟ้าอย่างง่ายเหมือนกันทุกส่วนประกอบ แต่คนหนึ่งวาดแผนภาพก่อนต่อจริง อีกคนต่อวงจรทันทีโดยไม่วาดแผนภาพ ข้อใดเป็นประโยชน์ของการวาดแผนภาพก่อน",
     "ช่วยวางแผนตำแหน่งการต่อส่วนประกอบให้ครบวงจรได้ถูกต้องก่อนลงมือต่อจริง ลดโอกาสต่อผิดพลาด",
     ("การวาดแผนภาพไม่มีประโยชน์ใด ๆ ต่อการต่อวงจรจริง", "การวาดแผนภาพทำให้วงจรไฟฟ้าทำงานได้แรงขึ้น", "การวาดแผนภาพจำเป็นต้องใช้แทนการต่อวงจรจริงเสมอ")),
    ("วงจรไฟฟ้าหนึ่งต่อสวิตช์ผิดตำแหน่ง โดยต่อสวิตช์ขนานกับหลอดไฟแทนที่จะต่ออนุกรมในเส้นทางหลัก คาดว่าจะเกิดอะไรขึ้นเมื่อกดสวิตช์",
     "หลอดไฟอาจสว่างตลอดเวลาโดยสวิตช์ไม่สามารถตัดวงจรของหลอดไฟได้ตามที่ตั้งใจ",
     ("หลอดไฟจะดับสนิทตลอดเวลาไม่ว่าสวิตช์จะอยู่ตำแหน่งใด", "ตำแหน่งของสวิตช์ในวงจรไม่มีผลต่อการทำงานเลย", "วงจรจะลัดวงจรทันทีไม่ว่าสวิตช์จะอยู่ตำแหน่งใด")),
)


@question_type(
    "phys.circuit_diagram_foundation",
    display_name={"th": "บอกเหตุผลของการใช้สัญลักษณ์ในแผนภาพวงจรไฟฟ้า"},
    level=SIXTH, subject=SUBJECT, topic=CIRCUIT_DIAGRAM_TOPIC,
)
class CircuitDiagramFoundation(QuestionType):
    """Why symbols, what a diagram needs, and which symbols a described circuit takes."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.35:
            stem, right, wrongs = rng.choice(CIRCUIT_DIAGRAM_FACTS)
            return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs),
                             hint="แผนภาพวงจรใช้สัญลักษณ์แทนอุปกรณ์ และเส้นตรงแทนสายไฟที่ต่อครบเป็นวงปิด",
                             topic=CIRCUIT_DIAGRAM_TOPIC)
        if roll < 0.8:
            cells, bulbs = rng.randint(1, 3), rng.randint(1, 3)
            switch = rng.random() < 0.6
            parts = f"ถ่านไฟฉาย {cells} ก้อน หลอดไฟ {bulbs} ดวง" + (" และสวิตช์ 1 ตัว" if switch else "")
            right = (f"สัญลักษณ์เซลล์ไฟฟ้า {cells} อัน หลอดไฟ {bulbs} อัน"
                     + (" และสวิตช์ 1 อัน" if switch else "") + " เชื่อมกันด้วยเส้นแทนสายไฟ")
            wrongs = [f"สัญลักษณ์เซลล์ไฟฟ้า {bulbs if bulbs != cells else cells + 1} อัน หลอดไฟ {cells if bulbs != cells else bulbs + 1} อัน"
                      + (" และสวิตช์ 1 อัน" if switch else "") + " เชื่อมกันด้วยเส้นแทนสายไฟ",
                      "วาดรูปถ่านไฟฉาย หลอดไฟ และสายไฟให้เหมือนของจริงทุกส่วน",
                      f"สัญลักษณ์เซลล์ไฟฟ้า {cells} อัน หลอดไฟ {bulbs} อัน"
                      + (" และสวิตช์ 1 อัน" if switch else "") + " โดยไม่ต้องลากเส้นเชื่อมให้ครบวง",
                      f"สัญลักษณ์เซลล์ไฟฟ้า 1 อันเสมอ ไม่ว่าจะใช้ถ่านกี่ก้อน และหลอดไฟ {bulbs} อัน"]
            return _labelled(
                stem=f"วงจรไฟฟ้าประกอบด้วย{parts} ต่อครบวงจร ถ้าเขียนเป็นแผนภาพวงจรไฟฟ้า ต้องมีสัญลักษณ์ใดบ้าง",
                correct=right, wrongs=tuple(w for w in dict.fromkeys(wrongs) if w != right)[:3],
                hint="อุปกรณ์แต่ละชิ้นในวงจรจริงใช้สัญลักษณ์หนึ่งอัน และลากเส้นแทนสายไฟให้ครบเป็นวงปิด",
                topic=CIRCUIT_DIAGRAM_TOPIC,
            )
        return _labelled(
            stem="เหตุใดจึงใช้สัญลักษณ์แทนส่วนประกอบเมื่อเขียนแผนภาพวงจรไฟฟ้า แทนที่จะวาดรูปจริง",
            correct="เพื่อให้สื่อสารและเข้าใจตรงกันได้ง่ายและรวดเร็วกว่าวาดรูปจริงที่ซับซ้อน",
            wrongs=("เพราะกฎหมายห้ามวาดรูปส่วนประกอบจริงในแผนภาพวงจร",
                    "เพราะการใช้สัญลักษณ์ทำให้วงจรไฟฟ้าทำงานได้ดีขึ้น",
                    "เพราะส่วนประกอบไฟฟ้าจริงไม่มีรูปร่างที่แน่นอน"),
            hint="สัญลักษณ์เป็นภาษากลางที่ทุกคนเข้าใจตรงกัน ไม่เกี่ยวกับรูปร่างจริงของอุปกรณ์",
            topic=CIRCUIT_DIAGRAM_TOPIC,
        )


@question_type(
    "phys.circuit_diagram_fluency",
    display_name={"th": "อ่านแผนภาพวงจรไฟฟ้าแล้วบอกว่าหลอดไฟสว่างหรือไม่"},
    level=SIXTH, subject=SUBJECT, topic=CIRCUIT_DIAGRAM_TOPIC,
)
class CircuitDiagramFluency(QuestionType):
    """A drawn circuit; whether it is complete, and so whether the bulb lights.

    The indicator is about แผนภาพ, so this shows one rather than describing one.
    The pool holds working circuits, circuits with the switch left open and
    circuits with a wire that does not reach the corner, so neither answer is
    ever the safe guess. The alt text stays with ``layout_alt``: what is wrong
    with the picture is exactly what the question asks.
    """

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        spec = rng.choice(FAULT_CIRCUITS)
        if spec.lights:
            correct = "สว่าง เพราะวงจรต่อครบเป็นวงปิด กระแสไฟฟ้าจึงไหลผ่านได้"
        elif spec.switch == "open":
            correct = "ไม่สว่าง เพราะสวิตช์ยังเปิดวงจรอยู่ กระแสไฟฟ้าจึงไหลผ่านไม่ได้"
        else:
            correct = "ไม่สว่าง เพราะมีสายไฟที่ยังไม่เชื่อมถึงกัน วงจรจึงไม่ครบวงจร"
        wrongs = tuple(c for c in (
            "สว่าง เพราะวงจรต่อครบเป็นวงปิด กระแสไฟฟ้าจึงไหลผ่านได้",
            "ไม่สว่าง เพราะสวิตช์ยังเปิดวงจรอยู่ กระแสไฟฟ้าจึงไหลผ่านไม่ได้",
            "ไม่สว่าง เพราะมีสายไฟที่ยังไม่เชื่อมถึงกัน วงจรจึงไม่ครบวงจร",
        ) if c != correct) + (rng.choice(("สว่างแต่หรี่ลง เพราะกระแสไฟฟ้าไหลผ่านได้เพียงบางส่วน",
                                          "สว่างเฉพาะหลอดที่อยู่ใกล้เซลล์ไฟฟ้าที่สุด",
                                          "ไม่สว่าง เพราะเซลล์ไฟฟ้าในแผนภาพมีมากเกินไป")),)
        return diagram_question(
            spec.asset_id, layout_alt(spec),
            stem="จากแผนภาพ หลอดไฟในวงจรนี้จะสว่างหรือไม่ เพราะเหตุใด",
            correct=correct,
            wrongs=wrongs,
            hint="ไล่สายไฟจากขั้วหนึ่งของเซลล์ไฟฟ้าไปรอบวงจร ถ้ากลับมาถึงอีกขั้วได้โดยไม่ขาดตอน วงจรนั้นครบวงจร",
            topic=CIRCUIT_DIAGRAM_TOPIC,
        )


@question_type(
    "phys.circuit_diagram_application",
    display_name={"th": "ตรวจสอบและแก้ไขการต่อวงจรไฟฟ้าจากแผนภาพ"},
    level=SIXTH, subject=SUBJECT, topic=CIRCUIT_DIAGRAM_TOPIC,
)
class CircuitDiagramApplication(QuestionType):
    """Authored cases, and a described diagram with one bulb burnt out."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.6:
            cells, bulbs = rng.randint(1, 3), rng.randint(2, 3)
            series = rng.random() < 0.5
            wiring = "อนุกรม" if series else "ขนาน"
            series_answer = "หลอดไฟดวงที่เหลือดับทั้งหมด เพราะวงจรอนุกรมมีเส้นทางเดียว ขาดตอนเดียวก็ไม่ครบวงจร"
            parallel_answer = "หลอดไฟดวงที่เหลือยังสว่าง เพราะแต่ละดวงมีเส้นทางของกระแสไฟฟ้าเป็นของตัวเอง"
            return _labelled(
                stem=(f"แผนภาพวงจรแสดงเซลล์ไฟฟ้า {cells} เซลล์ต่ออนุกรม และหลอดไฟ {bulbs} ดวงต่อแบบ{wiring} "
                      "สวิตช์ปิดวงจรอยู่ ถ้าหลอดไฟดวงหนึ่งขาด จะเกิดอะไรขึ้น"),
                correct=series_answer if series else parallel_answer,
                wrongs=(parallel_answer if series else series_answer,
                        *rng.sample(("หลอดไฟดวงที่เหลือสว่างจ้าขึ้นจนขาดตามทันที",
                                     "เซลล์ไฟฟ้าหยุดทำงานทุกเซลล์ แม้จะเปลี่ยนหลอดใหม่แล้วก็ตาม",
                                     "หลอดไฟดวงที่ขาดกลับมาสว่างเองเมื่อปิดเปิดสวิตช์",
                                     "สายไฟทุกเส้นในวงจรร้อนจนละลาย"), 2)),
                hint="วงจรอนุกรมมีทางเดินของกระแสทางเดียว วงจรขนานมีหลายทาง ทางหนึ่งขาดทางอื่นยังใช้ได้",
                topic=CIRCUIT_DIAGRAM_TOPIC,
            )
        return _retopic(scenario_question(
            rng, CIRCUIT_DIAGRAM_SCENARIOS,
            hint="ตรวจสอบว่าวงจรต่อครบเป็นวงปิดหรือไม่ และแต่ละส่วนประกอบอยู่ในเส้นทางที่ถูกต้องหรือไม่",
        ), CIRCUIT_DIAGRAM_TOPIC)
