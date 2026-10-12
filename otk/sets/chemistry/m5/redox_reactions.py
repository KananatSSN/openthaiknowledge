"""ความหมายของปฏิกิริยารีดอกซ์

เคมี · ม.5 · สสวท. พื้นฐาน
Indicators: ว 2.1 ม.5/23

Sets moved here from: science_wave_e9.
"""

from __future__ import annotations

from math import gcd
from random import Random
from typing import NamedTuple

from otk.core.content import math, text
from otk.core.distractors import fixed
from otk.core.provenance import Provenance
from otk.core.question import GeneratedQuestion
from otk.core.registry import QuestionType, question_type
from otk.sets._support.science_wave_e8 import EQUATIONS, equation_tex
from otk.sets._support.science_wave_e9 import SUBJECT, UPPER_FIVE, _labelled

PROVENANCE = Provenance("original")


TOPIC_REDOX = "ความหมายของปฏิกิริยารีดอกซ์"


OXIDATION, REDUCTION = "ปฏิกิริยาออกซิเดชัน", "ปฏิกิริยารีดักชัน"


HALF_LABELS = (OXIDATION, REDUCTION,
               "ไม่ใช่ทั้งสองแบบ เพราะไม่มีการถ่ายโอนอิเล็กตรอน",
               "เป็นทั้งออกซิเดชันและรีดักชันในครึ่งปฏิกิริยาเดียวกัน")


class Metal(NamedTuple):
    symbol: str
    charge: int
    thai: str
    salt: str        # a soluble salt that supplies the ion, in Thai


# Listed from the metal that gives up electrons most readily to the least.
METALS: tuple[Metal, ...] = (
    Metal("Mg", 2, "แมกนีเซียม", "สารละลายแมกนีเซียมซัลเฟต"),
    Metal("Al", 3, "อะลูมิเนียม", "สารละลายอะลูมิเนียมซัลเฟต"),
    Metal("Zn", 2, "สังกะสี", "สารละลายซิงค์ซัลเฟต"),
    Metal("Fe", 2, "เหล็ก", "สารละลายไอร์ออน(II)ซัลเฟต"),
    Metal("Pb", 2, "ตะกั่ว", "สารละลายเลด(II)ไนเตรต"),
    Metal("Cu", 2, "ทองแดง", "สารละลายคอปเปอร์(II)ซัลเฟต"),
    Metal("Ag", 1, "เงิน", "สารละลายซิลเวอร์ไนเตรต"),
)


# Halogens from the strongest electron-taker to the weakest.
HALOGENS = (("Cl", "คลอรีน"), ("Br", "โบรมีน"), ("I", "ไอโอดีน"))


def _charge(n: int, sign: str) -> str:
    return sign if n == 1 else f"{n}{sign}"


def ion_tex(symbol: str, n: int, sign: str = "+") -> str:
    return rf"\mathrm{{{symbol}}}^{{{_charge(n, sign)}}}"


def atom_tex(symbol: str) -> str:
    return rf"\mathrm{{{symbol}}}"


def _electrons(n: int) -> str:
    return f"{'' if n == 1 else n}e^{{-}}"


def _coef(n: int, tex: str) -> str:
    return tex if n == 1 else f"{n}{tex}"


class HalfReaction(NamedTuple):
    tex: str
    kind: str       # OXIDATION or REDUCTION


def half_reactions() -> tuple[HalfReaction, ...]:
    out = []
    for m in METALS:
        atom, ion, e = atom_tex(m.symbol), ion_tex(m.symbol, m.charge), _electrons(m.charge)
        out.append(HalfReaction(rf"{atom} \longrightarrow {ion} + {e}", OXIDATION))
        out.append(HalfReaction(rf"{ion} + {e} \longrightarrow {atom}", REDUCTION))
    for symbol, _ in HALOGENS:
        molecule = rf"\mathrm{{{symbol}_{{2}}}}"
        ion = ion_tex(symbol, 1, "-")
        out.append(HalfReaction(rf"{molecule} + 2e^{{-}} \longrightarrow 2{ion}", REDUCTION))
        out.append(HalfReaction(rf"2{ion} \longrightarrow {molecule} + 2e^{{-}}", OXIDATION))
    return tuple(out)


