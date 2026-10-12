"""แรงสัมผัสและแรงไม่สัมผัส

ฟิสิกส์ · ป.3 · สสวท. พื้นฐาน
Indicators: ว 2.2 ป.3/2

Sets moved here from: science_wave_d14.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_b9 import scenario_question
from otk.sets._support.science_wave_b14 import _labelled
from otk.sets._support.science_wave_b15 import _retopic
from otk.sets._support.science_wave_d14 import KIDS, SUBJECT, THIRD

PROVENANCE = Provenance("original")


CONTACT_TOPIC = "แรงสัมผัสและแรงไม่สัมผัส"


CONTACT = (
    "ผลักประตูให้เปิด", "ดึงเชือกลากกล่อง", "เตะลูกบอล", "ใช้มือบีบลูกโป่ง", "ลมพัดใบเรือให้เรือแล่น",
    "ใช้ไม้ตีลูกปิงปอง", "ใช้นิ้วกดปุ่มกริ่ง", "ใช้มือปั้นดินน้ำมัน",
)


NON_CONTACT = (
    "แม่เหล็กดูดคลิปหนีบกระดาษโดยไม่แตะกัน", "ผลมะม่วงหล่นจากต้นลงพื้น",
    "หวีที่ถูกับผมดึงดูดเศษกระดาษชิ้นเล็ก", "แม่เหล็กสองแท่งผลักกันก่อนแตะกัน",
    "ลูกบอลที่โยนขึ้นตกกลับลงมา", "ลูกโป่งที่ถูกับผมดึงดูดเส้นผมโดยไม่แตะกัน",
)


def _sorted(contact: list[str], non_contact: list[str]) -> str:
    return (f"แรงสัมผัส ต้องแตะวัตถุ: {', '.join(contact)} / "
            f"แรงไม่สัมผัส ไม่ต้องแตะวัตถุ: {', '.join(non_contact)}")


CONTACT_SCENARIOS = (
    ("นักเรียนถือแม่เหล็กไว้ใต้โต๊ะไม้บาง ๆ แล้วเลื่อนไปมา คลิปหนีบกระดาษบนโต๊ะเคลื่อนที่ตาม ข้อใดอธิบายได้ถูกต้อง",
     "แรงแม่เหล็กเป็นแรงไม่สัมผัส จึงกระทำต่อคลิปได้แม้มีโต๊ะกั้นและไม่ได้แตะกัน",
     ("แม่เหล็กแตะคลิปผ่านรูเล็ก ๆ บนโต๊ะ",
      "โต๊ะไม้ผลักคลิปให้เคลื่อนที่",
      "คลิปเคลื่อนที่เองโดยไม่มีแรง")),
    ("ข้อใดมีทั้งแรงสัมผัสและแรงไม่สัมผัสกระทำต่อวัตถุเดียวกัน",
     "นักเรียนโยนลูกบอลขึ้นด้วยมือ แล้วลูกบอลตกลงมาเพราะแรงโน้มถ่วง",
     ("นักเรียนผลักโต๊ะไปชิดผนัง",
      "นักเรียนดึงลิ้นชักออก",
      "นักเรียนบีบฟองน้ำ")),
    ("ทำไมผลไม้ที่หลุดจากกิ่งจึงตกลงพื้นทั้งที่ไม่มีใครแตะ",
     "โลกดึงดูดผลไม้ด้วยแรงโน้มถ่วง ซึ่งเป็นแรงไม่สัมผัส",
     ("ลมผลักผลไม้ลงพื้นเสมอ",
      "กิ่งไม้ผลักผลไม้ลงมา",
      "ผลไม้ไม่มีแรงกระทำจึงตกลงเอง")),
)


FORCE_EVENTS = (
    ("ลูกมะพร้าวหล่นจากต้น", "แรงโน้มถ่วงของโลก ซึ่งเป็นแรงไม่สัมผัส"),
    ("คลิปเหล็กวิ่งเข้าหาแม่เหล็กที่อยู่ห่างออกไป", "แรงแม่เหล็ก ซึ่งเป็นแรงไม่สัมผัส"),
    ("เศษกระดาษลอยขึ้นติดลูกโป่งที่ถูกับผม", "แรงไฟฟ้า ซึ่งเป็นแรงไม่สัมผัส"),
    ("กล่องที่ถูกลากไปตามพื้นเคลื่อนที่ช้าลงจนหยุดเมื่อปล่อยมือ", "แรงเสียดทานจากพื้น ซึ่งเป็นแรงสัมผัส"),
    ("ลูกบอลพุ่งออกไปเมื่อถูกเตะ", "แรงจากเท้าที่เตะ ซึ่งเป็นแรงสัมผัส"),
    ("สปริงที่ถูกกดดันนิ้วมือกลับขึ้นมา", "แรงดึงกลับของสปริง ซึ่งเป็นแรงสัมผัส"),
)


@question_type(
    "phys.contact_force_foundation",
    display_name={"th": "บอกความแตกต่างของแรงสัมผัสและแรงไม่สัมผัส"},
    level=THIRD, subject=SUBJECT, topic=CONTACT_TOPIC,
)
class ContactForceFoundation(QuestionType):
    """One activity's kind of force, or which of four activities is the other kind."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        contact = rng.random() < 0.5
        if rng.random() < 0.5:
            return _labelled(stem=f"ข้อใดเป็นแรง{'สัมผัส' if contact else 'ไม่สัมผัส'}", correct=rng.choice(CONTACT if contact else NON_CONTACT),
                             wrongs=tuple(NON_CONTACT if contact else CONTACT), hint="ถามว่าสิ่งที่ออกแรงแตะวัตถุหรือไม่",
                             topic=CONTACT_TOPIC)
        activity = rng.choice(CONTACT if contact else NON_CONTACT)
        yes = "แรงสัมผัส เพราะสิ่งที่ออกแรงต้องแตะวัตถุ"
        no = "แรงไม่สัมผัส เพราะแรงกระทำได้โดยไม่ต้องแตะวัตถุ"
        return _labelled(
            stem=f"\"{activity}\" เป็นแรงแบบใด",
            correct=yes if contact else no,
            wrongs=(no if contact else yes,
                    "แรงสัมผัส เพราะแรงกระทำได้โดยไม่ต้องแตะวัตถุ" if contact
                    else "แรงไม่สัมผัส เพราะสิ่งที่ออกแรงต้องแตะวัตถุ",
                    "ไม่มีแรงกระทำ เพราะวัตถุเคลื่อนที่เอง"),
            hint="ถามว่าสิ่งที่ออกแรงแตะวัตถุหรือไม่",
            topic=CONTACT_TOPIC,
        )


