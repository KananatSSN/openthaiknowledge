"""แผ่นกรองแสงสี การผสมแสงสี การผสมสารสี และการนำไปใช้ประโยชน์

ฟิสิกส์ · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.3 ม.5/10

Sets moved here from: science_wave_e15.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e15 import (
    COLOUR_NAME,
    LIGHT_NAME,
    OBJECTS,
    PIGMENTS,
    PRIMARY_LIGHTS,
    SUBJECT,
    UPPER_FIVE,
    B,
    G,
    R,
    _colour_choices,
    _labelled,
)

PROVENANCE = Provenance("original")


TOPIC_COLOUR_MIXING = "แผ่นกรองแสงสี การผสมแสงสี การผสมสารสี และการนำไปใช้ประโยชน์"


MIX_TRUE = (
    "แผ่นกรองแสงสีแดงยอมให้แสงสีแดงผ่านได้ และดูดกลืนแสงสีอื่นไว้",
    "แสงสีปฐมภูมิคือแสงสีแดง สีเขียว และสีน้ำเงิน ผสมกันทั้งสามสีได้แสงขาว",
    "สารสีปฐมภูมิคือสีเหลือง สีฟ้า (ไซแอน) และสีแดงม่วง (มาเจนตา) ผสมกันทั้งสามได้สีดำ",
    "การผสมแสงสีเป็นการรวมแสง ส่วนการผสมสารสีเป็นการที่สารสีแต่ละชนิดดูดกลืนแสงบางสีออกไป",
    "จอโทรทัศน์และจอโทรศัพท์สร้างสีต่าง ๆ จากจุดแสงสีแดง สีเขียว และสีน้ำเงิน",
    "เครื่องพิมพ์สีใช้หมึกสีฟ้า สีแดงม่วง และสีเหลือง (และสีดำ) ผสมกันให้เป็นสีต่าง ๆ",
)


MIX_FALSE = (
    "แผ่นกรองแสงสีแดงเปลี่ยนแสงทุกสีที่ผ่านให้กลายเป็นแสงสีแดง",
    "แสงสีแดงผสมกับแสงสีเขียวได้แสงสีน้ำตาล",
    "สารสีผสมกันทั้งสามสีปฐมภูมิแล้วได้สีขาว",
    "การผสมแสงสีกับการผสมสารสีให้ผลเหมือนกันทุกประการ",
    "จอโทรศัพท์ใช้จุดสีเหลือง สีฟ้า และสีแดงม่วงเปล่งแสง",
    "แผ่นกรองแสงสองแผ่นซ้อนกันยอมให้แสงผ่านได้มากกว่าแผ่นเดียว",
)


@question_type(
    "phys.colour_mixing_foundation",
    display_name={"th": "ผลของการผสมแสงสีปฐมภูมิ"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_COLOUR_MIXING,
)
class ColourMixingFoundation(QuestionType):
    """Adding primary lights, one pair or all three at a time."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        n = rng.choice((2, 2, 3))
        lights = rng.sample(PRIMARY_LIGHTS, n)
        total = frozenset().union(*lights)
        correct = COLOUR_NAME[total]
        return _labelled(
            stem=f"ฉาย{'และ'.join(LIGHT_NAME[ell] for ell in lights)}ซ้อนกันบนฉากสีขาว จะเห็นบริเวณที่แสงซ้อนกันเป็นสีใด",
            correct=correct, wrongs=_colour_choices(correct, rng),
            topic=TOPIC_COLOUR_MIXING,
            hint="แดง + เขียว = เหลือง เขียว + น้ำเงิน = ฟ้า แดง + น้ำเงิน = แดงม่วง และทั้งสามสีรวมกันเป็นขาว")