HALF_REACTIONS = half_reactions()


class Displacement(NamedTuple):
    """A redox reaction that goes: ``giver`` hands electrons to ``taker``."""
    tex: str
    giver: str          # TeX of the species oxidised
    taker: str          # TeX of the species reduced
    giver_after: str    # what the giver becomes
    taker_after: str    # what the taker becomes
    electrons: int      # electrons transferred in the balanced equation
    giver_thai: str
    taker_thai: str


def displacements() -> tuple[Displacement, ...]:
    out = []
    for i, m in enumerate(METALS):
        for n in METALS[i + 1:]:
            lcm = m.charge * n.charge // gcd(m.charge, n.charge)
            a, b = lcm // m.charge, lcm // n.charge
            giver, taker = atom_tex(m.symbol), ion_tex(n.symbol, n.charge)
            giver_after, taker_after = ion_tex(m.symbol, m.charge), atom_tex(n.symbol)
            tex = (rf"{_coef(a, giver)} + {_coef(b, taker)} \longrightarrow "
                   rf"{_coef(a, giver_after)} + {_coef(b, taker_after)}")
            out.append(Displacement(tex, giver, taker, giver_after, taker_after, lcm,
                                    f"โลหะ{m.thai}", f"ไอออนของ{n.thai}"))
    for i, (x, x_thai) in enumerate(HALOGENS):
        for y, y_thai in HALOGENS[i + 1:]:
            taker, giver = rf"\mathrm{{{x}_{{2}}}}", ion_tex(y, 1, "-")
            taker_after, giver_after = ion_tex(x, 1, "-"), rf"\mathrm{{{y}_{{2}}}}"
            tex = (rf"{taker} + 2{giver} \longrightarrow 2{taker_after} + {giver_after}")
            out.append(Displacement(tex, giver, taker, giver_after, taker_after, 2,
                                    f"ไอออนของ{y_thai}", f"แก๊ส{x_thai}" if x == "Cl" else f"{x_thai}"))
    return tuple(out)


DISPLACEMENTS = displacements()


# From the slice 8 bank, by reactants. Only reactions where a metal visibly
# becomes an ion (or back) count as redox here: the core course argues from
# electron transfer, not oxidation numbers, so combustion and the other
# covalent redox reactions are left out of both lists rather than argued.
REDOX_REACTANTS = frozenset({("Zn", "HCl"), ("Mg", "HCl"), ("Fe", "CuSO4"), ("Mg", "O2"),
                             ("Na", "H2O"), ("Al", "CuCl2")})


NOT_REDOX_REACTANTS = frozenset({("CaCO3",), ("NaOH", "HCl"), ("AgNO3", "NaCl"),
                                 ("CaCO3", "HCl"), ("BaCl2", "Na2SO4")})


def _reactants(eq) -> tuple[str, ...]:
    return tuple(s.formula for s in eq.reactants)


EVERYDAY_REDOX = (
    "เหล็กที่ตากฝนเกิดสนิม",
    "แก๊สหุงต้มเผาไหม้ให้ความร้อน",
    "ถ่านไฟฉายจ่ายกระแสไฟฟ้าให้ไฟฉาย",
    "การชุบช้อนด้วยโลหะเงินโดยใช้ไฟฟ้า",
    "เซลล์ในร่างกายใช้แก๊สออกซิเจนสลายกลูโคสเพื่อให้ได้พลังงาน",
    "พืชสังเคราะห์ด้วยแสงสร้างกลูโคสจากแก๊สคาร์บอนไดออกไซด์และน้ำ",
    "ภาชนะเงินหมองคล้ำเมื่อทิ้งไว้ในอากาศนาน ๆ",
)


