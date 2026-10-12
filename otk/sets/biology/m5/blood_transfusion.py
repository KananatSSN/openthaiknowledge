"""หมู่เลือดและการให้รับเลือด

ชีวะ · ม.5 · สสวท. เพิ่มเติม
Indicators: ชีววิทยาเพิ่มเติม 4 ม.5/13

Sets moved here from: science_wave_f62.
"""

from __future__ import annotations

from random import Random

from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.kit.answer_choices import _labelled
from otk.sets._support.science_wave_f62 import SUBJECT, UPPER_FIVE

PROVENANCE = Provenance("original")


TOPIC_GROUP = "หมู่เลือดและการให้รับเลือด"


ANTIGENS = {"A": {"A"}, "B": {"B"}, "AB": {"A", "B"}, "O": set()}


ANTIBODY_TEXT = {"A": "แอนติบอดี B (anti-B)", "B": "แอนติบอดี A (anti-A)", "AB": "ไม่มีแอนติบอดี A และ B", "O": "แอนติบอดี A และ B"}


ANTIGEN_TEXT = {"A": "แอนติเจน A", "B": "แอนติเจน B", "AB": "แอนติเจน A และ B", "O": "ไม่มีแอนติเจน A และ B"}


GROUP_HINT = ("เซลล์เม็ดเลือดแดงหมู่ A มีแอนติเจน A พลาสมามี anti-B หมู่ B กลับกัน หมู่ AB มีทั้งสองแอนติเจนแต่ไม่มีแอนติบอดี "
              "หมู่ O ไม่มีแอนติเจนแต่มีทั้งสองแอนติบอดี ผู้ให้ต้องไม่มีแอนติเจนที่ผู้รับมีแอนติบอดี Rh+ ให้ Rh− ไม่ได้")


def can_give(donor: str, donor_rh: str, recipient: str, recipient_rh: str) -> bool:
    return ANTIGENS[donor] <= ANTIGENS[recipient] and not (donor_rh == "+" and recipient_rh == "−")


