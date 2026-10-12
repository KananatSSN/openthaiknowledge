"""ลำดับเหตุการณ์ทางธรณีวิทยา

ธรณีวิทยา · ม.4 · สสวท. เพิ่มเติม
Indicators: โลก ดาราศาสตร์ และอวกาศเพิ่มเติม 1 ม.4/4

Sets moved here from: science_wave_f75.
"""

from __future__ import annotations

from fractions import Fraction
from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled, numeric
from otk.sets._support.science_wave_f75 import SUBJECT, UPPER_FOUR

PROVENANCE = Provenance("original")


TOPIC_HISTORY = "ลำดับเหตุการณ์ทางธรณีวิทยา"


PRINCIPLES = (
    ("กฎการลำดับชั้น", "ในชั้นหินที่ไม่ถูกรบกวน ชั้นล่างเกิดก่อนชั้นบน"),
    ("กฎการวางตัวในแนวราบ", "ตะกอนสะสมตัวในแนวราบ ชั้นหินที่เอียงหรือคดโค้งจึงถูกรบกวนภายหลัง"),
    ("กฎการตัดขวาง", "หินอัคนีหรือรอยเลื่อนที่ตัดผ่านชั้นหินเกิดหลังชั้นหินที่ถูกตัด"),
    ("กฎการมีเศษหินปน", "เศษหินที่ปนอยู่ในหินอื่นมีอายุมากกว่าหินที่มันปนอยู่"),
    ("รอยชั้นไม่ต่อเนื่อง", "ผิวรอยต่อที่บอกว่าช่วงหนึ่งไม่มีการสะสมตะกอนหรือชั้นหินถูกกัดกร่อนไป"),
)


HISTORY_HINT = ("ชั้นล่างเกิดก่อนชั้นบน สิ่งที่ตัดผ่านเกิดทีหลังสิ่งที่ถูกตัด ซากดึกดำบรรพ์ดัชนีบอกช่วงอายุ "
                "การหาอายุสัมบูรณ์ใช้ครึ่งชีวิตของธาตุกัมมันตรังสี")


LETTERS = "ABCDE"


