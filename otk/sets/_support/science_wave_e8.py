"""Wave E slice 8 — chemical equations and the rate of a chemical reaction.

Three core indicators under ``ว 2.1 ม.5``:

* ``ว 2.1 ม.5/20`` ระบุสูตรเคมีของสารตั้งต้น ผลิตภัณฑ์ และแปลความหมายของ
  สัญลักษณ์ในสมการเคมีของปฏิกิริยาเคมี — two free verbs joined by "และ", each
  with its own object (the formulas; the symbols), so Foundation and Fluency
  are both ``exact`` and Application is the ``standard_scope`` extension:
  writing and completing a balanced equation.
* ``ว 2.1 ม.5/21`` ทดลองและอธิบายผลของความเข้มข้น พื้นที่ผิว อุณหภูมิ และ
  ตัวเร่งปฏิกิริยาที่มีผลต่ออัตราการเกิดปฏิกิริยาเคมี — ทดลอง is done at the
  bench, not in a choice, so อธิบาย carries the record: default filing.
* ``ว 2.1 ม.5/22`` สืบค้นข้อมูลและอธิบายปัจจัยที่มีผลต่ออัตราการเกิดปฏิกิริยา
  เคมีที่ใช้ประโยชน์ในชีวิตประจำวันหรือในอุตสาหกรรม — สืบค้นข้อมูล is not
  itself assessable, so อธิบาย alone carries the record (the precedent of
  ``chem.element_use_effect``): default filing.

Written after the 2026-09-25 variety audit, which found earlier ม.5 sets a
handful of questions deep. Every set here draws from a bank of at least a
dozen real reactions or situations, and the calculating shapes draw their
numbers, so no set repeats within a sitting.
"""

from __future__ import annotations

import re
from typing import NamedTuple, Optional

from otk.core.content import text
from otk.core.distractors import label_pool
from otk.core.question import GeneratedQuestion

SUBJECT = "เคมี"
UPPER_FIVE = {"th": "ม.5"}


def _labelled(*, stem: str, correct: str, wrongs: tuple[str, ...], topic: str,
              hint: str) -> GeneratedQuestion:
    return GeneratedQuestion(
        stem=[text(stem)],
        correct=[text(correct)],
        distractors=label_pool([correct, *wrongs]),
        topic=topic,
        hint=[text(hint)],
    )


# ══ ว 2.1 ม.5/20 — the equation bank ═════════════════════════════════════════

HEAT = "heat"


class Species(NamedTuple):
    coef: int
    formula: str       # plain, e.g. "H2O" — the element counts are read off it
    state: str         # s, l, g or aq


class Equation(NamedTuple):
    reactants: tuple[Species, ...]
    products: tuple[Species, ...]
    condition: Optional[str]   # HEAT, a catalyst formula, or None
    thai: str                  # the reaction in words, states included


def _sp(coef: int, formula: str, state: str) -> Species:
    return Species(coef, formula, state)