@question_type(
    "phys.contact_force_fluency",
    display_name={"th": "เปรียบเทียบและยกตัวอย่างแรงสัมผัสและแรงไม่สัมผัสจากหลักฐาน"},
    level=THIRD, subject=SUBJECT, topic=CONTACT_TOPIC,
)
class ContactForceFluency(QuestionType):
    """Five observed activities; sort every one, with what tells the two apart."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        count = rng.choice((2, 3))
        chosen = rng.sample(CONTACT, count) + rng.sample(NON_CONTACT, 5 - count)
        rng.shuffle(chosen)
        contact = [a for a in chosen if a in CONTACT]
        non_contact = [a for a in chosen if a in NON_CONTACT]
        wrongs = []
        for item in rng.sample(chosen, 3):
            if item in contact:
                wrongs.append(_sorted([a for a in contact if a != item], non_contact + [item]))
            else:
                wrongs.append(_sorted(contact + [item], [a for a in non_contact if a != item]))
        # Two activities misplaced at once, so the answer is not the choice
        # every wrong differs from by a single move.
        for pair in (rng.sample(chosen, 2) for _ in range(2)):
            moved = set(pair)
            wrongs.append(_sorted([a for a in contact if a not in moved] + [a for a in non_contact if a in moved],
                                  [a for a in non_contact if a not in moved] + [a for a in contact if a in moved]))
        return _labelled(
            stem=(f"นักเรียนสังเกตกิจกรรมต่อไปนี้ ได้แก่ {', '.join(chosen)} "
                  "ข้อใดเปรียบเทียบและยกตัวอย่างแรงสัมผัสและแรงไม่สัมผัสได้ถูกต้อง"),
            correct=_sorted(contact, non_contact),
            wrongs=tuple(dict.fromkeys(wrongs)),
            hint="ถามทีละกิจกรรมว่าสิ่งที่ออกแรงแตะวัตถุหรือไม่",
            topic=CONTACT_TOPIC,
        )


@question_type(
    "phys.contact_force_application",
    display_name={"th": "ใช้แรงสัมผัสและแรงไม่สัมผัสอธิบายสถานการณ์"},
    level=THIRD, subject=SUBJECT, topic=CONTACT_TOPIC,
)
class ContactForceApplication(QuestionType):
    """Authored cases, and naming the force in an event with its kind."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            return _retopic(scenario_question(rng, CONTACT_SCENARIOS,
                                              hint="แรงไม่สัมผัส เช่น แรงแม่เหล็ก แรงไฟฟ้า และแรงโน้มถ่วง กระทำได้โดยไม่ต้องแตะ"), CONTACT_TOPIC)
        event, force = rng.choice(FORCE_EVENTS)
        others = [f for _, f in FORCE_EVENTS if f != force]
        kid = rng.choice(KIDS)
        return _labelled(stem=f"{kid}สังเกตเห็น{event} แรงใดเป็นสาเหตุ และเป็นแรงแบบใด", correct=force, wrongs=tuple(others),
                         hint="แรงไม่สัมผัส เช่น แรงแม่เหล็ก แรงไฟฟ้า และแรงโน้มถ่วง กระทำได้โดยไม่ต้องแตะ", topic=CONTACT_TOPIC)
