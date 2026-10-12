"""แรงไฟฟ้าจากการขัดถู

ฟิสิกส์ · ป.6 · สสวท. พื้นฐาน
Indicators: ว 2.2 ป.6/1

Sets moved here from: science_wave_d17.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_c23 import Part
from otk.sets._support.science_wave_c24 import parts_item
from otk.sets._support.science_wave_d14 import SUBJECT

PROVENANCE = Provenance("original")


SIXTH = {"th": "ป.6"}


STATIC_TOPIC = "แรงไฟฟ้าจากการขัดถู"


RUBBINGS = (
    ("ลูกโป่ง", "ผม"),
    ("แท่งพลาสติก", "ผ้าขนสัตว์"),
    ("หวีพลาสติก", "ผ้าแห้ง"),
    ("ไม้บรรทัดพลาสติก", "เสื้อไหมพรม"),
)


def static_parts(thing: str, cloth: str) -> tuple[Part, ...]:
    return (
        Part("การเกิด", f"การขัดถู{thing}กับ{cloth}ทำให้วัตถุทั้งสองมีประจุไฟฟ้า",
             f"การขัดถู{thing}กับ{cloth}ทำให้{thing}มีน้ำหนักเพิ่มขึ้น"),
        Part(f"{thing}สองอันที่ขัดถูแบบเดียวกัน", "มีประจุชนิดเดียวกันจึงผลักกัน",
             "มีประจุชนิดเดียวกันจึงดึงดูดกัน"),
        Part("เศษกระดาษที่ไม่ได้ขัดถู", f"ถูก{thing}ที่มีประจุดึงดูดเข้าหา",
             f"ถูก{thing}ที่มีประจุผลักออกทุกครั้ง"),
    )


STATIC_FACTS = (
    ("การขัดถูวัตถุบางชนิดเข้าด้วยกันทำให้เกิดสิ่งใด", "ประจุไฟฟ้าบนวัตถุ", ("แม่เหล็กบนวัตถุ", "น้ำหนักเพิ่มขึ้น", "วัตถุละลาย", "วัตถุมีสีเปลี่ยนไป", "แสงสว่างตลอดเวลา")),
    ("วัตถุที่มีประจุไฟฟ้ามีผลต่อเศษกระดาษชิ้นเล็กที่ไม่มีประจุอย่างไร", "ดึงดูดเศษกระดาษเข้าหา",
     ("ผลักเศษกระดาษออกไปเสมอ", "ไม่มีผลใด ๆ", "ทำให้เศษกระดาษลุกไหม้", "ทำให้เศษกระดาษเปียก", "ทำให้เศษกระดาษหนักขึ้น")),
    ("ประจุไฟฟ้ามีกี่ชนิด", "สองชนิด คือประจุบวกและประจุลบ", ("ชนิดเดียว", "สามชนิด", "ไม่มีชนิด", "สองชนิด คือประจุเหนือและประจุใต้", "สี่ชนิด")),
    ("ในวันที่อากาศชื้น การทดลองขัดถูลูกโป่งมักดูดเศษกระดาษได้น้อยลง เพราะเหตุใด", "ความชื้นในอากาศทำให้ประจุไฟฟ้ารั่วไหลออกจากวัตถุได้ง่าย",
     ("อากาศชื้นทำให้ลูกโป่งหนักขึ้น", "อากาศชื้นทำให้เศษกระดาษมีแม่เหล็ก", "ความชื้นเพิ่มประจุไฟฟ้า", "อากาศชื้นไม่มีผลใด ๆ", "ลูกโป่งละลายในอากาศชื้น")),
)


STATIC_HINT = "การขัดถูทำให้เกิดประจุไฟฟ้า ประจุชนิดเดียวกันผลักกัน ประจุต่างชนิดกันดึงดูดกัน และวัตถุมีประจุดึงดูดวัตถุเล็ก ๆ ที่ไม่มีประจุ"


STATIC_SCENARIOS = (
    ("ในวันที่อากาศแห้ง เมื่อถอดเสื้อไหมพรมบางครั้งได้ยินเสียงเปาะแปะและผมชี้ฟู เพราะเหตุใด",
     "การขัดถูระหว่างเสื้อกับผมทำให้เกิดประจุไฟฟ้า เส้นผมที่มีประจุชนิดเดียวกันจึงผลักกันจนชี้ฟู",
     ("เสื้อไหมพรมมีแม่เหล็กอยู่ข้างใน", "ผมเปียกน้ำจึงชี้ฟู", "อากาศแห้งทำให้ผมมีน้ำหนักเพิ่มขึ้น")),
    ("เหตุใดหน้าจอโทรทัศน์หรือจอคอมพิวเตอร์จึงมักมีฝุ่นเกาะ",
     "หน้าจอมีประจุไฟฟ้าจึงดึงดูดฝุ่นซึ่งเป็นวัตถุเล็ก ๆ",
     ("ฝุ่นมีแม่เหล็กจึงเกาะหน้าจอ", "หน้าจอเปียกจึงมีฝุ่นเกาะ", "ฝุ่นถูกแรงโน้มถ่วงดึงขึ้นไปบนหน้าจอ")),
    ("รถบรรทุกน้ำมันมักมีโซ่โลหะลากติดพื้น เพื่อประโยชน์ใด",
     "ถ่ายเทประจุไฟฟ้าที่เกิดจากการเสียดสีลงสู่พื้น ป้องกันประกายไฟที่อาจจุดน้ำมัน",
     ("ช่วยให้รถแล่นเร็วขึ้น", "ช่วยเบรกรถให้หยุดเร็วขึ้น", "ทำให้รถมีน้ำหนักมากขึ้นเพื่อไม่ให้ล้ม")),
)


STATIC_EVENTS = ("ลูกโป่งที่ถูกับผมแล้วติดผนังได้", "ผมชี้ฟูหลังหวีผมในวันอากาศแห้ง", "ถูกไฟช็อตเมื่อจับลูกบิดหลังเดินบนพรม",
                 "เศษกระดาษลอยขึ้นติดหวีที่เพิ่งหวีผม", "เสื้อผ้าใยสังเคราะห์ติดกันหลังอบผ้า", "ฟ้าผ่าในวันที่มีพายุฝนฟ้าคะนอง")


OTHER_EVENTS = ("ตะปูเหล็กติดแม่เหล็กเมื่อนำมาใกล้กัน", "ผลไม้หล่นจากต้นลงพื้นเมื่อลมพัด", "เข็มทิศชี้ทิศเหนือเมื่อวางบนโต๊ะ",
                "ลูกบอลกลิ้งช้าลงบนสนามหญ้าจนหยุด", "เรือลอยน้ำได้แม้จะบรรทุกของหนัก")


@question_type(
    "phys.static_force_foundation",
    display_name={"th": "บอกผลระหว่างประจุไฟฟ้าชนิดเดียวกันและต่างชนิดกัน"},
    level=SIXTH, subject=SUBJECT, topic=STATIC_TOPIC,
)
class StaticForceFoundation(QuestionType):
    """Like or unlike charges; attract or repel; and facts about rubbing."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.5:
            stem, right, wrongs = rng.choice(STATIC_FACTS)
            return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), hint=STATIC_HINT, topic=STATIC_TOPIC)
        same = rng.random() < 0.5
        a, b = rng.sample(("ลูกโป่ง ก", "ลูกโป่ง ข", "แท่งพลาสติก", "หวี", "ไม้บรรทัดพลาสติก", "แท่งแก้ว"), 2)
        pair = rng.choice((("บวก", "บวก"), ("ลบ", "ลบ"))) if same else rng.choice((("บวก", "ลบ"), ("ลบ", "บวก")))
        return _labelled(
            stem=f"{a}มีประจุ{pair[0]} {b}มีประจุ{pair[1]} เมื่อนำเข้าใกล้กันจะเกิดผลอย่างไร",
            correct="ผลักกัน" if same else "ดึงดูดกัน",
            wrongs=("ดึงดูดกัน" if same else "ผลักกัน", "ไม่เกิดแรงใด ๆ", "ติดไฟทันที"),
            hint=STATIC_HINT, topic=STATIC_TOPIC,
        )