# Every equation is real and balanced; the gate re-counts each element.
EQUATIONS: tuple[Equation, ...] = (
    Equation((_sp(2, "H2", "g"), _sp(1, "O2", "g")), (_sp(2, "H2O", "l"),), None,
             "แก๊สไฮโดรเจนทำปฏิกิริยากับแก๊สออกซิเจน ได้น้ำที่เป็นของเหลว"),
    Equation((_sp(1, "CH4", "g"), _sp(2, "O2", "g")), (_sp(1, "CO2", "g"), _sp(2, "H2O", "l")), None,
             "แก๊สมีเทนเผาไหม้ในแก๊สออกซิเจน ได้แก๊สคาร์บอนไดออกไซด์และน้ำที่เป็นของเหลว"),
    Equation((_sp(1, "Zn", "s"), _sp(2, "HCl", "aq")), (_sp(1, "ZnCl2", "aq"), _sp(1, "H2", "g")), None,
             "โลหะสังกะสีทำปฏิกิริยากับสารละลายกรดไฮโดรคลอริก ได้สารละลายซิงค์คลอไรด์และแก๊สไฮโดรเจน"),
    Equation((_sp(1, "CaCO3", "s"),), (_sp(1, "CaO", "s"), _sp(1, "CO2", "g")), HEAT,
             "เผาแคลเซียมคาร์บอเนตที่เป็นของแข็ง ได้แคลเซียมออกไซด์ที่เป็นของแข็งและแก๊สคาร์บอนไดออกไซด์"),
    Equation((_sp(1, "NaOH", "aq"), _sp(1, "HCl", "aq")), (_sp(1, "NaCl", "aq"), _sp(1, "H2O", "l")), None,
             "สารละลายโซเดียมไฮดรอกไซด์ทำปฏิกิริยากับสารละลายกรดไฮโดรคลอริก ได้สารละลายโซเดียมคลอไรด์และน้ำที่เป็นของเหลว"),
    Equation((_sp(1, "Mg", "s"), _sp(2, "HCl", "aq")), (_sp(1, "MgCl2", "aq"), _sp(1, "H2", "g")), None,
             "โลหะแมกนีเซียมทำปฏิกิริยากับสารละลายกรดไฮโดรคลอริก ได้สารละลายแมกนีเซียมคลอไรด์และแก๊สไฮโดรเจน"),
    Equation((_sp(1, "N2", "g"), _sp(3, "H2", "g")), (_sp(2, "NH3", "g"),), "Fe",
             "แก๊สไนโตรเจนทำปฏิกิริยากับแก๊สไฮโดรเจนโดยมีเหล็กเป็นตัวเร่งปฏิกิริยา ได้แก๊สแอมโมเนีย"),
    Equation((_sp(1, "C3H8", "g"), _sp(5, "O2", "g")), (_sp(3, "CO2", "g"), _sp(4, "H2O", "l")), None,
             "แก๊สโพรเพนเผาไหม้ในแก๊สออกซิเจน ได้แก๊สคาร์บอนไดออกไซด์และน้ำที่เป็นของเหลว"),
    Equation((_sp(2, "Mg", "s"), _sp(1, "O2", "g")), (_sp(2, "MgO", "s"),), HEAT,
             "เผาโลหะแมกนีเซียมในแก๊สออกซิเจน ได้แมกนีเซียมออกไซด์ที่เป็นของแข็ง"),
    Equation((_sp(1, "Fe", "s"), _sp(1, "CuSO4", "aq")), (_sp(1, "FeSO4", "aq"), _sp(1, "Cu", "s")), None,
             "โลหะเหล็กทำปฏิกิริยากับสารละลายคอปเปอร์(II)ซัลเฟต ได้สารละลายไอร์ออน(II)ซัลเฟตและโลหะทองแดง"),
    Equation((_sp(1, "AgNO3", "aq"), _sp(1, "NaCl", "aq")), (_sp(1, "AgCl", "s"), _sp(1, "NaNO3", "aq")), None,
             "สารละลายซิลเวอร์ไนเตรตทำปฏิกิริยากับสารละลายโซเดียมคลอไรด์ ได้ตะกอนซิลเวอร์คลอไรด์และสารละลายโซเดียมไนเตรต"),
    Equation((_sp(1, "CaCO3", "s"), _sp(2, "HCl", "aq")),
             (_sp(1, "CaCl2", "aq"), _sp(1, "H2O", "l"), _sp(1, "CO2", "g")), None,
             "แคลเซียมคาร์บอเนตทำปฏิกิริยากับสารละลายกรดไฮโดรคลอริก ได้สารละลายแคลเซียมคลอไรด์ น้ำที่เป็นของเหลว และแก๊สคาร์บอนไดออกไซด์"),
    Equation((_sp(2, "H2O2", "aq"),), (_sp(2, "H2O", "l"), _sp(1, "O2", "g")), "MnO2",
             "สารละลายไฮโดรเจนเพอร์ออกไซด์สลายตัวโดยมีแมงกานีส(IV)ออกไซด์เป็นตัวเร่งปฏิกิริยา ได้น้ำที่เป็นของเหลวและแก๊สออกซิเจน"),
    Equation((_sp(2, "Na", "s"), _sp(2, "H2O", "l")), (_sp(2, "NaOH", "aq"), _sp(1, "H2", "g")), None,
             "โลหะโซเดียมทำปฏิกิริยากับน้ำ ได้สารละลายโซเดียมไฮดรอกไซด์และแก๊สไฮโดรเจน"),
    Equation((_sp(2, "Al", "s"), _sp(3, "CuCl2", "aq")), (_sp(2, "AlCl3", "aq"), _sp(3, "Cu", "s")), None,
             "โลหะอะลูมิเนียมทำปฏิกิริยากับสารละลายคอปเปอร์(II)คลอไรด์ ได้สารละลายอะลูมิเนียมคลอไรด์และโลหะทองแดง"),
    Equation((_sp(1, "C2H5OH", "l"), _sp(3, "O2", "g")), (_sp(2, "CO2", "g"), _sp(3, "H2O", "l")), None,
             "เอทานอลที่เป็นของเหลวเผาไหม้ในแก๊สออกซิเจน ได้แก๊สคาร์บอนไดออกไซด์และน้ำที่เป็นของเหลว"),
    Equation((_sp(2, "SO2", "g"), _sp(1, "O2", "g")), (_sp(2, "SO3", "g"),), "V2O5",
             "แก๊สซัลเฟอร์ไดออกไซด์ทำปฏิกิริยากับแก๊สออกซิเจนโดยมีวาเนเดียม(V)ออกไซด์เป็นตัวเร่งปฏิกิริยา ได้แก๊สซัลเฟอร์ไตรออกไซด์"),
    Equation((_sp(1, "BaCl2", "aq"), _sp(1, "Na2SO4", "aq")), (_sp(1, "BaSO4", "s"), _sp(2, "NaCl", "aq")), None,
             "สารละลายแบเรียมคลอไรด์ทำปฏิกิริยากับสารละลายโซเดียมซัลเฟต ได้ตะกอนแบเรียมซัลเฟตและสารละลายโซเดียมคลอไรด์"),
)


