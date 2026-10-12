"""วัตถุที่แม่เหล็กดึงดูด

ฟิสิกส์ · ป.3 · สสวท. พื้นฐาน
Indicators: ว 2.2 ป.3/3

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
from otk.sets._support.science_wave_d14 import SUBJECT, THIRD

PROVENANCE = Provenance("original")


MAGNET_SORT_TOPIC = "วัตถุที่แม่เหล็กดึงดูด"


ATTRACTED = ("ตะปูเหล็ก", "คลิปหนีบกระดาษเหล็ก", "เข็มเย็บผ้า", "ฝาขวดน้ำอัดลมที่ทำจากเหล็ก", "ลวดเหล็ก", "กระป๋องเหล็ก", "น็อตเหล็ก")


NOT_ATTRACTED = ("กระป๋องอะลูมิเนียม", "ลวดทองแดง", "ยางลบ", "ไม้บรรทัดพลาสติก", "ช้อนไม้", "แก้วน้ำ", "เหรียญทองเหลือง", "กระดาษ")


def _magnet_groups(yes: list[str], no: list[str]) -> str:
    return f"แม่เหล็กดึงดูด: {', '.join(yes)} / แม่เหล็กไม่ดึงดูด: {', '.join(no)}"


MAGNET_HINT = "แม่เหล็กดึงดูดวัตถุที่ทำจากเหล็ก ไม่ดึงดูดอะลูมิเนียม ทองแดง ทองเหลือง ยาง พลาสติก ไม้ แก้ว และกระดาษ"


MAGNET_SORT_SCENARIOS = (
    ("เข็มหมุดเหล็กหกปนกับทรายในกล่อง วิธีใดแยกเข็มหมุดได้รวดเร็วที่สุด",
     "ใช้แม่เหล็กดูด เพราะแม่เหล็กดึงดูดเข็มหมุดเหล็กแต่ไม่ดึงดูดทราย",
     ("ใช้ตะแกรงร่อน เพราะเข็มหมุดเล็กกว่าเม็ดทราย",
      "เทน้ำลงไป เข็มหมุดจะลอยขึ้นมา",
      "ใช้แม่เหล็กดูด เพราะแม่เหล็กดึงดูดทรายแต่ไม่ดึงดูดเข็มหมุด")),
    ("โรงงานรีไซเคิลต้องแยกกระป๋องเหล็กออกจากกระป๋องอะลูมิเนียม ควรใช้วิธีใด",
     "ใช้แม่เหล็กขนาดใหญ่ดูดกระป๋องเหล็กออก เพราะแม่เหล็กไม่ดึงดูดอะลูมิเนียม",
     ("ใช้แม่เหล็กดูดกระป๋องอะลูมิเนียมออก",
      "ใช้น้ำแยกเพราะกระป๋องเหล็กลอยน้ำ",
      "แยกไม่ได้ เพราะเป็นโลหะเหมือนกัน")),
    ("นักเรียนพบว่าเหรียญชนิดหนึ่งติดแม่เหล็ก แต่อีกชนิดหนึ่งไม่ติด ข้อสรุปใดเหมาะสมที่สุด",
     "เหรียญสองชนิดน่าจะทำจากโลหะต่างกัน ชนิดที่ติดแม่เหล็กน่าจะมีเหล็กเป็นส่วนผสม",
     ("โลหะทุกชนิดติดแม่เหล็ก จึงเป็นไปไม่ได้",
      "เหรียญที่ไม่ติดแม่เหล็กไม่ใช่โลหะ",
      "แม่เหล็กเสียจึงดูดได้เพียงเหรียญเดียว")),
)


@question_type(
    "phys.magnet_sort_foundation",
    display_name={"th": "บอกวัตถุที่แม่เหล็กดึงดูด"},
    level=THIRD, subject=SUBJECT, topic=MAGNET_SORT_TOPIC,
)
class MagnetSortFoundation(QuestionType):
    """Which of four objects a magnet attracts, or does not."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        yes = rng.random() < 0.6
        return _labelled(
            stem="วัตถุใดถูกแม่เหล็กดึงดูด" if yes else "วัตถุใดไม่ถูกแม่เหล็กดึงดูด",
            correct=rng.choice(ATTRACTED if yes else NOT_ATTRACTED),
            wrongs=tuple(NOT_ATTRACTED if yes else ATTRACTED),
            hint=MAGNET_HINT, topic=MAGNET_SORT_TOPIC,
        )