@question_type(
    "phys.static_force_fluency",
    display_name={"th": "อธิบายการเกิดและผลของแรงไฟฟ้าจากการขัดถูจากหลักฐาน"},
    level=SIXTH, subject=SUBJECT, topic=STATIC_TOPIC,
)
class StaticForceFluency(QuestionType):
    """A rubbing record explained part by part, or what two rubbed objects' behaviour shows."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        thing, cloth = rng.choice(RUBBINGS)
        if rng.random() < 0.4:
            return parts_item(
                rng, static_parts(thing, cloth),
                stem=(f"นักเรียนนำ{thing}ขัดถูกับ{cloth} แล้วสังเกตได้ว่า — {thing}ดูดเศษกระดาษชิ้นเล็กได้ / "
                      f"เมื่อนำ{thing}อีกอันที่ขัดถูแบบเดียวกันมาใกล้กัน {thing}ทั้งสองเคลื่อนที่ออกห่างจากกัน / "
                      f"ก่อนขัดถู {thing}ไม่ดูดเศษกระดาษ จากหลักฐานนี้ ข้อใดอธิบายการเกิดและผลของแรงไฟฟ้าได้ถูกต้องทั้งหมด"),
                hint="เทียบก่อนและหลังขัดถู แล้วแยกผลที่เกิดกับวัตถุที่มีประจุเหมือนกัน และกับเศษกระดาษที่ไม่ได้ขัดถู",
                topic=STATIC_TOPIC,
            )
        other, cloth2 = rng.choice([r for r in RUBBINGS if r[0] != thing])
        repel = rng.random() < 0.5
        seen = "เคลื่อนที่ออกห่างจากกัน" if repel else "เคลื่อนที่เข้าหากัน"
        right = "มีประจุไฟฟ้าชนิดเดียวกัน" if repel else "มีประจุไฟฟ้าต่างชนิดกัน"
        return _labelled(stem=f"นักเรียนนำ{thing}ที่ขัดถูกับ{cloth}แล้ว ไปใกล้{other}ที่ขัดถูกับ{cloth2}แล้ว พบว่าทั้งสอง{seen} "
                              f"จากหลักฐานนี้ ข้อใดสรุปได้ถูกต้อง",
                         correct=right, wrongs=("มีประจุไฟฟ้าต่างชนิดกัน" if repel else "มีประจุไฟฟ้าชนิดเดียวกัน", "ไม่มีประจุไฟฟ้าทั้งคู่",
                                                "เป็นแม่เหล็กทั้งคู่"),
                         hint=STATIC_HINT, topic=STATIC_TOPIC)


@question_type(
    "phys.static_force_application",
    display_name={"th": "ใช้แรงไฟฟ้าจากการขัดถูอธิบายปรากฏการณ์รอบตัว"},
    level=SIXTH, subject=SUBJECT, topic=STATIC_TOPIC,
)
class StaticForceApplication(QuestionType):
    """Authored cases, and which everyday event is caused by static charge."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            return _retopic(scenario_question(rng, STATIC_SCENARIOS, hint=STATIC_HINT), STATIC_TOPIC)
        yes = rng.random() < 0.6
        if yes:
            return _labelled(stem="เหตุการณ์ใดเกิดจากแรงไฟฟ้าที่เกิดจากการขัดถูหรือประจุไฟฟ้าสะสม", correct=rng.choice(STATIC_EVENTS),
                             wrongs=tuple(OTHER_EVENTS), hint=STATIC_HINT, topic=STATIC_TOPIC)
        return _labelled(stem="เหตุการณ์ใดไม่ได้เกิดจากแรงไฟฟ้าหรือประจุไฟฟ้าสะสม", correct=rng.choice(OTHER_EVENTS),
                         wrongs=tuple(STATIC_EVENTS), hint=STATIC_HINT, topic=STATIC_TOPIC)