def formula_tex(formula: str) -> str:
    return r"\mathrm{" + re.sub(r"(\d+)", r"_{\1}", formula) + "}"


def species_tex(species: Species, *, coef: Optional[str] = None, state: bool = True) -> str:
    shown = coef if coef is not None else ("" if species.coef == 1 else str(species.coef))
    tail = rf"\mathrm{{({species.state})}}" if state else ""
    return f"{shown}{formula_tex(species.formula)}{tail}"


def _arrow(condition: Optional[str]) -> str:
    if condition is None:
        return r"\longrightarrow"
    # \overset rather than \xrightarrow: the CLI's matplotlib renderer parses
    # only the former, and KaTeX draws both.
    if condition == HEAT:
        return r"\overset{\Delta}{\longrightarrow}"
    return rf"\overset{{{formula_tex(condition)}}}{{\longrightarrow}}"


def equation_tex(eq: Equation, *, reactants=None, products=None,
                 blank: Optional[Species] = None) -> str:
    """The equation as TeX; ``blank`` shows that species' coefficient as a box."""
    def side(items):
        return " + ".join(species_tex(s, coef=r"\square\," if s == blank else None)
                          for s in items)
    return f"{side(reactants or eq.reactants)} {_arrow(eq.condition)} {side(products or eq.products)}"


# ══ ว 2.1 ม.5/20 — Foundation: ระบุสูตรเคมีของสารตั้งต้นและผลิตภัณฑ์ ═══════════


# ══ ว 2.1 ม.5/20 — Fluency: แปลความหมายของสัญลักษณ์ในสมการเคมี ══════════════════


# ══ ว 2.1 ม.5/20 — Application: เขียนและดุลสมการเคมี ══════════════════════════


# ══ ว 2.1 ม.5/21 — ปัจจัยที่มีผลต่ออัตราการเกิดปฏิกิริยา ═══════════════════════

CONCENTRATION, SURFACE, TEMPERATURE, CATALYST = (
    "ความเข้มข้น", "พื้นที่ผิว", "อุณหภูมิ", "ตัวเร่งปฏิกิริยา")
FACTORS = (CONCENTRATION, SURFACE, TEMPERATURE, CATALYST)

FASTER, SLOWER = "เกิดเร็วขึ้น", "เกิดช้าลง"


# ══ ว 2.1 ม.5/22 — ปัจจัยในชีวิตประจำวันและอุตสาหกรรม ════════════════════════════


