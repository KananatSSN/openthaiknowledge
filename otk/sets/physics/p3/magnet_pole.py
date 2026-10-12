"""ขั้วแม่เหล็ก

ฟิสิกส์ · ป.3 · สสวท. พื้นฐาน
Indicators: ว 2.2 ป.3/4

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


POLES_TOPIC = "ขั้วแม่เหล็ก"


def _facts(rng: Random, facts: tuple, *, hint: str, topic: str) -> GeneratedQuestion:
    stem, right, wrongs = rng.choice(facts)
    return _labelled(stem=stem, correct=right, wrongs=tuple(wrongs), hint=hint, topic=topic)


NORTH, SOUTH = "ขั้วเหนือ", "ขั้วใต้"


ATTRACT, REPEL = "ดึงดูดกัน", "ผลักกัน"


POLE_HINT = "ขั้วเหมือนกันผลักกัน ขั้วต่างกันดึงดูดกัน แม่เหล็กแท่งมีสองขั้วที่ต่างกันเสมอ และขั้วเหนือของแม่เหล็กที่หมุนได้อิสระชี้ทิศเหนือ"


POLE_FACTS = (
    ("แม่เหล็กแท่งหนึ่งแท่งมีขั้วแม่เหล็กกี่ขั้ว", "สองขั้ว คือขั้วเหนือและขั้วใต้",
     ("หนึ่งขั้วเท่านั้น", "สามขั้ว", "ไม่มีขั้ว", "สองขั้วที่เป็นขั้วเหนือทั้งคู่", "สี่ขั้ว")),
    ("บริเวณใดของแม่เหล็กแท่งดึงดูดคลิปหนีบกระดาษได้มากที่สุด", "บริเวณปลายทั้งสองข้าง ซึ่งเป็นขั้วแม่เหล็ก",
     ("บริเวณกึ่งกลางแท่ง", "ทุกบริเวณดึงดูดเท่ากัน", "เฉพาะด้านที่ทาสีแดง", "ไม่มีบริเวณใดดึงดูด", "เฉพาะขั้วเหนือ")),
    ("ถ้าหักแม่เหล็กแท่งออกเป็นสองท่อน แต่ละท่อนจะเป็นอย่างไร", "แต่ละท่อนเป็นแม่เหล็กที่มีทั้งขั้วเหนือและขั้วใต้",
     ("ท่อนหนึ่งเป็นขั้วเหนือ อีกท่อนเป็นขั้วใต้", "ทั้งสองท่อนไม่เป็นแม่เหล็กอีกต่อไป", "ทั้งสองท่อนมีแต่ขั้วเหนือ", "ท่อนหนึ่งมีสามขั้ว", "แม่เหล็กจะระเบิด")),
    ("เมื่อแขวนแม่เหล็กแท่งให้หมุนได้อิสระ ขั้วใต้ชี้ไปทางใด", "ทิศใต้", ("ทิศเหนือ", "ทิศตะวันออก", "ทิศตะวันตก", "ชี้ขึ้นฟ้า", "ชี้ทางใดก็ได้")),
)


def _other(pole: str) -> str:
    return SOUTH if pole == NORTH else NORTH


def _meet(a: str, b: str) -> str:
    return REPEL if a == b else ATTRACT


POLES_SCENARIOS = (
    ("ป้ายชื่อขั้วบนแม่เหล็กแท่งหนึ่งหลุดหาย นักเรียนมีแม่เหล็กอีกแท่งที่รู้ขั้วแล้ว ควรหาขั้วอย่างไร",
     "นำขั้วเหนือของแท่งที่รู้ขั้วเข้าใกล้ปลายหนึ่ง ถ้าผลักกันปลายนั้นเป็นขั้วเหนือ ถ้าดึงดูดกันเป็นขั้วใต้",
     ("นำปลายหนึ่งไปแตะคลิปหนีบกระดาษ ปลายที่ดูดคลิปได้คือขั้วเหนือ",
      "ดูสีของปลายแม่เหล็ก ปลายที่สีเข้มกว่าเป็นขั้วเหนือ",
      "ชั่งน้ำหนักแต่ละปลาย ปลายที่หนักกว่าเป็นขั้วใต้")),
    ("แขวนแม่เหล็กแท่งให้หมุนได้อย่างอิสระ เมื่อหยุดนิ่ง ขั้วเหนือของแม่เหล็กชี้ไปทางใด",
     "ทิศเหนือของโลก",
     ("ทิศใต้ของโลก", "ทิศตะวันออก", "ชี้ไปทางใดก็ได้แบบสุ่มทุกครั้ง")),
    ("ของเล่นรถไฟแม่เหล็กต่อตู้กันได้ด้วยแม่เหล็กที่ปลายตู้ ถ้าต่อตู้แล้วตู้ผลักกันไม่ยอมติด ควรทำอย่างไร",
     "หมุนตู้กลับด้าน เพื่อให้ขั้วที่ต่างกันหันเข้าหากันแล้วดึงดูดกัน",
     ("ดันให้แรงขึ้นเพราะขั้วเหมือนกันจะดึงดูดเมื่อดันแรง",
      "ทาน้ำที่แม่เหล็กเพื่อให้ติดกัน",
      "เปลี่ยนแม่เหล็กเป็นไม้")),
)


@question_type(
    "phys.magnet_pole_foundation",
    display_name={"th": "ระบุขั้วแม่เหล็กจากผลการทดสอบ"},
    level=THIRD, subject=SUBJECT, topic=POLES_TOPIC,
)
class MagnetPoleFoundation(QuestionType):
    """A known pole brought near an unknown end; or facts about poles."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.4:
            return _facts(rng, POLE_FACTS, hint=POLE_HINT, topic=POLES_TOPIC)
        known = rng.choice((NORTH, SOUTH))
        seen = rng.choice((ATTRACT, REPEL))
        end = known if seen == REPEL else _other(known)
        far = _other(end)
        return _labelled(
            stem=(f"นำ{known}ของแม่เหล็กแท่ง ก เข้าใกล้ปลาย X ของแม่เหล็กแท่ง ข พบว่า{seen} "
                  "จากหลักฐานนี้ ปลาย X และปลายอีกด้านหนึ่งของแท่ง ข เป็นขั้วใด"),
            correct=f"ปลาย X เป็น{end} ปลายอีกด้านเป็น{far}",
            wrongs=(f"ปลาย X เป็น{far} ปลายอีกด้านเป็น{end}",
                    f"ปลาย X และปลายอีกด้านเป็น{end}ทั้งคู่",
                    f"ปลาย X และปลายอีกด้านเป็น{far}ทั้งคู่"),
            hint=POLE_HINT, topic=POLES_TOPIC,
        )