@question_type(
    "phys.colour_mixing_fluency",
    display_name={"th": "อธิบายการทำงานของแผ่นกรองแสงสี การผสมแสงสี และการผสมสารสี"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_COLOUR_MIXING,
)
class ColourMixingFluency(QuestionType):
    """The indicator across its objects: filters, mixed light, and mixed pigment."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(4)
        if shape == 0:
            light = rng.choice([c for c in COLOUR_NAME if c])
            flt = rng.choice([c for c in COLOUR_NAME if c and len(c) < 3])
            correct = COLOUR_NAME[light & flt]
            return _labelled(
                stem=f"ส่อง{LIGHT_NAME[light]}ผ่านแผ่นกรองแสง{COLOUR_NAME[flt]} แสงที่ผ่านออกมาเห็นเป็นสีใด",
                correct=correct, wrongs=_colour_choices(correct, rng),
                topic=TOPIC_COLOUR_MIXING,
                hint="แผ่นกรองแสงให้ผ่านเฉพาะแสงสีของตัวเอง ถ้าแสงที่ส่องมาไม่มีสีนั้นเลย จะไม่มีแสงผ่าน (เห็นมืด)")
        if shape == 1:
            a, b = rng.sample([c for c in COLOUR_NAME if c and len(c) < 3], 2)
            correct = COLOUR_NAME[a & b]
            return _labelled(
                stem=f"ส่องแสงขาวผ่านแผ่นกรองแสง{COLOUR_NAME[a]} แล้วผ่านแผ่นกรองแสง{COLOUR_NAME[b]}ต่อ แสงที่ออกมาเห็นเป็นสีใด",
                correct=correct, wrongs=_colour_choices(correct, rng),
                topic=TOPIC_COLOUR_MIXING,
                hint="แสงที่ผ่านออกมาได้ต้องผ่านแผ่นกรองทั้งสองแผ่น คือสีที่ทั้งสองแผ่นยอมให้ผ่านร่วมกัน")
        if shape == 2:
            names = rng.sample(sorted(PIGMENTS), 2)
            correct = COLOUR_NAME[PIGMENTS[names[0]] & PIGMENTS[names[1]]]
            return _labelled(
                stem=f"ผสมสาร{names[0]}กับสาร{names[1]}ในปริมาณพอเหมาะ แล้วดูใต้แสงขาว จะเห็นเป็นสีใด",
                correct=correct, wrongs=_colour_choices(correct, rng),
                topic=TOPIC_COLOUR_MIXING,
                hint="สารสีแต่ละชนิดสะท้อนแสงบางสีและดูดกลืนที่เหลือ สารสีผสมกันจึงสะท้อนได้เฉพาะแสงที่ทั้งสองสะท้อนร่วมกัน")
        return _labelled(
            stem="ข้อใดกล่าวถึงแผ่นกรองแสงสี การผสมแสงสี หรือการผสมสารสีได้ถูกต้อง",
            correct=rng.choice(MIX_TRUE), wrongs=tuple(MIX_FALSE),
            topic=TOPIC_COLOUR_MIXING,
            hint="แสงสีผสมกันแบบรวมแสง (ยิ่งผสมยิ่งสว่าง) สารสีผสมกันแบบดูดกลืน (ยิ่งผสมยิ่งมืด)")


@question_type(
    "phys.colour_mixing_application",
    display_name={"th": "ใช้แผ่นกรองแสงและการผสมสีกับจอภาพ งานพิมพ์ และเวที"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_COLOUR_MIXING,
)
class ColourMixingApplication(QuestionType):
    """Work backwards: which lights make a colour on a screen, which filter a
    spotlight needs, which inks print a colour."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.randrange(4)
        if shape == 3:
            # An object under white light, seen through a filter: only what it
            # reflects *and* the filter passes reaches the eye.
            reflects = rng.choice([c for c in COLOUR_NAME if c and len(c) < 3])
            flt = rng.choice([c for c in COLOUR_NAME if c and len(c) < 3])
            thing, _ = rng.choice(OBJECTS)
            correct = COLOUR_NAME[reflects & flt]
            return _labelled(
                stem=(f"มอง{thing}ที่เห็นเป็น{COLOUR_NAME[reflects]}ใต้แสงขาว ผ่านแว่นที่ทำจาก"
                      f"แผ่นกรองแสง{COLOUR_NAME[flt]} จะเห็น{thing}เป็นสีใด"),
                correct=correct, wrongs=_colour_choices(correct, rng),
                topic=TOPIC_COLOUR_MIXING,
                hint="แสงที่มาถึงตาต้องเป็นสีที่วัตถุสะท้อน และแผ่นกรองยอมให้ผ่านด้วย ถ้าไม่มีสีใดตรงกันจะเห็นเป็นสีดำ")
        if shape == 0:
            target = rng.choice([c for c in COLOUR_NAME if len(c) >= 2])
            correct = "และ".join(LIGHT_NAME[frozenset({p})] for p in (R, G, B) if p in target)
            options = ["และ".join(LIGHT_NAME[frozenset({p})] for p in (R, G, B) if p in c)
                       for c in COLOUR_NAME if len(c) >= 2 and c != target]
            wrongs = options[:3] if len(options) >= 3 else options + ["แสงสีแดงเพียงสีเดียว"]
            return _labelled(
                stem=f"จุดภาพบนจอโทรศัพท์แสดง{COLOUR_NAME[target]} ต้องเปิดจุดแสงสีใดพร้อมกัน",
                correct=correct, wrongs=tuple(wrongs[:3]),
                topic=TOPIC_COLOUR_MIXING,
                hint="จอภาพผสมแสงสีแดง เขียว และน้ำเงิน: สีที่ต้องการประกอบด้วยแสงปฐมภูมิสีใดบ้าง")
        if shape == 1:
            want = rng.choice(PRIMARY_LIGHTS)
            filters = [c for c in COLOUR_NAME if c and len(c) < 3]
            ok = [f for f in filters if f == want]
            passes_more = [f for f in filters if want <= f and f != want]
            blocks = [f for f in filters if not want <= f]
            wrongs = [COLOUR_NAME[f] for f in (passes_more + blocks)][:3]
            return _labelled(
                stem=f"ต้องการให้ไฟสปอตไลต์ที่ให้แสงขาวส่องออกมาเป็น{LIGHT_NAME[want]}เท่านั้น ควรใช้แผ่นกรองแสงสีใด",
                correct=COLOUR_NAME[ok[0]], wrongs=tuple(wrongs),
                topic=TOPIC_COLOUR_MIXING,
                hint="แผ่นกรองสีเหลือง ฟ้า หรือแดงม่วงยอมให้แสงผ่านสองสี ต้องเลือกแผ่นที่ให้ผ่านเฉพาะสีที่ต้องการ")
        target = rng.choice([c for c in COLOUR_NAME if len(c) == 1])
        pair = [n for n, s in PIGMENTS.items() if target <= s]
        correct = f"{pair[0]}ผสมกับ{pair[1]}"
        wrong_pairs = [f"{a}ผสมกับ{b}" for a in PIGMENTS for b in PIGMENTS if a < b and {a, b} != set(pair)]
        return _labelled(
            stem=f"เครื่องพิมพ์ต้องพิมพ์ภาพ{COLOUR_NAME[target]} โดยใช้หมึกสีปฐมภูมิของสารสี ควรใช้หมึกสีใดผสมกัน",
            correct=correct,
            wrongs=(*wrong_pairs, f"{COLOUR_NAME[target]}ผสมกับสีขาว")[:3],
            topic=TOPIC_COLOUR_MIXING,
            hint="หมึกผสมกันสะท้อนได้เฉพาะแสงที่หมึกทั้งสองสะท้อนร่วมกัน หาคู่หมึกที่มีสีเป้าหมายอยู่ด้วยกันทั้งคู่")