@question_type(
    "geo.geologic_history_foundation",
    display_name={"th": "หลักการลำดับชั้นหินและการหาอายุ"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_HISTORY,
)
class GeologicHistoryFoundation(QuestionType):
    """The principles of relative dating, and fossils."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            facts = (("ซากดึกดำบรรพ์ดัชนีควรมีลักษณะใด", "มีช่วงอายุสั้น แพร่กระจายกว้าง และพบได้มาก",
                      ("มีช่วงอายุยาวนานมาก", "พบในที่เดียวเท่านั้น", "มีขนาดใหญ่มาก", "ยังมีชีวิตอยู่ในปัจจุบัน")),
                     ("การหาอายุสัมบูรณ์ของหินต่างจากอายุเปรียบเทียบอย่างไร", "บอกอายุเป็นตัวเลขจากการสลายตัวของธาตุกัมมันตรังสี",
                      ("บอกเพียงว่าชั้นใดเก่ากว่า", "ใช้ความหนาของชั้นหินเท่านั้น", "ใช้สีของหิน", "ใช้ได้กับหินทุกชนิดโดยไม่ต้องมีธาตุกัมมันตรังสี")))
            stem, right, wrongs = rng.choice(facts)
            return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), topic=TOPIC_HISTORY, hint=HISTORY_HINT)
        name, rule = rng.choice(PRINCIPLES)
        others = rng.sample([p for p in PRINCIPLES if p[0] != name], 3)
        if rng.random() < 0.5:
            return _labelled(stem=f"{name}กล่าวว่าอย่างไร", correct=rule, wrongs=tuple(p[1] for p in others), topic=TOPIC_HISTORY, hint=HISTORY_HINT)
        return _labelled(stem=f"\"{rule}\" เป็นหลักการใด", correct=name, wrongs=tuple(p[0] for p in others), topic=TOPIC_HISTORY, hint=HISTORY_HINT)


@question_type(
    "geo.geologic_history_fluency",
    display_name={"th": "เรียงลำดับเหตุการณ์จากภาพตัดขวางชั้นหิน"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_HISTORY,
)
class GeologicHistoryFluency(QuestionType):
    """Superposition plus one cross-cutting dike."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        n = rng.randint(3, 5)
        names = list(LETTERS[:n])
        rng.shuffle(names)  # bottom to top
        cut = rng.randint(1, n)  # the dike cuts the bottom `cut` layers only
        order = names[:cut] + ["พนังหินอัคนี X"] + names[cut:]
        description = (f"ชั้นหินที่ไม่ถูกพลิกกลับเรียงจากล่างขึ้นบนเป็น {', '.join(names)} มีพนังหินอัคนี X ตัดผ่านชั้น "
                       f"{', '.join(names[:cut])} แต่ไม่ตัดชั้นที่อยู่ข้างบน")
        roll = rng.random()
        if roll < 0.35:
            return _labelled(stem=f"{description} สิ่งใดเกิดก่อนสุด", correct=order[0],
                             wrongs=tuple([o for o in order if o != order[0]]), topic=TOPIC_HISTORY, hint=HISTORY_HINT)
        if roll < 0.7:
            return _labelled(stem=f"{description} สิ่งใดเกิดหลังสุด", correct=order[-1],
                             wrongs=tuple([o for o in order if o != order[-1]]), topic=TOPIC_HISTORY, hint=HISTORY_HINT)
        right = " → ".join(order)
        wrongs: dict[str, None] = {}   # insertion-ordered: a set's order changes per process
        while len(wrongs) < 3:
            o = order[:]
            rng.shuffle(o)
            if o != order:
                wrongs[" → ".join(o)] = None
        return _labelled(stem=f"{description} ข้อใดเรียงลำดับเหตุการณ์จากเก่าไปใหม่ได้ถูกต้อง", correct=right, wrongs=tuple(wrongs),
                         topic=TOPIC_HISTORY, hint=HISTORY_HINT)


@question_type(
    "geo.geologic_history_application",
    display_name={"th": "หาอายุสัมบูรณ์ของหินจากครึ่งชีวิต"},
    level=UPPER_FOUR, subject=SUBJECT, topic=TOPIC_HISTORY,
)
class GeologicHistoryApplication(QuestionType):
    """n half-lives leave 1/2ⁿ; the daughter share tells n too."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        element, half = rng.choice((("โพแทสเซียม-40", 1250), ("ยูเรเนียม-235", 704), ("รูบิเดียม-87", 49000), ("ยูเรเนียม-238", 4470)))
        n = rng.randint(1, 4)
        remain = Fraction(1, 2 ** n)
        if rng.random() < 0.6:
            return numeric(stem=f"หินอัคนีมี{element}เหลืออยู่ {remain.numerator}/{remain.denominator} ของปริมาณเริ่มต้น ถ้าครึ่งชีวิตเท่ากับ {half:,} ล้านปี "
                                f"หินนี้มีอายุกี่ล้านปี", answer=n * half, wrongs=[(n + 1) * half, half * 2 ** n if 2 ** n != n else half * 3,
                                                                               Fraction(half, 2) if n == 1 else (n - 1) * half],
                           unit="ล้านปี", topic=TOPIC_HISTORY, hint="เหลือ 1/2ⁿ แปลว่าผ่านไป n ครึ่งชีวิต อายุ = n × ครึ่งชีวิต")
        parent = 1
        daughter = 2 ** n - 1
        return numeric(stem=f"ในหินอัคนีมีธาตุลูก (ที่เกิดจากการสลายของ{element}) ต่อ{element}ที่เหลือเป็น {daughter} : {parent} "
                            f"ถ้าครึ่งชีวิตเท่ากับ {half:,} ล้านปี และเริ่มต้นไม่มีธาตุลูกเลย หินนี้มีอายุกี่ล้านปี", answer=n * half,
                       wrongs=[daughter * half, (n + 1) * half, half], unit="ล้านปี", topic=TOPIC_HISTORY,
                       hint="ธาตุลูก : ธาตุแม่ = (2ⁿ − 1) : 1 เมื่อผ่านไป n ครึ่งชีวิต")