@question_type(
    "phys.magnet_pole_fluency",
    display_name={"th": "พยากรณ์ผลเมื่อนำขั้วแม่เหล็กเข้าใกล้กัน"},
    level=THIRD, subject=SUBJECT, topic=POLES_TOPIC,
)
class MagnetPoleFluency(QuestionType):
    """Three bar magnets in a row, or two bars before and after one is turned round."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        roll = rng.random()
        if roll < 0.25:
            ends = [(p := rng.choice((NORTH, SOUTH)), _other(p)) for _ in range(3)]
            flip_b = ends[0][1] == ends[1][0]
            b_right = ends[1][0] if flip_b else ends[1][1]
            flip_c = b_right == ends[2][0]
            right = ("หมุนทั้งแท่ง ข และแท่ง ค" if flip_b and flip_c else "หมุนแท่ง ข" if flip_b
                     else "หมุนแท่ง ค" if flip_c else "ไม่ต้องหมุนแท่งใด")
            layout = " | ".join(f"แท่ง {name}: {left} – {right_}" for name, (left, right_) in zip("กขค", ends))
            return _labelled(stem=(f"วางแม่เหล็กแท่ง 3 แท่งเรียงจากซ้ายไปขวา — {layout} ถ้าไม่หมุนแท่ง ก "
                                   "ต้องหมุนแท่งใดกลับหัวท้ายเพื่อให้ทุกแท่งดูดติดกันเป็นแถว"),
                             correct=right, wrongs=tuple(o for o in ("หมุนแท่ง ข", "หมุนแท่ง ค", "หมุนทั้งแท่ง ข และแท่ง ค", "ไม่ต้องหมุนแท่งใด") if o != right),
                             hint="ปลายที่หันเข้าหากันต้องเป็นขั้วต่างกันจึงดูดกัน ตรวจทีละคู่จากซ้ายไปขวา", topic=POLES_TOPIC)
        if roll < 0.5:
            ends = [(p := rng.choice((NORTH, SOUTH)), _other(p)) for _ in range(4)]
            meets = [_meet(ends[i][1], ends[i + 1][0]) for i in range(3)]
            layout = " | ".join(f"แท่ง {name}: {left} – {right_}" for name, (left, right_) in zip("กขคง", ends))
            flip = {ATTRACT: REPEL, REPEL: ATTRACT}
            text = lambda m: " / ".join(f"{pair} {x}" for pair, x in zip(("ก กับ ข", "ข กับ ค", "ค กับ ง"), m))
            wrongs = [text([flip[m] if i == j else m for j, m in enumerate(meets)]) for i in range(3)]
            return _labelled(stem=(f"วางแม่เหล็กแท่ง 4 แท่งเรียงจากซ้ายไปขวา — {layout} "
                                   "เมื่อเลื่อนแต่ละแท่งเข้าใกล้แท่งถัดไป จะเกิดผลอย่างไร"),
                             correct=text(meets), wrongs=tuple(wrongs), hint="ดูเฉพาะปลายที่หันเข้าหากัน: ขั้วเหมือนกันผลักกัน ขั้วต่างกันดึงดูดกัน",
                             topic=POLES_TOPIC)
        if roll < 0.7:
            a_right = rng.choice((NORTH, SOUTH))
            b_left = rng.choice((NORTH, SOUTH))
            before = _meet(a_right, b_left)
            after = _meet(a_right, _other(b_left))
            line2 = lambda x, y: f"ก่อนหมุน{x} / หลังหมุน{y}"
            return _labelled(stem=(f"ปลายขวาของแม่เหล็กแท่ง ก เป็น{a_right} หันเข้าหาปลายซ้ายของแม่เหล็กแท่ง ข ซึ่งเป็น{b_left} "
                                   "ถ้าหมุนแท่ง ข กลับหัวท้าย แล้วนำเข้าใกล้อีกครั้ง ผลก่อนและหลังหมุนเป็นอย่างไร"),
                             correct=line2(before, after), wrongs=(line2(after, before), line2(before, before), line2(after, after)),
                             hint=POLE_HINT, topic=POLES_TOPIC)
        ends = [(p := rng.choice((NORTH, SOUTH)), _other(p)) for _ in range(3)]
        first = _meet(ends[0][1], ends[1][0])
        second = _meet(ends[1][1], ends[2][0])
        layout = " | ".join(f"แท่ง {name}: {left} – {right}" for name, (left, right) in zip("กขค", ends))

        def line(one: str, two: str) -> str:
            return f"แท่ง ก กับ ข {one} / แท่ง ข กับ ค {two}"

        flip = {ATTRACT: REPEL, REPEL: ATTRACT}
        return _labelled(
            stem=(f"วางแม่เหล็กแท่ง 3 แท่งเรียงกันจากซ้ายไปขวา โดยปลายซ้ายและปลายขวาของแต่ละแท่งเป็นดังนี้ — {layout} "
                  "เมื่อเลื่อนแต่ละแท่งเข้าใกล้แท่งถัดไป จะเกิดผลอย่างไร"),
            correct=line(first, second),
            wrongs=(line(flip[first], second), line(first, flip[second]), line(flip[first], flip[second])),
            hint="ดูเฉพาะปลายที่หันเข้าหากัน: ขั้วเหมือนกันผลักกัน ขั้วต่างกันดึงดูดกัน",
            topic=POLES_TOPIC,
        )


@question_type(
    "phys.magnet_pole_application",
    display_name={"th": "ใช้สมบัติของขั้วแม่เหล็กแก้ปัญหา"},
    level=THIRD, subject=SUBJECT, topic=POLES_TOPIC,
)
class MagnetPoleApplication(QuestionType):
    """Authored cases, and naming the ends of a freely hanging magnet from where they point."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        if rng.random() < 0.3:
            return _retopic(scenario_question(rng, POLES_SCENARIOS, hint=POLE_HINT), POLES_TOPIC)
        label = rng.choice(("ปลายที่ทาสีแดง", "ปลายที่มีสติกเกอร์", "ปลาย A", "ปลายที่มีรอยขีด"))
        points = rng.choice(("ทิศเหนือ", "ทิศใต้"))
        pole = NORTH if points == "ทิศเหนือ" else SOUTH
        kid = rng.choice(KIDS)
        return _labelled(stem=f"{kid}แขวนแม่เหล็กแท่งที่ไม่มีป้ายบอกขั้วให้หมุนได้อิสระ เมื่อหยุดนิ่ง{label}ชี้ไปทาง{points} {label}เป็นขั้วใด",
                         correct=pole, wrongs=(_other(pole), "ไม่มีขั้ว", "เป็นได้ทั้งสองขั้ว"), hint=POLE_HINT, topic=POLES_TOPIC)