@question_type(
    "phys.magnet_sort_fluency",
    display_name={"th": "จำแนกวัตถุโดยใช้การดึงดูดกับแม่เหล็กเป็นเกณฑ์จากผลการทดสอบ"},
    level=THIRD, subject=SUBJECT, topic=MAGNET_SORT_TOPIC,
)
class MagnetSortFluency(QuestionType):
    """Five objects tested with a magnet; sort every one by the result."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        count = rng.choice((2, 3))
        chosen = rng.sample(ATTRACTED, count) + rng.sample(NOT_ATTRACTED, 5 - count)
        rng.shuffle(chosen)
        record = " / ".join(f"{o}: {'ติดแม่เหล็ก' if o in ATTRACTED else 'ไม่ติดแม่เหล็ก'}" for o in chosen)
        yes = [o for o in chosen if o in ATTRACTED]
        no = [o for o in chosen if o in NOT_ATTRACTED]
        wrongs = []
        for item in rng.sample(chosen, 3):
            if item in yes:
                wrongs.append(_magnet_groups([o for o in yes if o != item], no + [item]))
            else:
                wrongs.append(_magnet_groups(yes + [item], [o for o in no if o != item]))
        # Two objects misplaced at once, so the answer is not the grouping
        # every wrong differs from by a single move.
        for pair in (rng.sample(chosen, 2) for _ in range(2)):
            moved = set(pair)
            wrongs.append(_magnet_groups([o for o in yes if o not in moved] + [o for o in no if o in moved],
                                         [o for o in no if o not in moved] + [o for o in yes if o in moved]))
        wrongs = list(dict.fromkeys(wrongs))
        return _labelled(
            stem=f"นักเรียนนำแม่เหล็กไปแตะวัตถุ 5 ชิ้น ได้ผลดังนี้ — {record} ข้อใดจำแนกวัตถุได้ถูกต้อง",
            correct=_magnet_groups(yes, no),
            wrongs=tuple(wrongs),
            hint="ใช้ผลการทดสอบเป็นเกณฑ์: วัตถุที่ติดแม่เหล็กอยู่กลุ่มหนึ่ง วัตถุที่ไม่ติดอยู่อีกกลุ่มหนึ่ง",
            topic=MAGNET_SORT_TOPIC,
        )


@question_type(
    "phys.magnet_sort_application",
    display_name={"th": "ใช้การดึงดูดกับแม่เหล็กแยกวัตถุในชีวิตประจำวัน"},
    level=THIRD, subject=SUBJECT, topic=MAGNET_SORT_TOPIC,
)
class MagnetSortApplication(QuestionType):
    """Authored cases, and whether a magnet can separate a given mixture."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            return _retopic(scenario_question(rng, MAGNET_SORT_SCENARIOS, hint="แม่เหล็กดึงดูดสิ่งที่มีเหล็ก จึงใช้แยกสิ่งนั้นออกจากสิ่งอื่นได้"),
                            MAGNET_SORT_TOPIC)
        kind = rng.randrange(3)
        if kind == 0:
            a, b = rng.choice(ATTRACTED), rng.choice(NOT_ATTRACTED)
        elif kind == 1:
            a, b = rng.sample(ATTRACTED, 2)
        else:
            a, b = rng.sample(NOT_ATTRACTED, 2)
        if rng.random() < 0.5:
            a, b = b, a
        can = (a in ATTRACTED) != (b in ATTRACTED)
        pulled = a if a in ATTRACTED else b
        right = f"ได้ เพราะแม่เหล็กดึงดูด{pulled}เพียงอย่างเดียว" if can else (
            "ไม่ได้ เพราะแม่เหล็กดึงดูดทั้งสองอย่าง" if kind == 1 else "ไม่ได้ เพราะแม่เหล็กไม่ดึงดูดทั้งสองอย่าง")
        options = ("ไม่ได้ เพราะแม่เหล็กดึงดูดทั้งสองอย่าง", "ไม่ได้ เพราะแม่เหล็กไม่ดึงดูดทั้งสองอย่าง",
                   f"ได้ เพราะแม่เหล็กดึงดูด{a}เพียงอย่างเดียว", f"ได้ เพราะแม่เหล็กดึงดูด{b}เพียงอย่างเดียว")
        return _labelled(stem=f"{a}ปนอยู่กับ{b} ใช้แม่เหล็กแยกออกจากกันได้หรือไม่", correct=right,
                         wrongs=tuple(o for o in options if o != right)[:3], hint=MAGNET_HINT, topic=MAGNET_SORT_TOPIC)