EVERYDAY_NOT_REDOX = (
    "น้ำแข็งละลายเป็นน้ำ",
    "เกลือแกงละลายในน้ำ",
    "ยาลดกรดสะเทินกรดในกระเพาะอาหาร",
    "น้ำระเหยกลายเป็นไอ",
    "น้ำตาลทรายละลายในน้ำร้อน",
)


@question_type(
    "chem.redox_foundation",
    display_name={"th": "ออกซิเดชัน รีดักชัน และครึ่งปฏิกิริยา"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_REDOX,
)
class RedoxFoundation(QuestionType):
    """The two halves on their own: what each word means, and which one a
    half-reaction shows."""

    DEFINITIONS = (
        ("ปฏิกิริยาออกซิเดชันหมายถึงข้อใด", "ปฏิกิริยาที่สารให้อิเล็กตรอน",
         ("ปฏิกิริยาที่สารรับอิเล็กตรอน", "ปฏิกิริยาที่สารรับโปรตอน",
          "ปฏิกิริยาที่สารละลายในน้ำ")),
        ("ปฏิกิริยารีดักชันหมายถึงข้อใด", "ปฏิกิริยาที่สารรับอิเล็กตรอน",
         ("ปฏิกิริยาที่สารให้อิเล็กตรอน", "ปฏิกิริยาที่สารให้โปรตอน",
          "ปฏิกิริยาที่สารเปลี่ยนสถานะ")),
        ("ปฏิกิริยารีดอกซ์หมายถึงข้อใด",
         "ปฏิกิริยาที่มีการให้และรับอิเล็กตรอนเกิดขึ้นพร้อมกัน",
         ("ปฏิกิริยาที่มีเฉพาะการให้อิเล็กตรอน", "ปฏิกิริยาที่มีเฉพาะการรับอิเล็กตรอน",
          "ปฏิกิริยาระหว่างกรดกับเบสได้เกลือและน้ำ")),
    )

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        hint = "ออกซิเดชันคือการให้อิเล็กตรอน (อิเล็กตรอนอยู่ทางขวาของลูกศร) รีดักชันคือการรับอิเล็กตรอน (อิเล็กตรอนอยู่ทางซ้าย)"
        shape = rng.random()
        if shape < 0.2:
            stem, correct, wrongs = rng.choice(self.DEFINITIONS)
            return _labelled(stem=stem, correct=correct, wrongs=wrongs,
                             topic=TOPIC_REDOX, hint=hint)
        if shape < 0.45:
            # One atom becoming its ion: which way the electrons go, and how many.
            if rng.random() < 0.7:
                m = rng.choice(METALS)
                atom, ion, n, gives = f"{m.thai}", ion_tex(m.symbol, m.charge), m.charge, True
            else:
                symbol, thai = rng.choice(HALOGENS)
                atom, ion, n, gives = f"อะตอม{thai}", ion_tex(symbol, 1, "-"), 1, False
            options = [f"{verb} {k} อิเล็กตรอน" for verb in ("ให้", "รับ") for k in (n, n + 1)]
            correct = f"{'ให้' if gives else 'รับ'} {n} อิเล็กตรอน"
            return _labelled(
                stem=[text(f"เมื่อ{atom}หนึ่งอะตอมเปลี่ยนเป็นไอออน "), math(ion),
                      text(" อะตอมนั้นให้หรือรับอิเล็กตรอนกี่อิเล็กตรอน")],
                correct=correct, wrongs=tuple(o for o in options if o != correct),
                topic=TOPIC_REDOX,
                hint="ไอออนบวกเกิดจากการให้อิเล็กตรอน ไอออนลบเกิดจากการรับอิเล็กตรอน จำนวนเท่ากับขนาดของประจุ",
            )
        half = rng.choice(HALF_REACTIONS)
        return _labelled(
            stem=[text("ครึ่งปฏิกิริยา "), math(half.tex), text(" เป็นปฏิกิริยาแบบใด")],
            correct=half.kind, wrongs=tuple(label for label in HALF_LABELS if label != half.kind),
            topic=TOPIC_REDOX, hint=hint,
        )


@question_type(
    "chem.redox_fluency",
    display_name={"th": "อธิบายปฏิกิริยารีดอกซ์ด้วยการให้และรับอิเล็กตรอน"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_REDOX,
)
class RedoxFluency(QuestionType):
    """The indicator: in a whole reaction, who gives electrons and who takes them."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        r = rng.choice(DISPLACEMENTS)
        stem = [text("จากปฏิกิริยา "), math(r.tex)]
        hint = "สารที่ประจุเพิ่มขึ้น (เช่น อะตอมกลายเป็นไอออนบวก) ให้อิเล็กตรอน สารที่ประจุลดลงรับอิเล็กตรอน"
        species = [r.giver, r.taker, r.giver_after, r.taker_after]
        shape = rng.random()
        if shape < 0.6:
            oxidised = rng.random() < 0.5
            answer = r.giver if oxidised else r.taker
            what = ("ให้อิเล็กตรอน จึงเกิดปฏิกิริยาออกซิเดชัน" if oxidised
                    else "รับอิเล็กตรอน จึงเกิดปฏิกิริยารีดักชัน")
            return GeneratedQuestion(
                stem=[*stem, text(f" สารใด{what}")],
                correct=[math(answer)],
                distractors=fixed(*[[math(s)] for s in species if s != answer]),
                topic=TOPIC_REDOX, hint=[text(hint)],
            )
        correct = (f"{r.giver_thai}ให้อิเล็กตรอนแก่{r.taker_thai} "
                   f"{r.giver_thai}จึงเกิดออกซิเดชัน และ{r.taker_thai}เกิดรีดักชัน")
        return _labelled(
            stem=[*stem, text(" ข้อใดอธิบายปฏิกิริยานี้ได้ถูกต้อง")],
            correct=correct,
            wrongs=(f"{r.taker_thai}ให้อิเล็กตรอนแก่{r.giver_thai} "
                    f"{r.taker_thai}จึงเกิดออกซิเดชัน และ{r.giver_thai}เกิดรีดักชัน",
                    f"{r.giver_thai}ให้อิเล็กตรอนแก่{r.taker_thai} "
                    f"{r.giver_thai}จึงเกิดรีดักชัน และ{r.taker_thai}เกิดออกซิเดชัน",
                    "ไม่มีการถ่ายโอนอิเล็กตรอน จึงไม่ใช่ปฏิกิริยารีดอกซ์"),
            topic=TOPIC_REDOX, hint=hint,
        )


@question_type(
    "chem.redox_application",
    display_name={"th": "ระบุและทำนายปฏิกิริยารีดอกซ์"},
    level=UPPER_FIVE, subject=SUBJECT, topic=TOPIC_REDOX,
)
class RedoxApplication(QuestionType):
    """Recognise redox among other reactions and in daily life, count the
    electrons a balanced equation moves, and predict whether a metal displaces."""

    def build(self, rng: Random, **params) -> GeneratedQuestion:
        shape = rng.random()
        hint = "ปฏิกิริยารีดอกซ์ต้องมีสารหนึ่งให้อิเล็กตรอนและอีกสารหนึ่งรับอิเล็กตรอนพร้อมกัน"
        if shape < 0.25:
            redox = [e for e in EQUATIONS if _reactants(e) in REDOX_REACTANTS]
            plain = [e for e in EQUATIONS if _reactants(e) in NOT_REDOX_REACTANTS]
            if rng.random() < 0.5:
                correct, wrongs, ask = rng.choice(redox), rng.sample(plain, 3), "เป็น"
            else:
                correct, wrongs, ask = rng.choice(plain), rng.sample(redox, 3), "ไม่ใช่"
            return GeneratedQuestion(
                stem=[text(f"ปฏิกิริยาในข้อใด{ask}ปฏิกิริยารีดอกซ์")],
                correct=[math(equation_tex(correct))],
                distractors=fixed(*[[math(equation_tex(w))] for w in wrongs]),
                topic=TOPIC_REDOX,
                hint=[text(hint + " ปฏิกิริยาที่เพียงสลับคู่ไอออน เช่น กรดกับเบส หรือการเกิดตะกอน ไม่ใช่รีดอกซ์")],
            )
        if shape < 0.45:
            correct = rng.choice(EVERYDAY_REDOX)
            return _labelled(
                stem="เหตุการณ์ในข้อใดเกี่ยวข้องกับปฏิกิริยารีดอกซ์",
                correct=correct, wrongs=tuple(EVERYDAY_NOT_REDOX),
                topic=TOPIC_REDOX,
                hint=hint + " การละลายและการเปลี่ยนสถานะไม่มีการถ่ายโอนอิเล็กตรอน",
            )
        if shape < 0.7:
            r = rng.choice(DISPLACEMENTS)
            answer = r.electrons
            wrongs = [answer // 2, answer * 2, answer + 1, answer - 1, answer + 2]
            return GeneratedQuestion(
                stem=[text("จากสมการที่ดุลแล้ว "), math(r.tex),
                      text(" มีการถ่ายโอนอิเล็กตรอนทั้งหมดกี่อิเล็กตรอนตามสมการ")],
                correct=[text(f"{answer} อิเล็กตรอน")],
                distractors=fixed(*[[text(f"{w} อิเล็กตรอน")] for w in wrongs if w > 0]),
                topic=TOPIC_REDOX,
                hint=[text("นับอิเล็กตรอนที่สารให้ไปทั้งหมด: จำนวนอะตอมที่ให้ × จำนวนอิเล็กตรอนที่แต่ละอะตอมให้ "
                           "ซึ่งต้องเท่ากับจำนวนที่อีกฝ่ายรับ")],
            )
        # Predict: the order of giving up electrons is stated, not assumed.
        four = sorted(rng.sample(range(len(METALS)), 4))
        order = " > ".join(METALS[i].symbol for i in four)
        i, j = rng.sample(four, 2)
        dipped, solution = METALS[i], METALS[j]
        goes = i < j
        yes = (f"เกิดปฏิกิริยา โดย{dipped.thai}ให้อิเล็กตรอนแก่ไอออนของ{solution.thai} "
               f"จึงมีโลหะ{solution.thai}มาเกาะที่แผ่นโลหะ")
        no = (f"ไม่เกิดปฏิกิริยา เพราะ{dipped.thai}ให้อิเล็กตรอนได้ยากกว่า{solution.thai}")
        wrong_way = f"เกิดปฏิกิริยา โดยไอออนของ{solution.thai}ให้อิเล็กตรอนแก่{dipped.thai}"
        if goes:
            correct = yes
            wrongs = (no, wrong_way, "ไม่เกิดปฏิกิริยา เพราะโลหะไม่ทำปฏิกิริยากับสารละลายของโลหะอื่น")
        else:
            correct = no
            wrongs = (yes, wrong_way, "ไม่เกิดปฏิกิริยา เพราะแผ่นโลหะละลายหมดก่อน")
        return _labelled(
            stem=(f"กำหนดลำดับความสามารถในการให้อิเล็กตรอนของโลหะ: {order} "
                  f"เมื่อจุ่มแผ่น{dipped.thai}ลงใน{solution.salt} ข้อใดถูกต้อง"),
            correct=correct, wrongs=wrongs,
            topic=TOPIC_REDOX,
            hint="โลหะที่ให้อิเล็กตรอนได้ง่ายกว่าจะให้อิเล็กตรอนแก่ไอออนของโลหะที่ให้อิเล็กตรอนได้ยากกว่า",
        )