@question_type(
    "biology.blood_transfusion_foundation",
    display_name={"th": "แอนติเจนและแอนติบอดีในหมู่เลือดระบบ ABO และ Rh"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_GROUP,
)
class BloodTransfusionFoundation(QuestionType):
    """What each group carries on its cells and in its plasma."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        group = rng.choice(sorted(ANTIGENS))
        others = [g for g in ANTIGENS if g != group]
        roll = rng.random()
        if roll < 0.35:
            def carried(g: str, r: str) -> str:
                names = sorted(ANTIGENS[g]) + (["Rh (D)"] if r == "+" else [])
                return "แอนติเจน " + " และ ".join(names) if names else "ไม่มีแอนติเจน A B และ Rh"
            rh = rng.choice(("+", "−"))
            right = carried(group, rh)
            pool = sorted({carried(g, r) for g in ANTIGENS for r in ("+", "−")} - {right})
            return _labelled(stem=f"ผิวเซลล์เม็ดเลือดแดงของคนหมู่เลือด {group} Rh{rh} มีแอนติเจนใด", correct=right,
                             wrongs=tuple(pool), topic=TOPIC_GROUP, hint=GROUP_HINT)
        if roll < 0.55:
            return _labelled(stem=f"พลาสมาของคนหมู่เลือด {group} มีแอนติบอดีใด", correct=ANTIBODY_TEXT[group],
                             wrongs=tuple(ANTIBODY_TEXT[g] for g in others), topic=TOPIC_GROUP, hint=GROUP_HINT)
        if roll < 0.75:
            if rng.random() < 0.5:
                return _labelled(stem=f"คนหมู่เลือดใดมี{ANTIBODY_TEXT[group]}ในพลาสมา" if group not in ("AB",) else
                                 "คนหมู่เลือดใดไม่มีแอนติบอดี A และ B ในพลาสมา", correct=f"หมู่ {group}",
                                 wrongs=tuple(f"หมู่ {g}" for g in others), topic=TOPIC_GROUP, hint=GROUP_HINT)
            return _labelled(stem=f"คนหมู่เลือดใดมีเซลล์เม็ดเลือดแดงที่{'มี' + ANTIGEN_TEXT[group] if group != 'O' else 'ไม่มีแอนติเจน A และ B'}",
                             correct=f"หมู่ {group}", wrongs=tuple(f"หมู่ {g}" for g in others), topic=TOPIC_GROUP, hint=GROUP_HINT)
        facts = (("คนหมู่เลือด Rh− จะสร้างแอนติบอดีต่อแอนติเจน Rh เมื่อใด", "หลังได้รับเลือด Rh+ เข้าสู่ร่างกาย",
                  ("มีอยู่แล้วตั้งแต่เกิด", "ไม่สร้างเลยตลอดชีวิต", "เมื่อได้รับเลือด Rh− ครั้งแรก")),
                 ("ทารกมีโอกาสเกิดภาวะเม็ดเลือดแดงแตกจากหมู่เลือด Rh เมื่อใด", "แม่ Rh− ที่เคยมีลูก Rh+ มาก่อน ตั้งครรภ์ลูก Rh+ อีกครั้ง",
                  ("แม่ Rh+ ตั้งครรภ์ลูก Rh− ครั้งแรก", "แม่และลูกเป็น Rh+ ทั้งคู่", "แม่ Rh− ตั้งครรภ์ลูก Rh− ทุกครั้ง")),
                 ("ในระบบ ABO คนหมู่เลือดใดให้เลือดแก่ผู้อื่นได้ทุกหมู่ (ถ้าไม่คำนึงถึง Rh)", "หมู่ O", ("หมู่ A", "หมู่ B", "หมู่ AB")),
                 ("ในระบบ ABO คนหมู่เลือดใดรับเลือดจากผู้อื่นได้ทุกหมู่ (ถ้าไม่คำนึงถึง Rh)", "หมู่ AB", ("หมู่ A", "หมู่ B", "หมู่ O")))
        stem, right, wrongs = rng.choice(facts)
        return _labelled(stem=stem, correct=right, wrongs=wrongs, topic=TOPIC_GROUP, hint=GROUP_HINT)


@question_type(
    "biology.blood_transfusion_fluency",
    display_name={"th": "หลักการให้และรับเลือด"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_GROUP,
)
class BloodTransfusionFluency(QuestionType):
    """Pick the donor a patient can safely take."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        groups = [(g, r) for g in ANTIGENS for r in ("+", "−")]
        while True:
            recipient, rrh = rng.choice(groups)
            ok = [d for d in groups if can_give(*d, recipient, rrh)]
            bad = [d for d in groups if not can_give(*d, recipient, rrh)]
            if len(bad) >= 3:
                break
        if rng.random() < 0.5:
            donor = rng.choice(ok)
            return _labelled(stem=f"ผู้ป่วยมีหมู่เลือด {recipient} Rh{rrh} ควรรับเลือดจากผู้ให้หมู่ใด", correct=f"{donor[0]} Rh{donor[1]}",
                             wrongs=tuple(f"{g} Rh{r}" for g, r in rng.sample(bad, 3)), topic=TOPIC_GROUP, hint=GROUP_HINT)
        donor = rng.choice(groups)
        # Both reasons would be true at once, so the question would have two right answers.
        while not ANTIGENS[donor[0]] <= ANTIGENS[recipient] and donor[1] == "+" and rrh == "−":
            donor = rng.choice(groups)
        allowed = can_give(*donor, recipient, rrh)
        reason = ("ได้ เพราะเซลล์ของผู้ให้ไม่มีแอนติเจนที่ผู้รับมีแอนติบอดี" if allowed else
                  "ไม่ได้ เพราะผู้ให้เป็น Rh+ แต่ผู้รับเป็น Rh−" if ANTIGENS[donor[0]] <= ANTIGENS[recipient] else
                  "ไม่ได้ เพราะแอนติบอดีในผู้รับจะทำให้เซลล์ของผู้ให้ตกตะกอน")
        options = ["ได้ เพราะเซลล์ของผู้ให้ไม่มีแอนติเจนที่ผู้รับมีแอนติบอดี", "ไม่ได้ เพราะผู้ให้เป็น Rh+ แต่ผู้รับเป็น Rh−",
                   "ไม่ได้ เพราะแอนติบอดีในผู้รับจะทำให้เซลล์ของผู้ให้ตกตะกอน", "ได้ เพราะแอนติบอดีในผู้รับช่วยทำลายเซลล์แปลกปลอมจากผู้ให้ก่อนเกิดอันตราย"]
        return _labelled(stem=f"คนหมู่เลือด {donor[0]} Rh{donor[1]} ให้เลือดแก่คนหมู่เลือด {recipient} Rh{rrh} ได้หรือไม่",
                         correct=reason, wrongs=tuple(o for o in options if o != reason), topic=TOPIC_GROUP, hint=GROUP_HINT)


@question_type(
    "biology.blood_transfusion_application",
    display_name={"th": "ตรวจหมู่เลือดจากการตกตะกอนกับแอนติซีรัม"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_GROUP,
)
class BloodTransfusionApplication(QuestionType):
    """Clumping with anti-A means antigen A; with anti-D means Rh+."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        group = rng.choice(sorted(ANTIGENS))
        rh = rng.choice(("+", "−"))
        clump = lambda yes: "ตกตะกอน" if yes else "ไม่ตกตะกอน"
        results = (f"หยดแอนติซีรัม anti-A แล้ว{clump('A' in ANTIGENS[group])} anti-B แล้ว{clump('B' in ANTIGENS[group])} "
                   f"และ anti-D (Rh) แล้ว{clump(rh == '+')}")
        right = f"{group} Rh{rh}"
        wrongs: dict[str, None] = {}   # insertion-ordered: a set's order changes per process
        for g in ANTIGENS:
            for r in ("+", "−"):
                if (g, r) != (group, rh) and (g == group or r == rh):
                    wrongs[f"{g} Rh{r}"] = None
        return _labelled(stem=f"ตรวจเลือดของคนหนึ่งโดย{results} คนนี้มีหมู่เลือดใด", correct=right,
                         wrongs=tuple(sorted(wrongs)), topic=TOPIC_GROUP,
                         hint="ตกตะกอนกับ anti-A แสดงว่ามีแอนติเจน A ตกตะกอนกับ anti-B แสดงว่ามีแอนติเจน B ตกตะกอนกับ anti-D แสดงว่าเป็น Rh+")
